#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
使用 fat tests JAR 加速单模块 Maven 项目的测试执行与覆盖率收集。
与原先“直接跑 mvn test”的 runner 对比：
- 如 target/*-fat-tests.jar 不存在，则先执行：
    mvn -DskipTests clean com.example:fat-test-maven-plugin:0.1.0:build
- 进入 target/，解出 JaCoCo agent：
    jar xf *-fat-tests.jar META-INF/fattest/jacoco-agent.jar
- （可选）仅对一个源码文件做替换式编译：
    javac -encoding UTF-8 -cp *-fat-tests.jar -d target/fattest-overrides <临时源码副本路径>
- 运行测试（fatjar 中的主类：com.example.fatrunner.Main）：
    java -ea \
         [-Dtest=...] [-DexcludedTests=...] \
         -javaagent:META-INF/fattest/jacoco-agent.jar=destfile=jacoco.exec,output=file,append=false,dumponexit=true \
         -cp target/fattest-overrides:* -fat-tests.jar \
         com.example.fatrunner.Main
- 解析 target/fat-tests-report.txt：
    == Test Cases ==
    <class#method> => PASS/FAIL/ERROR/SKIPPED
    ...
    == Well Covered Files ==
    <path/under/src>
    ...

对外 API（避免与旧实现同名）：
- Dataclass: FatJarTestResult
- Function : fatjar_testsuite_run(...)
    参数保持与旧版基本一致：included_tests / excluded_tests / timeout / require_not_interrupted /
    replace_file_path / replace_file_content / require_local_crash / target_method（后两者占位，不实际使用）
"""

import os
import re
import time
import uuid
import glob
import shutil
import subprocess
import xml.etree.ElementTree as ET  # 仅为兼容导入，未实际使用 XML 解析
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Tuple


# =========================
# 数据结构
# =========================

@dataclass
class FatJarTestResult:
    failed_tests: Optional[List[str]]
    covered_files: Optional[List[str]] # 实际上是 covered methods
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
        parts.append("=== Java (Fat-Jar) Test Result ===")
        parts.append(format_list("Failed tests ", self.failed_tests))
        parts.append(format_list("Covered methods", self.covered_files))
        parts.append(f"Running time : {self.running_time:.2f}s" if self.running_time is not None else "Running time : None")
        parts.append(f"Interrupted  : {self.interrupted}")
        parts.append(f"Timeout      : {self.timeout}")
        parts.append(f"Reports exist: {self.reports_exist}")
        parts.append(f"CMD          : \n    {self.cmd if self.cmd else 'None'}")

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

def _run_cmd(args: List[str], *, env: Optional[dict] = None, timeout: Optional[float] = None, cwd: Optional[str] = None) -> subprocess.CompletedProcess:
    """运行命令（非 shell），捕获 stdout+stderr 到 stdout。"""
    return subprocess.run(
        args,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        check=False,
        timeout=timeout,
        env=env,
        cwd=cwd,
    )


def _find_fatjar_in_target(target_dir: Path) -> Optional[Path]:
    """在 target/ 下寻找 *-fat-tests.jar，若有多个取修改时间最新的。"""
    candidates = list(target_dir.glob("*-fat-tests.jar"))
    if not candidates:
        return None
    candidates.sort(key=lambda p: p.stat().st_mtime, reverse=True)
    return candidates[0]


def _ensure_fatjar(project_root: Path, env: dict) -> Tuple[Optional[Path], str]:
    """
    确保 target 下存在 *-fat-tests.jar；若没有则执行构建插件。
    返回 (fatjar_path, stdout_of_build)
    """
    target_dir = project_root / "target"
    fatjar = _find_fatjar_in_target(target_dir)
    if fatjar and fatjar.exists():
        return fatjar, ""

    shutil.rmtree(".m2", ignore_errors=True)
    pi_worldir = os.getenv("PI_WORKDIR", "/tmp")
    if os.path.exists(f"{pi_worldir}/.m2"):
        shutil.copytree(f"{pi_worldir}/.m2", ".m2")

    build_cmd = [
        "mvn",
        "-DskipTests",
        "-Dmaven.repo.local=.m2/repository",
        "clean",
        "com.example:fat-test-maven-plugin:0.1.0:build",
    ]
    cp = _run_cmd(build_cmd, env=env, timeout=None, cwd=str(project_root))
    # 构建后再找一次
    fatjar = _find_fatjar_in_target(target_dir)
    return fatjar, (cp.stdout or "")


def _extract_jacoco_agent_in_target(target_dir: Path, fatjar_name: str, env: dict) -> Tuple[bool, str]:
    """
    在 target/ 内执行：
        jar xf <fatjar> META-INF/fattest/jacoco-agent.jar
    返回 (是否存在, stdout)
    """
    agent_rel = Path("META-INF/fattest/jacoco-agent.jar")
    agent_abs = target_dir / agent_rel
    if agent_abs.exists():
        return True, ""

    cp = _run_cmd(
        ["jar", "xf", fatjar_name, str(agent_rel).replace("\\", "/")],
        env=env, timeout=None, cwd=str(target_dir)
    )
    return agent_abs.exists(), (cp.stdout or "")


def _prepare_override_sources_and_compile(project_root: Path, fatjar: Path, replace_file_path: str, replace_file_content: str, env: dict) -> Tuple[Optional[Path], str, bool]:
    """
    将要替换的源码文件编译到 target/fattest-overrides/，仅编译这一个文件。
    - 在 target/fattest-src-tmp/ 下按原路径结构写入“临时源码副本”（不改动仓库文件）
    - javac -encoding UTF-8 -cp <fatjar> -d target/fattest-overrides <tmp_src>
    返回 (overrides_dir, stdout, compile_failed)
    """
    if not replace_file_path or replace_file_content is None:
        return None, "", False

    target_dir = project_root / "target"
    src_tmp_root = target_dir / "fattest-src-tmp"
    overrides_dir = target_dir / "fattest-overrides"

    # 清理并重建
    try:
        if src_tmp_root.exists():
            shutil.rmtree(src_tmp_root)
        if overrides_dir.exists():
            shutil.rmtree(overrides_dir)
    except Exception:
        pass
    src_tmp_root.mkdir(parents=True, exist_ok=True)
    overrides_dir.mkdir(parents=True, exist_ok=True)

    # 在 tmp 根下复刻原路径写入内容
    # replace_file_path 通常是仓库根的相对路径（如 src/main/java/.../Foo.java）
    rel_path = Path(replace_file_path)
    tmp_src_path = src_tmp_root / rel_path
    tmp_src_path.parent.mkdir(parents=True, exist_ok=True)
    with open(tmp_src_path, "w", encoding="utf-8") as f:
        f.write(replace_file_content)

    # 编译
    cp = _run_cmd(
        [
            "javac",
            "-encoding", "UTF-8",
            "-cp", str(fatjar.name),
            "-d", str(overrides_dir),
            str(tmp_src_path),
        ],
        env=env, timeout=None, cwd=str(target_dir)
    )
    stdout = cp.stdout or ""
    compile_failed = (cp.returncode != 0) or is_java_compile_failure(stdout)
    return overrides_dir if not compile_failed else None, stdout, compile_failed


def _build_java_cmd(fatjar_name: str, overrides_dir: Optional[Path],
                    included_tests: Optional[List[str]], excluded_tests: Optional[List[str]]) -> List[str]:
    """
    构造 java 命令列表（在 target/ 下执行）。
    -Dtest / -DexcludedTests 以逗号分隔
    -cp: overrides_dir（若有）放在前面，然后 fatjar
    """
    java_cmd = [
        "java",
        "-ea",
        # JaCoCo agent
        "-javaagent:META-INF/fattest/jacoco-agent.jar=destfile=jacoco.exec,output=file,append=false,dumponexit=true",
    ]
    if included_tests:
        java_cmd.append(f"-Dtest={','.join(included_tests)}")
    if excluded_tests:
        java_cmd.append(f"-DexcludedTests={','.join(excluded_tests)}")

    # classpath
    cp_elems = []
    if overrides_dir:
        cp_elems.append(str(overrides_dir))
    cp_elems.append(fatjar_name)
    java_cmd += ["-cp", os.pathsep.join(cp_elems)]

    # Main
    java_cmd.append("com.example.fatrunner.Main")
    return java_cmd


def _resolve_well_covered_paths(project_root: Path, items: List[str]) -> List[str]:
    """
    将 WellCoveredMethods 的每行 'relPath#methodDisplay [Lfirst-last]' 中的 relPath
    解析为【相对项目根】的真实路径，并替换回原行。解析失败的行会被丢弃。

    匹配策略（与旧版文件解析一致 + 兼容）：
      1) 先尝试常见源码根前缀：src/main/{java,kotlin,scala}、src/
      2) 若 relPath 本身已含 src/... 前缀，直接按 project_root/s 拼接检查
      3) 受控遍历项目源码（跳过 target/build/out/node_modules/.git 等），
         用“POSIX 路径后缀匹配”进行兜底

    返回：形如 '<project-rel-path>#methodDisplay [Lfirst-last]' 的列表
    """
    # 解析一行，拆出 relPath 与尾部（#method...）
    line_re = re.compile(
        r"^(?P<rel>.+?)#(?P<rest>.+?)\s*\[L(?P<first>\d+)-(?P<last>\d+)\]\s*$"
    )

    def _norm_posix(p: Path) -> str:
        return p.as_posix()

    # 先把输入解析成 (orig, rel, tail)；tail 以 '#...' 开头，包含 '[Lx-y]'
    parsed: List[tuple[str, str, str]] = []
    for raw in items:
        if not raw or not raw.strip():
            continue
        s = raw.strip()
        m = line_re.match(s)
        if not m:
            # 不符合新格式就跳过
            continue
        rel = m.group("rel").strip().lstrip("./").replace("\\", "/")
        # 恢复尾巴，保留原有空白格式（这里统一成 '#{rest} [Lfirst-last]'）
        tail = f"#{m.group('rest').strip()} [L{m.group('first')}-{m.group('last')}]"
        parsed.append((raw, rel, tail))

    if not parsed:
        return []

    # 常见源码根
    common_roots = [
        project_root / "src" / "main" / "java",
        project_root / "src" / "main" / "kotlin",
        project_root / "src" / "main" / "scala",
        project_root / "src",          # 有的项目直接 src/net/...
        project_root,                  # 极少数直接放在根
    ]

    # 第一次快速命中（不做全盘遍历）
    fast_hits: dict[str, Path] = {}
    for _, rel, _ in parsed:
        hit: Optional[Path] = None
        for base in common_roots:
            cand = base / Path(rel)
            if cand.exists() and cand.is_file():
                hit = cand
                break
        if hit is None and rel.startswith("src/"):
            cand2 = project_root / rel
            if cand2.exists() and cand2.is_file():
                hit = cand2
        if hit is not None:
            fast_hits[rel] = hit

    # 需要兜底遍历的项
    remain = [rel for _, rel, _ in parsed if rel not in fast_hits]

    # 受控遍历：收集源码文件池
    exclude_dirs = {
        ".git", ".hg", ".svn", ".idea", ".vscode",
        "target", "build", "out", "node_modules", ".gradle", ".mvn"
    }
    source_exts = (".java", ".kt", ".kts", ".scala")
    all_source_files: list[Path] = []
    if remain:
        for root, dirs, files in os.walk(project_root):
            # 目录剪枝
            dirs[:] = [d for d in dirs if d not in exclude_dirs]
            for fn in files:
                if fn.endswith(source_exts):
                    all_source_files.append(Path(root) / fn)

        # 用“路径后缀匹配”做兜底解析
        for rel in remain:
            rel_posix = rel  # 已经是 POSIX
            best: Optional[Path] = None
            for f in all_source_files:
                f_posix = _norm_posix(f)
                if f_posix.endswith("/" + rel_posix) or f_posix.endswith(rel_posix):
                    best = f
                    break
            if best is not None:
                fast_hits[rel] = best

    # 组装输出：把命中的 rel 替换为相对项目根路径；未命中的行丢弃
    out: List[str] = []
    seen: set[str] = set()  # 去重：基于整行
    for _, rel, tail in parsed:
        hit = fast_hits.get(rel)
        if not hit:
            continue
        rel_from_project = _norm_posix(hit.relative_to(project_root))
        line = f"{rel_from_project}{tail}"
        if line not in seen:
            seen.add(line)
            out.append(line)

    return out


def _parse_fat_report(report_path: Path) -> Tuple[List[str], List[str], Tuple[int, int, int, int]]:
    """
    解析 fat-tests-report.txt：
      - 返回 (failed_tests, covered_files, (total, failures, errors, skipped))
    """
    if not report_path.exists():
        return [], [], (0, 0, 0, 0)

    with open(report_path, "r", encoding="utf-8", errors="ignore") as f:
        lines = [ln.rstrip("\n") for ln in f]

    in_cases = in_cov = False
    failed: List[str] = []
    covered: List[str] = []

    total = failures = errors = skipped = 0

    for ln in lines:
        if ln.strip() == "== Test Cases ==":
            in_cases, in_cov = True, False
            continue
        if ln.strip() == "== Well Covered Methods ==":
            in_cases, in_cov = False, True
            continue
        if ln.strip().startswith("=="):
            in_cases = in_cov = False
            continue

        if in_cases:
            # 形如：pkg.Class#method => PASS
            m = re.match(r"^(?P<id>.+?)\s*=>\s*(?P<st>[A-Z]+)\s*$", ln.strip())
            if not m:
                continue
            nodeid = m.group("id").strip()
            st = m.group("st").strip().upper()
            total += 1
            if st == "PASS":
                pass
            elif st in ("FAIL", "FAILED"):
                failures += 1
                failed.append(nodeid)
            elif st in ("ERROR",):
                errors += 1
                failed.append(nodeid)
            elif st in ("SKIPPED", "IGNORE", "IGNORED"):
                skipped += 1
            else:
                # 未知状态计为失败
                failures += 1
                failed.append(nodeid)

        if in_cov:
            s = ln.strip()
            if s:
                covered.append(s)

    return failed, covered, (total, failures, errors, skipped)


# ---------- 去栈轨迹的 stdout 摘要（沿用原 runner 的逻辑） ----------

_STACK_LINE_RE = re.compile(
    r'^\s*(?:at\b\s+)+'              # 一个或多个 "at"
    r'(?:[\w.@+\-]+/)?'              # 可选 module 或 module@version
    r'[\w.$_]+(?:<init>)?'           # 类.方法 或 类.<init>
    r'\([^)]*\)\s*$'                 # 括号中的位置说明
)
_ELIDED_RE     = re.compile(r'^\s*\.\.\.\s+\d+\s+more\s*$')
_CAUSED_BY_RE  = re.compile(r'^\s*Caused by:\s+')
_SUPPRESSED_RE = re.compile(r'^\s*Suppressed:\s+')
_PROGRESS_NOISE= re.compile(r'^\[INFO\]\s*(Downloading|Downloaded|Uploading|Uploaded)\s')  # 主要对 mvn 输出有效
_PLUGIN_LINE   = re.compile(r'^\[ERROR\]\s+Failed to execute goal\b')

def _summarize_stdout(stdout: str) -> str:
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

        # 噪声：依赖下载/上传进度（mvn 构建时可能出现）
        if _PROGRESS_NOISE.match(l):
            i += 1
            continue

        # 开始堆栈
        if begins_stack(l):
            i += 1
            while i < len(lines) and (begins_stack(lines[i]) or lines[i].strip() == ""):
                i += 1
            continue

        # mvn 插件失败行（若走了构建）
        if _PLUGIN_LINE.match(l):
            out_lines.append(l)
            i += 1
            while i < len(lines) and begins_stack(lines[i]):
                i += 1
            continue

        out_lines.append(l)
        i += 1

    # 折叠空行
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
    flags = re.IGNORECASE | re.MULTILINE | re.DOTALL
    patterns = [
        r"Failed to execute goal .*maven-compiler-plugin:[^:]+:(?:compile|testCompile).*?(?:Compilation failure|Fatal error compiling)",
        r"\bCOMPILATION ERROR(?:S)?\b",
        r"^\[ERROR\]\s+.+\.java:(?:\[\d+,\d+\]|\d+:)\s",
        r"^\s*error:\s+.+",
        r"\bcannot find symbol\b",
        r"\bincompatible types\b",
        r"\bpackage\s+[a-zA-Z0-9_.]+\s+does not exist\b",
    ]
    return any(re.search(p, log_text, flags) for p in patterns)


# ---------- 中断判定（针对 fatjar 运行） ----------

def _infer_interrupted_fat(returncode: int, report_exists: bool, stdout: str) -> bool:
    """
    更贴近“初始化阶段失败”的判定：
    - 若 report 不存在且 returncode != 0，且 stdout 未出现 '== Test Cases =='，视为中断
    - 若 report 存在（说明已进入测试阶段），不算中断
    """
    return not report_exists


# =========================
# 主流程
# =========================

def fatjar_testsuite_run(
    included_tests: Optional[List[str]] = None,
    excluded_tests: Optional[List[str]] = None,
    timeout: Optional[float] = None,
    require_not_interrupted: bool = False,
    replace_file_path: Optional[str] = None,
    replace_file_content: Optional[str] = None,
    # 兼容旧签名（占位，无实际使用）
    require_local_crash: bool = False,
    local_crash_line_range=None,
    target_method=None,
    need_coverage=False,
) -> FatJarTestResult:
    """
    使用 fat tests JAR 执行测试并汇总结果。
    - included_tests / excluded_tests: 传给 Main 的 -Dtest / -DexcludedTests（逗号分隔，支持通配符或 Class#method）
    - timeout: 仅作用于 java 运行阶段（构建与 javac 不设限）
    - replace_file_*：不改动仓库文件，仅在 target/ 下创建临时源码副本，单文件编译后置于 target/fattest-overrides 并优先于 fatjar
    """
    project_root = Path(".").resolve()
    target_dir = project_root / "target"
    report_path = target_dir / "fat-tests-report.txt"

    env = os.environ.copy()
    # 允许外部覆盖 JAVA_HOME；未设置时不强制
    env["PATH"] = ":".join([
        "/usr/local/sbin", "/usr/local/bin", "/usr/sbin", "/usr/bin", "/sbin", "/bin",
        env.get("PATH", "")
    ])

    extra_cmds: List[str] = []
    build_stdout = ""
    extract_stdout = ""
    javac_stdout = ""
    java_stdout = ""
    test_summary = ""
    compile_failure = False

    try:
        # 0) 确保 target 目录存在
        target_dir.mkdir(exist_ok=True)

        # 1) 确保 fatjar 存在
        fatjar_path, build_stdout = _ensure_fatjar(project_root, env)
        if fatjar_path is None or not fatjar_path.exists():
            # 构建失败
            combined = build_stdout
            result = FatJarTestResult(
                failed_tests=None,
                covered_files=None,
                running_time=None,
                interrupted=True,
                timeout=False,
                compile_failure=is_java_compile_failure(build_stdout),
                reports_exist=False,
                jml_fail=("JML Post-condition Failed" in build_stdout),
                cmd="mvn -DskipTests clean com.example:fat-test-maven-plugin:0.1.0:build",
                test_summary=_summarize_stdout(build_stdout),
                stdout=combined,
            )
            if require_not_interrupted:
                raise RuntimeError("fatjar build interrupted or missing:\n" + result.to_string())
            return result
        extra_cmds.append("mvn -DskipTests clean com.example:fat-test-maven-plugin:0.1.0:build")

        # 2) 确保解出 jacoco agent
        ok, extract_stdout = _extract_jacoco_agent_in_target(target_dir, fatjar_path.name, env)
        extra_cmds.append(f"cd target && jar xf {fatjar_path.name} META-INF/fattest/jacoco-agent.jar")
        # 即使解包失败，后面 java -javaagent 会直接报错；由中断判定兜底

        # 3) （可选）单文件编译覆盖
        overrides_dir: Optional[Path] = None
        if replace_file_path is not None and replace_file_content is not None:
            overrides_dir, javac_stdout, compile_failure = _prepare_override_sources_and_compile(
                project_root, fatjar_path, replace_file_path, replace_file_content, env
            )
            extra_cmds.append(f"cd target && javac -encoding UTF-8 -cp {fatjar_path.name} -d fattest-overrides <{replace_file_path}>")
            if compile_failure:
                # 单文件编译失败，直接返回（对齐原版 compile_failure 语义）
                combined = "\n\n".join(
                    [s for s in [build_stdout, extract_stdout, javac_stdout] if s]
                ).strip()
                result = FatJarTestResult(
                    failed_tests=None,
                    covered_files=None,
                    running_time=None,
                    interrupted=True,          # 认为未进入测试阶段
                    timeout=False,
                    compile_failure=True,
                    reports_exist=False,
                    jml_fail=("JML Post-condition Failed" in combined),
                    cmd=" && ".join(extra_cmds),
                    test_summary=_summarize_stdout(combined),
                    stdout=combined,
                )
                if require_not_interrupted:
                    raise RuntimeError("javac single-file compile failed:\n" + result.to_string())
                return result

        # 4) 运行测试（在 target/ 下）
        # 先清理旧报告
        try:
            if report_path.exists():
                report_path.unlink()
        except Exception:
            pass

        # 构造 java 命令
        java_cmd = _build_java_cmd(fatjar_path.name, overrides_dir, included_tests, excluded_tests)
        extra_cmds.append("cd target && " + " ".join(java_cmd))

        start = time.time()
        cp_java = _run_cmd(java_cmd, env=env, timeout=timeout, cwd=str(target_dir))
        end = time.time()
        running_time = end - start
        java_stdout = cp_java.stdout or ""

        # 5) 解析报告（若固定文件名不存在，做一次兜底匹配）
        if not report_path.exists():
            fallback = sorted(target_dir.glob("*fat-tests*.txt"), key=lambda p: p.stat().st_mtime, reverse=True)
            if fallback:
                report = fallback[0]
            else:
                report = report_path
        else:
            report = report_path

        failed, covered, (total, failures, errors, skipped) = _parse_fat_report(report)
        reports_exist = report.exists()

        resolved_covered = _resolve_well_covered_paths(project_root, covered) if reports_exist else None

        # 6) 生成摘要（去堆栈）并拼接“Tests run ...”汇总
        combined_stdout = "\n\n".join(
            [s for s in [build_stdout, extract_stdout, javac_stdout, java_stdout] if s]
        ).strip()
        stackless = _summarize_stdout(combined_stdout)
        header = f"Tests run: {total}, Failures: {failures}, Errors: {errors}, Skipped: {skipped}" if reports_exist else ""
        test_summary = (header + ("\n" + stackless if stackless else "")).strip()

        # JML 失败标记
        jml_fail = ("JML Post-condition Failed" in combined_stdout)

        # 中断判断
        interrupted = _infer_interrupted_fat(cp_java.returncode, reports_exist, java_stdout)

        result = FatJarTestResult(
            failed_tests=failed if reports_exist else None,
            covered_files=resolved_covered if reports_exist else None,
            running_time=running_time,
            interrupted=interrupted,
            timeout=False,
            compile_failure=False,
            reports_exist=reports_exist,
            jml_fail=jml_fail,
            cmd=" && ".join(extra_cmds),
            test_summary=test_summary,
            stdout=combined_stdout,
        )

    except subprocess.TimeoutExpired:
        result = FatJarTestResult(
            failed_tests=None,
            covered_files=None,
            running_time=None,
            interrupted=True,
            timeout=True,
            compile_failure=False,
            reports_exist=False,
            jml_fail=False,
            cmd="java (timeout)",
            test_summary=None,
            stdout=None,
        )
    except Exception as e:
        combined = "\n\n".join([s for s in [build_stdout, extract_stdout, javac_stdout, java_stdout, f"[runner exception] {e}"] if s]).strip()
        result = FatJarTestResult(
            failed_tests=None,
            covered_files=None,
            running_time=None,
            interrupted=True,
            timeout=False,
            compile_failure=False,
            reports_exist=False,
            jml_fail=("JML Post-condition Failed" in combined),
            cmd=" && ".join(extra_cmds) if extra_cmds else "None",
            test_summary=_summarize_stdout(combined),
            stdout=combined,
        )

    if require_not_interrupted:
        if result.interrupted:
            raise RuntimeError(f"test suite run interrupted:\n{result.to_string()}")
        if result.failed_tests is None:
            raise RuntimeError("not interrupted but failed tests is None:\n" + result.to_string())

    return result
