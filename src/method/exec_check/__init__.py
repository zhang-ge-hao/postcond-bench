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
            need_coverage=False,
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
            need_coverage=False,
            timeout=20)
        
        method.test_time = run_result.running_time

        if run_result.to_flag() != "passed" \
                or "Exception within current method!" in run_result.stdout:
            import logging
            logging.error(run_result.to_string())
            raise RuntimeError()
        
        return method


def exec_check_pool(
        input_dir=None, 
        output_dir=None, 
        debug_mode=False,
        task_num=None, task_idx=None):
    task_name = "exec_check"
    log_dir = f"data/__log/{task_name}--{get_uuid7()}"
    os.makedirs(log_dir, exist_ok=True)

    methods: List[Method] = []
    for file_name in os.listdir(input_dir):
        if file_name.endswith(".jsonl"):
            for m in Method.load_li(f"{input_dir}/{file_name}"):
                methods.append(m)
    
    if task_num is not None and task_idx is not None:
        github_paths = [m.repo.github_path for m in methods]
        github_paths = list(set(github_paths))
        github_paths.sort()
        selected_paths = [p for i, p in enumerate(github_paths) 
                          if i % task_num == task_idx]

        # ban_paths = [
        #     "lemon24/reader",
        #     "Password4j/password4j",
        #     "falconry/falcon",
        #     "yzhao062/combo",
        #     "wangguanquan/eec/writeTo-2",
        #     "sanic-org/sanic",
        #     "lemon24/reader",
        #     "sanic-org/sanic",
        #     "lemon24/reader",
        #     "lemon24/reader",
        #     "falconry/falcon",
        #     "yzhao062/combo/fit-4",
        #     "KittehOrg/KittehIRCClientLib",
        #     "Password4j/password4j",
        #     "cdown/srt",
        #     "falconry/falcon",
        #     "falconry/falcon",
        #     "wangguanquan/eec/find-2",
        #     "Password4j/password4j",
        #     "falconry/falcon",
        #     "deedy5/ddgs",
        #     "bramp/ffmpeg-cli-wrapper",
        #     "mojohaus/extra-enforcer-rules",
        #     "sanic-org/sanic",
        #     "falconry/falcon",
        #     "wangguanquan/eec/put-2",
        #     "sanic-org/sanic",
        #     "nbedos/termtosvg",
        #     "falconry/falcon",
        #     "pndurette/gTTS",
        # ]

        # selected_paths = [p for p in selected_paths if p not in ban_paths]

        methods = [m for m in methods if m.repo.github_path in selected_paths]
        print(len(selected_paths))
        print(len(methods))

    if debug_mode:
        import random
        random.seed(42)
        python_methods = [m for m in methods if m.repo.language == "python"]
        java_methods = [m for m in methods if m.repo.language == "java"]
        python_methods = random.sample(python_methods, 100)
        java_methods = random.sample(java_methods, 100)
        methods = python_methods + java_methods

    # methods.sort(key=lambda m: -m.repo.test_time)
    import random
    random.shuffle(methods)

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
