https://github.com/pypyr/pypyr/blob/b3e8f8c6063c11e37c1c762b89b4cd8620460c79/./pypyr/context.py#L474-L507
```
@icontract.ensure(lambda keys, result: len(result) == len(keys))
@icontract.ensure(lambda keys, result: all(
    result[i].key == keys[i][0] and result[i].expected_type == keys[i][1]
    for i in range(len(keys))
))
@icontract.ensure(lambda self, keys, result: all(
    result[i].key_in_context == (keys[i][0] in self)
    for i in range(len(keys))
))
@icontract.ensure(lambda self, result: all(
    (item.is_expected_type is None if not item.key_in_context
     else item.is_expected_type == isinstance(self[item.key], item.expected_type))
    for item in result
))
@icontract.ensure(lambda self, result: all(
    item.has_value == (item.key_in_context and self[item.key] is not None)
    for item in result
))
```
```
limited spec

*keys
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
