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
    methods = read_benchmark("data/step/8.benchmark")

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


def cal_metrics(methods: List[Method]):
    res_list = []
    for method in methods:
        for corr_res, comp_res in zip(method.postcond_corr, method.mutant_kill):
            res_list.append((corr_res, comp_res))
    tot_count = len(res_list)
    corr_count = len([
        corr_res for corr_res, comp_res in res_list
        if corr_res == "passed"])
    comp_count = len([
        corr_res for corr_res, comp_res in res_list
        if corr_res == "passed" \
            and all(f in KFS for f in comp_res)])
    if tot_count == 0:
        return tot_count, corr_count, comp_count, 0.0, 0.0
    return tot_count, corr_count, comp_count, corr_count / tot_count, comp_count / tot_count

def mutator_precision(methods: List[Method]):
    tags = ["rule", "llm"]
    res_list = []
    exist_list = {t: [] for t in tags}
    for method in methods:
        for corr_res, comp_res in zip(method.postcond_corr, method.mutant_kill):
            res_list.append((corr_res, comp_res, method.mutant_tags))
        
        method_mut_tags = set()
        for __tags in method.mutant_tags:
            for __tag in __tags:
                method_mut_tags.add(__tag)
        for tag in tags:
            exist_list[tag].append(1 if tag in method_mut_tags else 0)

    precision_list = {t: [] for t in tags}
    for corr_res, comp_res, mutant_tags in res_list:
        if corr_res == "passed":
            comp_res_bool = all([f in KFS for f in comp_res])
            for tag in tags:
                tag_comp_res = [
                    f for f, mutant_tag in zip(comp_res, mutant_tags) 
                    if tag in mutant_tag]
                if len(tag_comp_res) == 0:
                    continue
                tag_comp_res_bool = all([f in KFS for f in tag_comp_res])
                if tag_comp_res_bool:
                    precision_list[tag].append(1 if comp_res_bool else 0)
            pass
    return {t: sum(l) / len(l) for t, l in precision_list.items()}, \
            {t: sum(l) / len(l) for t, l in exist_list.items()}


