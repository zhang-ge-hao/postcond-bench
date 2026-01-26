from __future__ import annotations

import ast
from dataclasses import dataclass
from typing import List, Optional, Tuple, Dict, Set


# -----------------------------
# Data model for issues
# -----------------------------

@dataclass(frozen=True)
class Issue:
    code: str                # e.g., IC001
    rule: str                # short rule name
    message: str             # human readable (English)
    line: int                # 1-based
    col: int                 # 0-based
    end_line: Optional[int] = None
    end_col: Optional[int] = None
    snippet: Optional[str] = None
    caret: Optional[str] = None

    def format(self) -> str:
        loc = f"Line {self.line}, Col {self.col}"
        # header = f"[{self.code}] {self.rule} — {loc}"
        header = f"{self.rule} — {loc}"
        body = self.message
        if self.snippet is not None and self.caret is not None:
            return f"{header}\n{body}\n\n{self.snippet}\n{self.caret}"
        return f"{header}\n{body}"


# -----------------------------
# Helpers: location/snippet
# -----------------------------

def _linecol_from_index(text: str, idx: int) -> Tuple[int, int]:
    # returns 1-based line, 0-based col
    line = 1
    col = 0
    for i, ch in enumerate(text):
        if i == idx:
            return line, col
        if ch == "\n":
            line += 1
            col = 0
        else:
            col += 1
    return line, col  # idx at EOF

def _make_snippet(lines: List[str], line: int, col: int, context: int = 0) -> Tuple[str, str]:
    # context=0 => single line
    i = max(1, line) - 1
    if i < 0 or i >= len(lines):
        return "", ""
    snippet = lines[i].rstrip("\n")
    caret = (" " * col) + "^"
    return snippet, caret

def _node_span(node: ast.AST) -> Tuple[int, int]:
    # best-effort start location
    line = getattr(node, "lineno", 1)
    col = getattr(node, "col_offset", 0)
    return int(line), int(col)


# -----------------------------
# Rule #4: bracket matching excluding strings
# -----------------------------

_BR_OPEN = {"(": ")", "[": "]", "{": "}"}
_BR_CLOSE = {")": "(", "]": "[", "}": "{"}

def _check_bracket_matching(code: str) -> List[Tuple[int, int, str]]:
    """
    Return list of (line, col, message) for bracket mismatches.
    Ignores brackets in strings and comments.
    """
    issues: List[Tuple[int, int, str]] = []
    stack: List[Tuple[str, int]] = []  # (opening_char, absolute_index)

    i = 0
    n = len(code)

    in_str = False
    str_quote = ""          # one of ', ", ''' or """
    triple = False
    escape = False

    def startswith_at(s: str, pos: int) -> bool:
        return code.startswith(s, pos)

    while i < n:
        ch = code[i]

        # Handle comment start (#) when not in string
        if not in_str and ch == "#":
            # skip to end of line
            while i < n and code[i] != "\n":
                i += 1
            continue

        # Handle string start/end
        if not in_str:
            if startswith_at("'''", i) or startswith_at('"""', i):
                in_str = True
                triple = True
                str_quote = code[i:i+3]
                i += 3
                continue
            if ch == "'" or ch == '"':
                in_str = True
                triple = False
                str_quote = ch
                i += 1
                continue
        else:
            # inside string
            if escape:
                escape = False
                i += 1
                continue
            if ch == "\\":
                escape = True
                i += 1
                continue

            if triple:
                if startswith_at(str_quote, i):
                    in_str = False
                    triple = False
                    str_quote = ""
                    i += 3
                    continue
            else:
                if ch == str_quote:
                    in_str = False
                    str_quote = ""
                    i += 1
                    continue

            i += 1
            continue

        # Not in string/comment => process brackets
        if ch in _BR_OPEN:
            stack.append((ch, i))
        elif ch in _BR_CLOSE:
            if not stack:
                line, col = _linecol_from_index(code, i)
                issues.append((line, col, f"Unmatched closing bracket '{ch}'."))
            else:
                top, top_idx = stack[-1]
                if _BR_CLOSE[ch] != top:
                    line, col = _linecol_from_index(code, i)
                    exp = _BR_OPEN[top]
                    issues.append((line, col, f"Mismatched bracket: got '{ch}', expected '{exp}' to close '{top}'."))
                else:
                    stack.pop()

        i += 1

    # Any unmatched openings
    for top, top_idx in stack:
        line, col = _linecol_from_index(code, top_idx)
        issues.append((line, col, f"Unmatched opening bracket '{top}'."))
    return issues


