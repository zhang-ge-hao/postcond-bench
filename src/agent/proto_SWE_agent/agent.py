import asyncio
import glob
import json
import os
import subprocess
import tempfile
from typing import List, Optional, Tuple

from src.ds import Method
from src.clone import repository_reproduct


prompt_template = """\
Write a set of postconditions with icontract for method `{method_name}` in line {line} of `{file_path}`.

Your response MUST contain ONLY decorator lines starting with: `@icontract.snapshot(...)` and `@icontract.ensure(...)`. The generated postcondition should be correct and complete.

You should apply a minimal modification that only includes postcondition injection.
"""


def _extract_postcond(patch_text: str) -> str:
    lines = []
    for raw in patch_text.splitlines():
        if raw.startswith("+") and not raw.startswith("+++"):
            line = raw[1:]
            stripped = line.strip()
            if stripped.startswith("@icontract.snapshot") or stripped.startswith("@icontract.ensure"):
                lines.append(line)
    return "\n".join(lines)


def _run_git(cmd: list[str], cwd: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        cmd,
        cwd=cwd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        check=False,
    )


def ensure_clean_git_repo(repo_dir: str) -> None:
    """
    Make sure repo_dir is a valid git repo with a committed HEAD and clean worktree.
    This must run AFTER postcond.md is written, so that file is tracked too.
    """
    git_dir = os.path.join(repo_dir, ".git")

    # Initialize repo if missing
    if not os.path.exists(git_dir):
        result = _run_git(["git", "init"], repo_dir)
        if result.returncode != 0:
            raise RuntimeError(f"git init failed:\n{result.stdout}")

    # Configure local identity so commits work on any machine / Unity node
    for cmd in (
        ["git", "config", "user.name", "PostcondBench"],
        ["git", "config", "user.email", "postcondbench@example.com"],
    ):
        result = _run_git(cmd, repo_dir)
        if result.returncode != 0:
            raise RuntimeError(f"{' '.join(cmd)} failed:\n{result.stdout}")

    # Stage everything, including postcond.md and env_config changes
    result = _run_git(["git", "add", "-A"], repo_dir)
    if result.returncode != 0:
        raise RuntimeError(f"git add -A failed:\n{result.stdout}")

    # If HEAD does not exist yet, create initial commit
    head_check = _run_git(["git", "rev-parse", "--verify", "HEAD"], repo_dir)
    if head_check.returncode != 0:
        result = _run_git(["git", "commit", "-m", "Initial benchmark snapshot"], repo_dir)
        if result.returncode != 0:
            raise RuntimeError(f"initial git commit failed:\n{result.stdout}")
    else:
        # If repo already has HEAD but is dirty, commit current snapshot
        status = _run_git(["git", "status", "--short"], repo_dir)
        if status.returncode != 0:
            raise RuntimeError(f"git status failed:\n{status.stdout}")
        if status.stdout.strip():
            result = _run_git(["git", "commit", "-m", "Update benchmark snapshot"], repo_dir)
            if result.returncode != 0:
                raise RuntimeError(f"snapshot git commit failed:\n{result.stdout}")

    # Final verification
    result = _run_git(["git", "rev-parse", "HEAD"], repo_dir)
    if result.returncode != 0:
        raise RuntimeError(f"HEAD missing after git setup:\n{result.stdout}")

    result = _run_git(["git", "status", "--short"], repo_dir)
    if result.returncode != 0:
        raise RuntimeError(f"git status failed after setup:\n{result.stdout}")
    if result.stdout.strip():
        raise RuntimeError(f"repo still dirty after setup:\n{result.stdout}")


async def run_agent(
    method: Method,
    model: str = "gpt-5-mini",
    max_rounds: int = 20,
    print_stdout: bool = False,
    mutant_sample_num: int = 5,
    collect_logs: bool = False,
) -> Tuple[str, List[dict], Optional[str], Optional[str]]:
    del max_rounds, mutant_sample_num  # currently unused by the CLI wrapper

    # 1. Write SWE-agent problem statement
    with open("postcond.md", "w") as f:
        f.write(
            prompt_template.format(
                method_name=method.name,
                line=method.start_line,
                file_path=method.file,
            )
        )

    # 2. Ensure the reproduced repo is a valid clean git repo with HEAD
    repo_dir = os.getcwd()
    ensure_clean_git_repo(repo_dir)

    # 3. Run SWE-agent and capture patch outputs
    with tempfile.TemporaryDirectory(prefix="swe_out_") as out_dir:
        cmd = [
            "sweagent",
            "run",
            f"--agent.model.name={model}",
            '--agent.model.completion_kwargs={"reasoning_effort":"low","drop_params":true}',
            "--env.repo.path=.",
            "--agent.model.per_instance_cost_limit=0.05",
            "--problem_statement.path=postcond.md",
            "--env.deployment.image=python:3.12",
            "--env.deployment.type=docker",
            f"--output_dir={out_dir}",
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
        log = (result.stdout or "") + "\n" + (result.stderr or "")

        if print_stdout:
            print(result.stdout)
            print(result.stderr)

        patch_files = glob.glob(os.path.join(out_dir, "**", "*.patch"), recursive=True)
        patch_text = open(patch_files[0], encoding="utf-8").read() if patch_files else ""

    # 4. Extract postconditions from patch
    postcond = _extract_postcond(patch_text)

    history = [
        {
            "role": "sweagent",
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode,
            "patch_files_found": patch_files,
            "postcond_nonempty": bool(postcond.strip()),
        }
    ]
    summary = None

    return postcond, history, log if collect_logs else None, summary


if __name__ == "__main__":
    method_path = "data/step/8.benchmark/keon--algorithms--hailstone.json"
    with open(method_path, encoding="utf-8") as file:
        method = Method.from_dict(json.load(file))

    with repository_reproduct(method.repo) as repo_dir:
        model = "gpt-5-mini"
        print(repo_dir)
        postcond, history, log, _ = asyncio.run(run_agent(method, model, print_stdout=True, collect_logs=True))
        print(repr(postcond))
        print(json.dumps(history, indent=2))
        if log:
            print(log)

