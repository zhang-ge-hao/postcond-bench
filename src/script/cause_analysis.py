
from src.ds import *
import os
from src.util import get_diff
from multiprocessing import Pool
import random

KFS = ["jml_fail", "icontract_fail"]

def read_benchmark(p) -> List[Method]:
    methods: List[Method] = []
    for fn in os.listdir(p):
        with open(f"{p}/{fn}") as f:
            method = Method.from_dict(json.load(f))
            methods.append(method)
    return methods

def read_benchmark_with_exclude(p) -> List[Method]:
    methods = read_benchmark(p)
    with open("data/cause_analysis/comment_filter.md") as file:
        doc_liens = [l.strip() for l in file]
    exluded_methods: List[Method] = []
    for m in methods:
        rn = m.repo.github_path.replace("/", "--")
        pat = f"[x] {rn}--{m.rlid}"
        if pat not in doc_liens:
            exluded_methods.append(m)
    ex_methods_python = [m for m in exluded_methods if m.repo.language == "python"]
    ex_methods_java = [m for m in exluded_methods if m.repo.language == "java"]
    print(len(ex_methods_python), len(ex_methods_java))
    ex_methods_python.sort(key=lambda m: m.traversal_rank)
    ex_methods_java.sort(key=lambda m: m.traversal_rank)
    min_len = min(len(ex_methods_python), len(ex_methods_java))
    ex_methods_python = ex_methods_python[: min_len]
    ex_methods_java = ex_methods_java[: min_len]
    return ex_methods_python + ex_methods_java

def sample_corr():
    root_dir = "data/step"
    model_names = ["claude-sonnet-4-5", "gpt-5"]

    methods: List[Method] = []
    for dir_name in os.listdir(root_dir):
        if any(dir_name.startswith(f"9.{mn}") for mn in model_names):
            methods.extend(read_benchmark_with_exclude(f"{root_dir}/{dir_name}"))

    random.seed(99)

    methods.sort(key=lambda m: (
        m.model_name, m.prompting, m.repo.language, m.traversal_rank))

    incorr_postconds: List[Tuple[Method, int]] = []

    for method in methods:
        for p_idx in range(5):
            if method.postcond_corr[p_idx] != "passed":
                incorr_postconds.append((method, p_idx))

    print(len(methods))
    print(len(incorr_postconds))
    incorr_postconds = random.sample(incorr_postconds, 5)

    for method, p_idx in incorr_postconds:
        dir = f"data/cause_analysis/corr"
        rn = method.repo.github_path.replace("/", "--")
        fn = f"{rn}--{method.rlid}--{method.model_name}--{method.prompting}--{p_idx}.md"
        postcond = method.postconds[p_idx]
        corr_res = method.postcond_corr[p_idx]
        with open(f"{dir}/{fn}", "w") as file:
            file.write(method.github_url + "\n")
            file.write(f"```\n{postcond}\n```\n")
            file.write(f"```\n\n```\n")
            file.write(str(corr_res) + "\n")
            file.write(f"```\n{method.ref_postcond}\n```\n")


def sample_comp():
    root_dir = "data/step"
    model_names = ["claude-sonnet-4-5", "gpt-5"]

    methods: List[Method] = []
    for dir_name in os.listdir(root_dir):
        if any(dir_name.startswith(f"9.{mn}") for mn in model_names):
            methods.extend(read_benchmark_with_exclude(f"{root_dir}/{dir_name}"))

    random.seed(99)

    methods.sort(key=lambda m: (
        m.model_name, m.prompting, m.repo.language, m.traversal_rank))

    incorr_postconds: List[Tuple[Method, int]] = []

    for method in methods:
        for p_idx in range(5):
            if method.postcond_corr[p_idx] == "passed":
                assert len(method.mutant_kill[p_idx]) == len(method.ref_mutant_kill)
                for m_idx, (f, r_f) in enumerate(zip(method.mutant_kill[p_idx], method.ref_mutant_kill)):
                    if r_f in KFS and f not in KFS:
                        incorr_postconds.append((method, p_idx, m_idx))

    print(len(methods))
    print(len(incorr_postconds))
    incorr_postconds = random.sample(incorr_postconds, 50)

    for method, p_idx, m_idx in incorr_postconds:
        dir = f"data/cause_analysis/comp"
        rn = method.repo.github_path.replace("/", "--")
        fn = f"{rn}--{method.rlid}--{method.model_name}--{method.prompting}--{p_idx}-{m_idx}.md"
        postcond = method.postconds[p_idx]
        corr_res = method.postcond_corr[p_idx]
        with open(f"{dir}/{fn}", "w") as file:
            file.write(method.github_url + "\n")
            file.write(f"```\n{postcond}\n```\n")
            file.write(f"```\n\n```\n")
            file.write(str(corr_res) + "\n")
            file.write(f"```\n{method.ref_postcond}\n```\n")

            mutant = method.mutants[m_idx]
            file.write(f"===== {m_idx}: {method.mutant_kill[p_idx][m_idx]} =====\n")
            file.write(f"```\n{get_diff(method.content, mutant)}\n```\n")
            file.write(f"```\n{mutant}\n```\n")


