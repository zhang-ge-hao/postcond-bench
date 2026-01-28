from __future__ import annotations

import ast
from typing import List, Tuple


def linecol_from_index(text: str, idx: int) -> Tuple[int, int]:
    # returns 1-based line, 0-based col
    line = 1
    col = 0
    for i, ch in enumerate(text):
        if i == idx:
            return line, col
        if ch == "\n":
            line += 1
            col = 0
        else:
            col += 1
    return line, col  # idx at EOF


def make_snippet(lines: List[str], line: int, col: int) -> Tuple[str, str]:
    i = max(1, line) - 1
    if i < 0 or i >= len(lines):
        return "", ""
    snippet = lines[i].rstrip("\n")
    caret = (" " * col) + "^"
    return snippet, caret


def node_span(node: ast.AST) -> Tuple[int, int]:
    line = getattr(node, "lineno", 1)
    col = getattr(node, "col_offset", 0)
    return int(line), int(col)
