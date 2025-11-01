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


def overall():
    methods = read_benchmark("data/step/7.reference_update")

    py_ms = [m for m in methods if m.repo.language == "python"]
    java_ms = [m for m in methods if m.repo.language == "java"]

    print("Count Python: ", len(py_ms))
    print("Count Java: ", len(java_ms))

    print("Python methods w/ corr ref: ", 
        len([m for m in py_ms if m.ref_postcond is not None]))
    print("Java methods w/ corr ref: ", 
        len([m for m in java_ms if m.ref_postcond is not None]))

    print("Python methods w/ complete ref: ", 
        len([m for m in py_ms if m.ref_postcond is not None and \
            all(f in KFS for f in m.ref_mutant_kill)]))
    print("Java methods w/ complete ref: ", 
        len([m for m in java_ms if m.ref_postcond is not None and \
            all(f in KFS for f in m.ref_mutant_kill)]))

    py_mutant_counts = [len(m.mutants) for m in py_ms]
    java_mutant_counts = [len(m.mutants) for m in java_ms]
    print("Mutant count Python:", 
        sum(py_mutant_counts), "/", len(py_mutant_counts), "=", 
        f"{np.mean(py_mutant_counts):.1f}", "Med:", np.median(py_mutant_counts),
        "Max:", max(py_mutant_counts))
    print("Mutant count Java:", 
        sum(java_mutant_counts), "/", len(java_mutant_counts), "=", 
        f"{np.mean(java_mutant_counts):.1f}", "Med:", np.median(java_mutant_counts))

    py_mutant_counts_killed = [0 if not m.ref_mutant_kill 
                            else len([f for f in m.ref_mutant_kill if f in KFS]) 
                            for m in py_ms]
    java_mutant_counts_killed = [0 if not m.ref_mutant_kill 
                                else len([f for f in m.ref_mutant_kill if f in KFS]) 
                                for m in java_ms]
    print("Killed Mutant count Python (=0 when no correct reference methods):\n", 
        sum(py_mutant_counts_killed), "/", len(py_mutant_counts_killed), "=", 
        f"{np.mean(py_mutant_counts_killed):.1f}", "Med:", np.median(py_mutant_counts_killed))
    print("Killed Mutant count Java (=0 when no correct reference methods):\n", 
        sum(java_mutant_counts_killed), "/", len(java_mutant_counts_killed), "=", 
        f"{np.mean(java_mutant_counts_killed):.1f}", "Med:", np.median(java_mutant_counts_killed))
    
    print("Python methods w/ >=5 Killed mutants:\n",
          len([c for c in py_mutant_counts_killed if c >= 5]))
    print("Java methods w/ >=5 Killed mutants:\n",
          len([c for c in java_mutant_counts_killed if c >= 5]))

def comp_mutant_and_update():
    methods_ori = read_benchmark("data/step/6.mutation")
    methods = [m for m in methods_ori if m.repo.language == "python"]
    methods_update = read_benchmark("data/step/6.mutation_update")
    print(len(methods))
    print(len(methods_update))
    print("===")

    mean_v = np.mean([len(m.mutants) for m in methods])
    med_v = np.median([len(m.mutants) for m in methods])
    mean_v_update = np.mean([len(m.mutants) for m in methods_update])
    med_v_update = np.median([len(m.mutants) for m in methods_update])
    print(mean_v)
    print(med_v)
    print(mean_v_update)
    print(med_v_update)
    print("===")

    methods = [m for m in methods_ori if m.repo.language == "java"]
    mean_v = np.mean([len(m.mutants) for m in methods])
    med_v = np.median([len(m.mutants) for m in methods])
    print(mean_v)
    print(med_v)

def diff_update():
    methods_update = read_benchmark("data/step/6.mutation_update")
    diffs = []
    for method in methods_update:
        for mutant in method.mutants:
            diff_str = get_diff(method.content, mutant)
            lines = diff_str.split("\n")
            if len([l for l in lines if l.startswith("+")]) > 1:
                diffs.append((method, diff_str))
    print(len(diffs))
    diffs = random.sample(diffs, 10)
    for method, diff_str in diffs:
        print(method.github_url)
        print("-" * 30)
        print(diff_str)

        print("=" * 30)


def sample_suv_mutants():
    methods = read_benchmark()

    methods_and_mutants = []

    for m in methods:
        if m.ref_mutant_kill:
            for mutant, f in zip(m.mutants, m.ref_mutant_kill):
                if f not in KFS:
                    methods_and_mutants.append((m, mutant))
    
    methods_and_mutants = random.sample(methods_and_mutants, 10)
    for method, mutant in methods_and_mutants:
        print(method.github_url)
        print("-" * 30)
        print(mutant)
        print("-" * 30)
        
        diff_str = get_diff(method.content, mutant)
        print(diff_str)

        print("=" * 30)


def update_ref():
    methods_ref = read_benchmark("data/step/7.reference")
    methods_mu = read_benchmark("data/step/6.mutation")
    method_pairs: List[Tuple[Method, List[str]]] = []
    for method_ref in methods_ref:
        for method_mu in methods_mu:
            if method_mu.github_url == method_ref.github_url:
                method_pairs.append((method_ref, method_mu.mutants))
                continue
    assert len(method_pairs) == len(methods_ref)
    print(len(methods_ref))
    print(len(method_pairs))
    for method, mutants in method_pairs:
        mutant_idxs = [i for i, m in enumerate(method.mutants) 
                       if m in mutants]
        method.mutants = [
            m for i, m in enumerate(method.mutants)
            if i in mutant_idxs]
        method.mutant_tags = [
            m for i, m in enumerate(method.mutant_tags)
            if i in mutant_idxs]
        if method.ref_mutant_kill:
            method.ref_mutant_kill = [
                m for i, m in enumerate(method.ref_mutant_kill)
                if i in mutant_idxs]
        file_name = f"{method.repo.github_path.replace('/', '--')}--{method.rlid}.json"
        with open(f"data/step/7.reference_update/{file_name}", "w") as file:
            json.dump(method.to_dict(), file)

if __name__ == "__main__":
    overall()
    # update_ref()
    # sample_suv_mutants()