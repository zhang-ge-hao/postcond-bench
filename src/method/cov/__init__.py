from src.ds import *
from src.util import read_code
from src.clone import repository_reproduct
from src.inject import must_fail_inj
from src.runner import testsuite_run
from src.cov import compute_method_line_coverage
from src.pool import run_with_pool_file_monitor
from src.util import get_uuid7
import os

def cov_filter(repo: Repo, methods: List[Method]):
    lang = repo.language
    excluded_tests = repo.failed_tests

    with repository_reproduct(repo) as repo_dir:
        run_result = testsuite_run(
            lang=lang,
            excluded_tests=excluded_tests,
            require_not_interrupted=True,
            timeout=200)
        for method in methods:
            cov = compute_method_line_coverage(method)
            method.line_cov = cov["coverage"]

        return repo, [m for m in methods if m.line_cov and m.line_cov >= 0.9]

def cov_filter_pool(input_dir=None, output_dir=None):
    task_name = "cov"
    log_dir = f"data/__log/{task_name}--{get_uuid7()}"
    os.makedirs(log_dir, exist_ok=True)

    repo_map: Dict[Tuple, Repo] = {}
    method_map: Dict[Tuple, List[Method]] = {}
    for file_name in os.listdir(input_dir):
        if file_name.endswith(".jsonl"):
            methods = Method.load_li(f"{input_dir}/{file_name}")
            for m in methods:
                key = (m.repo.github_path, m.repo.commit)
                repo_map[key] = m.repo
                if key not in method_map:
                    method_map[key] = []
                method_map[key].append(m)
    params_list: List[Tuple[Repo, List[Method]]] = []
    for k, r in repo_map.items():
        params_list.append((r, method_map[k]))

    summary_path = f"{log_dir}/__summary.md"
    task_names = [r.github_path.replace("/", "--")
                  for r, ms in params_list]
    log_paths = [f"{log_dir}/{tn}.log" for tn in task_names]
    _, ret = run_with_pool_file_monitor(
        func=cov_filter,
        task_names=task_names,
        log_paths=log_paths,
        params_list=params_list,
        processes=30,
        summary_path=summary_path,
        refresh_interval=1,
    )
    for __ret in ret:
        if __ret:
            r, ms = __ret
            rn = r.github_path.replace("/", "--")
            if ms:
                file_path = f"{output_dir}/{rn}.jsonl"
                Method.save_li(ms, file_path)
