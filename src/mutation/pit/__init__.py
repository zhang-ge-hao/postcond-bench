# src/mutation/engine.py
from __future__ import annotations
from typing import List, Tuple

from src.util import parse_code, get_language_and_parser

from .java_mutators import ALL_JAVA_MUTATORS, TextEdit, apply_single_edit

def generate_mutants_for_method(method: str) -> List[str]:
    """
    输入：Method.content 为单个 Java 方法源码
    输出：各突变点（槽位）按源码先后顺序返回的变体列表（一次只改一个点）
    仅对 Java 生效；非 Java 返回空列表。
    """
    # --- 用固定外壳包裹，保证 parser 能识别 method_declaration ---
    prefix = "class __W__ {\n"
    suffix = "\n}\n"
    wrapped = prefix + method.strip("\n") + "\n" + suffix

    lang, parser = get_language_and_parser("java")
    tree, code_str, code_bytes = parse_code(wrapped, parser)
    root = tree.root_node

    # 1) 先从所有 mutator 收集 TextEdit（包含 start_byte/end_byte）
    all_edits: List[Tuple[int, int, TextEdit]] = []  # (start_byte, seq, edit)
    seq = 0
    for mutator in ALL_JAVA_MUTATORS:
        # 直接调用“受保护”方法没问题：这是同一工程内约定俗成的内部 API
        edits = mutator._collect_edits(code_str, root)  # type: ignore[attr-defined]
        for e in edits:
            all_edits.append((e.start_byte, seq, e))
            seq += 1

    # 2) 按 start_byte 升序排序；同起点按发现顺序稳定排序
    all_edits.sort(key=lambda t: (t[0], t[1]))

    # 3) 逐个应用到“原始包裹源码”，得到排序后的 mutants（仍是包裹形态）
    mutants_wrapped: List[str] = []
    for _, _, e in all_edits:
        mw = apply_single_edit(code_str, e)
        mutants_wrapped.append(mw)

    # 4) 去掉外壳，仅返回方法源码
    pre_b = prefix.encode("utf-8")
    suf_b = suffix.encode("utf-8")
    result: List[str] = []
    for mw in mutants_wrapped:
        b = mw.encode("utf-8")
        inner = b[len(pre_b): len(b) - len(suf_b)]
        result.append(inner.decode("utf-8"))

    # 5) 去重但保序（避免同一位置被不同 mutator 生成相同文本）
    result = list(dict.fromkeys(result))
    return result
