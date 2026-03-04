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

    methods.sort(key=lambda m: m.repo.github_path.replace("/", "--") + "--" + m.rlid)

    postcond_idx = -1

    target_m = "a2aproject--a2a-python--routes"

    for m in methods:
        m_id = m.repo.github_path.replace("/", "--") + "--" + m.rlid
        if m_id == target_m:
            with open("data/anno/agent.log", "w") as file:
                file.write(m.log)
            
            postcond = m.postconds[postcond_idx]
            results = eval_postcond(m, postcond, mutant_idxs=[])
            
            print(results)
            print(postcond)
            print(f"{input_dir}/{m_id}.json")
    exit()

    for m in methods:
        postcond_corr = m.postcond_corr[postcond_idx]
        postcond = m.postconds[postcond_idx]
        if postcond_corr != "passed":
            r2_passed = False
            r3_passed = False
            for item in m.responses:
                if item["next_agent"] == "yield":
                    r3_passed = True
                    r2_passed = True
                elif item["next_agent"] == "judge_mutant_assistant":
                    r2_passed = True
            
            m_id = m.repo.github_path.replace("/", "--") + "--" + m.rlid

            # results = eval_postcond(m, postcond, mutant_idxs=[])

            print(m_id)
            
            print("-" * 30)

            # print(m.github_url)
            
            # print("-" * 30)

            print(m.postcond_corr[-2])

            # print("-" * 30)

            # print("Passed" if r2_passed else "Failed", 
            #         "Passed" if r3_passed else "Failed")

            # print("-" * 30)

            # print(postcond)

            # print("-" * 30)

            # print(results)

            print("=" * 30)


if __name__ == "__main__":
    observe()
