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


KFS = ["jml_fail", "icontract_fail"]
KS = [1, 3, 5]
LANGUAGES = ["python", "java"]

with open("data/step/0.append/dep_anno_python.txt") as file:
    dep_anno_python: Dict[str, str] = {l.split("\t")[0]: l.strip().split("\t")[1] for l in file}
with open("data/step/0.append/dep_anno_java.txt") as file:
    dep_anno_java: Dict[str, int] = {l.split("\t")[0]: l.strip().split("\t")[1] for l in file}

DEP_ANNO = {**dep_anno_python, **dep_anno_java}

ORDERED_MODELS = [
    "gpt-5",
    "gpt-4.1", 
    "gpt-4o-mini", 
    "claude-sonnet-4-5", 
    "claude-sonnet-4", 
    "claude-3-5-haiku",
    "Qwen3-32B", 
    "Qwen3-8B",
    "phi-4", 
    "phi-4-mini",
    "deepseek-coder-v2",
]

MODEL_NAME_MAP = {
    "gpt-5": "gpt-5", 
    "gpt-4.1": "gpt-4.1", 
    "gpt-4o-mini": "gpt-4o-mini", 
    "claude-sonnet-4": "Claude 4", 
    "claude-3-5-haiku": "Claude 3.5", 
    "claude-sonnet-4-5": "Claude 4.5", 
    "Qwen3-32B": "Qwen3-32B", 
    "Qwen3-8B": "Qwen3-8B",
    "phi-4": "phi-4", 
    "phi-4-mini": "phi-4-mini",
    "deepseek-coder-v2": "DS Coder",
}

@dataclass
class ExpRes:
    model_name: str
    language: str
    w_code: bool
    prompting: str
    method_range: str

    method_count: int
    postcond_count: int
    
    corr_1: float
    corr_3: float
    corr_5: float
    comp_1: float
    comp_3: float
    comp_5: float

    vacu_r: float

    rule_precision: float
    llm_precision: float

def new_exp_res(
        model_name: str, 
        language: str, 
        w_code: bool, 
        prompting: str, 
        method_range: str) -> ExpRes:
    return ExpRes(
        model_name=model_name,
        language=language,
        w_code=w_code,
        prompting=prompting,
        method_range=method_range,
        method_count=None, postcond_count=None,
        corr_1=None, corr_3=None, corr_5=None,
        comp_1=None, comp_3=None, comp_5=None,
        vacu_r=None,
        rule_precision=None, llm_precision=None)

def calculate_pass_k(n, c, k) -> float:
    if n < k:
        return 0.0
    numerator = math.comb(n - c, k)   # C(n-c, k)
    denominator = math.comb(n, k)     # C(n, k)
    return 1 - numerator / denominator

def set_metrics(res: ExpRes, 
                corr_and_comps: List[float],
                vacu_r: float,
                rule_precision,
                llm_precision):
    assert isinstance(corr_and_comps, list)
    assert len(corr_and_comps) == 6
    res.corr_1 = corr_and_comps[0]
    res.corr_3 = corr_and_comps[1]
    res.corr_5 = corr_and_comps[2]
    res.comp_1 = corr_and_comps[3]
    res.comp_3 = corr_and_comps[4]
    res.comp_5 = corr_and_comps[5]
    res.vacu_r = vacu_r
    res.rule_precision = rule_precision
    res.llm_precision = llm_precision

def set_metrics_none(res: ExpRes):
    set_metrics(res, [None, None, None, None, None, None], None, None, None)

def dump_exp_results(results: List[ExpRes], jsonl_path: str, csv_path: str) -> None:
    dict_rows = [asdict(r) for r in results]

    with open(jsonl_path, "w", encoding="utf-8") as f_jsonl:
        for row in dict_rows:
            f_jsonl.write(json.dumps(row, ensure_ascii=False) + "\n")

    fieldnames = [f.name for f in fields(ExpRes)]
    with open(csv_path, "w", encoding="utf-8", newline="") as f_csv:
        writer = csv.DictWriter(f_csv, fieldnames=fieldnames)
        writer.writeheader()
        for row in dict_rows:
            writer.writerow(row)

def check_method(method: Method, config: ExpRes) -> bool:
    if method.model_name != config.model_name:
        return False
    if method.repo.language != config.language:
        return False
    if method.w_code != config.w_code:
        return False
    if (method.prompting is None) != (config.prompting is None):
        return False
    if method.prompting is not None and method.prompting != config.prompting:
        return False
    if config.method_range is not None:
        method_range_title = config.method_range.split("__")[0]
        if method_range_title == "dep":
            w_dep = config.method_range.split("__")[1]
            if w_dep != DEP_ANNO.get(method.github_url, None):
                return False
        elif method_range_title in ("line", "cc"):
            range_str = config.method_range.split("__")[1]
            range_l, range_r = range_str.split("_")
            range_l = int(range_l)
            range_r = float("inf") if range_r == "inf" else int(range_r)
            if method_range_title == "line":
                if not (range_l <= method.lines < range_r):
                    return False
            elif method_range_title == "cc":
                if not (range_l <= method.cc < range_r):
                    return False
    return True

