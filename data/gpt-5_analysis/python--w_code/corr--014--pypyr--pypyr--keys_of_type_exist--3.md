https://github.com/pypyr/pypyr/blob/b3e8f8c6063c11e37c1c762b89b4cd8620460c79/./pypyr/context.py#L474-L507
```
@icontract.ensure(lambda result: isinstance(result, tuple))
@icontract.ensure(lambda result: all(isinstance(r, ContextItemInfo) for r in result))
@icontract.ensure(lambda result, keys: len(result) == len(keys))
@icontract.ensure(lambda result, keys: all(r.key == k[0] for r, k in zip(result, keys)))
@icontract.ensure(lambda result, keys: all(r.expected_type == k[1] for r, k in zip(result, keys)))
@icontract.ensure(lambda self, result: all((r.key in self) == r.key_in_context for r in result))
@icontract.ensure(lambda self, result: all((r.is_expected_type is None) if not r.key_in_context else (r.is_expected_type == isinstance(self[r.key], r.expected_type)) for r in result))
@icontract.ensure(lambda self, result: all((not r.key_in_context and r.has_value is False) or (r.key_in_context and (r.has_value == (self[r.key] is not None))) for r in result))
@icontract.ensure(lambda result: all((isinstance(r.is_expected_type, bool) or r.is_expected_type is None) and isinstance(r.has_value, bool) for r in result))
```
```
Limited specification language knowledge.

`def keys_of_type_exist(self, *keys):`
```
icontract_fail
```
@icontract.ensure(
    lambda result: isinstance(result, tuple)
)
@icontract.ensure(
    lambda result: all(isinstance(item, ContextItemInfo) for item in result)
)
@icontract.ensure(
    lambda _ARGS, result: len(result) == len(_ARGS) - 1
)
@icontract.ensure(
    lambda _ARGS, result: all(
        item.key == pair[0]
        for item, pair in zip(result, _ARGS[1:])
    )
)
@icontract.ensure(
    lambda _ARGS, result: all(
        item.expected_type == pair[1]
        for item, pair in zip(result, _ARGS[1:])
    )
)
@icontract.ensure(
    lambda result: all(
        isinstance(item.key_in_context, bool)
        for item in result
    )
)
@icontract.ensure(
    lambda self, result: all(
        item.key_in_context == (item.key in self)
        for item in result
    )
)
@icontract.ensure(
    lambda result: all(
        item.key_in_context or (item.is_expected_type is None)
        for item in result
    )
)
@icontract.ensure(
    lambda self, result: all(
        (not (item.key_in_context and item.key in self))
        or (item.is_expected_type
            == isinstance(self[item.key], item.expected_type))
        for item in result
    )
)
@icontract.ensure(
    lambda result: all(
        isinstance(item.has_value, bool)
        for item in result
    )
)
@icontract.ensure(
    lambda self, result: all(
        item.has_value
        == (item.key_in_context and item.key in self and self[item.key] is not None)
        for item in result
    )
)

```
