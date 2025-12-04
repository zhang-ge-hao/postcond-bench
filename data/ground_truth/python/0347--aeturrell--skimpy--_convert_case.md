https://github.com/aeturrell/skimpy/blob/9cd3ed61e0d7e6d36cada4c6807ea7452a8c14df/./src/skimpy/__init__.py#L965-L1003
```
@icontract.snapshot(
    lambda name: "header" if name in NULL_VALUES else str(name),
    name="normalized_name",
)
@icontract.ensure(
    lambda OLD, case, result:
    case != "snake"
    or result == "_".join(_split_strip_string(OLD.normalized_name)).lower()
)
@icontract.ensure(
    lambda OLD, case, result:
    case != "kebab"
    or result == "-".join(_split_strip_string(OLD.normalized_name)).lower()
)
@icontract.ensure(
    lambda OLD, case, result:
    case != "camel"
    or result
    == (
        lambda words: words[0].lower()
        + "".join(w.capitalize() for w in words[1:])
    )(_split_strip_string(OLD.normalized_name))
)
@icontract.ensure(
    lambda OLD, case, result:
    case != "pascal"
    or result
    == "".join(w.capitalize() for w in _split_strip_string(OLD.normalized_name))
)
@icontract.ensure(
    lambda OLD, case, result:
    case != "const"
    or result
    == "_".join(_split_strip_string(OLD.normalized_name)).upper()
)
@icontract.ensure(
    lambda OLD, case, result:
    case != "sentence"
    or result
    == " ".join(_split_string(OLD.normalized_name)).capitalize()
)
@icontract.ensure(
    lambda OLD, case, result:
    case != "title"
    or result
    == " ".join(
        w.capitalize() for w in _split_string(OLD.normalized_name)
    )
)
@icontract.ensure(
    lambda OLD, case, result:
    case != "lower"
    or result
    == " ".join(_split_string(OLD.normalized_name)).lower()
)
@icontract.ensure(
    lambda OLD, case, result:
    case != "upper"
    or result
    == " ".join(_split_string(OLD.normalized_name)).upper()
)
```
```
@icontract.snapshot(lambda name: name, name="orig_name")
@icontract.ensure(lambda OLD, case, result: (OLD.orig_name not in NULL_VALUES) or (
    (case == "snake" and result == "header") or
    (case == "kebab" and result == "header") or
    (case == "camel" and result == "header") or
    (case == "pascal" and result == "Header") or
    (case == "const" and result == "HEADER") or
    (case == "sentence" and result == "Header") or
    (case == "title" and result == "Header") or
    (case == "lower" and result == "header") or
    (case == "upper" and result == "HEADER")
))
@icontract.ensure(lambda case, result: (case != "snake") or (isinstance(result, str) and result == result.lower() and " " not in result and "-" not in result))
@icontract.ensure(lambda case, result: (case != "kebab") or (isinstance(result, str) and result == result.lower() and " " not in result and "_" not in result))
@icontract.ensure(lambda case, result: (case != "camel") or (isinstance(result, str) and result != "" and result[0].islower() and all(sep not in result for sep in ("_", "-", " "))))
@icontract.ensure(lambda case, result: (case != "pascal") or (isinstance(result, str) and result != "" and result[0].isupper() and all(sep not in result for sep in ("_", "-", " "))))
@icontract.ensure(lambda case, result: (case != "const") or (isinstance(result, str) and result == result.upper() and " " not in result and "-" not in result))
@icontract.ensure(lambda case, result: (case != "sentence") or (isinstance(result, str) and result == result.capitalize()))
@icontract.ensure(lambda case, result: (case != "title") or (isinstance(result, str) and all(((w and w[0].isalpha() and w[0].isupper()) or (w and not w[0].isalpha()) or (not w)) for w in result.split(" "))))
@icontract.ensure(lambda case, result: (case != "lower") or (isinstance(result, str) and result == result.lower()))
@icontract.ensure(lambda case, result: (case != "upper") or (isinstance(result, str) and result == result.upper()))
```
[8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 26, 27, 28, 39, 53, 63, 64, 65, 71, 74, 77, 81, 97, 102, 103, 105, 107, 118, 128, 129]
===== 8 =====
```
     if name in NULL_VALUES:
         name = "header"
 
-    if case in {"snake", "kebab", "camel", "pascal", "const"}:
+    if case in {"SNAKE", "kebab", "camel", "pascal", "const"}:
         words = _split_strip_string(str(name))
     else:
         words = _split_string(str(name))
@@ -36,4 +36,4 @@     elif case == "upper":
         name = " ".join(words).upper()
 
-    return name+    return name
```
```
@typechecked
def _convert_case(name: Any, case: str) -> Any:
    """Convert case style of a column name.

    Args:
        name (Any): Column name.
        case (str): Preferred case type, eg snake or camel.

    Returns:
        Any: name with case converted.
    """
    if name in NULL_VALUES:
        name = "header"

    if case in {"SNAKE", "kebab", "camel", "pascal", "const"}:
        words = _split_strip_string(str(name))
    else:
        words = _split_string(str(name))

    if case == "snake":
        name = "_".join(words).lower()
    elif case == "kebab":
        name = "-".join(words).lower()
    elif case == "camel":
        name = words[0].lower() + "".join(w.capitalize() for w in words[1:])
    elif case == "pascal":
        name = "".join(w.capitalize() for w in words)
    elif case == "const":
        name = "_".join(words).upper()
    elif case == "sentence":
        name = " ".join(words).capitalize()
    elif case == "title":
        name = " ".join(w.capitalize() for w in words)
    elif case == "lower":
        name = " ".join(words).lower()
    elif case == "upper":
        name = " ".join(words).upper()

    return name

```
===== 9 =====
```
     if name in NULL_VALUES:
         name = "header"
 
-    if case in {"snake", "kebab", "camel", "pascal", "const"}:
+    if case in {"XXsnakeXX", "kebab", "camel", "pascal", "const"}:
         words = _split_strip_string(str(name))
     else:
         words = _split_string(str(name))
@@ -36,4 +36,4 @@     elif case == "upper":
         name = " ".join(words).upper()
 
-    return name+    return name
```
```
@typechecked
def _convert_case(name: Any, case: str) -> Any:
    """Convert case style of a column name.

    Args:
        name (Any): Column name.
        case (str): Preferred case type, eg snake or camel.

    Returns:
        Any: name with case converted.
    """
    if name in NULL_VALUES:
        name = "header"

    if case in {"XXsnakeXX", "kebab", "camel", "pascal", "const"}:
        words = _split_strip_string(str(name))
    else:
        words = _split_string(str(name))

    if case == "snake":
        name = "_".join(words).lower()
    elif case == "kebab":
        name = "-".join(words).lower()
    elif case == "camel":
        name = words[0].lower() + "".join(w.capitalize() for w in words[1:])
    elif case == "pascal":
        name = "".join(w.capitalize() for w in words)
    elif case == "const":
        name = "_".join(words).upper()
    elif case == "sentence":
        name = " ".join(words).capitalize()
    elif case == "title":
        name = " ".join(w.capitalize() for w in words)
    elif case == "lower":
        name = " ".join(words).lower()
    elif case == "upper":
        name = " ".join(words).upper()

    return name

```
===== 10 =====
```
     if name in NULL_VALUES:
         name = "header"
 
-    if case in {"snake", "kebab", "camel", "pascal", "const"}:
+    if case in {"snake", "KEBAB", "camel", "pascal", "const"}:
         words = _split_strip_string(str(name))
     else:
         words = _split_string(str(name))
@@ -36,4 +36,4 @@     elif case == "upper":
         name = " ".join(words).upper()
 
-    return name+    return name
```
```
@typechecked
def _convert_case(name: Any, case: str) -> Any:
    """Convert case style of a column name.

    Args:
        name (Any): Column name.
        case (str): Preferred case type, eg snake or camel.

    Returns:
        Any: name with case converted.
    """
    if name in NULL_VALUES:
        name = "header"

    if case in {"snake", "KEBAB", "camel", "pascal", "const"}:
        words = _split_strip_string(str(name))
    else:
        words = _split_string(str(name))

    if case == "snake":
        name = "_".join(words).lower()
    elif case == "kebab":
        name = "-".join(words).lower()
    elif case == "camel":
        name = words[0].lower() + "".join(w.capitalize() for w in words[1:])
    elif case == "pascal":
        name = "".join(w.capitalize() for w in words)
    elif case == "const":
        name = "_".join(words).upper()
    elif case == "sentence":
        name = " ".join(words).capitalize()
    elif case == "title":
        name = " ".join(w.capitalize() for w in words)
    elif case == "lower":
        name = " ".join(words).lower()
    elif case == "upper":
        name = " ".join(words).upper()

    return name

```
===== 11 =====
```
     if name in NULL_VALUES:
         name = "header"
 
-    if case in {"snake", "kebab", "camel", "pascal", "const"}:
+    if case in {"snake", "XXkebabXX", "camel", "pascal", "const"}:
         words = _split_strip_string(str(name))
     else:
         words = _split_string(str(name))
@@ -36,4 +36,4 @@     elif case == "upper":
         name = " ".join(words).upper()
 
-    return name+    return name
```
```
@typechecked
def _convert_case(name: Any, case: str) -> Any:
    """Convert case style of a column name.

    Args:
        name (Any): Column name.
        case (str): Preferred case type, eg snake or camel.

    Returns:
        Any: name with case converted.
    """
    if name in NULL_VALUES:
        name = "header"

    if case in {"snake", "XXkebabXX", "camel", "pascal", "const"}:
        words = _split_strip_string(str(name))
    else:
        words = _split_string(str(name))

    if case == "snake":
        name = "_".join(words).lower()
    elif case == "kebab":
        name = "-".join(words).lower()
    elif case == "camel":
        name = words[0].lower() + "".join(w.capitalize() for w in words[1:])
    elif case == "pascal":
        name = "".join(w.capitalize() for w in words)
    elif case == "const":
        name = "_".join(words).upper()
    elif case == "sentence":
        name = " ".join(words).capitalize()
    elif case == "title":
        name = " ".join(w.capitalize() for w in words)
    elif case == "lower":
        name = " ".join(words).lower()
    elif case == "upper":
        name = " ".join(words).upper()

    return name

```
===== 12 =====
```
     if name in NULL_VALUES:
         name = "header"
 
-    if case in {"snake", "kebab", "camel", "pascal", "const"}:
+    if case in {"snake", "kebab", "CAMEL", "pascal", "const"}:
         words = _split_strip_string(str(name))
     else:
         words = _split_string(str(name))
@@ -36,4 +36,4 @@     elif case == "upper":
         name = " ".join(words).upper()
 
-    return name+    return name
```
```
@typechecked
def _convert_case(name: Any, case: str) -> Any:
    """Convert case style of a column name.

    Args:
        name (Any): Column name.
        case (str): Preferred case type, eg snake or camel.

    Returns:
        Any: name with case converted.
    """
    if name in NULL_VALUES:
        name = "header"

    if case in {"snake", "kebab", "CAMEL", "pascal", "const"}:
        words = _split_strip_string(str(name))
    else:
        words = _split_string(str(name))

    if case == "snake":
        name = "_".join(words).lower()
    elif case == "kebab":
        name = "-".join(words).lower()
    elif case == "camel":
        name = words[0].lower() + "".join(w.capitalize() for w in words[1:])
    elif case == "pascal":
        name = "".join(w.capitalize() for w in words)
    elif case == "const":
        name = "_".join(words).upper()
    elif case == "sentence":
        name = " ".join(words).capitalize()
    elif case == "title":
        name = " ".join(w.capitalize() for w in words)
    elif case == "lower":
        name = " ".join(words).lower()
    elif case == "upper":
        name = " ".join(words).upper()

    return name

```
===== 13 =====
```
     if name in NULL_VALUES:
         name = "header"
 
-    if case in {"snake", "kebab", "camel", "pascal", "const"}:
+    if case in {"snake", "kebab", "XXcamelXX", "pascal", "const"}:
         words = _split_strip_string(str(name))
     else:
         words = _split_string(str(name))
@@ -36,4 +36,4 @@     elif case == "upper":
         name = " ".join(words).upper()
 
-    return name+    return name
```
```
@typechecked
def _convert_case(name: Any, case: str) -> Any:
    """Convert case style of a column name.

    Args:
        name (Any): Column name.
        case (str): Preferred case type, eg snake or camel.

    Returns:
        Any: name with case converted.
    """
    if name in NULL_VALUES:
        name = "header"

    if case in {"snake", "kebab", "XXcamelXX", "pascal", "const"}:
        words = _split_strip_string(str(name))
    else:
        words = _split_string(str(name))

    if case == "snake":
        name = "_".join(words).lower()
    elif case == "kebab":
        name = "-".join(words).lower()
    elif case == "camel":
        name = words[0].lower() + "".join(w.capitalize() for w in words[1:])
    elif case == "pascal":
        name = "".join(w.capitalize() for w in words)
    elif case == "const":
        name = "_".join(words).upper()
    elif case == "sentence":
        name = " ".join(words).capitalize()
    elif case == "title":
        name = " ".join(w.capitalize() for w in words)
    elif case == "lower":
        name = " ".join(words).lower()
    elif case == "upper":
        name = " ".join(words).upper()

    return name

```
===== 14 =====
```
     if name in NULL_VALUES:
         name = "header"
 
-    if case in {"snake", "kebab", "camel", "pascal", "const"}:
+    if case in {"snake", "kebab", "camel", "PASCAL", "const"}:
         words = _split_strip_string(str(name))
     else:
         words = _split_string(str(name))
@@ -36,4 +36,4 @@     elif case == "upper":
         name = " ".join(words).upper()
 
-    return name+    return name
```
```
@typechecked
def _convert_case(name: Any, case: str) -> Any:
    """Convert case style of a column name.

    Args:
        name (Any): Column name.
        case (str): Preferred case type, eg snake or camel.

    Returns:
        Any: name with case converted.
    """
    if name in NULL_VALUES:
        name = "header"

    if case in {"snake", "kebab", "camel", "PASCAL", "const"}:
        words = _split_strip_string(str(name))
    else:
        words = _split_string(str(name))

    if case == "snake":
        name = "_".join(words).lower()
    elif case == "kebab":
        name = "-".join(words).lower()
    elif case == "camel":
        name = words[0].lower() + "".join(w.capitalize() for w in words[1:])
    elif case == "pascal":
        name = "".join(w.capitalize() for w in words)
    elif case == "const":
        name = "_".join(words).upper()
    elif case == "sentence":
        name = " ".join(words).capitalize()
    elif case == "title":
        name = " ".join(w.capitalize() for w in words)
    elif case == "lower":
        name = " ".join(words).lower()
    elif case == "upper":
        name = " ".join(words).upper()

    return name

```
===== 15 =====
```
     if name in NULL_VALUES:
         name = "header"
 
-    if case in {"snake", "kebab", "camel", "pascal", "const"}:
+    if case in {"snake", "kebab", "camel", "XXpascalXX", "const"}:
         words = _split_strip_string(str(name))
     else:
         words = _split_string(str(name))
@@ -36,4 +36,4 @@     elif case == "upper":
         name = " ".join(words).upper()
 
-    return name+    return name
```
```
@typechecked
def _convert_case(name: Any, case: str) -> Any:
    """Convert case style of a column name.

    Args:
        name (Any): Column name.
        case (str): Preferred case type, eg snake or camel.

    Returns:
        Any: name with case converted.
    """
    if name in NULL_VALUES:
        name = "header"

    if case in {"snake", "kebab", "camel", "XXpascalXX", "const"}:
        words = _split_strip_string(str(name))
    else:
        words = _split_string(str(name))

    if case == "snake":
        name = "_".join(words).lower()
    elif case == "kebab":
        name = "-".join(words).lower()
    elif case == "camel":
        name = words[0].lower() + "".join(w.capitalize() for w in words[1:])
    elif case == "pascal":
        name = "".join(w.capitalize() for w in words)
    elif case == "const":
        name = "_".join(words).upper()
    elif case == "sentence":
        name = " ".join(words).capitalize()
    elif case == "title":
        name = " ".join(w.capitalize() for w in words)
    elif case == "lower":
        name = " ".join(words).lower()
    elif case == "upper":
        name = " ".join(words).upper()

    return name

```
===== 16 =====
```
     if name in NULL_VALUES:
         name = "header"
 
-    if case in {"snake", "kebab", "camel", "pascal", "const"}:
+    if case in {"snake", "kebab", "camel", "pascal", "CONST"}:
         words = _split_strip_string(str(name))
     else:
         words = _split_string(str(name))
@@ -36,4 +36,4 @@     elif case == "upper":
         name = " ".join(words).upper()
 
-    return name+    return name
```
```
@typechecked
def _convert_case(name: Any, case: str) -> Any:
    """Convert case style of a column name.

    Args:
        name (Any): Column name.
        case (str): Preferred case type, eg snake or camel.

    Returns:
        Any: name with case converted.
    """
    if name in NULL_VALUES:
        name = "header"

    if case in {"snake", "kebab", "camel", "pascal", "CONST"}:
        words = _split_strip_string(str(name))
    else:
        words = _split_string(str(name))

    if case == "snake":
        name = "_".join(words).lower()
    elif case == "kebab":
        name = "-".join(words).lower()
    elif case == "camel":
        name = words[0].lower() + "".join(w.capitalize() for w in words[1:])
    elif case == "pascal":
        name = "".join(w.capitalize() for w in words)
    elif case == "const":
        name = "_".join(words).upper()
    elif case == "sentence":
        name = " ".join(words).capitalize()
    elif case == "title":
        name = " ".join(w.capitalize() for w in words)
    elif case == "lower":
        name = " ".join(words).lower()
    elif case == "upper":
        name = " ".join(words).upper()

    return name

```
===== 17 =====
```
     if name in NULL_VALUES:
         name = "header"
 
-    if case in {"snake", "kebab", "camel", "pascal", "const"}:
+    if case in {"snake", "kebab", "camel", "pascal", "XXconstXX"}:
         words = _split_strip_string(str(name))
     else:
         words = _split_string(str(name))
@@ -36,4 +36,4 @@     elif case == "upper":
         name = " ".join(words).upper()
 
-    return name+    return name
```
```
@typechecked
def _convert_case(name: Any, case: str) -> Any:
    """Convert case style of a column name.

    Args:
        name (Any): Column name.
        case (str): Preferred case type, eg snake or camel.

    Returns:
        Any: name with case converted.
    """
    if name in NULL_VALUES:
        name = "header"

    if case in {"snake", "kebab", "camel", "pascal", "XXconstXX"}:
        words = _split_strip_string(str(name))
    else:
        words = _split_string(str(name))

    if case == "snake":
        name = "_".join(words).lower()
    elif case == "kebab":
        name = "-".join(words).lower()
    elif case == "camel":
        name = words[0].lower() + "".join(w.capitalize() for w in words[1:])
    elif case == "pascal":
        name = "".join(w.capitalize() for w in words)
    elif case == "const":
        name = "_".join(words).upper()
    elif case == "sentence":
        name = " ".join(words).capitalize()
    elif case == "title":
        name = " ".join(w.capitalize() for w in words)
    elif case == "lower":
        name = " ".join(words).lower()
    elif case == "upper":
        name = " ".join(words).upper()

    return name

```
===== 18 =====
```
     if name in NULL_VALUES:
         name = "header"
 
-    if case in {"snake", "kebab", "camel", "pascal", "const"}:
+    if case in {"snake", "kebab", "camel", "pascal", "const"} and case != "snake":
         words = _split_strip_string(str(name))
     else:
         words = _split_string(str(name))
```
```
@typechecked
def _convert_case(name: Any, case: str) -> Any:
    """Convert case style of a column name.

    Args:
        name (Any): Column name.
        case (str): Preferred case type, eg snake or camel.

    Returns:
        Any: name with case converted.
    """
    if name in NULL_VALUES:
        name = "header"

    if case in {"snake", "kebab", "camel", "pascal", "const"} and case != "snake":
        words = _split_strip_string(str(name))
    else:
        words = _split_string(str(name))

    if case == "snake":
        name = "_".join(words).lower()
    elif case == "kebab":
        name = "-".join(words).lower()
    elif case == "camel":
        name = words[0].lower() + "".join(w.capitalize() for w in words[1:])
    elif case == "pascal":
        name = "".join(w.capitalize() for w in words)
    elif case == "const":
        name = "_".join(words).upper()
    elif case == "sentence":
        name = " ".join(words).capitalize()
    elif case == "title":
        name = " ".join(w.capitalize() for w in words)
    elif case == "lower":
        name = " ".join(words).lower()
    elif case == "upper":
        name = " ".join(words).upper()

    return name
```
===== 19 =====
```
     if name in NULL_VALUES:
         name = "header"
 
-    if case in {"snake", "kebab", "camel", "pascal", "const"}:
+    if case in {"snake", "kebab", "camel", "pascal", "const"} and len(case) > 5:
         words = _split_strip_string(str(name))
     else:
         words = _split_string(str(name))
```
```
@typechecked
def _convert_case(name: Any, case: str) -> Any:
    """Convert case style of a column name.

    Args:
        name (Any): Column name.
        case (str): Preferred case type, eg snake or camel.

    Returns:
        Any: name with case converted.
    """
    if name in NULL_VALUES:
        name = "header"

    if case in {"snake", "kebab", "camel", "pascal", "const"} and len(case) > 5:
        words = _split_strip_string(str(name))
    else:
        words = _split_string(str(name))

    if case == "snake":
        name = "_".join(words).lower()
    elif case == "kebab":
        name = "-".join(words).lower()
    elif case == "camel":
        name = words[0].lower() + "".join(w.capitalize() for w in words[1:])
    elif case == "pascal":
        name = "".join(w.capitalize() for w in words)
    elif case == "const":
        name = "_".join(words).upper()
    elif case == "sentence":
        name = " ".join(words).capitalize()
    elif case == "title":
        name = " ".join(w.capitalize() for w in words)
    elif case == "lower":
        name = " ".join(words).lower()
    elif case == "upper":
        name = " ".join(words).upper()

    return name
```
===== 20 =====
```
     if name in NULL_VALUES:
         name = "header"
 
-    if case in {"snake", "kebab", "camel", "pascal", "const"}:
+    if case in {"snake", "kebab", "camel", "pascal"}:  # Missing 'const'
         words = _split_strip_string(str(name))
     else:
         words = _split_string(str(name))
```
```
@typechecked
def _convert_case(name: Any, case: str) -> Any:
    """Convert case style of a column name.

    Args:
        name (Any): Column name.
        case (str): Preferred case type, eg snake or camel.

    Returns:
        Any: name with case converted.
    """
    if name in NULL_VALUES:
        name = "header"

    if case in {"snake", "kebab", "camel", "pascal"}:  # Missing 'const'
        words = _split_strip_string(str(name))
    else:
        words = _split_string(str(name))

    if case == "snake":
        name = "_".join(words).lower()
    elif case == "kebab":
        name = "-".join(words).lower()
    elif case == "camel":
        name = words[0].lower() + "".join(w.capitalize() for w in words[1:])
    elif case == "pascal":
        name = "".join(w.capitalize() for w in words)
    elif case == "const":
        name = "_".join(words).upper()
    elif case == "sentence":
        name = " ".join(words).capitalize()
    elif case == "title":
        name = " ".join(w.capitalize() for w in words)
    elif case == "lower":
        name = " ".join(words).lower()
    elif case == "upper":
        name = " ".join(words).upper()

    return name
```
===== 21 =====
```
     if name in NULL_VALUES:
         name = "header"
 
-    if case in {"snake", "kebab", "camel", "pascal", "const"}:
+    if case not in {"snake", "kebab", "camel", "pascal", "const"}:
         words = _split_strip_string(str(name))
     else:
         words = _split_string(str(name))
@@ -36,4 +36,4 @@     elif case == "upper":
         name = " ".join(words).upper()
 
-    return name+    return name
```
```
@typechecked
def _convert_case(name: Any, case: str) -> Any:
    """Convert case style of a column name.

    Args:
        name (Any): Column name.
        case (str): Preferred case type, eg snake or camel.

    Returns:
        Any: name with case converted.
    """
    if name in NULL_VALUES:
        name = "header"

    if case not in {"snake", "kebab", "camel", "pascal", "const"}:
        words = _split_strip_string(str(name))
    else:
        words = _split_string(str(name))

    if case == "snake":
        name = "_".join(words).lower()
    elif case == "kebab":
        name = "-".join(words).lower()
    elif case == "camel":
        name = words[0].lower() + "".join(w.capitalize() for w in words[1:])
    elif case == "pascal":
        name = "".join(w.capitalize() for w in words)
    elif case == "const":
        name = "_".join(words).upper()
    elif case == "sentence":
        name = " ".join(words).capitalize()
    elif case == "title":
        name = " ".join(w.capitalize() for w in words)
    elif case == "lower":
        name = " ".join(words).lower()
    elif case == "upper":
        name = " ".join(words).upper()

    return name

```
===== 22 =====
```
         name = "header"
 
     if case in {"snake", "kebab", "camel", "pascal", "const"}:
-        words = _split_strip_string(str(name))
+        words = _split_string(str(name))  # This will not strip punctuation, leading to incorrect casing.
     else:
         words = _split_string(str(name))
```
```
@typechecked
def _convert_case(name: Any, case: str) -> Any:
    """Convert case style of a column name.

    Args:
        name (Any): Column name.
        case (str): Preferred case type, eg snake or camel.

    Returns:
        Any: name with case converted.
    """
    if name in NULL_VALUES:
        name = "header"

    if case in {"snake", "kebab", "camel", "pascal", "const"}:
        words = _split_string(str(name))  # This will not strip punctuation, leading to incorrect casing.
    else:
        words = _split_string(str(name))

    if case == "snake":
        name = "_".join(words).lower()
    elif case == "kebab":
        name = "-".join(words).lower()
    elif case == "camel":
        name = words[0].lower() + "".join(w.capitalize() for w in words[1:])
    elif case == "pascal":
        name = "".join(w.capitalize() for w in words)
    elif case == "const":
        name = "_".join(words).upper()
    elif case == "sentence":
        name = " ".join(words).capitalize()
    elif case == "title":
        name = " ".join(w.capitalize() for w in words)
    elif case == "lower":
        name = " ".join(words).lower()
    elif case == "upper":
        name = " ".join(words).upper()

    return name
```
===== 23 =====
```
         name = "header"
 
     if case in {"snake", "kebab", "camel", "pascal", "const"}:
-        words = _split_strip_string(str(name))
+        words = _split_strip_string(name.lower())  # This will convert the name to lowercase before splitting, losing original casing.
     else:
         words = _split_string(str(name))
```
```
@typechecked
def _convert_case(name: Any, case: str) -> Any:
    """Convert case style of a column name.

    Args:
        name (Any): Column name.
        case (str): Preferred case type, eg snake or camel.

    Returns:
        Any: name with case converted.
    """
    if name in NULL_VALUES:
        name = "header"

    if case in {"snake", "kebab", "camel", "pascal", "const"}:
        words = _split_strip_string(name.lower())  # This will convert the name to lowercase before splitting, losing original casing.
    else:
        words = _split_string(str(name))

    if case == "snake":
        name = "_".join(words).lower()
    elif case == "kebab":
        name = "-".join(words).lower()
    elif case == "camel":
        name = words[0].lower() + "".join(w.capitalize() for w in words[1:])
    elif case == "pascal":
        name = "".join(w.capitalize() for w in words)
    elif case == "const":
        name = "_".join(words).upper()
    elif case == "sentence":
        name = " ".join(words).capitalize()
    elif case == "title":
        name = " ".join(w.capitalize() for w in words)
    elif case == "lower":
        name = " ".join(words).lower()
    elif case == "upper":
        name = " ".join(words).upper()

    return name
```
===== 26 =====
```
     if case in {"snake", "kebab", "camel", "pascal", "const"}:
         words = _split_strip_string(str(name))
     else:
-        words = _split_string(str(name))
+        words = _split_string(str(None))
 
     if case == "snake":
         name = "_".join(words).lower()
@@ -36,4 +36,4 @@     elif case == "upper":
         name = " ".join(words).upper()
 
-    return name+    return name
```
```
@typechecked
def _convert_case(name: Any, case: str) -> Any:
    """Convert case style of a column name.

    Args:
        name (Any): Column name.
        case (str): Preferred case type, eg snake or camel.

    Returns:
        Any: name with case converted.
    """
    if name in NULL_VALUES:
        name = "header"

    if case in {"snake", "kebab", "camel", "pascal", "const"}:
        words = _split_strip_string(str(name))
    else:
        words = _split_string(str(None))

    if case == "snake":
        name = "_".join(words).lower()
    elif case == "kebab":
        name = "-".join(words).lower()
    elif case == "camel":
        name = words[0].lower() + "".join(w.capitalize() for w in words[1:])
    elif case == "pascal":
        name = "".join(w.capitalize() for w in words)
    elif case == "const":
        name = "_".join(words).upper()
    elif case == "sentence":
        name = " ".join(words).capitalize()
    elif case == "title":
        name = " ".join(w.capitalize() for w in words)
    elif case == "lower":
        name = " ".join(words).lower()
    elif case == "upper":
        name = " ".join(words).upper()

    return name

```
===== 27 =====
```
     if case in {"snake", "kebab", "camel", "pascal", "const"}:
         words = _split_strip_string(str(name))
     else:
-        words = _split_string(str(name))
+        words = _split_strip_string(str(name))  # Incorrect function used, may not split as intended.
 
     if case == "snake":
         name = "_".join(words).lower()
```
```
@typechecked
def _convert_case(name: Any, case: str) -> Any:
    """Convert case style of a column name.

    Args:
        name (Any): Column name.
        case (str): Preferred case type, eg snake or camel.

    Returns:
        Any: name with case converted.
    """
    if name in NULL_VALUES:
        name = "header"

    if case in {"snake", "kebab", "camel", "pascal", "const"}:
        words = _split_strip_string(str(name))
    else:
        words = _split_strip_string(str(name))  # Incorrect function used, may not split as intended.

    if case == "snake":
        name = "_".join(words).lower()
    elif case == "kebab":
        name = "-".join(words).lower()
    elif case == "camel":
        name = words[0].lower() + "".join(w.capitalize() for w in words[1:])
    elif case == "pascal":
        name = "".join(w.capitalize() for w in words)
    elif case == "const":
        name = "_".join(words).upper()
    elif case == "sentence":
        name = " ".join(words).capitalize()
    elif case == "title":
        name = " ".join(w.capitalize() for w in words)
    elif case == "lower":
        name = " ".join(words).lower()
    elif case == "upper":
        name = " ".join(words).upper()

    return name
```
===== 28 =====
```
     if case in {"snake", "kebab", "camel", "pascal", "const"}:
         words = _split_strip_string(str(name))
     else:
-        words = _split_string(str(name))
+        words = str(name).split()  # Splits by whitespace only, losing other delimiters.
 
     if case == "snake":
         name = "_".join(words).lower()
```
```
@typechecked
def _convert_case(name: Any, case: str) -> Any:
    """Convert case style of a column name.

    Args:
        name (Any): Column name.
        case (str): Preferred case type, eg snake or camel.

    Returns:
        Any: name with case converted.
    """
    if name in NULL_VALUES:
        name = "header"

    if case in {"snake", "kebab", "camel", "pascal", "const"}:
        words = _split_strip_string(str(name))
    else:
        words = str(name).split()  # Splits by whitespace only, losing other delimiters.

    if case == "snake":
        name = "_".join(words).lower()
    elif case == "kebab":
        name = "-".join(words).lower()
    elif case == "camel":
        name = words[0].lower() + "".join(w.capitalize() for w in words[1:])
    elif case == "pascal":
        name = "".join(w.capitalize() for w in words)
    elif case == "const":
        name = "_".join(words).upper()
    elif case == "sentence":
        name = " ".join(words).capitalize()
    elif case == "title":
        name = " ".join(w.capitalize() for w in words)
    elif case == "lower":
        name = " ".join(words).lower()
    elif case == "upper":
        name = " ".join(words).upper()

    return name
```
===== 39 =====
```
         words = _split_string(str(name))
 
     if case == "snake":
-        name = "_".join(words).lower()
+        name = "XX_XX".join(words).lower()
     elif case == "kebab":
         name = "-".join(words).lower()
     elif case == "camel":
@@ -36,4 +36,4 @@     elif case == "upper":
         name = " ".join(words).upper()
 
-    return name+    return name
```
```
@typechecked
def _convert_case(name: Any, case: str) -> Any:
    """Convert case style of a column name.

    Args:
        name (Any): Column name.
        case (str): Preferred case type, eg snake or camel.

    Returns:
        Any: name with case converted.
    """
    if name in NULL_VALUES:
        name = "header"

    if case in {"snake", "kebab", "camel", "pascal", "const"}:
        words = _split_strip_string(str(name))
    else:
        words = _split_string(str(name))

    if case == "snake":
        name = "XX_XX".join(words).lower()
    elif case == "kebab":
        name = "-".join(words).lower()
    elif case == "camel":
        name = words[0].lower() + "".join(w.capitalize() for w in words[1:])
    elif case == "pascal":
        name = "".join(w.capitalize() for w in words)
    elif case == "const":
        name = "_".join(words).upper()
    elif case == "sentence":
        name = " ".join(words).capitalize()
    elif case == "title":
        name = " ".join(w.capitalize() for w in words)
    elif case == "lower":
        name = " ".join(words).lower()
    elif case == "upper":
        name = " ".join(words).upper()

    return name

```
===== 53 =====
```
     if case == "snake":
         name = "_".join(words).lower()
     elif case == "kebab":
-        name = "-".join(words).lower()
+        name = "XX-XX".join(words).lower()
     elif case == "camel":
         name = words[0].lower() + "".join(w.capitalize() for w in words[1:])
     elif case == "pascal":
@@ -36,4 +36,4 @@     elif case == "upper":
         name = " ".join(words).upper()
 
-    return name+    return name
```
```
@typechecked
def _convert_case(name: Any, case: str) -> Any:
    """Convert case style of a column name.

    Args:
        name (Any): Column name.
        case (str): Preferred case type, eg snake or camel.

    Returns:
        Any: name with case converted.
    """
    if name in NULL_VALUES:
        name = "header"

    if case in {"snake", "kebab", "camel", "pascal", "const"}:
        words = _split_strip_string(str(name))
    else:
        words = _split_string(str(name))

    if case == "snake":
        name = "_".join(words).lower()
    elif case == "kebab":
        name = "XX-XX".join(words).lower()
    elif case == "camel":
        name = words[0].lower() + "".join(w.capitalize() for w in words[1:])
    elif case == "pascal":
        name = "".join(w.capitalize() for w in words)
    elif case == "const":
        name = "_".join(words).upper()
    elif case == "sentence":
        name = " ".join(words).capitalize()
    elif case == "title":
        name = " ".join(w.capitalize() for w in words)
    elif case == "lower":
        name = " ".join(words).lower()
    elif case == "upper":
        name = " ".join(words).upper()

    return name

```
===== 63 =====
```
     elif case == "kebab":
         name = "-".join(words).lower()
     elif case == "camel":
-        name = words[0].lower() + "".join(w.capitalize() for w in words[1:])
+        name = words[0].lower() + "".join(w.capitalize() for w in words[2:])
     elif case == "pascal":
         name = "".join(w.capitalize() for w in words)
     elif case == "const":
@@ -36,4 +36,4 @@     elif case == "upper":
         name = " ".join(words).upper()
 
-    return name+    return name
```
```
@typechecked
def _convert_case(name: Any, case: str) -> Any:
    """Convert case style of a column name.

    Args:
        name (Any): Column name.
        case (str): Preferred case type, eg snake or camel.

    Returns:
        Any: name with case converted.
    """
    if name in NULL_VALUES:
        name = "header"

    if case in {"snake", "kebab", "camel", "pascal", "const"}:
        words = _split_strip_string(str(name))
    else:
        words = _split_string(str(name))

    if case == "snake":
        name = "_".join(words).lower()
    elif case == "kebab":
        name = "-".join(words).lower()
    elif case == "camel":
        name = words[0].lower() + "".join(w.capitalize() for w in words[2:])
    elif case == "pascal":
        name = "".join(w.capitalize() for w in words)
    elif case == "const":
        name = "_".join(words).upper()
    elif case == "sentence":
        name = " ".join(words).capitalize()
    elif case == "title":
        name = " ".join(w.capitalize() for w in words)
    elif case == "lower":
        name = " ".join(words).lower()
    elif case == "upper":
        name = " ".join(words).upper()

    return name

```
===== 64 =====
```
     elif case == "kebab":
         name = "-".join(words).lower()
     elif case == "camel":
-        name = words[0].lower() + "".join(w.capitalize() for w in words[1:])
+        name = words[0].lower() + "".join(w.lower() for w in words[1:])  # All words in lowercase
     elif case == "pascal":
         name = "".join(w.capitalize() for w in words)
     elif case == "const":
```
```
@typechecked
def _convert_case(name: Any, case: str) -> Any:
    """Convert case style of a column name.

    Args:
        name (Any): Column name.
        case (str): Preferred case type, eg snake or camel.

    Returns:
        Any: name with case converted.
    """
    if name in NULL_VALUES:
        name = "header"

    if case in {"snake", "kebab", "camel", "pascal", "const"}:
        words = _split_strip_string(str(name))
    else:
        words = _split_string(str(name))

    if case == "snake":
        name = "_".join(words).lower()
    elif case == "kebab":
        name = "-".join(words).lower()
    elif case == "camel":
        name = words[0].lower() + "".join(w.lower() for w in words[1:])  # All words in lowercase
    elif case == "pascal":
        name = "".join(w.capitalize() for w in words)
    elif case == "const":
        name = "_".join(words).upper()
    elif case == "sentence":
        name = " ".join(words).capitalize()
    elif case == "title":
        name = " ".join(w.capitalize() for w in words)
    elif case == "lower":
        name = " ".join(words).lower()
    elif case == "upper":
        name = " ".join(words).upper()

    return name
```
===== 65 =====
```
     elif case == "kebab":
         name = "-".join(words).lower()
     elif case == "camel":
-        name = words[0].lower() + "".join(w.capitalize() for w in words[1:])
+        name = words[0].lower() + "XXXX".join(w.capitalize() for w in words[1:])
     elif case == "pascal":
         name = "".join(w.capitalize() for w in words)
     elif case == "const":
@@ -36,4 +36,4 @@     elif case == "upper":
         name = " ".join(words).upper()
 
-    return name+    return name
```
```
@typechecked
def _convert_case(name: Any, case: str) -> Any:
    """Convert case style of a column name.

    Args:
        name (Any): Column name.
        case (str): Preferred case type, eg snake or camel.

    Returns:
        Any: name with case converted.
    """
    if name in NULL_VALUES:
        name = "header"

    if case in {"snake", "kebab", "camel", "pascal", "const"}:
        words = _split_strip_string(str(name))
    else:
        words = _split_string(str(name))

    if case == "snake":
        name = "_".join(words).lower()
    elif case == "kebab":
        name = "-".join(words).lower()
    elif case == "camel":
        name = words[0].lower() + "XXXX".join(w.capitalize() for w in words[1:])
    elif case == "pascal":
        name = "".join(w.capitalize() for w in words)
    elif case == "const":
        name = "_".join(words).upper()
    elif case == "sentence":
        name = " ".join(words).capitalize()
    elif case == "title":
        name = " ".join(w.capitalize() for w in words)
    elif case == "lower":
        name = " ".join(words).lower()
    elif case == "upper":
        name = " ".join(words).upper()

    return name

```
===== 71 =====
```
     elif case == "camel":
         name = words[0].lower() + "".join(w.capitalize() for w in words[1:])
     elif case == "pascal":
-        name = "".join(w.capitalize() for w in words)
+        name = "".join(w.capitalize() for w in words) + "!"
     elif case == "const":
         name = "_".join(words).upper()
     elif case == "sentence":
```
```
@typechecked
def _convert_case(name: Any, case: str) -> Any:
    """Convert case style of a column name.

    Args:
        name (Any): Column name.
        case (str): Preferred case type, eg snake or camel.

    Returns:
        Any: name with case converted.
    """
    if name in NULL_VALUES:
        name = "header"

    if case in {"snake", "kebab", "camel", "pascal", "const"}:
        words = _split_strip_string(str(name))
    else:
        words = _split_string(str(name))

    if case == "snake":
        name = "_".join(words).lower()
    elif case == "kebab":
        name = "-".join(words).lower()
    elif case == "camel":
        name = words[0].lower() + "".join(w.capitalize() for w in words[1:])
    elif case == "pascal":
        name = "".join(w.capitalize() for w in words) + "!"
    elif case == "const":
        name = "_".join(words).upper()
    elif case == "sentence":
        name = " ".join(words).capitalize()
    elif case == "title":
        name = " ".join(w.capitalize() for w in words)
    elif case == "lower":
        name = " ".join(words).lower()
    elif case == "upper":
        name = " ".join(words).upper()

    return name
```
===== 74 =====
```
     elif case == "camel":
         name = words[0].lower() + "".join(w.capitalize() for w in words[1:])
     elif case == "pascal":
-        name = "".join(w.capitalize() for w in words)
+        name = "XXXX".join(w.capitalize() for w in words)
     elif case == "const":
         name = "_".join(words).upper()
     elif case == "sentence":
@@ -36,4 +36,4 @@     elif case == "upper":
         name = " ".join(words).upper()
 
-    return name+    return name
```
```
@typechecked
def _convert_case(name: Any, case: str) -> Any:
    """Convert case style of a column name.

    Args:
        name (Any): Column name.
        case (str): Preferred case type, eg snake or camel.

    Returns:
        Any: name with case converted.
    """
    if name in NULL_VALUES:
        name = "header"

    if case in {"snake", "kebab", "camel", "pascal", "const"}:
        words = _split_strip_string(str(name))
    else:
        words = _split_string(str(name))

    if case == "snake":
        name = "_".join(words).lower()
    elif case == "kebab":
        name = "-".join(words).lower()
    elif case == "camel":
        name = words[0].lower() + "".join(w.capitalize() for w in words[1:])
    elif case == "pascal":
        name = "XXXX".join(w.capitalize() for w in words)
    elif case == "const":
        name = "_".join(words).upper()
    elif case == "sentence":
        name = " ".join(words).capitalize()
    elif case == "title":
        name = " ".join(w.capitalize() for w in words)
    elif case == "lower":
        name = " ".join(words).lower()
    elif case == "upper":
        name = " ".join(words).upper()

    return name

```
===== 77 =====
```
     elif case == "camel":
         name = words[0].lower() + "".join(w.capitalize() for w in words[1:])
     elif case == "pascal":
-        name = "".join(w.capitalize() for w in words)
+        name = words[0].capitalize() + "".join(w for w in words[1:])
     elif case == "const":
         name = "_".join(words).upper()
     elif case == "sentence":
```
```
@typechecked
def _convert_case(name: Any, case: str) -> Any:
    """Convert case style of a column name.

    Args:
        name (Any): Column name.
        case (str): Preferred case type, eg snake or camel.

    Returns:
        Any: name with case converted.
    """
    if name in NULL_VALUES:
        name = "header"

    if case in {"snake", "kebab", "camel", "pascal", "const"}:
        words = _split_strip_string(str(name))
    else:
        words = _split_string(str(name))

    if case == "snake":
        name = "_".join(words).lower()
    elif case == "kebab":
        name = "-".join(words).lower()
    elif case == "camel":
        name = words[0].lower() + "".join(w.capitalize() for w in words[1:])
    elif case == "pascal":
        name = words[0].capitalize() + "".join(w for w in words[1:])
    elif case == "const":
        name = "_".join(words).upper()
    elif case == "sentence":
        name = " ".join(words).capitalize()
    elif case == "title":
        name = " ".join(w.capitalize() for w in words)
    elif case == "lower":
        name = " ".join(words).lower()
    elif case == "upper":
        name = " ".join(words).upper()

    return name
```
===== 81 =====
```
     elif case == "pascal":
         name = "".join(w.capitalize() for w in words)
     elif case == "const":
-        name = "_".join(words).upper()
+        name = "XX_XX".join(words).upper()
     elif case == "sentence":
         name = " ".join(words).capitalize()
     elif case == "title":
@@ -36,4 +36,4 @@     elif case == "upper":
         name = " ".join(words).upper()
 
-    return name+    return name
```
```
@typechecked
def _convert_case(name: Any, case: str) -> Any:
    """Convert case style of a column name.

    Args:
        name (Any): Column name.
        case (str): Preferred case type, eg snake or camel.

    Returns:
        Any: name with case converted.
    """
    if name in NULL_VALUES:
        name = "header"

    if case in {"snake", "kebab", "camel", "pascal", "const"}:
        words = _split_strip_string(str(name))
    else:
        words = _split_string(str(name))

    if case == "snake":
        name = "_".join(words).lower()
    elif case == "kebab":
        name = "-".join(words).lower()
    elif case == "camel":
        name = words[0].lower() + "".join(w.capitalize() for w in words[1:])
    elif case == "pascal":
        name = "".join(w.capitalize() for w in words)
    elif case == "const":
        name = "XX_XX".join(words).upper()
    elif case == "sentence":
        name = " ".join(words).capitalize()
    elif case == "title":
        name = " ".join(w.capitalize() for w in words)
    elif case == "lower":
        name = " ".join(words).lower()
    elif case == "upper":
        name = " ".join(words).upper()

    return name

```
===== 97 =====
```
     elif case == "const":
         name = "_".join(words).upper()
     elif case == "sentence":
-        name = " ".join(words).capitalize()
+        name = "XX XX".join(words).capitalize()
     elif case == "title":
         name = " ".join(w.capitalize() for w in words)
     elif case == "lower":
@@ -36,4 +36,4 @@     elif case == "upper":
         name = " ".join(words).upper()
 
-    return name+    return name
```
```
@typechecked
def _convert_case(name: Any, case: str) -> Any:
    """Convert case style of a column name.

    Args:
        name (Any): Column name.
        case (str): Preferred case type, eg snake or camel.

    Returns:
        Any: name with case converted.
    """
    if name in NULL_VALUES:
        name = "header"

    if case in {"snake", "kebab", "camel", "pascal", "const"}:
        words = _split_strip_string(str(name))
    else:
        words = _split_string(str(name))

    if case == "snake":
        name = "_".join(words).lower()
    elif case == "kebab":
        name = "-".join(words).lower()
    elif case == "camel":
        name = words[0].lower() + "".join(w.capitalize() for w in words[1:])
    elif case == "pascal":
        name = "".join(w.capitalize() for w in words)
    elif case == "const":
        name = "_".join(words).upper()
    elif case == "sentence":
        name = "XX XX".join(words).capitalize()
    elif case == "title":
        name = " ".join(w.capitalize() for w in words)
    elif case == "lower":
        name = " ".join(words).lower()
    elif case == "upper":
        name = " ".join(words).upper()

    return name

```
===== 102 =====
```
     elif case == "sentence":
         name = " ".join(words).capitalize()
     elif case == "title":
-        name = " ".join(w.capitalize() for w in words)
+        name = " ".join(w.capitalize() for w in words) + "!"  # This will add an exclamation mark at the end, altering the intended format.
     elif case == "lower":
         name = " ".join(words).lower()
     elif case == "upper":
```
```
@typechecked
def _convert_case(name: Any, case: str) -> Any:
    """Convert case style of a column name.

    Args:
        name (Any): Column name.
        case (str): Preferred case type, eg snake or camel.

    Returns:
        Any: name with case converted.
    """
    if name in NULL_VALUES:
        name = "header"

    if case in {"snake", "kebab", "camel", "pascal", "const"}:
        words = _split_strip_string(str(name))
    else:
        words = _split_string(str(name))

    if case == "snake":
        name = "_".join(words).lower()
    elif case == "kebab":
        name = "-".join(words).lower()
    elif case == "camel":
        name = words[0].lower() + "".join(w.capitalize() for w in words[1:])
    elif case == "pascal":
        name = "".join(w.capitalize() for w in words)
    elif case == "const":
        name = "_".join(words).upper()
    elif case == "sentence":
        name = " ".join(words).capitalize()
    elif case == "title":
        name = " ".join(w.capitalize() for w in words) + "!"  # This will add an exclamation mark at the end, altering the intended format.
    elif case == "lower":
        name = " ".join(words).lower()
    elif case == "upper":
        name = " ".join(words).upper()

    return name
```
===== 103 =====
```
     elif case == "sentence":
         name = " ".join(words).capitalize()
     elif case == "title":
-        name = " ".join(w.capitalize() for w in words)
+        name = " ".join(w.capitalize() for w in words[:-1])  # This will capitalize all but the last word, leading to inconsistent casing.
     elif case == "lower":
         name = " ".join(words).lower()
     elif case == "upper":
```
```
@typechecked
def _convert_case(name: Any, case: str) -> Any:
    """Convert case style of a column name.

    Args:
        name (Any): Column name.
        case (str): Preferred case type, eg snake or camel.

    Returns:
        Any: name with case converted.
    """
    if name in NULL_VALUES:
        name = "header"

    if case in {"snake", "kebab", "camel", "pascal", "const"}:
        words = _split_strip_string(str(name))
    else:
        words = _split_string(str(name))

    if case == "snake":
        name = "_".join(words).lower()
    elif case == "kebab":
        name = "-".join(words).lower()
    elif case == "camel":
        name = words[0].lower() + "".join(w.capitalize() for w in words[1:])
    elif case == "pascal":
        name = "".join(w.capitalize() for w in words)
    elif case == "const":
        name = "_".join(words).upper()
    elif case == "sentence":
        name = " ".join(words).capitalize()
    elif case == "title":
        name = " ".join(w.capitalize() for w in words[:-1])  # This will capitalize all but the last word, leading to inconsistent casing.
    elif case == "lower":
        name = " ".join(words).lower()
    elif case == "upper":
        name = " ".join(words).upper()

    return name
```
===== 105 =====
```
     elif case == "sentence":
         name = " ".join(words).capitalize()
     elif case == "title":
-        name = " ".join(w.capitalize() for w in words)
+        name = " ".join(w.upper() for w in words)  # This will convert all words to uppercase, which is not the intended behavior.
     elif case == "lower":
         name = " ".join(words).lower()
     elif case == "upper":
```
```
@typechecked
def _convert_case(name: Any, case: str) -> Any:
    """Convert case style of a column name.

    Args:
        name (Any): Column name.
        case (str): Preferred case type, eg snake or camel.

    Returns:
        Any: name with case converted.
    """
    if name in NULL_VALUES:
        name = "header"

    if case in {"snake", "kebab", "camel", "pascal", "const"}:
        words = _split_strip_string(str(name))
    else:
        words = _split_string(str(name))

    if case == "snake":
        name = "_".join(words).lower()
    elif case == "kebab":
        name = "-".join(words).lower()
    elif case == "camel":
        name = words[0].lower() + "".join(w.capitalize() for w in words[1:])
    elif case == "pascal":
        name = "".join(w.capitalize() for w in words)
    elif case == "const":
        name = "_".join(words).upper()
    elif case == "sentence":
        name = " ".join(words).capitalize()
    elif case == "title":
        name = " ".join(w.upper() for w in words)  # This will convert all words to uppercase, which is not the intended behavior.
    elif case == "lower":
        name = " ".join(words).lower()
    elif case == "upper":
        name = " ".join(words).upper()

    return name
```
===== 107 =====
```
     elif case == "sentence":
         name = " ".join(words).capitalize()
     elif case == "title":
-        name = " ".join(w.capitalize() for w in words)
+        name = "XX XX".join(w.capitalize() for w in words)
     elif case == "lower":
         name = " ".join(words).lower()
     elif case == "upper":
         name = " ".join(words).upper()
 
-    return name+    return name
```
```
@typechecked
def _convert_case(name: Any, case: str) -> Any:
    """Convert case style of a column name.

    Args:
        name (Any): Column name.
        case (str): Preferred case type, eg snake or camel.

    Returns:
        Any: name with case converted.
    """
    if name in NULL_VALUES:
        name = "header"

    if case in {"snake", "kebab", "camel", "pascal", "const"}:
        words = _split_strip_string(str(name))
    else:
        words = _split_string(str(name))

    if case == "snake":
        name = "_".join(words).lower()
    elif case == "kebab":
        name = "-".join(words).lower()
    elif case == "camel":
        name = words[0].lower() + "".join(w.capitalize() for w in words[1:])
    elif case == "pascal":
        name = "".join(w.capitalize() for w in words)
    elif case == "const":
        name = "_".join(words).upper()
    elif case == "sentence":
        name = " ".join(words).capitalize()
    elif case == "title":
        name = "XX XX".join(w.capitalize() for w in words)
    elif case == "lower":
        name = " ".join(words).lower()
    elif case == "upper":
        name = " ".join(words).upper()

    return name

```
===== 118 =====
```
     elif case == "title":
         name = " ".join(w.capitalize() for w in words)
     elif case == "lower":
-        name = " ".join(words).lower()
+        name = "XX XX".join(words).lower()
     elif case == "upper":
         name = " ".join(words).upper()
 
-    return name+    return name
```
```
@typechecked
def _convert_case(name: Any, case: str) -> Any:
    """Convert case style of a column name.

    Args:
        name (Any): Column name.
        case (str): Preferred case type, eg snake or camel.

    Returns:
        Any: name with case converted.
    """
    if name in NULL_VALUES:
        name = "header"

    if case in {"snake", "kebab", "camel", "pascal", "const"}:
        words = _split_strip_string(str(name))
    else:
        words = _split_string(str(name))

    if case == "snake":
        name = "_".join(words).lower()
    elif case == "kebab":
        name = "-".join(words).lower()
    elif case == "camel":
        name = words[0].lower() + "".join(w.capitalize() for w in words[1:])
    elif case == "pascal":
        name = "".join(w.capitalize() for w in words)
    elif case == "const":
        name = "_".join(words).upper()
    elif case == "sentence":
        name = " ".join(words).capitalize()
    elif case == "title":
        name = " ".join(w.capitalize() for w in words)
    elif case == "lower":
        name = "XX XX".join(words).lower()
    elif case == "upper":
        name = " ".join(words).upper()

    return name

```
===== 128 =====
```
     elif case == "lower":
         name = " ".join(words).lower()
     elif case == "upper":
-        name = " ".join(words).upper()
+        name = "XX XX".join(words).upper()
 
-    return name+    return name
```
```
@typechecked
def _convert_case(name: Any, case: str) -> Any:
    """Convert case style of a column name.

    Args:
        name (Any): Column name.
        case (str): Preferred case type, eg snake or camel.

    Returns:
        Any: name with case converted.
    """
    if name in NULL_VALUES:
        name = "header"

    if case in {"snake", "kebab", "camel", "pascal", "const"}:
        words = _split_strip_string(str(name))
    else:
        words = _split_string(str(name))

    if case == "snake":
        name = "_".join(words).lower()
    elif case == "kebab":
        name = "-".join(words).lower()
    elif case == "camel":
        name = words[0].lower() + "".join(w.capitalize() for w in words[1:])
    elif case == "pascal":
        name = "".join(w.capitalize() for w in words)
    elif case == "const":
        name = "_".join(words).upper()
    elif case == "sentence":
        name = " ".join(words).capitalize()
    elif case == "title":
        name = " ".join(w.capitalize() for w in words)
    elif case == "lower":
        name = " ".join(words).lower()
    elif case == "upper":
        name = "XX XX".join(words).upper()

    return name

```
===== 129 =====
```
     elif case == "lower":
         name = " ".join(words).lower()
     elif case == "upper":
-        name = " ".join(words).upper()
+        name = "_".join(words).upper()  # This will join words with underscores instead of spaces and convert to uppercase.
 
     return name
```
```
@typechecked
def _convert_case(name: Any, case: str) -> Any:
    """Convert case style of a column name.

    Args:
        name (Any): Column name.
        case (str): Preferred case type, eg snake or camel.

    Returns:
        Any: name with case converted.
    """
    if name in NULL_VALUES:
        name = "header"

    if case in {"snake", "kebab", "camel", "pascal", "const"}:
        words = _split_strip_string(str(name))
    else:
        words = _split_string(str(name))

    if case == "snake":
        name = "_".join(words).lower()
    elif case == "kebab":
        name = "-".join(words).lower()
    elif case == "camel":
        name = words[0].lower() + "".join(w.capitalize() for w in words[1:])
    elif case == "pascal":
        name = "".join(w.capitalize() for w in words)
    elif case == "const":
        name = "_".join(words).upper()
    elif case == "sentence":
        name = " ".join(words).capitalize()
    elif case == "title":
        name = " ".join(w.capitalize() for w in words)
    elif case == "lower":
        name = " ".join(words).lower()
    elif case == "upper":
        name = "_".join(words).upper()  # This will join words with underscores instead of spaces and convert to uppercase.

    return name
```
