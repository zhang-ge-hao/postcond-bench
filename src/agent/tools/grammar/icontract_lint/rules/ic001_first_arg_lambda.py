from __future__ import annotations

import ast
from typing import List

from ..ast_utils import get_first_positional_arg, is_lambda
from ..context import CheckContext
from ..models import Issue
from ..snippet import make_snippet, node_span


def run(ctx: CheckContext) -> List[Issue]:
    issues: List[Issue] = []

    def check_call(call: ast.Call, kind: str) -> None:
        first = get_first_positional_arg(call)
        if first is None:
            line, col = node_span(call)
            snippet, caret = make_snippet(ctx.lines, line, col)
            issues.append(Issue(
                code="IC001",
                rule="First argument must be lambda",
                message=f"@icontract.{kind}(...) must receive a lambda as its first positional argument, but no positional argument was provided.",
                line=line, col=col, snippet=snippet, caret=caret
            ))
            return
        if not is_lambda(first):
            line, col = node_span(first)
            snippet, caret = make_snippet(ctx.lines, line, col)
            issues.append(Issue(
                code="IC001",
                rule="First argument must be lambda",
                message=f"@icontract.{kind}(...) first positional argument must be a lambda expression, but found {type(first).__name__}.",
                line=line, col=col, snippet=snippet, caret=caret
            ))

    for call in ctx.snapshot_calls:
        check_call(call, "snapshot")
    for call in ctx.ensure_calls:
        check_call(call, "ensure")

    return issues
