import os, json, math, random
import numpy as np
from dataclasses import dataclass
from typing import List, Dict, Tuple
from itertools import product
from multiprocessing import Pool

from src.mutation.mutmut import generate_mutants_for_method as python_mut
from src.mutation.pit import generate_mutants_for_method as java_mut

from src.ds import Method  # 你已有的 Method 定义

KFS = ["jml_fail", "icontract_fail"]
LANGUAGES = ["python", "java"]
PROMPTINGS = ["v2-code", "v2-nl", "v2-all"]


# ========== IO ==========
def read_benchmark_dir(p: str, save_mem: bool = True) -> List[Method]:
    methods: List[Method] = []
    for fn in os.listdir(p):
        fp = os.path.join(p, fn)
        if not os.path.isfile(fp):
            continue
        with open(fp, "r", encoding="utf-8") as f:
            m = Method.from_dict(json.load(f))
            if save_mem:
                m.repo.env_config = None
                m.repo.failed_tests = None
                m.cover_tests = None
                m.mutants = None
                m.postconds = None
                m.responses = None
            methods.append(m)
    return methods


def load_all_methods_for_model(step_dir: str, model_name: str) -> List[Method]:
    all_methods: List[Method] = []
    for folder_name in os.listdir(step_dir):
        if not folder_name.startswith("9."):
            continue
        if folder_name.startswith(f"9.{model_name}--"):
            all_methods.extend(
                read_benchmark_dir(os.path.join(step_dir, folder_name), save_mem=True)
            )
    return all_methods


# ========== metrics ==========
def calculate_pass_1(n: int, c: int) -> float:
    """pass@1 = c/n (if n>0)"""
    if n <= 0:
        return 0.0
    return c / n


def _is_complete_under_subset(
    corr_res: str,
    comp_res: List[str],
    ref_mutant_kill: List[str],
    selected_mutant_indices: List[int],
) -> bool:
    if corr_res != "passed":
        return False
    if len(selected_mutant_indices) == 0:
        return False
    if len(comp_res) == 0:
        return False
    assert len(comp_res) == len(ref_mutant_kill), (len(comp_res), len(ref_mutant_kill))

    for i in selected_mutant_indices:
        r_f = ref_mutant_kill[i]
        f = comp_res[i]
        if r_f in KFS and f not in KFS:
            return False
    return True


def comp_at_1_for_methods_with_sampling(
    methods: List[Method],
    frac: float,
    rng: random.Random,
) -> Dict[str, float]:
    """
    Return:
      {
        "method_count": ...,
        "avg_sampled_mutants": ...,
        "comp_1": ...,
      }
    """
    assert 0 < frac <= 1.0
    assert len(methods) > 0

    generate_num = methods[0].generate_num
    assert all(m.generate_num == generate_num for m in methods)
    assert generate_num in (1, 5)

    pass1_list = []
    sampled_sizes = []

    for m in methods:
        total_muts = len(m.ref_mutant_kill) if m.ref_mutant_kill is not None else 0
        if total_muts <= 0:
            sampled_sizes.append(0)
            pass1_list.append(0.0)
            continue

        sample_size = int(round(total_muts * frac))
        sample_size = max(1, min(sample_size, total_muts))
        sampled_sizes.append(sample_size)

        selected = rng.sample(range(total_muts), k=sample_size)

        comp_count = 0
        for corr_res, comp_res in zip(m.postcond_corr, m.mutant_kill):
            if _is_complete_under_subset(corr_res, comp_res, m.ref_mutant_kill, selected):
                comp_count += 1

        # Comp@1 at method level: pass@1 with n=generate_num, c=comp_count
        pass1_list.append(calculate_pass_1(generate_num, comp_count))

    return {
        "method_count": float(len(methods)),
        "avg_sampled_mutants": float(np.mean(sampled_sizes)),
        "comp_1": float(np.mean(pass1_list)),
    }


# ========== experiment driver ==========
@dataclass
class SliceConfig:
    language: str
    prompting: str


