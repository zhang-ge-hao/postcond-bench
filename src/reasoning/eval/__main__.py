import argparse
import ast
import json
import os
import time
import urllib.error
import urllib.request
from copy import deepcopy

from src.clone import repository_reproduct
from src.ds import Method
from src.inject import postcond_inj
from src.pool import run_with_pool_file_monitor
from src.postcond import is_local_crash, postcond_checking
from src.reasoning.eval.prompting import build_method_prompt
from src.runner import testsuite_run
from src.util import get_uuid7, read_code


DEFAULT_VLLM_TIMEOUT_SECONDS = 600.0
DEFAULT_VLLM_MAX_TOKENS = 30000
DEFAULT_VLLM_MAX_RETRIES = 3
DEFAULT_REASONING_TRACE = "[no reasoning trace returned by model]"


def read_benchmark(input_dir: str) -> list[Method]:
    methods: list[Method] = []
    for file_name in sorted(os.listdir(input_dir)):
        if not file_name.endswith(".json"):
            continue
        file_path = os.path.join(input_dir, file_name)
        with open(file_path) as file:
            methods.append(Method.from_dict(json.load(file)))
    return methods


def build_prompt(method: Method, prompt_mode: str) -> str:
    return build_method_prompt(method, prompt_mode)


def strip_code_fences(text: str) -> str:
    stripped = text.strip()
    if not stripped.startswith("```"):
        return text

    lines = stripped.splitlines()
    if len(lines) >= 2 and lines[-1].strip() == "```":
        return "\n".join(lines[1:-1])
    return text


def _char_balance_delta(line: str) -> int:
    single_quote = False
    double_quote = False
    escaped = False
    delta = 0
    for char in line:
        if escaped:
            escaped = False
            continue
        if char == "\\":
            escaped = True
            continue
        if char == "'" and not double_quote:
            single_quote = not single_quote
            continue
        if char == '"' and not single_quote:
            double_quote = not double_quote
            continue
        if single_quote or double_quote:
            continue
        if char in "([{":
            delta += 1
        elif char in ")]}":
            delta -= 1
    return delta


def clean_postconditions(response_text: str) -> str:
    text = strip_code_fences(response_text).replace("\r\n", "\n").replace("\r", "\n")
    raw_lines = text.split("\n")

    kept_lines: list[str] = []
    collecting = False
    balance = 0
    finished_group = False

    for raw_line in raw_lines:
        line = raw_line.rstrip()
        stripped = line.strip()
        if not stripped:
            if collecting and balance > 0:
                kept_lines.append("")
            continue

        if finished_group:
            break

        starts_decorator = stripped.startswith("@icontract.ensure") or stripped.startswith("@icontract.snapshot")
        if starts_decorator:
            collecting = True
            kept_lines.append(line)
            balance = _char_balance_delta(stripped)
            continue

        if collecting and balance > 0:
            kept_lines.append(line)
            balance += _char_balance_delta(stripped)
            continue

        if collecting and balance <= 0:
            finished_group = True
            break

    while kept_lines and not kept_lines[0].strip():
        kept_lines.pop(0)
    while kept_lines and not kept_lines[-1].strip():
        kept_lines.pop()

    cleaned = "\n".join(kept_lines)
    if not cleaned:
        return ""

    min_indent: int | None = None
    for line in cleaned.splitlines():
        if not line.strip():
            continue
        indent = len(line) - len(line.lstrip(" \t"))
        if min_indent is None or indent < min_indent:
            min_indent = indent

    if min_indent is None:
        return ""

    dedented_lines = []
    for line in cleaned.splitlines():
        if not line.strip():
            dedented_lines.append("")
        else:
            dedented_lines.append(line[min_indent:])
    dedented = "\n".join(dedented_lines).strip()
    if not dedented:
        return ""

    snippet = f"{dedented}\n" + "def __icontract_target__():\n    pass\n"
    try:
        ast.parse(snippet)
    except SyntaxError:
        return ""
    return dedented


def _extract_message_text(content) -> str:
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for item in content:
            if isinstance(item, dict):
                text = item.get("text")
                if isinstance(text, str):
                    parts.append(text)
            elif isinstance(item, str):
                parts.append(item)
        return "".join(parts)
    return ""


def _extract_reasoning_text(value):
    if value is None:
        return None
    if isinstance(value, str):
        return value
    if isinstance(value, dict):
        if "reasoningText" in value:
            return _extract_reasoning_text(value["reasoningText"])
        if isinstance(value.get("text"), str):
            return value["text"]
        if isinstance(value.get("thinking"), str):
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


