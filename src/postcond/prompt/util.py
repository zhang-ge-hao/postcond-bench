

from src.ds import *
from src.util import (
    parse_code, 
    get_language_and_parser
)
from src.method.static import (
    iter_method_ts_node,
    get_method
)

def remove_method_bodies(
        code_str: str, 
        code_path: str, 
        repo: Repo, 
        lang: str) -> str:
    omit = "..."
    _, parser = get_language_and_parser(lang)
    tree, code_str, code_bytes = parse_code(code_str, parser)
    body_lines = set()
    for method_ts_node in iter_method_ts_node(tree, lang):
        method = get_method(method_ts_node, code_str, 
                            code_bytes, code_path, repo,
                            apply_restriction=False)
        if method is not None:
            for line in range(method.body_start_line, method.end_line + 1):
                body_lines.add(line - 1)
    ret_lines = []
    for line_idx, line in enumerate(code_str.split("\n")):
        if line_idx not in body_lines:
            if not line.strip() and (ret_lines and ret_lines[-1] == omit):
                continue
            ret_lines.append(line)
        elif ret_lines and ret_lines[-1] == omit:
            continue
        else:
            ret_lines.append(omit)
    return "\n".join(ret_lines)

def remove_all_comments(code_str: str, lang: str) -> str:
    _, parser = get_language_and_parser(lang)
    tree, code_str, code_bytes = parse_code(code_str, parser)

    # ---------- helpers ----------
    def iter_nodes(root):
        stack = [root]
        while stack:
            n = stack.pop()
            yield n
            for ch in reversed(getattr(n, "children", []) or []):
                stack.append(ch)

    def is_word_byte(b: int) -> bool:
        # [A-Za-z0-9_]
        return (48 <= b <= 57) or (65 <= b <= 90) or (97 <= b <= 122) or b == 95

    def merge_ranges(ranges: list[tuple[int, int]]) -> list[tuple[int, int]]:
        if not ranges:
            return []
        ranges.sort()
        merged = [ranges[0]]
        for s, e in ranges[1:]:
            ps, pe = merged[-1]
            if s <= pe:
                merged[-1] = (ps, max(pe, e))
            else:
                merged.append((s, e))
        return merged

    # line start offsets
    line_starts = [0]
    for i, b in enumerate(code_bytes):
        if b == 10:  # \n
            line_starts.append(i + 1)

    nbytes = len(code_bytes)

    def byte_to_line(idx: int) -> int:
        # rightmost line_start <= idx
        import bisect

        if idx < 0:
            return 0
        if idx >= nbytes:
            return len(line_starts) - 1
        return bisect.bisect_right(line_starts, idx) - 1

    def line_bounds(line_idx: int) -> tuple[int, int, int]:
        """
        return (ls, le_no_nl, le_with_nl)
        """
        ls = line_starts[line_idx]
        if line_idx + 1 < len(line_starts):
            le_with_nl = line_starts[line_idx + 1]
            le_no_nl = le_with_nl - 1  # exclude '\n'
        else:
            le_with_nl = nbytes
            le_no_nl = nbytes
        return ls, le_no_nl, le_with_nl

    def is_whitespace_only(bs: bytes) -> bool:
        return bs.strip(b" \t\r") == b""

    # ---------- collect removable nodes (raw ranges) ----------
    removable_nodes: list[tuple[int, int]] = []

    # 1) comments (python/java)
    for node in iter_nodes(tree.root_node):
        t = node.type or ""
        if t == "comment" or "comment" in t:
            if node.end_byte > node.start_byte:
                removable_nodes.append((node.start_byte, node.end_byte))

    # 2) python: remove all lonely string statements
    if lang.lower() == "python":
        def is_lonely_string_expr_stmt(n) -> bool:
            if (n.type or "") != "expression_statement":
                return False
            named = [c for c in n.children if getattr(c, "is_named", False)]
            if len(named) != 1:
                return False
            et = named[0].type or ""
            return "string" in et  # string / string_literal / concatenated_string ...

        for node in iter_nodes(tree.root_node):
            if is_lonely_string_expr_stmt(node):
                removable_nodes.append((node.start_byte, node.end_byte))

    if not removable_nodes:
        return code_str

    # ---------- expand to full-line deletion when it would leave an empty line ----------
    expanded: list[tuple[int, int]] = []
    for s, e in removable_nodes:
        # clamp
        s = max(0, min(s, nbytes))
        e = max(0, min(e, nbytes))
        if e <= s:
            continue

        start_line = byte_to_line(s)
        end_line = byte_to_line(e - 1)

        ls, _le_no_nl, _le_with_nl = line_bounds(start_line)
        _ls2, le_no_nl2, le_with_nl2 = line_bounds(end_line)

        # Check "standalone on its line(s)":
        # - before start in start line: only whitespace
        # - after end in end line: only whitespace
        before = code_bytes[ls:s]
        after = code_bytes[e:le_no_nl2]
        standalone = is_whitespace_only(before) and is_whitespace_only(after)

        if standalone:
            # delete whole lines covering it, including trailing newline if exists
            expanded.append((ls, le_with_nl2))
        else:
            expanded.append((s, e))

    ranges = merge_ranges(expanded)
    if not ranges:
        return code_str

    # ---------- apply deletions (do NOT preserve original newlines) ----------
    out = bytearray()
    cur = 0

    for s, e in ranges:
        if s > cur:
            out.extend(code_bytes[cur:s])

        # If deleting may glue two identifiers, insert a space
        prev_b = out[-1] if out else None
        next_b = code_bytes[e] if e < nbytes else None
        if prev_b is not None and next_b is not None and is_word_byte(prev_b) and is_word_byte(next_b):
            out.extend(b" ")

        cur = e

    if cur < nbytes:
        out.extend(code_bytes[cur:])

    return out.decode("utf-8", errors="replace")
