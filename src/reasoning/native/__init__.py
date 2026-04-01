import json
import os
from pathlib import Path
from typing import Iterable, List, Tuple

from src.clone import repository_reproduct
from src.ds import Method
from src.inject import postcond_inj
from src.pool import run_with_pool_file_monitor
from src.postcond import (
    is_local_crash,
    postcond_checking,
    response_post_process,
)
from src.postcond.prompt.infile import ICONTRACT_EXAMPLES, JML_EXAMPLES
from src.postcond.prompt.v2 import (
    ICONTRACT_TARGET_DESC,
    JML_GARMMAR_RESTRICTION,
    JML_TARGET_DESC,
)
from src.runner import testsuite_run
from src.util import get_uuid7, read_code


PROMPT_TEMPLATE = (
    "## Code Context\n"
    "```\n"
    "{code_context}\n"
    "```\n"
    "## Target Method\n"
    "```\n"
    "{target_method}\n"
    "```\n"
    "{grammar_examples}\n"
    "## Guideline\n"
    "Above is the {lang} code context and target method. "
    "You should generate {dsl_name} format postconditions for "
    "this method `{method_name}`.\n"
    "{grammar_restriction}"
    "Try to generate correct and complete postconditions.\n"
    "Note that your response should only contain {target_desc}."
)


def _optional_list(values):
    if any(value is not None for value in values):
        return values
    return None


def _save_method(method: Method, output_path: str):
    with open(output_path, "w") as file:
        json.dump(method.to_dict(), file, indent=2)


def _indent_of(line: str) -> str:
    return line[: len(line) - len(line.lstrip())]


def _python_placeholder_indent(method: Method, code_lines: List[str]) -> str:
    for line in code_lines[method.body_start_line - 1: method.end_line]:
        if line.strip():
            return _indent_of(line)
    header_last_line = code_lines[method.body_start_line - 2]
    return _indent_of(header_last_line) + "    "


def _target_method_skeleton(method: Method, code_str: str) -> str:
    code_lines = code_str.split("\n")
    header_lines = code_lines[method.start_line - 1: method.body_start_line - 1]
    if method.repo.language == "python":
        indent = _python_placeholder_indent(method, code_lines)
        return "\n".join(header_lines + [f"{indent}..."])
    if method.repo.language == "java":
        method_indent = _indent_of(code_lines[method.start_line - 1])
        placeholder_indent = method_indent + "    "
        return "\n".join(header_lines + [f"{placeholder_indent}...", f"{method_indent}}}"])
    raise NotImplementedError()


def _code_context_without_target_body(method: Method, code_str: str) -> str:
    skeleton = _target_method_skeleton(method, code_str)
    if method.content not in code_str:
        raise RuntimeError(f"Failed to locate target method in file for {method.rlid}.")
    return code_str.replace(method.content, skeleton, 1)


def prompt_native(method: Method) -> str:
    lang = method.repo.language
    if lang == "python":
        dsl_name = "icontract"
        grammar_examples = ICONTRACT_EXAMPLES
        target_desc = ICONTRACT_TARGET_DESC
        grammar_restriction = ""
    elif lang == "java":
        dsl_name = "JML"
        grammar_examples = JML_EXAMPLES
        target_desc = JML_TARGET_DESC
        grammar_restriction = JML_GARMMAR_RESTRICTION
    else:
        raise NotImplementedError()

    code_str, _ = read_code(method.file)
    target_method = _target_method_skeleton(method, code_str)
    code_context = _code_context_without_target_body(method, code_str)

    return PROMPT_TEMPLATE.format(
        code_context=code_context,
        target_method=target_method,
        grammar_examples=grammar_examples,
        lang=lang,
        dsl_name=dsl_name,
        method_name=method.name,
        target_desc=target_desc,
        grammar_restriction=grammar_restriction,
    )


BEDROCK_METADATA_FILE = "bedrock_config.json"
BEDROCK_INPUT_FILE = "bedrock_input.jsonl"
METHODS_DIR = "methods"
KFS = ["jml_fail", "icontract_fail"]
NO_REASONING_TRACE = "[no reasoning trace returned by model]"


def _supports_reasoning_trace(model_name: str) -> bool:
    return model_name == "deepseek-reasoner"


def default_generate_num(model_name: str) -> int:
    if model_name in {"deepseek-reasoner", "gpt-oss-120b"}:
        return 2
    raise NotImplementedError(f"Unsupported reasoning model: {model_name}")