def _extract_completion_result(payload: dict) -> tuple[str, str, int | None, int | None, int | None]:
    choice = payload.get("choices", [{}])[0]
    if not isinstance(choice, dict):
        choice = {}
    message = choice.get("message") or {}
    if not isinstance(message, dict):
        message = {}

    response = _extract_message_text(message.get("content"))
    thought = _extract_reasoning_text(message.get("reasoning_content") or message.get("reasoningContent"))
    if thought is None:
        thought = DEFAULT_REASONING_TRACE

    usage = payload.get("usage")
    if not isinstance(usage, dict):
        usage = {}
    input_tokens = usage.get("prompt_tokens")
    output_tokens = usage.get("completion_tokens")
    reasoning_tokens = None
    details = usage.get("completion_tokens_details")
    if isinstance(details, dict):
        reasoning_tokens = details.get("reasoning_tokens")

    return response or "", thought, input_tokens, output_tokens, reasoning_tokens


def _request_json(url: str, payload: dict, timeout_seconds: float, max_retries: int) -> dict:
    request_body = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=request_body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    backoff_seconds = 1.0
    last_error: Exception | None = None
    for attempt in range(1, max_retries + 1):
        try:
            with urllib.request.urlopen(request, timeout=timeout_seconds) as response:
                return json.loads(response.read().decode("utf-8"))
        except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
            last_error = exc
            if attempt >= max_retries:
                break
            time.sleep(backoff_seconds)
            backoff_seconds *= 2
    raise RuntimeError(f"vLLM request failed after {max_retries} attempts: {last_error}")


def _resolve_model_name(server_url: str, requested_model_name: str) -> str:
    if requested_model_name and requested_model_name != "placeholder-vllm-model":
        return requested_model_name

    models_url = server_url.rstrip("/")
    if models_url.endswith("/v1"):
        models_url += "/models"
    else:
        models_url += "/v1/models"

    with urllib.request.urlopen(models_url, timeout=30) as response:
        payload = json.loads(response.read().decode("utf-8"))

    model_items = payload.get("data")
    if not isinstance(model_items, list) or not model_items:
        raise RuntimeError(f"No models returned from vLLM endpoint: {models_url}")
    model_id = model_items[0].get("id")
    if not isinstance(model_id, str) or not model_id:
        raise RuntimeError(f"Invalid model metadata returned from vLLM endpoint: {models_url}")
    return model_id


def generate_postcondition_responses(
    method: Method,
    server_url: str,
    model_name: str,
) -> list[str]:
    resolved_model_name = _resolve_model_name(server_url, model_name)
    responses: list[str] = []
    thoughts: list[str] = []
    request_input_tokens: list[int | None] = []
    request_output_tokens: list[int | None] = []
    request_reasoning_tokens: list[int | None] = []

    endpoint = server_url.rstrip("/")
    if endpoint.endswith("/v1"):
        endpoint += "/chat/completions"
    else:
        endpoint += "/v1/chat/completions"

    generate_num = method.generate_num or 1
    for _ in range(generate_num):
        payload = {
            "model": resolved_model_name,
            "messages": [{"role": "user", "content": method.prompt}],
            "temperature": 0.6,
            "top_p": 0.95,
            "max_tokens": DEFAULT_VLLM_MAX_TOKENS,
            "chat_template_kwargs": {"enable_thinking": True},
        }
        raw_payload = _request_json(
            url=endpoint,
            payload=payload,
            timeout_seconds=DEFAULT_VLLM_TIMEOUT_SECONDS,
            max_retries=DEFAULT_VLLM_MAX_RETRIES,
        )
        response, thought, input_tokens, output_tokens, reasoning_tokens = _extract_completion_result(raw_payload)
        responses.append(response)
        thoughts.append(thought)
        request_input_tokens.append(input_tokens)
        request_output_tokens.append(output_tokens)
        request_reasoning_tokens.append(reasoning_tokens)

    method.model_name = resolved_model_name
    method.thoughts = thoughts
    method.request_input_tokens = request_input_tokens
    method.request_output_tokens = request_output_tokens
    method.request_reasoning_tokens = request_reasoning_tokens
    return responses


def evaluate_generated_method(method: Method) -> Method:
    if method.responses is None or any(response is None for response in method.responses):
        return method

    with repository_reproduct(method.repo):
        code_str, _ = read_code(method.file)
        method.postconds = [clean_postconditions(response) for response in method.responses]
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

            mutant_kill: list[str] = []
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


def evaluate_method_with_vllm(
    method: Method,
    server_url: str,
    model_name: str,
    prompt_mode: str,
    generate_num: int,
    output_path: str | None = None,
) -> int:
    method.model_name = model_name
    method.prompting = "reasoning-eval-vllm"
    method.generate_num = generate_num
    with repository_reproduct(method.repo):
        method.prompt = build_prompt(method, prompt_mode)
    method.responses = generate_postcondition_responses(
        method=method,
        server_url=server_url,
        model_name=model_name,
    )
    method = evaluate_generated_method(method)

    if output_path is not None:
        with open(output_path, "w") as file:
            json.dump(method.to_dict(), file, indent=2)
    return 0


