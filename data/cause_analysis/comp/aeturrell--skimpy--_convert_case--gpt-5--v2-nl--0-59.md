https://github.com/aeturrell/skimpy/blob/9cd3ed61e0d7e6d36cada4c6807ea7452a8c14df/./src/skimpy/__init__.py#L965-L1003
```
@icontract.ensure(
    lambda name, result: (not isinstance(name, str) and result == name) or isinstance(result, str),
    "Non-string names are returned unchanged; string input yields string output.",
)
@icontract.ensure(
    lambda name, result: not isinstance(name, str) or result == result.strip(),
    "String results have no leading or trailing whitespace.",
)
@icontract.ensure(
    lambda name, case, result: not isinstance(name, str) or case != "upper" or result == result.upper(),
    "Upper case style yields an uppercase-only string.",
)
@icontract.ensure(
    lambda name, case, result: not isinstance(name, str) or case != "lower" or result == result.lower(),
    "Lower case style yields a lowercase-only string.",
)
@icontract.ensure(
    lambda name, case, result: not isinstance(name, str) or case != "const" or (result == result.upper() and " " not in result),
    "Const case style yields uppercase with no spaces.",
)
@icontract.ensure(
    lambda name, case, result: not isinstance(name, str) or case != "snake" or (" " not in result and "-" not in result and result == result.lower()),
    "Snake case style yields lowercase with no spaces or hyphens.",
)
@icontract.ensure(
    lambda name, case, result: not isinstance(name, str) or case != "kebab" or (" " not in result and "_" not in result and result == result.lower()),
    "Kebab case style yields lowercase with no spaces or underscores.",
)
@icontract.ensure(
    lambda name, case, result: not isinstance(name, str) or case != "camel" or (" " not in result and "_" not in result and "-" not in result),
    "Camel case style yields no spaces, underscores, or hyphens.",
)
@icontract.ensure(
    lambda name, case, result: not isinstance(name, str) or case != "pascal" or (" " not in result and "_" not in result and "-" not in result and (not any(ch.isalpha() for ch in result) or result[0].isupper())),
    "Pascal case style yields no separators and starts with an uppercase letter when alphabetic.",
)
@icontract.ensure(
    lambda name, case, result: not isinstance(name, str) or case != "title" or ("_" not in result and "-" not in result),
    "Title case style yields no underscores or hyphens.",
)
@icontract.ensure(
    lambda name, case, result: not isinstance(name, str) or case != "sentence" or ("_" not in result and "-" not in result),
    "Sentence case style yields no underscores or hyphens.",
)
```
```
return value - primitive-like/scalar types

return value content

primitive-like/scalar types
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
===== 59: local_crash =====
```
     elif case == "kebab":
         name = "-".join(words).lower()
     elif case == "camel":
-        name = words[0].lower() + "".join(w.capitalize() for w in words[1:])
+        name = "".join(w.capitalize() for w in words)  # Missing the first word's lowercase
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
        name = "".join(w.capitalize() for w in words)  # Missing the first word's lowercase
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
