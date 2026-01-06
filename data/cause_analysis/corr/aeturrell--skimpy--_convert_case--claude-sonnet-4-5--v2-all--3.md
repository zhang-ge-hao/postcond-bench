https://github.com/aeturrell/skimpy/blob/9cd3ed61e0d7e6d36cada4c6807ea7452a8c14df/./src/skimpy/__init__.py#L965-L1003
```
@icontract.ensure(lambda result: isinstance(result, str) or result in NULL_VALUES)
@icontract.ensure(lambda result, name, case: result == "header" if (name in NULL_VALUES and case in {"snake", "kebab", "camel", "lower"}) else True)
@icontract.ensure(lambda result, name, case: result == "HEADER" if (name in NULL_VALUES and case in {"const", "upper"}) else True)
@icontract.ensure(lambda result, name, case: result == "Header" if (name in NULL_VALUES and case in {"pascal", "sentence", "title"}) else True)
@icontract.ensure(lambda result, case: "_" not in result if case == "camel" else True)
@icontract.ensure(lambda result, case: "_" not in result if case == "pascal" else True)
@icontract.ensure(lambda result, case: "-" not in result if case == "kebab" or "_" not in result else True)
@icontract.ensure(lambda result, case: result.isupper() or "_" in result if case == "const" else True)
@icontract.ensure(lambda result, case: " " in result or len(result) <= 1 or result in {"header", "Header", "HEADER"} if case in {"sentence", "title", "lower", "upper"} else True)
```
```
hallucination on semantics

@icontract.ensure(lambda result, case: "-" not in result if case == "kebab" or "_" not in result else True)

the will be

@icontract.ensure(lambda result, case: ("-" not in result) if (case == "kebab" or "_" not in result) else True)

correct

@icontract.ensure(lambda result, case: ("_" not in result) if case == "kebab" else ("-" not in result))

```
icontract_fail
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
