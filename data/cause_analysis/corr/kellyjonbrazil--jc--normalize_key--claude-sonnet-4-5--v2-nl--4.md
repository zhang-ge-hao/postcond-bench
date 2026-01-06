https://github.com/kellyjonbrazil/jc/blob/9fd13e698709da95f5ee505ff1fde10564544d48/./jc/utils.py#L212-L249
```
@icontract.ensure(lambda result: result == result.lower(), "Result must be lowercase")
@icontract.ensure(lambda result: not any(c in result for c in ' !"#$%&\'()*+,-./:;<=>?@[\\]^`{|}~'), "Result must not contain special characters")
@icontract.ensure(lambda result: '__' not in result, "Result must not contain consecutive underscores")
@icontract.ensure(lambda result: not result.endswith('_'), "Result must not end with underscore")
@icontract.ensure(lambda result: not result.startswith('_'), "Result must not start with underscore")
```
```
hallucination on semantics

The comment does not mention the starting underscore.
```
icontract_fail
```
@icontract.snapshot(lambda data: data, name="orig")
@icontract.snapshot(lambda data: data.strip().lower(), name="base")
@icontract.snapshot(
    lambda data: ''.join(
        ['_' if c in r'''!"#$%&'()*+,-./:;<=>?@[\]^`{|}~ ''' else c
         for c in data.strip().lower()]
    ),
    name="replaced",
)
@icontract.ensure(
    lambda OLD, result:
        result is not None
        and (
            ('_' if OLD.replaced.startswith('_') else '')
            + '_'.join(OLD.replaced.strip('_').replace('_', ' ').split())
        ) == result
        and result == result.lower()
        and '__' not in result
        and not result.endswith('_')
        and ' ' not in result
        and set(result) <= set('abcdefghijklmnopqrstuvwxyz0123456789_')
        and (lambda r: (
            ('_' if r.startswith('_') else '')
            + '_'.join(r.strip('_').replace('_', ' ').split())
        ))(result) == result
)

```
