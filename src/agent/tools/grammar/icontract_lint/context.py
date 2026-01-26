from __future__ import annotations

import ast
from dataclasses import dataclass
from typing import Dict, List, Optional, Set

from .ast_utils import decorator_kind, derive_snapshot_props, func_param_names

def _find_first_function(node: ast.AST) -> Optional[ast.FunctionDef | ast.AsyncFunctionDef]:
    """
    Find the first function definition in source order.
    - Prefer module-level functions
    - If not present, look into classes (methods), including @property/@staticmethod cases
    """
    if isinstance(node, ast.Module):
        # 1) module-level first
        for stmt in node.body:
            if isinstance(stmt, (ast.FunctionDef, ast.AsyncFunctionDef)):
                return stmt
        # 2) otherwise search into classes in order
        for stmt in node.body:
            if isinstance(stmt, ast.ClassDef):
                for cstmt in stmt.body:
                    if isinstance(cstmt, (ast.FunctionDef, ast.AsyncFunctionDef)):
                        return cstmt
        # 3) fallback: any nested (rare)
        for sub in ast.walk(node):
            if isinstance(sub, (ast.FunctionDef, ast.AsyncFunctionDef)):
                return sub
        return None
    # generic fallback
    for sub in ast.walk(node):
        if isinstance(sub, (ast.FunctionDef, ast.AsyncFunctionDef)):
            return sub
    return None


@dataclass(frozen=True)
class CheckContext:
    combined: str
    lines: List[str]

    tree: ast.AST
    fn_node: ast.FunctionDef | ast.AsyncFunctionDef

    func_params: Set[str]
    fn_vararg: Optional[str]
    fn_kwarg: Optional[str]

    snapshot_calls: List[ast.Call]
    ensure_calls: List[ast.Call]
    snapshot_props: Dict[str, ast.Call]


def build_context(combined: str, lines: List[str], tree: ast.AST) -> Optional[CheckContext]:
    fn_node = _find_first_function(tree)
    if fn_node is None:
        return None

    func_params, fn_vararg, fn_kwarg = func_param_names(fn_node)

    snapshot_calls: List[ast.Call] = []
    ensure_calls: List[ast.Call] = []

    for dec in fn_node.decorator_list:
        kind = decorator_kind(dec)
        if kind is None or not isinstance(dec, ast.Call):
            continue
        if kind == "snapshot":
            snapshot_calls.append(dec)
        elif kind == "ensure":
            ensure_calls.append(dec)

    snapshot_props = derive_snapshot_props(snapshot_calls)

    return CheckContext(
        combined=combined,
        lines=lines,
        tree=tree,
        fn_node=fn_node,
        func_params=func_params,
        fn_vararg=fn_vararg,
        fn_kwarg=fn_kwarg,
        snapshot_calls=snapshot_calls,
        ensure_calls=ensure_calls,
        snapshot_props=snapshot_props,
    )
