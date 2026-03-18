from __future__ import annotations

import json
import os
import re
import subprocess
import time
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_core import CancellationToken

from src.agent.lint.icontract_lint import grammar_verify
from src.agent.proto_v4.mut import load_mutation
from src.agent.proto_v5.agents import get_llm_based_agent
from src.ds import Method
from src.util import get_diff


R1_TIMEOUT_SECONDS = 5
R2_TIMEOUT_MULTIPLIER = 2
MUTANT_FILTER_TIMEOUT_MULTIPLIER = 2
R3_TIMEOUT_MULTIPLIER = 4
INPUT_TIMEOUT_DROP_THRESHOLD = 2
STABLE_MUTANT_ROUNDS_TO_CONVERGE = 2
DEFAULT_MAX_LLM_CALLS = 20
DEFAULT_INPUTS_FEEDBACK = "Please add new and stronger cases."


INPUTS_BUILDER_R1_TEMPLATE = r"""\
import coverage


# ===== method metadata start =====
src_path = "src/agent/proto_v4/_cov_demo/something.py"
func_start = 2
func_end = 12
# ===== method metadata end =====

# ===== inputs program start =====
def construct_inputs_and_run() -> None:
    from src.agent.proto_v4._cov_demo.something import func
    func(1, 2)
    func(-1, -2)
# ===== inputs program end =====

INPUT_RUN_TIMINGS = []


def get_input_run_timings():
    return list(INPUT_RUN_TIMINGS)


def line_coverage_for_range(
    cov: coverage.Coverage,
    filename: str,
    start: int,
    end: int,
    src_lines: list[str],
    covered_tag: str = "COVERED",
    uncovered_tag: str = "UNCOVERED",
):
    _, statements, _, missing, _ = cov.analysis2(filename)

    statements_set = set(statements)
    missing_set = set(missing)

    stmts_in_range = [ln for ln in statements if start <= ln <= end]
    missing_in_range = [ln for ln in missing if start <= ln <= end]
    covered_in_range = [ln for ln in stmts_in_range if ln not in set(missing_in_range)]

    total = len(stmts_in_range)
    covered = len(covered_in_range)
    rate = (covered / total) if total else 1.0

    out_lines = [
        f"Total Statements: {total}",
        f"Covered Statements: {covered}",
        f"Code Coverage: {rate}",
    ]
    for lineno in range(start, end + 1):
        idx = lineno - 1
        code = src_lines[idx] if 0 <= idx < len(src_lines) else ""
        if (lineno in statements_set) and (lineno in missing_set):
            if code.strip() == "":
                annotated = f"{code}  # {covered_tag}"
            else:
                annotated = f"{code}  # {uncovered_tag}"
        else:
            annotated = code
        out_lines.append(f"{lineno:4d}: {annotated}")

    return rate, "\n".join(out_lines)


if __name__ == "__main__":
    with open(src_path) as file:
        src_file = file.read()
    src_lines = src_file.split("\n")

    cov = coverage.Coverage(branch=False, include=[src_path])
    cov.start()
    construct_inputs_and_run()
    cov.stop()
    cov.save()

    rate, annotated = line_coverage_for_range(
        cov, src_path, start=func_start, end=func_end, src_lines=src_lines
    )
    for name, elapsed in get_input_run_timings():
        print(f"INPUT_METHOD_TIME {name}: {elapsed}")
    print(annotated)
    print(f"Code Coverage: {rate}")
    print("Finished without exception.")
"""


INPUTS_BUILDER_R2_3_TEMPLATE = r"""\
# ===== inputs program start =====
def construct_inputs_and_run() -> None:
    from src.agent.proto_v4._cov_demo.something import func
    func(1, 2)
    func(-1, -2)
# ===== inputs program end =====

INPUT_RUN_TIMINGS = []


def get_input_run_timings():
    return list(INPUT_RUN_TIMINGS)


if __name__ == "__main__":
    construct_inputs_and_run()
    print("Finished without exception.")
"""


@dataclass
class _LlmCallBudget:
    max_calls: Optional[int]
    used_calls: int = 0

    def snapshot(self) -> str:
        if self.max_calls is None:
            return f"{self.used_calls}/unlimited"
        return f"{self.used_calls}/{self.max_calls}"

    def consume(self, agent_name: str) -> None:
        if self.max_calls is not None and self.used_calls >= self.max_calls:
            raise _LlmCallLimitReached(
                f"LLM call limit reached before calling {agent_name}: "
                f"{self.used_calls}/{self.max_calls}"
            )
        self.used_calls += 1


class _LlmCallLimitReached(RuntimeError):
    pass


def _iteration_allowed(index: int, limit: Optional[int]) -> bool:
    return limit is None or index < limit


def _markdown_code_block(content: str, language: str = "text") -> str:
    body = content if content else "(empty)"
    return f"```{language}\n{body}\n```"


def _append_log_block(log_lines: List[str], print_stdout: bool, block: str) -> None:
    log_lines.append(block)
    if print_stdout:
        print(block)


def _format_markdown_list(items: List[Tuple[str, object]]) -> str:
    return "\n".join(f"- **{key}:** {value}" for key, value in items)


def _log_llm_call(
    log_lines: List[str],
    print_stdout: bool,
    outer_round: int,
    inner_round: int,
    agent_name: str,
    prompt: str,
    response: str,
    llm_budget: _LlmCallBudget,
) -> None:
    block = "\n".join(
        [
            f"## LLM Call · Outer {outer_round + 1} · Inner {inner_round + 1} · {agent_name}",
            _format_markdown_list(
                [
                    ("LLM calls used", llm_budget.snapshot()),
                ]
            ),
            "### Prompt",
            _markdown_code_block(prompt),
            "### Response",
            _markdown_code_block(response, "python"),
        ]
    )
    _append_log_block(log_lines, print_stdout, block)


