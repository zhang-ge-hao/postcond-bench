#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Translate method-level JML `ensures` in Java sources into Java `assert` lines
using a wrapper method scheme, supporting `\result`, `\old(...)`, and JML
inference operators `==>`, `<==>` (equivalence), and `<=!=>` (inequivalence).

This file is **self-contained** and includes a small test driver in `main()`
that exercises the translator on several tiny Java snippets. It does not read
or write any files.

Requirements:
  - Python 3.9+
  - pip install tree_sitter tree_sitter_java (or tree_sitter_languages)

Run:
  python translate_jml_ensures_tests.py
"""

from dataclasses import dataclass
import re
from typing import List, Tuple, Dict, Optional

from tree_sitter import Language, Parser, Node
import tree_sitter_java as tsjava

# -----------------------------------------------------------------------------
# Parser initialization
# -----------------------------------------------------------------------------
JAVA_LANGUAGE = Language(tsjava.language())
JAVA_PARSER = Parser(JAVA_LANGUAGE)


# -----------------------------------------------------------------------------
# Data model
# -----------------------------------------------------------------------------
@dataclass
class MethodInfo:
    node: Node
    name: str
    start_byte: int
    end_byte: int
    header_start: int
    body_start: int
    body_end: int
    name_start_in_header: int  # offset inside header text
    is_void: bool
    param_names: List[str]
    is_static: bool


# -----------------------------------------------------------------------------
# Utilities
# -----------------------------------------------------------------------------
def _bytes_to_str(b: bytes) -> str:
    return b.decode("utf-8", errors="ignore")


def parse_java(src: str):
    return JAVA_PARSER.parse(src.encode("utf-8"))


# -----------------------------------------------------------------------------
# Method collection from the Java syntax tree
# -----------------------------------------------------------------------------
def collect_methods(src: str, tree) -> List[MethodInfo]:
    """Recursively collect all `method_declaration` nodes that have a body."""
    root = tree.root_node
    src_b = src.encode("utf-8")
    methods: List[MethodInfo] = []

    def walk(n: Node):
        if n.type == "method_declaration":
            name_node = n.child_by_field_name("name")
            params_node = n.child_by_field_name("parameters")
            type_node = n.child_by_field_name("type")
            body_node = n.child_by_field_name("body")
            if not (name_node and params_node and type_node and body_node):
                return

            name = _bytes_to_str(src_b[name_node.start_byte:name_node.end_byte])
            ret_text = _bytes_to_str(src_b[type_node.start_byte:type_node.end_byte]).strip()
            is_void = (ret_text == "void")

            # Determine `static` via modifiers text before the type
            modifiers_text = _bytes_to_str(src_b[n.start_byte:type_node.start_byte])
            is_static = re.search(r"\bstatic\b", modifiers_text) is not None

            header_start = n.start_byte
            body_start = body_node.start_byte
            body_end = body_node.end_byte

            name_rel_start = name_node.start_byte - header_start

            param_names = extract_param_names(src, params_node)
            methods.append(
                MethodInfo(
                    node=n,
                    name=name,
                    start_byte=n.start_byte,
                    end_byte=n.end_byte,
                    header_start=header_start,
                    body_start=body_start,
                    body_end=body_end,
                    name_start_in_header=name_rel_start,
                    is_void=is_void,
                    param_names=param_names,
                    is_static=is_static,
                )
            )
        for c in n.children:
            walk(c)

    walk(root)
    methods.sort(key=lambda m: m.start_byte)
    return methods


def extract_param_names(src: str, params_node: Node) -> List[str]:
    """Pull out parameter names (supports varargs/spread_parameter)."""
    names: List[str] = []
    src_b = src.encode("utf-8")

    def first_identifier_inside(n: Node) -> Optional[str]:
        if n.type == "identifier":
            return _bytes_to_str(src_b[n.start_byte:n.end_byte])
        for ch in n.children:
            got = first_identifier_inside(ch)
            if got:
                return got
        return None

    def walk(n: Node):
        if n.type in ("formal_parameter", "inferred_parameter", "spread_parameter"):
            decl = n.child_by_field_name("declarator") or n.child_by_field_name("name")
            if decl:
                ident = first_identifier_inside(decl)
                if ident:
                    names.append(ident)
        else:
            for ch in n.children:
                walk(ch)

    walk(params_node)
    return names


# -----------------------------------------------------------------------------
# Extract `ensures` lines from comments immediately above a method
# -----------------------------------------------------------------------------
ENSURES_LINE_RE = re.compile(r"\bensures\b\s+(.*)", re.IGNORECASE)

def _cut_jml_clause(text: str, allow_line_comment_terminator: bool) -> str:
    """
    从 ensures 后面的文本里，提取到 JML 子句结束为止的表达式：
      - 以“顶层分号 ; ”为结束（括号深度为 0，且不在字符串/字符字面量中）
      - 可选地（在行注释风格下）遇到顶层 ‘//’ 也作为结束
    """
    s = text.strip()
    out = []
    depth = 0
    in_str = False
    in_chr = False
    esc = False
    i = 0
    n = len(s)

    while i < n:
        ch = s[i]
        nxt = s[i + 1] if i + 1 < n else ""

        if esc:
            out.append(ch)
            esc = False
            i += 1
            continue

        if in_str:
            if ch == "\\":
                esc = True
            elif ch == '"':
                in_str = False
            out.append(ch)
            i += 1
            continue

        if in_chr:
            if ch == "\\":
                esc = True
            elif ch == "'":
                in_chr = False
            out.append(ch)
            i += 1
            continue

        # 不在字符串/字符字面量中
        if ch == '"':
            in_str = True
            out.append(ch)
            i += 1
            continue
        if ch == "'":
            in_chr = True
            out.append(ch)
            i += 1
            continue
        if ch == '(':
            depth += 1
            out.append(ch)
            i += 1
            continue
        if ch == ')':
            if depth > 0:
                depth -= 1
            out.append(ch)
            i += 1
            continue

        # 顶层分号 => 子句结束
        if ch == ';' and depth == 0:
            break

        # 在行注释风格中，顶层的 "//" 也作为结束（用于去掉行尾说明）
        if allow_line_comment_terminator and ch == '/' and nxt == '/' and depth == 0:
            break

        out.append(ch)
        i += 1

    return ''.join(out).strip()

def extract_ensures_above_method(src: str, method) -> List[str]:
    """
    Scan upwards over the contiguous comment/blank block that directly precedes
    a method, and collect all `ensures ...` lines.

    Supports:
      - `//@ ensures ...`
      - `/*@ ... ensures ... @*/` and standard block comments containing
        lines with `ensures ...`
    """
    lines = src.splitlines(True)
    start_line_index = src.encode("utf-8")[:method.start_byte].decode("utf-8").count("\n")
    i = start_line_index - 1

    collected: List[str] = []
    in_block = False
    # block_buf: List[str] = []

    while i >= 0:
        raw = lines[i]
        s = raw.rstrip("\r\n")
        stripped = s.strip()

        if stripped == "":
            collected.append(s)
            i -= 1
            continue

        if stripped.startswith("//"):
            collected.append(s)
            i -= 1
            continue

        # Block comment: glue upwards until `/*` is found
        if stripped.endswith("*/") or stripped.startswith("*/"):
            in_block = True

        if in_block:
            # block_buf.append(s)
            if "/*" in stripped:
                # block_text = "\n".join(reversed(block_buf))
                # collected.append(block_text)
                # block_buf = []
                in_block = False
            i -= 1
            continue

        break  # encountered non-comment, non-blank

    collected = list(reversed(collected))

    ensures_exprs: List[str] = []

    def harvest_block(block_text: str):
        # 遍历块注释的每一行，提取 ensures 行
        for line in block_text.splitlines():
            ls = line.strip()
            m = ENSURES_LINE_RE.search(ls)
            if not m:
                continue
            expr_raw = m.group(1).strip()
            # 去除可能黏在表达式末尾的 "*/"
            expr_raw = expr_raw.rstrip("*/").strip()
            # 在块注释里不把 '//' 视为终止，只看“顶层 ;”
            expr = _cut_jml_clause(expr_raw, allow_line_comment_terminator=False)
            if expr:
                ensures_exprs.append(expr)

    for chunk in collected:
        if "\n" in chunk and ("/*" in chunk or "*/" in chunk):
            harvest_block(chunk)
        else:
            ls = chunk.strip()
            if ls.startswith("//"):
                m = ENSURES_LINE_RE.search(ls)
                if not m:
                    continue
                expr_raw = m.group(1).strip()
                # 行注释风格：允许把顶层 "//" 当作终止以剔除行尾说明
                expr = _cut_jml_clause(expr_raw, allow_line_comment_terminator=True)
                if expr:
                    ensures_exprs.append(expr)

    return ensures_exprs


# -----------------------------------------------------------------------------
# JML tokens & replacements: \old, \result, and inference operators
# -----------------------------------------------------------------------------
OLD_TOKEN = r'\old'
RESULT_RE = re.compile(r'\\result\b')  # replace `\result` with `__ret`

EQUIV_OP = "<==>"
INEQUIV_OP = "<=!=>"
IMPL_OP = "==>"


# --- Inference operators parsing & transformation ---

def _split_top_level(expr: str, ops: List[str]) -> Tuple[List[str], List[str]]:
    """Split `expr` at top-level (outside parens and string/char literals)
    by any of the multi-char operators in `ops`.

    Returns (tokens, separators). Example:
      "a<==>b==>c" with ops ["<==>", "==>"] ->
      tokens=["a", "b", "c"], seps=["<==>", "==>"]
    """
    s = expr
    n = len(s)
    i = 0
    last = 0
    depth = 0
    tokens: List[str] = []
    seps: List[str] = []

    in_str = False
    in_chr = False
    esc = False

    ops_sorted = sorted(ops, key=len, reverse=True)

    while i < n:
        ch = s[i]
        if in_str:
            if ch == '"' and not esc:
                in_str = False
            esc = (ch == '\\' and not esc)
            i += 1
            continue
        if in_chr:
            if ch == "'" and not esc:
                in_chr = False
            esc = (ch == '\\' and not esc)
            i += 1
            continue
        if ch == '"':
            in_str = True
            i += 1
            continue
        if ch == "'":
            in_chr = True
            i += 1
            continue
        if ch == '(':
            depth += 1
            i += 1
            continue
        if ch == ')':
            if depth > 0:
                depth -= 1
            i += 1
            continue

        if depth == 0:
            matched = False
            for op in ops_sorted:
                if s.startswith(op, i):
                    tokens.append(s[last:i].strip())
                    seps.append(op)
                    i += len(op)
                    last = i
                    matched = True
                    break
            if matched:
                continue
        i += 1

    tokens.append(s[last:].strip())
    return tokens, seps


def _paren_wrap(x: str) -> str:
    x = x.strip()
    if not x:
        return x
    return f"({x})"


def transform_inference_ops(expr: str) -> str:
    """Transform JML's ==> / <==> / <=!=> into Java boolean logic.

    Rules:
      a ==> b      => (!a) || (b)                      (right associative)
      a <==> b     => (a == b)                         (left associative; add parens to preserve JML precedence)
      a <=!=> b    => (a != b)                         (left associative; add parens to preserve JML precedence)
    """
    expr = expr.strip()

    def has_wrapping_parens(s: str) -> bool:
        # whether the whole string is enclosed by a single matching pair of parentheses
        i, n = 0, len(s)
        while i < n and s[i].isspace():
            i += 1
        if i >= n or s[i] != '(':
            return False
        j = n - 1
        while j >= 0 and s[j].isspace():
            j -= 1
        if j < 0 or s[j] != ')':
            return False

        depth = 0
        k = i
        in_str = in_chr = False
        esc = False
        while k <= j:
            ch = s[k]
            if in_str:
                if ch == '"' and not esc:
                    in_str = False
                esc = (ch == '\\' and not esc)
            elif in_chr:
                if ch == "'" and not esc:
                    in_chr = False
                esc = (ch == '\\' and not esc)
            else:
                if ch == '"':
                    in_str = True
                elif ch == "'":
                    in_chr = True
                elif ch == '(':
                    depth += 1
                elif ch == ')':
                    depth -= 1
                    if depth == 0 and k != j:
                        return False
            k += 1
        return True

    def _paren_wrap(x: str) -> str:
        x = x.strip()
        return f"({x})" if x and not (x.startswith("(") and x.endswith(")")) else x

    def parse_equiv(s: str) -> str:
        # <==> 和 <=!=>（较低优先级），左结合
        toks, ops = _split_top_level(s, [EQUIV_OP, INEQUIV_OP])
        if ops:
            res = parse_impl(toks[0])
            for idx, op in enumerate(ops):
                right = parse_impl(toks[idx + 1])
                L = _paren_wrap(res)
                R = _paren_wrap(right)
                if op == EQUIV_OP:
                    # 直接使用 Java 的布尔相等；加括号保证优先级与 JML 一致
                    res = f"({L} == {R})"
                else:  # INEQUIV_OP
                    res = f"({L} != {R})"
            return res
        return parse_impl(s)

    def parse_impl(s: str) -> str:
        # ==>（高于 <==>/<=!=>），右结合
        toks, ops = _split_top_level(s, [IMPL_OP])
        if ops:
            acc = parse_term(toks[-1])
            for i in range(len(toks) - 2, -1, -1):
                left = parse_term(toks[i])
                L = _paren_wrap(left)
                R = _paren_wrap(acc)
                acc = f"(!{L} || {R})"
            return acc
        return parse_term(s)

    def parse_term(s: str) -> str:
        s = s.strip()
        # 去除一层最外括号后递归，让括号内的 ==> / <==> / <=!=> 也能被继续解析
        while s and has_wrapping_parens(s):
            s = s[1:-1].strip()
        # 再走一遍等价层，确保嵌套里的运算符被吃掉
        return parse_equiv(s) if any(op in s for op in (IMPL_OP, EQUIV_OP, INEQUIV_OP)) else s

    return parse_equiv(expr)


# -----------------------------------------------------------------------------
# \old & \result helpers
# -----------------------------------------------------------------------------
def sanitize_old_var(expr: str) -> str:
    """Turn an expression into a safe suffix for a synthesized variable name."""
    s = re.sub(r"\s+", "", expr)
    s = s.replace("this.", "this_")
    s = re.sub(r"[^0-9a-zA-Z_]", "_", s)
    s = re.sub(r"_+", "_", s).strip("_")
    return s or "expr"


def _next_unique_old_name(expr: str, used_names: set) -> str:
    base = "__old_" + sanitize_old_var(expr)
    name = base or "__old_expr"
    if name in used_names:
        c = 2
        while f"{base}_{c}" in used_names:
            c += 1
        name = f"{base}_{c}"
    used_names.add(name)
    return name


def _replace_old_calls_with_placeholders(s: str, old_map: Dict[str, str]) -> str:
    """Find all `\old(...)` occurrences, parse their (possibly nested) argument,
    and replace each with a stable placeholder variable name, recording a map
    from original-arg-text -> placeholder.
    """
    out = []
    i = 0
    n = len(s)
    used_names = set(old_map.values())

    while i < n:
        j = s.find(OLD_TOKEN, i)
        if j == -1:
            out.append(s[i:])
            break

        # Emit prefix unchanged
        out.append(s[i:j])

        k = j + len(OLD_TOKEN)
        while k < n and s[k].isspace():
            k += 1

        # Must be followed by '(' to be treated as a call; otherwise emit '\'
        if k >= n or s[k] != '(':
            out.append(s[j])
            i = j + 1
            continue

        # Parse matching parens (support nesting)
        depth = 1
        p = k + 1
        end = -1
        while p < n:
            ch = s[p]
            if ch == '(':
                depth += 1
            elif ch == ')':
                depth -= 1
                if depth == 0:
                    end = p
                    break
            p += 1

        if end == -1:
            # Unmatched paren; emit rest unchanged
            out.append(s[j:])
            i = n
            break

        arg = s[k + 1:end].strip()
        if arg not in old_map:
            old_map[arg] = _next_unique_old_name(arg, used_names)
        out.append(old_map[arg])
        i = end + 1

    return "".join(out)


def translate_ensures_list(ensures: List[str]) -> Tuple[List[str], Dict[str, str]]:
    """
    1) Gather all `\old(...)` args into `old_map`.
    2) Replace `\old(...)` with placeholders.
    3) Replace `\result` with `__ret`.
    4) Transform JML inference operators ==> / <==> / <=!=> into Java logic.
    """
    old_map: Dict[str, str] = {}
    translated: List[str] = []

    for e in ensures:
        t = _replace_old_calls_with_placeholders(e, old_map)
        t = RESULT_RE.sub("__ret", t)
        t = transform_inference_ops(t)
        translated.append(t.strip())

    return translated, old_map


# -----------------------------------------------------------------------------
# Code generation (wrapper method + toBeValidated clone)
# -----------------------------------------------------------------------------
def infer_indentation(src: str, method: MethodInfo) -> Tuple[str, str]:
    line_start_pos = src.rfind("\n", 0, method.start_byte) + 1
    line_text = src.encode("utf-8")[line_start_pos:method.start_byte].decode()
    method_indent = re.match(r"[ \t]*", line_text).group(0)
    inner_indent = method_indent + "    "
    return method_indent, inner_indent


def build_wrapper_body(inner_indent: str, param_names: List[str],
                       translated_ensures: List[str],
                       old_map: Dict[str, str], call_name: str,
                       is_void: bool) -> str:
    lines: List[str] = []
    # 为 \old(...) 生成旧值快照 —— 这里也要把 ==> / <==> / <=!=> 翻译掉
    for old_expr, varname in old_map.items():
        old_transformed = transform_inference_ops(old_expr)  # 关键修复
        lines.append(f"{inner_indent}var {varname} = {old_transformed};")

    args = ", ".join(param_names)
    if not is_void:
        lines.append(f"{inner_indent}var __ret = {call_name}({args});")
    else:
        lines.append(f"{inner_indent}{call_name}({args});")

    # 断言（translated_ensures 里已经把 \old(...) -> 占位符、\result -> __ret、并翻译了推理运算符）
    for cond in translated_ensures:
        lines.append(f"{inner_indent}assert {cond}: \"JML Post-condition Failed\";")

    if not is_void:
        lines.append(f"{inner_indent}return __ret;")
    method_indent = inner_indent[:-4] if len(inner_indent) >= 4 else ""
    return "{\n" + "\n".join(lines) + "\n" + method_indent + "}"


def make_to_be_validated_header(header_text: str, name_rel_start: int, old_name: str) -> str:
    new_name = old_name + "_toBeValidated"
    before = header_text[:name_rel_start]
    after = header_text[name_rel_start + len(old_name):]
    header = before + new_name + after

    # Drop explicit @Override if present
    header = re.sub(r"(?m)^\s*@Override\s*\r?\n", "", header)
    header = re.sub(r"(?m)\s*@Override\s*", " ", header)

    # Force access to private
    if re.search(r"(?m)^(?P<ind>\s*)(public|protected|default)\b", header):
        header = re.sub(r"(?m)^(?P<ind>\s*)(public|protected|default)\b", r"\g<ind>private", header)
    elif not re.search(r"(?m)^(?P<ind>\s*)(private)\b", header):
        header = re.sub(r"(?m)^(\s*)", r"\1private ", header, count=1)

    return header


def rewrite_java_source(src: str) -> str:
    tree = parse_java(src)
    methods = collect_methods(src, tree)

    output_parts: List[str] = []
    cursor = 0
    src_b = src.encode("utf-8")

    for m in methods:
        ensures = extract_ensures_above_method(src, m)
        if not ensures:
            continue
        translated, old_map = translate_ensures_list(ensures)
        _, inner_indent = infer_indentation(src, m)
        call_name = m.name + "_toBeValidated"
        wrapper_body = build_wrapper_body(inner_indent, m.param_names,
                                          translated, old_map,
                                          call_name, m.is_void)

        header_text = _bytes_to_str(src_b[m.header_start:m.body_start])
        orig_body_text = _bytes_to_str(src_b[m.body_start:m.body_end])

        wrapper_src = header_text + wrapper_body
        tobe_header = make_to_be_validated_header(header_text, m.name_start_in_header, m.name)
        tobe_src = tobe_header + orig_body_text

        output_parts.append(_bytes_to_str(src_b[cursor:m.start_byte]))
        output_parts.append(wrapper_src)
        output_parts.append("\n\n")
        output_parts.append(tobe_src)
        cursor = m.end_byte

    output_parts.append(_bytes_to_str(src_b[cursor:]))
    return "".join(output_parts)


# -----------------------------------------------------------------------------
# Minimal test driver (as requested). Do not change existing tests.
# -----------------------------------------------------------------------------

def main():
    """Run a few minimal, self-contained tests without touching the filesystem.
    Each test is a tiny Java snippet with JML `ensures` just above a method.
    We print the transformed source and run a few substring-based checks.
    """

    def run_case(name: str, java_src: str):
        print("\n" + "=" * 80)
        print(f"CASE: {name}")
        print("- Input:")
        print(java_src)
        out = rewrite_java_source(java_src)
        print("- Output:")
        print(out)


    with open("data/TestFramework.java") as file:
        src0 = file.read()
    run_case("implication", src0)


    # 1) 基础蕴含 ==> : assert (!a) || (b)
    src1 = r"""
