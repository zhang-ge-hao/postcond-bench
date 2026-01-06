import numpy as np
import os, json
from src.ds import *
import random
from src.util import get_diff
import math
from dataclasses import dataclass, asdict, fields
from typing import List
import csv
from itertools import product

from copy import deepcopy
from multiprocessing import Pool  # 新增
import matplotlib.pyplot as plt
import re
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
from matplotlib import colors as mcolors   # 新增

import colorsys

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


methods = read_benchmark("data/step/8.benchmark")

method_map = {(m.repo.github_path, m.rlid): m for m in methods}

issue_paths = set()

for dir in os.listdir("data/step"):
    if dir.startswith("9.") and "fsl" not in dir:
        methods = read_benchmark(f"data/step/{dir}")
        assert len(methods) == 460
        for method in methods:
            bench_method = method_map[(method.repo.github_path, method.rlid)]
            method.ref_postcond = bench_method.ref_postcond
            method.ref_mutant_kill = bench_method.ref_mutant_kill
            method.ref_source = bench_method.ref_source

            rn = method.repo.github_path.replace("/", "--")
            fn = f"{rn}--{method.rlid}.json"
            out_path = f"data/step/{dir}/{fn}"
            assert os.path.exists(out_path)

            lengths = [len(method.mutants), len(method.mutant_tags), len(method.ref_mutant_kill)]
            if len(set(lengths)) != 1:
                issue_paths.add(out_path)

            for mut_res in method.mutant_kill:
                if len(mut_res) != 0 and len(mut_res) != len(method.ref_mutant_kill):
                    issue_paths.add(out_path)

print("\n".join(list(issue_paths)))
print(len(issue_paths))