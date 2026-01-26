from __future__ import annotations

import ast
from typing import List, Set

from ..ast_utils import get_first_positional_arg, is_lambda, lambda_param_names
from ..context import CheckContext
from ..models import Issue
from ..snippet import make_snippet, node_span


_ALLOWED_SPECIAL: Set[str] = {"result", "OLD", "_ARGS", "_KWARGS"}


def run(ctx: CheckContext) -> List[Issue]:
    issues: List[Issue] = []

    # Snapshot: params must be subset of function params; disallow *args/**kwargs in lambda signature
    for call in ctx.snapshot_calls:
        first = get_first_positional_arg(call)
        if not (first and is_lambda(first)):
            continue
        lam: ast.Lambda = first  # type: ignore[assignment]
        lam_names, lam_vararg, lam_kwarg = lambda_param_names(lam)

        for name in lam_names:
            if name not in ctx.func_params:
                line, col = node_span(lam)
                snippet, caret = make_snippet(ctx.lines, line, col)
                issues.append(Issue(
                    code="IC003",
                    rule="Snapshot lambda parameters",
                    message=(
                        f"snapshot capture lambda parameter '{name}' is not a parameter of the decorated function. "
                        f"Snapshot capture functions must accept only a subset of the function parameters."
                    ),
                    line=line, col=col, snippet=snippet, caret=caret
                ))

        if lam_vararg is not None or lam_kwarg is not None:
            line, col = node_span(lam)
            snippet, caret = make_snippet(ctx.lines, line, col)
            issues.append(Issue(
                code="IC003",
                rule="Snapshot lambda parameters",
                message=(
                    "snapshot capture lambda should not use *args/**kwargs in its signature. "
                    "Use explicit parameter names from the function signature instead."
                ),
                line=line, col=col, snippet=snippet, caret=caret
            ))

    # Ensure: params must be function params OR special; disallow *args/**kwargs in lambda signature
    for call in ctx.ensure_calls:
        first = get_first_positional_arg(call)
        if not (first and is_lambda(first)):
            continue
        lam: ast.Lambda = first  # type: ignore[assignment]
        lam_names, lam_vararg, lam_kwarg = lambda_param_names(lam)

        for name in lam_names:
            if name in _ALLOWED_SPECIAL:
                continue
            if name not in ctx.func_params and name not in ctx.snapshot_props:
                line, col = node_span(lam)
                snippet, caret = make_snippet(ctx.lines, line, col)
                issues.append(Issue(
                    code="IC003",
                    rule="Ensure lambda parameters",
                    message=(
                        f"ensure lambda parameter '{name}' is neither a function parameter nor a special name "
                        f"({', '.join(sorted(_ALLOWED_SPECIAL))})."
                    ),
                    line=line, col=col, snippet=snippet, caret=caret
                ))

        if lam_vararg is not None or lam_kwarg is not None:
            line, col = node_span(lam)
            snippet, caret = make_snippet(ctx.lines, line, col)
            issues.append(Issue(
                code="IC003",
                rule="Ensure lambda parameters",
                message=(
                    "ensure lambda should not use *args/**kwargs in its signature. "
                    "Bind explicit parameter names, or use placeholders '_ARGS'/'_KWARGS' when referring to call arguments."
                ),
                line=line, col=col, snippet=snippet, caret=caret
            ))

    return issues
