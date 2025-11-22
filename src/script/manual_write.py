
from src.ds import *
import os
from src.util import get_diff

KFS = ["jml_fail", "icontract_fail"]

def read_benchmark(p="data/step/7.reference") -> List[Method]:
    methods: List[Method] = []
    for fn in os.listdir(p):
        with open(f"{p}/{fn}") as f:
            method = Method.from_dict(json.load(f))
            methods.append(method)
    return methods

def print_stat():
    langs = ["python", "java"]
    amount = 200
    mut_theo = 5
    methods = read_benchmark("data/step/8.benchmark_m")
    for lang in langs:
        print(lang)
        lang_methods = [m for m in methods if m.repo.language == lang]
        lang_methods.sort(key=lambda m: m.traversal_rank)
        count = 0
        method_count = 0
        mutant_count = 0
        for method in lang_methods:
            if len(method.mutants) < mut_theo:
                continue

            if method.ref_postcond is None:
                mut_count = len(method.mutants)
            elif any(f not in KFS for f in method.ref_mutant_kill):
                mut_count = len([f not in KFS for f in method.ref_mutant_kill])
            else:
                mut_count = 0
            if mut_count > 0:
                method_count += 1
                mutant_count += mut_count

            count += 1
            if count >= amount:
                print(f"rank: {method.traversal_rank}")
                break
        print(f"method need attention: {method_count}")
        print(f"mutant need attention: {mutant_count}")


def write_doc():

    def _write(method: Method):
        lang = method.repo.language
        rn = method.repo.github_path.replace("/", "--")
        fn = f"{method.traversal_rank:04d}--{rn}--{method.rlid}"
        output_path = f"data/ground_truth/{lang}/{fn}.md"
        with open(output_path, "w") as file:
            file.write(f"{method.github_url}\n")
            file.write("```\n```\n")
            file.write(f"```\n{method.ref_postcond}\n```\n")
            if method.ref_postcond is None:
                suv_mut_idxs = list(range(len(method.mutants)))
            else:
                suv_mut_idxs = [i for i, f in enumerate(method.ref_mutant_kill) if f not in KFS]
            file.write(str(suv_mut_idxs) + "\n")
            for mut_idx in suv_mut_idxs:
                mutant = method.mutants[mut_idx]
                file.write(f"===== {mut_idx} =====\n")
                file.write(f"```\n{get_diff(method.content, mutant)}\n```\n")
                file.write(f"```\n{mutant}\n```\n")

    langs = ["python", "java"]
    amount = 200
    mut_theo = 5
    methods = read_benchmark("data/step/8.benchmark_m")
    for lang in langs:
        print(lang)
        lang_methods = [m for m in methods if m.repo.language == lang]
        lang_methods.sort(key=lambda m: m.traversal_rank)
        count = 0
        method_count = 0
        mutant_count = 0
        for method in lang_methods:
            if len(method.mutants) < mut_theo:
                continue

            if method.ref_postcond is None:
                mut_count = len(method.mutants)
            elif any(f not in KFS for f in method.ref_mutant_kill):
                mut_count = len([f not in KFS for f in method.ref_mutant_kill])
            else:
                mut_count = 0
            if mut_count > 0:
                method_count += 1
                mutant_count += mut_count
                _write(method)

            count += 1
            if count >= amount:
                print(f"rank: {method.traversal_rank}")
                break
        print(f"method need attention: {method_count}")
        print(f"mutant need attention: {mutant_count}")


def eval():
    from src.curator.eval_postcond import eval_postcond
    method_fn = "pypyr--pypyr--keys_of_type_exist"
    mut_idx = None

    method_dir = "data/step/8.benchmark_m"
    with open(f"{method_dir}/{method_fn}.json") as file:
        method = Method.from_dict(json.load(file))
    manual_dir = f"data/ground_truth/{method.repo.language}"
    for file_name in os.listdir(manual_dir):
        if file_name.endswith(f"{method_fn}.md"):
            manual_doc = f"{manual_dir}/{file_name}"
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
                                mutant_idx=mut_idx, early_stop=True)
        print(results)


if __name__ == "__main__":
    eval()