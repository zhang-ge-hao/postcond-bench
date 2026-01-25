from __future__ import annotations

import ast
from dataclasses import dataclass
from typing import Iterable, List, Optional, Tuple, Dict, Set


@dataclass(frozen=True)
class SplitPostcondition:
    """One ensure + the snapshots it depends on (via OLD.<name>)."""
    ensure_src: str
    snapshot_srcs: Tuple[str, ...]
    old_deps: Tuple[str, ...]  # names referenced as OLD.<name>

    def to_decorator_block(self) -> str:
        """Render as decorators-only block (no def)."""
        parts = [*self.snapshot_srcs, self.ensure_src]
        return "\n".join(parts).rstrip() + "\n"


def _is_icontract_call(dec: ast.AST, target: str) -> bool:
    """
    True if decorator looks like:
      @icontract.ensure(...)
      @ensure(...)
      @ic.ensure(...)
    """
    if not isinstance(dec, ast.Call):
        return False

    f = dec.func
    if isinstance(f, ast.Attribute):
        return f.attr == target
    if isinstance(f, ast.Name):
        return f.id == target
    return False


def _get_source_segment(src: str, node: ast.AST) -> str:
    seg = ast.get_source_segment(src, node)
    if seg is None:
        # Fallback: ast.get_source_segment can be None if positions are missing
        return ""
    return seg.strip()


def _snapshot_name_from_call(call: ast.Call) -> Optional[str]:
    """
    Determine the OLD attribute name produced by @snapshot(...).

    - If keyword name="foo" is present and is a constant string -> "foo"
    - Else if first positional arg is a lambda with exactly one parameter -> that parameter name
      (per icontract docs, omitted name defaults to argument name) :contentReference[oaicite:1]{index=1}
    - Else return None (unknown / ambiguous)
    """
    # keyword: name="..."
    for kw in call.keywords or []:
        if kw.arg == "name" and isinstance(kw.value, ast.Constant) and isinstance(kw.value.value, str):
            return kw.value.value

    # infer from lambda argument name
    if call.args:
        first = call.args[0]
        if isinstance(first, ast.Lambda):
            args = first.args.args
            if len(args) == 1:
                return args[0].arg

    return None


class _OldAttrCollector(ast.NodeVisitor):
    """Collect attribute names accessed as OLD.<attr> in a lambda body."""
    def __init__(self) -> None:
        self.attrs: Set[str] = set()

    def visit_Attribute(self, node: ast.Attribute) -> None:
        # match OLD.something
        if isinstance(node.value, ast.Name) and node.value.id == "OLD":
            self.attrs.add(node.attr)
        self.generic_visit(node)


def _ensure_old_deps_from_call(call: ast.Call) -> Set[str]:
    """
    Parse ensure condition lambda and collect OLD.<name> dependencies.
    We look only for direct attribute accesses OLD.xxx.
    """
    if not call.args:
        return set()
    cond = call.args[0]
    if not isinstance(cond, ast.Lambda):
        return set()

    collector = _OldAttrCollector()
    collector.visit(cond.body)
    return collector.attrs


