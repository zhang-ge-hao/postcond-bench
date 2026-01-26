from __future__ import annotations

import ast
from typing import List

from .context import build_context
from .models import Issue
from .rules import run_pre_rules, run_rules
from .snippet import make_snippet
from .normalize import normalize_post_and_method  # 新增


def check_icontract_postconditions(method_src: str, postconditions_src: str) -> List[Issue]:
    """
    Validate icontract snapshot/ensure decorators for a single method.

    Returns a list of Issues (English messages, with line/col and snippet).
    """
    post_norm, method_norm = normalize_post_and_method(postconditions_src, method_src)
    combined = (post_norm.rstrip() + "\n" + method_norm.rstrip()).rstrip() + "\n"
    lines = combined.splitlines(True)

    issues: List[Issue] = []

    # Pre-parse rules (e.g., bracket matching)
    issues.extend(run_pre_rules(combined, lines))

    # AST parse
    try:
        tree = ast.parse(combined)
    except SyntaxError as e:
        line = int(e.lineno or 1)
        col = int(e.offset or 0)
        snippet, caret = make_snippet(lines, line, col)
        issues.append(Issue(
            code="IC000",
            rule="Python syntax",
            message=f"Python syntax error while parsing the provided code: {e.msg}.",
            line=line,
            col=col,
            snippet=snippet,
            caret=caret
        ))
        return issues

    ctx = build_context(combined, lines, tree)
    if ctx is None:
        issues.append(Issue(
            code="IC000",
            rule="Missing function",
            message="No function definition (def ...) was found in the provided method source.",
            line=1,
            col=0
        ))
        return issues

    # Run rule set
    issues.extend(run_rules(ctx))
    return issues


def format_issues(issues: List[Issue]) -> str:
    if not issues:
        return "No issues found."
    return "\n\n".join(issue.format() for issue in issues)


def grammar_verify(method: str, postconds: str) -> str:
    issues = check_icontract_postconditions(method, postconds)
    return format_issues(issues)
