from __future__ import annotations

from typing import List, Tuple

from .snippet import linecol_from_index

_BR_OPEN = {"(": ")", "[": "]", "{": "}"}
_BR_CLOSE = {")": "(", "]": "[", "}": "{"}


def check_bracket_matching(code: str) -> List[Tuple[int, int, str]]:
    """
    Return list of (line, col, message) for bracket mismatches.
    Ignores brackets in strings and comments.
    """
    issues: List[Tuple[int, int, str]] = []
    stack: List[Tuple[str, int]] = []  # (opening_char, absolute_index)

    i = 0
    n = len(code)

    in_str = False
    str_quote = ""          # one of ', ", ''' or """
    triple = False
    escape = False

    def startswith_at(s: str, pos: int) -> bool:
        return code.startswith(s, pos)

    while i < n:
        ch = code[i]

        # comment start (#) when not in string
        if not in_str and ch == "#":
            while i < n and code[i] != "\n":
                i += 1
            continue

        # string start/end
        if not in_str:
            if startswith_at("'''", i) or startswith_at('"""', i):
                in_str = True
                triple = True
                str_quote = code[i:i+3]
                i += 3
                continue
            if ch == "'" or ch == '"':
                in_str = True
                triple = False
                str_quote = ch
                i += 1
                continue
        else:
            if escape:
                escape = False
                i += 1
                continue
            if ch == "\\":
                escape = True
                i += 1
                continue

            if triple:
                if startswith_at(str_quote, i):
                    in_str = False
                    triple = False
                    str_quote = ""
                    i += 3
                    continue
            else:
                if ch == str_quote:
                    in_str = False
                    str_quote = ""
                    i += 1
                    continue

            i += 1
            continue

        # Not in string/comment => process brackets
        if ch in _BR_OPEN:
            stack.append((ch, i))
        elif ch in _BR_CLOSE:
            if not stack:
                line, col = linecol_from_index(code, i)
                issues.append((line, col, f"Unmatched closing bracket '{ch}'."))
            else:
                top, top_idx = stack[-1]
                if _BR_CLOSE[ch] != top:
                    line, col = linecol_from_index(code, i)
                    exp = _BR_OPEN[top]
                    issues.append((line, col, f"Mismatched bracket: got '{ch}', expected '{exp}' to close '{top}'."))
                else:
                    stack.pop()

        i += 1

    for top, top_idx in stack:
        line, col = linecol_from_index(code, top_idx)
        issues.append((line, col, f"Unmatched opening bracket '{top}'."))
    return issues
