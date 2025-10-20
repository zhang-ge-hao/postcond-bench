from src.ds import *
from src.clone import repository_reproduct
from src.util import read_code
from src.inject import (
    must_fail_inj,
    check_postcond_exec_inj
)
from src.runner import testsuite_run
from src.util import get_uuid7
import os
from src.pool import run_with_pool_file_monitor


def exec_check(method: Method) -> Method:
    """covering tests + postcond have to be executed"""
    repo = method.repo
    lang = repo.language
    excluded_tests = repo.failed_tests
    with repository_reproduct(repo) as repo_dir:
        code_str, code_bytes = read_code(method.file)
        must_fail_code_src = must_fail_inj(method, code_str)
        run_result = testsuite_run(
            lang=lang,
            excluded_tests=excluded_tests,
            require_not_interrupted=True,
            replace_file_path=method.file,
            replace_file_content=must_fail_code_src,
            timeout=200)
        method.cover_tests = run_result.failed_tests

        check_pc_exec_code_src = check_postcond_exec_inj(method, code_str)
        run_result = testsuite_run(
            lang=lang,
            included_tests=method.cover_tests,
            excluded_tests=excluded_tests,
            require_not_interrupted=True,
            replace_file_path=method.file,
            replace_file_content=check_pc_exec_code_src,
            timeout=20)

        if run_result.to_flag() != "passed" \
                or "Exception within current method!" in run_result.stdout:
            import logging
            logging.error(run_result.to_string())
            raise RuntimeError()
        
        return method


def exec_check_pool(input_dir=None, output_dir=None):
    task_name = "exec_check"
    log_dir = f"data/__log/{task_name}--{get_uuid7()}"
    os.makedirs(log_dir, exist_ok=True)

    methods: List[Method] = []
    for file_name in os.listdir(input_dir):
        if file_name.endswith(".jsonl"):
            for m in Method.load_li(f"{input_dir}/{file_name}"):
                methods.append(m)
    
    import random
    random.seed(52)
    methods = random.sample(methods, 100)
    # print(len([m for m in methods if m.repo.language == "java"]))
    # print(len([m for m in methods if m.repo.language == "python"]))
    # exit()

    methods.sort(key=lambda m: -m.repo.test_time)

    task_names = []
    log_paths = []
    for m in methods:
        rn = m.repo.github_path.replace("/", "--")
        tn = f"{rn}--{m.rlid}"
        task_names.append(tn)
        log_paths.append(f"{log_dir}/{rn}.log")

    summary_path = f"{log_dir}/__summary.md"
    _, ret = run_with_pool_file_monitor(
        func=exec_check,
        task_names=task_names,
        log_paths=log_paths,
        params_list=methods,
        processes=30,
        summary_path=summary_path,
        refresh_interval=1,
    )
    rn_2_ms = {}
    for bef_m, aft_m in zip(methods, ret):
        if aft_m is None:
            print(bef_m.github_url)
            continue
        rn = bef_m.repo.github_path.replace("/", "--")
        if rn not in rn_2_ms:
            rn_2_ms[rn] = []
        rn_2_ms[rn].append(aft_m)
    for rn, ms in rn_2_ms.items():
        file_path = f"{output_dir}/{rn}.jsonl"
        Method.save_li(ms, file_path)
