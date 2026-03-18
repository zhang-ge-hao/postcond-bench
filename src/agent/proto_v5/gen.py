import asyncio
import json
import os
import re

from src.agent.proto_v5.agent import run_agent
from src.clone import repository_reproduct
from src.ds import *
from src.inject import postcond_inj
from src.pool import run_with_pool_file_monitor
from src.runner import testsuite_run
from src.util import get_uuid7, read_code


def postcond_checking(method: Method, postcond: str) -> bool:
    """
    Some small models may output dead code after decorators.
    For Python, reject outputs that define a function body.
    """
    if method.repo.language == "python":
        for line in postcond.split("\n"):
            if line.strip().startswith("def "):
                return False
    return True


def is_local_crash(stdout: str, hot_range: Tuple[int, int], file_path: str) -> bool:
    if not stdout or hot_range is None:
        return False

    file_path = file_path.strip()
    if file_path.startswith("./"):
        file_path = file_path[2:]
    hot_line_start, hot_line_end = hot_range

    for line in stdout.split():
        pattern = rf"{re.escape(file_path)}:(\d+)"
        match = re.search(pattern, line)
        if match:
            crash_line_number = int(match.group(1))
            if hot_line_start <= crash_line_number <= hot_line_end:
                return True
    return False


def postcond_generation_v5(
    method: Method,
    output_path: str = None,
    model: str = "gpt-5-mini",
    max_llm_calls: int = 20,
):
    lang = method.repo.language
    excluded_tests = method.repo.failed_tests

    import logging

    with repository_reproduct(method.repo):
        agent_res, history, log, _summary = asyncio.run(
            run_agent(
                method,
                model=model,
                max_llm_calls=max_llm_calls,
                collect_logs=True,
            )
        )

        method.postconds = [agent_res]
        method.responses = history
        method.log = log

        code_str, _ = read_code(method.file)
        method.postcond_corr = []
        method.mutant_kill = []

        for p_idx, postcond in enumerate(method.postconds):
            logging.info(f"{method.rlid} postcond {p_idx} eval start.")
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
                corr_flag = run_result.to_flag()
                if corr_flag == "failed" and hot_range is not None:
                    local_crash = is_local_crash(run_result.stdout, hot_range, method.file)
                    if local_crash:
                        corr_flag = "local_crash"

            logging.info(f"{method.rlid} postcond {p_idx} is {corr_flag}.")
            method.postcond_corr.append(corr_flag)

            mutant_kill = []
            method.mutant_kill.append(mutant_kill)
            if corr_flag != "passed":
                continue

            for mut_idx, mutant in enumerate(method.mutants):
                logging.info(f"{method.rlid} postcond {p_idx} mutant {mut_idx} eval start.")

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
                        local_crash = is_local_crash(run_result.stdout, hot_range, method.file)
                        if local_crash:
                            comp_flag = "local_crash"

                logging.info(f"{method.rlid} postcond {p_idx} mutant {mut_idx} is {comp_flag}.")
                mutant_kill.append(comp_flag)
    if output_path is not None:
        with open(output_path, "w") as file:
            json.dump(method.to_dict(), file, indent=2)


def postcond_generation_v5_pool(
    input_dir=None,
    output_dir=None,
    task_num=None,
    task_idx=None,
    lang=None,
    github_path=None,
    model="gpt-5-mini",
    max_llm_calls: int = 20,
):
    task_name = "postcond_gen"

    pi_workdir = os.getenv("PI_WORKDIR")
    log_base = os.path.join(pi_workdir, "sb_tmp__log")

    log_dir = f"{log_base}/{task_name}--{get_uuid7()}"
    output_dir = os.path.abspath(output_dir)
    os.makedirs(log_dir, exist_ok=True)

    methods: List[Method] = []
    for file_name in os.listdir(input_dir):
        if file_name.endswith(".json"):
            with open(f"{input_dir}/{file_name}") as file:
                methods.append(Method.from_dict(json.load(file)))

    for method in methods:
        method.generate_num = 1

    methods.sort(key=lambda method: (-method.test_time * len(method.mutants), method.repo.github_path, method.rlid))
    if task_num is not None and task_idx is not None:
        methods = [method for i, method in enumerate(methods) if i % task_num == task_idx]
    if lang is not None:
        methods = [method for method in methods if method.repo.language == lang]
    if github_path is not None:
        methods = [method for method in methods if method.repo.github_path == github_path]

    params_list = []
    task_names = []
    log_paths = []
    for method in methods:
        repo_name = method.repo.github_path.replace("/", "--")
        task_label = f"{repo_name}--{method.rlid}"
        out_path = f"{output_dir}/{task_label}.json"
        if os.path.exists(out_path):
            with open(out_path) as file:
                saved_method = Method.from_dict(json.load(file))
            if saved_method.postcond_corr is not None:
                continue

        params_list.append((method, out_path, model, max_llm_calls))
        task_names.append(task_label)
        log_paths.append(f"{log_dir}/{repo_name}.log")

    print(len(params_list))

    summary_path = f"{log_dir}/__summary.md"
    run_with_pool_file_monitor(
        func=postcond_generation_v5,
        task_names=task_names,
        log_paths=log_paths,
        params_list=params_list,
        processes=30,
        summary_path=summary_path,
        refresh_interval=1,
    )


if __name__ == "__main__":
    input_dir = "data/step/8.benchmark"
    model = "gpt-5-mini"
    output_dir = f"data/step/9.{model}--proto_v5"
    os.makedirs(output_dir, exist_ok=True)

    postcond_generation_v5_pool(
        input_dir=input_dir,
        output_dir=output_dir,
        task_num=1,
        task_idx=0,
        lang="python",
        model=model,
    )