def _log_lint_result(
    log_lines: List[str],
    print_stdout: bool,
    outer_round: int,
    inner_round: int,
    lint_message: str,
) -> None:
    block = "\n".join(
        [
            f"## Lint Tool Call · Outer {outer_round + 1} · Inner {inner_round + 1}",
            _markdown_code_block(lint_message),
        ]
    )
    _append_log_block(log_lines, print_stdout, block)


def _log_r1_execution(
    log_lines: List[str],
    print_stdout: bool,
    outer_round: int,
    inner_round: int,
    inputs_builder_code: str,
    r1_stdout: str,
) -> None:
    block = "\n".join(
        [
            f"## R1 Call · Outer {outer_round + 1} · Inner {inner_round + 1}",
            "### Inputs Builder Code",
            _markdown_code_block(inputs_builder_code, "python"),
            "### Execution Result",
            _markdown_code_block(r1_stdout),
        ]
    )
    _append_log_block(log_lines, print_stdout, block)


def _log_r2_r3_execution(
    log_lines: List[str],
    print_stdout: bool,
    outer_round: int,
    next_role: str,
    accepted_inputs_program: str,
    battle_result: Dict[str, object],
) -> None:
    mutant_blocks: List[str] = []
    for mutant_run in battle_result.get("r3_mutant_runs", []):
        mutant_blocks.extend(
            [
                f"### Mutant {mutant_run['mut_index']}",
                _format_markdown_list(
                    [
                        ("Status", mutant_run["status"]),
                        ("Reached in R3", mutant_run["reached"]),
                    ]
                ),
                "#### Mutant Code",
                _markdown_code_block(str(mutant_run.get("mutant") or ""), "python"),
                "#### Execution Result",
                _markdown_code_block(str(mutant_run.get("stdout") or "")),
            ]
        )

    summary_items = [
        ("Next role", next_role),
        ("R2 success", battle_result.get("r2_success")),
        ("R3 status", battle_result.get("r3_status")),
        ("R3 checked mutants", battle_result.get("r3_checked_mutants")),
        ("R3 failed mutant index", battle_result.get("r3_failed_mutant_index")),
        ("Timeout-banned mutants", len(battle_result.get("timeout_banned_mutants", []))),
    ]
    block_parts = [
        f"## R2/R3 Call · Outer {outer_round + 1}",
        "### Summary",
        _format_markdown_list(summary_items),
        "### Inputs Builder Code",
        _markdown_code_block(accepted_inputs_program, "python"),
        "### R2 Execution Result",
        _markdown_code_block(str(battle_result.get("r2_stdout") or "")),
    ]
    if mutant_blocks:
        block_parts.extend(mutant_blocks)
    block = "\n".join(block_parts)
    _append_log_block(log_lines, print_stdout, block)


def _replace_block(text: str, start_marker: str, end_marker: str, new_block: str) -> str:
    pattern = re.compile(
        rf"(^\s*{re.escape(start_marker)}\s*$)(.*?)(^\s*{re.escape(end_marker)}\s*$)",
        flags=re.MULTILINE | re.DOTALL,
    )
    match = pattern.search(text)
    if not match:
        raise ValueError(f"Cannot find block markers: {start_marker} ... {end_marker}")

    new_block = new_block.rstrip("\n") + "\n"
    return text[: match.end(1)] + "\n" + new_block + text[match.start(3) :]


def _format_code_context(method: Method) -> str:
    assert method.file_content
    # TODO: extend this to repository-level context, such as RAG or a SWE-agent style scan.
    return method.file_content


def init_inputs_builder_prompt(method: Method) -> str:
    return f"""\
Code context:
{_format_code_context(method)}

Target method (located in {method.file}):
{method.content}
"""


def refine_inputs_builder_prompt(
    method: Method,
    accepted_inputs_program: str,
    latest_candidate: str,
    execution_feedback: str,
) -> str:
    latest_candidate_section = ""
    if latest_candidate.strip():
        latest_candidate_section = f"""

Latest candidate inputs function:
{latest_candidate}"""

    return f"""\
Code context:
{_format_code_context(method)}

Target method (located in {method.file}):
{method.content}

Accepted inputs program that already works:
{accepted_inputs_program}
{latest_candidate_section}

Execution feedback:
{execution_feedback}
"""


def init_postcondition_prompt(method: Method, accepted_inputs_program: str) -> str:
    return f"""\
Code context:
{_format_code_context(method)}

Target method:
{method.content}

Current accepted inputs program:
{accepted_inputs_program}
"""


def refine_postcondition_prompt(
    method: Method,
    accepted_inputs_program: str,
    postconditions: str,
    feedback: str,
) -> str:
    return f"""\
Code context:
{_format_code_context(method)}

Target method:
{method.content}

Current accepted inputs program:
{accepted_inputs_program}

Current postconditions:
{postconditions}

Feedback:
{feedback}
"""


def _postcondition_lint_feedback(method: Method, postconditions: str, lint_message: str) -> str:
    return f"""\
The current postconditions do not pass icontract lint.

Target method:
{method.content}

Current postconditions:
{postconditions}

Lint message:
{lint_message}
"""


