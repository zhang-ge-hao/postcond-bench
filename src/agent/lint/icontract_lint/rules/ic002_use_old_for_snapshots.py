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

    for call in ctx.ensure_calls:
        first = get_first_positional_arg(call)
        if not (first and is_lambda(first)):
            continue

        lam: ast.Lambda = first  # type: ignore[assignment]
        lam_names, _, _ = lambda_param_names(lam)

        for name in lam_names:
            if name in _ALLOWED_SPECIAL:
                continue
            if name not in ctx.func_params and name in ctx.snapshot_props:
                line, col = node_span(lam)
                snippet, caret = make_snippet(ctx.lines, line, col)
                issues.append(Issue(
                    code="IC002",
                    rule="Use OLD for snapshots",
                    message=(
                        f"ensure lambda binds '{name}', which matches a snapshot property. "
                        f"This is not how icontract snapshots are provided. "
                        f"Use 'OLD' as a parameter and access the snapshot as OLD.{name} "
                        f"(e.g., lambda OLD, ...: ... OLD.{name} ...)."
                    ),
                    line=line, col=col, snippet=snippet, caret=caret
                ))

    return issues