def classify_corr():
    classes_map = {}
    for fn in os.listdir("data/cause_analysis/corr"):
        with open(f"data/cause_analysis/corr/{fn}") as file:
            lines = file.readlines()
        cb_count = 0
        for l_idx, line in enumerate(lines):
            if line.startswith("```"):
                cb_count += 1
            if cb_count == 3:
                label = lines[l_idx + 1]
                if label not in classes_map:
                    classes_map[label] = 0
                classes_map[label] += 1
                break
    print(json.dumps(classes_map, indent=2))


def classify_comp():
    classes_map = {}
    for fn in os.listdir("data/cause_analysis/comp"):
        with open(f"data/cause_analysis/comp/{fn}") as file:
            lines = file.readlines()
        cb_count = 0
        for l_idx, line in enumerate(lines):
            if line.startswith("```"):
                cb_count += 1
            if cb_count == 3:
                label = lines[l_idx + 1]
                if label not in classes_map:
                    classes_map[label] = 0
                classes_map[label] += 1
                break
    print(json.dumps(classes_map, indent=2))


def all_comments():
    methods = read_benchmark("data/step/8.benchmark")
    with open("data/cause_analysis/comment_filter.md", "w") as file:
        for m in methods:
            rn = m.repo.github_path.replace("/", "--")
            file.write(f"[ ] {rn}--{m.rlid}\n")
            file.write(m.github_url + "\n")
            file.write(f"```\n{m.content}\n```\n")


def eval(dir, fn, mut_idxs = None, ban_mut_idxs = None):
    method_fn = "--".join(fn.split("--")[: -3])
    print(f"{method_fn} start")

    from src.curator.eval_postcond import eval_postcond

    method_dir = "data/step/8.benchmark"
    with open(f"{method_dir}/{method_fn}.json") as file:
        method = Method.from_dict(json.load(file))
    manual_doc = f"{dir}/{fn}.md"
    with open(manual_doc) as file:
        lines = []
        in_block = False
        for line in file:
            if line.startswith("```") and not in_block:
                in_block = True
            elif line.startswith("```") and in_block:
                break
            elif in_block:
                lines.append(line)
        postcond = "".join(lines)
        
        # results = eval_postcond(method, postcond, mutant_idx=mut_idx)
        results = eval_postcond(method, postcond, 
                                mutant_idxs=mut_idxs, 
                                ban_mutant_idxs=ban_mut_idxs, 
                                early_stop=True)

    print(f"{method_fn} done")

    prompt = f"""原方法：
```
{method.content}
```
postcondition：
```
{postcond}
```
报错：
```

```
这是icontract的一组postcondition以及要校验的方法。
现在这组postcondition随正确方法运行的时候报错了。
帮我看下怎么回事。
"""
    print(prompt)
    return method_fn, results


if __name__ == "__main__":
    # sample_corr()
    # exit()

    # sample_comp()
    # exit()

    # all_comments()
    # exit()

    classify_corr()
    classify_comp()
    exit()

    # # corr
    # dir = "data/cause_analysis/corr"
    # fn = "dynaconf--dynaconf--_ensure_serializable--claude-sonnet-4-5--v2-nl--0"
    # method_fn, results = eval(dir=dir, fn=fn, mut_idxs=[])

    # # comp
    # dir = "data/cause_analysis/comp"
    # fn = "wntrblm--nox--_find_pbs_python--claude-sonnet-4-5--v2-code--0-22"
    # mut_idx = int(fn.split("-")[-1])
    # method_fn, results = eval(dir=dir, fn=fn, mut_idxs=[mut_idx])
