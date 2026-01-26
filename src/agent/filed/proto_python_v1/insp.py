
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

    github_url = "https://github.com/z3z1ma/dbt-osmosis/blob/cd453ea69e9473e45df5390d8bb2a41e201dd4ee/./src/dbt_osmosis/core/introspection.py#L83-L159"
    p_idx = 0

    methods = read_benchmark("data/step/9.Qwen3-32B-reason--v2-all")

    method = [m for m in methods if m.github_url == github_url][0]
    postcond = method.postconds[p_idx]

    postcond = """
icontract.snapshot(lambda node: node.meta if node is not None else {}, name="node_meta")
icontract.snapshot(lambda node: node.config.extra if node is not None else {}, name="node_config_extra")
icontract.ensure(
    lambda result, node, opt, fallback, OLD: 
        (node is not None and result == fallback and not any(
            opt.replace("_", "-") in source or 
            opt.replace("-", "_") in source or 
            f"dbt-osmosis-{opt.replace('_', '-')}" in source or 
            f"dbt_osmosis_{opt.replace('-', '_')}" in source 
            for source in [OLD.node_meta, OLD.node_config_extra]
        ))
)"""

    print(postcond)

    results = eval_postcond(method, postcond, 
                            mutant_idxs=[], 
                            ban_mutant_idxs=None, 
                            early_stop=True)

    print(results)