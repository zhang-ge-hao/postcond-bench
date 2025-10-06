from src.ds import *
from src.util import read_code
from src.clone import repository_reproduct
from src.inject import must_fail_inj
from src.runner import testsuite_run

def dynamic_collection(method: StaticMethod) -> DynamicMethod:
    lang = method.repo.language
    excluded_tests = method.repo.failed_tests

    with repository_reproduct(method.repo) as repo_dir:
        
        # cover tests collection
        code_str, code_bytes = read_code(method.file)
        injected_code_str = must_fail_inj(method, code_str)
        run_result = testsuite_run(
            excluded_tests=excluded_tests,
            require_not_interrupted=True,
            replace_file_path=method.file,
            replace_file_content=injected_code_str,
            timeout=200)
        cover_tests = run_result.failed_tests

        for _ in range(3):
            run_result = testsuite_run(
                included_tests=cover_tests,
                require_not_interrupted=True,
                replace_file_path=method.file,
                replace_file_content=injected_code_str,
                timeout=20)
            assert run_result.to_flag() == "passed"

        # line cov collection
        if lang == "python":
            pass
        elif lang == "java":
            # for fatjar runner, the `covered_files` list
            # is method level actrually
            run_result.covered_files
        
        pass
