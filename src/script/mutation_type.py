import os, json, math, random
import numpy as np
from typing import List, Dict, Tuple, Optional, Set
from itertools import combinations
from multiprocessing import Pool

from src.mutation.mutmut import generate_mutants_for_method as python_mut
from src.mutation.pit import generate_mutants_for_method as java_mut
from src.ds import Method

KFS = ["jml_fail", "icontract_fail"]


# ===================== IO =====================
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
                # keep mutants + mutant_tags
                m.cover_tests = None
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


# ===================== core metrics =====================
def calculate_pass_1(n: int, c: int) -> float:
    return 0.0 if n <= 0 else c / n


def _is_complete_under_subset(
    corr_res: str,
    comp_res: List[str],
    ref_mutant_kill: List[str],
    selected_mutant_indices: List[int],
) -> bool:
    # IMPORTANT: empty selected set is vacuously complete (if corr passed)
    if corr_res != "passed":
        return False
    if len(selected_mutant_indices) == 0:
        return True
    if len(comp_res) == 0:
        return False
    assert len(comp_res) == len(ref_mutant_kill), (len(comp_res), len(ref_mutant_kill))

    for i in selected_mutant_indices:
        r_f = ref_mutant_kill[i]
        f = comp_res[i]
        if r_f in KFS and f not in KFS:
            return False
    return True


# ===================== mutant helpers =====================
def tags_set(tags: List[str]) -> Set[str]:
    return set(tags)


def is_rule_only(tags: List[str]) -> bool:
    s = tags_set(tags)
    return ("rule" in s) and ("llm" not in s)


def is_llm_only(tags: List[str]) -> bool:
    s = tags_set(tags)
    return ("llm" in s) and ("rule" not in s)


def get_eval_mutants_and_tags(m: Method) -> Optional[Tuple[List[str], List[List[str]]]]:
    if not hasattr(m, "mutants") or not hasattr(m, "mutant_tags"):
        return None
    muts = getattr(m, "mutants")
    tags = getattr(m, "mutant_tags")
    if not isinstance(muts, list) or not (len(muts) == 0 or isinstance(muts[0], str)):
        return None
    if not isinstance(tags, list) or not (len(tags) == 0 or isinstance(tags[0], list)):
        return None
    if len(muts) != len(tags):
        return None
    return muts, tags


def method_key(m: Method) -> str:
    return getattr(m, "id", None) or f"{m.repo.github_path}::{m.file}::{m.start_line}-{m.end_line}"


def norm_code(s: str) -> str:
    return "\n".join(line.rstrip() for line in s.strip().splitlines())


# ===================== rule mutator name inference (string match) =====================
def gen_rule_mutator_map_for_method(m: Method) -> Dict[str, str]:
    src = m.content
    if m.repo.language == "python":
        muts, names = python_mut(src, w_mut_name=True)
    elif m.repo.language == "java":
        muts, names = java_mut(src, w_mut_name=True)
    else:
        return {}

    mp: Dict[str, str] = {}
    for s, nm in zip(muts, names):
        k = norm_code(s)
        if k not in mp:
            mp[k] = nm
    return mp


def infer_rule_mutator_types_for_eval(
    m: Method,
    eval_mutants: List[str],
    eval_tags: List[List[str]],
    rule_map: Dict[str, str],
) -> List[Optional[str]]:
    out: List[Optional[str]] = []
    for s, tags in zip(eval_mutants, eval_tags):
        if is_rule_only(tags):
            nm = rule_map.get(norm_code(s))
            out.append(nm if nm is not None else "other_rule")
        else:
            out.append(None)
    return out


# ===================== selection policies =====================
def selected_indices_baseline(total_muts: int) -> List[int]:
    return list(range(total_muts))


