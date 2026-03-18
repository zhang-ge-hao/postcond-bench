from src.ds import *
from src.clone import repository_reproduct

import time, random
import re, subprocess
import asyncio, os
import yaml
from tqdm import tqdm

from typing import Tuple, Optional, Dict

from autogen_core import CancellationToken

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_agentchat.teams import SelectorGroupChat

from src.agent.proto_v4.agents import get_llm_based_agent
from src.agent.proto_v4.models import client
from src.agent.proto_v4.mut import load_mutation
from src.agent.lint.icontract_lint import grammar_verify

from src.util import get_diff

INPUTS_BUILDER_R1_TEMPLATE = r"""\
import inspect
import coverage


# ===== method metadata start =====
src_path = "src/agent/proto_v4/_cov_demo/something.py"
func_start = 2
func_end = 12
# ===== method metadata end =====

# ===== construct_inputs_and_run start =====
def construct_inputs_and_run():
    from src.agent.proto_v4._cov_demo.something import func
    func(1, 2)
    func(-1, -2)
# ===== construct_inputs_and_run end =====

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

    report = {
        "start": start,
        "end": end,
        "total_statements": total,
        "covered_statements": covered,
        "rate": rate,
        "covered_lines": covered_in_range,
        "missing_lines": missing_in_range,
    }
    out_lines = [
        f"Total Statements: {total}",
        f"Covered Statements: {covered}",
        f"Code Coverage: {rate}"
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

    annotated_code_str = "\n".join(out_lines)

    return report, annotated_code_str


if __name__ == "__main__":
    with open(src_path) as file:
        src_file = file.read()
    src_lines = src_file.split("\n")

    cov = coverage.Coverage(
        branch=False,
        include=[src_path],
    )

    cov.start()
    construct_inputs_and_run()
    cov.stop()
    cov.save()

    func_report, annotated = line_coverage_for_range(
        cov, src_path, start=func_start, end=func_end, src_lines=src_lines
    )

    # print("\n=== func line coverage ===")
    # print(func_report)

    # print("\n=== func code (annotated) ===")
    print(annotated)
    print("Finished without exception.")
"""


INPUTS_BUILDER_R2_3_TEMPLATE = r"""\
import inspect
import random
import coverage

# ===== construct_inputs_and_run start =====
def construct_inputs_and_run():
    from src.agent.proto_v4._cov_demo.something import func
    func(1, 2)
    func(-1, -2)
# ===== construct_inputs_and_run end =====


if __name__ == "__main__":
    construct_inputs_and_run()
    print("Finished without exception.")
"""


def _replace_block(text: str, start_marker: str, end_marker: str, new_block: str) -> str:
    pattern = re.compile(
        rf"(^\s*{re.escape(start_marker)}\s*$)(.*?)(^\s*{re.escape(end_marker)}\s*$)",
        flags=re.MULTILINE | re.DOTALL,
    )
    m = pattern.search(text)
    if not m:
        raise ValueError(f"Cannot find block markers: {start_marker} ... {end_marker}")

    new_block = new_block.rstrip("\n") + "\n"

    return text[:m.end(1)] + "\n" + new_block + text[m.start(3):]


def init_generation_prompt(method: Method) -> str:
    assert method.file_content
    return f"""\
Code context:
{method.file_content}\n\n
Target method:
{method.content}
"""


def init_inputs_builder_prompt(method: Method) -> str:
    assert method.file_content
    return f"""\
Code context:
{method.file_content}\n\n
Target method (located in {method.file}):
{method.content}
"""


def _generation_refine_prompt(method: Method, 
                              postconditions: str, 
                              feedback: str) -> str:
    assert method.file_content
    return f"""\
Code context:
{method.file_content}\n\n
Target method:
{method.content}\n\n
Previous postconditions:
{postconditions}\n\n
Execution feedback:
{feedback}
"""


def _inputs_build_refine_prompt(method: Method, 
                                inputs_builder_code: str, 
                                feedback: str) -> str:
    assert method.file_content
    return f"""\
Code context:
{method.file_content}\n\n
Target method (located in {method.file}):
{method.content}\n\n
Previous construct_inputs_and_run():
{inputs_builder_code}\n\n
Execution feedback:
{feedback}
"""


