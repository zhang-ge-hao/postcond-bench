from __future__ import annotations

import ast
from typing import List

from ..ast_utils import snapshot_declared_name
from ..context import CheckContext
from ..models import Issue
from ..snippet import make_snippet, node_span


def run(ctx: CheckContext) -> List[Issue]:
    issues: List[Issue] = []

    for call in ctx.snapshot_calls:
        # 如果完全无法推导 name（比如 lambda 有0或>1参数且没给 name），这是更严重的问题
        inferred = snapshot_declared_name(call)
        if inferred is None:
            line, col = node_span(call)
            snippet, caret = make_snippet(ctx.lines, line, col)
            issues.append(Issue(
                code="IC009",
                rule="Snapshot name",
                message=(
                    "snapshot name could not be determined. "
                    "Provide name=\"...\" (recommended) or pass a single-parameter capture lambda so it can be inferred."
                ),
                line=line, col=col, snippet=snippet, caret=caret
            ))
            continue

        # 如果不是用 keyword name=，给一个“风格提示”（仍然是 Issue，但语义上是推荐）
        has_name_kw = any(kw.arg == "name" for kw in call.keywords)
        if not has_name_kw:
            line, col = node_span(call)
            snippet, caret = make_snippet(ctx.lines, line, col)
            issues.append(Issue(
                code="IC009",
                rule="Snapshot name style",
                message=(
                    f"snapshot name is resolved as '{inferred}', but for readability it is recommended to write it explicitly "
                    f"as name=\"{inferred}\" (instead of omitting it or passing it positionally)."
                ),
                line=line, col=col, snippet=snippet, caret=caret
            ))

    return issues