# -----------------------------
# icontract decorator identification
# -----------------------------

def _decorator_kind(dec: ast.AST) -> Optional[str]:
    """
    Returns 'snapshot' or 'ensure' if the decorator matches icontract usage.
    Supports:
      - @icontract.snapshot(...)
      - @icontract.ensure(...)
      - @snapshot(...), @ensure(...)  (if imported directly)
    """
    if not isinstance(dec, ast.Call):
        return None
    fn = dec.func
    if isinstance(fn, ast.Attribute):
        # icontract.snapshot / icontract.ensure
        if fn.attr in ("snapshot", "ensure"):
            return fn.attr
    elif isinstance(fn, ast.Name):
        if fn.id in ("snapshot", "ensure"):
            return fn.id
    return None

def _get_first_positional_arg(dec_call: ast.Call) -> Optional[ast.AST]:
    return dec_call.args[0] if dec_call.args else None

def _is_lambda(node: ast.AST) -> bool:
    return isinstance(node, ast.Lambda)

def _lambda_param_names(lam: ast.Lambda) -> Tuple[List[str], Optional[str], Optional[str]]:
    """
    Returns (positional_param_names, vararg_name, kwarg_name).
    """
    args = lam.args
    names: List[str] = []
    # positional-only + pos/kw
    for a in getattr(args, "posonlyargs", []):
        names.append(a.arg)
    for a in args.args:
        names.append(a.arg)
    # kw-only
    for a in args.kwonlyargs:
        names.append(a.arg)
    vararg = args.vararg.arg if args.vararg else None
    kwarg = args.kwarg.arg if args.kwarg else None
    return names, vararg, kwarg

def _func_param_names(fn: ast.FunctionDef | ast.AsyncFunctionDef) -> Tuple[Set[str], Optional[str], Optional[str]]:
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

def _keyword_str_value(call: ast.Call, key: str) -> Optional[str]:
    for kw in call.keywords:
        if kw.arg == key and isinstance(kw.value, ast.Constant) and isinstance(kw.value.value, str):
            return kw.value.value
    return None


def _loaded_names(node: ast.AST) -> Set[str]:
    """
    Collect all identifiers used in Load context in the given AST node.
    (We intentionally do *not* try to resolve globals/imports; we only use this
    to detect missing bindings for *function parameters* referenced in lambda bodies.)
    """
    out: Set[str] = set()
    for sub in ast.walk(node):
        if isinstance(sub, ast.Name) and isinstance(sub.ctx, ast.Load):
            out.add(sub.id)
    return out



# -----------------------------
# Main checker
# -----------------------------

