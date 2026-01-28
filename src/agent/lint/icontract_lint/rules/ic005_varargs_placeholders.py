from __future__ import annotations

import ast
from typing import List

from ..ast_utils import get_first_positional_arg, is_lambda, lambda_param_names
from ..context import CheckContext
from ..models import Issue
from ..snippet import make_snippet, node_span


def run(ctx: CheckContext) -> List[Issue]:
    issues: List[Issue] = []

    for call in ctx.ensure_calls:
        first = get_first_positional_arg(call)
        if not (first and is_lambda(first)):
            continue
        lam: ast.Lambda = first  # type: ignore[assignment]
        lam_names, lam_vararg, lam_kwarg = lambda_param_names(lam)

        if ctx.fn_vararg is not None:
            bad = []
            if ctx.fn_vararg in lam_names:
                bad.append(ctx.fn_vararg)
            if lam_vararg == ctx.fn_vararg:
                bad.append(f"*{ctx.fn_vararg}")
            if bad:
                line, col = node_span(lam)
                snippet, caret = make_snippet(ctx.lines, line, col)
                issues.append(Issue(
                    code="IC005",
                    rule="Varargs placeholders",
                    message=(
                        f"The function defines variable positional arguments (*{ctx.fn_vararg}), so the contract should not "
                        f"bind '{ctx.fn_vararg}' in the ensure lambda signature. "
                        f"Prefer the placeholder '_ARGS' and refer to positional call arguments via _ARGS[...] as described in the docs."
                    ),
                    line=line, col=col, snippet=snippet, caret=caret
                ))

        if ctx.fn_kwarg is not None:
            bad = []
            if ctx.fn_kwarg in lam_names:
                bad.append(ctx.fn_kwarg)
            if lam_kwarg == ctx.fn_kwarg:
                bad.append(f"**{ctx.fn_kwarg}")
            if bad:
                line, col = node_span(lam)
                snippet, caret = make_snippet(ctx.lines, line, col)
                issues.append(Issue(
                    code="IC005",
                    rule="Varargs placeholders",
                    message=(
                        f"The function defines variable keyword arguments (**{ctx.fn_kwarg}), so the contract should not "
                        f"bind '{ctx.fn_kwarg}' in the ensure lambda signature. "
                        f"Prefer the placeholder '_KWARGS' and refer to keyword call arguments via _KWARGS[...] as described in the docs."
                    ),
                    line=line, col=col, snippet=snippet, caret=caret
                ))

    return issues
