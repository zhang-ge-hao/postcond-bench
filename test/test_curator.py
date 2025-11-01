
from src.curator import ref_gen_pool
from src.ds import *
from src.curator.eval_postcond import eval_postcond

if __name__ == "__main__":

    method_path = "data/step/7.reference/a2aproject--a2a-python--routes.json"
    with open(method_path) as file:
        method = Method.from_dict(json.load(file))

    mutant = method.mutants[20]
    print(mutant)

    method.mutants = [mutant]

    eval_postcond(method, method.ref_postcond)

    # ref_gen_pool(
    #     input_dir="data/step/6.mutation",
    #     output_dir="data/step/7.reference"
    # )