def get_mutator_precision(methods: List[Method]):
    tags = ["rule", "llm"]
    res_list = []
    exist_list = {t: [] for t in tags}
    for method in methods:
        for corr_res, comp_res in zip(method.postcond_corr, method.mutant_kill):
            res_list.append((
                corr_res, comp_res, method.mutant_tags, method.ref_mutant_kill))
        
        method_mut_tags = set()
        for __tags in method.mutant_tags:
            for __tag in __tags:
                method_mut_tags.add(__tag)
        for tag in tags:
            exist_list[tag].append(1 if tag in method_mut_tags else 0)

    precision_list = {t: [] for t in tags}
    for corr_res, comp_res, mutant_tags, ref_mutant_kill in res_list:
        if corr_res == "passed":
            assert len(comp_res) == 0 or len(comp_res) == len(ref_mutant_kill)
            comp_res_bool = all([r_f not in KFS or f in KFS 
                                 for f, r_f in zip(comp_res, ref_mutant_kill)])
            for tag in tags:
                tag_comp_res = [
                    (f, r_f) 
                    for f, mutant_tag, r_f in zip(comp_res, mutant_tags, ref_mutant_kill) 
                    if tag in mutant_tag]
                if len(tag_comp_res) == 0:
                    continue
                tag_comp_res_bool = all([
                    r_f not in KFS or f in KFS for f, r_f in tag_comp_res])
                if tag_comp_res_bool:
                    precision_list[tag].append(1 if comp_res_bool else 0)
            pass
    return {t: sum(l) / len(l) if len(l) > 0 else None for t, l in precision_list.items()}, \
           {t: sum(l) / len(l) if len(l) > 0 else None for t, l in exist_list.items()}


def cal_metrics(methods: List[Method], res: ExpRes) -> ExpRes:
    for method in methods:
        assert method.generate_num == len(method.postcond_corr)
        assert len(method.postcond_corr) == len(method.mutant_kill)

    if len(methods) == 0:
        set_metrics_none(res)
        return res

    assert len(set([m.generate_num for m in methods])) == 1
    generate_num = methods[0].generate_num
    assert generate_num in (1, 5)

    res.method_count = len(methods)
    res.postcond_count = len(methods) * generate_num

    pass_k = {n: {i: [] for i in KS} for n in ["corr", "comp"]}
    tot_corr_count = 0
    tot_vacu_count = 0
    for method in methods:
        corr_count, comp_count, vacu_count = 0, 0, 0
        for corr_res, comp_res in zip(method.postcond_corr, method.mutant_kill):
            if corr_res == "passed":
                corr_count += 1
                assert len(comp_res) == 0 or len(comp_res) == len(method.ref_mutant_kill)
                if all(r_f not in KFS or f in KFS 
                       for f, r_f in zip(comp_res, method.ref_mutant_kill)):
                    comp_count += 1
                if all(f not in KFS for f in comp_res):
                    vacu_count += 1
        for k in KS:
            pass_k["corr"][k].append(
                calculate_pass_k(generate_num, corr_count, k))
            pass_k["comp"][k].append(
                calculate_pass_k(generate_num, comp_count, k))
        tot_corr_count += corr_count
        tot_vacu_count += vacu_count

    corr_and_comps = [np.mean(pass_k["corr"][k]).item() for k in KS]
    corr_and_comps.extend(np.mean(pass_k["comp"][k]).item() for k in KS)

    vacu_rate = None
    if tot_corr_count > 0:
        vacu_rate = tot_vacu_count / tot_corr_count

    mutator_precision, _ = get_mutator_precision(methods)
    p_rule = mutator_precision["rule"]
    p_llm = mutator_precision["llm"]

    set_metrics(res, corr_and_comps, vacu_rate, p_rule, p_llm)

    return res


def get_exp_res_list(model_name: str) -> List[ExpRes]:
    """
    现在专门处理一个 model_name，方便给进程池用。
    """
    step_dir = "data/step"

    promptings = [None, "no_gram", "fsl_1", "fsl_3", "fsl_5", "fsl_10"]
    method_ranges = ["dep__0", "dep__1", 
                     "line__00_20", 
                     "line__20_40", 
                     "line__40_inf",
                     "cc__00_05", 
                     "cc__05_10", 
                     "cc__10_inf"]

    __config_iter = product(
        [model_name], LANGUAGES, 
        [True, False], promptings)

    exp_res_list: List[ExpRes] = []
    for mn, lang, w_code, prompting in __config_iter:
        exp_res = new_exp_res(
            model_name=mn,
            language=lang,
            w_code=w_code,
            prompting=prompting,
            method_range=None)
        exp_res_list.append(exp_res)
        if prompting is None:
            for method_range in method_ranges:
                exp_res_w_range = deepcopy(exp_res)
                exp_res_w_range.method_range = method_range
                exp_res_list.append(exp_res_w_range)

    all_methods: List[Method] = []

    # 只加载当前 model_name 相关的文件夹
    for folder_name in os.listdir(step_dir):
        if not folder_name.startswith("9."):
            continue
        if folder_name.startswith(f"9.{model_name}"):
            all_methods.extend(read_benchmark(
                f"{step_dir}/{folder_name}", save_mem=True))

    print(f"{model_name} file read finished.")

    # 对当前 model_name 的所有配置计算指标
    for idx, exp_res in enumerate(exp_res_list):
        methods = [m for m in all_methods if check_method(m, exp_res)]
        exp_res = cal_metrics(methods, exp_res)
        exp_res_list[idx] = exp_res
    
    print(f"{model_name} finished.")

    return exp_res_list


def get_exp_res():
    output_dir = "data"
    all_model_names = [
        "gpt-5", 
        "gpt-4.1", 
        "gpt-4o-mini", 
        "claude-sonnet-4-5",
        "claude-sonnet-4", 
        "claude-3-5-haiku", 
        "Qwen3-32B", 
        "Qwen3-8B",
        # "gemma-3-27b", 
        # "gemma-3-4b",
        "phi-4", 
        "phi-4-mini",
        # "deepseek-coder-v2",
        # "Llama-3.1-70B",
        # "Llama-3.1-8B",
    ]

    processes = 3
    with Pool(processes=processes) as pool:
        # 每个进程跑一个 model_name，返回 List[ExpRes]
        per_model_results = pool.map(get_exp_res_list, all_model_names)

    # 展平结果
    exp_res_list: List[ExpRes] = [
        res for sublist in per_model_results for res in sublist
    ]

    dump_exp_results(
        exp_res_list, 
        f"{output_dir}/res.jsonl", 
        f"{output_dir}/res.csv")


def _f2s(num: float):
    return f"{num:.3f}"