def _inputs_build_increase_coverage_prompt(method: Method, 
                                           inputs_builder_code: str, 
                                           first_round_stdout: str,
                                           code_coverage_threshold: float) -> str:
    assert method.file_content
    return f"""\
Code context:
{method.file_content}\n\n
Target method (located in {method.file}):
{method.content}\n\n
Previous construct_inputs_and_run():
{inputs_builder_code}\n\n
Execution feedback:
{first_round_stdout}
The code coverage is relatively low (lower than {code_coverage_threshold}).
Please try to cover more statements.
"""


def _judge_prompt_r2(method: Method, 
                     postconditions: str, 
                     inputs_builder_code: str, 
                     second_round_stdout: str) -> str:
    assert method.file_content
    return f"""\
Code context:
{method.file_content}\n\n
Target method:
{method.content}\n\n
Current postconditions:
{postconditions}\n\n
Current construct_inputs_and_run():
{inputs_builder_code}\n\n
Execution feedback:
{second_round_stdout}
"""


def _judge_prompt_r3(method: Method, 
                     postconditions: str, 
                     inputs_builder_code: str, 
                     third_round_mutant: str,
                     third_round_stdout: str,
                     coverage_report: str) -> str:
    assert method.file_content

    __src = method.content + ("" if method.content.endswith("\n") else "\n")
    __tgt = third_round_mutant + ("" if third_round_mutant.endswith("\n") else "\n")
    diff = get_diff(__src, __tgt)

    return f"""\
Code context:
{method.file_content}\n\n
Target method:
{method.content}\n\n
Current postconditions:
{postconditions}\n\n
Current construct_inputs_and_run():
{inputs_builder_code}\n\n
Code Coverage Information:
{coverage_report}\n\n
Buggy method:
{third_round_mutant}\n\n
Diff:
{diff}\n\n
Buggy method execution stdout:
{third_round_stdout}
"""


def _grammar_prompt(method_content: str, 
                    postconditions: str,
                    lint_message: str) -> str:
    return f"""\
Target method:
{method_content}\n\n
Current postconditions:
{postconditions}\n\n
Error message:
{lint_message}
"""


def _icontract_inj(
        code_str: str, 
        method_start_line: int,
        method_end_line: int,
        postcond: str):

    code_lines = code_str.split("\n")

    method_lines = code_lines[method_start_line - 1: method_end_line]
    
    # 计算方法的缩进
    __line = method_lines[0]
    init_indent = __line[: -len(__line.lstrip())]

    # 去除postcond前后的空行
    postcond_lines = postcond.split("\n")
    while postcond_lines and len(postcond_lines[0].strip()) == 0:
        postcond_lines = postcond_lines[1: ]
    while postcond_lines and len(postcond_lines[-1].strip()) == 0:
        postcond_lines = postcond_lines[: -1]
    
    # 将postcond行的缩进和方法默认缩进进行统一
    __line = postcond_lines[0]
    postcond_indent = __line[: -len(__line.lstrip())]
    for l_idx, l in enumerate(postcond_lines):
        postcond_lines[l_idx] = init_indent + l[len(postcond_indent): ]

    # 获取插入postcond后的方法行
    # 注意python的所有postcondition行一定要出现在所有其他装饰器之后
    # 正确顺序：
    # @classmethod
    # @icontract.snapshot(...
    # def push(...
    inj_method_lines = []
    injected = False
    for l in method_lines:
        if l.strip().startswith("def ") and not injected:
            injected = True
            inj_method_lines.extend(postcond_lines)
        inj_method_lines.append(l)

    prefix_lines = code_lines[:method_start_line - 1]
    suffix_lines = code_lines[method_end_line: ]

    # 插入python的import icontract
    # 希望它能成为文件中的第二个import 如果文件中本身没找到import行
    # 就插入到文件第一行
    __prefix_lines = []
    added = False
    for line in prefix_lines:
        __prefix_lines.append(line)
        if not added and \
            (line.startswith("from") or line.startswith("import")):
            __prefix_lines.append("import icontract")
            added = True
    if not added:
        __prefix_lines.insert(0, "import icontract")
    prefix_lines = __prefix_lines

    # 组合为插入后的文件
    inj_code_lines = prefix_lines + inj_method_lines + suffix_lines

    inj_code = "\n".join(inj_code_lines)
    return inj_code


