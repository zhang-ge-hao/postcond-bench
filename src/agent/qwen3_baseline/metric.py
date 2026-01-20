
import os, json
from src.ds import *
from typing import List


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

def cal_corr_and_comp_counts(methods: List[Method]):
    corr_count = 0
    comp_count = 0
    for m in methods:
        for corr_res, comp_res in zip(m.postcond_corr, m.mutant_kill):
            if corr_res == "passed":
                corr_count += 1
                assert len(comp_res) == 0 or len(comp_res) == len(m.ref_mutant_kill)
                if all(r_f not in KFS or f in KFS 
                       for f, r_f in zip(comp_res, m.ref_mutant_kill)):
                    comp_count += 1
    return corr_count, comp_count

if __name__ == "__main__":
    expected_method_count = 210
    postcond_pre_method = 1

    expected_postcond_count = expected_method_count * postcond_pre_method

    methods = read_benchmark("data/step/9.Qwen3-32B-reason--v2-all")

    python_methods = [m for m in methods if m.repo.language == "python"]
    java_methods = [m for m in methods if m.repo.language == "java"]

    python_corr_count, python_comp_count = cal_corr_and_comp_counts(python_methods)
    print(f"{python_corr_count / expected_postcond_count:.3f}")
    print(f"{python_comp_count / expected_postcond_count:.3f}")
    java_corr_count, java_comp_count = cal_corr_and_comp_counts(java_methods)
    print(f"{java_corr_count / expected_postcond_count:.3f}")
    print(f"{java_comp_count / expected_postcond_count:.3f}")