def selected_indices_exclude_rule_operator_set(
    rule_types: List[Optional[str]],
    excluded_ops: Set[str],
) -> Tuple[List[int], int]:
    excluded_idx = [i for i, t in enumerate(rule_types) if (t is not None and t in excluded_ops)]
    excluded_set = set(excluded_idx)
    selected = [i for i in range(len(rule_types)) if i not in excluded_set]
    return selected, len(excluded_idx)


def selected_indices_exclude_half_llm_keep_rule(
    eval_tags: List[List[str]],
    rng: random.Random,
) -> Tuple[List[int], int, int]:
    llm_only_candidates = [i for i, tags in enumerate(eval_tags) if is_llm_only(tags)]
    candidate_count = len(llm_only_candidates)
    if candidate_count == 0:
        return list(range(len(eval_tags))), 0, 0

    k = candidate_count // 2
    remove_idx = set(rng.sample(llm_only_candidates, k=k))
    selected = [i for i in range(len(eval_tags)) if i not in remove_idx]
    return selected, len(remove_idx), candidate_count


def selected_indices_exclude_all_rule_only(eval_tags: List[List[str]]) -> Tuple[List[int], int]:
    remove_idx = {i for i, tags in enumerate(eval_tags) if is_rule_only(tags)}
    selected = [i for i in range(len(eval_tags)) if i not in remove_idx]
    return selected, len(remove_idx)


def selected_indices_exclude_all_llm_only(eval_tags: List[List[str]]) -> Tuple[List[int], int]:
    remove_idx = {i for i, tags in enumerate(eval_tags) if is_llm_only(tags)}
    selected = [i for i in range(len(eval_tags)) if i not in remove_idx]
    return selected, len(remove_idx)


# ===================== compute Comp@1 under a selection rule =====================
def comp_at_1_with_selector(
    methods: List[Method],
    selector_fn,
) -> Dict[str, float]:
    assert methods
    generate_num = methods[0].generate_num
    assert all(m.generate_num == generate_num for m in methods)
    assert generate_num in (1, 5)

    pass1_list = []
    total_muts_list = []
    removed_list = []

    for m in methods:
        total_muts = len(m.ref_mutant_kill) if m.ref_mutant_kill is not None else 0
        total_muts_list.append(total_muts)

        if total_muts <= 0:
            pass1_list.append(0.0)
            removed_list.append(0)
            continue

        selected, removed, _meta = selector_fn(m, total_muts)

        comp_count = 0
        for corr_res, comp_res in zip(m.postcond_corr, m.mutant_kill):
            if _is_complete_under_subset(corr_res, comp_res, m.ref_mutant_kill, selected):
                comp_count += 1

        pass1_list.append(calculate_pass_1(generate_num, comp_count))
        removed_list.append(removed)

    return {
        "method_count": float(len(methods)),
        "avg_total_mutants": float(np.mean(total_muts_list)) if total_muts_list else 0.0,
        "avg_removed_mutants": float(np.mean(removed_list)) if removed_list else 0.0,
        "comp_1": float(np.mean(pass1_list)) if pass1_list else 0.0,
    }