def _bold(str: str):
    return f"\\textbf{{{str}}}"

def analyze_dep():
    exp_res_list: List[ExpRes] = []
    with open("data/res.jsonl") as file:
        for line in file:
            exp_res_list.append(ExpRes(**json.loads(line)))
    exp_res_list = [
        r for r in exp_res_list 
        if (r.method_range is None or "dep__" in r.method_range) \
            and r.prompting is None]
    model_names = list(set([r.model_name for r in exp_res_list]))
    model_names = [m for m in ORDERED_MODELS if m in model_names]

    @dataclass
    class _number:
        model_name: str
        language: str
        w_code: bool
        metric: str
        is_dep: bool
        number: float
        should_bold: bool

    numbers: List[_number] = []

    def _find(numbers: List[_number], 
              model_name, language, w_code, metric, is_dep) -> _number:
        for number in numbers:
            if model_name != number.model_name:
                continue
            if language != number.language:
                continue
            if w_code != number.w_code:
                continue
            if metric != number.metric:
                continue
            if is_dep != number.is_dep:
                continue
            return number
        return None

    __iter = product(LANGUAGES, [True, False], model_names)
    for lang, w_code, model_name in __iter:
        __exp_res_list = [
            r for r in exp_res_list if 
            model_name == r.model_name and lang == r.language \
                and w_code == r.w_code]
        assert len(__exp_res_list) == 3
        ori_res = [r for r in __exp_res_list if r.method_range is None][0]
        dep_res = [r for r in __exp_res_list if r.method_range == "dep__1"][0]
        stn_res = [r for r in __exp_res_list if r.method_range == "dep__0"][0]
        # if ori_res.corr_1 < 0.01:
        #     continue
        if ori_res.corr_1 > max(dep_res.corr_1, stn_res.corr_1) + 0.01 or \
                ori_res.corr_1 < min(dep_res.corr_1, stn_res.corr_1) - 0.01:
            print("WARN: corr ", lang, w_code, model_name, ori_res.corr_1)
        if ori_res.comp_1 > max(dep_res.comp_1, stn_res.comp_1) + 0.01 or \
                ori_res.comp_1 < min(dep_res.comp_1, stn_res.comp_1) - 0.01:
            print("WARN: comp ", lang, w_code, model_name, ori_res.comp_1)

        def should_bold(this_n, that_n):
            return this_n > that_n # and this_n >= 0.01

        numbers.append(
            _number(
                model_name=model_name, language=lang, w_code=w_code,
                metric="corr",
                is_dep=True,
                number=dep_res.corr_1,
                should_bold=should_bold(dep_res.corr_1, stn_res.corr_1)
            )
        )
        numbers.append(
            _number(
                model_name=model_name, language=lang, w_code=w_code,
                metric="corr",
                is_dep=False,
                number=stn_res.corr_1,
                should_bold=should_bold(stn_res.corr_1, dep_res.corr_1)
            )
        )
        numbers.append(
            _number(
                model_name=model_name, language=lang, w_code=w_code,
                metric="comp",
                is_dep=True,
                number=dep_res.comp_1,
                should_bold=should_bold(dep_res.comp_1, stn_res.comp_1)
            )
        )
        numbers.append(
            _number(
                model_name=model_name, language=lang, w_code=w_code,
                metric="comp",
                is_dep=False,
                number=stn_res.comp_1,
                should_bold=should_bold(stn_res.comp_1, dep_res.comp_1)
            )
        )

    w_code_map = {
        True: "C2P",
        False: "N2P",
    }

    width = 8
    merge_row = 2

    avg_list = [[] for _ in range(width)]
    __iter = product(model_names, [True, False])
    for row_idx, (model_name, w_code) in enumerate(__iter):
        number_str_list = []
        ___iter = product(LANGUAGES, ["corr", "comp"], [True, False])
        for col_idx, (lang, metric, is_dep) in enumerate(___iter):
            number = _find(numbers, model_name, lang, w_code, metric, is_dep)
            if number is None:
                continue
            avg_list[col_idx].append(number.number)
            number_str = _f2s(number.number)
            if number.should_bold:
                # number_str = f"\033[1m{number_str}\033[0m"
                # number_str = f"\033[7m{number_str}\033[0m"
                number_str = _bold(number_str)
            number_str_list.append(number_str)
        assert len(number_str_list) == width

        if row_idx % merge_row == 0:
            # if row_idx != 0:
            #     print("\\midrule")
            la_model_name = MODEL_NAME_MAP[model_name]
            la_model_name = f"\multirow{{2}}{{*}}{{{la_model_name}}}"
        else:
            la_model_name = ""

        print(f"{la_model_name} & {w_code_map[w_code]} & ", end="")
        print(" & ".join(number_str_list) + f" \\\\")

    avg_list = [np.mean(l).item() for l in avg_list]
    avg_str_list = []
    for idx, avg in enumerate(avg_list):
        that_idx = idx ^ 1
        that_avg = avg_list[that_idx]
        avg_str = _f2s(avg)
        if should_bold(avg, that_avg):
            avg_str = _bold(avg_str)
        avg_str_list.append(avg_str)
    print("\\midrule")
    print("\\multicolumn{2}{c|}{\\textbf{Avg}} & ", end="")
    print(" & ".join(avg_str_list) + "\\\\")

    w_code_map = {
        True: "C2P",
        False: "N2P",
    }

    # width = 8
    # merge_row = 8

    # avg_list = [[] for _ in range(width)]
    # __iter = product([True, False], model_names)
    # for row_idx, (w_code, model_name) in enumerate(__iter):
    #     number_str_list = []
    #     ___iter = product(LANGUAGES, ["corr", "comp"], [True, False])
    #     for col_idx, (lang, metric, is_dep) in enumerate(___iter):
    #         number = _find(numbers, model_name, lang, w_code, metric, is_dep)
    #         if number is None:
    #             continue
    #         avg_list[col_idx].append(number.number)
    #         number_str = f"{number.number:.4f}"
    #         if number.should_bold:
    #             # number_str = f"\033[1m{number_str}\033[0m"
    #             # number_str = f"\033[7m{number_str}\033[0m"
    #             number_str = f"\\textbf{{{number_str}}}"
    #         number_str_list.append(number_str)
    #     assert len(number_str_list) == width

    #     if row_idx % merge_row == 0:
    #         l_w_code = w_code_map[w_code]
    #         la_w_code = f"\multirow{{{merge_row}}}{{*}}{{{l_w_code}}}"
    #     else:
    #         la_w_code = ""

    #     print(f"{la_w_code} & {model_name} & ", end="")
    #     print(" & ".join(number_str_list) + f" \\\\")

    # avg_list = [np.mean(l).item() for l in avg_list]
    # avg_list = [f"{f:.4f}" for f in avg_list]
    # print(" & ".join(avg_list))


