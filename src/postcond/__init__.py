

import os
from src.ds import *
from openai import OpenAI

from src.runner import testsuite_run
from src.postcond.prompt.infile import prompt_infile
from src.util import get_uuid7, read_code
from src.inject import postcond_inj
from src.clone import repository_reproduct
from src.pool import run_with_pool_file_monitor

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


def postcond_generation(method: Method) -> Method:
    lang = method.repo.language

    import logging

    logging.info(f"{method.rlid} started.")

    lang = method.repo.language
    excluded_tests = method.repo.failed_tests
    with repository_reproduct(method.repo) as repo_dir:
        prompt = prompt_infile(method, True)

        code_str, code_bytes = read_code(method.file)

        client = OpenAI()

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": prompt},
            ],
            n=5
        )
        postconditions = [
            choice.message.content for choice in response.choices]
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
            postcond_code_src, local_crash_line_range = postcond_inj(
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
                    local_crash_line_range=local_crash_line_range,
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
                postcond_code_src, local_crash_line_range = postcond_inj(
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
                        local_crash_line_range=local_crash_line_range,
                        timeout=30)
                    comp_flag = run_result.to_flag()

                # ===== Debug =====
                print("===== Debug =====")
                print(run_result.stdout)
                # ===== Debug End =====

                mutant_kill.append(comp_flag)
            pass
    return method


def postcond_generation_pool(input_dir=None, output_dir=None):
    task_name = "postcond_gen"
    log_dir = f"data/__log/{task_name}--{get_uuid7()}"
    os.makedirs(log_dir, exist_ok=True)

    methods: List[Method] = []
    for file_name in os.listdir(input_dir):
        if file_name.endswith(".jsonl"):
            for m in Method.load_li(f"{input_dir}/{file_name}"):
                methods.append(m)

    esti = (len(m.mutants) + 1) * (m.test_time if m.test_time else 1)
    methods.sort(key=lambda m: -esti)

    task_names = []
    log_paths = []
    for m in methods:
        rn = m.repo.github_path.replace("/", "--")
        tn = f"{rn}--{m.rlid}"
        task_names.append(tn)
        log_paths.append(f"{log_dir}/{rn}.log")

    summary_path = f"{log_dir}/__summary.md"
    _, ret = run_with_pool_file_monitor(
        func=postcond_generation,
        task_names=task_names,
        log_paths=log_paths,
        params_list=methods,
        processes=30,
        summary_path=summary_path,
        refresh_interval=1,
    )

    rn_2_ms = {}
    for m in ret:
        if m:
            rn = m.repo.github_path.replace("/", "--")
            if rn not in rn_2_ms:
                rn_2_ms[rn] = []
            rn_2_ms[rn].append(m)

    for rn, ms in rn_2_ms.items():
        file_path = f"{output_dir}/{rn}.jsonl"
        Method.save_li(ms, file_path)
