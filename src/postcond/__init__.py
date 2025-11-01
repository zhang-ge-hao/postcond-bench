

import os
from src.ds import *

from src.runner import testsuite_run
from src.postcond.prompt.infile import prompt_infile
from src.util import get_uuid7, read_code
from src.inject import postcond_inj
from src.clone import repository_reproduct
from src.pool import run_with_pool_file_monitor
from src.postcond.model import LLM_MAP

def response_post_process(response: str):
    quote_mark_count = 0
    for line in response.split("\n"):
        if line.strip().startswith("```"):
            quote_mark_count += 1
    if quote_mark_count == 0:
        return response
    met_quote_mark = False
    lines = []
    for line in response.split("\n"):
        if not met_quote_mark and line.strip().startswith("```"):
            met_quote_mark = True
        elif met_quote_mark and line.strip().startswith("```"):
            break
        elif met_quote_mark:
            lines.append(line)
    return "\n".join(lines)


def postcond_generation(method: Method, output_path: str=None) -> Method:
    assert method.model_name is not None
    assert method.generate_num is not None
    assert method.w_code is not None

    model = LLM_MAP[method.model_name]()

    lang = method.repo.language

    import logging

    logging.info(f"{method.rlid} started.")

    lang = method.repo.language
    excluded_tests = method.repo.failed_tests
    with repository_reproduct(method.repo) as repo_dir:
        prompt = prompt_infile(method, w_code=method.w_code)

        method.prompt = prompt

        code_str, code_bytes = read_code(method.file)

        postconditions = model.generate(
            prompt=prompt, 
            n=method.generate_num)

        postconditions = [
            response_post_process(m) for m in postconditions]
        
        # # ===== Debug =====
        # print("===== Debug =====")
        # print("\n=====\n".join(postconditions))
        # pass
        # # ===== Debug End =====

        method.postconds = postconditions
        method.postcond_corr = []
        method.mutant_kill = []
        for postcond in method.postconds:
            postcond_code_src = postcond_inj(
                method=method,
                code_str=code_str,
                postcond=postcond
            )
            if not postcond_code_src: # 目前应该只有在java的情况下会出现为None
                corr_flag = "compile_failure"
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
            method.postcond_corr.append(corr_flag)

            # # ===== Debug =====
            # print("===== Debug =====")
            # print(run_result.stdout)
            # # ===== Debug End =====

            mutant_kill = []
            method.mutant_kill.append(mutant_kill)
            if corr_flag != "passed":
                continue
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

                # ===== Debug =====
                print("===== Debug =====")
                print(run_result.stdout)
                # ===== Debug End =====

                mutant_kill.append(comp_flag)
            pass
    if output_path is not None:
        with open(output_path, "w") as file:
            json.dump(method.to_dict(), file, indent=2)
    return method


def postcond_generation_pool(
        input_dir=None, output_dir=None, 
        model_name=None, generate_num=None, w_code=None,
        task_num=None, task_idx=None):
    task_name = "postcond_gen"
    log_dir = f"data/__log/{task_name}--{get_uuid7()}"
    output_dir = os.path.abspath(output_dir)
    os.makedirs(log_dir, exist_ok=True)

    methods: List[Method] = []
    for file_name in os.listdir(input_dir):
        if file_name.endswith(".json"):
            with open(f"{input_dir}/{file_name}") as file:
                methods.append(Method.from_dict(json.load(file)))

    for m in methods:
        m.model_name = model_name
        m.generate_num = generate_num
        m.w_code = w_code

    methods.sort(key=lambda m: (-m.test_time * len(m.mutants), 
                                m.repo.github_path, 
                                m.rlid))
    if task_num is not None and task_idx is not None:
        methods = [m for i, m in enumerate(methods) 
                   if i % task_num == task_idx]

    params_list = []
    task_names = []
    log_paths = []
    for m in methods:
        rn = m.repo.github_path.replace("/", "--")
        tn = f"{rn}--{m.rlid}"
        out_path = f"{output_dir}/{tn}.json"
        if os.path.exists(out_path):
            continue
        params_list.append((m, out_path))
        task_names.append(tn)
        log_paths.append(f"{log_dir}/{rn}.log")

    summary_path = f"{log_dir}/__summary.md"
    _, ret = run_with_pool_file_monitor(
        func=postcond_generation,
        task_names=task_names,
        log_paths=log_paths,
        params_list=params_list,
        processes=30,
        summary_path=summary_path,
        refresh_interval=1,
    )