def default_work_dir(model_name: str) -> str:
    return f"data/reasoning/9.{model_name}--native-bedrock"


def _method_file_name(method: Method) -> str:
    repo_name = method.repo.github_path.replace("/", "--")
    return f"{repo_name}--{method.rlid}.json"


def _method_output_path(work_dir: str, method: Method) -> str:
    return os.path.join(work_dir, METHODS_DIR, _method_file_name(method))


def _record_id(method: Method, generate_idx: int) -> str:
    repo_name = method.repo.github_path.replace("/", "--")
    return f"{repo_name}--{method.rlid}--{generate_idx}"


def _parse_record_id(record_id: str) -> Tuple[str, int]:
    method_id, generate_idx = record_id.rsplit("--", 1)
    return f"{method_id}.json", int(generate_idx)


def _prepare_dirs(work_dir: str):
    os.makedirs(os.path.join(work_dir, METHODS_DIR), exist_ok=True)


def _load_method_file(file_path: str) -> Method:
    with open(file_path) as file:
        return Method.from_dict(json.load(file))


def _load_selected_benchmark(
        input_dir: str,
        model_name: str,
        task_num: int = 1,
        task_idx: int = 0,
        lang: str = None,
        limit: int = None) -> List[Method]:
    methods: List[Method] = []
    for file_name in os.listdir(input_dir):
        if file_name.endswith(".json"):
            with open(f"{input_dir}/{file_name}") as file:
                methods.append(Method.from_dict(json.load(file)))

    methods.sort(key=lambda method: (
        -method.test_time * len(method.mutants),
        method.repo.github_path,
        method.rlid,
    ))
    methods = [
        method for idx, method in enumerate(methods)
        if idx % task_num == task_idx
    ]
    if lang is not None:
        methods = [method for method in methods if method.repo.language == lang]
    if limit is not None:
        methods = methods[: limit]

    for method in methods:
        method.task_version = "reasoning-native-bedrock"
        method.model_name = model_name
        method.generate_num = default_generate_num(model_name)
        method.prompting = "reasoning-native-bedrock"

    return methods


def _bedrock_request_for_method(method: Method) -> dict:
    if method.model_name == "deepseek-reasoner":
        return {
            "messages": [{"role": "user", "content": [{"text": method.prompt}]}],
            "inferenceConfig": {"temperature": 1},
            "additionalModelRequestFields": {"reasoning_config": "high"},
            "performanceConfig": {"latency": "standard"},
        }
    if method.model_name == "gpt-oss-120b":
        return {
            "messages": [{"role": "user", "content": [{"text": method.prompt}]}],
            "performanceConfig": {"latency": "standard"},
        }
    raise NotImplementedError(f"Unsupported reasoning model: {method.model_name}")


def _bedrock_config(model_name: str) -> dict:
    config = {
        "workflow": "reasoning-native-bedrock",
        "invocation_type": "Converse",
        "model_name": model_name,
        "generate_num": default_generate_num(model_name),
        "notes": [
            "Each JSONL row is a Bedrock batch record with recordId and modelInput.",
            "Create the Bedrock batch job with invocation type Converse.",
            "Select the actual Bedrock model or inference profile ID manually when creating the job.",
        ],
    }
    if model_name == "deepseek-reasoner":
        config["suggested_model_id"] = "deepseek.v3.2"
    elif model_name == "gpt-oss-120b":
        config["suggested_model_id"] = "openai.gpt-oss-120b-1:0"
        config["notes"].append(
            "GPT-OSS responses on Bedrock may not include a separate reasoning trace; merge fills a placeholder when absent."
        )
    else:
        raise NotImplementedError(f"Unsupported reasoning model: {model_name}")
    return config


def _iter_method_files(work_dir: str) -> Iterable[str]:
    methods_dir = os.path.join(work_dir, METHODS_DIR)
    if not os.path.exists(methods_dir):
        return []
    return [
        os.path.join(methods_dir, file_name)
        for file_name in sorted(os.listdir(methods_dir))
        if file_name.endswith(".json")
    ]


def _prepare_prompt(method: Method) -> Method:
    with repository_reproduct(method.repo):
        method.prompt = prompt_native(method)
    return method


def _write_batch_input(work_dir: str, methods: List[Method]) -> int:
    records = []
    for method in methods:
        for generate_idx in range(method.generate_num):
            records.append({
                "recordId": _record_id(method, generate_idx),
                "modelInput": _bedrock_request_for_method(method),
            })

    output_path = os.path.join(work_dir, BEDROCK_INPUT_FILE)
    with open(output_path, "w") as file:
        for record in records:
            file.write(json.dumps(record) + "\n")
    return len(records)


