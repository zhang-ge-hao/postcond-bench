from __future__ import annotations

import ast
from typing import Dict, List, Optional, Set, Tuple


def decorator_kind(dec: ast.AST) -> Optional[str]:
    if not isinstance(dec, ast.Call):
        return None
    fn = dec.func
    if isinstance(fn, ast.Attribute):
        if isinstance(fn.value, ast.Name) and fn.value.id == "icontract":
            if fn.attr in ("snapshot", "ensure"):
                return fn.attr
    return None


def get_first_positional_arg(dec_call: ast.Call) -> Optional[ast.AST]:
    return dec_call.args[0] if dec_call.args else None


def is_lambda(node: ast.AST) -> bool:
    return isinstance(node, ast.Lambda)


def lambda_param_names(lam: ast.Lambda) -> Tuple[List[str], Optional[str], Optional[str]]:
    """
    Returns (positional_param_names, vararg_name, kwarg_name).
    """
    args = lam.args
    names: List[str] = []
    for a in getattr(args, "posonlyargs", []):
        names.append(a.arg)
    for a in args.args:
        names.append(a.arg)
    for a in args.kwonlyargs:
        names.append(a.arg)
    vararg = args.vararg.arg if args.vararg else None
    kwarg = args.kwarg.arg if args.kwarg else None
    return names, vararg, kwarg


def func_param_names(fn: ast.FunctionDef | ast.AsyncFunctionDef) -> Tuple[Set[str], Optional[str], Optional[str]]:
    args = fn.args
    names: Set[str] = set()
    for a in getattr(args, "posonlyargs", []):
        names.add(a.arg)
    for a in args.args:
        names.add(a.arg)
    for a in args.kwonlyargs:
        names.add(a.arg)
    vararg = args.vararg.arg if args.vararg else None
    kwarg = args.kwarg.arg if args.kwarg else None
    if vararg:
        names.add(vararg)
    if kwarg:
        names.add(kwarg)
    return names, vararg, kwarg


def keyword_str_value(call: ast.Call, key: str) -> Optional[str]:
    for kw in call.keywords:
        if kw.arg == key and isinstance(kw.value, ast.Constant) and isinstance(kw.value.value, str):
            return kw.value.value
    return None


def loaded_names(node: ast.AST) -> Set[str]:
    """
    Collect all identifiers used in Load context in the given AST node.
    """
    out: Set[str] = set()
    for sub in ast.walk(node):
        if isinstance(sub, ast.Name) and isinstance(sub.ctx, ast.Load):
            out.add(sub.id)
    return out


def snapshot_declared_name(call: ast.Call) -> Optional[str]:
    """
    Resolve snapshot name by icontract conventions:
      1) keyword: name="xxx"
      2) second positional arg: "xxx"
      3) omitted name + capture lambda has exactly one parameter => that parameter name
    """
    # 1) keyword name="xxx"
    for kw in call.keywords:
        if kw.arg == "name" and isinstance(kw.value, ast.Constant) and isinstance(kw.value.value, str):
            return kw.value.value

    # 2) positional name: snapshot(lambda ..., "xxx")
    if len(call.args) >= 2 and isinstance(call.args[1], ast.Constant) and isinstance(call.args[1].value, str):
        return call.args[1].value

    # 3) omitted: infer from lambda single parameter
    first = get_first_positional_arg(call)
    if isinstance(first, ast.Lambda):
        names, _, _ = lambda_param_names(first)
        if len(names) == 1:
            return names[0]

    return None


def derive_snapshot_props(snapshot_calls: List[ast.Call]) -> Dict[str, ast.Call]:
    props: Dict[str, ast.Call] = {}
    for call in snapshot_calls:
        name = snapshot_declared_name(call)
        if name is not None:
            props[name] = call
    return props
