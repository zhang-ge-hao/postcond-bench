


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
    input_dir = "data/step/9.Qwen3-32B-reason--v2-all"

    methods = read_benchmark(input_dir)
    methods = [m for m in methods if m.repo.language == "java"]

    counts = [0, 0, 0, 0]
    for m in methods:
        if m.postcond_corr[0] != "passed" and m.postcond_corr[0] != "jml_fail":
            counts[0] += 1
        if m.postcond_corr[0] == "jml_fail":
            counts[1] += 1
            print(m.github_url)
            print("-" * 30)
            print(m.content)
            print("-" * 30)
            print(m.postconds[0])
            print("=" * 30)
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
    github_url = "https://github.com/keon/algorithms/blob/5b63e90624bebb371949fbe49bbf20aa3c8e14d0/./algorithms/compression/huffman_coding.py#L87-L102"
    p_idx = 0

    methods = read_benchmark("data/step/9.Qwen3-32B-reason--v2-all")

    method = [m for m in methods if m.github_url == github_url][0]
    postcond = method.postconds[p_idx]

    postcond = r"""
@icontract.snapshot(lambda self: list(self.buffer), name="old_buffer")
@icontract.snapshot(lambda self: len(self.buffer), name="old_len")
@icontract.snapshot(lambda self: self.file.tell(), name="old_pos")
@icontract.snapshot(lambda self: (len(self.file.getbuffer()) - self.file.tell()) if hasattr(self.file, "getbuffer") else None, name="old_remaining")
@icontract.ensure(lambda self, result, OLD: (not result) <= (self.buffer == OLD.old_buffer))
@icontract.ensure(lambda self, result, OLD, buff_limit: result <= ((OLD.old_len > buff_limit and len(self.buffer) == OLD.old_len) or (OLD.old_len <= buff_limit and len(self.buffer) == OLD.old_len + 8)))
@icontract.ensure(lambda self, result, OLD: (not result) <= (self.file.tell() == OLD.old_pos))
@icontract.ensure(lambda self, result, OLD, buff_limit: (OLD.old_remaining is None) or (OLD.old_remaining == 0) or (OLD.old_len > buff_limit) or result)
@icontract.ensure(lambda self: all(bit in ("0", "1") for bit in self.buffer))
"""

    print(postcond)

    results = eval_postcond(method, postcond, 
                            mutant_idxs=[]
                            )

    print(results)

if __name__ == "__main__":
    # observe()
    eval()