def analyze_no_gram():
    exp_res_list: List[ExpRes] = []
    with open("data/res.jsonl") as file:
        for line in file:
            exp_res_list.append(ExpRes(**json.loads(line)))
    exp_res_list = [
        r for r in exp_res_list 
        if r.method_range is None and \
            (r.prompting is None or r.prompting == "no_gram")]
    model_names = list(set([r.model_name for r in exp_res_list]))
    model_names = [m for m in ORDERED_MODELS if m in model_names]

    @dataclass
    class _number:
        model_name: str
        language: str
        w_code: bool
        metric: str
        w_gram: bool
        number: float
        should_bold: bool

    numbers: List[_number] = []

    def _find(numbers: List[_number], 
              model_name, language, w_code, metric, w_gram) -> _number:
        for number in numbers:
            if model_name != number.model_name:
                continue
            if language != number.language:
                continue
            if w_code != number.w_code:
                continue
            if metric != number.metric:
                continue
            if w_gram != number.w_gram:
                continue
            return number
        return None

    __iter = product(LANGUAGES, [True, False], model_names)
    for lang, w_code, model_name in __iter:
        __exp_res_list = [
            r for r in exp_res_list if 
            model_name == r.model_name and lang == r.language \
                and w_code == r.w_code]
        assert len(__exp_res_list) == 2
        ori_res = [r for r in __exp_res_list if r.prompting is None][0]
        no_gram_res = [r for r in __exp_res_list if r.prompting == "no_gram"][0]

        def should_bold(this_n, that_n):
            return this_n > that_n # and this_n >= 0.01

        numbers.append(
            _number(
                model_name=model_name, language=lang, w_code=w_code,
                metric="corr",
                w_gram=True,
                number=ori_res.corr_1,
                should_bold=should_bold(ori_res.corr_1, no_gram_res.corr_1)
            )
        )
        numbers.append(
            _number(
                model_name=model_name, language=lang, w_code=w_code,
                metric="corr",
                w_gram=False,
                number=no_gram_res.corr_1,
                should_bold=should_bold(no_gram_res.corr_1, ori_res.corr_1)
            )
        )
        numbers.append(
            _number(
                model_name=model_name, language=lang, w_code=w_code,
                metric="comp",
                w_gram=True,
                number=ori_res.comp_1,
                should_bold=should_bold(ori_res.comp_1, no_gram_res.comp_1)
            )
        )
        numbers.append(
            _number(
                model_name=model_name, language=lang, w_code=w_code,
                metric="comp",
                w_gram=False,
                number=no_gram_res.comp_1,
                should_bold=should_bold(no_gram_res.comp_1, ori_res.comp_1)
            )
        )

    w_code_map = {
        True: "C2P",
        False: "N2P",
    }

    width = 8
    merge_row = 2

    avg_list = [[] for _ in range(width)]
    __iter = product(model_names, [True, False])
    for row_idx, (model_name, w_code) in enumerate(__iter):
        number_str_list = []
        ___iter = product(LANGUAGES, ["corr", "comp"], [True, False])
        for col_idx, (lang, metric, w_gram) in enumerate(___iter):
            number = _find(numbers, model_name, lang, w_code, metric, w_gram)
            if number is None:
                continue
            avg_list[col_idx].append(number.number)
            number_str = _f2s(number.number)
            if number.should_bold:
                # number_str = f"\033[1m{number_str}\033[0m"
                # number_str = f"\033[7m{number_str}\033[0m"
                number_str = _bold(number_str)
            number_str_list.append(number_str)
        assert len(number_str_list) == width

        if row_idx % merge_row == 0:
            # if row_idx != 0:
            #     print("\\midrule")
            la_model_name = MODEL_NAME_MAP[model_name]
            la_model_name = f"\multirow{{2}}{{*}}{{{la_model_name}}}"
        else:
            la_model_name = ""

        print(f"{la_model_name} & {w_code_map[w_code]} & ", end="")
        print(" & ".join(number_str_list) + f" \\\\")

    avg_list = [np.mean(l).item() for l in avg_list]
    avg_str_list = []
    for idx, avg in enumerate(avg_list):
        that_idx = idx ^ 1
        that_avg = avg_list[that_idx]
        avg_str = _f2s(avg)
        if should_bold(avg, that_avg):
            avg_str = _bold(avg_str)
        avg_str_list.append(avg_str)
    print("\\midrule")
    print("\\multicolumn{2}{c|}{\\textbf{Avg}} & ", end="")
    print(" & ".join(avg_str_list) + "\\\\")

    w_code_map = {
        True: "C2P",
        False: "N2P",
    }



