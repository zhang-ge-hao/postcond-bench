https://github.com/dynaconf/dynaconf/blob/09c10d1a91854894986da19fb70f1b54a47cd865/./dynaconf/utils/__init__.py#L146-L165
```
@icontract.snapshot(lambda names: None if names is None else list(names), name="old_names")
@icontract.ensure(lambda result, obj, names: (obj is None or not names) implies result is None)
@icontract.ensure(lambda result, obj, names: obj is not None and names is not None and len(names) == 1 and ("[" not in names[0]) implies result == getattr(obj, names[0], None))
@icontract.ensure(lambda result, obj, names: obj is not None and names is not None and len(names) == 1 and ("[" in names[0]) and hasattr(obj, "__len__") and hasattr(obj, "__getitem__") implies (
    result == (obj[int(names[0].replace("[", "").replace("]", ""))] if int(names[0].replace("[", "").replace("]", "")) < len(obj) else [])
))
@icontract.ensure(lambda result, obj, names: obj is not None and names is not None and len(names) > 1 and ("[" not in names[0]) implies (
    result == recursive_get(getattr(obj, names[0], None), names[1:])
))
@icontract.ensure(lambda result, obj, names: obj is not None and names is not None and len(names) > 1 and ("[" in names[0]) and hasattr(obj, "__len__") and hasattr(obj, "__getitem__") implies (
    result == recursive_get(
        (obj[int(names[0].replace("[", "").replace("]", ""))] if int(names[0].replace("[", "").replace("]", "")) < len(obj) else []),
        names[1:]
    )
))
@icontract.ensure(lambda old_names, names: (names is None and old_names is None) or (names == old_names))
```
```
syntax error

E   SyntaxError: invalid syntax. Perhaps you forgot a comma?
```
syntax_error
```
@icontract.snapshot(lambda obj, names: None if (not names or obj is None) else __import__("functools").reduce(  # compute the expected value by walking the names
    lambda acc, name: (
        (lambda idx: acc[idx] if hasattr(acc, "__len__") and idx < len(acc) else [])(int(name.replace("[", "").replace("]", "")))
        if "[" in name else getattr(acc, name, None)
    ) if acc is not None else None,
    names,
    obj
), name="expected")
@icontract.ensure(lambda OLD, result: result == OLD.expected)
```
