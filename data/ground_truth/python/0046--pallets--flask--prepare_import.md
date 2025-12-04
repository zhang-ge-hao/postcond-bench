https://github.com/pallets/flask/blob/330123258e8c3dc391cbe55ab1ed94891ca83af3/./src/flask/cli.py#L200-L226
```
@icontract.snapshot(lambda path: os.path.realpath(path), name="real")
@icontract.snapshot(
    lambda path: (
        os.path.dirname(os.path.splitext(os.path.realpath(path))[0])
        if os.path.basename(os.path.splitext(os.path.realpath(path))[0]) == "__init__"
        else (os.path.splitext(os.path.realpath(path))[0]
              if os.path.splitext(os.path.realpath(path))[1] == ".py"
              else os.path.realpath(path))
    ),
    name="base",
)
@icontract.ensure(lambda result: isinstance(result, str) and result != "")
@icontract.ensure(
    lambda OLD, result: result
    == (
        "" if os.path.relpath(OLD.base, start=sys.path[0]) == "."
        else os.path.relpath(OLD.base, start=sys.path[0]).replace(os.sep, ".")
    )
)
@icontract.ensure(lambda OLD: os.path.commonpath([OLD.real, sys.path[0]]) == sys.path[0])
@icontract.ensure(
    lambda result, path: (
        lambda state: (
            (
                state.update({"path": os.path.splitext(state["path"])[0]})
                if os.path.splitext(state["path"])[1] == ".py"
                else None
            ),
            (
                state.update({"path": os.path.dirname(state["path"])})
                if os.path.basename(state["path"]) == "__init__"
                else None
            ),
            [
                (
                    state.update({"_split": os.path.split(state["path"])}),
                    state["module_name"].append(state["_split"][1]),
                    state.update({"path": state["_split"][0]}),
                    state.update(
                        {
                            "done": not os.path.exists(
                                os.path.join(state["path"], "__init__.py")
                            )
                        }
                    ),
                )
                for _ in range(1000)
                if not state["done"]
            ],
            ".".join(state["module_name"][::-1]) == result,
        )[-1]
    )(
        {
            "path": os.path.realpath(path),
            "module_name": [],
            "done": False,
        }
    )
)
@icontract.ensure(
    lambda result, path: (
        (lambda state: (
            (
                state.update({"path": os.path.splitext(state["path"])[0]})
                if os.path.splitext(state["path"])[1] == ".py"
                else None
            ),
            (
                state.update({"path": os.path.dirname(state["path"])})
                if os.path.basename(state["path"]) == "__init__"
                else None
            ),
            [
                (
                    state.update({"_split": os.path.split(state["path"])}),
                    state["module_name"].append(state["_split"][1]),
                    state.update({"path": state["_split"][0]}),
                    state.update(
                        {
                            "done": not os.path.exists(
                                os.path.join(state["path"], "__init__.py")
                            )
                        }
                    ),
                )
                for _ in range(1000)
                if not state["done"]
            ],
            sys.path[0] == state["path"],
        )[-1])(
            {
                "path": os.path.realpath(path),
                "module_name": [],
                "done": False,
            }
        )
    )
)
@icontract.ensure(
    lambda result, path: isinstance(sys.path[0], str) and sys.path[0] != ""
)
```
```
@icontract.snapshot(lambda path: os.path.realpath(path), name="real")
@icontract.snapshot(
    lambda path: (
        os.path.dirname(os.path.splitext(os.path.realpath(path))[0])
        if os.path.basename(os.path.splitext(os.path.realpath(path))[0]) == "__init__"
        else (os.path.splitext(os.path.realpath(path))[0]
              if os.path.splitext(os.path.realpath(path))[1] == ".py"
              else os.path.realpath(path))
    ),
    name="base",
)
@icontract.ensure(lambda result: isinstance(result, str) and result != "")
@icontract.ensure(
    lambda OLD, result: result
    == (
        "" if os.path.relpath(OLD.base, start=sys.path[0]) == "."
        else os.path.relpath(OLD.base, start=sys.path[0]).replace(os.sep, ".")
    )
)
@icontract.ensure(lambda OLD: os.path.commonpath([OLD.real, sys.path[0]]) == sys.path[0])
```
[0, 24, 35, 36, 37, 38, 46, 47]
===== 0 =====
```
     """Given a filename this will try to calculate the python path, add it
     to the search path and return the actual module name that is expected.
     """
-    path = os.path.realpath(path)
+    path = os.path.basename(path)
 
     fname, ext = os.path.splitext(path)
     if ext == ".py":
```
```
def prepare_import(path: str) -> str:
    """Given a filename this will try to calculate the python path, add it
    to the search path and return the actual module name that is expected.
    """
    path = os.path.basename(path)

    fname, ext = os.path.splitext(path)
    if ext == ".py":
        path = fname

    if os.path.basename(path) == "__init__":
        path = os.path.dirname(path)

    module_name = []

    # move up until outside package structure (no __init__.py)
    while True:
        path, name = os.path.split(path)
        module_name.append(name)

        if not os.path.exists(os.path.join(path, "__init__.py")):
            break

    if sys.path[0] != path:
        sys.path.insert(0, path)

    return ".".join(module_name[::-1])
```
===== 24 =====
```
         path = fname
 
     if os.path.basename(path) == "__init__":
-        path = os.path.dirname(path)
+        path = os.path.basename(path)
 
     module_name = []
```
```
def prepare_import(path: str) -> str:
    """Given a filename this will try to calculate the python path, add it
    to the search path and return the actual module name that is expected.
    """
    path = os.path.realpath(path)

    fname, ext = os.path.splitext(path)
    if ext == ".py":
        path = fname

    if os.path.basename(path) == "__init__":
        path = os.path.basename(path)

    module_name = []

    # move up until outside package structure (no __init__.py)
    while True:
        path, name = os.path.split(path)
        module_name.append(name)

        if not os.path.exists(os.path.join(path, "__init__.py")):
            break

    if sys.path[0] != path:
        sys.path.insert(0, path)

    return ".".join(module_name[::-1])
```
===== 35 =====
```
         path, name = os.path.split(path)
         module_name.append(name)
 
-        if not os.path.exists(os.path.join(path, "__init__.py")):
+        if not os.path.exists(os.path.join("__init__.py")):
             break
 
     if sys.path[0] != path:
         sys.path.insert(0, path)
 
-    return ".".join(module_name[::-1])+    return ".".join(module_name[::-1])
```
```
def prepare_import(path: str) -> str:
    """Given a filename this will try to calculate the python path, add it
    to the search path and return the actual module name that is expected.
    """
    path = os.path.realpath(path)

    fname, ext = os.path.splitext(path)
    if ext == ".py":
        path = fname

    if os.path.basename(path) == "__init__":
        path = os.path.dirname(path)

    module_name = []

    # move up until outside package structure (no __init__.py)
    while True:
        path, name = os.path.split(path)
        module_name.append(name)

        if not os.path.exists(os.path.join("__init__.py")):
            break

    if sys.path[0] != path:
        sys.path.insert(0, path)

    return ".".join(module_name[::-1])

```
===== 36 =====
```
         path, name = os.path.split(path)
         module_name.append(name)
 
-        if not os.path.exists(os.path.join(path, "__init__.py")):
+        if not os.path.exists(os.path.join(path, "XX__init__.pyXX")):
             break
 
     if sys.path[0] != path:
         sys.path.insert(0, path)
 
-    return ".".join(module_name[::-1])+    return ".".join(module_name[::-1])
```
```
def prepare_import(path: str) -> str:
    """Given a filename this will try to calculate the python path, add it
    to the search path and return the actual module name that is expected.
    """
    path = os.path.realpath(path)

    fname, ext = os.path.splitext(path)
    if ext == ".py":
        path = fname

    if os.path.basename(path) == "__init__":
        path = os.path.dirname(path)

    module_name = []

    # move up until outside package structure (no __init__.py)
    while True:
        path, name = os.path.split(path)
        module_name.append(name)

        if not os.path.exists(os.path.join(path, "XX__init__.pyXX")):
            break

    if sys.path[0] != path:
        sys.path.insert(0, path)

    return ".".join(module_name[::-1])

```
===== 37 =====
```
         path, name = os.path.split(path)
         module_name.append(name)
 
-        if not os.path.exists(os.path.join(path, "__init__.py")):
+        if not os.path.exists(os.path.join(path, "__INIT__.PY")):
             break
 
     if sys.path[0] != path:
         sys.path.insert(0, path)
 
-    return ".".join(module_name[::-1])+    return ".".join(module_name[::-1])
```
```
def prepare_import(path: str) -> str:
    """Given a filename this will try to calculate the python path, add it
    to the search path and return the actual module name that is expected.
    """
    path = os.path.realpath(path)

    fname, ext = os.path.splitext(path)
    if ext == ".py":
        path = fname

    if os.path.basename(path) == "__init__":
        path = os.path.dirname(path)

    module_name = []

    # move up until outside package structure (no __init__.py)
    while True:
        path, name = os.path.split(path)
        module_name.append(name)

        if not os.path.exists(os.path.join(path, "__INIT__.PY")):
            break

    if sys.path[0] != path:
        sys.path.insert(0, path)

    return ".".join(module_name[::-1])

```
===== 38 =====
```
         path, name = os.path.split(path)
         module_name.append(name)
 
-        if not os.path.exists(os.path.join(path, "__init__.py")):
+        if not os.path.exists(os.path.join(path, "setup.py")):
             break
 
     if sys.path[0] != path:
```
```
def prepare_import(path: str) -> str:
    """Given a filename this will try to calculate the python path, add it
    to the search path and return the actual module name that is expected.
    """
    path = os.path.realpath(path)

    fname, ext = os.path.splitext(path)
    if ext == ".py":
        path = fname

    if os.path.basename(path) == "__init__":
        path = os.path.dirname(path)

    module_name = []

    # move up until outside package structure (no __init__.py)
    while True:
        path, name = os.path.split(path)
        module_name.append(name)

        if not os.path.exists(os.path.join(path, "setup.py")):
            break

    if sys.path[0] != path:
        sys.path.insert(0, path)

    return ".".join(module_name[::-1])
```
===== 46 =====
```
             break
 
     if sys.path[0] != path:
-        sys.path.insert(0, path)
+        sys.path.insert(0, "")  # Inserting an empty string
 
     return ".".join(module_name[::-1])
```
```
def prepare_import(path: str) -> str:
    """Given a filename this will try to calculate the python path, add it
    to the search path and return the actual module name that is expected.
    """
    path = os.path.realpath(path)

    fname, ext = os.path.splitext(path)
    if ext == ".py":
        path = fname

    if os.path.basename(path) == "__init__":
        path = os.path.dirname(path)

    module_name = []

    # move up until outside package structure (no __init__.py)
    while True:
        path, name = os.path.split(path)
        module_name.append(name)

        if not os.path.exists(os.path.join(path, "__init__.py")):
            break

    if sys.path[0] != path:
        sys.path.insert(0, "")  # Inserting an empty string

    return ".".join(module_name[::-1])
```
===== 47 =====
```
             break
 
     if sys.path[0] != path:
-        sys.path.insert(0, path)
+        sys.path.insert(0, None)
 
-    return ".".join(module_name[::-1])+    return ".".join(module_name[::-1])
```
```
def prepare_import(path: str) -> str:
    """Given a filename this will try to calculate the python path, add it
    to the search path and return the actual module name that is expected.
    """
    path = os.path.realpath(path)

    fname, ext = os.path.splitext(path)
    if ext == ".py":
        path = fname

    if os.path.basename(path) == "__init__":
        path = os.path.dirname(path)

    module_name = []

    # move up until outside package structure (no __init__.py)
    while True:
        path, name = os.path.split(path)
        module_name.append(name)

        if not os.path.exists(os.path.join(path, "__init__.py")):
            break

    if sys.path[0] != path:
        sys.path.insert(0, None)

    return ".".join(module_name[::-1])

```