def main_res():
    exp_res_list: List[ExpRes] = []
    with open("data/res.jsonl") as file:
        for line in file:
            exp_res_list.append(ExpRes(**json.loads(line)))
    exp_res_list = [
        r for r in exp_res_list 
        if r.method_range is None and r.prompting is None]
    model_names = list(set([r.model_name for r in exp_res_list]))
    model_names = [m for m in ORDERED_MODELS if m in model_names]


    @dataclass
    class _number:
        model_name: str
        language: str
        w_code: bool
        metric: str
        number: float
        should_bold: bool

    numbers: List[_number] = []

    def _find(numbers: List[_number], 
              model_name, language, w_code, metric) -> _number:
        for number in numbers:
            if model_name != number.model_name:
                continue
            if language != number.language:
                continue
            if w_code != number.w_code:
                continue
            if metric != number.metric:
                continue
            return number
        return None

    metric_field_names = [
        f"{metric}_{k}" for metric, k in product(["corr", "comp"], [1, 5])]
    metric_field_names.append("vacu_r")
    
    __iter = product(LANGUAGES, [True, False])
    for lang, w_code in __iter:
        __exp_res_list = [
            r for r in exp_res_list if 
            lang == r.language and w_code == r.w_code]
        assert len(__exp_res_list) == len(model_names)
        for r in __exp_res_list:
            for field_name in metric_field_names:
                n = getattr(r, field_name)
                if field_name == "vacu_r":
                    should_bold = all(n <= getattr(rr, field_name) for rr in __exp_res_list)
                    should_bold = False
                else:
                    should_bold = all(n >= getattr(rr, field_name) for rr in __exp_res_list)
                numbers.append(_number(
                    model_name=r.model_name,
                    language=r.language,
                    w_code=r.w_code,
                    metric=field_name,
                    number=n,
                    should_bold=should_bold
                ))

    # =====

    # model_metrics = {model_name: [] for model_name in model_names}
    # for _n in numbers:
    #     if _n.metric != "vacu_r":
    #         model_metrics[_n.model_name].append(_n.number)
    # avgs = []
    # for mn, ms in model_metrics.items():
    #     avg = sum(ms) / len(ms)
    #     avgs.append((avg, mn, len(ms)))
    # avgs.sort()
    # for avg, mn, length in avgs:
    #     print(f"{avg:.3f} {mn} {length}")
    
    # =====

    # C2P_vs_N2P_map = {}
    # for _n in numbers:
    #     if _n.metric != "vacu_r":
    #         key = (_n.model_name, _n.language, _n.metric)
    #         if key not in C2P_vs_N2P_map:
    #             C2P_vs_N2P_map[key] = [None, None]
    #         C2P_vs_N2P_map[key][1 if _n.w_code else 0] = _n.number

    # count = [0, 0, 0]
    # for key, ns in C2P_vs_N2P_map.items():
    #     assert all(n is not None for n in ns)
    #     wo_code_n, w_code_n = ns
    #     if wo_code_n < w_code_n:
    #         count[0] += 1
    #     elif wo_code_n == w_code_n:
    #         count[1] += 1
    #     else:
    #         count[2] += 1
    # print(count)

    # =====

    # proprietary_map = {"prop": [], "os": []}
    # for _n in numbers:
    #     if _n.metric != "vacu_r":
    #         if "gpt" in _n.model_name.lower() or "claude" in _n.model_name.lower():
    #             proprietary_map["prop"].append(_n.number)
    #         else:
    #             proprietary_map["os"].append(_n.number)

    # for key, ns in proprietary_map.items():
    #     avg = sum(ns) / len(ns)
    #     print(f"{avg:.3f} {key} {len(ns)}")

    # =====

    # model_vacus = {model_name: [] for model_name in model_names}
    # for _n in numbers:
    #     if _n.metric == "vacu_r":
    #         model_vacus[_n.model_name].append(_n.number)
    # model_vacus = [(sum(ns) / len(ns), key, len(ns)) 
    #                for key, ns in model_vacus.items()]
    # model_vacus.sort()
    # for avg, key, length in model_vacus:
    #     print(f"{avg:.3f} {key} {length}")

    # =====

    width = 10

    for lang_idx, lang in enumerate(LANGUAGES):
        print("\\midrule")
        print(f"\\multicolumn{{{width+1}}}{{c}}{{{_bold(lang.capitalize())}}} \\\\")
        print("\\midrule")
        for row_idx, model_name in enumerate(model_names):
            number_str_list = []
            ___iter = product([True, False], metric_field_names)
            for col_idx, (w_code, field_name) in enumerate(___iter):
                number = _find(numbers, model_name, lang, w_code, field_name)
                number_str = _f2s(number.number)
                if number.should_bold:
                    number_str = _bold(number_str)
                number_str_list.append(number_str)
            assert len(number_str_list) == width

            la_model_name = MODEL_NAME_MAP[model_name]

            print(f"{la_model_name} & ", end="")
            print(" & ".join(number_str_list) + f" \\\\")


