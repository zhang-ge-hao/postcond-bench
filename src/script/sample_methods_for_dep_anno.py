from src.ds import *
from typing import *
import os, json, random

def read_benchmark(p="data/step/8.benchmark") -> List[Method]:
    methods: List[Method] = []
    for fn in os.listdir(p):
        with open(f"{p}/{fn}") as f:
            method = Method.from_dict(json.load(f))
            methods.append(method)
    return methods

random.seed(42)

methods = read_benchmark()

java_methods = [m for m in methods if m.repo.language == "java"]
python_methods = [m for m in methods if m.repo.language == "python"]

java_methods.sort(key=lambda m: m.traversal_rank)
python_methods.sort(key=lambda m: m.traversal_rank)

java_methods = [m.github_url for m in java_methods]
python_methods = [m.github_url for m in python_methods]

random.shuffle(java_methods)
random.shuffle(python_methods)

java_methods = java_methods[60: 100]
python_methods = python_methods[60: 100]

print("\n".join(java_methods))
print()
print("\n".join(python_methods))
