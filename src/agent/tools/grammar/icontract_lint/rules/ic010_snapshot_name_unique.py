from __future__ import annotations

import ast
from typing import Dict, List, Optional

from ..ast_utils import snapshot_declared_name
from ..context import CheckContext
from ..models import Issue
from ..snippet import make_snippet, node_span

def run(ctx: CheckContext) -> List[Issue]:
    issues: List[Issue] = []
    seen: Dict[str, ast.AST] = {}

    for call in ctx.snapshot_calls:
        name = snapshot_declared_name(call)
        if name is None:
            # 让 IC009 去报“无法推导 name”
            continue

        if name in seen:
            line, col = node_span(call)
            snippet, caret = make_snippet(ctx.lines, line, col)
            issues.append(Issue(
                code="IC010",
                rule="Snapshot name conflicts",
                message=f"snapshot name '{name}' is duplicated. Snapshot names must be unique.",
                line=line, col=col, snippet=snippet, caret=caret
            ))
        else:
            seen[name] = call

    return issues