def _run_python_script(script_path: str, timeout_seconds: int = 15) -> str:
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
    except subprocess.TimeoutExpired as e:
        out = (e.stdout or "")
        if not isinstance(out, str):
            try:
                out = out.decode("utf-8", errors="replace")
            except Exception:
                out = ""
        out += f"\n[TIMEOUT] timeout_seconds={timeout_seconds}"
        return out
    except Exception as e:
        return f"[EXCEPTION] {type(e).__name__}: {e}"


def _run_execution_r1(method: Method, inputs_builder_code: str, inputs_builder_path: str) -> str:
    """wo/ postconds; only test whether inputs builder is runnable"""

    inputs_builder_full = INPUTS_BUILDER_R1_TEMPLATE
    src_path = method.file
    func_start = method.start_line
    func_end = method.end_line
    metadata_block = (
        f'src_path = "{src_path}"\n'
        f"func_start = {func_start}\n"
        f"func_end = {func_end}\n"
    )
    inputs_builder_full = _replace_block(
        inputs_builder_full,
        "# ===== method metadata start =====",
        "# ===== method metadata end =====",
        metadata_block,
    )
    inputs_builder_full = _replace_block(
        inputs_builder_full,
        "# ===== construct_inputs_and_run start =====",
        "# ===== construct_inputs_and_run end =====",
        inputs_builder_code.strip("\n") + "\n",
    )

    with open(inputs_builder_path, "w") as file:
        file.write(inputs_builder_full)

    first_round_stdout = _run_python_script(inputs_builder_path)

    if os.path.exists(inputs_builder_path):
        os.remove(inputs_builder_path)
    
    return first_round_stdout


def _run_execution_r2(inputs_builder_code: str, 
                      inputs_builder_path: str, 
                      postconditions: str, 
                      method_start_line: int, 
                      method_end_line: int, 
                      method_file_path: str) -> str:
    """w/ original method + postconds"""

    inputs_builder_full = INPUTS_BUILDER_R2_3_TEMPLATE
    inputs_builder_full = _replace_block(
        inputs_builder_full,
        "# ===== construct_inputs_and_run start =====",
        "# ===== construct_inputs_and_run end =====",
        inputs_builder_code.strip("\n") + "\n",
    )

    with open(inputs_builder_path, "w") as file:
        file.write(inputs_builder_full)

    with open(method_file_path) as file:
        ori_file_content = file.read()

    inj_content = _icontract_inj(ori_file_content, 
                                 method_start_line, 
                                 method_end_line,
                                 postconditions)
    with open(method_file_path, "w") as file:
        file.write(inj_content)

    second_round_stdout = _run_python_script(inputs_builder_path)

    # recover
    if os.path.exists(inputs_builder_path):
        os.remove(inputs_builder_path)
    with open(method_file_path, "w") as file:
        file.write(ori_file_content)
    
    return second_round_stdout


def _run_execution_r3(inputs_builder_code: str, 
                      inputs_builder_path: str, 
                      postconditions: str, 
                      method: Method,
                      selected_mut_indexs: List[int]) -> Tuple[str, str, int]:
    """w/ mutant + postconds"""

    inputs_builder_full = INPUTS_BUILDER_R2_3_TEMPLATE
    inputs_builder_full = _replace_block(
        inputs_builder_full,
        "# ===== construct_inputs_and_run start =====",
        "# ===== construct_inputs_and_run end =====",
        inputs_builder_code.strip("\n") + "\n",
    )

    with open(inputs_builder_path, "w") as file:
        file.write(inputs_builder_full)

    with open(method.file) as file:
        ori_file_content = file.read()

    third_round_stdout = ""
    third_round_mutant = ""
    third_round_mut_idx = None

    assert len(method.mut_files_4a) == len(method.mut_lines_4a) == len(method.mutants_4a)

    for mut_idx in selected_mut_indexs:
        mutant = method.mutants_4a[mut_idx]
        mut_file = method.mut_files_4a[mut_idx]
        start_line, end_line = method.mut_lines_4a[mut_idx]

        inj_content = _icontract_inj(mut_file, start_line, end_line, 
                                     postconditions)
        with open(method.file, "w") as file:
            file.write(inj_content)

        third_round_stdout = _run_python_script(inputs_builder_path)
        third_round_mutant = mutant
        third_round_mut_idx = mut_idx

        if "icontract.errors.ViolationError" not in third_round_stdout:
            break

    # recover
    if os.path.exists(inputs_builder_path):
        os.remove(inputs_builder_path)
    with open(method.file, "w") as file:
        file.write(ori_file_content)
    
    return third_round_stdout, third_round_mutant, third_round_mut_idx


