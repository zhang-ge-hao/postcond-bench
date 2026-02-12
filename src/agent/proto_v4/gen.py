
import os, re
import asyncio
from src.ds import *
from src.agent.proto_v4.agent import run_agent
from src.clone import repository_reproduct

from src.runner import testsuite_run
from src.util import get_uuid7, read_code
from src.inject import postcond_inj
from src.clone import repository_reproduct
from src.pool import run_with_pool_file_monitor


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


def postcond_generation_v2(
        method: Method, 
        output_path: str=None,
        model: str="gpt-5-mini",
        max_rounds: int=20):
    lang = method.repo.language
    excluded_tests = method.repo.failed_tests
    
    import logging

    with repository_reproduct(method.repo) as repo_dir:

        agent_res, history = asyncio.run(
            run_agent(method, model, max_rounds=max_rounds))

        lint_loop_broke = False
        corr_loop_broke = False
        for round, item in enumerate(history):
            if round == 0:
                non_agent_res = item["postcond"]
            if not lint_loop_broke:
                lint_only_res = item["postcond"]
            if not corr_loop_broke:
                corr_only_res = item["postcond"]

            if item["next_agent"] == "inputs_builder_assistant":
                lint_loop_broke = True
            if item["next_agent"] == "judge_mutant_assistant":
                corr_loop_broke = True
            
        method.postconds = [non_agent_res, lint_only_res, corr_only_res, agent_res]
        method.responses = history

        # ===== eval start =====
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
            # ===== eval end =====
    if output_path is not None:
        with open(output_path, "w") as file:
            json.dump(method.to_dict(), file, indent=2)


def postcond_generation_v2_pool(
        input_dir=None, output_dir=None, 
        task_num=None, task_idx=None, lang=None, github_path=None,
        model="gpt-5-mini"):
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

    for m in methods:
        m.generate_num = 1

    methods.sort(key=lambda m: (-m.test_time * len(m.mutants), 
                                m.repo.github_path, 
                                m.rlid))
    if task_num is not None and task_idx is not None:
        methods = [m for i, m in enumerate(methods) 
                   if i % task_num == task_idx]
    if lang is not None:
        methods = [m for m in methods if m.repo.language == lang]
    
    if github_path is not None:
        methods = [m for m in methods if m.repo.github_path == github_path]

    params_list = []
    task_names = []
    log_paths = []
    for m in methods:
        rn = m.repo.github_path.replace("/", "--")
        tn = f"{rn}--{m.rlid}"
        out_path = f"{output_dir}/{tn}.json"
        if os.path.exists(out_path):
            with open(out_path) as file:
                m = Method.from_dict(json.load(file))
            if m.postcond_corr is not None:
                continue
        params_list.append((m, out_path, model)) # NOTE: removed all_methods; add model
        task_names.append(tn)
        # log_paths.append(None)
        log_paths.append(f"{log_dir}/{rn}.log")
    
    print(len(params_list))

    summary_path = f"{log_dir}/__summary.md"
    _, ret = run_with_pool_file_monitor(
        func=postcond_generation_v2,
        task_names=task_names,
        log_paths=log_paths,
        params_list=params_list,
        processes=30,
        summary_path=summary_path,
        refresh_interval=1,
    )


if __name__ == "__main__":
    input_dir = "data/step/8.benchmark"
    model = "gpt-4o-mini"
    output_dir = f"data/step/9.{model}--proto_v4"
    os.makedirs(output_dir, exist_ok=True)

    postcond_generation_v2_pool(
        input_dir=input_dir,
        output_dir=output_dir,
        task_num=1, task_idx=0,
        github_path="keon/algorithms",
        model=model
    )
