from __future__ import annotations

import ast
from typing import Dict, List, Optional, Set

from ..ast_utils import get_first_positional_arg, is_lambda
from ..context import CheckContext
from ..models import Issue
from ..snippet import make_snippet, node_span

def _snapshot_names(ctx: CheckContext) -> Set[str]:
    out: Set[str] = set()
    for call in ctx.snapshot_calls:
        for kw in call.keywords:
            if kw.arg == "name" and isinstance(kw.value, ast.Constant) and isinstance(kw.value.value, str):
                out.add(kw.value.value)
    return out

def _build_parent_map(root: ast.AST) -> Dict[ast.AST, ast.AST]:
    parent: Dict[ast.AST, ast.AST] = {}
    for p in ast.walk(root):
        for c in ast.iter_child_nodes(p):
            parent[c] = p
    return parent

def run(ctx: CheckContext) -> List[Issue]:
    issues: List[Issue] = []
    snap_names = set(ctx.snapshot_props.keys())

    for call in ctx.ensure_calls:
        first = get_first_positional_arg(call)
        if not (first and is_lambda(first)):
            continue
        lam: ast.Lambda = first  # type: ignore[assignment]

        parent = _build_parent_map(lam.body)

        for node in ast.walk(lam.body):
            # 1) forbid OLD["xxx"]
            if isinstance(node, ast.Subscript) and isinstance(node.value, ast.Name) and node.value.id == "OLD":
                line, col = node_span(node)
                snippet, caret = make_snippet(ctx.lines, line, col)
                issues.append(Issue(
                    code="IC011",
                    rule="OLD usage",
                    message="OLD must be accessed as 'OLD.<name>', not as subscripting (e.g., OLD[\"name\"]).",
                    line=line, col=col, snippet=snippet, caret=caret
                ))

            # 2) check OLD.xxx where xxx must be defined snapshot name
            if isinstance(node, ast.Attribute) and isinstance(node.value, ast.Name) and node.value.id == "OLD":
                attr = node.attr
                if attr not in snap_names:
                    line, col = node_span(node)
                    snippet, caret = make_snippet(ctx.lines, line, col)
                    issues.append(Issue(
                        code="IC011",
                        rule="OLD usage",
                        message=(
                            f"OLD.{attr} is used, but snapshot name '{attr}' is not defined. "
                            f"Define it via @icontract.snapshot(..., name=\"{attr}\")."
                        ),
                        line=line, col=col, snippet=snippet, caret=caret
                    ))

            # 3) OLD name must not be used “bare” (must be OLD.xxx)
            if isinstance(node, ast.Name) and node.id == "OLD" and isinstance(node.ctx, ast.Load):
                p = parent.get(node)
                ok = isinstance(p, ast.Attribute) and p.value is node  # OLD as value of Attribute
                if not ok:
                    line, col = node_span(node)
                    snippet, caret = make_snippet(ctx.lines, line, col)
                    issues.append(Issue(
                        code="IC011",
                        rule="OLD usage",
                        message="OLD can only be used as 'OLD.<name>' (attribute access).",
                        line=line, col=col, snippet=snippet, caret=caret
                    ))

    return issues
