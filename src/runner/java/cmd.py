
import subprocess
from typing import *
import os
from pathlib import Path

def _run_cmd(args: List[str], *, 
             env: Optional[dict] = None, 
             cwd: Optional[str] = None,
             timeout: Optional[float] = None) -> subprocess.CompletedProcess:
    """运行命令（非 shell），捕获 stdout+stderr 到 stdout。"""
    return subprocess.run(
        args,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        check=False,
        timeout=timeout,
        env=env,
        cwd=cwd
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


def _build_java_cmd(fatjar_path: str, overrides_dir: Optional[Path],
                    included_tests: Optional[List[str]], excluded_tests: Optional[List[str]]) -> List[str]:
    """
    构造 java 命令列表（在 target/ 下执行）。
    -Dtest / -DexcludedTests 以逗号分隔
    -cp: overrides_dir（若有）放在前面，然后 fatjar
    """
    agent_cmd = (
        "-javaagent:META-INF/fattest/jacoco-agent.jar="
        "destfile=jacoco.exec,output=file,append=false,dumponexit=true"
    )
    java_cmd = [
        "java",
        "-ea",
        "--add-exports", "java.base/jdk.internal.ref=ALL-UNNAMED",
        "--add-exports", "java.base/jdk.internal.misc=ALL-UNNAMED",
        "--add-opens", "java.base/java.lang=ALL-UNNAMED",
        "--add-opens", "java.base/java.nio=ALL-UNNAMED",
        "--add-opens", "java.base/sun.nio.ch=ALL-UNNAMED",
        "--add-exports", "jdk.compiler/com.sun.tools.javac.api=ALL-UNNAMED",
        "--add-exports", "jdk.compiler/com.sun.tools.javac.file=ALL-UNNAMED",
        "--add-exports", "jdk.compiler/com.sun.tools.javac.main=ALL-UNNAMED",
        "--add-exports", "jdk.compiler/com.sun.tools.javac.util=ALL-UNNAMED",
        "--add-exports", "jdk.compiler/com.sun.tools.javac.processing=ALL-UNNAMED",
        "--add-exports", "jdk.compiler/com.sun.tools.javac.model=ALL-UNNAMED",
        "--add-exports", "jdk.compiler/com.sun.tools.javac.tree=ALL-UNNAMED",
        "--add-exports", "jdk.compiler/com.sun.tools.javac.parser=ALL-UNNAMED",
        agent_cmd,
    ]
    if included_tests:
        java_cmd.append(f"-Dtest={','.join(included_tests)}")
    if excluded_tests:
        java_cmd.append(f"-DexcludedTests={','.join(excluded_tests)}")

    # classpath
    cp_elems = []
    if overrides_dir:
        cp_elems.append(str(overrides_dir))
    cp_elems.append(fatjar_path)
    java_cmd += ["-cp", os.pathsep.join(cp_elems)]

    # Main
    java_cmd.append("com.example.fatrunner.Main")
    return java_cmd
