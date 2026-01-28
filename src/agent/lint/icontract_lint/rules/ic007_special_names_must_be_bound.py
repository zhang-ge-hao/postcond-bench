from __future__ import annotations

import ast
from typing import List, Set

from ..ast_utils import get_first_positional_arg, is_lambda, lambda_param_names, loaded_names
from ..context import CheckContext
from ..models import Issue
from ..snippet import make_snippet, node_span

SPECIAL: Set[str] = {"result", "OLD", "_ARGS", "_KWARGS"}

def run(ctx: CheckContext) -> List[Issue]:
    issues: List[Issue] = []

    def check_lambda(lam: ast.Lambda, kind: str) -> None:
        lam_names, _, _ = lambda_param_names(lam)
        used = loaded_names(lam.body)
        missing = sorted((used & SPECIAL) - set(lam_names))
        if missing:
            line, col = node_span(lam)
            snippet, caret = make_snippet(ctx.lines, line, col)
            issues.append(Issue(
                code="IC007",
                rule="Bind special names",
                message=(
                    f"{kind} lambda references special name(s) {missing}, "
                    f"but does not declare them in the lambda signature. "
                    f"Bind them explicitly in the parameter list."
                ),
                line=line, col=col, snippet=snippet, caret=caret
            ))

    # snapshot lambdas
    for call in ctx.snapshot_calls:
        first = get_first_positional_arg(call)
        if first and is_lambda(first):
            check_lambda(first, "snapshot")

    # ensure lambdas
    for call in ctx.ensure_calls:
        first = get_first_positional_arg(call)
        if first and is_lambda(first):
            check_lambda(first, "ensure")

    return issues
