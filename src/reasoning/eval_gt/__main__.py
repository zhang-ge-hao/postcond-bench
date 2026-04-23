import argparse
import json
import os
from copy import deepcopy

from src.clone import repository_reproduct
from src.ds import Method
from src.inject import postcond_inj
from src.pool import run_with_pool_file_monitor
from src.postcond import is_local_crash, postcond_checking
from src.runner import testsuite_run
from src.util import get_uuid7, read_code


def read_benchmark(input_dir: str) -> list[Method]:
    methods: list[Method] = []
    for file_name in sorted(os.listdir(input_dir)):
        if not file_name.endswith(".json"):
            continue
        file_path = os.path.join(input_dir, file_name)
        with open(file_path) as file:
            methods.append(Method.from_dict(json.load(file)))
    return methods


def evaluate_ground_truth_method(method: Method, output_path: str | None = None) -> int:
    lang = method.repo.language
    excluded_tests = method.repo.failed_tests
    ground_truth_postcond = method.ref_postcond

    if not ground_truth_postcond:
        raise ValueError(f"Missing ref_postcond for {method.repo.github_path}::{method.rlid}")

    with repository_reproduct(method.repo):
        code_str, _ = read_code(method.file)
        # Keep the serialized result aligned with the rest of the pipeline while
        # making the evaluation source explicit.
        method.postconds = [ground_truth_postcond]
        method.postcond_corr = []
        method.mutant_kill = []

        if not postcond_checking(method, ground_truth_postcond):
            postcond_code_src, hot_range = None, None
        elif not ground_truth_postcond.strip():
            postcond_code_src, hot_range = None, None
        else:
            postcond_code_src, hot_range = postcond_inj(
                method=method,
                code_str=code_str,
                postcond=ground_truth_postcond,
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
            corr_flag = run_result.to_flag()
            if corr_flag == "failed" and hot_range is not None:
                local_crash = is_local_crash(run_result.stdout, hot_range, method.file)
                if local_crash:
                    corr_flag = "local_crash"

        method.postcond_corr.append(corr_flag)

        mutant_kill: list[str] = []
        method.mutant_kill.append(mutant_kill)
        if corr_flag == "passed":
            for mutant in method.mutants:
                postcond_code_src, hot_range = postcond_inj(
                    method=method,
                    code_str=code_str,
                    postcond=ground_truth_postcond,
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
                        local_crash = is_local_crash(run_result.stdout, hot_range, method.file)
                        if local_crash:
                            comp_flag = "local_crash"
                mutant_kill.append(comp_flag)

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
        if not method.ref_postcond:
            continue
        if lang is not None and method.repo.language != lang:
            continue
        if github_path is not None and method.repo.github_path != github_path:
            continue
        if rlid is not None and method.rlid != rlid:
            continue

        eval_method = deepcopy(method)
        eval_method.postconds = None
        eval_method.responses = None
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
) -> dict:
    os.makedirs(output_dir, exist_ok=True)
    log_dir = os.path.join(output_dir, "logs", f"gt_eval--{get_uuid7()}")
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
        params_list.append((method, out_path))

    summary_path = os.path.join(log_dir, "__summary.md")
    return_codes, _ = run_with_pool_file_monitor(
        func=evaluate_ground_truth_method,
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
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run benchmark ground-truth evaluation.")
    parser.add_argument("--input_dir", default="data/step/8.benchmark")
    parser.add_argument("--output_dir", required=True)
    parser.add_argument("--task_num", type=int, default=None)
    parser.add_argument("--task_idx", type=int, default=None)
    parser.add_argument("--lang", default=None)
    parser.add_argument("--github_path", default=None)
    parser.add_argument("--rlid", default=None)
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--processes", type=int, default=1)
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
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()