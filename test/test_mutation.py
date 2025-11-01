

from src.mutation import (
    mutant_generation,
    mutant_generation_pool
)
from src.ds import *
from src.clone import repository_reproduct
import os
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--task_num", type=int, default=None)
    parser.add_argument("--task_idx", type=int, default=None)
    args = parser.parse_args()

    # input_dir = "data/step/5.exec_check/ajanata--PretendYoureXyzzy.jsonl"
    # methods = Method.load_li(input_dir)
    # method = methods[0]

    # input_dir = "data/step/5.exec_check/SolaceLabs--solace-agent-mesh.jsonl"
    # methods = Method.load_li(input_dir)
    # method = methods[1]

    # method = mutant_generation(method)

    # method_path = "data/step/6.mutation_update/kellyjonbrazil--jc--_process-94.json"
    # method_path = "data/step/6.mutation_update/capitalone--datacompy--_get_mismatch_stats.json"
    # with open(method_path) as file:
    #     method = Method.from_dict(json.load(file))

    # mutant_generation(method, None)

    methods = []
    input_dir = "data/step/6.mutation"
    for fn in os.listdir(input_dir):
        input_path = f"{input_dir}/{fn}"
        if input_path.endswith(".json"):
            with open(input_path) as file:
                method = Method.from_dict(json.load(file))
            # ===== debug =====
            if method.repo.language != "python":
                continue
            # ===== debug =====
            methods.append(method)

    mutant_generation_pool(
        methods=methods,
        output_dir="data/step/6.mutation_update",
        task_num=args.task_num,
        task_idx=args.task_idx
    )