def code_line_line_chart():
    plt.rcParams['font.family'] = 'DejaVu Serif'   # 直接用这句就够了

    ranges = [
        "line__00_20", 
        "line__20_40", 
        "line__40_inf",
    ]
    exp_res_list: List[ExpRes] = []
    with open("data/res.jsonl") as file:
        for line in file:
            exp_res_list.append(ExpRes(**json.loads(line)))
    exp_res_list = [r for r in exp_res_list if r.method_range in ranges]

    model_names = list(set([r.model_name for r in exp_res_list]))
    model_names = [m for m in ORDERED_MODELS if m in model_names]

    @dataclass
    class _number:
        model_name: str
        language: str
        w_code: bool
        metric: str
        line_range: str
        number: float

    numbers: List[_number] = []

    def _find(
        numbers: List[_number],
        model_name,
        language,
        w_code,
        metric,
        line_range,
    ):
        for number in numbers:
            if model_name != number.model_name:
                continue
            if language != number.language:
                continue
            if w_code != number.w_code:
                continue
            if metric != number.metric:
                continue
            if line_range != number.line_range:
                continue
            return number
        return None

    # 仍然把 corr/comp 的 1 和 5 都展开成 numbers
    metric_field_names = [
        f"{metric}_{k}" for metric, k in product(["corr", "comp"], [1, 5])
    ]

    for r in exp_res_list:
        for field_name in metric_field_names:
            n = getattr(r, field_name)
            numbers.append(
                _number(
                    model_name=r.model_name,
                    language=r.language,
                    w_code=r.w_code,
                    metric=field_name,
                    line_range=r.method_range,
                    number=n,
                )
            )
    
    map_for_avg = {r: [] for r in ranges}
    for n in numbers:
        if n.metric in ["corr_1", "comp_1"]:
            map_for_avg[n.line_range].append(n.number)
    for r in ranges:
        print(r)
        print(map_for_avg[r])
        print(f"{sum(map_for_avg[r]) / len(map_for_avg[r]):.3f}")
        print(len(map_for_avg[r]))
        print()

    # ============ 画图部分 ============

    # 一行四列，四个子图共用 y 轴（对齐纵轴）
    # 用 constrained_layout 帮你自动腾出图例和标题的空间
    fig, axes = plt.subplots(
        2, 4, figsize=(12, 5.2), 
        sharey='row', sharex=True, constrained_layout=False
    )

    if isinstance(axes, np.ndarray):
        axes = axes.ravel()
    else:
        axes = [axes]

    # 子图顺序：先 python 后 java
    # 从左到右依次：python/corr_1, python/comp_1, java/corr_1, java/comp_1
    subplot_specs = [
        ("corr_1", "python", True),
        ("corr_1", "python", False),
        ("corr_1", "java", True),
        ("corr_1", "java", False),
        ("comp_1", "python", True),
        ("comp_1", "python", False),
        ("comp_1", "java", True),
        ("comp_1", "java", False),
    ]

    color_cycle = plt.rcParams["axes.prop_cycle"].by_key()["color"]

    def ensure_not_too_light(color, max_l=0.80):
        r, g, b = mcolors.to_rgb(color)
        h, l, s = colorsys.rgb_to_hls(r, g, b)
        if l > max_l:
            l = max_l
            r, g, b = colorsys.hls_to_rgb(h, l, s)
        return (r, g, b)

    def make_variant_colors(model_names, color_cycle):
        model_to_color = {}

        for i, model in enumerate(model_names):
            family_idx = i // 2
            base_color = color_cycle[family_idx % len(color_cycle)]

            r, g, b = mcolors.to_rgb(base_color)
            h, l, s = colorsys.rgb_to_hls(r, g, b)

            if i % 2 == 0:
                # family 的第一个：基色，但也可以过一遍 ensure_not_too_light
                variant = ensure_not_too_light((r, g, b), max_l=0.5)
            else:
                # family 的第二个：偏一点色相 + 变亮 + 降饱和
                h2 = (h + 0.08) % 1.0
                l2 = min(1.0, l + 0.08)
                s2 = max(0.0, min(1.0, s * 0.9))
                r2, g2, b2 = colorsys.hls_to_rgb(h2, l2, s2)
                variant = ensure_not_too_light((r2, g2, b2), max_l=0.5)

            model_to_color[model] = variant

        return model_to_color

    model_to_color = make_variant_colors(model_names, color_cycle)

    for i, (ax, (metric, lang, w_code)) in enumerate(zip(axes, subplot_specs)):
        for model_name in model_names:
            y_values = []
            has_any = False
            for line_range in ranges:
                n = _find(
                    numbers,
                    model_name=model_name,
                    language=lang,
                    w_code=w_code,
                    metric=metric,
                    line_range=line_range
                )
                if n is not None:
                    y_values.append(n.number)
                    has_any = True
                else:
                    y_values.append(float("nan"))

            if not has_any:
                continue

            linestyle = "-" if w_code else "--"
            color = model_to_color[model_name]

            task_name = "C2P" if w_code else "N2P"

            ax.plot(
                [1, 3, 5],
                y_values,
                linestyle=linestyle,
                marker="o",
                color=color,
                alpha=0.7,   # 半透明
                # linewidth=2.5,     # 线更粗一点
                markersize=7,      # 点更大一点
            )

        if i < 4:
            ax.set_title(f"{lang.capitalize()} {task_name}", fontsize=15)
        else:
            ax.set_xlabel("#LoC", fontsize=15)
        ax.set_xticks([1, 3, 5])
        ax.set_xticklabels(["[0,20)", "[20,40)", "[40,$\infty$)"])
        ax.tick_params(axis="both", labelsize=15)

        if i == 0:
            ax.set_ylabel("Corr@1", fontsize=15)
        elif i == 4:
            ax.set_ylabel("Comp@1", fontsize=15)

    # ========= 图例部分 =========

    # 1）颜色图例：用方形色块（Patch），左下，3×3
    color_handles = [
        Patch(facecolor=model_to_color[m], label=MODEL_NAME_MAP[m], 
              alpha=0.7)
        for m in model_names
    ]
    color_legend = fig.legend(
        handles=color_handles,
        labels=[MODEL_NAME_MAP[m] for m in model_names],
        loc="lower left",
        bbox_to_anchor=(0.05, 0.98),  # 左下角附近
        ncol=5,                        # 3 列 → 最多 3×3
        frameon=True,
        fontsize=13,
    )

    # 2）线型图例：只要线，不要点；右下，2 行 1 列
    style_handles = [
        Line2D([0], [0], linestyle="-",  linewidth=3, color="black", label="C2P"),
        Line2D([0], [0], linestyle="--", linewidth=3, color="black", label="N2P"),
    ]
    style_legend = fig.legend(
        handles=style_handles,
        loc="lower right",
        bbox_to_anchor=(0.95, 0.98),   # 右下角附近
        ncol=1,                        # 1 列 → 两行
        frameon=True,
        fontsize=13,
    )

    # 给两个图例都加黑色边框
    for leg in (color_legend, style_legend):
        frame = leg.get_frame()
        frame.set_edgecolor("black")
        frame.set_linewidth(0.8)

    fig.tight_layout(pad=2)

    plt.savefig("data/lines.pdf", bbox_inches="tight")


