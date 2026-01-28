from __future__ import annotations

import ast
from typing import List

from ..context import CheckContext
from ..models import Issue
from ..snippet import make_snippet, node_span

_TARGETS = {"snapshot", "ensure"}

def run(ctx: CheckContext) -> List[Issue]:
    issues: List[Issue] = []

    for dec in ctx.fn_node.decorator_list:
        if not isinstance(dec, ast.Call):
            continue

        fn = dec.func

        # Case 1: @snapshot(...) / @ensure(...)  (NOT allowed)
        if isinstance(fn, ast.Name) and fn.id.lower() in _TARGETS:
            line, col = node_span(fn)
            snippet, caret = make_snippet(ctx.lines, line, col)
            issues.append(Issue(
                code="IC008",
                rule="Decorator must be icontract-qualified",
                message=(
                    f"Decorator '@{fn.id}(...)' is not allowed. "
                    f"Use '@icontract.{fn.id.lower()}(...)' instead."
                ),
                line=line, col=col, snippet=snippet, caret=caret
            ))
            continue

        # Case 2: @icontract.Snapshot(...) / @icontract.Ensure(...) (wrong case)
        if isinstance(fn, ast.Attribute) and isinstance(fn.value, ast.Name) and fn.value.id == "icontract":
            if fn.attr.lower() in _TARGETS and fn.attr not in _TARGETS:
                line, col = node_span(fn)
                snippet, caret = make_snippet(ctx.lines, line, col)
                issues.append(Issue(
                    code="IC008",
                    rule="Decorator must be icontract-qualified",
                    message=(
                        f"Decorator '@icontract.{fn.attr}(...)' has incorrect casing. "
                        f"Use '@icontract.{fn.attr.lower()}(...)'."
                    ),
                    line=line, col=col, snippet=snippet, caret=caret
                ))
            continue

        # Case 3: @something.snapshot(...) / @something.ensure(...) (NOT allowed)
        if isinstance(fn, ast.Attribute) and fn.attr in _TARGETS:
            # if it's not icontract.snapshot/ensure, complain
            ok = isinstance(fn.value, ast.Name) and fn.value.id == "icontract"
            if not ok:
                line, col = node_span(fn)
                snippet, caret = make_snippet(ctx.lines, line, col)
                issues.append(Issue(
                    code="IC008",
                    rule="Decorator must be icontract-qualified",
                    message=(
                        f"Decorator must be '@icontract.{fn.attr}(...)'. "
                        f"Other forms (e.g., '@{ast.unparse(fn)}(...)') are not allowed."
                    ),
                    line=line, col=col, snippet=snippet, caret=caret
                ))

    return issues
