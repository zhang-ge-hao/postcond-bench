# src/mutation/pit/__init__.py
from __future__ import annotations
from typing import List, Tuple

from src.util import parse_code, get_language_and_parser

from .java_mutators import ALL_JAVA_MUTATORS, TextEdit, apply_single_edit


def generate_mutants_for_method(method: str, w_mut_name: bool = False):
    # --- 用固定外壳包裹，保证 parser 能识别 method_declaration ---
    prefix = "class __W__ {\n"
    suffix = "\n}\n"
    wrapped = prefix + method.strip("\n") + suffix

    lang, parser = get_language_and_parser("java")
    tree, code_str, code_bytes = parse_code(wrapped, parser)
    root = tree.root_node

    # 1) 从所有 mutator 收集 TextEdit（包含 start_byte/end_byte） + mutator name
    # (start_byte, seq, edit, mut_name)
    all_edits: List[Tuple[int, int, TextEdit, str]] = []
    seq = 0
    for mutator in ALL_JAVA_MUTATORS:
        mut_name = getattr(mutator, "name", mutator.__class__.__name__)
        edits = mutator._collect_edits(code_str, root)  # type: ignore[attr-defined]
        for e in edits:
            all_edits.append((e.start_byte, seq, e, mut_name))
            seq += 1

    # 2) 按 start_byte 升序排序；同起点按发现顺序稳定排序
    all_edits.sort(key=lambda t: (t[0], t[1]))

    # 3) 逐个应用到“原始包裹源码”，得到排序后的 mutants（仍是包裹形态）
    mutants_wrapped: List[str] = []
    mut_names_wrapped: List[str] = []
    for _, _, e, mut_name in all_edits:
        mw = apply_single_edit(code_str, e)
        mutants_wrapped.append(mw)
        if w_mut_name:
            mut_names_wrapped.append(mut_name)

    # 4) 去掉外壳，仅返回方法源码
    pre_b = prefix.encode("utf-8")
    suf_b = suffix.encode("utf-8")

    mutants: List[str] = []
    mut_names: List[str] = []

    for i, mw in enumerate(mutants_wrapped):
        b = mw.encode("utf-8")
        inner = b[len(pre_b): len(b) - len(suf_b)]
        mtxt = inner.decode("utf-8")
        mutants.append(mtxt)
        if w_mut_name:
            mut_names.append(mut_names_wrapped[i])

    # 5) 去重但保序（避免同一位置被不同 mutator 生成相同文本）
    if not w_mut_name:
        mutants = list(dict.fromkeys(mutants))
        return mutants

    seen = set()
    uniq_mutants: List[str] = []
    uniq_names: List[str] = []
    for mtxt, nm in zip(mutants, mut_names):
        if mtxt in seen:
            continue
        seen.add(mtxt)
        uniq_mutants.append(mtxt)
        uniq_names.append(nm)

    return uniq_mutants, uniq_names
