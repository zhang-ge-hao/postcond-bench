


import os, json
from src.ds import *
from typing import *
import random


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


if __name__ == "__main__":
    input_dir = "data/step/9.Qwen3-32B-agent--v2-all"

    methods = read_benchmark(input_dir)

    for m in methods:
        if m.postcond_corr[0] == "passed":
            ref_kill = m.ref_mutant_kill
            kill = m.mutant_kill[0]
            if any(r_f in KFS and f not in KFS 
                    for f, r_f in zip(kill, ref_kill)):
                print(m.github_url)
                print("-" * 30)
                print(m.content)
                print("-" * 30)
                print(m.postconds[0])
                print("=" * 30)
