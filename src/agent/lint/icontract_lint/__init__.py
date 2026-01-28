from src.agent.lint.icontract_lint.checker import (
    check_icontract_postconditions, 
    format_issues, 
    grammar_verify
)

__all__ = ["check_icontract_postconditions", "format_issues", "grammar_verify"]


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

    run_case(
        "CASE 24 — Regression testing",
        post="""
@icontract.snapshot(lambda self: self.root_path, name='root_path')
@icontract.snapshot(lambda self: self.path, name='path')
@icontract.snapshot(lambda self: self.query_string, name='query_string')
@icontract.ensure(lambda result, root_path, path, query_string: result == root_path + path + (f'?{query_string}' if query_string else ''))
""",
        method="""
    @property
    def relative_uri(self) -> str:
        if self._cached_relative_uri is None:
            if self.query_string:
                self._cached_relative_uri = (
                    self.root_path + self.path + '?' + self.query_string
                )
            else:
                self._cached_relative_uri = self.root_path + self.path

        return self._cached_relative_uri
""",
    )

    # ------------------------------------------------------------
    # New rules: IC007 - IC011
    # Case numbering starts from 25
    # ------------------------------------------------------------

    # ------------------------------------------------------------
    # IC007: special names used in lambda body must be bound in parameters
    # ------------------------------------------------------------

    run_case(
        "CASE 25 — IC007: ensure uses OLD in body but does not bind OLD in lambda parameters",
        post="""
@icontract.snapshot(lambda x: x, name="x0")
@icontract.ensure(lambda result, x: result == OLD.x0 + 1)
""",
        method="""
def inc_from_old(x):
    return x + 1
""",
    )

    run_case(
        "CASE 26 — OK (IC007 fixed): ensure binds OLD when using OLD.xxx",
        post="""
@icontract.snapshot(lambda x: x, name="x0")
@icontract.ensure(lambda OLD, result, x: result == OLD.x0 + 1)
""",
        method="""
def inc_from_old(x):
    return x + 1
""",
    )

    run_case(
        "CASE 27 — IC007: ensure uses _ARGS in body but does not bind _ARGS in lambda parameters",
        post="""
@icontract.ensure(lambda result: len(_ARGS) >= 0)
""",
        method="""
def f(*args):
    return args
""",
    )

    run_case(
        "CASE 28 — OK (IC007 fixed): ensure binds _ARGS when using it",
        post="""
@icontract.ensure(lambda _ARGS, result: len(_ARGS) >= 0)
""",
        method="""
def f(*args):
    return args
""",
    )

    # ------------------------------------------------------------
    # IC008: decorator must be @icontract.ensure(...) / @icontract.snapshot(...)
    # ------------------------------------------------------------

    run_case(
        "CASE 29 — IC008: uses @ensure(...) instead of @icontract.ensure(...)",
        post="""
@ensure(lambda result, x: result == x)
""",
        method="""
def f(x):
    return x
""",
    )

    run_case(
        "CASE 30 — OK (IC008 fixed): uses @icontract.ensure(...)",
        post="""
@icontract.ensure(lambda result, x: result == x)
""",
        method="""
def f(x):
    return x
""",
    )

    run_case(
        "CASE 31 — IC008: wrong casing @icontract.Snapshot(...)",
        post="""
@icontract.Snapshot(lambda x: x, name="x0")
@icontract.ensure(lambda OLD, result, x: result == OLD.x0)
""",
        method="""
def f(x):
    return x
""",
    )

    run_case(
        "CASE 32 — OK (IC008 fixed): correct casing @icontract.snapshot(...)",
        post="""
@icontract.snapshot(lambda x: x, name="x0")
@icontract.ensure(lambda OLD, result, x: result == OLD.x0)
""",
        method="""
def f(x):
    return x
""",
    )

    # ------------------------------------------------------------
    # IC009: snapshot must explicitly use name="..."
    # ------------------------------------------------------------

    run_case(
        "CASE 33 — IC009: snapshot omits name= (name inferred by lambda param, but disallowed by rule)",
        post="""
@icontract.snapshot(lambda x: x)   # name omitted => disallowed by IC009
@icontract.ensure(lambda OLD, result, x: result == x)
""",
        method="""
def f(x):
    return x
""",
    )

    run_case(
        "CASE 34 — OK (IC009 fixed): snapshot uses explicit name=",
        post="""
@icontract.snapshot(lambda x: x, name="x0")
@icontract.ensure(lambda OLD, result, x: result == x)
""",
        method="""
def f(x):
    return x
""",
    )

    run_case(
        "CASE 35 — IC009: snapshot passes name positionally (disallowed; must be name=...)",
        post="""
@icontract.snapshot(lambda x: x, "x0")
@icontract.ensure(lambda OLD, result, x: result == OLD.x0)
""",
        method="""
def f(x):
    return x
""",
    )

    run_case(
        "CASE 36 — OK (IC009 fixed): snapshot passes name via keyword",
        post="""
@icontract.snapshot(lambda x: x, name="x0")
@icontract.ensure(lambda OLD, result, x: result == OLD.x0)
""",
        method="""
def f(x):
    return x
""",
    )

    # ------------------------------------------------------------
    # IC010: snapshot name must be unique and must not conflict with function parameters
    # ------------------------------------------------------------

    run_case(
        "CASE 37 — IC010: snapshot name duplicates another snapshot name",
        post="""
@icontract.snapshot(lambda a: a, name="old_a")
@icontract.snapshot(lambda b: b, name="old_a")   # duplicate
@icontract.ensure(lambda OLD, a, b: a == OLD.old_a)
""",
        method="""
def f(a, b):
    return a + b
""",
    )

    run_case(
        "CASE 38 — OK (IC010 fixed): snapshot names are unique",
        post="""
@icontract.snapshot(lambda a: a, name="old_a")
@icontract.snapshot(lambda b: b, name="old_b")
@icontract.ensure(lambda OLD, a, b: a == OLD.old_a and b == OLD.old_b)
""",
        method="""
def f(a, b):
    return a + b
""",
    )

    run_case(
        "CASE 39 — IC010: snapshot name conflicts with function parameter name",
        post="""
@icontract.snapshot(lambda x: x, name="x")   # conflicts with function parameter 'x'
@icontract.ensure(lambda OLD, result, x: result == OLD.x)
""",
        method="""
def f(x):
    return x
""",
    )

    run_case(
        "CASE 40 — OK (IC010 fixed): snapshot name does not conflict with parameters",
        post="""
@icontract.snapshot(lambda x: x, name="old_x")
@icontract.ensure(lambda OLD, result, x: result == OLD.old_x)
""",
        method="""
def f(x):
    return x
""",
    )

    # ------------------------------------------------------------
    # IC011: OLD must be accessed as OLD.xxx; forbid OLD["xxx"]; and xxx must be defined by snapshot
    # ------------------------------------------------------------

    run_case(
        "CASE 41 — IC011: OLD used with subscripting OLD[\"x0\"] (forbidden)",
        post="""
@icontract.snapshot(lambda x: x, name="x0")
@icontract.ensure(lambda OLD, result, x: result == OLD["x0"])
""",
        method="""
def f(x):
    return x
""",
    )

    run_case(
        "CASE 42 — OK (IC011 fixed): OLD accessed as attribute OLD.x0",
        post="""
@icontract.snapshot(lambda x: x, name="x0")
@icontract.ensure(lambda OLD, result, x: result == OLD.x0)
""",
        method="""
def f(x):
    return x
""",
    )

    run_case(
        "CASE 43 — IC011: OLD.xxx used but xxx not defined by any snapshot",
        post="""
@icontract.snapshot(lambda x: x, name="x0")
@icontract.ensure(lambda OLD, result, x: result == OLD.not_defined)
""",
        method="""
def f(x):
    return x
""",
    )

    run_case(
        "CASE 44 — OK (IC011 fixed): OLD.xxx refers to a defined snapshot name",
        post="""
@icontract.snapshot(lambda x: x, name="x0")
@icontract.ensure(lambda OLD, result, x: result == OLD.x0)
""",
        method="""
def f(x):
    return x
""",
    )
