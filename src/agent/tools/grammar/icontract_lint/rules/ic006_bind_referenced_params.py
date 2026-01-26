from __future__ import annotations

import ast
from typing import List, Set

from ..ast_utils import get_first_positional_arg, is_lambda, lambda_param_names, loaded_names
from ..context import CheckContext
from ..models import Issue
from ..snippet import make_snippet, node_span

_ALLOWED_SPECIAL: Set[str] = {"result", "OLD", "_ARGS", "_KWARGS"}


def run(ctx: CheckContext) -> List[Issue]:
    issues: List[Issue] = []

    # Snapshots
    for call in ctx.snapshot_calls:
        first = get_first_positional_arg(call)
        if not (first and is_lambda(first)):
            continue
        lam: ast.Lambda = first  # type: ignore[assignment]
        lam_names, _, _ = lambda_param_names(lam)

        used = loaded_names(lam.body)
        missing = (used & ctx.func_params) - set(lam_names)
        if missing:
            line, col = node_span(lam)
            snippet, caret = make_snippet(ctx.lines, line, col)
            missing_list = ", ".join(sorted(missing))
            issues.append(Issue(
                code="IC006",
                rule="Bind referenced parameters",
                message=(
                    f"snapshot capture lambda references function parameter(s) [{missing_list}] in its body, "
                    f"but does not declare them in the lambda signature. "
                    f"In icontract, snapshot capture functions receive the original function arguments via their parameters; "
                    f"declare the needed parameters explicitly (e.g., lambda {missing_list}: ...)."
                ),
                line=line, col=col, snippet=snippet, caret=caret
            ))

    # Ensures
    for call in ctx.ensure_calls:
        first = get_first_positional_arg(call)
        if not (first and is_lambda(first)):
            continue
        lam: ast.Lambda = first  # type: ignore[assignment]
        lam_names, _, _ = lambda_param_names(lam)

        used = loaded_names(lam.body)
        missing = (used & ctx.func_params) - set(lam_names) - _ALLOWED_SPECIAL
        if missing:
            line, col = node_span(lam)
            snippet, caret = make_snippet(ctx.lines, line, col)
            missing_list = ", ".join(sorted(missing))
            issues.append(Issue(
                code="IC006",
                rule="Bind referenced parameters",
                message=(
                    f"ensure lambda references function parameter(s) [{missing_list}] in its body, "
                    f"but does not declare them in the lambda signature. "
                    f"In icontract, postcondition functions receive the original function arguments via their parameters; "
                    f"declare the needed parameters explicitly (e.g., lambda result, {missing_list}: ...)."
                ),
                line=line, col=col, snippet=snippet, caret=caret
            ))

        # Optional hint: varargs/kwargs referenced in body should use placeholders
        if ctx.fn_vararg is not None and ctx.fn_vararg in used and "_ARGS" not in set(lam_names):
            line, col = node_span(lam)
            snippet, caret = make_snippet(ctx.lines, line, col)
            issues.append(Issue(
                code="IC006",
                rule="Bind referenced parameters",
                message=(
                    f"ensure lambda references '*{ctx.fn_vararg}' in its body. "
                    f"When the function defines *{ctx.fn_vararg}, prefer binding the placeholder '_ARGS' "
                    f"and refer to positional call arguments via _ARGS[...]."
                ),
                line=line, col=col, snippet=snippet, caret=caret
            ))

        if ctx.fn_kwarg is not None and ctx.fn_kwarg in used and "_KWARGS" not in set(lam_names):
            line, col = node_span(lam)
            snippet, caret = make_snippet(ctx.lines, line, col)
            issues.append(Issue(
                code="IC006",
                rule="Bind referenced parameters",
                message=(
                    f"ensure lambda references '**{ctx.fn_kwarg}' in its body. "
                    f"When the function defines **{ctx.fn_kwarg}, prefer binding the placeholder '_KWARGS' "
                    f"and refer to keyword call arguments via _KWARGS[...]."
                ),
                line=line, col=col, snippet=snippet, caret=caret
            ))

    return issues
