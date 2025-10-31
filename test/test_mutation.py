

from src.mutation import (
    mutant_generation,
    mutant_generation_pool
)
from src.ds import *
from src.clone import repository_reproduct

if __name__ == "__main__":
    # input_dir = "data/step/5.exec_check/ajanata--PretendYoureXyzzy.jsonl"
    # methods = Method.load_li(input_dir)
    # method = methods[0]

    input_dir = "data/step/5.exec_check/SolaceLabs--solace-agent-mesh.jsonl"
    methods = Method.load_li(input_dir)
    method = methods[1]

    method = mutant_generation(method)

    # mutant_generation_pool(
    #     input_dir="data/step/5.exec_check",
    #     output_dir="data/step/6.mutation"
    # )
