from typing import List, Tuple, Optional, Set
from bisect import bisect_right

from src.util import get_language_and_parser, parse_code

# ------------ helpers ------------
def _walk(node):
    yield node
    for i in range(node.named_child_count):
        child = node.named_children[i]
        yield from _walk(child)

def _line_start_byte_indices(text: str) -> List[int]:
    """Return 0-based list of byte offsets for the start of each line."""
    starts = []
    b = 0
    for line in text.splitlines(keepends=True):
        starts.append(b)
        b += len(line.encode("utf-8"))
    # handle empty file
    if not starts:
        starts = [0]
    return starts

def _byte_to_line(line_starts: List[int], byte_pos: int) -> int:
    """Map a byte offset to a 0-based line index using binary search."""
    # index of first start > byte_pos
    i = bisect_right(line_starts, byte_pos) - 1
    if i < 0:
        return 0
    if i >= len(line_starts):
        return len(line_starts) - 1
    return i

def _span_bytes_to_line_range(text: str, start_b: int, end_b: int) -> Tuple[int, int]:
    """
    Convert a half-open byte span [start_b, end_b) to inclusive 0-based line range.
    If end_b falls exactly on a line start, the last covered line is previous line.
    """
    line_starts = _line_start_byte_indices(text)
    start_ln = _byte_to_line(line_starts, start_b)
    # For end byte, subtract 1 so that a span ending at a line start doesn't include the next line.
    end_b_adj = max(start_b, end_b - 1)
    end_ln = _byte_to_line(line_starts, end_b_adj)
    return start_ln, end_ln

# ------------ site collectors (only 3 kinds) ------------
def _collect_sites_python(code: str, tree) -> List[Tuple[int, int, str]]:
    """
    Return list of (start_byte, end_byte, kind), where kind in {"cond", "loop-header", "call"}.
    """
    root = tree.root_node
    spans: List[Tuple[int, int, str]] = []

    for n in _walk(root):
        t = n.type

        # 1) 条件：if/while 的 condition 字段
        if t == "if_statement":
            cond = n.child_by_field_name("condition")
            if cond:
                spans.append((cond.start_byte, cond.end_byte, "cond"))
        if t == "while_statement":
            cond = n.child_by_field_name("condition")
            if cond:
                spans.append((cond.start_byte, cond.end_byte, "cond"))

        # 2) for 头（Python：从 for 节点起到 body 起点）
        if t == "for_statement":
            body = n.child_by_field_name("body")
            if body:
                spans.append((n.start_byte, body.start_byte, "loop-header"))

        # 3) 方法调用整体（整颗 call 节点）
        if t == "call":
            spans.append((n.start_byte, n.end_byte, "call"))

    # 去重（按字节区间+类型）
    seen = set()
    out = []
    for s in spans:
        if s not in seen:
            seen.add(s)
            out.append(s)
    return out

def _collect_sites_java(code: str, tree) -> List[Tuple[int, int, str]]:
    """
    Return list of (start_byte, end_byte, kind), where kind in {"cond", "loop-header", "call"}.
    """
    root = tree.root_node
    spans: List[Tuple[int, int, str]] = []

    for n in _walk(root):
        t = n.type

        # 1) 条件：if/while/do 的 condition；switch 的 expression
        if t in ("if_statement", "while_statement", "do_statement"):
            cond = n.child_by_field_name("condition")
            if cond:
                spans.append((cond.start_byte, cond.end_byte, "cond"))
        if t in ("switch_expression", "switch_statement"):
            expr = n.child_by_field_name("expression")
            if expr:
                spans.append((expr.start_byte, expr.end_byte, "cond"))

        # 2) for 头（Java：括号内部整体）
        if t in ("for_statement", "enhanced_for_statement"):
            start_b, end_b = _find_paren_inner_span(code, n.start_byte, n.end_byte)
            if start_b is not None and end_b is not None and start_b <= end_b:
                spans.append((start_b, end_b, "loop-header"))

        # 3) 方法调用整体
        if t == "method_invocation":
            spans.append((n.start_byte, n.end_byte, "call"))

    # 去重
    seen = set()
    out = []
    for s in spans:
        if s not in seen:
            seen.add(s)
            out.append(s)
    return out

def _find_paren_inner_span(code: str, start_byte: int, end_byte: int) -> Tuple[Optional[int], Optional[int]]:
    """Find the first balanced (...) inside [start_byte, end_byte) and return inner byte-span (without parens)."""
    text = code[start_byte:end_byte]
    base = start_byte
    depth = 0
    lpos = None
    for i, ch in enumerate(text):
        if ch == '(':
            if depth == 0:
                lpos = i
            depth += 1
        elif ch == ')':
            depth -= 1
            if depth == 0 and lpos is not None:
                return base + lpos + 1, base + i
    return None, None

# ------------ public functions (single-arg, return 0-based line numbers) ------------
def find_placeholder_lines_python(file_code: str) -> List[int]:
    """
    输入：Python 源文件全文字符串
    返回：所有占位符（条件 / for 头 / 方法调用整体）覆盖到的 0-based 行号（升序、去重）
    """
    _, parser = get_language_and_parser("python")
    tree, *_ = parse_code(file_code, parser)
    spans = _collect_sites_python(file_code, tree)

    lines: Set[int] = set()
    for start_b, end_b, _kind in spans:
        s, e = _span_bytes_to_line_range(file_code, start_b, end_b)
        for ln in range(s, e + 1):
            lines.add(ln)
    return sorted(lines)

def find_placeholder_lines_java(file_code: str) -> List[int]:
    """
    输入：Java 源文件全文字符串
    返回：所有占位符（条件 / for 头 / 方法调用整体）覆盖到的 0-based 行号（升序、去重）
    """
    _, parser = get_language_and_parser("java")
    tree, *_ = parse_code(file_code, parser)
    spans = _collect_sites_java(file_code, tree)

    lines: Set[int] = set()
    for start_b, end_b, _kind in spans:
        s, e = _span_bytes_to_line_range(file_code, start_b, end_b)
        for ln in range(s, e + 1):
            lines.add(ln)
    return sorted(lines)
