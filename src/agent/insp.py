


import os, json
from src.ds import *
from typing import *
import random
from src.curator.eval_postcond import eval_postcond


KFS = ["jml_fail", "icontract_fail"]

def read_benchmark(p, save_mem=False) -> List[Method]:
    print(f"Reading {p}.")
    methods: List[Method] = []
    for fn in os.listdir(p):
        with open(f"{p}/{fn}") as f:
            method = Method.from_dict(json.load(f))
            if save_mem:
                method.repo.env_config = None
                method.repo.failed_tests = None
                method.cover_tests = None
                method.mutants = None
                method.postconds = None
                method.responses = None
            methods.append(method)
    return methods

def observe():
    input_dir = "data/step/9.Qwen3-32B-reason--v2-all"

    methods = read_benchmark(input_dir)
    methods = [m for m in methods if m.repo.language == "java"]

    counts = [0, 0, 0, 0]
    for m in methods:
        if m.postcond_corr[0] != "passed" and m.postcond_corr[0] != "jml_fail":
            counts[0] += 1
        if m.postcond_corr[0] == "jml_fail":
            counts[1] += 1
            print(m.github_url)
            print("-" * 30)
            print(m.content)
            print("-" * 30)
            print(m.postconds[0])
            print("=" * 30)
        if m.postcond_corr[0] == "passed":
            ref_kill = m.ref_mutant_kill
            kill = m.mutant_kill[0]
            if any(r_f in KFS and f not in KFS 
                    for f, r_f in zip(kill, ref_kill)):
                counts[2] += 1
            else:
                counts[3] += 1
    print(counts)

def eval():
    github_url = "https://github.com/aiogram/aiogram/blob/4caf56814e22af63248e78c25c9755c7ba51c60d/./aiogram/utils/web_app.py#L111-L140"
    p_idx = 0

    methods = read_benchmark("data/step/8.benchmark")

    method = [m for m in methods if m.github_url == github_url][0]
    # postcond = method.postconds[p_idx]

    postcond = r"""
@icontract.ensure(lambda token, init_data, result: isinstance(result, bool))
@icontract.ensure(lambda token, init_data, result: (not result) or ("hash=" in init_data))
"""

    print(postcond)

    results = eval_postcond(method, postcond, 
                            # mutant_idxs=[]
                            )

    print(results)

if __name__ == "__main__":
    # observe()
    eval()