def fsl_line_chart():
    plt.rcParams['font.family'] = 'DejaVu Serif'   # 直接用这句就够了

    # 只画 corr_1 和 comp_1
    promptings = [
        "fsl_0",
        "fsl_1", 
        "fsl_3", 
        "fsl_5", 
        # "fsl_10", 
    ]
    exp_res_list: List[ExpRes] = []
    with open("data/res.jsonl") as file:
        for line in file:
            exp_res_list.append(ExpRes(**json.loads(line)))
    exp_res_list = [r for r in exp_res_list if 
                    r.prompting in promptings or \
                        (r.prompting is None and r.method_range is None)]
    for r in exp_res_list:
        if r.prompting is None:
            r.prompting = "fsl_0"

    model_names = list(set([r.model_name for r in exp_res_list]))
    model_names = [m for m in ORDERED_MODELS if m in model_names]

    @dataclass
    class _number:
        model_name: str
        language: str
        w_code: bool
        metric: str
        prompting: str
        number: float

    numbers: List[_number] = []

    def _find(
        numbers: List[_number],
        model_name,
        language,
        w_code,
        metric,
        prompting,
    ):
        for number in numbers:
            if model_name != number.model_name:
                continue
            if language != number.language:
                continue
            if w_code != number.w_code:
                continue
            if metric != number.metric:
                continue
            if prompting != number.prompting:
                continue
            return number
        return None

    # 仍然把 corr/comp 的 1 和 5 都展开成 numbers
    metric_field_names = [
        f"{metric}_{k}" for metric, k in product(["corr", "comp"], [1, 5])
    ]

    for r in exp_res_list:
        for field_name in metric_field_names:
            n = getattr(r, field_name)
            numbers.append(
                _number(
                    model_name=r.model_name,
                    language=r.language,
                    w_code=r.w_code,
                    metric=field_name,
                    prompting=r.prompting,
                    number=n,
                )
            )

    # ============ 画图部分 ============

    # 一行四列，四个子图共用 y 轴（对齐纵轴）
    # 用 constrained_layout 帮你自动腾出图例和标题的空间
    fig, axes = plt.subplots(
        2, 4, figsize=(12, 5.2), 
        sharey='row', sharex=True, constrained_layout=False
    )

    if isinstance(axes, np.ndarray):
        axes = axes.ravel()
    else:
        axes = [axes]

    # 子图顺序：先 python 后 java
    # 从左到右依次：python/corr_1, python/comp_1, java/corr_1, java/comp_1
    subplot_specs = [
        ("corr_1", "python", True),
        ("corr_1", "python", False),
        ("corr_1", "java", True),
        ("corr_1", "java", False),
        ("comp_1", "python", True),
        ("comp_1", "python", False),
        ("comp_1", "java", True),
        ("comp_1", "java", False),
    ]

    color_cycle = plt.rcParams["axes.prop_cycle"].by_key()["color"]

    def ensure_not_too_light(color, max_l=0.80):
        r, g, b = mcolors.to_rgb(color)
        h, l, s = colorsys.rgb_to_hls(r, g, b)
        if l > max_l:
            l = max_l
            r, g, b = colorsys.hls_to_rgb(h, l, s)
        return (r, g, b)

    def make_variant_colors(model_names, color_cycle):
        model_to_color = {}

        for i, model in enumerate(model_names):
            family_idx = i // 2
            base_color = color_cycle[family_idx % len(color_cycle)]

            r, g, b = mcolors.to_rgb(base_color)
            h, l, s = colorsys.rgb_to_hls(r, g, b)

            if i % 2 == 0:
                # family 的第一个：基色，但也可以过一遍 ensure_not_too_light
                variant = ensure_not_too_light((r, g, b), max_l=0.5)
            else:
                # family 的第二个：偏一点色相 + 变亮 + 降饱和
                h2 = (h + 0.08) % 1.0
                l2 = min(1.0, l + 0.08)
                s2 = max(0.0, min(1.0, s * 0.9))
                r2, g2, b2 = colorsys.hls_to_rgb(h2, l2, s2)
                variant = ensure_not_too_light((r2, g2, b2), max_l=0.5)

            model_to_color[model] = variant

        return model_to_color

    model_to_color = make_variant_colors(model_names, color_cycle)

    x_positions = [int(p.split("_")[1]) for p in promptings]
    print(x_positions)

    for i, (ax, (metric, lang, w_code)) in enumerate(zip(axes, subplot_specs)):
        for model_name in model_names:
            y_values = []
            has_any = False
            for prompting in promptings:
                n = _find(
                    numbers,
                    model_name=model_name,
                    language=lang,
                    w_code=w_code,
                    metric=metric,
                    prompting=prompting,
                )
                if n is not None:
                    y_values.append(n.number)
                    has_any = True
                else:
                    y_values.append(float("nan"))

            if not has_any:
                continue

            linestyle = "-" if w_code else "--"
            color = model_to_color[model_name]

            task_name = "C2P" if w_code else "N2P"

            ax.plot(
                x_positions,
                y_values,
                linestyle=linestyle,
                marker="o",
                color=color,
                alpha=0.7,   # 半透明
                # linewidth=2.5,     # 线更粗一点
                markersize=7,      # 点更大一点
            )

        if i < 4:
            ax.set_title(f"{lang.capitalize()} {task_name}", fontsize=15)
        else:
            ax.set_xlabel("#Shot", fontsize=15)
        ax.set_xticks(x_positions)
        ax.set_xticklabels(x_positions)
        ax.tick_params(axis="both", labelsize=15)

        if i == 0:
            ax.set_ylabel("Corr@1", fontsize=15)
        elif i == 4:
            ax.set_ylabel("Comp@1", fontsize=15)

    # ========= 图例部分 =========

    # 1）颜色图例：用方形色块（Patch），左下，3×3
    color_handles = [
        Patch(facecolor=model_to_color[m], label=MODEL_NAME_MAP[m], 
              alpha=0.7)
        for m in model_names
    ]
    color_legend = fig.legend(
        handles=color_handles,
        labels=[MODEL_NAME_MAP[m] for m in model_names],
        loc="lower left",
        bbox_to_anchor=(0.05, 0.98),  # 左下角附近
        ncol=5,                        # 3 列 → 最多 3×3
        frameon=True,
        fontsize=13,
    )

    # 2）线型图例：只要线，不要点；右下，2 行 1 列
    style_handles = [
        Line2D([0], [0], linestyle="-",  linewidth=3, color="black", label="C2P"),
        Line2D([0], [0], linestyle="--", linewidth=3, color="black", label="N2P"),
    ]
    style_legend = fig.legend(
        handles=style_handles,
        loc="lower right",
        bbox_to_anchor=(0.95, 0.98),   # 右下角附近
        ncol=1,                        # 1 列 → 两行
        frameon=True,
        fontsize=13,
    )

    # 给两个图例都加黑色边框
    for leg in (color_legend, style_legend):
        frame = leg.get_frame()
        frame.set_edgecolor("black")
        frame.set_linewidth(0.8)

    fig.tight_layout(pad=2)

    plt.savefig("data/fsl.pdf", bbox_inches="tight")


