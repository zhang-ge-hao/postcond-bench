
from src.ds import *
import os
from src.util import get_diff
from multiprocessing import Pool

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
        assert not os.path.exists(output_path), output_path
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

    langs = [
        # "python", 
        "java"
    ]
    SAMPLE_RNAGE = {
        "python": (200, 340),
        "java": (270, 276),
    }
    mut_theo = 5
    methods = read_benchmark("data/step/8.benchmark_m")
    for lang in langs:
        sample_range = SAMPLE_RNAGE[lang]
        print(lang)
        lang_methods = [m for m in methods if m.repo.language == lang]
        lang_methods.sort(key=lambda m: m.traversal_rank)
        count = 0
        method_count = 0
        mutant_count = 0
        for method in lang_methods:
            if len(method.mutants) < mut_theo:
                continue

            count += 1
            if count - 1 < sample_range[0] or count - 1 >= sample_range[1]:
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

            if count >= sample_range[1]:
                print(f"rank: {method.traversal_rank}")
                break
        print(f"method need attention: {method_count}")
        print(f"mutant need attention: {mutant_count}")


def write_final_benchmark():

    key_2_postcond = {}
    eval_results = {}
    filtered_keys = []
    for dir in ["data/ground_truth/java", "data/ground_truth/python"]:
        with open(f"{dir}/eval_results.json") as file:
            _eval_results = json.load(file)
        eval_results = {**eval_results, **_eval_results}
        for fn in os.listdir(f"{dir}/filtered"):
            filtered_keys.append(fn[6:-3])
        for fn in os.listdir(dir):
            if not fn.endswith(".md"):
                continue
            with open(f"{dir}/{fn}") as file:
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
            key_2_postcond[fn[6:-3]] = postcond

    langs = [
        "python", 
        "java"
    ]
    mut_theo = 5
    methods = read_benchmark("data/step/7.reference")
    for lang in langs:
        print(lang)
        lang_methods = [m for m in methods if m.repo.language == lang]
        lang_methods.sort(key=lambda m: m.traversal_rank)
        auto_written_count = 0
        human_written_count = 0
        for method in lang_methods:
            key = method.repo.github_path.replace("/", "--") + "--" + method.rlid

            if len(method.mutants) < mut_theo:
                continue

            if method.ref_postcond is not None and all(f in KFS for f in method.ref_mutant_kill):
                method.ref_source = "auto"
                auto_written_count += 1
                with open(f"data/step/8.benchmark/{key}.json", "w") as file:
                    json.dump(method.to_dict(), file, indent=2)
            elif key in key_2_postcond and key in eval_results:
                method.ref_source = "human"
                human_written_count += 1
                method.ref_postcond = key_2_postcond[key]
                method.ref_mutant_kill = eval_results[key]
                with open(f"data/step/8.benchmark/{key}.json", "w") as file:
                    json.dump(method.to_dict(), file, indent=2)
            else:
                assert key in filtered_keys

            if auto_written_count + human_written_count == 230:
                break
        print(lang, auto_written_count, human_written_count)


def cal_methods():
    lang = "java"
    idx_theo = 324
    mut_theo = 5
    
    methods = read_benchmark("data/step/8.benchmark_m")
    lang_methods = [m for m in methods if m.repo.language == lang and m.traversal_rank < idx_theo]
    lang_methods.sort(key=lambda m: m.traversal_rank)
    count = 0
    mutant_count = 0
    for method in lang_methods:
        if len(method.mutants) < mut_theo:
            continue
        if method.ref_postcond and all(f in KFS for f in method.ref_mutant_kill):
            count += 1
            mutant_count += len(method.ref_mutant_kill)
            print(method.traversal_rank, end=", ")
    print()

    print(count)
    print(mutant_count)


def eval(method_fn, mut_idxs = None, ban_mut_idxs = None, early_stop = False):
    print(f"{method_fn} start")

    from src.curator.eval_postcond import eval_postcond

    method_dir = "data/step/8.benchmark"
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
                                mutant_idxs=mut_idxs, 
                                ban_mutant_idxs=ban_mut_idxs, 
                                early_stop=early_stop)

    print(f"{method_fn} done")

    return method_fn, results


if __name__ == "__main__":
    # cal_methods()
    # exit()

    # write_doc()
    # exit()

    # write_final_benchmark()
    # exit()

    method_fn = "keon--algorithms--k_closest"
    mut_idxs = [10]
    ban_mut_idxs = None
    early_stop = True
    method_fn, results = eval(
        method_fn=method_fn,
        mut_idxs=mut_idxs,
        ban_mut_idxs=ban_mut_idxs,
        early_stop=early_stop
    )
    print(results)

    # method_fns = os.listdir("data/ground_truth/java")
    # method_fns = [fn for fn in method_fns if fn.endswith(".md")]
    # method_fns = [fn[6: -3] for fn in method_fns]

    # print("\n".join(method_fns))
    # print(len(method_fns))

    # pool_size = 30

    # with Pool(processes=pool_size) as pool:
    #     # map 会把 method_fns 逐个传给 eval_one
    #     outputs = pool.map(eval, method_fns)

    # # 收集成 dict: method_fn -> results
    # result_dict = {method_fn: results for method_fn, results in outputs}

    # # 存成 json 文件
    # out_path = "eval_results.json"
    # with open(out_path, "w", encoding="utf-8") as f:
    #     json.dump(result_dict, f, ensure_ascii=False, indent=2)

    # print(f"Saved results to {out_path}")
