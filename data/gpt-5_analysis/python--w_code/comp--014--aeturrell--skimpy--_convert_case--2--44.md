https://github.com/aeturrell/skimpy/blob/9cd3ed61e0d7e6d36cada4c6807ea7452a8c14df/./src/skimpy/__init__.py#L965-L1003
```
@icontract.ensure(lambda result: isinstance(result, str))
@icontract.ensure(lambda result: len(result) > 0)
@icontract.ensure(lambda result, case: case != "snake" or (" " not in result and "-" not in result and result == result.lower() and all(seg != "" for seg in result.split("_"))))
@icontract.ensure(lambda result, case: case != "kebab" or (" " not in result and "_" not in result and result == result.lower() and all(seg != "" for seg in result.split("-"))))
@icontract.ensure(lambda result, case: case != "camel" or (" " not in result and "_" not in result and "-" not in result and (len(result) == 0 or result[:1] == result[:1].lower())))
@icontract.ensure(lambda result, case: case != "pascal" or (" " not in result and "_" not in result and "-" not in result and (len(result) == 0 or result[:1] == result[:1].upper())))
@icontract.ensure(lambda result, case: case != "const" or (" " not in result and "-" not in result and result == result.upper() and all(seg != "" for seg in result.split("_"))))
@icontract.ensure(lambda result, case: case != "sentence" or result == result.capitalize())
@icontract.ensure(lambda result, case: case != "title" or ("_" not in result and "-" not in result and " ".join(part.capitalize() for part in result.split(" ")) == result))
@icontract.ensure(lambda result, case: case != "lower" or result == result.lower())
@icontract.ensure(lambda result, case: case != "upper" or result == result.upper())
```
```
Type error.

E   TypeError: argument of type 'NoneType' is not iterable
```
passed
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
===== 44 =====
local_crash
```
         words = _split_string(str(name))
 
     if case == "snake":
-        name = "_".join(words).lower()
+        name = None
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
        name = None
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
