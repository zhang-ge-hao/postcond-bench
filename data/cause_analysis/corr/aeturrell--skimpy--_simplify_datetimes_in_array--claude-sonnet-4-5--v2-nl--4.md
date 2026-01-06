https://github.com/aeturrell/skimpy/blob/9cd3ed61e0d7e6d36cada4c6807ea7452a8c14df/./src/skimpy/__init__.py#L183-L207
```
@icontract.snapshot(lambda rows: rows.shape, name="original_shape")
@icontract.ensure(lambda result: isinstance(result, np.ndarray))
@icontract.ensure(lambda result, original_shape: result.shape == original_shape)
@icontract.ensure(lambda result: not any(" 00:00:00" in str(item) for item in result.flat if item is not None))
```
```
limited spec

original_shape
```
local_crash
```
@icontract.snapshot(lambda rows: [list(item) for item in rows], name="rows_before")
@icontract.ensure(lambda OLD, rows: len(rows) == len(OLD.rows_before) and all(len(rows[i]) == len(OLD.rows_before[i]) for i in range(len(rows))))
@icontract.ensure(
    lambda OLD, rows: all(
        (
            isinstance(OLD.rows_before[i][j], pd._libs.tslibs.timestamps.Timestamp)
            and OLD.rows_before[i][j].hour == 0
            and OLD.rows_before[i][j].minute == 0
            and OLD.rows_before[i][j].second == 0
            and isinstance(rows[i][j], str)
            and rows[i][j] == OLD.rows_before[i][j].strftime("%Y-%m-%d")
        )
        or (
            isinstance(OLD.rows_before[i][j], pd._libs.tslibs.timestamps.Timestamp)
            and not (OLD.rows_before[i][j].hour == 0 and OLD.rows_before[i][j].minute == 0 and OLD.rows_before[i][j].second == 0)
            and isinstance(rows[i][j], pd._libs.tslibs.timestamps.Timestamp)
            and rows[i][j] == OLD.rows_before[i][j]
        )
        or (
            not isinstance(OLD.rows_before[i][j], pd._libs.tslibs.timestamps.Timestamp)
            and rows[i][j] == OLD.rows_before[i][j]
        )
        for i in range(len(OLD.rows_before))
        for j in range(len(OLD.rows_before[i]))
    )
)
```