def _run_execution_single_mut(inputs_builder_code: str, 
                              method: Method,
                              mut_index: int) -> str:
    """wo/ postconds; only test whether inputs builder + mutant is runnable"""

    inputs_builder_path = "inputs.py"

    inputs_builder_full = INPUTS_BUILDER_R2_3_TEMPLATE
    inputs_builder_full = _replace_block(
        inputs_builder_full,
        "# ===== construct_inputs_and_run start =====",
        "# ===== construct_inputs_and_run end =====",
        inputs_builder_code.strip("\n") + "\n",
    )

    with open(inputs_builder_path, "w") as file:
        file.write(inputs_builder_full)

    with open(method.file) as file:
        ori_file_content = file.read()

    assert len(method.mut_files_4a) == len(method.mut_lines_4a) == len(method.mutants_4a)

    mut_file = method.mut_files_4a[mut_index]
    with open(method.file, "w") as file:
        file.write(mut_file)

    stdout = _run_python_script(inputs_builder_path)

    # recover
    if os.path.exists(inputs_builder_path):
        os.remove(inputs_builder_path)
    with open(method.file, "w") as file:
        file.write(ori_file_content)
    
    return stdout


def _parse_code_coverage(first_round_stdout: str):
    assert "Finished without exception." in first_round_stdout
    coverage_report = first_round_stdout.replace("Finished without exception.", "").strip()
    for li in first_round_stdout.split("\n"):
        if "code coverage" in li.lower():
            return float(li.split(":")[-1]), coverage_report
    return None, coverage_report


def run_execution(method: Method, 
                  postconditions: str, 
                  inputs_builder_code: str,
                  selected_mut_indexs: List[int],
                  code_coverage_threshold: float = 0.85) -> Tuple[str, str, Dict[str, Union[str, int]]]:
    inputs_builder_path = "inputs.py"
    log_dict = {"r1_stdout": None, 
                "r2_stdout": None, 
                "r3_stdout": None, 
                "r3_mutant": None, 
                "r3_mut_idx": None}

    first_round_stdout = _run_execution_r1(method, 
                                           inputs_builder_code, 
                                           inputs_builder_path)
    log_dict["r1_stdout"] = first_round_stdout

    if "Finished without exception." not in first_round_stdout:
        next_prompt = _inputs_build_refine_prompt(
            method, inputs_builder_code, first_round_stdout)
        return "inputs_builder_assistant", next_prompt, log_dict

    # round 1 is passed; parse the coverage
    code_coverage, coverage_report = _parse_code_coverage(first_round_stdout)

    # prepone the coverage checking
    if code_coverage < code_coverage_threshold:
        next_prompt = _inputs_build_increase_coverage_prompt(
            method, inputs_builder_code, first_round_stdout, code_coverage_threshold)
        return "inputs_builder_assistant", next_prompt, log_dict

    second_round_stdout = _run_execution_r2(inputs_builder_code, 
                                            inputs_builder_path, 
                                            postconditions, 
                                            method.start_line,
                                            method.end_line,
                                            method.file)
    log_dict["r2_stdout"] = second_round_stdout

    if "Finished without exception." not in second_round_stdout:
        next_prompt = _judge_prompt_r2(method, 
                                       postconditions, 
                                       inputs_builder_code, 
                                       second_round_stdout)
        return "judge_assistant", next_prompt, log_dict

    __res_r3 = _run_execution_r3(inputs_builder_code, 
                                 inputs_builder_path, 
                                 postconditions, method,
                                 selected_mut_indexs)
    third_round_stdout, third_round_mutant, third_round_mut_idx = __res_r3

    log_dict["r3_stdout"] = third_round_stdout
    log_dict["r3_mutant"] = third_round_mutant
    log_dict["r3_mut_idx"] = third_round_mut_idx

    if third_round_stdout and "icontract.errors.ViolationError" not in third_round_stdout:
        next_prompt = _judge_prompt_r3(method,
                                       postconditions, 
                                       inputs_builder_code,
                                       third_round_mutant,
                                       third_round_stdout,
                                       coverage_report)
        return "judge_mutant_assistant", next_prompt, log_dict

    return "yield", None, log_dict


