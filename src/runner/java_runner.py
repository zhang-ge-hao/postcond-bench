#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
用 Python 驱动 Maven 对“单模块 Java 项目”执行测试与覆盖率，并汇总结果。
特性：
- 运行 `mvn test`，自动检测是否已生成 JaCoCo 报告；若没有则补跑 `mvn -q jacoco:report`
- 解析 Surefire XML，汇总用例统计与失败用例列表
- 解析 JaCoCo XML，筛出“行覆盖=100% 且 分支覆盖=100%”的源码文件
- stdout 字段：保留完整控制台输出
- test_summary 字段：对 stdout 做“去栈轨迹”的精简（仍保留 BUILD FAILURE/SUCCESS、Tests run 等关键信息）
- interrupted：尽量仅标记“初始化阶段失败”（未真正进入用例执行），对齐你原 pytest 脚本的语义
"""

import os
import re
import time
import uuid
import subprocess
import xml.etree.ElementTree as ET
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Tuple


# =========================
# 数据结构
# =========================

@dataclass
class JavaTestResult:
    failed_tests: Optional[List[str]]
    covered_files: Optional[List[str]]
    running_time: Optional[float]
    interrupted: bool
    timeout: bool
    compile_failure: bool
    reports_exist: bool
    jml_fail: bool
    cmd: str
    test_summary: Optional[str]  # 去除栈轨迹后的精简 stdout（并可拼接 XML 汇总）
    stdout: Optional[str]        # 完整 stdout

    def to_flag(self) -> str:
        if self.timeout:
            return "timeout"
        if not self.reports_exist and self.compile_failure:
            return "compile_failure"
        if not self.reports_exist:
            return "reports_not_exist"
        if self.interrupted:
            return "interrupted"
        if self.failed_tests is not None and len(self.failed_tests) == 0:
            return "passed"
        if self.jml_fail:
            return "jml_fail"
        return "failed"

    def to_string(self) -> str:
        def format_list(title: str, items: Optional[List[str]]):
            if items is None:
                return f"{title}: None"
            if len(items) == 0:
                return f"{title}: []"
            lines = [f"{title}:"]
            lines += [f"    - {x}" for x in items]
            return "\n".join(lines)

        parts = []
        parts.append("=== Java (Maven) Test Result ===")
        parts.append(format_list("Failed tests ", self.failed_tests))
        parts.append(format_list("Covered files", self.covered_files))
        parts.append(f"Running time : {self.running_time:.2f}s" if self.running_time is not None else "Running time : None")
        parts.append(f"Interrupted  : {self.interrupted}")
        parts.append(f"Timeout      : {self.timeout}")
        parts.append(f"Reports exist: {self.reports_exist}")
        parts.append(f"CMD          : \n    {self.cmd if self.cmd else 'None'}")

        # if self.test_summary:
        #     parts.append("Test Summary (stackless):")
        #     parts += [f"    {line}" for line in self.test_summary.strip().split("\n")]
        # else:
        #     parts.append("Test Summary : None")

        if self.stdout:
            output_dir = "/tmp/sb_tmp_sbout"
            os.makedirs(output_dir, exist_ok=True)
            file_path = os.path.join(output_dir, f"{uuid.uuid4().hex}.log")
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(self.stdout)
            parts.append(f"Stdout file  : {file_path}")
        else:
            parts.append("Stdout file  : None")

        return "\n".join(parts)


# =========================
# 工具函数
# =========================

def _run_cmd(args: List[str], *, env: Optional[dict] = None, timeout: Optional[float] = None) -> subprocess.CompletedProcess:
    """运行命令（非 shell），捕获 stdout+stderr 到 stdout。"""
    return subprocess.run(
        args,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        check=False,
        timeout=timeout,
        env=env,
    )


def _mvn_cmd(included_tests: Optional[List[str]], excluded_tests: Optional[List[str]]) -> List[str]:
    """
    构造 mvn test 命令（单模块）：
    - 通过 -Dtest / -DexcludedTests 进行包含/排除（逗号分隔，支持通配符）
    """
    cmd = [
        "mvn",
        "-DskipTests=false",
        "-DfailIfNoTests=false",
        "-Dsurefire.printSummary=true",
        "-DenableAssertions=true",
        "-Dcheckstyle.skip=true",
        "-Dmaven.repo.local=.m2/repository",
        "test",
    ]
    if included_tests:
        cmd.append(f"-Dtest={','.join(included_tests)}")
    if excluded_tests:
        cmd.append(f"-DexcludedTests={','.join(excluded_tests)}")
    return cmd


def _jacoco_cmd() -> List[str]:
    """
    构造 mvn test 命令（单模块）：
    - 通过 -Dtest / -DexcludedTests 进行包含/排除（逗号分隔，支持通配符）
    """
    cmd = [
        "mvn",
        "-DskipTests=false",
        "-DfailIfNoTests=false",
        "-Dsurefire.printSummary=true",
        "-DenableAssertions=true",
        "-Dcheckstyle.skip=true",
        "-Dmaven.repo.local=.m2/repository",
        "-q", "jacoco:report",
    ]
    return cmd


def _collect_maven_summary_from_xml(surefire_dir: Path) -> Tuple[str, List[str]]:
    """
    扫描 target/surefire-reports/*.xml，汇总总数与失败的 nodeid（classname#method）。
    """
    if not surefire_dir.exists():
        return ("", [])
    total_tests = total_failures = total_errors = total_skipped = 0
    failed: List[str] = []

    for xml_path in surefire_dir.glob("*.xml"):
        try:
            tree = ET.parse(xml_path)
            root = tree.getroot()
        except Exception:
            continue

        ts_tests = int(root.get("tests", "0"))
        ts_fail = int(root.get("failures", "0"))
        ts_err = int(root.get("errors", "0"))
        ts_skip = int(root.get("skipped", root.get("disabled", "0")))

        total_tests += ts_tests
        total_failures += ts_fail
        total_errors += ts_err
        total_skipped += ts_skip

        for case in root.findall(".//testcase"):
            classname = case.get("classname", "")
            name = case.get("name", "")
            nodeid = f"{classname}#{name}" if classname else name
            if case.find("failure") is not None or case.find("error") is not None:
                failed.append(nodeid)

    summary = f"Tests run: {total_tests}, Failures: {total_failures}, Errors: {total_errors}, Skipped: {total_skipped}"
    return (summary, failed)


def extract_well_covered_filenames_jacoco(jacoco_xml_path: Path) -> List[str]:
    """
    读取 target/site/jacoco/jacoco.xml，筛出“行覆盖=100% 且 分支覆盖=100%”的源文件路径。
    - JaCoCo: <package> -> <class sourcefilename="..."> -> <counter type="LINE/BRANCH" missed=".." covered="..">
    - 过滤测试文件（文件名包含 Test 或以 test.java 结尾）
    - 输出相对路径：默认拼为 src/main/java/<pkg_path>/<sourcefilename>
    """
    if not jacoco_xml_path.exists():
        return []
    try:
        tree = ET.parse(jacoco_xml_path)
        root = tree.getroot()
    except Exception:
        return []

    results: List[str] = []
    for pkg in root.findall(".//package"):
        pkg_name = pkg.get("name", "").strip("/")
        for cls in pkg.findall("class"):
            source_filename = cls.get("sourcefilename", "")

            counters = {c.get("type"): c for c in cls.findall("counter")}
            def full_covered(kind: str) -> bool:
                c = counters.get(kind)
                if c is None:
                    return False
                missed = int(c.get("missed", "0"))
                covered = int(c.get("covered", "0"))
                return missed == 0 and covered > 0

            if not (full_covered("LINE") and full_covered("BRANCH")):
                continue
            if "Test" in source_filename or source_filename.lower().endswith("test.java"):
                continue

            rel_path = Path("src/main/java") / (pkg_name.replace(".", "/")) / source_filename
            results.append(str(rel_path))

    return sorted(set(results))


def _ensure_jacoco_report(env: dict) -> Tuple[Path, str]:
    """
    确保 jacoco.xml 存在：
    - 若 target/site/jacoco/jacoco.xml 已存在，直接返回；
    - 否则尝试执行 `mvn -q jacoco:report` 生成；
    返回 (jacoco_xml_path, stdout_append)
    """
    jacoco_xml = Path("target/site/jacoco/jacoco.xml")
    if jacoco_xml.exists():
        return jacoco_xml, ""
    cp = _run_cmd(_jacoco_cmd(), env=env, timeout=None)
    return jacoco_xml, (cp.stdout or "")


# ---------- 中断判定（更贴近“初始化阶段失败”） ----------

def _infer_interrupted(returncode: int, surefire_dir: Path, stdout: str) -> bool:
    """
    仅在“未进入用例执行阶段的失败”时返回 True：
    - 若已经产出 surefire XML，则认为已进入测试阶段，不算中断
    - 若 stdout 出现典型的编译/插件/启动失败关键词且 returncode!=0，则算中断
    - 若 returncode!=0 且没有 XML，兜底认为中断
    - returncode==0 且无 XML（且 failIfNoTests=false）时，不算中断
    """
    xmls = list(surefire_dir.glob("*.xml"))
    has_xml = len(xmls) > 0
    out = stdout or ""

    if has_xml:
        return False
    if "There are test failures." in out:
        return False

    error_markers = (
        "COMPILATION ERROR",
        "Failed to execute goal org.apache.maven.plugins:maven-compiler-plugin",
        "Failed to execute goal org.apache.maven.plugins:maven-surefire-plugin",
        "Error occurred in starting fork",
        "java.lang.NoClassDefFoundError",
        "Plugin org.apache.maven.plugins:maven-surefire-plugin",
        "BUILD FAILURE",
    )
    if returncode != 0 and any(tok in out for tok in error_markers):
        return True
    if returncode != 0 and not has_xml:
        return True
    return False


# ---------- 去栈轨迹的 stdout 摘要 ----------

_STACK_LINE_RE = re.compile(
    r'^\s*(?:at\b\s+)+'              # 一个或多个 "at"
    r'(?:[\w.@+\-]+/)?'              # 可选的 模块 或 模块@版本（含 . @ + -），后接 /
    r'[\w.$_]+(?:<init>)?'           # 类.方法 或 类.<init>
    r'\([^)]*\)\s*$'                 # 括号里的源码位置/Native/Unknown 等
)
_ELIDED_RE     = re.compile(r'^\s*\.\.\.\s+\d+\s+more\s*$')
_CAUSED_BY_RE  = re.compile(r'^\s*Caused by:\s+')
_SUPPRESSED_RE = re.compile(r'^\s*Suppressed:\s+')
_SUREFIRE_HDR  = re.compile(r'^\[ERROR\]\s+Tests run:|^\[INFO\]\s+Results:')
_PROGRESS_NOISE= re.compile(r'^\[INFO\]\s*(Downloading|Downloaded|Uploading|Uploaded)\s')
_PLUGIN_LINE   = re.compile(r'^\[ERROR\]\s+Failed to execute goal\b')

def _summarize_maven_stdout(stdout: str) -> str:
    """
    生成“去掉所有堆栈”的精简版 maven 控制台输出：
    - 移除 Java 栈轨迹块（以 'at ' 开头，Caused by, Suppressed, '... N more'）
    - 移除 surefire 失败详情中的堆栈
    - 保留 BUILD FAILURE/ SUCCESS、Tests run 汇总、Failed to execute goal 等关键信息
    - 去掉下载/上传噪声；折叠多余空行
    """
    if not stdout:
        return ""

    lines = stdout.splitlines()
    out_lines: List[str] = []

    def begins_stack(l: str) -> bool:
        return (
            _STACK_LINE_RE.match(l) is not None
            or _CAUSED_BY_RE.match(l) is not None
            or _SUPPRESSED_RE.match(l) is not None
            or _ELIDED_RE.match(l) is not None
        )

    i = 0
    while i < len(lines):
        l = lines[i]

        # 噪声：依赖下载/上传进度
        if _PROGRESS_NOISE.match(l):
            i += 1
            continue

        # 发现堆栈开始：跳过直至遇到“非栈轨迹”行（空行也跳过）
        if begins_stack(l):
            i += 1
            while i < len(lines) and (begins_stack(lines[i]) or lines[i].strip() == ""):
                i += 1
            # # 保留一个空行作为分隔（可选）
            # if out_lines and out_lines[-1].strip() != "":
            #     out_lines.append("...")
            continue

        # surefire 报错段落里，header 后紧跟的堆栈也剔除
        if _SUREFIRE_HDR.match(l) or _PLUGIN_LINE.match(l):
            out_lines.append(l)
            i += 1
            # 向后看若是堆栈则整块跳过
            while i < len(lines) and begins_stack(lines[i]):
                i += 1
            continue

        out_lines.append(l)
        i += 1

    # 折叠多余空行 & 去掉收尾空行
    compact: List[str] = []
    for l in out_lines:
        if l.strip() == "":
            if compact and compact[-1].strip() == "":
                continue
        compact.append(l)
    while compact and compact[0].strip() == "":
        compact.pop(0)
    while compact and compact[-1].strip() == "":
        compact.pop()

    return "\n".join(compact)


def is_java_compile_failure(log_text: str) -> bool:
    """
    仅判断是否为 javac 编译失败（不区分测试失败/其它失败）。
    用法：
        with open("build.log", "r", encoding="utf-8", errors="ignore") as f:
            print(is_java_compile_failure(f.read()))
    """
    flags = re.IGNORECASE | re.MULTILINE | re.DOTALL
    patterns = [
        # 典型：compiler 插件直接宣判编译失败/致命编译错误
        r"Failed to execute goal .*maven-compiler-plugin:[^:]+:(?:compile|testCompile).*?(?:Compilation failure|Fatal error compiling)",
        # 旧式标题
        r"\bCOMPILATION ERROR(?:S)?\b",
        # Maven 标准错误行：.../X.java:[行,列] ...
        r"^\[ERROR\]\s+.+\.java:(?:\[\d+,\d+\]|\d+:)\s",
        # javac 常见错误关键词（有些环境会去掉前缀）
        r"^\s*error:\s+.+",
        r"\bcannot find symbol\b",
        r"\bincompatible types\b",
        r"\bpackage\s+[a-zA-Z0-9_.]+\s+does not exist\b",
    ]
    return any(re.search(p, log_text, flags) for p in patterns)

# =========================
# 主流程
# =========================

def java_testsuite_run(
    included_tests: Optional[List[str]] = None,
    excluded_tests: Optional[List[str]] = None,
    timeout: Optional[float] = None,
    require_not_interrupted: bool = False,
    replace_file_path: Optional[str] = None,
    replace_file_content: Optional[str] = None,
    # just for keep the same API with python. acturally ignored 
    require_local_crash: bool = False,
    local_crash_line_range=None,
    # just for keep the same API with python. acturally ignored 
    target_method = None,
    need_coverage=False
) -> JavaTestResult:
    """
    执行 mvn test（单模块），并生成测试/覆盖率汇总。
    - included_tests / excluded_tests 传入 surefire 的 -Dtest / -DexcludedTests
      例：included_tests=["MyClassTest","OtherTest#methodA","**/IT*"]
    - 超时为整体 mvn test 的超时（秒）
    - replace_file_*：测试前临时替换某文件内容，收尾恢复
    """

    # 可选的临时替换文件
    if replace_file_path is not None and replace_file_content is not None:
        with open(replace_file_path, "r", encoding="utf-8", errors="ignore") as f:
            ori_file_content = f.read()
        with open(replace_file_path, "w", encoding="utf-8") as f:
            f.write(replace_file_content)

    extra_cmds: List[str] = []
    try:
        env = os.environ.copy()
        env["JAVA_HOME"] = "/usr"
        env["PATH"] = ":".join([
            "/usr/local/sbin", "/usr/local/bin", "/usr/sbin", "/usr/bin", "/sbin", "/bin",
            env.get("PATH", "")
        ])
        env["HOME"] = os.path.join(Path.cwd(), ".home")

        surefire_dir = Path("target/surefire-reports")
        jacoco_xml_path = Path("target/site/jacoco/jacoco.xml")

        # 清理旧 XML（可选）
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

        # 1) mvn test
        test_cmd = _mvn_cmd(included_tests, excluded_tests)
        extra_cmds.append(" ".join(test_cmd))
        start = time.time()
        cp_test = _run_cmd(test_cmd, env=env, timeout=timeout)
        stdout_test = cp_test.stdout or ""

        # 2) 确保 jacoco.xml 存在（若已在 pom 绑定则此时已存在；否则尝试补跑 jacoco:report）
        jacoco_xml, stdout_after = _ensure_jacoco_report(env)
        if stdout_after:
            extra_cmds.append(" ".join(_jacoco_cmd()))

        end = time.time()
        total_time = end - start

        # 解析 surefire
        summary_by_xml, failed = _collect_maven_summary_from_xml(surefire_dir)

        # 完整 stdout
        combined_stdout = (stdout_test + ("\n\n" + stdout_after if stdout_after else "")).strip()

        logging.info(f"\n{combined_stdout}")

        # 摘要（去堆栈），并把 XML 的总览拼到开头，辅助快速定位
        test_summary_stackless = _summarize_maven_stdout(combined_stdout)
        if summary_by_xml:
            test_summary = summary_by_xml + ("\n" + test_summary_stackless if test_summary_stackless else "")
        else:
            test_summary = test_summary_stackless

        jml_fail = "JML Post-condtion Failed" in combined_stdout

        interrupted = _infer_interrupted(cp_test.returncode, surefire_dir, stdout_test)
        covered_files = extract_well_covered_filenames_jacoco(jacoco_xml) if jacoco_xml.exists() else None
        reports_exist = surefire_dir.exists() and any(surefire_dir.glob("*.xml")) and jacoco_xml.exists()
        compile_failure = is_java_compile_failure(combined_stdout)

        result = JavaTestResult(
            failed_tests=failed if failed is not None else None,
            covered_files=covered_files,
            running_time=total_time,
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
            covered_files=None,
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
        if replace_file_path is not None and replace_file_content is not None:
            with open(replace_file_path, "w", encoding="utf-8") as f:
                f.write(ori_file_content)

    if require_not_interrupted:
        if result.interrupted:
            raise RuntimeError(f"test suite run interrupted:\n{result.to_string()}")
        if result.failed_tests is None:
            raise RuntimeError("not interrupted but failed tests is None:\n" + result.to_string())

    return result
