import numpy as np
import os, json
from src.ds import *
import random
from src.util import get_diff

KFS = ["jml_fail", "icontract_fail"]


def read_benchmark(p="data/step/7.reference") -> List[Method]:
    methods: List[Method] = []
    for fn in os.listdir(p):
        with open(f"{p}/{fn}") as f:
            method = Method.from_dict(json.load(f))
            methods.append(method)
    return methods

if __name__ == "__main__":
    output_path = "data/step/8.benchmark"

    methods = read_benchmark()


    count_map = {
        "python": {"lt5": 0, "kl": 0},
        "java": {"lt5": 0, "kl": 0}
    }

    for method in methods:
        if method.ref_mutant_kill is None:
            continue
        mutant_idxs = [i for i, f in enumerate(method.ref_mutant_kill) 
                       if f in KFS]
        if len(method.ref_mutant_kill):
            count_map[method.repo.language]["lt5"] += 1
            if all(f in KFS for f in method.ref_mutant_kill):
                count_map[method.repo.language]["kl"] += 1
        # if len(mutant_idxs) < 5:
        #     continue
        # method.mutants = [
        #     m for i, m in enumerate(method.mutants)
        #     if i in mutant_idxs]
        # method.mutant_tags = [
        #     m for i, m in enumerate(method.mutant_tags)
        #     if i in mutant_idxs]
        # if method.ref_mutant_kill:
        #     method.ref_mutant_kill = [
        #         m for i, m in enumerate(method.ref_mutant_kill)
        #         if i in mutant_idxs]
        # file_name = f"{method.repo.github_path.replace('/', '--')}--{method.rlid}.json"
        # with open(f"{output_path}/{file_name}", "w") as file:
        #     json.dump(method.to_dict(), file, indent=2)
    print(json.dumps(count_map, indent=2))