def prompt_workflow(
        input_dir: str,
        work_dir: str,
        model_name: str,
        task_num: int = 1,
        task_idx: int = 0,
        lang: str = None,
        limit: int = None) -> dict:
    _prepare_dirs(work_dir)
    methods = _load_selected_benchmark(
        input_dir=input_dir,
        model_name=model_name,
        task_num=task_num,
        task_idx=task_idx,
        lang=lang,
        limit=limit,
    )

    initialized_methods = []
    existing_method_count = 0
    for method in methods:
        output_path = _method_output_path(work_dir, method)
        if os.path.exists(output_path):
            existing_method_count += 1
            continue
        method = _prepare_prompt(method)
        _save_method(method, output_path)
        initialized_methods.append(method)

    batch_record_count = _write_batch_input(work_dir, initialized_methods)
    with open(os.path.join(work_dir, BEDROCK_METADATA_FILE), "w") as file:
        json.dump(_bedrock_config(model_name), file, indent=2)

    return {
        "initialized_method_count": len(initialized_methods),
        "existing_method_count": existing_method_count,
        "batch_record_count": batch_record_count,
        "work_dir": work_dir,
        "batch_input_path": os.path.join(work_dir, BEDROCK_INPUT_FILE),
    }


def _try_parse_json(value):
    if isinstance(value, str):
        stripped = value.strip()
        if stripped.startswith("{") or stripped.startswith("["):
            try:
                return json.loads(stripped)
            except json.JSONDecodeError:
                return value
    return value


def _unwrap_batch_payload(payload):
    payload = _try_parse_json(payload)
    changed = True
    while changed:
        changed = False
        if isinstance(payload, dict):
            for key in ("modelOutput", "output", "result", "body"):
                if key in payload:
                    candidate = _try_parse_json(payload[key])
                    if candidate is not payload:
                        payload = candidate
                        changed = True
                        break
    return payload


def _stringify(value) -> str:
    if value is None:
        return None
    if isinstance(value, str):
        return value
    return json.dumps(value, ensure_ascii=False)


def _extract_reasoning_text(value):
    value = _try_parse_json(value)
    if isinstance(value, str):
        return value
    if isinstance(value, dict):
        if "reasoningText" in value:
            return _extract_reasoning_text(value["reasoningText"])
        if "text" in value and isinstance(value["text"], str):
            return value["text"]
        if "thinking" in value and isinstance(value["thinking"], str):
            return value["thinking"]
        if "reasoningContent" in value:
            return _extract_reasoning_text(value["reasoningContent"])
        if "redactedContent" in value:
            return "[redacted reasoning]"
    if isinstance(value, list):
        parts = [_extract_reasoning_text(item) for item in value]
        parts = [part for part in parts if part]
        if parts:
            return "\n\n".join(parts)
    return None


def _extract_text_and_thought(payload) -> Tuple[str, str]:
    payload = _unwrap_batch_payload(payload)
    response_parts = []
    thought_parts = []

    if isinstance(payload, dict):
        message = None
        if isinstance(payload.get("output"), dict):
            output = payload["output"]
            if isinstance(output.get("message"), dict):
                message = output["message"]
        if message is None and isinstance(payload.get("message"), dict):
            message = payload["message"]
        if message is not None and isinstance(message.get("content"), list):
            for block in message["content"]:
                if not isinstance(block, dict):
                    continue
                reasoning_content = block.get("reasoningContent")
                if isinstance(block.get("text"), str):
                    response_parts.append(block["text"])
                if reasoning_content is not None:
                    reasoning = _extract_reasoning_text(reasoning_content)
                    if reasoning:
                        thought_parts.append(reasoning)
                elif block.get("type") == "thinking":
                    reasoning = block.get("thinking") or block.get("text")
                    if reasoning:
                        thought_parts.append(reasoning)
                elif block.get("type") == "redacted_thinking":
                    thought_parts.append("[redacted reasoning]")

        if not response_parts and isinstance(payload.get("content"), list):
            for block in payload["content"]:
                if not isinstance(block, dict):
                    continue
                if isinstance(block.get("text"), str):
                    response_parts.append(block["text"])
                reasoning_content = block.get("reasoningContent")
                if reasoning_content is not None:
                    reasoning = _extract_reasoning_text(reasoning_content)
                    if reasoning:
                        thought_parts.append(reasoning)

        if not response_parts and isinstance(payload.get("choices"), list) and payload["choices"]:
            choice = payload["choices"][0]
            if isinstance(choice, dict):
                if isinstance(choice.get("text"), str):
                    response_parts.append(choice["text"])
                if isinstance(choice.get("message"), dict):
                    msg = choice["message"]
                    if isinstance(msg.get("content"), str):
                        response_parts.append(msg["content"])
                    reasoning = msg.get("reasoning_content") or msg.get("reasoningContent")
                    reasoning = _extract_reasoning_text(reasoning)
                    if reasoning:
                        thought_parts.append(reasoning)

        if not response_parts and isinstance(payload.get("text"), str):
            response_parts.append(payload["text"])

        if not thought_parts:
            reasoning = payload.get("reasoning_content") or payload.get("reasoningContent")
            reasoning = _extract_reasoning_text(reasoning)
            if reasoning:
                thought_parts.append(reasoning)

    response = "".join(part for part in response_parts if part) or None
    thought = "\n\n".join(part for part in thought_parts if part) or None
    return response, thought


