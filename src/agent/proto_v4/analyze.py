import os, json
from src.ds import *
from typing import *
import random
from src.curator.eval_postcond import eval_postcond

from src.agent.proto_v4.agent import _parse_yaml

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


def observe_judge():
    input_dir = "data/step/9.gpt-5-mini--proto_v4"

    methods = read_benchmark(input_dir)
    methods = [m for m in methods if m.repo.language == "python"]

    judge_logs_split: Dict[str, List[Tuple[str, str]]] = {}
    judge_mutant_logs_split: Dict[str, List[Tuple[str, str]]] = {}

    for m in methods:
        m_id = m.repo.github_path.replace("/", "--") + "--" + m.rlid
        log = m.log
        m_log_lines = log.split("\n")
        for l_idx, line in enumerate(m_log_lines):
            if line.startswith("===== PROMPT for AGENT: judge_mutant_assistant") \
                    or line.startswith("===== PROMPT for AGENT: judge_assistant"):
                for collect_l_idx in range(l_idx + 1, len(m_log_lines)):
                    if m_log_lines[collect_l_idx].startswith("===== The Next for AGENT:") \
                            or m_log_lines[collect_l_idx].startswith("===== Remove Mutant for AGENT:"):
                        judge_log = "\n".join(m_log_lines[l_idx: collect_l_idx])
                        break    
                log_lines = judge_log.split("\n")
                for l_idx, line in enumerate(log_lines):
                    if line.startswith("===== RESPONSE for AGENT: "):
                        first_line = log_lines[0]
                        prompt = "\n".join(log_lines[1: l_idx])
                        response = "\n".join(log_lines[l_idx + 1: ])
                        if "judge_assistant" in first_line:
                            judge_result = _parse_yaml(response, ["summary", "fault"])
                            if not judge_result or judge_result["fault"].strip() not in ["inputs", "postcondition"]:
                                flag = "format_error"
                            else:
                                flag = judge_result["fault"].strip()
                            if flag not in judge_logs_split:
                                judge_logs_split[flag] = []
                            judge_logs_split[flag].append((m_id, m, judge_log, prompt, response))
                        elif "judge_mutant_assistant" in first_line:
                            judge_result = _parse_yaml(response, ["evidence_summary", "fix_suggestion", "responsible"])
                            if not judge_result or judge_result["responsible"].strip() not in ["inputs", "postcondition", "bug"]:
                                flag = "format_error"
                            else:
                                flag = judge_result["responsible"].strip()
                            if flag not in judge_mutant_logs_split:
                                judge_mutant_logs_split[flag] = []
                            judge_mutant_logs_split[flag].append((m_id, m, judge_log, prompt, response))
    random.seed(42)
    print("judge")
    for k, v in judge_logs_split.items():
        print(k, len(v))
        sampled = random.sample(v, 5)
        with open(f"data/anno/judge/r2/{k}.txt", "w") as file:
            for m_id, m, judge_log, prompt, response in sampled:
                file.write(f"===== {m_id} =====\n")
                file.write(f"= {m.github_url} =\n")
                file.write(f"{judge_log}\n\n\n")

    print("judge_mutant")
    for k, v in judge_mutant_logs_split.items():
        print(k, len(v))
        sampled = random.sample(v, 5)
        with open(f"data/anno/judge/r3/{k}.txt", "w") as file:
            for m_id, m, judge_log, prompt, response in sampled:
                file.write(f"===== {m_id} =====\n")
                file.write(f"= {m.github_url} =\n")
                file.write(f"{judge_log}\n\n\n")
    


if __name__ == "__main__":
    observe_judge()
