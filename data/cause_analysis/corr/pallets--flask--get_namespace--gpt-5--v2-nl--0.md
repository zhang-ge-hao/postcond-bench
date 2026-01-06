https://github.com/pallets/flask/blob/330123258e8c3dc391cbe55ab1ed94891ca83af3/./src/flask/config.py#L323-L364
```
@icontract.snapshot(lambda self: list(self.items()), name="items_before")
@icontract.ensure(
    lambda result, namespace, lowercase, trim_namespace, items_before:
        set(result.keys()) == {
            (
                ((k[len(namespace):] if trim_namespace else k).lower()
                 if lowercase else (k[len(namespace):] if trim_namespace else k))
            )
            for (k, _v) in items_before
            if k.startswith(namespace)
        }
)
@icontract.ensure(
    lambda result, namespace, lowercase, trim_namespace, items_before:
        all(
            result[tkey] == next(
                v for (k, v) in reversed(items_before)
                if k.startswith(namespace) and (
                    ((k[len(namespace):] if trim_namespace else k).lower()
                     if lowercase else (k[len(namespace):] if trim_namespace else k))
                ) == tkey
            )
            for tkey in result.keys()
        )
)
@icontract.ensure(lambda result: isinstance(result, dict))
@icontract.ensure(lambda result, lowercase: (not lowercase) or all(k == k.lower() for k in result.keys()))
```
```
limited spec

E   The argument(s) of the contract condition have not been set: ['items_before']. Does the original function define them? Did you supply them in the call?
```
failed
```
@icontract.snapshot(lambda self: dict(self))
@icontract.ensure(lambda result, OLD, namespace, lowercase, trim_namespace: result == {(((k[len(namespace):] if trim_namespace else k).lower() if lowercase else (k[len(namespace):] if trim_namespace else k))): v for k, v in OLD.self.items() if k.startswith(namespace)})
```
