https://github.com/TomasTomecek/sen/blob/3a31c949f3732910a1f2e58ef8ee88c4758c1107/./sen/tui/widgets/table.py#L11-L32
```
@icontract.snapshot(lambda table: tuple(tuple(row) for row in table), name="orig_table")
@icontract.snapshot(lambda size: size, name="orig_size")
@icontract.ensure(lambda result: isinstance(result, dict))
@icontract.ensure(lambda result: all(isinstance(k, int) and k >= 0 for k in result.keys()))
@icontract.ensure(lambda result: all(isinstance(v, int) and v >= 0 for v in result.values()))
@icontract.ensure(lambda result, table: all(any(len(row) > k for row in table) for k in result.keys()))
@icontract.ensure(lambda result, table: len(result) <= max((len(row) for row in table), default=0))
@icontract.ensure(lambda result, table: (max((len(row) for row in table), default=0) == 0) == (len(result) == 0))
@icontract.ensure(lambda OLD, table: OLD.orig_table == tuple(tuple(row) for row in table))
@icontract.ensure(lambda OLD, size: OLD.orig_size == size)
```
```
Type Error.

E   TypeError: 'ResponsiveRowWidget' object is not iterable
```
icontract_fail
```
@icontract.snapshot(lambda _ARGS: _ARGS[0], name="table")
@icontract.snapshot(lambda _ARGS: _ARGS[1], name="size")
@icontract.ensure(lambda OLD, result, table, size: isinstance(result, dict))
@icontract.ensure(lambda OLD, result, table, size: all(isinstance(k, int) and k >= 0 for k in result.keys()))
@icontract.ensure(lambda OLD, result, table, size: all(isinstance(v, int) and v >= 0 for v in result.values()))
@icontract.ensure(lambda OLD, result, table, size: (not OLD.table and result == {0: 1}) or (OLD.table and (max((len(r.widgets) for r in OLD.table), default=0) == 0 and result == {0: 1}) or (OLD.table and max((len(r.widgets) for r in OLD.table), default=0) > 0)))
@icontract.ensure(lambda OLD, result, table, size: (not OLD.table) or (max((len(r.widgets) for r in OLD.table), default=0) == 0 and result == {0: 1}) or (set(result.keys()) == set(range(max(len(r.widgets) for r in OLD.table)))))
@icontract.ensure(lambda OLD, result, table, size: (not OLD.table) or (max((len(r.widgets) for r in OLD.table), default=0) == 0) or all(
    any(idx < len(r.widgets) for r in OLD.table) and
    result[idx] == max([r.widgets[idx].pack((OLD.size[0],))[0] for r in OLD.table if idx < len(r.widgets)])
    for idx in result.keys()
))
```
