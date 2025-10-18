from src.ds import *
from src.clone import repository_reproduct
from src.util import read_code
from src.inject import (
    must_fail_inj,
    check_postcond_exec_inj
)
from src.runner import testsuite_run


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
            timeout=20,
            need_print=True)

        if run_result.to_flag() != "passed" \
                or "Exception within current method!" in run_result.stdout:
            return None
        
        return method