def _normalize_thought(model_name: str, thought: str) -> str:
    if thought is not None:
        return thought
    if _supports_reasoning_trace(model_name):
        return None
    return NO_REASONING_TRACE


def _extract_usage(payload) -> Tuple[int, int, int]:
    parsed_payload = _try_parse_json(payload)
    usage = parsed_payload.get("usage") if isinstance(parsed_payload, dict) else None
    if not isinstance(usage, dict):
        payload = _unwrap_batch_payload(payload)
        if not isinstance(payload, dict):
            return None, None, None
        usage = payload.get("usage")
    if not isinstance(usage, dict):
        return None, None, None
    input_tokens = usage.get("inputTokens", usage.get("prompt_tokens"))
    output_tokens = usage.get("outputTokens", usage.get("completion_tokens"))
    reasoning_tokens = usage.get("reasoningTokens")
    if reasoning_tokens is None:
        details = usage.get("completionTokensDetails") or usage.get("completion_tokens_details")
        if isinstance(details, dict):
            reasoning_tokens = details.get("reasoningTokens", details.get("reasoning_tokens"))
    return input_tokens, output_tokens, reasoning_tokens


def _iter_batch_output_records(batch_output_path: str):
    path = Path(batch_output_path)
    if path.is_file():
        files = [path]
    else:
        files = sorted(path.rglob("*.jsonl")) + sorted(path.rglob("*.json"))
    for file_path in files:
        with open(file_path) as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                yield json.loads(line)


def _has_full_outputs(values, generate_num: int) -> bool:
    return (
        isinstance(values, list)
        and len(values) == generate_num
        and all(value is not None for value in values)
    )


def _can_merge_method(method: Method) -> bool:
    return (
        method.prompt is not None
        and method.responses is None
        and method.thoughts is None
    )


def _load_methods_from_work_dir(work_dir: str) -> List[Method]:
    return [_load_method_file(method_path) for method_path in _iter_method_files(work_dir)]


def cal_corr_and_comp_counts(methods: List[Method]) -> Tuple[int, int]:
    corr_count = 0
    comp_count = 0
    corr_list = []
    comp_list = []
    for method in methods:
        m_id = method.repo.github_path.replace("/", "--") + "--" + method.rlid
        if method.postcond_corr is None or method.mutant_kill is None:
            continue
        for p_idx, (corr_res, comp_res) in enumerate(zip(method.postcond_corr, method.mutant_kill)):
            if corr_res == "passed":
                corr_list.append((m_id, p_idx))
                corr_count += 1
                ref_mutant_kill = method.ref_mutant_kill or []
                assert len(comp_res) == 0 or len(comp_res) == len(ref_mutant_kill)
                if all(ref_flag not in KFS or flag in KFS for flag, ref_flag in zip(comp_res, ref_mutant_kill)):
                    comp_list.append((m_id, p_idx))
                    comp_count += 1
    import random
    random.shuffle(corr_list)
    random.shuffle(comp_list)
    print("Corr")
    print("\n".join([f"{m_id} {p_idx}" for m_id, p_idx in corr_list]))
    print("Comp")
    print("\n".join([f"{m_id} {p_idx}" for m_id, p_idx in comp_list]))
    return corr_count, comp_count


