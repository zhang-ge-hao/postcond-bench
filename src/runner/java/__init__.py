
from typing import *
import subprocess
from pathlib import Path
import os
import logging
import time

from .ds import JavaTestResult
from .env import _get_env
from .cmd import (
    _mvn_cmd,
    _jacoco_cmd,
    _run_cmd,
    _build_java_cmd,
)
from .surefire import _collect_maven_summary_from_xml
from .mvn import (
    _summarize_maven_stdout,
    _is_java_compile_failure,
    _infer_interrupted,
)
from .fat import (
    _ensure_fatjar,
    _extract_jacoco_agent_in_target,
    _prepare_override_sources_and_compile,
    _infer_interrupted_fat
)

def java_testsuite_run(
    included_tests: Optional[List[str]] = None,
    excluded_tests: Optional[List[str]] = None,
    timeout: Optional[float] = None,
    require_not_interrupted: bool = False,
    replace_file_path: Optional[str] = None,
    replace_file_content: Optional[str] = None,
    fatjar_mode: bool = True,
    **kwargs
) -> JavaTestResult:

    extra_cmds: List[str] = []
    try:
        env = _get_env()

        project_root = Path(".").resolve()
        target_dir = project_root / "target"
        surefire_dir = project_root / "target/surefire-reports"
        jacoco_xml_path = project_root / "target/site/jacoco/jacoco.xml"

        if not fatjar_mode:
            if replace_file_path is not None and replace_file_content is not None:
                with open(replace_file_path, "r", encoding="utf-8", errors="ignore") as f:
                    ori_file_content = f.read()
                with open(replace_file_path, "w", encoding="utf-8") as f:
                    f.write(replace_file_content)
        else:
            # 0) 确保 target 目录存在
            target_dir.mkdir(exist_ok=True)

            # 1) 确保 fatjar 存在
            fatjar_path, build_stdout = _ensure_fatjar(
                project_root, env)
            
            if fatjar_path is None or not fatjar_path.exists():
                # 构建失败
                combined = build_stdout
                result = JavaTestResult(
                    failed_tests=None,
                    running_time=None,
                    interrupted=True,
                    timeout=False,
                    compile_failure=_is_java_compile_failure(build_stdout),
                    reports_exist=False,
                    jml_fail=("JML Post-condition Failed" in build_stdout),
                    cmd="mvn -DskipTests clean com.example:fat-test-maven-plugin:0.1.0:build",
                    test_summary=_summarize_maven_stdout(build_stdout),
                    stdout=combined,
                )
                if require_not_interrupted:
                    raise RuntimeError("fatjar build interrupted or missing:\n" + result.to_string())
                return result
            ok, extract_stdout = _extract_jacoco_agent_in_target(project_root, str(fatjar_path), env)
            extra_cmds.append(f"jar xf {fatjar_path} META-INF/fattest/jacoco-agent.jar")
            # 即使解包失败，后面 java -javaagent 会直接报错；由中断判定兜底

            # 3) （可选）单文件编译覆盖
            overrides_dir: Optional[Path] = None
            if replace_file_path is not None and replace_file_content is not None:
                overrides_dir, javac_stdout, compile_failure = _prepare_override_sources_and_compile(
                    project_root, str(fatjar_path), replace_file_path, replace_file_content, env
                )
                extra_cmds.append(f"javac -encoding UTF-8 -cp {fatjar_path} -d fattest-overrides <{replace_file_path}>")
                if compile_failure:
                    # 单文件编译失败，直接返回（对齐原版 compile_failure 语义）
                    combined = "\n\n".join(
                        [s for s in [build_stdout, extract_stdout, javac_stdout] if s]
                    ).strip()
                    result = JavaTestResult(
                        failed_tests=None,
                        running_time=None,
                        interrupted=True,          # 认为未进入测试阶段
                        timeout=False,
                        compile_failure=True,
                        reports_exist=False,
                        jml_fail=("JML Post-condition Failed" in combined),
                        cmd=" && ".join(extra_cmds),
                        test_summary=_summarize_maven_stdout(combined),
                        stdout=combined,
                    )
                    if require_not_interrupted:
                        raise RuntimeError("javac single-file compile failed:\n" + result.to_string())
                    return result
            else:
                javac_stdout = ""

        # 清理旧 XML
        try:
            if surefire_dir.exists():
                for f in surefire_dir.glob("*.xml"):
                    f.unlink(missing_ok=True)
        except Exception:
            pass
        try:
            if jacoco_xml_path.exists():
                jacoco_xml_path.unlink(missing_ok=True)
        except Exception:
            pass

        if not fatjar_mode:
            # 1) mvn test
            test_cmd = _mvn_cmd(included_tests, excluded_tests)
            extra_cmds.append(" ".join(test_cmd))
            start = time.time()
            cp_test = _run_cmd(test_cmd, env=env, timeout=timeout)
            stdout_test = cp_test.stdout or ""
            # 2) 确保 jacoco.xml 存在（若已在 pom 绑定则此时已存在；否则尝试补跑 jacoco:report）
            stdout_after = None
            if not jacoco_xml_path.exists():
                cp = _run_cmd(_jacoco_cmd(), env=env, timeout=None)
                stdout_after = cp.stdout or ""
            end = time.time()
            running_time = end - start
            if stdout_after:
                extra_cmds.append(" ".join(_jacoco_cmd()))
            combined_stdout = (stdout_test + ("\n\n" + stdout_after if stdout_after else "")).strip()
            reports_exist = surefire_dir.exists() and any(surefire_dir.glob("*.xml")) and jacoco_xml_path.exists()
            interrupted = _infer_interrupted(cp_test.returncode, surefire_dir, stdout_test)
        else:
            # 构造 java 命令
            java_cmd = _build_java_cmd(str(fatjar_path), overrides_dir, included_tests, excluded_tests)
            extra_cmds.append(" ".join(java_cmd))

            start = time.time()
            cp_java = _run_cmd(java_cmd, env=env, timeout=timeout)
            end = time.time()
            running_time = end - start
            java_stdout = cp_java.stdout or ""
            combined_stdout = "\n\n".join(
                [s for s in [build_stdout, extract_stdout, javac_stdout, java_stdout] if s]
            ).strip()
            reports_exist = surefire_dir.exists() and any(surefire_dir.glob("*.xml")) and jacoco_xml_path.exists()
            interrupted = _infer_interrupted_fat(cp_java.returncode, reports_exist, java_stdout)
        # logging.info(f"\n{combined_stdout}")

        # 解析 surefire
        summary_by_xml, failed = _collect_maven_summary_from_xml(surefire_dir)        

        # 摘要（去堆栈），并把 XML 的总览拼到开头，辅助快速定位
        test_summary_stackless = _summarize_maven_stdout(combined_stdout)
        if summary_by_xml:
            test_summary = summary_by_xml + ("\n" + test_summary_stackless if test_summary_stackless else "")
        else:
            test_summary = test_summary_stackless

        jml_fail = "JML Post-condition Failed" in combined_stdout
        compile_failure = _is_java_compile_failure(combined_stdout)

        result = JavaTestResult(
            failed_tests=failed if failed is not None else None,
            running_time=running_time,
            interrupted=interrupted,
            timeout=False,
            compile_failure=compile_failure,
            reports_exist=reports_exist,
            jml_fail=jml_fail,
            cmd=" && ".join(extra_cmds),
            test_summary=test_summary,
            stdout=combined_stdout,
        )

    except subprocess.TimeoutExpired:
        result = JavaTestResult(
            failed_tests=None,
            running_time=None,
            interrupted=True,
            timeout=True,
            compile_failure=None,
            reports_exist=False,
            jml_fail=None,
            cmd="mvn test (timeout)",
            test_summary=None,
            stdout=None,
        )

    finally:
        # 还原临时替换文件
        if not fatjar_mode:
            if replace_file_path is not None and replace_file_content is not None:
                with open(replace_file_path, "w", encoding="utf-8") as f:
                    f.write(ori_file_content)

    if require_not_interrupted:
        if result.interrupted:
            cmds = '\n'.join(extra_cmds)
            raise RuntimeError(f"test suite run interrupted:\n{result.to_string()}\n\n{cmds}")
        if result.failed_tests is None:
            raise RuntimeError("not interrupted but failed tests is None:\n" + result.to_string())

    return result