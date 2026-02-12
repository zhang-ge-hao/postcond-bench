
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

def cal_corr_and_comp_counts(methods: List[Method], selected_p_idx=None):
    corr_count = 0
    comp_count = 0
    for m in methods:
        for p_idx, (corr_res, comp_res) in enumerate(zip(m.postcond_corr, m.mutant_kill)):
            if selected_p_idx is not None and selected_p_idx != p_idx:
                continue
            if corr_res == "passed":
                corr_count += 1
                assert len(comp_res) == 0 or len(comp_res) == len(m.ref_mutant_kill)
                if all(r_f not in KFS or f in KFS 
                       for f, r_f in zip(comp_res, m.ref_mutant_kill)):
                    comp_count += 1
    return corr_count, comp_count

def get_incorr_postconds(methods: List[Method]) -> List[Tuple[int, Method]]:
    res = []
    for m in methods:
        for p_idx, (corr_res, comp_res) in enumerate(zip(m.postcond_corr, m.mutant_kill)):
            if corr_res != "passed":
                res.append((p_idx, m))
    return res

def print_incorr_postconds(postconds: List[Tuple[int, Method]], file_path):
    with open(file_path, "w") as file:
        content = []
        for p_idx, m in postconds:
            content.append("=" * 30)
            content.append(m.github_url)
            content.append("-" * 30)
            content.append(m.postcond_corr[p_idx])
            content.append("-" * 30)
            content.append(m.responses[p_idx])
        file.write("\n".join(content))


if __name__ == "__main__":
    expected_method_count = 31

    random.seed(42)

    postcond_pre_method = 1
    expected_postcond_count = expected_method_count * postcond_pre_method

    methods = read_benchmark("data/step/9.gpt-5-mini--proto_v4")

    python_methods = [m for m in methods if m.repo.language == "python"]
    python_methods = [m for m in methods if m.repo.github_path == "keon/algorithms"]

    for p_idx in range(4):
        python_corr_count, python_comp_count = cal_corr_and_comp_counts(
            python_methods, selected_p_idx=p_idx)
        print(f"{p_idx}")
        print(f"{python_corr_count / expected_postcond_count:.3f}")
        print(f"{python_comp_count / expected_postcond_count:.3f}")



    methods = read_benchmark("data/step/9.gpt-4o-mini--proto_v4")

    python_methods = [m for m in methods if m.repo.language == "python"]
    python_methods = [m for m in methods if m.repo.github_path == "keon/algorithms"]

    for p_idx in range(4):
        python_corr_count, python_comp_count = cal_corr_and_comp_counts(
            python_methods, selected_p_idx=p_idx)
        print(f"{p_idx}")
        print(f"{python_corr_count / expected_postcond_count:.3f}")
        print(f"{python_comp_count / expected_postcond_count:.3f}")



    postcond_pre_method = 5
    expected_postcond_count = expected_method_count * postcond_pre_method

    methods = read_benchmark("data/step/9.claude-sonnet-4-5--v2-all")

    python_methods = [m for m in methods if m.repo.language == "python"]
    python_methods = [m for m in methods if m.repo.github_path == "keon/algorithms"]

    python_corr_count, python_comp_count = cal_corr_and_comp_counts(python_methods)
    print(f"{python_corr_count / expected_postcond_count:.3f}")
    print(f"{python_comp_count / expected_postcond_count:.3f}")

    methods = read_benchmark("data/step/9.gpt-5--v2-all")

    python_methods = [m for m in methods if m.repo.language == "python"]
    python_methods = [m for m in methods if m.repo.github_path == "keon/algorithms"]

    python_corr_count, python_comp_count = cal_corr_and_comp_counts(python_methods)
    print(len(python_methods))
    print(f"{python_corr_count / expected_postcond_count:.3f}")
    print(f"{python_comp_count / expected_postcond_count:.3f}")