def metric_workflow(work_dir: str, lang: str = None) -> dict:
    methods = _load_methods_from_work_dir(work_dir)
    if lang is not None:
        methods = [method for method in methods if method.repo.language == lang]
    evaluated_methods = [method for method in methods if method.postcond_corr is not None]

    total_postcond_count = sum(len(method.postcond_corr) for method in evaluated_methods)
    corr_count, comp_count = cal_corr_and_comp_counts(evaluated_methods)

    return {
        "work_dir": work_dir,
        "lang": lang,
        "method_count": len(methods),
        "evaluated_method_count": len(evaluated_methods),
        "postcondition_count": total_postcond_count,
        "correctness_count": corr_count,
        "completeness_count": comp_count,
        "correctness": None if total_postcond_count == 0 else corr_count / total_postcond_count,
        "completeness": None if total_postcond_count == 0 else comp_count / total_postcond_count,
    }


def merge_batch_outputs(work_dir: str, batch_output_path: str) -> dict:
    methods_dir = os.path.join(work_dir, METHODS_DIR)
    grouped_records = {}
    duplicates = set()
    merged_record_count = 0
    merged_method_count = 0
    unresolved = []

    for record in _iter_batch_output_records(batch_output_path):
        record_id = record.get("recordId") or record.get("custom_id")
        if record_id is None:
            unresolved.append({"reason": "missing-record-id", "record": record})
            continue

        method_file_name, generate_idx = _parse_record_id(record_id)
        grouped = grouped_records.setdefault(method_file_name, {})
        if generate_idx in grouped:
            duplicates.add((method_file_name, generate_idx))
        grouped[generate_idx] = record

    for method_file_name, records_by_idx in grouped_records.items():
        method_path = os.path.join(methods_dir, method_file_name)
        record_ids = [
            (record.get("recordId") or record.get("custom_id"))
            for _, record in sorted(records_by_idx.items())
        ]
        if any((method_file_name, idx) in duplicates for idx in records_by_idx):
            for record_id in record_ids:
                unresolved.append({"reason": "duplicate-record", "recordId": record_id})
            continue
        if not os.path.exists(method_path):
            for record_id in record_ids:
                unresolved.append({"reason": "missing-method-file", "recordId": record_id})
            continue

        method = _load_method_file(method_path)
        if not _can_merge_method(method):
            for record_id in record_ids:
                unresolved.append({"reason": "method-not-mergeable", "recordId": record_id})
            continue

        expected_indices = set(range(method.generate_num))
        if set(records_by_idx) != expected_indices:
            for record_id in record_ids:
                unresolved.append({
                    "reason": "incomplete-method-records",
                    "recordId": record_id,
                    "expected_generate_num": method.generate_num,
                })
            continue

        responses = [None] * method.generate_num
        thoughts = [None] * method.generate_num
        request_input_tokens = [None] * method.generate_num
        request_output_tokens = [None] * method.generate_num
        request_reasoning_tokens = [None] * method.generate_num
        request_costs = [None] * method.generate_num
        parse_failed = False

        for generate_idx in range(method.generate_num):
            record = records_by_idx[generate_idx]
            record_id = record.get("recordId") or record.get("custom_id")
            payload = record.get("modelOutput", record)
            response, thought = _extract_text_and_thought(payload)
            thought = _normalize_thought(method.model_name, thought)
            input_tokens, output_tokens, reasoning_tokens = _extract_usage(record)
            if response is None or thought is None:
                unresolved.append({
                    "reason": "missing-response-or-thought",
                    "recordId": record_id,
                })
                parse_failed = True
                continue

            responses[generate_idx] = response
            thoughts[generate_idx] = thought
            request_input_tokens[generate_idx] = input_tokens
            request_output_tokens[generate_idx] = output_tokens
            request_reasoning_tokens[generate_idx] = reasoning_tokens

        if parse_failed:
            continue

        method.responses = responses
        method.thoughts = thoughts
        method.request_input_tokens = _optional_list(request_input_tokens)
        method.request_output_tokens = _optional_list(request_output_tokens)
        method.request_reasoning_tokens = _optional_list(request_reasoning_tokens)
        method.request_costs = _optional_list(request_costs)

        _save_method(method, method_path)
        merged_record_count += method.generate_num
        merged_method_count += 1

    merge_report = {
        "merged_record_count": merged_record_count,
        "merged_method_count": merged_method_count,
        "unresolved": unresolved,
        "work_dir": work_dir,
    }
    with open(os.path.join(work_dir, "merge_report.json"), "w") as file:
        json.dump(merge_report, file, indent=2)
    return merge_report


