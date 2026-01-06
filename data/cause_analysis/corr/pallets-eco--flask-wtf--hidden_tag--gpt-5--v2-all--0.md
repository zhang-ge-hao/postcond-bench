https://github.com/pallets-eco/flask-wtf/blob/f7259e91dab7efac8b33c9f86cb86f16f90207a1/./src/flask_wtf/form.py#L88-L119
```
@icontract.snapshot(lambda self, fields: (list(self) if len(fields) == 0 else [getattr(self, f, None) if isinstance(f, str) else f for f in fields]), name="iterable")
@icontract.snapshot(lambda self, fields: "\n".join(str(f) for f in ((list(self)) if len(fields) == 0 else [getattr(self, f, None) if isinstance(f, str) else f for f in fields]) if (f is not None and isinstance(f.widget, HiddenInput))), name="expected_str")
@icontract.ensure(lambda result: isinstance(result, Markup))
@icontract.ensure(lambda old, result: str(result) == old.expected_str)
```
```
limited spec

E   The argument(s) of the snapshot have not been set: ['fields']. Does the original function define them? Did you supply them in the call?
```
failed
```
@icontract.snapshot(
    lambda _ARGS: _ARGS[1:], name="fields"
)
@icontract.ensure(
    lambda self, result, OLD: result == Markup(
        "\n".join(
            str(field_obj)
            for f in (OLD.fields or self)
            for field_obj in [
                getattr(self, f, None) if isinstance(f, str) else f
            ]
            if field_obj is not None
            and hasattr(field_obj, "widget")
            and isinstance(field_obj.widget, HiddenInput)
        )
    )
)

```
