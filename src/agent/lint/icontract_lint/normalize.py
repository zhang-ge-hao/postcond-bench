from __future__ import annotations

import re
from typing import Tuple


def _dedent_preserve_relative(code: str) -> str:
    """
    Dedent code by removing the common leading indentation across all non-empty lines.
    Similar to textwrap.dedent, but implemented explicitly and stable for mixed whitespace.

    - Ignores empty/blank lines.
    - Preserves relative indentation inside the snippet.
    """
    if not code:
        return code

    lines = code.splitlines(True)

    # Find minimal indent among non-blank lines
    indents = []
    for ln in lines:
        if ln.strip() == "":
            continue
        # leading whitespace
        m = re.match(r"[ \t]*", ln)
        indents.append(len(m.group(0)) if m else 0)

    if not indents:
        return code

    min_indent = min(indents)

    if min_indent == 0:
        return code

    # Remove min_indent spaces/tabs *as characters* from each non-blank line
    out = []
    for ln in lines:
        if ln.strip() == "":
            out.append(ln)
        else:
            out.append(ln[min_indent:])
    return "".join(out)


def normalize_post_and_method(postconditions_src: str, method_src: str) -> Tuple[str, str]:
    """
    Normalize two snippets so that they can be concatenated and parsed as a module.

    - Dedent method_src (common for class-indented method snippet).
    - Also dedent postconditions_src defensively.
    - Ensure there's exactly one newline between them when concatenated by caller.
    """
    post = postconditions_src.rstrip("\n")
    method = method_src.rstrip("\n")

    # Most of the time postconditions are already top-level, but we dedent anyway for robustness
    post = _dedent_preserve_relative(post)

    # Method is often indented; dedent is essential
    method = _dedent_preserve_relative(method)

    return post, method