def split_icontract_postconditions(src: str) -> List[SplitPostcondition]:
    """
    Input:
      Python source containing a function with stacked icontract decorators
      (multiple @snapshot and @ensure).

    Output:
      One item per ensure:
        - exactly one ensure decorator source
        - only the snapshots *above it* that are referenced via OLD.<name>
    """
    # If user passes only decorators, wrap into a dummy function so ast can parse.
    wrapped = src
    if "def " not in src and "async def " not in src:
        wrapped = src.rstrip() + "\n" + "def __dummy__():\n    pass\n"

    tree = ast.parse(wrapped)

    func: Optional[ast.AST] = None
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            func = node
            break
    if func is None:
        raise ValueError("No function definition found to attach decorators to.")

    decorator_list: List[ast.AST] = getattr(func, "decorator_list", [])
    # decorator_list is in source order: top -> bottom.

    # Collect snapshots in order with their names and source
    snapshots: List[Tuple[int, Optional[str], ast.Call, str]] = []
    ensures: List[Tuple[int, ast.Call, str]] = []

    for idx, dec in enumerate(decorator_list):
        if _is_icontract_call(dec, "snapshot"):
            call = dec  # type: ignore[assignment]
            assert isinstance(call, ast.Call)
            name = _snapshot_name_from_call(call)
            dec_src = _get_source_segment(wrapped, dec)
            snapshots.append((idx, name, call, dec_src))
        elif _is_icontract_call(dec, "ensure"):
            call = dec  # type: ignore[assignment]
            assert isinstance(call, ast.Call)
            dec_src = _get_source_segment(wrapped, dec)
            ensures.append((idx, call, dec_src))
        else:
            # ignore other decorators (require/invariant/staticmethod/etc.)
            continue

    results: List[SplitPostcondition] = []

    # For quick lookup: for each ensure, consider only snapshots with smaller idx (above it)
    for e_idx, e_call, e_src in ensures:
        deps = _ensure_old_deps_from_call(e_call)
        deps_sorted = tuple(sorted(deps))

        # Map snapshot name -> snapshot src for snapshots above ensure
        above = [(s_idx, s_name, s_src) for (s_idx, s_name, _s_call, s_src) in snapshots if s_idx < e_idx]
        name_to_src: Dict[str, str] = {}
        for s_idx, s_name, s_src in above:
            if s_name is None:
                continue
            # if duplicates, keep the nearest (the one closest to ensure, i.e., largest s_idx)
            if s_name not in name_to_src or s_idx > max(i for i, n, _ in above if n == s_name):
                name_to_src[s_name] = s_src

        # Pick only snapshots referenced via OLD.<name>
        chosen: List[Tuple[int, str]] = []
        missing: List[str] = []
        for dep in deps:
            if dep in name_to_src:
                # keep original order by snapshot position
                s_pos = next(s_idx for (s_idx, s_name, _s_src) in above if s_name == dep)
                chosen.append((s_pos, name_to_src[dep]))
            else:
                missing.append(dep)

        if missing:
            # This usually means: ensure refers to OLD.<x> but no matching snapshot above it.
            raise ValueError(
                f"ensure at decorator index {e_idx} references OLD.{missing}, "
                f"but matching @snapshot(name=...) not found above it."
            )

        chosen.sort(key=lambda t: t[0])  # keep snapshots in source order
        snapshot_srcs = tuple(src for _, src in chosen)

        results.append(
            SplitPostcondition(
                ensure_src=e_src,
                snapshot_srcs=snapshot_srcs,
                old_deps=deps_sorted,
            )
        )

    return results


# -----------------------------
# Demo / simple tests
# -----------------------------
if __name__ == "__main__":
    code = """
@icontract.snapshot(lambda app: logging.getLogger(app.name).level, name='original_level')
@icontract.snapshot(lambda cls: "__tablename__" in cls.__dict__, name="has_tablename_before")
@icontract.ensure(
    lambda result, cls: not ("__tablename__" in cls.__dict__) if result is None else True,
    "If the result is None, the class's __dict__ must not contain __tablename__."
)
@icontract.ensure(
    lambda result: isinstance(result, sa.Table) or result is None,
    "The result must be a Table instance or None."
)
@icontract.ensure(lambda result, app: result.name == app.name)
@icontract.ensure(lambda OLD, result, app: not (app.debug and OLD.original_level == 0) or (result.level == logging.DEBUG))
@icontract.ensure(lambda result: has_level_handler(result))
"""

    parts = split_icontract_postconditions(code)
    for k, p in enumerate(parts, 1):
        print(f"--- Part {k} ---")
        print("OLD deps:", p.old_deps)
        print(p.to_decorator_block())
