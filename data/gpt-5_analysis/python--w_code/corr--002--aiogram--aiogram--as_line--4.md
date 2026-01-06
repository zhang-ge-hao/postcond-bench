https://github.com/aiogram/aiogram/blob/4caf56814e22af63248e78c25c9755c7ba51c60d/./aiogram/utils/formatting.py#L603-L619
```
@icontract.ensure(lambda result: isinstance(result, Text))
@icontract.ensure(lambda result, end: result.render()[0].endswith(end))
@icontract.ensure(lambda result, items, end, sep: result._body == tuple(v for i, item in enumerate(items) for v in ((item, sep) if (bool(sep) and i < len(items) - 1) else (item,))) + (end,))
```
```
Limited specification language knowledge.

The method definition is `def as_line(*items: NodeType, ...)`.
Directly use `items` in `ensure` raise error.
```
icontract_fail
```
@icontract.snapshot(lambda _ARGS: tuple(_ARGS), name="ITEMS")
@icontract.snapshot(lambda _KWARGS: _KWARGS.get("sep"), name="SEP")
@icontract.snapshot(lambda _KWARGS: _KWARGS.get("end"), name="END")
@icontract.ensure(lambda result, OLD: result.render()[0] == (OLD.SEP if OLD.SEP is not None else "").join(map(str, OLD.ITEMS)) + (OLD.END if OLD.END is not None else "\n"))
@icontract.ensure(lambda result, OLD: len(result._body) == (2 * len(OLD.ITEMS) if (OLD.SEP if OLD.SEP is not None else "") else len(OLD.ITEMS) + 1))
@icontract.ensure(lambda result, OLD: (OLD.SEP not in result._body) if OLD.SEP is None else True)
```