def _postcondition_feedback_r2(
    method: Method,
    accepted_inputs_program: str,
    postconditions: str,
    stdout: str,
) -> str:
    return f"""\
The current postconditions fail on the original method.

Target method:
{method.content}

Current accepted inputs program:
{accepted_inputs_program}

Current postconditions:
{postconditions}

Execution feedback:
{stdout}
"""


def _postcondition_feedback_r3(
    method: Method,
    accepted_inputs_program: str,
    postconditions: str,
    mutant: str,
    stdout: str,
) -> str:
    src = method.content + ("" if method.content.endswith("\n") else "\n")
    tgt = mutant + ("" if mutant.endswith("\n") else "\n")
    diff = get_diff(src, tgt)
    return f"""\
The current postconditions do not reject a runnable mutant.

Target method:
{method.content}

Current accepted inputs program:
{accepted_inputs_program}

Current postconditions:
{postconditions}

Buggy method:
{mutant}

Diff:
{diff}

Execution feedback:
{stdout}
"""


def _inputs_strengthen_feedback(
    method: Method,
    accepted_inputs_program: str,
    postconditions: str,
    runnable_mutant_count: int,
    total_mutant_count: int,
    stable_rounds: int,
) -> str:
    return f"""\
The current accepted inputs are not strong enough yet.

Target method:
{method.content}

Current accepted inputs program:
{accepted_inputs_program}

Current postconditions:
{postconditions}

Result summary:
- Total mutants loaded: {total_mutant_count}
- Runnable mutants under the accepted inputs: {runnable_mutant_count}
- All runnable mutants raised icontract.errors.ViolationError.
- Consecutive rounds with the same runnable mutant set: {stable_rounds}

Please add new and stronger cases.
"""


def _inputs_empty_mutant_feedback(
    method: Method,
    accepted_inputs_program: str,
    total_mutant_count: int,
) -> str:
    return f"""\
The current accepted inputs are too weak.

Target method:
{method.content}

Current accepted inputs program:
{accepted_inputs_program}

Result summary:
- Total mutants loaded: {total_mutant_count}
- Runnable mutants under the accepted inputs: 0

Please add new and stronger cases so that more mutants can run without crashing.
"""


def _rename_construct_inputs(source: str, new_name: str) -> str:
    pattern = re.compile(r"(^\s*def\s+)construct_inputs_and_run(\s*\()", flags=re.MULTILINE)
    renamed, count = pattern.subn(rf"\1{new_name}\2", source, count=1)
    if count != 1:
        raise ValueError("Cannot find construct_inputs_and_run() in inputs builder output.")
    return renamed


def _parse_input_method_times(stdout: str) -> List[Tuple[str, float]]:
    res: List[Tuple[str, float]] = []
    for line in stdout.splitlines():
        if not line.startswith("INPUT_METHOD_TIME "):
            continue
        prefix, value = line.split(":", 1)
        name = prefix.replace("INPUT_METHOD_TIME ", "").strip()
        try:
            elapsed = float(value.strip())
        except ValueError:
            continue
        res.append((name, elapsed))
    return res


def _format_input_method_times(method_timings: List[Tuple[str, float]]) -> str:
    if not method_timings:
        return "No previous input timing data."
    return "\n".join(f"- {name}: {elapsed:.6f}s" for name, elapsed in method_timings)


def _drop_slowest_accepted_input(
    accepted_inputs_versions: List[str],
    accepted_input_timings: List[Tuple[str, float]],
) -> Optional[Tuple[int, str, float]]:
    if not accepted_inputs_versions or not accepted_input_timings:
        return None

    scan_count = min(len(accepted_inputs_versions), len(accepted_input_timings))
    slowest_index = max(range(scan_count), key=lambda idx: accepted_input_timings[idx][1])
    slowest_name, slowest_elapsed = accepted_input_timings[slowest_index]

    accepted_inputs_versions.pop(slowest_index)
    accepted_input_timings.pop(slowest_index)
    return slowest_index, slowest_name, slowest_elapsed


def combine_inputs_builders(inputs_builder_versions: List[str]) -> str:
    if not inputs_builder_versions:
        return ""

    parts: List[str] = ["import time"]
    call_names: List[str] = []
    for index, source in enumerate(inputs_builder_versions):
        call_name = f"construct_inputs_and_run_v{index}"
        parts.append(_rename_construct_inputs(source.strip(), call_name))
        call_names.append(call_name)

    dispatcher_lines = [
        "def construct_inputs_and_run() -> None:",
        "    INPUT_RUN_TIMINGS.clear()",
    ]
    for call_name in call_names:
        dispatcher_lines.extend(
            [
                "    __start = time.perf_counter()",
                f"    {call_name}()",
                "    __elapsed = time.perf_counter() - __start",
                f"    INPUT_RUN_TIMINGS.append((\"{call_name}\", __elapsed))",
            ]
        )

    parts.append("\n".join(dispatcher_lines))
    return "\n\n".join(parts).rstrip() + "\n"