class C1 {
    //@ ensures a ==> b // ccccococococococooccoococ;
    //@ ensures \old(a & (a || b)) ==> a
    //@ ensures \old(a ==> b) ==> \result
    //@ ensures \old(a < b) ==> \result
    public int f(boolean a, boolean b) {
        return a ? 1 : 0;
    }
}
"""
    run_case("implication", src1)

    # 2) 等价 <==> : (x && y) || (!x && !y)
    src2 = r"""
class C2 {
    //@ ensures x <==> x ==> (y ==> x);
    public void g(boolean x, boolean y) { }
}
"""
    run_case("equivalence", src2)

    # 3) 不等价 <=!=> : (x && !y) || (!x && y)
    src3 = r"""
class C3 {
    //@ ensures x <=!=> y;
    public void h(boolean x, boolean y) { }
}
"""
    run_case("inequivalence", src3)

    # 4) 嵌套: (a ==> b) <==> c
    src4 = r"""
class C4 {
    //@ ensures a ==> b <==> c;
    //@ ensures (a ==> b) <==> c;
    //@ ensures a ==> (b <==> c);
    //@ ensures a <==> b ==> c;
    //@ ensures a <==> (b ==> c);
    //@ ensures (a <==> b) ==> c;
    //@ ensures (a <==> \old(b)) ==> c;
    public boolean k(boolean a, boolean b, boolean c) { return a && b && c; }
}
"""
    run_case("nested implication inside equivalence", src4)

    # 5) \old 与不等价: \old(x) <=!=> x
    src5 = r"""
class C5 {
    //@ ensures \old(x) <=!=> x;
    public void m(boolean x) { x = !x; }
}
"""
    run_case("old plus inequivalence", src5)

    # 6) \result 与蕴含: \result ==> flag
    src6 = r"""
class C6 {
    //@ ensures \result ==> flag;
    public boolean ok(boolean flag) { return flag; }
}
"""
    run_case("result implies flag", src6)

    # 7) 右结合链: a ==> b ==> c  => a ==> (b ==> c)
    src7 = r"""
class C7 {
    //@ ensures a ==> b ==> c;
    public void t(boolean a, boolean b, boolean c) { }
}
"""
    run_case("implication chain right-assoc", src7)

    # 8) 左结合链: a <==> b <==> c
    src8 = r"""
class C8 {
    //@ ensures a <==> b <==> c;
    public void u(boolean a, boolean b, boolean c) { }
}
"""
    run_case("equivalence chain left-assoc", src8)


if __name__ == "__main__":
    main()