# ===================== combined experiment =====================
def run_combined_experiments(all_methods: List[Method], model_name: str) -> Dict:
    ms = [m for m in all_methods if m.model_name == model_name and m.repo.language in ("python", "java")]
    if not ms:
        return {"model_name": model_name, "baseline": None}

    rule_map_cache: Dict[str, Dict[str, str]] = {}
    rule_types_cache: Dict[str, Optional[List[Optional[str]]]] = {}

    def get_rule_types(m: Method, total_muts: int) -> Optional[List[Optional[str]]]:
        key = method_key(m)
        cached = rule_types_cache.get(key)
        if cached is not None or key in rule_types_cache:
            return cached

        mt = get_eval_mutants_and_tags(m)
        if mt is None:
            rule_types_cache[key] = None
            return None
        eval_muts, eval_tags = mt
        if len(eval_muts) != total_muts:
            rule_types_cache[key] = None
            return None

        rmap = rule_map_cache.get(key)
        if rmap is None:
            rmap = gen_rule_mutator_map_for_method(m)
            rule_map_cache[key] = rmap

        rule_types = infer_rule_mutator_types_for_eval(m, eval_muts, eval_tags, rmap)
        if len(rule_types) != total_muts:
            rule_types_cache[key] = None
            return None

        rule_types_cache[key] = rule_types
        return rule_types

    # ---------- (1) baseline (combined) ----------
    def baseline_selector(m: Method, total_muts: int):
        return selected_indices_baseline(total_muts), 0, {}

    baseline = comp_at_1_with_selector(ms, baseline_selector)
    baseline_comp = baseline["comp_1"]

    # ---------- collect rule-only operator universe per language ----------
    py_ops: Set[str] = set()
    ja_ops: Set[str] = set()
    for m in ms:
        total_muts = len(m.ref_mutant_kill) if m.ref_mutant_kill is not None else 0
        if total_muts <= 0:
            continue
        rule_types = get_rule_types(m, total_muts)
        if rule_types is None:
            continue
        for t in rule_types:
            if t is None:
                continue
            if m.repo.language == "python":
                py_ops.add(t)
            else:
                ja_ops.add(t)

    py_ops_sorted = sorted(py_ops)
    ja_ops_sorted = sorted(ja_ops)

    # ---------- (3) exclude 5+5 rule-ops, RANDOM SAMPLE 50 combos ----------
    SAMPLES_5OPS = 50
    BASE_SEED_5OPS = 20260217 + 12345

    five_op_stats = None
    five_op_samples = []  # store sampled operator sets for reproducibility/debug
    if len(py_ops_sorted) >= 5 and len(ja_ops_sorted) >= 5:
        rng = random.Random(BASE_SEED_5OPS)

        comp_vals = []
        removed_vals = []

        # sample 50 distinct combos if possible
        seen = set()
        max_tries = 2000

        def sample_one_5set(ops: List[str]) -> Tuple[str, ...]:
            return tuple(sorted(rng.sample(ops, k=5)))

        tries = 0
        while len(five_op_samples) < SAMPLES_5OPS and tries < max_tries:
            tries += 1
            py_set = sample_one_5set(py_ops_sorted)
            ja_set = sample_one_5set(ja_ops_sorted)
            key = (py_set, ja_set)
            if key in seen:
                continue
            seen.add(key)
            five_op_samples.append({"py": list(py_set), "java": list(ja_set)})

        def make_selector_pair(ex_py: Set[str], ex_ja: Set[str]):
            def _sel(m: Method, total_muts: int):
                rule_types = get_rule_types(m, total_muts)
                if rule_types is None:
                    return selected_indices_baseline(total_muts), 0, {"note": "no_rule_types"}
                if m.repo.language == "python":
                    selected, removed = selected_indices_exclude_rule_operator_set(rule_types, ex_py)
                else:
                    selected, removed = selected_indices_exclude_rule_operator_set(rule_types, ex_ja)
                return selected, removed, {}
            return _sel

        for s in five_op_samples:
            ex_py = set(s["py"])
            ex_ja = set(s["java"])
            rr = comp_at_1_with_selector(ms, make_selector_pair(ex_py, ex_ja))
            comp_vals.append(rr["comp_1"])
            removed_vals.append(rr["avg_removed_mutants"])

        five_op_stats = {
            "py_ops_total": int(len(py_ops_sorted)),
            "ja_ops_total": int(len(ja_ops_sorted)),
            "samples": int(len(five_op_samples)),
            "seed": int(BASE_SEED_5OPS),
            "comp_1_mean": float(np.mean(comp_vals)) if comp_vals else 0.0,
            "comp_1_std": float(np.std(comp_vals, ddof=0)) if comp_vals else 0.0,
            "avg_removed_mutants_mean": float(np.mean(removed_vals)) if removed_vals else 0.0,
            "avg_removed_mutants_std": float(np.std(removed_vals, ddof=0)) if removed_vals else 0.0,
            "diff_mean_from_baseline": float((float(np.mean(comp_vals)) if comp_vals else 0.0) - baseline_comp),
            "distinct_samples": int(len(seen)),
        }
    else:
        five_op_stats = {
            "py_ops_total": int(len(py_ops_sorted)),
            "ja_ops_total": int(len(ja_ops_sorted)),
            "samples": 0,
            "seed": int(BASE_SEED_5OPS),
            "comp_1_mean": None,
            "comp_1_std": None,
            "avg_removed_mutants_mean": None,
            "avg_removed_mutants_std": None,
            "diff_mean_from_baseline": None,
            "distinct_samples": 0,
        }

    # ---------- (4) exclude HALF LLM-only mutants (50 runs), combined ----------
    REPEATS = 50
    BASE_SEED = 20260217

    comp_vals = []
    removed_vals = []
    for r in range(REPEATS):
        rng = random.Random(BASE_SEED + r)

        def make_llm_half_selector(rng_local: random.Random):
            def _sel(m: Method, total_muts: int):
                mt = get_eval_mutants_and_tags(m)
                if mt is None:
                    return selected_indices_baseline(total_muts), 0, {"note": "no_tags"}
                _muts, tags = mt
                if len(tags) != total_muts:
                    return selected_indices_baseline(total_muts), 0, {"note": "len_mismatch"}
                selected, removed, _cand = selected_indices_exclude_half_llm_keep_rule(tags, rng_local)
                return selected, removed, {}
            return _sel

        rr = comp_at_1_with_selector(ms, make_llm_half_selector(rng))
        comp_vals.append(rr["comp_1"])
        removed_vals.append(rr["avg_removed_mutants"])

    llm_half_stats = {
        "repeats": REPEATS,
        "seed_base": int(BASE_SEED),
        "comp_1_mean": float(np.mean(comp_vals)) if comp_vals else 0.0,
        "comp_1_std": float(np.std(comp_vals, ddof=0)) if comp_vals else 0.0,
        "avg_removed_mutants_mean": float(np.mean(removed_vals)) if removed_vals else 0.0,
        "avg_removed_mutants_std": float(np.std(removed_vals, ddof=0)) if removed_vals else 0.0,
        "diff_mean_from_baseline": float((float(np.mean(comp_vals)) if comp_vals else 0.0) - baseline_comp),
    }

    # ---------- (5) exclude ALL rule-only OR ALL llm-only (both always kept), combined ----------
    def exclude_all_rule_only_selector(m: Method, total_muts: int):
        mt = get_eval_mutants_and_tags(m)
        if mt is None:
            return selected_indices_baseline(total_muts), 0, {"note": "no_tags"}
        _muts, tags = mt
        if len(tags) != total_muts:
            return selected_indices_baseline(total_muts), 0, {"note": "len_mismatch"}
        selected, removed = selected_indices_exclude_all_rule_only(tags)
        return selected, removed, {}

    def exclude_all_llm_only_selector(m: Method, total_muts: int):
        mt = get_eval_mutants_and_tags(m)
        if mt is None:
            return selected_indices_baseline(total_muts), 0, {"note": "no_tags"}
        _muts, tags = mt
        if len(tags) != total_muts:
            return selected_indices_baseline(total_muts), 0, {"note": "len_mismatch"}
        selected, removed = selected_indices_exclude_all_llm_only(tags)
        return selected, removed, {}

    excl_all_rule_only = comp_at_1_with_selector(ms, exclude_all_rule_only_selector)
    excl_all_llm_only = comp_at_1_with_selector(ms, exclude_all_llm_only_selector)

    excl_all_stats = {
        "exclude_all_rule_only": {
            **excl_all_rule_only,
            "diff_from_baseline": float(excl_all_rule_only["comp_1"] - baseline_comp),
        },
        "exclude_all_llm_only": {
            **excl_all_llm_only,
            "diff_from_baseline": float(excl_all_llm_only["comp_1"] - baseline_comp),
        },
    }

    return {
        "model_name": model_name,
        "baseline": baseline,  # (1) combined
        "py_rule_ops": py_ops_sorted,
        "ja_rule_ops": ja_ops_sorted,
        "exclude_five_ops_py_and_ja_sampled": five_op_stats,   # (3) sampled
        "exclude_five_ops_samples": five_op_samples,           # sampled operator sets
        "exclude_half_llm_keep_rule": llm_half_stats,          # (4) combined
        "exclude_all_rule_or_llm_only": excl_all_stats,        # (5) combined
    }


