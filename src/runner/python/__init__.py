import subprocess
import os
import re
from dataclasses import dataclass
from typing import *
import xml.etree.ElementTree as ET
import uuid
from pathlib import Path
import time
import json
from datetime import datetime
import toml


@dataclass
class PythonTestResult:
    failed_tests: List[str]
    running_time: float
    interrupted: bool
    timeout: bool
    reports_exist: bool
    syntax_error: bool
    icontract_fail: bool
    cmd: str
    test_summary: str
    stdout: str

    def to_flag(self):
        if self.timeout:
            return "timeout"
        if self.syntax_error:
            return "syntax_error"
        if self.icontract_fail:
            return "icontract_fail"
        if not self.reports_exist:
            return "reports_not_exist"
        if self.interrupted:
            return "interrupted"
        if self.failed_tests is not None and len(self.failed_tests) == 0:
            return "passed"
        return "failed"

    def to_string(self):
        def format_list(title: str, items: Optional[List[str]]):
            if items is None:
                return f"{title}: None"
            if len(items) == 0:
                return f"{title}: []"
            lines = [f"{title}:"]
            for item in items:
                lines.append(f"    - {item}")
            return "\n".join(lines)

        parts = []
        parts.append("=== Python Test Result ===")
        parts.append(format_list("Failed tests ", self.failed_tests))
        parts.append(f"Running time : {self.running_time:.2f}s" if self.running_time is not None else "Running time : None")
        parts.append(f"Interrupted  : {self.interrupted if self.interrupted is not None else 'None'}")
        parts.append(f"Timeout      : {self.timeout if self.timeout is not None else 'None'}")
        parts.append(f"Reports exist: {self.reports_exist if self.reports_exist is not None else 'None'}")
        parts.append(f"CMD          : \n    {self.cmd if self.cmd is not None else 'None'}")

        if self.test_summary:
            parts.append(format_list("Test Summary ", self.test_summary.strip().split("\n")))
        else:
            parts.append(f"Test Summary : None")

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


def _ensure_poetry_virtualenv_in_project():
    config_path = "poetry.toml"
    if os.path.exists(config_path):
        with open(config_path, "r", encoding="utf-8") as f:
            try:
                config = toml.load(f)
            except toml.TomlDecodeError:
                config = {}
    else:
        config = {}
    if "virtualenvs" not in config:
        config["virtualenvs"] = {}
    config["virtualenvs"]["in-project"] = True
    config["virtualenvs"]["create"] = True
    if "options" not in config["virtualenvs"]:
        config["virtualenvs"]["options"] = {}
    config["virtualenvs"]["options"]["system-site-packages"] = False
    with open(config_path, "w", encoding="utf-8") as f:
        toml.dump(config, f)
    
    config_path = "pyproject.toml"
    if os.path.exists(config_path):
        with open(config_path, "r", encoding="utf-8") as f:
            try:
                config = toml.load(f)
            except:
                return
    else:
        config = {}
    if "project" not in config:
        config["project"] = {}
    if "version" not in config["project"]:
        config["project"]["version"] = "0.1.0"
    with open(config_path, "w", encoding="utf-8") as f:
        toml.dump(config, f)

def _run_cmd(args: List[str], *, env: Optional[dict]=None, timeout: Optional[float]=None) -> subprocess.CompletedProcess:
    """统一的运行器：不用 shell，捕获 stdout/stderr 到 stdout。"""
    return subprocess.run(
        args,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        check=False,
        timeout=timeout,
        env=env,
    )

def _get_env():
    env = os.environ.copy()

    # 关键 1：禁用“偏好活动 venv”，并强制 in-project
    env["POETRY_VIRTUALENVS_PREFER_ACTIVE"] = "false"
    env["POETRY_VIRTUALENVS_IN_PROJECT"] = "true"
    env["PYTEST_DISABLE_PLUGIN_AUTOLOAD"] = "1"

    # 关键 2：清掉上游 venv 痕迹，防止 Poetry 误判
    env.pop("VIRTUAL_ENV", None)
    env.pop("CONDA_PREFIX", None)

    # 子进程不能是debug模式启动的
    for k in list(env):
        if k.startswith(("DEBUGPY_", "PYDEVD_")):
            env.pop(k, None)
    env["PYTHONBREAKPOINT"] = "0"

    extra_paths = [
        "/root/.cargo/bin",
        "/opt/maven/bin",
        "/root/.local/bin",
        "/root/.pyenv/bin",
        "/root/.pyenv/shims",
        "/usr/local/sbin",
        "/usr/local/bin",
        "/usr/sbin",
        "/usr/bin",
        "/sbin",
        "/bin",
    ]
    env["PATH"] = ":".join(extra_paths)
    env["SSL_CERT_FILE"] = "/etc/ssl/certs/ca-certificates.crt"
    env["PYTHONPATH"] = "."

    return env


def _get_poetry_venv_path() -> str:
    """获取 poetry 当前项目的 venv 绝对路径"""
    vpath = subprocess.check_output(["poetry", "env", "info", "--path"], text=True).strip()
    if not vpath or not os.path.isdir(vpath):
        raise RuntimeError(f"Cannot resolve poetry venv path: {vpath!r}")
    return vpath