def exp_res():
    dir_prefix = "data/step/9."
    # model_names = ["gpt-4.1", "gpt-4o-mini"]
    # model_names = ["gpt-4.1", "gpt-4o-mini", "claude-3-5-haiku", "Qwen3-8B"]
    model_names = ["Qwen3-32B"]
    # model_names = ["gemma-3-4b"]
    task_names = ["w_code", "wo_code"]
    promptings = [None, "no_gram", "fsl_1", "fsl_3", "fsl_5"]

    tn_map = {"w_code": "[code to postcond]", "wo_code": "[nl to postcond]"}
    p_map = {
        "no_gram": "No Grammar Guidance",
        "cot": "CoT",
        "fsl_1": "1-shot",
        "fsl_3": "3-shot",
        "fsl_5": "5-shot",
    }

    for model_name in model_names:
        for task_name in task_names:
            for prompting in promptings:
                result_dir = f"{dir_prefix}{model_name}--{task_name}"
                if prompting:
                    result_dir += f"--{prompting}"
                
                if not os.path.exists(result_dir):
                    continue

                methods = read_benchmark(result_dir)

                if len(methods) == 0:
                    continue

                py_ms = [m for m in methods if m.repo.language == "python"]
                java_ms = [m for m in methods if m.repo.language == "java"]

                _, _, py_comp_count, py_corr_rate, py_comp_rate = cal_metrics(py_ms)
                _, _, java_comp_count, java_corr_rate, java_comp_rate = cal_metrics(java_ms)

                title_line = f"{model_name}, {tn_map[task_name]}"
                if prompting:
                    title_line += f" {p_map[prompting]}"
                print(title_line)
                # print(f"Python corr: {corr_py:4d} / {count_py:4d} = {corr_py / count_py:.2f} comp: {comp_py:4d} / {count_py:4d} = {comp_py / count_py:.2f}")
                # print(f"  Java corr: {corr_java:4d} / {count_java:4d} = {corr_java / count_java:.2f} comp: {comp_java:4d} / {count_java:4d} = {comp_java / count_java:.2f}")
                print(f"Python corr: {py_corr_rate:.4f} comp: {py_comp_rate:.4f}  "
                      f"Java corr: {java_corr_rate:.4f} comp: {java_comp_rate:.4f}")

                if prompting is None:
                    with open("data/step/0.append/dep_anno_python.txt") as file:
                        dep_anno_python: Dict[str, str] = {l.split("\t")[0]: l.strip().split("\t")[1] for l in file}
                    with open("data/step/0.append/dep_anno_java.txt") as file:
                        dep_anno_java: Dict[str, int] = {l.split("\t")[0]: l.strip().split("\t")[1] for l in file}
                    dep_anno = {**dep_anno_python, **dep_anno_java}
                    py_ms_wo_dep = [
                        m for m in methods 
                        if m.repo.language == "python" and \
                            dep_anno.get(m.github_url, None) == "0"]
                    py_ms_w_dep = [
                        m for m in methods 
                        if m.repo.language == "python" and \
                            dep_anno.get(m.github_url, None) == "1"]
                    java_ms_wo_dep = [
                        m for m in methods 
                        if m.repo.language == "java" and \
                            dep_anno.get(m.github_url, None) == "0"]
                    java_ms_w_dep = [
                        m for m in methods 
                        if m.repo.language == "java" and \
                            dep_anno.get(m.github_url, None) == "1"]
                    py_wo_dep_count, _, _, py_corr_rate_wo_dep, py_comp_rate_wo_dep = cal_metrics(py_ms_wo_dep)
                    py_w_dep_count, _, _, py_corr_rate_w_dep, py_comp_rate_w_dep = cal_metrics(py_ms_w_dep)
                    print(f"    With dep count: {py_w_dep_count}; Wo dep count: {py_wo_dep_count}")
                    print(f"    With dep:    Python corr: {py_corr_rate_w_dep:.4f} comp: {py_comp_rate_w_dep:.4f}")
                    print(f"    Without dep: Python corr: {py_corr_rate_wo_dep:.4f} comp: {py_comp_rate_wo_dep:.4f}")

                    java_wo_dep_count, _, _, java_corr_rate_wo_dep, java_comp_rate_wo_dep = cal_metrics(java_ms_wo_dep)
                    java_w_dep_count, _, _, java_corr_rate_w_dep, java_comp_rate_w_dep = cal_metrics(java_ms_w_dep)
                    print(f"    With dep count: {java_w_dep_count}; Wo dep count: {java_wo_dep_count}")
                    print(f"    With dep:    Java corr: {java_corr_rate_w_dep:.4f} comp: {java_comp_rate_w_dep:.4f}")
                    print(f"    Without dep: Java corr: {java_corr_rate_wo_dep:.4f} comp: {java_comp_rate_wo_dep:.4f}")
                    
                    if py_comp_count > 0:
                        py_mut_prec, py_mut_exi = mutator_precision(py_ms)
                        print(f"    Python mutator "
                            #   f"exist: rule: {py_mut_exi['rule']:.4f} "
                            #   f"llm: {py_mut_exi['llm']:.4f} "
                            f"precision: rule: {py_mut_prec['rule']:.4f} "
                            f"llm: {py_mut_prec['llm']:.4f} ")
                    if java_comp_count > 0:
                        java_mut_prec, java_mut_exi = mutator_precision(java_ms)
                        print(f"    Java mutator "
                            #   f"exist: rule: {java_mut_exi['rule']:.4f} "
                            #   f"llm: {java_mut_exi['llm']:.4f} "
                            f"precision: rule: {java_mut_prec['rule']:.4f} "
                            f"llm: {java_mut_prec['llm']:.4f} ")
                    pass

if __name__ == "__main__":
    exp_res()
    # update_ref()
    # sample_suv_mutants()