# ===================== main =====================
def main():
    STEP_DIR = "data/step"
    # MODEL = "gpt-5"
    # MODEL = "claude-sonnet-4-5"
    # MODEL = "llama-4-maverick"
    # MODEL = "Qwen3-32B"
    MODEL = "gemma-3-27b"
    out_path = "data/ablation_combined_sampled_5ops.json"

    all_methods = load_all_methods_for_model(STEP_DIR, MODEL)
    print(f"[load] model={MODEL}, methods={len(all_methods)}")

    result = run_combined_experiments(all_methods, MODEL)

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    b = result["baseline"]
    if b is None:
        print("[baseline] none")
        return

    print("\n=== COMBINED (PY+JAVA) ===")
    print(f"(1) baseline Comp@1 = {b['comp_1']:.4f}  (avg_total_mutants={b['avg_total_mutants']:.2f})")

    five = result["exclude_five_ops_py_and_ja_sampled"]
    print("\n(3) exclude FIVE rule-ops in python + FIVE rule-ops in java (RANDOM 50 samples):")
    if five["samples"] == 0:
        print("  not enough operators to sample 5-sets in both languages")
    else:
        print(
            f"  py_ops_total={five['py_ops_total']}  ja_ops_total={five['ja_ops_total']}  "
            f"samples={five['samples']}  seed={five['seed']}  distinct={five['distinct_samples']}\n"
            f"  Comp@1 mean={five['comp_1_mean']:.4f}  std={five['comp_1_std']:.4f}  "
            f"Δ_mean={five['diff_mean_from_baseline']:+.4f}\n"
            f"  removed(avg) mean={five['avg_removed_mutants_mean']:.2f}  std={five['avg_removed_mutants_std']:.2f}"
        )

    llm = result["exclude_half_llm_keep_rule"]
    print("\n(4) exclude HALF LLM-only mutants (50 runs, rule-tag protected), combined:")
    print(
        f"  Comp@1 mean={llm['comp_1_mean']:.4f}  std={llm['comp_1_std']:.4f}  "
        f"Δ_mean={llm['diff_mean_from_baseline']:+.4f}\n"
        f"  removed(avg) mean={llm['avg_removed_mutants_mean']:.2f}  std={llm['avg_removed_mutants_std']:.2f}"
    )

    ex = result["exclude_all_rule_or_llm_only"]
    r_only = ex["exclude_all_rule_only"]
    l_only = ex["exclude_all_llm_only"]
    print("\n(5) exclude ALL rule-only vs ALL llm-only (both-tag never removed), combined:")
    print(
        f"  -all rule-only: Comp@1={r_only['comp_1']:.4f}  Δ={r_only['diff_from_baseline']:+.4f}  "
        f"removed(avg)={r_only['avg_removed_mutants']:.2f}"
    )
    print(
        f"  -all llm-only : Comp@1={l_only['comp_1']:.4f}  Δ={l_only['diff_from_baseline']:+.4f}  "
        f"removed(avg)={l_only['avg_removed_mutants']:.2f}"
    )

    print(f"\n[done] wrote {out_path}")


if __name__ == "__main__":
    main()
