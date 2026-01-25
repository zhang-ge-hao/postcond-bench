
from src.ds import *
import os
from src.util import get_diff
from multiprocessing import Pool
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


if __name__ == "__main__":

    github_url = "https://github.com/beanshell/beanshell/blob/eee36c81c35525fd771285e77b6fb8173db3f1dc/./src/main/java/bsh/org/objectweb/asm/SymbolTable.java#L843-L866"
    p_idx = 0

    methods = read_benchmark("data/step/9.Qwen3-32B-reason--v2-all")

    method = [m for m in methods if m.github_url == github_url][0]
    postcond = method.postconds[p_idx]

#     postcond = """
# //@ ensures (check ==> message == \old(message)) && (!check ==> message.size() == \old(message.size()) + p.size() - 1);
# """

    print(postcond)

    results = eval_postcond(method, postcond, 
                            mutant_idxs=[], 
                            ban_mutant_idxs=None, 
                            early_stop=True)

    print(results)