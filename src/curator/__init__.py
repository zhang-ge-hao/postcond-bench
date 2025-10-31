
from src.curator.call_gpt import call_gpt
from src.curator.eval_postcond import eval_postcond

from src.pool import run_with_pool_file_monitor

from src.ds import *

from src.util import get_uuid7

import os

def ref_gen_pool(input_dir=None, output_dir=None,
                 task_num=None, task_idx=None):
    task_name = "ref_gen"
    log_dir = f"data/__log/{task_name}--{get_uuid7()}"
    os.makedirs(log_dir, exist_ok=True)

    methods: List[Method] = []
    for file_name in os.listdir(input_dir):
        if file_name.endswith(".json"):
            file_path = f"{input_dir}/{file_name}"
            with open(file_path) as file:
                methods.append(Method.from_dict(json.load(file)))

    methods.sort(key=lambda m: (-m.test_time * len(m.mutants), 
                                m.repo.github_path, 
                                m.rlid))
    
    if task_num is not None and task_idx is not None:
        methods = [m for i, m in enumerate(methods) 
                   if i % task_num == task_idx]

    abs_out_dir = os.path.abspath(output_dir)

    params_list = []
    task_names = []
    log_paths = []
    for m in methods:
        rn = m.repo.github_path.replace("/", "--")
        tn = f"{rn}--{m.rlid}"

        out_path = f"{abs_out_dir}/{tn}.json"
        if os.path.exists(out_path):
            continue

        params_list.append((m, out_path))
        task_names.append(tn)
        log_paths.append(f"{log_dir}/{rn}.log")

    print(len(params_list))

    summary_path = f"{log_dir}/__summary.md"
    _, ret = run_with_pool_file_monitor(
        func=call_gpt,
        task_names=task_names,
        log_paths=log_paths,
        params_list=params_list,
        processes=30,
        summary_path=summary_path,
        refresh_interval=1,
    )