def build_eval_methods(
    input_dir: str,
    task_num: int | None,
    task_idx: int | None,
    lang: str | None,
    github_path: str | None,
    rlid: str | None,
    limit: int | None,
) -> list[Method]:
    methods = []
    for method in read_benchmark(input_dir):
        if lang is not None and method.repo.language != lang:
            continue
        if github_path is not None and method.repo.github_path != github_path:
            continue
        if rlid is not None and method.rlid != rlid:
            continue

        eval_method = deepcopy(method)
        eval_method.prompt = None
        eval_method.responses = None
        eval_method.postconds = None
        eval_method.postcond_corr = None
        eval_method.incorr_msgs = None
        eval_method.mutant_kill = None
        methods.append(eval_method)

    methods.sort(
        key=lambda method: (
            -method.test_time * len(method.mutants),
            method.repo.github_path,
            method.rlid,
        )
    )

    if task_num is not None and task_idx is not None:
        methods = [method for i, method in enumerate(methods) if i % task_num == task_idx]
    if limit is not None:
        methods = methods[:limit]
    return methods


def run_eval(
    input_dir: str,
    output_dir: str,
    task_num: int | None,
    task_idx: int | None,
    lang: str | None,
    github_path: str | None,
    rlid: str | None,
    limit: int | None,
    processes: int,
    server_url: str,
    model_name: str,
    prompt_mode: str,
    generate_num: int,
) -> dict:
    os.makedirs(output_dir, exist_ok=True)
    log_dir = os.path.join(output_dir, "logs", f"eval--{get_uuid7()}")
    os.makedirs(log_dir, exist_ok=True)

    methods = build_eval_methods(
        input_dir=input_dir,
        task_num=task_num,
        task_idx=task_idx,
        lang=lang,
        github_path=github_path,
        rlid=rlid,
        limit=limit,
    )

    params_list = []
    task_names = []
    log_paths = []
    skipped_existing = 0
    for method in methods:
        repo_name = method.repo.github_path.replace("/", "--")
        file_name = f"{repo_name}--{method.rlid}.json"
        out_path = os.path.join(output_dir, file_name)
        if os.path.exists(out_path):
            with open(out_path) as file:
                saved_method = Method.from_dict(json.load(file))
            if saved_method.postcond_corr is not None:
                skipped_existing += 1
                continue

        task_names.append(f"{repo_name}--{method.rlid}")
        log_paths.append(os.path.join(log_dir, f"{repo_name}.log"))
        params_list.append((method, server_url, model_name, prompt_mode, generate_num, out_path))

    summary_path = os.path.join(log_dir, "__summary.md")
    return_codes, _ = run_with_pool_file_monitor(
        func=evaluate_method_with_vllm,
        task_names=task_names,
        log_paths=log_paths,
        params_list=params_list,
        processes=processes,
        summary_path=summary_path,
        refresh_interval=1,
    )

    failed_tasks = [task_name for task_name, return_code in return_codes.items() if return_code != 0]
    return {
        "input_dir": os.path.abspath(input_dir),
        "output_dir": os.path.abspath(output_dir),
        "log_dir": os.path.abspath(log_dir),
        "summary_path": os.path.abspath(summary_path),
        "scheduled": len(params_list),
        "skipped_existing": skipped_existing,
        "failed_tasks": failed_tasks,
        "server_url": server_url,
        "model_name": model_name,
        "prompt_mode": prompt_mode,
        "generate_num": generate_num,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run benchmark evaluation with a vLLM-backed generation step.")
    parser.add_argument("--input_dir", default="data/step/8.benchmark")
    parser.add_argument("--output_dir", required=True)
    parser.add_argument("--task_num", type=int, default=None)
    parser.add_argument("--task_idx", type=int, default=None)
    parser.add_argument("--lang", default=None)
    parser.add_argument("--github_path", default=None)
    parser.add_argument("--rlid", default=None)
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--processes", type=int, default=1)
    parser.add_argument("--vllm_server_url", default="http://127.0.0.1:8000/v1")
    parser.add_argument("--model_name", default="placeholder-vllm-model")
    parser.add_argument("--prompt_mode", choices=["baseline", "rpg"], default="baseline")
    parser.add_argument("--generate_num", type=int, default=1)
    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    if (args.task_num is None) != (args.task_idx is None):
        raise ValueError("--task_num and --task_idx must be set together.")
    if args.task_num is not None and args.task_idx >= args.task_num:
        raise ValueError("--task_idx must be smaller than --task_num.")

    result = run_eval(
        input_dir=args.input_dir,
        output_dir=args.output_dir,
        task_num=args.task_num,
        task_idx=args.task_idx,
        lang=args.lang,
        github_path=args.github_path,
        rlid=args.rlid,
        limit=args.limit,
        processes=args.processes,
        server_url=args.vllm_server_url,
        model_name=args.model_name,
        prompt_mode=args.prompt_mode,
        generate_num=args.generate_num,
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()