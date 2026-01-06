
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

def sample():
    C2P_methods = read_benchmark("data/step/9.gpt-5--w_code")
    N2P_methods = read_benchmark("data/step/9.gpt-5--wo_code")

    methods_list = C2P_methods + N2P_methods

    langs = ["python", "java"]
    w_code_li = [True, False]

    methods = {lang: {w_code: [] for w_code in w_code_li} 
            for lang in langs}


    random.seed(99)

    for lang, lang_methods in methods.items():
        for w_code, w_code_methods in lang_methods.items():
            w_code_methods.extend([
                m for m in methods_list 
                if m.repo.language == lang and m.w_code == w_code])
            w_code_methods.sort(key=lambda m: m.traversal_rank)

    postconds = {lang: {w_code: {"corr": [], "comp": []} for w_code in w_code_li} 
            for lang in langs}

    for lang, lang_methods in methods.items():
        for w_code, w_code_methods in lang_methods.items():
            w_code_postconds = postconds[lang][w_code]
            for m in w_code_methods:
                for p_idx in range(5):
                    if m.postcond_corr[p_idx] != "passed":
                        w_code_postconds["corr"].append((p_idx, m))
                    else:
                        mutant_kill = m.mutant_kill[p_idx]
                        assert len(mutant_kill) == len(m.ref_mutant_kill)
                        for m_idx, (f, r_f) in enumerate(zip(mutant_kill, m.ref_mutant_kill)):
                            if r_f in KFS and f not in KFS:
                                w_code_postconds["comp"].append((m_idx, p_idx, m))

            random.shuffle(w_code_postconds["corr"])
            random.shuffle(w_code_postconds["comp"])

            print(len(w_code_postconds["corr"]))
            print(len(w_code_postconds["comp"]))

    sample_size = 20

    for lang, lang_postconds in postconds.items():
        for w_code, w_code_postconds in lang_postconds.items():
            w_code_postconds["corr"] = w_code_postconds["corr"][: sample_size]
            w_code_postconds["comp"] = w_code_postconds["comp"][: sample_size]
            for rank, (p_idx, m) in enumerate(w_code_postconds["corr"]):
                dir = f"data/gpt-5_analysis/{m.repo.language}--" + ("w_code" if m.w_code else "wo_code")
                rn = m.repo.github_path.replace("/", "--")
                fn = f"corr--{rank:03d}--{rn}--{m.rlid}--{p_idx}.md"
                postcond = m.postconds[p_idx]
                corr_res = m.postcond_corr[p_idx]
                with open(f"{dir}/{fn}", "w") as file:
                    file.write(m.github_url + "\n")
                    file.write(f"```\n{postcond}\n```\n")
                    file.write(f"```\n\n```\n")
                    file.write(str(corr_res) + "\n")
                    file.write(f"```\n{m.ref_postcond}\n```\n")

            for rank, (m_idx, p_idx, m) in enumerate(w_code_postconds["comp"]):
                dir = f"data/gpt-5_analysis/{m.repo.language}--" + ("w_code" if m.w_code else "wo_code")
                rn = m.repo.github_path.replace("/", "--")
                fn = f"comp--{rank:03d}--{rn}--{m.rlid}--{p_idx}--{m_idx}.md"
                postcond = m.postconds[p_idx]
                corr_res = m.postcond_corr[p_idx]
                comp_res = m.mutant_kill[p_idx][m_idx]
                mutant = m.mutants[m_idx]
                with open(f"{dir}/{fn}", "w") as file:
                    file.write(m.github_url + "\n")
                    file.write(f"```\n{postcond}\n```\n")
                    file.write(f"```\n\n```\n")
                    file.write(str(corr_res) + "\n")
                    file.write(f"```\n{m.ref_postcond}\n```\n")
                    file.write(f"===== {m_idx} =====\n")
                    file.write(str(comp_res) + "\n")
                    file.write(f"```\n{get_diff(m.content, mutant)}\n```\n")
                    file.write(f"```\n{mutant}\n```\n")


def eval(dir, method_fn, mut_idxs = None, ban_mut_idxs = None):
    print(f"{method_fn} start")

    from src.curator.eval_postcond import eval_postcond

    method_dir = "data/step/8.benchmark"
    with open(f"{method_dir}/{method_fn}.json") as file:
        method = Method.from_dict(json.load(file))
    for file_name in os.listdir(dir):
        if f"--{method_fn}--" in file_name:
            manual_doc = f"{dir}/{file_name}"
            break
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
                                early_stop=False)

    print(f"{method_fn} done")

    prompt = f"""原方法：
```
{method.content}
```
Buggy版本：
```
{method.mutants[mut_idxs[0]]}
```
postcondition：
```
{postcond}
```
报错：
```

```
这是icontract的一组postcondition，要校验的方法，以及一个buggy版本。
我们觉得一组完备的postcondition是要在随buggy版本运行的时候报icontract.ViolationError的。
现在这组postcondition随正确方法运行可以不报错，但不够完备，随buggy版本运行的时候没有报出icontract.ViolationError。
上面我也给出了postcondition随buggy运行时候的报错。
帮我看下怎么回事。
"""
    print(prompt)
    return method_fn, results


if __name__ == "__main__":
    # sample()
    # exit()

    dir = "data/gpt-5_analysis/python--w_code"
    fn = "comp--004--kellyjonbrazil--jc--_process-125--0--4"
    method_fn = "--".join(fn.split("--")[2: -2]) if fn.startswith("comp") else "--".join(fn.split("--")[2: -1])
    mut_idxs = [int(fn.split("--")[-1])] if fn.startswith("comp") else []
    ban_mut_idxs = None
    early_stop = True
    method_fn, results = eval(
        dir=dir,
        method_fn=method_fn,
        mut_idxs=mut_idxs,
        ban_mut_idxs=ban_mut_idxs,
    )