def python_testsuite_run(
        included_tests=None, 
        excluded_tests=None, 
        timeout=None,
        require_not_interrupted=False,
        replace_file_path=None,
        replace_file_content=None,
        need_coverage=True,
        need_print=False,
        **kwargs) -> PythonTestResult:

    _ensure_poetry_virtualenv_in_project()

    if replace_file_path is not None and replace_file_content is not None:
        with open(replace_file_path, 'r', encoding='utf-8', errors='ignore') as file:
            ori_file_content = file.read()
        with open(replace_file_path, 'w', encoding='utf-8') as file:
            file.write(replace_file_content)

    try:
        env = _get_env()

        # 1) poetry install（不用 shell）
        install_cp = _run_cmd(["poetry", "install", "--no-interaction"], env=env)
        stdout_install = install_cp.stdout  # 如需记录日志可用

        # 3) 清理旧产物
        for f in ("coverage.xml", "reportlog.jsonl"):
            try:
                os.remove(f)
            except FileNotFoundError:
                pass

        # venv_python = f"{_get_poetry_venv_path()}/bin/python"
        venv_python = ".venv/bin/python"

        if not os.path.exists(venv_python):
            return PythonTestResult(
                failed_tests=None, running_time=None, 
                interrupted=True, timeout=None, reports_exist=False,
                syntax_error=None, icontract_fail=None,
                cmd="pytest (no env)", test_summary=None, 
                stdout=stdout_install)

        # 4) 构造 pytest 命令（直接用 venv 的 python 跑 -m pytest）
        cmd = [
            venv_python, "-m", "pytest",
            # "-c", "/dev/null",
            "--tb=short",
            "-p", "pytest_reportlog",
            "--report-log=reportlog.jsonl",
        ]
        if need_print:
            cmd.append("--capture=no")
        if need_coverage:
            cmd.extend([
                "-p", "pytest_cov",
                "--cov=.", "--cov-branch",
                "--cov-report=term-missing",
                "--cov-report=xml:coverage.xml",
            ])

        # include / exclude
        if included_tests:
            # 直接追加 nodeids 或路径，无需加引号或 \ 续行
            cmd += list(included_tests)
        if excluded_tests:
            for t in excluded_tests:
                cmd += [f"--deselect={t}"]

        # 5) 运行 pytest
        start_time = time.time()
        cp = _run_cmd(cmd, env=env, timeout=timeout)
        end_time = time.time()
        stdout = stdout_install + "\n\n" + cp.stdout

        # 6) 生成结果对象
        reports_exist = os.path.exists("reportlog.jsonl")
        if need_coverage:
            reports_exist = reports_exist and os.path.exists("coverage.xml")

        # 提取测试摘要
        lines = stdout.strip().split("\n")
        test_summary = [lines[-1]] if lines else []
        met_summary = False
        for line in lines:
            if "= short test summary info =" in line:
                met_summary = True
                test_summary = []
            if met_summary:
                test_summary.append(line)
        test_summary = "\n".join(test_summary) if test_summary else None

        running_time = end_time - start_time

        last_line = lines[-1] if lines else ""
        should_have_failed_tests = (" errors" in last_line) or (" failed" in last_line) or (" in " not in last_line)

        if os.path.exists("reportlog.jsonl"):
            interrupted, failed_tests = parse_pytest_reportlog("reportlog.jsonl")
            if should_have_failed_tests and len(failed_tests) == 0:
                interrupted, failed_tests = True, None
        else:
            interrupted, failed_tests = True, None

        syntax_error = False
        icontract_fail = False
        for line in lines:
            if "icontract.errors.ViolationError" in line or \
                    "RuntimeError: Failed to recompute the values of the contract condition" in line:
                icontract_fail = True
            if "SyntaxError:" in line:
                syntax_error = True
            if "IndentationError:" in line:
                syntax_error = True

        cmd_str_for_log = " ".join(cmd)

        test_result = PythonTestResult(
            failed_tests=failed_tests,
            running_time=running_time, interrupted=interrupted, 
            timeout=False, reports_exist=reports_exist, 
            syntax_error=syntax_error, icontract_fail=icontract_fail,
            cmd=cmd_str_for_log, test_summary=test_summary, stdout=stdout)

    except subprocess.TimeoutExpired:
        test_result = PythonTestResult(
            failed_tests=None, running_time=None, 
            interrupted=True, timeout=True, reports_exist=False,
            syntax_error=None, icontract_fail=None,
            cmd="pytest (timeout)", test_summary=None, stdout=None)

    finally:
        if replace_file_path is not None and replace_file_content is not None:
            with open(replace_file_path, 'w', encoding='utf-8') as file:
                file.write(ori_file_content)

    if require_not_interrupted:
        if test_result.interrupted:
            msg = f"test suite run interrupted:\n"
            msg += test_result.to_string()
            raise RuntimeError(msg)
        if test_result.failed_tests is None:
            msg = "not interrupted but failed tests is None:\n"
            msg += test_result.to_string()
            raise RuntimeError(msg)

    return test_result


def parse_pytest_reportlog(jsonl_path: str | Path) -> Tuple[bool, List[str]]:
    p = Path(jsonl_path)
    if not p.exists():
        raise FileNotFoundError(f"No such file: {jsonl_path}")

    failed_nodeids = []
    seen = set()
    interrupted = False
    finish_exitstatus = None

    with p.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
            except Exception:
                continue

            rtype = rec.get("$report_type")
            if rtype == "SessionStart":
                pass
            elif rtype == "SessionFinish":
                finish_exitstatus = rec.get("exitstatus")
                out = rec.get("outcome")
                if out == "interrupted":
                    interrupted = True

            elif rtype in ("TestReport", "CollectReport"):
                outcome = rec.get("outcome")
                if outcome in {"failed", "error"}:
                    nid = rec.get("nodeid")
                    if nid and nid not in seen:
                        seen.add(nid)
                        failed_nodeids.append(nid)

    if not interrupted and finish_exitstatus == 2:
        interrupted = True

    return interrupted, failed_nodeids