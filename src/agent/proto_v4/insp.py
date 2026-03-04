


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
    input_dir = "data/step/9.gpt-5-mini--proto_v4"

    methods = read_benchmark(input_dir)
    methods = [m for m in methods if m.repo.language == "python"]

    postcond_idx = -1

    counts = [0, 0, 0, 0]
    for m in methods:
        postcond_corr = m.postcond_corr[postcond_idx]
        postcond = m.postconds[postcond_idx]
        if postcond_corr != "passed":
            print(m.github_url)
            print("-" * 30)
            print(m.content)
            print("-" * 30)
            print(postcond)
            print("=" * 30)

        if postcond_corr != "passed" \
                and postcond_corr not in KFS:
            counts[0] += 1
        if postcond_corr in KFS:
            counts[1] += 1
        if postcond_corr == "passed":
            ref_kill = m.ref_mutant_kill
            kill = m.mutant_kill[0]
            if any(r_f in KFS and f not in KFS 
                    for f, r_f in zip(kill, ref_kill)):
                counts[2] += 1
            else:
                counts[3] += 1
    print(counts)

def eval():
    github_url = "https://github.com/capitalone/datacompy/blob/2600d7c93f2656de63b108cdb8d37cbec8eb8bbf/./datacompy/core.py#L709-L764"
    p_idx = -1

    result_dir = "data/step/9.gpt-5-mini--proto_v4"

    methods = read_benchmark(result_dir)

    method = [m for m in methods if m.github_url == github_url][0]
    postcond = method.postconds[p_idx]

    postcond = r"""
@icontract.snapshot(lambda self, sample_count: self.column_stats, name="column_stats")
@icontract.snapshot(lambda self, sample_count: sample_count, name="sample_count")
@icontract.ensure(lambda OLD, self, sample_count, result: isinstance(result, dict))
@icontract.ensure(lambda OLD, self, sample_count, result: "mismatch_stats" in result and isinstance(result.get("mismatch_stats", None), dict))
@icontract.ensure(lambda OLD, self, sample_count, result: result.get("mismatch_stats", {}).get("has_mismatches") in (True, False))
@icontract.ensure(lambda OLD, self, sample_count, result: result.get("mismatch_stats", {}).get("has_mismatches") == any(not col.get("all_match", False) for col in OLD.column_stats))
@icontract.ensure(lambda OLD, self, sample_count, result: (result.get("mismatch_stats", {}).get("has_mismatches") is True) >> ("stats" in result.get("mismatch_stats", {}) and isinstance(result.get("mismatch_stats", {})["stats"], list)))
@icontract.ensure(lambda OLD, self, sample_count, result: (result.get("mismatch_stats", {}).get("has_mismatches") is True) >> ("samples" in result.get("mismatch_stats", {}) and isinstance(result.get("mismatch_stats", {})["samples"], list)))
"""

    print(postcond)

    results = eval_postcond(method, postcond, 
                            mutant_idxs=[]
                            )

    print(results)

    print()
    filenames = os.listdir(result_dir)
    for fn in filenames:
        if method.rlid in fn:
            print(f"{result_dir}/{fn}")
    print()

    with open("data/anno/agent.log", "w") as file:
        file.write(method.log)

if __name__ == "__main__":
    # observe()
    eval()