def check_icontract_postconditions(method_src: str, postconditions_src: str) -> List[Issue]:
    """
    Validate icontract snapshot/ensure decorators for a single method.

    Returns a list of Issues (English messages, with line/col and snippet).
    """
    # Combine sources so AST has decorators attached to the function node
    combined = (postconditions_src.rstrip() + "\n" + method_src.lstrip()).rstrip() + "\n"
    lines = combined.splitlines(True)

    issues: List[Issue] = []

    # Rule #4: bracket matching (ignore strings/comments)
    for (line, col, msg) in _check_bracket_matching(combined):
        snippet, caret = _make_snippet(lines, line, col)
        issues.append(Issue(
            code="IC004",
            rule="Bracket matching",
            message=msg + " (Brackets inside strings/comments are ignored.)",
            line=line,
            col=col,
            snippet=snippet,
            caret=caret
        ))

    # Parse AST (also catches syntax errors beyond simple bracket mismatches)
    try:
        tree = ast.parse(combined)
    except SyntaxError as e:
        line = int(e.lineno or 1)
        col = int(e.offset or 0)
        snippet, caret = _make_snippet(lines, line, col)
        issues.append(Issue(
            code="IC000",
            rule="Python syntax",
            message=f"Python syntax error while parsing the provided code: {e.msg}.",
            line=line,
            col=col,
            snippet=snippet,
            caret=caret
        ))
        return issues  # can't proceed reliably

    # Find the function definition (first one in the snippet)
    fn_node: Optional[ast.FunctionDef | ast.AsyncFunctionDef] = None
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            fn_node = node
            break

    if fn_node is None:
        issues.append(Issue(
            code="IC000",
            rule="Missing function",
            message="No function definition (def ...) was found in the provided method source.",
            line=1,
            col=0
        ))
        return issues

    func_params, fn_vararg, fn_kwarg = _func_param_names(fn_node)

    # Collect snapshot properties (names inside OLD.<prop>)
    snapshot_props: Dict[str, ast.Call] = {}  # prop_name -> decorator call
    snapshot_calls: List[ast.Call] = []
    ensure_calls: List[ast.Call] = []

    for dec in fn_node.decorator_list:
        kind = _decorator_kind(dec)
        if kind is None:
            continue
        if not isinstance(dec, ast.Call):
            continue

        if kind == "snapshot":
            snapshot_calls.append(dec)
        elif kind == "ensure":
            ensure_calls.append(dec)

    # --- Rule #1 / #3 / snapshot prop derivation ---
    for call in snapshot_calls:
        # Rule #1: first arg must be lambda
        first = _get_first_positional_arg(call)
        if first is None:
            line, col = _node_span(call)
            snippet, caret = _make_snippet(lines, line, col)
            issues.append(Issue(
                code="IC001",
                rule="First argument must be lambda",
                message="@icontract.snapshot(...) must receive a lambda as its first positional argument, but no positional argument was provided.",
                line=line,
                col=col,
                snippet=snippet,
                caret=caret
            ))
            continue
        if not _is_lambda(first):
            line, col = _node_span(first)
            snippet, caret = _make_snippet(lines, line, col)
            issues.append(Issue(
                code="IC001",
                rule="First argument must be lambda",
                message=f"@icontract.snapshot(...) first positional argument must be a lambda expression, but found {type(first).__name__}.",
                line=line,
                col=col,
                snippet=snippet,
                caret=caret
            ))
            continue

        lam: ast.Lambda = first  # type: ignore[assignment]
        lam_names, lam_vararg, lam_kwarg = _lambda_param_names(lam)

        # Rule #3 (snapshot): lambda params must come from function param list
        for name in lam_names:
            if name not in func_params:
                line, col = _node_span(lam)
                snippet, caret = _make_snippet(lines, line, col)
                issues.append(Issue(
                    code="IC003",
                    rule="Snapshot lambda parameters",
                    message=(
                        f"snapshot capture lambda parameter '{name}' is not a parameter of the decorated function. "
                        f"Snapshot capture functions must accept only a subset of the function parameters."
                    ),
                    line=line,
                    col=col,
                    snippet=snippet,
                    caret=caret
                ))

        # Also disallow using *varargs/**kwargs in lambda for snapshot (rare, but usually wrong)
        if lam_vararg is not None or lam_kwarg is not None:
            line, col = _node_span(lam)
            snippet, caret = _make_snippet(lines, line, col)
            issues.append(Issue(
                code="IC003",
                rule="Snapshot lambda parameters",
                message=(
                    "snapshot capture lambda should not use *args/**kwargs in its signature. "
                    "Use explicit parameter names from the function signature instead."
                ),
                line=line,
                col=col,
                snippet=snippet,
                caret=caret
            ))

        # --- NEW Rule IC006: lambda body must not reference function params that are not bound in lambda signature ---
        # icontract snapshots/capture functions are called with arguments of the original function,
        # so referencing a function parameter without binding it in the lambda signature is almost always a mistake.
        used = _loaded_names(lam.body)
        missing = (used & func_params) - set(lam_names)
        if missing:
            line, col = _node_span(lam)
            snippet, caret = _make_snippet(lines, line, col)
            missing_list = ", ".join(sorted(missing))
            issues.append(Issue(
                code="IC006",
                rule="Bind referenced parameters",
                message=(
                    f"snapshot capture lambda references function parameter(s) [{missing_list}] in its body, "
                    f"but does not declare them in the lambda signature. "
                    f"In icontract, snapshot capture functions receive the original function arguments via their parameters; "
                    f"declare the needed parameters explicitly (e.g., lambda {missing_list}: ...)."
                ),
                line=line,
                col=col,
                snippet=snippet,
                caret=caret
            ))


        # Derive snapshot property name (name=... or omitted with single argument)
        explicit_name = _keyword_str_value(call, "name")
        if explicit_name is not None:
            prop = explicit_name
        else:
            # Per docs: if capture function has a single argument, name can be omitted and equals that argument
            # (If 0 or >1 args and name omitted => we can't reliably name it; skip).
            prop = lam_names[0] if len(lam_names) == 1 else None

        if prop is not None:
            snapshot_props[prop] = call

    # --- Ensure rules (#1, #3, #2, #5) ---
    allowed_special = {"result", "OLD", "_ARGS", "_KWARGS"}

    for call in ensure_calls:
        first = _get_first_positional_arg(call)
        if first is None:
            line, col = _node_span(call)
            snippet, caret = _make_snippet(lines, line, col)
            issues.append(Issue(
                code="IC001",
                rule="First argument must be lambda",
                message="@icontract.ensure(...) must receive a lambda as its first positional argument, but no positional argument was provided.",
                line=line,
                col=col,
                snippet=snippet,
                caret=caret
            ))
            continue
        if not _is_lambda(first):
            line, col = _node_span(first)
            snippet, caret = _make_snippet(lines, line, col)
            issues.append(Issue(
                code="IC001",
                rule="First argument must be lambda",
                message=f"@icontract.ensure(...) first positional argument must be a lambda expression, but found {type(first).__name__}.",
                line=line,
                col=col,
                snippet=snippet,
                caret=caret
            ))
            continue

        lam: ast.Lambda = first  # type: ignore[assignment]
        lam_names, lam_vararg, lam_kwarg = _lambda_param_names(lam)

        # Rule #5: if function uses *args/**kwargs, do NOT use those names in ensure lambda params
        if fn_vararg is not None:
            bad = []
            if fn_vararg in lam_names:
                bad.append(fn_vararg)
            if lam_vararg == fn_vararg:
                bad.append(f"*{fn_vararg}")
            if bad:
                line, col = _node_span(lam)
                snippet, caret = _make_snippet(lines, line, col)
                issues.append(Issue(
                    code="IC005",
                    rule="Varargs placeholders",
                    message=(
                        f"The function defines variable positional arguments (*{fn_vararg}), so the contract should not "
                        f"bind '{fn_vararg}' in the ensure lambda signature. "
                        f"Prefer the placeholder '_ARGS' and refer to positional call arguments via _ARGS[...] as described in the docs."
                    ),
                    line=line,
                    col=col,
                    snippet=snippet,
                    caret=caret
                ))

        if fn_kwarg is not None:
            bad = []
            if fn_kwarg in lam_names:
                bad.append(fn_kwarg)
            if lam_kwarg == fn_kwarg:
                bad.append(f"**{fn_kwarg}")
            if bad:
                line, col = _node_span(lam)
                snippet, caret = _make_snippet(lines, line, col)
                issues.append(Issue(
                    code="IC005",
                    rule="Varargs placeholders",
                    message=(
                        f"The function defines variable keyword arguments (**{fn_kwarg}), so the contract should not "
                        f"bind '{fn_kwarg}' in the ensure lambda signature. "
                        f"Prefer the placeholder '_KWARGS' and refer to keyword call arguments via _KWARGS[...] as described in the docs."
                    ),
                    line=line,
                    col=col,
                    snippet=snippet,
                    caret=caret
                ))

        # Rule #3 (ensure): params must be function params OR special names (result/OLD/_ARGS/_KWARGS)
        for name in lam_names:
            if name in allowed_special:
                continue
            if name not in func_params:
                # Rule #2 specialization: looks like they tried to pass snapshot old-value directly (wrong)
                if name in snapshot_props:
                    line, col = _node_span(lam)
                    snippet, caret = _make_snippet(lines, line, col)
                    issues.append(Issue(
                        code="IC002",
                        rule="Use OLD for snapshots",
                        message=(
                            f"ensure lambda binds '{name}', which matches a snapshot property. "
                            f"This is not how icontract snapshots are provided. "
                            f"Use 'OLD' as a parameter and access the snapshot as OLD.{name} "
                            f"(e.g., lambda OLD, ...: ... OLD.{name} ...)."
                        ),
                        line=line,
                        col=col,
                        snippet=snippet,
                        caret=caret
                    ))
                else:
                    line, col = _node_span(lam)
                    snippet, caret = _make_snippet(lines, line, col)
                    issues.append(Issue(
                        code="IC003",
                        rule="Ensure lambda parameters",
                        message=(
                            f"ensure lambda parameter '{name}' is neither a function parameter nor a special name "
                            f"('result' or 'OLD')."
                        ),
                        line=line,
                        col=col,
                        snippet=snippet,
                        caret=caret
                    ))

        # --- NEW Rule IC006: lambda body must not reference function params that are not bound in lambda signature ---
        used = _loaded_names(lam.body)
        missing = (used & func_params) - set(lam_names) - allowed_special
        if missing:
            line, col = _node_span(lam)
            snippet, caret = _make_snippet(lines, line, col)
            missing_list = ", ".join(sorted(missing))
            issues.append(Issue(
                code="IC006",
                rule="Bind referenced parameters",
                message=(
                    f"ensure lambda references function parameter(s) [{missing_list}] in its body, "
                    f"but does not declare them in the lambda signature. "
                    f"In icontract, postcondition functions receive the original function arguments via their parameters; "
                    f"declare the needed parameters explicitly (e.g., lambda result, {missing_list}: ...)."
                ),
                line=line,
                col=col,
                snippet=snippet,
                caret=caret
            ))

        # Optional extra hint: varargs/kwargs referenced in body should use placeholders
        # (Your existing IC005 checks binding the *name* in the signature; this catches using it in the body.)
        if fn_vararg is not None and fn_vararg in used and "_ARGS" not in set(lam_names):
            line, col = _node_span(lam)
            snippet, caret = _make_snippet(lines, line, col)
            issues.append(Issue(
                code="IC006",
                rule="Bind referenced parameters",
                message=(
                    f"ensure lambda references '*{fn_vararg}' in its body. "
                    f"When the function defines *{fn_vararg}, prefer binding the placeholder '_ARGS' "
                    f"and refer to positional call arguments via _ARGS[...]."
                ),
                line=line,
                col=col,
                snippet=snippet,
                caret=caret
            ))
        if fn_kwarg is not None and fn_kwarg in used and "_KWARGS" not in set(lam_names):
            line, col = _node_span(lam)
            snippet, caret = _make_snippet(lines, line, col)
            issues.append(Issue(
                code="IC006",
                rule="Bind referenced parameters",
                message=(
                    f"ensure lambda references '**{fn_kwarg}' in its body. "
                    f"When the function defines **{fn_kwarg}, prefer binding the placeholder '_KWARGS' "
                    f"and refer to keyword call arguments via _KWARGS[...]."
                ),
                line=line,
                col=col,
                snippet=snippet,
                caret=caret
            ))



        # Also: if snapshots exist AND ensure tries to use snapshot property but forgets OLD entirely,
        # the IC002 above already covers (since it flags the param). But we add an extra hint if snapshots exist
        # and lambda doesn't include OLD at all (optional but helpful).
        if snapshot_props and "OLD" not in lam_names:
            # Only warn if they bind *any* snapshot prop name (likely old-value attempt) OR if they use snapshots at all.
            # We keep it as a hint (still an error-ish issue) because some postconditions legitimately don't need OLD.
            pass  # intentionally not emitting a generic error

        # Disallow ensure lambda vararg/kwarg in general (usually not how icontract expects condition signature)
        if lam_vararg is not None or lam_kwarg is not None:
            line, col = _node_span(lam)
            snippet, caret = _make_snippet(lines, line, col)
            issues.append(Issue(
                code="IC003",
                rule="Ensure lambda parameters",
                message=(
                    "ensure lambda should not use *args/**kwargs in its signature. "
                    "Bind explicit parameter names, or use placeholders '_ARGS'/'_KWARGS' when referring to call arguments."
                ),
                line=line,
                col=col,
                snippet=snippet,
                caret=caret
            ))

    return issues