def mutation_FDR():
    exp_res_list: List[ExpRes] = []
    with open("data/res.jsonl") as file:
        for line in file:
            exp_res_list.append(ExpRes(**json.loads(line)))
    exp_res_list = [
        r for r in exp_res_list 
        if r.method_range is None and r.prompting is None]
    model_names = list(set([r.model_name for r in exp_res_list]))
    model_names = [m for m in ORDERED_MODELS if m in model_names]


    @dataclass
    class _number:
        model_name: str
        language: str
        w_code: bool
        metric: str
        number: float
        should_bold: bool

    numbers: List[_number] = []

    def _find(numbers: List[_number], 
              model_name, language, w_code, metric) -> _number:
        for number in numbers:
            if model_name != number.model_name:
                continue
            if language != number.language:
                continue
            if w_code != number.w_code:
                continue
            if metric != number.metric:
                continue
            return number
        return None

    metric_field_names = [
        "rule_precision", "llm_precision"]
    
    __iter = product(model_names, LANGUAGES, [True, False])
    for model_name, lang, w_code in __iter:
        __exp_res_list = [
            r for r in exp_res_list if 
            lang == r.language and w_code == r.w_code and model_name == r.model_name]
        assert len(__exp_res_list) == 1
        exp_res = __exp_res_list[0]
        for field_name in metric_field_names:
            n = getattr(exp_res, field_name)
            if n is None:
                continue
            should_bold = all(n >= getattr(exp_res, field_name) 
                              for field_name in metric_field_names)
            numbers.append(_number(
                model_name=exp_res.model_name,
                language=exp_res.language,
                w_code=exp_res.w_code,
                metric=field_name,
                number=n,
                should_bold=should_bold
            ))

    __iter = product(LANGUAGES, [True, False], metric_field_names)
    avg_numbers: List[_number] = []
    for lang, w_code, field_name in __iter:
        __exp_res_list = [
            r for r in exp_res_list if 
            lang == r.language and w_code == r.w_code]
        assert len(__exp_res_list) == len(model_names)
        avg = [getattr(exp_res, field_name) for exp_res in __exp_res_list]
        avg = [n for n in avg if n is not None]
        avg = sum(avg) / len(avg)
        pal_numbers = [_n for _n in avg_numbers 
                       if _n.language == lang and _n.w_code == w_code]
        assert len(pal_numbers) in [0, 1]
        cur =_number(
            model_name="Avg",
            language=lang,
            w_code=w_code,
            metric=field_name,
            number=avg,
            should_bold=None
        )
        avg_numbers.append(cur)
        if len(pal_numbers) > 0:
            pal = pal_numbers[0]
            pal.should_bold = pal.number >= cur.number
            cur.should_bold = cur.number >= pal.number
    numbers.extend(avg_numbers)

    width = 8

    for row_idx, model_name in enumerate(model_names + ["Avg"]):
        if model_name == "Avg":
            print("\\midrule")
        number_str_list = []
        ___iter = product(["python", "java"], [True, False], metric_field_names)
        for col_idx, (lang, w_code, field_name) in enumerate(___iter):
            number = _find(numbers, model_name, lang, w_code, field_name)
            if number is not None:
                # NOTE: FDR = 1 - precision !!!
                fdr = 1 - number.number
                number_str = _f2s(fdr)
                if number.should_bold:
                    number_str = _bold(number_str)
            else:
                number_str = "-"
            number_str_list.append(number_str)
        assert len(number_str_list) == width, f"{len(number_str_list)} != {width}"

        if model_name == "Avg":
            la_model_name = "\\textbf{Avg}"
        else:
            la_model_name = MODEL_NAME_MAP[model_name]

        print(f"{la_model_name} & ", end="")
        print(" & ".join(number_str_list) + f" \\\\")


if __name__ == "__main__":
    # data = []
    # for file_name in os.listdir("data/batch--gpt-5--out--1st-run"):
    #     with open(f"data/batch--gpt-5--out--1st-run/{file_name}") as file:
    #         data.extend([json.loads(l) for l in file])
    # lengths = [i["response"]["body"]["usage"]["input_tokens"] for i in data]
    # token_sum = sum(lengths)
    # print(token_sum / len(data))
    # print(token_sum)
    # print(len([l for l in lengths if l > 8000]))
    # print(len(data))
    # exit()

    # get_exp_res()
    main_res()
    # analyze_dep()
    # code_line_line_chart()
    # analyze_no_gram()
    fsl_line_chart()
    # mutation_FDR()
    print("done")