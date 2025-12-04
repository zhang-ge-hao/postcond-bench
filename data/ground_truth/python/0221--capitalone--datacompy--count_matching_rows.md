https://github.com/capitalone/datacompy/blob/2600d7c93f2656de63b108cdb8d37cbec8eb8bbf/./datacompy/core.py#L452-L464
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
```
@icontract.snapshot(lambda self: list(self.intersect_columns()), name="intersect_cols")
@icontract.snapshot(lambda self: list(self.join_columns), name="join_cols")
@icontract.ensure(lambda result, OLD, self: 0 <= result <= self.intersect_rows.shape[0])
@icontract.ensure(lambda OLD, self: all((col + "_match") in self.intersect_rows.columns for col in OLD.intersect_cols if col not in OLD.join_cols))
@icontract.ensure(lambda result, OLD, self: result == self.intersect_rows[[col + "_match" for col in OLD.intersect_cols if col not in OLD.join_cols]].all(axis=1).sum())
@icontract.ensure(lambda result, OLD, self: (len([c for c in OLD.intersect_cols if c not in OLD.join_cols]) == 0) or result <= min(self.intersect_rows[col + "_match"].sum() for col in (c for c in OLD.intersect_cols if c not in OLD.join_cols)))
@icontract.ensure(lambda result, OLD, self: (len([c for c in OLD.intersect_cols if c not in OLD.join_cols]) == 0) or result * len([c for c in OLD.intersect_cols if c not in OLD.join_cols]) <= self.intersect_rows[[col + "_match" for col in OLD.intersect_cols if col not in OLD.join_cols]].sum().sum())
```
[8]
===== 8 =====
```
         for column in self.intersect_columns():
             if column not in self.join_columns:
                 match_columns.append(column + "_match")
-        return self.intersect_rows[match_columns].all(axis=1).sum()+        return self.intersect_rows[match_columns].sum()
```
```
    def count_matching_rows(self) -> int:
        """Count the number of rows match (on overlapping fields).

        Returns
        -------
        int
            Number of matching rows
        """
        match_columns = []
        for column in self.intersect_columns():
            if column not in self.join_columns:
                match_columns.append(column + "_match")
        return self.intersect_rows[match_columns].sum()
```