def filter_methods(methods: List[Method], model_name: str, lang: str, prompting: str) -> List[Method]:
    out = []
    for m in methods:
        if m.model_name != model_name:
            continue
        if m.repo.language != lang:
            continue
        if m.prompting != prompting:
            continue
        out.append(m)
    return out


def run_one_frac(
    all_methods: List[Method],
    model_name: str,
    frac: float,
    repeats: int,
    base_seed: int,
) -> Dict:
    slices = [SliceConfig(l, p) for l, p in product(LANGUAGES, PROMPTINGS)]
    slice_results = {}

    # overall weighted by #methods across slices
    overall_vals = []
    overall_weights = []
    overall_stds = []  # for completeness; not used in weighted std

    for sl in slices:
        ms = filter_methods(all_methods, model_name, sl.language, sl.prompting)
        if len(ms) == 0:
            continue

        reps = []
        for r in range(repeats):
            seed = (
                base_seed
                + 100000 * int(frac * 100)
                + 1000 * r
                + (hash((sl.language, sl.prompting)) % 9973)
            )
            rng = random.Random(seed)
            reps.append(comp_at_1_for_methods_with_sampling(ms, frac, rng))

        comp1s = [d["comp_1"] for d in reps]
        avg_muts = [d["avg_sampled_mutants"] for d in reps]

        comp1_mean = float(np.mean(comp1s))
        comp1_std = float(np.std(comp1s, ddof=0))
        avg_mut_mean = float(np.mean(avg_muts))
        avg_mut_std = float(np.std(avg_muts, ddof=0))

        method_count = int(reps[0]["method_count"])

        slice_key = f"{sl.language}__{sl.prompting}"
        slice_results[slice_key] = {
            "method_count": method_count,
            "avg_sampled_mutants_mean": avg_mut_mean,
            "avg_sampled_mutants_std": avg_mut_std,
            "comp_1_mean": comp1_mean,
            "comp_1_std": comp1_std,
        }

        overall_vals.append(comp1_mean)
        overall_weights.append(method_count)
        overall_stds.append(comp1_std)

    if len(overall_weights) > 0:
        w = np.array(overall_weights, dtype=float)
        overall_comp1_weighted = float(np.average(overall_vals, weights=w))

        # 这里给一个“可解释”的 overall std：简单把各 slice 的 std 做方法数加权平均
        # （严格的 overall std 需要把每次repeat的整体加权值也算出来；你如果想要那个，我也能给你改）
        overall_comp1_std_weighted = float(np.average(overall_stds, weights=w))

        overall = {
            "comp_1_weighted_mean": overall_comp1_weighted,
            "comp_1_weighted_std": overall_comp1_std_weighted,
            "total_methods": int(np.sum(w)),
        }
    else:
        overall = None

    return {
        "model_name": model_name,
        "frac": frac,
        "repeats": repeats,
        "overall": overall,
        "slices": slice_results,
    }


def main():
    STEP_DIR = "data/step"
    # MODEL = "gpt-5"
    # MODEL = "claude-sonnet-4-5"
    # MODEL = "llama-4-maverick"
    # MODEL = "Qwen3-32B"
    MODEL = "gemma-3-27b"
    FRACS = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
    REPEATS = 50                    # 想要一次就设 1
    BASE_SEED = 20260217

    out_path = "data/comp_sampling_comp1.json"

    all_methods = load_all_methods_for_model(STEP_DIR, MODEL)
    print(f"[load] model={MODEL}, methods={len(all_methods)}")

    args = [(all_methods, MODEL, frac, REPEATS, BASE_SEED) for frac in FRACS]
    with Pool(processes=min(len(FRACS), 5)) as pool:
        results = pool.starmap(run_one_frac, args)

    results.sort(key=lambda d: d["frac"])

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print("\n=== Overall (weighted by #methods across slices) ===")
    for r in results:
        ov = r["overall"]
        if ov is None:
            continue
        print(
            f"frac={r['frac']:.1f}  "
            f"Comp@1={ov['comp_1_weighted_mean']:.4f} ± {ov['comp_1_weighted_std']:.4f}  "
            f"(methods={ov['total_methods']})"
        )

    print(f"\n[done] wrote {out_path}")


if __name__ == "__main__":
    main()