def format_issues(issues: List[Issue]) -> str:
    if not issues:
        return "No issues found."
    return "\n\n".join(issue.format() for issue in issues)


def grammar_verify(method, postconds):
    issues = check_icontract_postconditions(method, postconds)
    return format_issues(issues)

# -----------------------------
# Example usage (optional)
# -----------------------------
if __name__ == "__main__":
    def run_case(title: str, post: str, method: str):
        print("=" * 90)
        print(title)
        print("-" * 90)
        print("POSTCONDITIONS:")
        print(post.strip() + "\n")
        print("METHOD:")
        print(method.strip() + "\n")
        issues = check_icontract_postconditions(method, post)
        print("RESULT:")
        print(format_issues(issues))
        print()

    # ------------------------------------------------------------
    # 0) Clean / should pass
    # ------------------------------------------------------------
    run_case(
        "CASE 0 — OK: snapshot + ensure using OLD correctly (no errors expected)",
        post="""
@icontract.snapshot(lambda lst: lst[:])  # name omitted => OLD.lst
@icontract.ensure(lambda OLD, lst, value: lst == OLD.lst + [value])
""",
        method="""
def append_one(lst, value):
    lst.append(value)
    return lst
""",
    )

    # ------------------------------------------------------------
    # 1) Rule #1: first arg is not lambda
    # ------------------------------------------------------------
    run_case(
        "CASE 1 — IC001: snapshot first arg not a lambda",
        post="""
@icontract.snapshot(list)  # not a lambda
@icontract.ensure(lambda OLD, lst: True)
""",
        method="""
def f(lst):
    return lst
""",
    )

    run_case(
        "CASE 2 — IC001: ensure first arg not a lambda",
        post="""
@icontract.ensure(True)  # not a lambda
""",
        method="""
def f(x):
    return x
""",
    )

    run_case(
        "CASE 3 — IC001: snapshot missing first positional argument entirely",
        post="""
@icontract.snapshot(name="old_x")
@icontract.ensure(lambda OLD, x: True)
""",
        method="""
def f(x):
    return x
""",
    )

    run_case(
        "CASE 4 — IC001: ensure missing first positional argument entirely",
        post="""
@icontract.ensure(description="must hold")  # no positional arg
""",
        method="""
def f(x):
    return x
""",
    )

    # ------------------------------------------------------------
    # 2) Rule #2: wrong OLD usage (binding snapshot property directly)
    # ------------------------------------------------------------
    run_case(
        "CASE 5 — IC002: WRONG (binding snapshot property directly in ensure params)",
        post="""
@icontract.snapshot(lambda lst: lst[:], name="old_lst")
@icontract.ensure(lambda old_lst, lst, value: lst == old_lst + [value])
""",
        method="""
def append_one(lst, value):
    lst.append(value)
""",
    )

    run_case(
        "CASE 6 — IC002: WRONG (name omitted => snapshot property is the capture parameter name)",
        post="""
@icontract.snapshot(lambda lst: lst[:])  # OLD.lst
@icontract.ensure(lambda lst, value: True)  # binds 'lst' (also function param, so IC002 may not trigger)
""",
        method="""
def f(lst, value):
    return lst
""",
    )
    # Note: In this checker, IC002 triggers only when ensure binds a name that is NOT a function param
    # but matches a snapshot property. In this case 'lst' is a function param, so it won't raise IC002.

    run_case(
        "CASE 7 — IC002: name omitted but capture param is NOT a function param => IC003(snapshot) and possible IC002 later",
        post="""
@icontract.snapshot(lambda not_in_sig: not_in_sig, name="old_x")
@icontract.ensure(lambda old_x, x: True)
""",
        method="""
def f(x):
    return x
""",
    )

    # ------------------------------------------------------------
    # 3) Rule #3: lambda params must be in function params (snapshot), or params/result/OLD (ensure)
    # ------------------------------------------------------------
    run_case(
        "CASE 8 — IC003: snapshot lambda param not in function signature",
        post="""
@icontract.snapshot(lambda y: y)  # y not in f(x)
@icontract.ensure(lambda OLD, x: True)
""",
        method="""
def f(x):
    return x
""",
    )

    run_case(
        "CASE 9 — IC003: ensure lambda param not allowed",
        post="""
@icontract.ensure(lambda x, y: True)  # y not in signature; not result/OLD
""",
        method="""
def f(x):
    return x
""",
    )

    run_case(
        "CASE 10 — OK: ensure uses 'result' (allowed special)",
        post="""
@icontract.ensure(lambda result, x: result == x + 1)
""",
        method="""
def inc(x):
    return x + 1
""",
    )

    run_case(
        "CASE 11 — OK: ensure uses OLD even without snapshots (allowed special; checker should not error)",
        post="""
@icontract.ensure(lambda OLD, x: True)
""",
        method="""
def f(x):
    return x
""",
    )

    # ------------------------------------------------------------
    # 4) Rule #4: bracket matching (ignore strings/comments)
    # ------------------------------------------------------------
    run_case(
        "CASE 12 — IC004: missing closing bracket in decorator expression",
        post="""
@icontract.ensure(lambda x: (x > 0) and (x < 10)  # missing ')'
""",
        method="""
def f(x):
    return x
""",
    )

    run_case(
        "CASE 13 — OK: brackets inside strings should be ignored by bracket matcher",
        post=r"""
@icontract.ensure(lambda x: "text with ( ) [ ] { }" and (x > 0))
""",
        method="""
def f(x):
    return x
""",
    )

    run_case(
        "CASE 14 — IC004: mismatched closing bracket",
        post="""
@icontract.ensure(lambda x: (x > 0])
""",
        method="""
def f(x):
    return x
""",
    )

    # ------------------------------------------------------------
    # 5) Rule #5: function has *args/**kwargs; lambda must not bind those names
    # ------------------------------------------------------------
    run_case(
        "CASE 15 — IC005: function uses *args but ensure binds 'args' (should suggest _ARGS)",
        post="""
@icontract.ensure(lambda args: len(args) > 0)
""",
        method="""
def f(*args):
    return args
""",
    )

    run_case(
        "CASE 16 — IC005: function uses **kwargs but ensure binds 'kwargs' (should suggest _KWARGS)",
        post="""
@icontract.ensure(lambda kwargs: "x" in kwargs)
""",
        method="""
def f(**kwargs):
    return kwargs
""",
    )

    run_case(
        "CASE 17 — OK-ish: function uses *args/**kwargs but ensure uses placeholders (no error expected)",
        post="""
@icontract.ensure(lambda _ARGS, _KWARGS: len(_ARGS) >= 0 and isinstance(_KWARGS, dict))
""",
        method="""
def f(*args, **kwargs):
    return args, kwargs
""",
    )

    # ------------------------------------------------------------
    # Extra: ensure lambda uses *args/**kwargs itself (IC003 in this checker)
    # ------------------------------------------------------------
    run_case(
        "CASE 18 — IC003: ensure lambda uses *args/**kwargs (discouraged / should error in this checker)",
        post="""
@icontract.ensure(lambda x, *rest: True)
""",
        method="""
def f(x, y):
    return x
""",
    )

    run_case(
        "CASE 19 — IC003: snapshot lambda uses *args/**kwargs (discouraged / should error in this checker)",
        post="""
@icontract.snapshot(lambda *args: args[0])
@icontract.ensure(lambda OLD, x: True)
""",
        method="""
def f(x):
    return x
""",
    )

    # ------------------------------------------------------------
    # Extra: multiple snapshots; ensure incorrectly binds one of them
    # ------------------------------------------------------------
    run_case(
        "CASE 20 — IC002: multiple snapshots; ensure binds snapshot property directly",
        post="""
@icontract.snapshot(lambda a: a, name="old_a")
@icontract.snapshot(lambda b: b, name="old_b")
@icontract.ensure(lambda old_a, old_b, a, b: a == old_a and b == old_b)
""",
        method="""
def f(a, b):
    return a + b
""",
    )

    run_case(
        "CASE 21 — IC006: lambda body must not reference function params that are not bound in lambda signature",
        post="""
@icontract.ensure(
    lambda result: len(result) == sum(1 for part in parts if isinstance(part.root, FilePart)),
    "The length of the result should match the number of FilePart objects in the input list."
)
""",
        method="""
def get_file_parts(parts: list[Part]) -> list[FileWithBytes | FileWithUri]:
    return [part.root.file for part in parts if isinstance(part.root, FilePart)]
""",
    )

    run_case(
        "CASE 22 — IC006: fixed -- lambda body must not reference function params that are not bound in lambda signature",
        post="""
@icontract.ensure(
    lambda result, parts: len(result) == sum(1 for part in parts if isinstance(part.root, FilePart)),
    "The length of the result should match the number of FilePart objects in the input list."
)
""",
        method="""
def get_file_parts(parts: list[Part]) -> list[FileWithBytes | FileWithUri]:
    return [part.root.file for part in parts if isinstance(part.root, FilePart)]
""",
    )

    run_case(
        "CASE 23 — Regression testing",
        post="""
@icontract.snapshot(lambda self: self.environ.get('HTTP_AUTHORIZATION', ''), name='http_authorization')  
@icontract.snapshot(lambda self: self.environ.get('REMOTE_USER'), name='remote_user')  
@icontract.ensure(lambda result: result is None or (isinstance(result, tuple) and len(result) == 2))  
@icontract.ensure(lambda result: result is None or (isinstance(result[0], str) and (result[1] is None or isinstance(result[1], str))))  
@icontract.ensure(lambda result, remote_user: result is None or not (isinstance(result, tuple) and result[1] is None and (remote_user is None or result[0] != remote_user)))  
@icontract.ensure(lambda result, http_authorization: result is None or not (isinstance(result, tuple) and result[1] is not None and http_authorization == ''))
""",
        method="""
    @property
    def auth(self):
        basic = parse_auth(self.environ.get('HTTP_AUTHORIZATION', ''))
        if basic: return basic
        ruser = self.environ.get('REMOTE_USER')
        if ruser: return (ruser, None)
        return None
""",
    )