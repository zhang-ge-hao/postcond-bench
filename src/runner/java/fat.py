
import shutil
import os
from pathlib import Path
from typing import *

from .cmd import _run_cmd
from .mvn import _is_java_compile_failure

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
    cp = _run_cmd(build_cmd, env=env, timeout=None)
    # 构建后再找一次
    fatjar = _find_fatjar_in_target(target_dir)
    return fatjar, (cp.stdout or "")


def _extract_jacoco_agent_in_target(project_root: Path, fatjar_path: str, env: dict) -> Tuple[bool, str]:
    """
    在 target/ 内执行：
        jar xf <fatjar> META-INF/fattest/jacoco-agent.jar
    返回 (是否存在, stdout)
    """
    agent_rel = Path("META-INF/fattest/jacoco-agent.jar")
    agent_abs = project_root / agent_rel
    if agent_abs.exists():
        return True, ""

    cp = _run_cmd(
        ["jar", "xf", fatjar_path, str(agent_rel).replace("\\", "/")],
        env=env, timeout=None
    )
    return agent_abs.exists(), (cp.stdout or "")


def _prepare_override_sources_and_compile(
        project_root: Path, 
        fatjar_path: str, 
        replace_file_path: str, 
        replace_file_content: str, env: dict) -> Tuple[Optional[Path], str, bool]:
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
            "-cp", fatjar_path,
            "-d", str(overrides_dir),
            str(tmp_src_path),
        ],
        env=env, timeout=None
    )
    stdout = cp.stdout or ""
    compile_failed = (cp.returncode != 0) or _is_java_compile_failure(stdout)
    return overrides_dir if not compile_failed else None, stdout, compile_failed


def _infer_interrupted_fat(returncode: int, report_exists: bool, stdout: str) -> bool:
    """
    更贴近“初始化阶段失败”的判定：
    - 若 report 不存在且 returncode != 0，且 stdout 未出现 '== Test Cases =='，视为中断
    - 若 report 存在（说明已进入测试阶段），不算中断
    """
    return not report_exists