def _icontract_inj(code_str: str, method_start_line: int, method_end_line: int, postcond: str) -> str:
    code_lines = code_str.split("\n")
    method_lines = code_lines[method_start_line - 1 : method_end_line]

    first_line = method_lines[0]
    init_indent = first_line[: -len(first_line.lstrip())]

    postcond_lines = postcond.split("\n")
    while postcond_lines and not postcond_lines[0].strip():
        postcond_lines = postcond_lines[1:]
    while postcond_lines and not postcond_lines[-1].strip():
        postcond_lines = postcond_lines[:-1]

    if not postcond_lines:
        return code_str

    postcond_indent = postcond_lines[0][: -len(postcond_lines[0].lstrip())]
    normalized_lines = []
    for line in postcond_lines:
        normalized_lines.append(init_indent + line[len(postcond_indent) :])
    postcond_lines = normalized_lines

    injected_method_lines: List[str] = []
    injected = False
    for line in method_lines:
        if line.strip().startswith("def ") and not injected:
            injected = True
            injected_method_lines.extend(postcond_lines)
        injected_method_lines.append(line)

    prefix_lines = code_lines[: method_start_line - 1]
    suffix_lines = code_lines[method_end_line:]

    new_prefix_lines: List[str] = []
    added_import = False
    for line in prefix_lines:
        new_prefix_lines.append(line)
        if not added_import and (line.startswith("from") or line.startswith("import")):
            new_prefix_lines.append("import icontract")
            added_import = True
    if not added_import:
        new_prefix_lines.insert(0, "import icontract")

    return "\n".join(new_prefix_lines + injected_method_lines + suffix_lines)


