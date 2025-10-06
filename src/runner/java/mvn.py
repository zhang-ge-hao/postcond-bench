import re
from typing import *
from pathlib import Path

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


def _is_java_compile_failure(log_text: str) -> bool:
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
