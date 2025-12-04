https://github.com/kellyjonbrazil/jc/blob/9fd13e698709da95f5ee505ff1fde10564544d48/./jc/utils.py#L212-L249
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
```
@icontract.snapshot(lambda data: data, name="orig")
@icontract.snapshot(lambda data: data.strip().lower(), name="base")
@icontract.snapshot(lambda data: ''.join(['_' if c in r'''!"#$%&'()*+,-./:;<=>?@[\]^`{|}~ ''' else c for c in data.strip().lower()]), name="replaced")
@icontract.ensure(lambda OLD, result: (('_' if OLD.replaced.startswith('_') else '') + '_'.join(OLD.replaced.strip('_').replace('_', ' ').split())) == result)
@icontract.ensure(lambda OLD, result: result == result.lower())
@icontract.ensure(lambda OLD, result: '__' not in result)
@icontract.ensure(lambda OLD, result: not result.endswith('_'))
@icontract.ensure(lambda OLD, result: ' ' not in result)
@icontract.ensure(lambda OLD, result: set(result) <= set('abcdefghijklmnopqrstuvwxyz0123456789_'))
@icontract.ensure(lambda OLD, result: (lambda r: (('_' if r.startswith('_') else '') + '_'.join(r.strip('_').replace('_', ' ').split()))) (result) == result)
```
[34]
===== 34 =====
```
     data = '_'.join(data.split())
 
     if initial_underscore:
-        data = '_' + data
+        data = None
 
-    return data+    return data
```
```
def normalize_key(data: str) -> str:
    r"""
    Normalize a key name by shifting to lower-case and converting special
    characters to underscores.

    Special characters are defined as `space` and the following:

        !"#$%&'()*+,-./:;<=>?@[\]^`{|}~

    This is a lossy algorithm. Repeating and trailing underscores are
    removed.

    Parameters:

        data:       (string) Input value

    Returns:

        string
    """
    special = r'''!"#$%&'()*+,-./:;<=>?@[\]^`{|}~ '''
    initial_underscore = False
    data = data.strip().lower()

    for special_char in special:
        data = data.replace(special_char, '_')

    if data.startswith('_'):
        initial_underscore = True

    # swap back to space so split() will compress multiple consecutive down to one
    data = data.strip('_').replace('_', ' ')
    data = '_'.join(data.split())

    if initial_underscore:
        data = None

    return data

```