def _evaluate_method(method: Method) -> Method:
    if method.responses is None or any(response is None for response in method.responses):
        return method

    with repository_reproduct(method.repo):
        code_str, _ = read_code(method.file)
        method.postconds = [response_post_process(response) for response in method.responses]
        method.postcond_corr = []
        method.incorr_msgs = []
        method.mutant_kill = []
        excluded_tests = method.repo.failed_tests
        lang = method.repo.language

        for postcond in method.postconds:
            corr_stdout = ""
            if not postcond_checking(method, postcond):
                postcond_code_src, hot_range = None, None
            elif not postcond.strip():
                postcond_code_src, hot_range = None, None
            else:
                postcond_code_src, hot_range = postcond_inj(
                    method=method,
                    code_str=code_str,
                    postcond=postcond,
                    need_hot_range=True,
                )

            if not postcond_code_src:
                corr_flag = "compile_failure"
            else:
                run_result = testsuite_run(
                    lang=lang,
                    included_tests=method.cover_tests,
                    excluded_tests=excluded_tests,
                    replace_file_path=method.file,
                    replace_file_content=postcond_code_src,
                    need_coverage=False,
                    timeout=30,
                )
                corr_stdout = run_result.stdout or ""
                corr_flag = run_result.to_flag()
                if corr_flag == "failed" and hot_range is not None:
                    if is_local_crash(run_result.stdout, hot_range, method.file):
                        corr_flag = "local_crash"

            method.postcond_corr.append(corr_flag)
            method.incorr_msgs.append(corr_stdout)
            mutant_kill = []
            method.mutant_kill.append(mutant_kill)
            if corr_flag != "passed":
                continue

            for mutant in method.mutants:
                postcond_code_src, hot_range = postcond_inj(
                    method=method,
                    code_str=code_str,
                    postcond=postcond,
                    mutant=mutant,
                    need_hot_range=True,
                )
                if not postcond_code_src:
                    comp_flag = "compile_failure"
                else:
                    run_result = testsuite_run(
                        lang=lang,
                        included_tests=method.cover_tests,
                        excluded_tests=excluded_tests,
                        replace_file_path=method.file,
                        replace_file_content=postcond_code_src,
                        need_coverage=False,
                        timeout=30,
                    )
                    comp_flag = run_result.to_flag()
                    if comp_flag == "failed" and hot_range is not None:
                        if is_local_crash(run_result.stdout, hot_range, method.file):
                            comp_flag = "local_crash"
                mutant_kill.append(comp_flag)

    return method


def _evaluate_method_file(method_path: str) -> int:
    method = _load_method_file(method_path)
    method = _evaluate_method(method)
    _save_method(method, method_path)
    return 0


def evaluate_workflow(work_dir: str) -> dict:
    task_name = "reasoning-native-evaluate"
    pi_workdir = os.getenv("PI_WORKDIR")
    if pi_workdir is None:
        log_base = "data/__log"
    else:
        log_base = os.path.join(pi_workdir, "sb_tmp__log")
    log_dir = f"{log_base}/{task_name}--{get_uuid7()}"
    os.makedirs(log_dir, exist_ok=True)

    evaluated = 0
    skipped = 0
    pending = 0
    failed = 0
    params_list = []
    task_names = []
    log_paths = []

    for method_path in _iter_method_files(work_dir):
        method = _load_method_file(method_path)
        if not _has_full_outputs(method.responses, method.generate_num):
            pending += 1
            continue
        if method.postcond_corr is not None and \
                _has_full_outputs(method.incorr_msgs, method.generate_num):
            skipped += 1
            continue

        repo_name = method.repo.github_path.replace("/", "--")
        task_names.append(f"{repo_name}--{method.rlid}")
        log_paths.append(f"{log_dir}/{repo_name}.log")
        params_list.append((method_path,))

    if params_list:
        summary_path = f"{log_dir}/__summary.md"
        rc_map, _ = run_with_pool_file_monitor(
            func=_evaluate_method_file,
            task_names=task_names,
            log_paths=log_paths,
            params_list=params_list,
            processes=min(30, len(params_list)),
            summary_path=summary_path,
            refresh_interval=1,
        )
        evaluated = sum(1 for task_name in task_names if rc_map.get(task_name) == 0)
        failed = len(task_names) - evaluated

    return {
        "evaluated_method_count": evaluated,
        "skipped_method_count": skipped,
        "pending_method_count": pending,
        "failed_method_count": failed,
        "log_dir": log_dir,
        "work_dir": work_dir,
    }