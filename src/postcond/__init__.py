

import os
import re
from src.ds import *

from src.runner import testsuite_run
from src.postcond.prompt.infile import prompt_infile
from src.postcond.prompt.cot import prompt_cot
from src.postcond.prompt.fsl import prompt_fsl
from src.postcond.prompt.no_gram import prompt_no_gram
from src.util import get_uuid7, read_code
from src.inject import postcond_inj
from src.clone import repository_reproduct
from src.pool import run_with_pool_file_monitor
from src.postcond.model import model_generate

def response_post_process(response: str):
    quote_mark_count = 0
    for line in response.split("\n"):
        if line.strip().startswith("```"):
            quote_mark_count += 1
    if quote_mark_count == 0:
        return response
    met_quote_mark = False
    lines = []
    for line in reversed(response.split("\n")):
        if not met_quote_mark and line.strip().startswith("```"):
            met_quote_mark = True
        elif met_quote_mark and line.strip().startswith("```"):
            break
        elif met_quote_mark:
            lines.insert(0, line)
    return "\n".join(lines)


def is_local_crash(
        stdout: str, 
        hot_range: Tuple[int, int], 
        file_path: str) -> bool:
    if not stdout or hot_range is None:
        return False

    file_path = file_path.strip()
    if file_path.startswith("./"):
        file_path = file_path[2: ]
    hot_line_start, hot_line_end = hot_range

    for line in stdout.split():
        pattern = rf"{re.escape(file_path)}:(\d+)"
        match = re.search(pattern, line)
        if match:
            crash_line_number = int(match.group(1))
            if hot_line_start <= crash_line_number <= hot_line_end:
                return True
    return False


def postcond_checking(method: Method, postcond: str) -> bool:
    """
    小模型的 instruction following 较差
    在 python 生成了一些 icontract 行 + def 一个方法
    插入后相当于插入一段死代码 反而能 pass 测试用例
    """
    if method.repo.language == "python":
        for line in postcond.split("\n"):
            if line.strip().startswith("def "):
                return False
    return True


def postcond_generation(
        method: Method, 
        output_path: str=None,
        methods: List[Method]=None) -> Method:
    assert method.model_name is not None
    assert method.generate_num is not None
    assert method.w_code is not None

    lang = method.repo.language

    import logging

    logging.info(f"{method.rlid} started.")

    lang = method.repo.language
    excluded_tests = method.repo.failed_tests
    with repository_reproduct(method.repo) as repo_dir:
        if method.postconds is None:
            context_ratio = 1
            while True:
                try:
                    if method.prompting is None:
                        prompt = prompt_infile(
                            method, w_code=method.w_code,
                            context_ratio=context_ratio)
                    elif method.prompting.lower() == "cot":
                        prompt = prompt_cot(
                            method, w_code=method.w_code,
                            context_ratio=context_ratio)
                    elif method.prompting.lower().startswith("fsl"):
                        shot_num = int(method.prompting.split("_")[1])
                        prompt = prompt_fsl(
                            method, 
                            w_code=method.w_code, 
                            methods=methods,
                            shot_num=shot_num,
                            context_ratio=context_ratio)
                    elif method.prompting.lower() == "no_gram":
                        prompt = prompt_no_gram(
                            method, w_code=method.w_code,
                            context_ratio=context_ratio)
                    else:
                        raise NotImplementedError()

                    method.prompt = prompt

                    logging.info(f"{method.rlid} generation start.")
                    
                    responses = model_generate(
                        model_name=method.model_name,
                        prompt=prompt, 
                        n=method.generate_num,
                        port=method.port)

                    break
                except BaseException as e:
                    if "Please reduce the length of the messages or completion." in str(e):
                        context_ratio -= 0.1
                        if context_ratio < 0:
                            raise RuntimeError("The prompt is still too long.")
                    else:
                        raise e

            postconditions = [
                response_post_process(r) for r in responses]

            logging.info(f"{method.rlid} generated.")

            method.postconds = postconditions
            # 目前只需要 CoT 的时候记录一下 reasoning 就行了
            if method.prompting is not None and method.prompting.lower() == "cot":
                method.responses = responses

        code_str, code_bytes = read_code(method.file)
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
                    need_hot_range=True
                )
            # 会为 None 的情况 1) JML 翻译失败 2) 空生成结果 3) 后置校验没通过
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
                    timeout=30)
                corr_flag = run_result.to_flag()
                # 判断是否 local_crash
                if corr_flag == "failed" and hot_range is not None:
                    local_crash = is_local_crash(
                        run_result.stdout, hot_range, method.file)
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
                    need_hot_range=True
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
                    # 判断是否 local_crash
                    if comp_flag == "failed" and hot_range is not None:
                        local_crash = is_local_crash(
                            run_result.stdout, hot_range, method.file)
                        if local_crash:
                            comp_flag = "local_crash"

                logging.info(f"{method.rlid} postcond {p_idx} mutant {mut_idx} is {comp_flag}.")

                mutant_kill.append(comp_flag)
            pass
    if output_path is not None:
        with open(output_path, "w") as file:
            json.dump(method.to_dict(), file, indent=2)
    return method


def postcond_generation_pool(
        input_dir=None, output_dir=None, 
        model_name=None, generate_num=None, w_code=None,
        task_num=None, task_idx=None, lang=None, port=None,
        prompting=None):
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
    all_methods = [m for m in methods]

    for m in methods:
        m.model_name = model_name
        m.generate_num = generate_num
        m.w_code = w_code
        m.prompting = prompting
        if port is not None:
            m.port = port
        else:
            m.port = f"1999{task_idx}"

    methods.sort(key=lambda m: (-m.test_time * len(m.mutants), 
                                m.repo.github_path, 
                                m.rlid))
    if task_num is not None and task_idx is not None:
        methods = [m for i, m in enumerate(methods) 
                   if i % task_num == task_idx]
    if lang is not None:
        methods = [m for m in methods if m.repo.language == lang]

    params_list = []
    task_names = []
    log_paths = []
    for m in methods:
        rn = m.repo.github_path.replace("/", "--")
        tn = f"{rn}--{m.rlid}"
        out_path = f"{output_dir}/{tn}.json"
        if os.path.exists(out_path):
            continue
        params_list.append((m, out_path, all_methods))
        task_names.append(tn)
        # log_paths.append(None)
        log_paths.append(f"{log_dir}/{rn}.log")
    
    print(len(params_list))

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