def _run_python_script(script_path: str, timeout_seconds: int) -> str:
    try:
        completed = subprocess.run(
            ["poetry", "run", "python", script_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            check=False,
            timeout=timeout_seconds,
        )
        return completed.stdout or ""
    except subprocess.TimeoutExpired as exc:
        out = exc.stdout or ""
        if not isinstance(out, str):
            try:
                out = out.decode("utf-8", errors="replace")
            except Exception:
                out = ""
        return out + f"\n[TIMEOUT] timeout_seconds={timeout_seconds}"
    except Exception as exc:
        return f"[EXCEPTION] {type(exc).__name__}: {exc}"


def _write_inputs_program(template: str, inputs_program: str, script_path: str) -> None:
    full_code = _replace_block(
        template,
        "# ===== inputs program start =====",
        "# ===== inputs program end =====",
        inputs_program.strip("\n") + "\n",
    )
    with open(script_path, "w", encoding="utf-8") as file:
        file.write(full_code)


def _run_execution_r1(
    method: Method,
    inputs_program: str,
    script_path: str,
    timeout_seconds: int,
) -> str:
    metadata_block = (
        f'src_path = "{method.file}"\n'
        f"func_start = {method.start_line}\n"
        f"func_end = {method.end_line}\n"
    )
    full_code = _replace_block(
        INPUTS_BUILDER_R1_TEMPLATE,
        "# ===== method metadata start =====",
        "# ===== method metadata end =====",
        metadata_block,
    )
    full_code = _replace_block(
        full_code,
        "# ===== inputs program start =====",
        "# ===== inputs program end =====",
        inputs_program.strip("\n") + "\n",
    )

    with open(script_path, "w", encoding="utf-8") as file:
        file.write(full_code)

    stdout = _run_python_script(script_path, timeout_seconds=timeout_seconds)
    if os.path.exists(script_path):
        os.remove(script_path)
    return stdout


def _run_execution_r2(
    inputs_program: str,
    script_path: str,
    postconditions: str,
    method: Method,
    timeout_seconds: int,
) -> str:
    _write_inputs_program(INPUTS_BUILDER_R2_3_TEMPLATE, inputs_program, script_path)

    with open(method.file, encoding="utf-8") as file:
        original_file_content = file.read()

    injected_content = _icontract_inj(
        original_file_content,
        method.start_line,
        method.end_line,
        postconditions,
    )
    with open(method.file, "w", encoding="utf-8") as file:
        file.write(injected_content)

    stdout = _run_python_script(script_path, timeout_seconds=timeout_seconds)

    if os.path.exists(script_path):
        os.remove(script_path)
    with open(method.file, "w", encoding="utf-8") as file:
        file.write(original_file_content)
    return stdout


def _run_execution_single_mut(
    inputs_program: str,
    method: Method,
    mut_index: int,
    timeout_seconds: int,
) -> str:
    script_path = "inputs.py"
    _write_inputs_program(INPUTS_BUILDER_R2_3_TEMPLATE, inputs_program, script_path)

    with open(method.file, encoding="utf-8") as file:
        original_file_content = file.read()

    with open(method.file, "w", encoding="utf-8") as file:
        file.write(method.mut_files_4a[mut_index])

    stdout = _run_python_script(script_path, timeout_seconds=timeout_seconds)

    if os.path.exists(script_path):
        os.remove(script_path)
    with open(method.file, "w", encoding="utf-8") as file:
        file.write(original_file_content)
    print(f"mut_index={mut_index} status={_classify_mutant_execution(stdout)}")
    return stdout


def _run_execution_r3(
    inputs_program: str,
    script_path: str,
    postconditions: str,
    method: Method,
    runnable_mutant_indexes: List[int],
    timeout_seconds: int,
) -> Dict[str, object]:
    _write_inputs_program(INPUTS_BUILDER_R2_3_TEMPLATE, inputs_program, script_path)

    with open(method.file, encoding="utf-8") as file:
        original_file_content = file.read()

    result: Dict[str, object] = {
        "status": "all_violated",
        "checked_mutants": 0,
        "failed_mutant_index": None,
        "failed_mutant": None,
        "failed_stdout": None,
        "mutant_runs": [],
    }

    try:
        for mut_index in runnable_mutant_indexes:
            result["checked_mutants"] = int(result["checked_mutants"]) + 1
            mutant = method.mutants_4a[mut_index]
            start_line, end_line = method.mut_lines_4a[mut_index]
            injected_content = _icontract_inj(method.mut_files_4a[mut_index], start_line, end_line, postconditions)

            with open(method.file, "w", encoding="utf-8") as file:
                file.write(injected_content)

            stdout = _run_python_script(script_path, timeout_seconds=timeout_seconds)
            status = _classify_mutant_execution(stdout)
            result["mutant_runs"].append(
                {
                    "mut_index": mut_index,
                    "mutant": mutant,
                    "stdout": stdout,
                    "status": status,
                    "reached": True,
                }
            )
            if "icontract.errors.ViolationError" not in stdout:
                result["status"] = "postcondition_failure"
                result["failed_mutant_index"] = mut_index
                result["failed_mutant"] = mutant
                result["failed_stdout"] = stdout
                break
    finally:
        if os.path.exists(script_path):
            os.remove(script_path)
        with open(method.file, "w", encoding="utf-8") as file:
            file.write(original_file_content)

    return result


def _parse_code_coverage(stdout: str) -> Tuple[Optional[float], str]:
    assert "Finished without exception." in stdout
    coverage_report = stdout.replace("Finished without exception.", "").strip()
    for line in stdout.split("\n"):
        if "code coverage" in line.lower():
            return float(line.split(":")[-1].strip()), coverage_report
    return None, coverage_report


def _classify_mutant_execution(stdout: str) -> str:
    if "[TIMEOUT]" in stdout:
        return "timeout"
    if "icontract.errors.ViolationError" in stdout:
        return "violation"
    if "Finished without exception." in stdout:
        return "no_error"
    return "other_error"


def _select_runnable_mutants(
    method: Method,
    inputs_program: str,
    timeout_seconds: int,
    banned_mutant_indexes: Optional[set[int]] = None,
) -> Tuple[List[int], set[int]]:
    banned_indexes = set(banned_mutant_indexes or set())
    runnable_indexes: List[int] = []
    for mut_index in range(len(method.mutants_4a)):
        if mut_index in banned_indexes:
            continue
        stdout = _run_execution_single_mut(
            inputs_program,
            method,
            mut_index,
            timeout_seconds=timeout_seconds,
        )
        if _classify_mutant_execution(stdout) != "no_error":
            banned_indexes.add(mut_index)
            continue
        if "Finished without exception." in stdout:
            runnable_indexes.append(mut_index)
    return runnable_indexes, banned_indexes


async def _call_agent_once(agent: AssistantAgent, prompt: str, llm_budget: _LlmCallBudget) -> str:
    llm_budget.consume(agent.name)
    messages = [TextMessage(content=prompt, source="user")]
    token = CancellationToken()
    try:
        result = await agent.on_messages(messages, token)
    except BaseException as exc:
        raise RuntimeError(f"{exc}\n\n{prompt}")
    if not getattr(result, "chat_message", None):
        return ""
    return getattr(result.chat_message, "content", "") or ""


async def _get_lint_passed_postconditions(
    agent: AssistantAgent,
    method: Method,
    accepted_inputs_program: str,
    current_postconditions: str,
    feedback: Optional[str],
    max_inner_rounds: Optional[int],
    log_lines: List[str],
    print_stdout: bool,
    outer_round: int,
    llm_budget: _LlmCallBudget,
) -> Tuple[str, str]:
    prompt = (
        init_postcondition_prompt(method, accepted_inputs_program)
        if not current_postconditions
        else refine_postcondition_prompt(
            method,
            accepted_inputs_program,
            current_postconditions,
            feedback or "Please improve the postconditions.",
        )
    )
    candidate = current_postconditions
    last_lint_message = ""

    inner_round = 0
    while _iteration_allowed(inner_round, max_inner_rounds):
        candidate = await _call_agent_once(agent, prompt, llm_budget)
        _log_llm_call(
            log_lines,
            print_stdout,
            outer_round,
            inner_round,
            "postcondition_assistant",
            prompt,
            candidate,
            llm_budget,
        )

        lint_message = grammar_verify(method.content, candidate)
        last_lint_message = lint_message
        _log_lint_result(log_lines, print_stdout, outer_round, inner_round, lint_message)
        if "No issues found" in lint_message:
            return candidate, ""
        prompt = refine_postcondition_prompt(
            method,
            accepted_inputs_program,
            candidate,
            _postcondition_lint_feedback(method, candidate, lint_message),
        )
        inner_round += 1

    return candidate, last_lint_message


async def _get_valid_inputs_builder(
    agent: AssistantAgent,
    method: Method,
    accepted_inputs_versions: List[str],
    accepted_input_timings: List[Tuple[str, float]],
    feedback: Optional[str],
    max_inner_rounds: Optional[int],
    coverage_threshold: float,
    timeout_seconds: int,
    log_lines: List[str],
    print_stdout: bool,
    outer_round: int,
    llm_budget: _LlmCallBudget,
) -> Tuple[Optional[str], Dict[str, object]]:
    accepted_program = combine_inputs_builders(accepted_inputs_versions)
    prompt = (
        init_inputs_builder_prompt(method)
        if not accepted_inputs_versions
        else refine_inputs_builder_prompt(
            method,
            accepted_program,
            "",
            feedback or "Please add new and stronger cases.",
        )
    )
    last_info: Dict[str, object] = {
        "feedback": feedback or "",
        "r1_stdout": "",
        "coverage": None,
        "coverage_report": "",
        "input_method_timings": list(accepted_input_timings),
        "accepted_program": accepted_program,
    }
    timeout_streak = 0
    inner_round = 0

    while _iteration_allowed(inner_round, max_inner_rounds):
        candidate = await _call_agent_once(agent, prompt, llm_budget)
        _log_llm_call(
            log_lines,
            print_stdout,
            outer_round,
            inner_round,
            "inputs_builder_assistant",
            prompt,
            candidate,
            llm_budget,
        )

        trial_program = combine_inputs_builders(accepted_inputs_versions + [candidate])
        r1_stdout = _run_execution_r1(
            method,
            trial_program,
            "inputs.py",
            timeout_seconds=timeout_seconds,
        )
        last_info["r1_stdout"] = r1_stdout
        _log_r1_execution(log_lines, print_stdout, outer_round, inner_round, trial_program, r1_stdout)

        if "Finished without exception." not in r1_stdout:
            if "[TIMEOUT]" in r1_stdout:
                timeout_streak += 1
            else:
                timeout_streak = 0

            if timeout_streak >= INPUT_TIMEOUT_DROP_THRESHOLD and accepted_inputs_versions:
                dropped = _drop_slowest_accepted_input(accepted_inputs_versions, accepted_input_timings)
                if dropped is not None:
                    _, _, _ = dropped
                    accepted_program = combine_inputs_builders(accepted_inputs_versions)
                    last_info["accepted_program"] = accepted_program
                    last_info["input_method_timings"] = list(accepted_input_timings)
                    timeout_streak = 0
                    last_info["feedback"] = DEFAULT_INPUTS_FEEDBACK
                    prompt = refine_inputs_builder_prompt(
                        method,
                        accepted_program,
                        "",
                        DEFAULT_INPUTS_FEEDBACK,
                    )
                    inner_round += 1
                    continue

            last_info["feedback"] = r1_stdout
            prompt = refine_inputs_builder_prompt(method, accepted_program, candidate, r1_stdout)
            inner_round += 1
            continue

        timeout_streak = 0
        coverage, coverage_report = _parse_code_coverage(r1_stdout)
        input_method_timings = _parse_input_method_times(r1_stdout)
        last_info["coverage"] = coverage
        last_info["coverage_report"] = coverage_report
        last_info["input_method_timings"] = input_method_timings

        if coverage is None or coverage < coverage_threshold:
            coverage_feedback = (
                f"Execution finished, but code coverage is too low.\n\n"
                f"Coverage threshold: {coverage_threshold}\n"
                f"Current coverage: {coverage}\n\n"
                f"Accepted method times:\n{_format_input_method_times(input_method_timings)}\n\n"
                f"Coverage report:\n{coverage_report}"
            )
            last_info["feedback"] = coverage_feedback
            prompt = refine_inputs_builder_prompt(method, accepted_program, candidate, coverage_feedback)
            inner_round += 1
            continue

        last_info["accepted_program"] = trial_program
        return candidate, last_info

    return None, last_info


async def run_agent(
    method: Method,
    model: str = "gpt-5-mini",
    max_rounds: Optional[int] = None,
    max_inner_rounds: Optional[int] = None,
    max_llm_calls: Optional[int] = DEFAULT_MAX_LLM_CALLS,
    coverage_threshold: float = 0.85,
    r1_timeout_seconds: int = R1_TIMEOUT_SECONDS,
    print_stdout: bool = False,
    collect_logs: bool = False,
) -> Tuple[str, List[dict], Optional[str], Optional[dict]]:
    load_mutation(method)

    postcondition_assistant = get_llm_based_agent("postcondition_assistant", model=model)
    inputs_builder_assistant = get_llm_based_agent("inputs_builder_assistant", model=model)

    postconditions = ""
    accepted_inputs_versions: List[str] = []
    accepted_input_timings: List[Tuple[str, float]] = []
    accepted_inputs_program = ""
    runnable_mutant_indexes: List[int] = []
    timeout_banned_mutant_indexes: set[int] = set()

    last_r2_passed = ""
    last_all_violation = ""
    history: List[dict] = []
    log_lines: List[str] = []
    llm_budget = _LlmCallBudget(max_calls=max_llm_calls)
    stop_reason: Optional[str] = None

    next_role = "inputs"
    postcondition_feedback: Optional[str] = None
    inputs_feedback: Optional[str] = None
    previous_all_violation_mutants: Optional[Tuple[int, ...]] = None
    stable_mutant_rounds = 0

    r2_timeout_seconds = r1_timeout_seconds * R2_TIMEOUT_MULTIPLIER
    mutant_filter_timeout_seconds = r1_timeout_seconds * MUTANT_FILTER_TIMEOUT_MULTIPLIER
    r3_timeout_seconds = r1_timeout_seconds * R3_TIMEOUT_MULTIPLIER

    outer_round = 0
    while _iteration_allowed(outer_round, max_rounds):
        if next_role == "inputs":
            try:
                candidate, info = await _get_valid_inputs_builder(
                    inputs_builder_assistant,
                    method,
                    accepted_inputs_versions,
                    accepted_input_timings,
                    inputs_feedback,
                    max_inner_rounds,
                    coverage_threshold,
                    r1_timeout_seconds,
                    log_lines,
                    print_stdout,
                    outer_round,
                    llm_budget,
                )
            except _LlmCallLimitReached as exc:
                stop_reason = str(exc)
                break
            accepted_inputs_program = str(info.get("accepted_program") or accepted_inputs_program)
            history.append(
                {
                    "outer_round": outer_round,
                    "role": "inputs_builder_assistant",
                    "accepted": candidate is not None,
                    "feedback": inputs_feedback,
                    "r1_stdout": info.get("r1_stdout"),
                    "coverage": info.get("coverage"),
                    "input_method_timings": info.get("input_method_timings"),
                    "llm_calls_used": llm_budget.used_calls,
                }
            )
            if candidate is None:
                inputs_feedback = str(info.get("feedback") or "Failed to build valid inputs.")
                outer_round += 1
                continue

            accepted_inputs_versions.append(candidate)
            accepted_inputs_program = str(info.get("accepted_program") or combine_inputs_builders(accepted_inputs_versions))
            accepted_input_timings = list(info.get("input_method_timings") or [])
            runnable_mutant_indexes, timeout_banned_mutant_indexes = _select_runnable_mutants(
                method,
                accepted_inputs_program,
                timeout_seconds=mutant_filter_timeout_seconds,
                banned_mutant_indexes=timeout_banned_mutant_indexes,
            )
            inputs_feedback = None
            previous_all_violation_mutants = None
            stable_mutant_rounds = 0

            if not postconditions:
                next_role = "postcondition"
            else:
                next_role = "battle"
            outer_round += 1
            continue

        if next_role == "postcondition":
            try:
                candidate, lint_feedback = await _get_lint_passed_postconditions(
                    postcondition_assistant,
                    method,
                    accepted_inputs_program,
                    postconditions,
                    postcondition_feedback,
                    max_inner_rounds,
                    log_lines,
                    print_stdout,
                    outer_round,
                    llm_budget,
                )
            except _LlmCallLimitReached as exc:
                stop_reason = str(exc)
                break
            history.append(
                {
                    "outer_round": outer_round,
                    "role": "postcondition_assistant",
                    "lint_passed": not lint_feedback,
                    "feedback": postcondition_feedback,
                    "postconditions": candidate,
                    "llm_calls_used": llm_budget.used_calls,
                }
            )
            if lint_feedback:
                postconditions = candidate
                postcondition_feedback = lint_feedback
                outer_round += 1
                continue

            postconditions = candidate
            postcondition_feedback = None
            next_role = "battle"
            outer_round += 1
            continue

        if next_role != "battle":
            raise ValueError(f"Unexpected next_role: {next_role!r}")

        if not accepted_inputs_program:
            next_role = "inputs"
            outer_round += 1
            continue
        if not postconditions:
            next_role = "postcondition"
            outer_round += 1
            continue

        battle_result: Dict[str, object] = {
            "r2_stdout": None,
            "r2_success": None,
            "r3_status": None,
            "r3_checked_mutants": len(runnable_mutant_indexes),
            "r3_failed_mutant_index": None,
            "r3_mutant_runs": [],
            "timeout_banned_mutants": sorted(timeout_banned_mutant_indexes),
            "input_method_timings": accepted_input_timings,
            "r1_timeout_seconds": r1_timeout_seconds,
            "r2_timeout_seconds": r2_timeout_seconds,
            "mutant_filter_timeout_seconds": mutant_filter_timeout_seconds,
            "r3_timeout_seconds": r3_timeout_seconds,
        }

        r2_stdout = _run_execution_r2(
            accepted_inputs_program,
            "inputs.py",
            postconditions,
            method,
            timeout_seconds=r2_timeout_seconds,
        )
        battle_result["r2_stdout"] = r2_stdout
        battle_result["r2_success"] = "Finished without exception." in r2_stdout

        if "Finished without exception." not in r2_stdout:
            previous_all_violation_mutants = None
            stable_mutant_rounds = 0
            postcondition_feedback = _postcondition_feedback_r2(
                method,
                accepted_inputs_program,
                postconditions,
                r2_stdout,
            )
            battle_result["r3_status"] = "skip_r3_due_to_r2_failure"
            history.append(
                {
                    "outer_round": outer_round,
                    "role": "battle",
                    "next_role": "postcondition",
                    "runnable_mutants": list(runnable_mutant_indexes),
                    "battle_result": battle_result,
                    "postconditions": postconditions,
                    "accepted_inputs_program": accepted_inputs_program,
                    "llm_calls_used": llm_budget.used_calls,
                }
            )
            _log_r2_r3_execution(log_lines, print_stdout, outer_round, "postcondition", accepted_inputs_program, battle_result)
            next_role = "postcondition"
            outer_round += 1
            continue

        last_r2_passed = postconditions

        if not runnable_mutant_indexes:
            inputs_feedback = _inputs_empty_mutant_feedback(
                method,
                accepted_inputs_program,
                len(method.mutants_4a),
            )
            battle_result["r3_status"] = "no_runnable_mutants"
            history.append(
                {
                    "outer_round": outer_round,
                    "role": "battle",
                    "next_role": "inputs",
                    "runnable_mutants": [],
                    "battle_result": battle_result,
                    "postconditions": postconditions,
                    "accepted_inputs_program": accepted_inputs_program,
                    "llm_calls_used": llm_budget.used_calls,
                }
            )
            _log_r2_r3_execution(log_lines, print_stdout, outer_round, "inputs", accepted_inputs_program, battle_result)
            next_role = "inputs"
            outer_round += 1
            continue

        r3_result = _run_execution_r3(
            accepted_inputs_program,
            "inputs.py",
            postconditions,
            method,
            runnable_mutant_indexes,
            timeout_seconds=r3_timeout_seconds,
        )
        battle_result["r3_status"] = r3_result["status"]
        battle_result["r3_checked_mutants"] = r3_result["checked_mutants"]
        battle_result["r3_failed_mutant_index"] = r3_result["failed_mutant_index"]
        battle_result["r3_mutant_runs"] = r3_result["mutant_runs"]

        if r3_result["status"] == "postcondition_failure":
            previous_all_violation_mutants = None
            stable_mutant_rounds = 0
            postcondition_feedback = _postcondition_feedback_r3(
                method,
                accepted_inputs_program,
                postconditions,
                str(r3_result["failed_mutant"] or ""),
                str(r3_result["failed_stdout"] or ""),
            )
            history.append(
                {
                    "outer_round": outer_round,
                    "role": "battle",
                    "next_role": "postcondition",
                    "runnable_mutants": list(runnable_mutant_indexes),
                    "battle_result": battle_result,
                    "postconditions": postconditions,
                    "accepted_inputs_program": accepted_inputs_program,
                    "llm_calls_used": llm_budget.used_calls,
                }
            )
            _log_r2_r3_execution(log_lines, print_stdout, outer_round, "postcondition", accepted_inputs_program, battle_result)
            next_role = "postcondition"
            outer_round += 1
            continue

        last_all_violation = postconditions
        current_mutants = tuple(runnable_mutant_indexes)
        if previous_all_violation_mutants == current_mutants:
            stable_mutant_rounds += 1
        else:
            stable_mutant_rounds = 1
        previous_all_violation_mutants = current_mutants

        if stable_mutant_rounds >= STABLE_MUTANT_ROUNDS_TO_CONVERGE:
            battle_result["r3_status"] = "converged_all_violated"
            battle_result["stable_mutant_rounds"] = stable_mutant_rounds
            history.append(
                {
                    "outer_round": outer_round,
                    "role": "battle",
                    "next_role": "yield",
                    "runnable_mutants": list(runnable_mutant_indexes),
                    "battle_result": battle_result,
                    "postconditions": postconditions,
                    "accepted_inputs_program": accepted_inputs_program,
                    "llm_calls_used": llm_budget.used_calls,
                }
            )
            _log_r2_r3_execution(log_lines, print_stdout, outer_round, "yield", accepted_inputs_program, battle_result)
            break

        inputs_feedback = _inputs_strengthen_feedback(
            method,
            accepted_inputs_program,
            postconditions,
            len(runnable_mutant_indexes),
            len(method.mutants_4a),
            stable_mutant_rounds,
        )
        history.append(
            {
                "outer_round": outer_round,
                "role": "battle",
                "next_role": "inputs",
                "runnable_mutants": list(runnable_mutant_indexes),
                "battle_result": battle_result,
                "postconditions": postconditions,
                "accepted_inputs_program": accepted_inputs_program,
                "llm_calls_used": llm_budget.used_calls,
            }
        )
        _log_r2_r3_execution(log_lines, print_stdout, outer_round, "inputs", accepted_inputs_program, battle_result)
        next_role = "inputs"
        outer_round += 1

    final_postconditions = last_all_violation or last_r2_passed or postconditions
    summary = {
        "final_postconditions": final_postconditions,
        "stop_reason": stop_reason,
        "last_r2_passed": last_r2_passed,
        "last_all_violation": last_all_violation,
        "accepted_inputs_versions": len(accepted_inputs_versions),
        "accepted_input_timings": accepted_input_timings,
        "runnable_mutants": len(runnable_mutant_indexes),
        "timeout_banned_mutants": len(timeout_banned_mutant_indexes),
        "timeout_banned_mutant_indexes": sorted(timeout_banned_mutant_indexes),
        "stable_mutant_rounds": stable_mutant_rounds,
        "loaded_mutants": len(method.mutants_4a),
        "llm_calls_used": llm_budget.used_calls,
        "max_llm_calls": llm_budget.max_calls,
        "r1_timeout_seconds": r1_timeout_seconds,
        "r2_timeout_seconds": r2_timeout_seconds,
        "mutant_filter_timeout_seconds": mutant_filter_timeout_seconds,
        "r3_timeout_seconds": r3_timeout_seconds,
    }
    history.append({"role": "summary", **summary})

    _append_log_block(
        log_lines,
        print_stdout,
        "\n".join(
            [
                "## Final Summary",
                _format_markdown_list(
                    [
                        ("Stop reason", stop_reason or "normal_return"),
                        ("Final postconditions chosen", "present" if final_postconditions else "empty"),
                        ("Accepted inputs versions", len(accepted_inputs_versions)),
                        ("Runnable mutants", len(runnable_mutant_indexes)),
                        ("Timeout-banned mutants", len(timeout_banned_mutant_indexes)),
                        ("LLM calls used", llm_budget.snapshot()),
                    ]
                ),
                "### JSON Summary",
                _markdown_code_block(json.dumps(summary, indent=2, ensure_ascii=False), "json"),
            ]
        ),
    )

    logs_str = "\n".join(log_lines)
    if collect_logs:
        return final_postconditions, history, logs_str, summary
    return final_postconditions, history, None, summary


if __name__ == "__main__":
    from src.clone import repository_reproduct

    method_path = "data/step/9.gpt-5-mini--proto_v4/aiogram--aiogram--check_webapp_signature.json"
    method_path = "data/step/8.benchmark/keon--algorithms--hailstone.json"
    with open(method_path, encoding="utf-8") as file:
        method = Method.from_dict(json.load(file))

    with repository_reproduct(method.repo) as repo_dir:
        print(repo_dir)
        result, history, _, summary = __import__("asyncio").run(
            run_agent(method, model="gpt-5-mini", print_stdout=True, collect_logs=True)
        )
        print(result)
        print(json.dumps(summary, indent=2, ensure_ascii=False))