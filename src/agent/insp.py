


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
    input_dir = "data/step/9.Qwen3-32B-agent--v2-all"

    methods = read_benchmark(input_dir)

    counts = [0, 0, 0, 0]
    for m in methods:
        if m.postcond_corr[0] != "passed" and m.postcond_corr[0] != "icontract_fail":
            counts[0] += 1
            print(m.github_url)
            print("-" * 30)
            print(m.content)
            print("-" * 30)
            print(m.postconds[0])
            print("=" * 30)
        if m.postcond_corr[0] == "icontract_fail":
            counts[1] += 1
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
    github_url = "https://github.com/a2aproject/a2a-python/blob/aa159f3e1076ae6eaad5576119d7857c2a9b2448/./src/a2a/utils/helpers.py#L51-L110"
    p_idx = 0

    methods = read_benchmark("data/step/8.benchmark")

    method = [m for m in methods if m.github_url == github_url][0]
    # postcond = method.postconds[p_idx]

    postcond = """
@icontract.snapshot(lambda task: task.artifacts, name="original_artifacts")
@icontract.ensure(lambda task: isinstance(task.artifacts, list))
@icontract.ensure(lambda OLD, task, event: not event.append or event.artifact in task.artifacts)
@icontract.ensure(
    lambda OLD, task, event: not event.append or (
        (OLD.original_artifacts is None and not any(art.artifact_id == event.artifact.artifact_id for art in task.artifacts)) 
        or (OLD.original_artifacts is not None and any(art.artifact_id == event.artifact.artifact_id for art in OLD.original_artifacts) == any(art.artifact_id == event.artifact.artifact_id for art in task.artifacts))
    )
)
@icontract.ensure(
    lambda OLD, task, event: not event.append or (
        (OLD.original_artifacts is None or not any(art.artifact_id == event.artifact.artifact_id for art in OLD.original_artifacts)) 
        or (
            (next((a for a in task.artifacts if a.artifact_id == event.artifact.artifact_id), None) is not None) 
            and (next((a for a in OLD.original_artifacts if a.artifact_id == event.artifact.artifact_id), None) is not None) 
            and (next(a for a in task.artifacts if a.artifact_id == event.artifact.artifact_id).parts == (
                next(a for a in OLD.original_artifacts if a.artifact_id == event.artifact.artifact_id).parts + event.artifact.parts
            ))
        )
    )
)"""

    print(postcond)

    results = eval_postcond(method, postcond, 
                            mutant_idxs=[], 
                            ban_mutant_idxs=None, 
                            early_stop=True)

    print(results)

if __name__ == "__main__":
    # observe()
    eval()
