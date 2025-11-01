


import os
from src.ds import *
from openai import OpenAI

from src.runner import testsuite_run
from src.postcond.prompt.infile import prompt_infile
from src.util import get_uuid7, read_code
from src.inject import postcond_inj
from src.clone import repository_reproduct
from src.pool import run_with_pool_file_monitor


def eval_postcond(method: Method, postcond):
    with repository_reproduct(method.repo) as repo_dir:
        lang = method.repo.language
        excluded_tests = method.repo.failed_tests

        code_str, code_bytes = read_code(method.file)

        postcond_code_src = postcond_inj(
            method=method,
            code_str=code_str,
            postcond=postcond
        )
        if postcond_code_src is None: # 目前应该只有在java的情况下会出现为None
            assert method.repo.language == "java"
            return "JML parser runs with a syntax error."
        else:
            run_result = testsuite_run(
                lang=lang,
                included_tests=method.cover_tests,
                excluded_tests=excluded_tests,
                replace_file_path=method.file,
                replace_file_content=postcond_code_src,
                need_coverage=False,
                timeout=30)
            corr_flag = run_result.to_flag()
            if corr_flag != "passed":
                return run_result.stdout

        # # ===== Debug =====
        # print("===== Debug =====")
        # print(run_result.stdout)
        # # ===== Debug End =====

        mutant_results = []

        for mut_idx, mutant in enumerate(method.mutants):
            postcond_code_src = postcond_inj(
                method=method,
                code_str=code_str,
                postcond=postcond,
                mutant=mutant,
            )
            if not postcond_code_src: # 目前应该只有在java的情况下会出现为None
                comp_flag = "compile_failure"
            else:
                run_result = testsuite_run(
                    lang=lang,
                    included_tests=method.cover_tests,
                    excluded_tests=excluded_tests,
                    replace_file_path=method.file,
                    replace_file_content=postcond_code_src,
                    need_coverage=False,
                    timeout=30)
                comp_flag = run_result.to_flag()
            mutant_results.append(comp_flag)
            pass
        return mutant_results


if __name__ == "__main__":
#     postcond = """// @ ensures contents.get().size() == \old(contents.get().size()) + 1;
# // @ ensures contents.get().get(contents.get().size() - 1) == segment;
# // @ ensures java.util.Arrays.equals(contents.get().subList(0, contents.get().size() - 1).toArray(), \old(contents.get().toArray()));"""
#     # postcond = "//@ ensures props.containsKey(name) ==> (\\result != null && \\result.size() > 0);\n//@ ensures props.containsKey(name) ==> props.getProperty(name).split(\",\").length == \\result.size();\n//@ ensures !props.containsKey(name) ==> \\result == defaultProperties;\n//@ ensures \\result != null;\n//@ ensures \\old(props.getProperty(name)) != null ==> \\result != null;\n//@ ensures \\old(props.getProperty(name)) != null ==> \\result.size() == \\old(props.getProperty(name).split(\",\")).length;"
#     methods = Method.load_li("data/step/6.mutation/adyliu--jafka.jsonl")
#     method = methods[1]

    postcond = '@icontract.ensure(lambda result, items: result == {k: (vs if len(vs) > 1 else vs[0]) for k, vs in ((k, [v for kk, v in items if kk == k]) for k in {k for k, _ in items})})'
    methods = Method.load_li("data/step/6.mutation/abersheeran--kui.jsonl")
    method = methods[0]

    eval_postcond(method, postcond)