def _parse_yaml(yaml_content: str, expected_keys: List[str]) -> Dict[str, str]:
    try:
        data = yaml.safe_load(yaml_content)
    except Exception:
        return None
    if not isinstance(data, dict):
        return None
    if set(data.keys()) != set(expected_keys):
        return None
    if any(not isinstance(v, str) for v in data.values()):
        return None
    return data


def analyze_judge_result(method: Method, postconditions: str, 
                         inputs_builder_code: str, 
                         judge_result: str, prev_exec_log: str,
                         prev_prompt: str) -> Tuple[str, str]:
    
    judge_result = _parse_yaml(judge_result, ["summary", "fault"])

    if not judge_result or judge_result["fault"].strip() not in ["inputs", "postcondition"]:
        # invalid output from judge, rollback
        return "judge_assistant", prev_prompt

    flag = judge_result["fault"].strip()

    if flag == "inputs":
        next_agent = "inputs_builder_assistant"
        next_prompt = _inputs_build_refine_prompt(
            method, inputs_builder_code, prev_exec_log)
    elif flag == "postcondition":
        next_agent = "generation_assistant"
        next_prompt = _generation_refine_prompt(
            method, postconditions, prev_exec_log)
    return next_agent, next_prompt


def analyze_judge_mutant_result(method: Method, postconditions: str, 
                                inputs_builder_code: str, 
                                judge_result: str, prev_mutant: str, prev_stdout: str,
                                prev_prompt: str) -> Tuple[str, str]:

    judge_result = _parse_yaml(judge_result, ["evidence_summary", "fix_suggestion", "responsible"])

    if not judge_result or judge_result["responsible"].strip() not in ["inputs", "postcondition", "bug"]:
        # invalid output from judge, rollback
        return "judge_mutant_assistant", prev_prompt

    prev_exec_feedback = judge_result["fix_suggestion"].strip()
    flag = judge_result["responsible"].strip()
    
    if flag == "bug":
        return "resample_mutants", None

    if flag == "inputs":
        next_agent = "inputs_builder_assistant"
        next_prompt = _inputs_build_refine_prompt(
            method, inputs_builder_code, prev_exec_feedback)
    elif flag == "postcondition":
        next_agent = "generation_assistant"
        next_prompt = _generation_refine_prompt(
            method, postconditions, prev_exec_feedback)
    return next_agent, next_prompt


async def _call_agent_once(agent: AssistantAgent, prompt: str) -> str:
    """
    Call an AssistantAgent with exactly ONE input message (no history kept),
    and return the assistant's textual output.
    """
    msgs = [TextMessage(content=prompt, source="user")]

    # AssistantAgent in autogen_agentchat returns a result object whose .messages
    # contains generated messages. We only take the last message content.
    token = CancellationToken()
    try:
        result = await agent.on_messages(msgs, token)
    except BaseException as e:
        raise RuntimeError(f"{str(e)}\n\n{prompt}")
    if not getattr(result, "chat_message", None):
        return ""
    last = result.chat_message
    return getattr(last, "content", "") or ""


