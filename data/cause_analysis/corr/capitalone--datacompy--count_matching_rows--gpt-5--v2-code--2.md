https://github.com/capitalone/datacompy/blob/2600d7c93f2656de63b108cdb8d37cbec8eb8bbf/./datacompy/core.py#L452-L464
```
@icontract.snapshot(lambda self: [f"{col}_match" for col in self.intersect_columns() if col not in self.join_columns], name="match_columns")
@icontract.snapshot(lambda self: int(self.intersect_rows.shape[0]), name="intersect_row_count")
@icontract.ensure(lambda result: isinstance(result, (int, np.integer)))
@icontract.ensure(lambda self, result, match_columns: result == int(self.intersect_rows[match_columns].all(axis=1).sum()))
@icontract.ensure(lambda result, intersect_row_count: 0 <= result <= intersect_row_count)
@icontract.ensure(lambda result, intersect_row_count: (intersect_row_count != 0) or (result == 0))
@icontract.ensure(lambda result, match_columns, intersect_row_count: (len(match_columns) != 0) or (result == intersect_row_count))
```
```
limited spec

match_columns
```
failed
```
@icontract.snapshot(lambda self: list(self.intersect_columns()), name="intersect_cols")
@icontract.snapshot(lambda self: list(self.join_columns), name="join_cols")
@icontract.ensure(lambda result, OLD, self: 0 <= result <= self.intersect_rows.shape[0])
@icontract.ensure(lambda OLD, self: all((col + "_match") in self.intersect_rows.columns for col in OLD.intersect_cols if col not in OLD.join_cols))
@icontract.ensure(lambda result, OLD, self: result == self.intersect_rows[[col + "_match" for col in OLD.intersect_cols if col not in OLD.join_cols]].all(axis=1).sum())
@icontract.ensure(lambda result, OLD, self: (len([c for c in OLD.intersect_cols if c not in OLD.join_cols]) == 0) or result <= min(self.intersect_rows[col + "_match"].sum() for col in (c for c in OLD.intersect_cols if c not in OLD.join_cols)))
@icontract.ensure(lambda result, OLD, self: (len([c for c in OLD.intersect_cols if c not in OLD.join_cols]) == 0) or result * len([c for c in OLD.intersect_cols if c not in OLD.join_cols]) <= self.intersect_rows[[col + "_match" for col in OLD.intersect_cols if col not in OLD.join_cols]].sum().sum())
@icontract.ensure(lambda result, self: isinstance(result, (int, np.integer)) and 0 <= result <= self.intersect_rows.shape[0])

```