async def run_agent(
    method: Method,
    model: str = "gpt-5-mini",
    max_rounds: int = 20,
    print_stdout: bool = False,
    mutant_sample_num: int = 5,
    collect_logs: bool = False,
) -> Tuple[str, List[dict], Optional[str]]:
    
    load_mutation(method) # many mutants are loaded

    generation_assistant = get_llm_based_agent(
        name="generation_assistant", model=model)
    icontract_grammar_assistant = get_llm_based_agent(
        name="icontract_grammar_assistant", model=model)
    inputs_builder_assistant = get_llm_based_agent(
        name="inputs_builder_assistant", model=model)
    judge_assistant = get_llm_based_agent(
        name="judge_assistant", model=model)
    judge_mutant_assistant = get_llm_based_agent(
        name="judge_mutant_assistant", model=model)

    team = SelectorGroupChat(
        participants=[generation_assistant, 
                      icontract_grammar_assistant,
                      inputs_builder_assistant, 
                      judge_assistant,
                      judge_mutant_assistant],
        model_client=client(model) # TODO: tmp. could raise error with some model names
    )

    agents: Dict[str, AssistantAgent] = {
        "generation_assistant": generation_assistant,
        "icontract_grammar_assistant": icontract_grammar_assistant,
        "inputs_builder_assistant": inputs_builder_assistant,
        "judge_assistant": judge_assistant,
        "judge_mutant_assistant": judge_mutant_assistant,
    }

    postconditions: str = ""
    inputs_builder_code: str = ""
    log_dict: Dict[str, str] = {}
    history: List[Dict[str, str]] = []

    last_lint_passed: str = ""
    last_corr_passed: str = ""

    selected_mut_indexs = list(range(len(method.mutants_4a)))
    random.shuffle(selected_mut_indexs)
    selected_mut_indexs = selected_mut_indexs[: mutant_sample_num]
    banned_mut_indexs: List[int] = []

    log_lines: List[str] = []

    def _simplify_prompt_for_print(prompt: str) -> str:
        if not prompt or not prompt.startswith("Code context"):
            return prompt
        lines = prompt.split("\n")
        for li_idx, li in enumerate(lines):
            if li.lower().startswith("target method"):
                return "\n".join([lines[0], "..."] + lines[li_idx: ])
        return prompt

    def _print(title: str, agent: str, round_id: int, content: str) -> None:
        header = f"===== {title} for AGENT: {agent} (round {round_id}) ====="
        body = content or ""
        msg = header + "\n" + body

        if print_stdout:
            print(header)
            print(body)

        if collect_logs:
            log_lines.append(msg)

    def _print_execution(round_id: int, pc: str, ib: str, log_dict: Dict[str, str]) -> None:
        parts = [
            f"===== EXECUTION postconditions (round {round_id}) =====",
            pc or "",
            f"===== EXECUTION inputs_builder_code (round {round_id}) =====",
            ib or "",
            f"===== EXECUTION stdout r1 (round {round_id}) =====",
            (log_dict or {}).get("r1_stdout") or "",
            f"===== EXECUTION stdout r2 (round {round_id}) =====",
            (log_dict or {}).get("r2_stdout") or "",
            f"===== EXECUTION mutant r3 (round {round_id}) =====",
            (log_dict or {}).get("r3_mutant") or "",
            f"===== EXECUTION stdout r3 (round {round_id}) =====",
            (log_dict or {}).get("r3_stdout") or "",
        ]
        msg = "\n".join(parts)

        if print_stdout:
            print(msg)

        if collect_logs:
            log_lines.append(msg)

    def _run_execution():
        nonlocal next_agent, next_prompt, log_dict, last_corr_passed

        next_agent, next_prompt, log_dict = run_execution(
            method, postconditions, inputs_builder_code, selected_mut_indexs)
        _print_execution(round_id, postconditions, inputs_builder_code, log_dict)
        if log_dict["r2_stdout"] and "Finished without exception." in log_dict["r2_stdout"]:
            last_corr_passed = postconditions

    def _update_selected_mut_indexs():
        nonlocal banned_mut_indexs, selected_mut_indexs

        if print_stdout is True:
            traversed = 0
            total_candidates = len(candidate_mut_indexs)
            pbar = tqdm(
                total=mutant_sample_num,
                initial=len(selected_mut_indexs),
                desc="Selecting mutants",
                unit="mut",
                dynamic_ncols=True,
                leave=True,
            )
        for mut_idx in candidate_mut_indexs:
            mut_stdout = _run_execution_single_mut(inputs_builder_code, method, mut_idx)
            if "Finished without exception." in mut_stdout:
                selected_mut_indexs.append(mut_idx)
            elif "[TIMEOUT]" in mut_stdout:
                # once a mutant is timeout, it should be banned
                banned_mut_indexs.append(mut_idx)
            if len(selected_mut_indexs) >= mutant_sample_num:
                break
            if print_stdout is True:
                traversed += 1
                if "Finished without exception." in mut_stdout:
                    pbar.update(1)
                pbar.set_postfix_str(
                    f"scanned={traversed}/{total_candidates} | "
                    f"selected={len(selected_mut_indexs)}/{mutant_sample_num}")
        if print_stdout is True:
            pbar.close()

    # 3) Main loop
    for round_id in range(max_rounds):
        if round_id == 0:
            next_agent = "generation_assistant"
            next_prompt = init_generation_prompt(method)

        _print("PROMPT", next_agent, round_id, _simplify_prompt_for_print(next_prompt) or "")
        _curr_agent = next_agent # for logging

        if next_agent in ["generation_assistant", "icontract_grammar_assistant"]:
            postconditions = await _call_agent_once(agents[next_agent], next_prompt)
            _print("RESPONSE", next_agent, round_id, postconditions)
            
            lint_message = grammar_verify(method.content, postconditions)
            if "No issues found" in lint_message:
                last_lint_passed = postconditions
                if not inputs_builder_code:
                    next_agent = "inputs_builder_assistant"
                    next_prompt = init_inputs_builder_prompt(method)
                else:
                    _run_execution()
            else:
                next_agent = "icontract_grammar_assistant"
                next_prompt = _grammar_prompt(method.content, postconditions, lint_message)

        elif next_agent == "inputs_builder_assistant":
            inputs_builder_code = await _call_agent_once(agents[next_agent], next_prompt)
            _print("RESPONSE", next_agent, round_id, inputs_builder_code)
            _run_execution()
            # if updated inputs builder is runnable with original method,
            # update selected_mut_indexs
            if log_dict["r1_stdout"] and "Finished without exception." in log_dict["r1_stdout"]:
                candidate_mut_indexs = [i for i in range(len(method.mutants_4a)) 
                                        if i not in selected_mut_indexs + banned_mut_indexs]
                random.shuffle(candidate_mut_indexs)
                candidate_mut_indexs = selected_mut_indexs + candidate_mut_indexs
                selected_mut_indexs = []
                if next_agent != "yield":
                    _update_selected_mut_indexs()

        elif next_agent == "judge_assistant":
            judge_result = await _call_agent_once(agents[next_agent], next_prompt)
            _print("RESPONSE", next_agent, round_id, judge_result)

            next_agent, next_prompt = analyze_judge_result(
                method, postconditions, inputs_builder_code, judge_result, 
                log_dict["r2_stdout"], next_prompt)

        elif next_agent == "judge_mutant_assistant":
            judge_result = await _call_agent_once(agents[next_agent], next_prompt)
            _print("RESPONSE", next_agent, round_id, judge_result)

            next_agent, next_prompt = analyze_judge_mutant_result(
                method, postconditions, inputs_builder_code, judge_result, 
                log_dict["r3_mutant"], log_dict["r3_stdout"], next_prompt)
            
            if next_agent == "resample_mutants":
                _print("Remove Mutant", next_agent, round_id, str(log_dict["r3_mut_idx"]))
                banned_mut_indexs.append(log_dict["r3_mut_idx"])
                if log_dict["r3_mut_idx"] in selected_mut_indexs:
                    selected_mut_indexs.remove(log_dict["r3_mut_idx"])
                candidate_mut_indexs = [i for i in range(len(method.mutants_4a)) 
                                        if i not in selected_mut_indexs + banned_mut_indexs]
                random.shuffle(candidate_mut_indexs)
                _update_selected_mut_indexs()
                _run_execution()

        elif next_agent == "yield":
            break

        else:
            raise ValueError(f"Unexpected next_agent: {next_agent!r}")
        
        history.append({"round": round_id, 
                        "curr_agent": _curr_agent, 
                        "next_agent": next_agent, 
                        "postcond": postconditions,
                        "inputs": inputs_builder_code})

        _print("The Next", next_agent, round_id, None)

    res = last_corr_passed if last_corr_passed else (
        last_lint_passed if last_lint_passed else postconditions)
    
    logs_str = "\n".join(log_lines)

    if collect_logs:
        return res, history, logs_str

    return res, history


if __name__ == "__main__":
    method_path = "data/step/8.benchmark/keon--algorithms--hailstone.json"
    with open(method_path) as file:
        method = Method.from_dict(json.load(file))

    with repository_reproduct(method.repo) as repo_dir:
        model = "gpt-5-mini"

        print(repo_dir)

        postconditions, history = asyncio.run(
            run_agent(method, model, print_stdout=True))

        print(json.dumps(history, indent=2))
