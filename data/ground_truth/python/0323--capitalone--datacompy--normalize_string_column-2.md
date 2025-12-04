https://github.com/capitalone/datacompy/blob/2600d7c93f2656de63b108cdb8d37cbec8eb8bbf/./datacompy/polars.py#L1104-L1132
```
@icontract.snapshot(lambda column: column.to_list(), name="old_values")
@icontract.snapshot(lambda column: str(column.dtype.base_type()), name="old_base_type")
@icontract.ensure(
    lambda OLD, result, ignore_spaces, ignore_case: 
        result is not None
        and
        len(result) == len(OLD.old_values)
        and
        [repr(x) for x in result.to_list()] == [
            (
                repr(None)
                if v is None
                else (
                    repr(
                        ((v.strip() if ignore_spaces else v).upper() if ignore_case
                        else (v.strip() if ignore_spaces else v))
                    )
                    if str(OLD.old_base_type) in STRING_TYPE
                    else repr(v)
                )
            )
            for v in OLD.old_values
        ]
)
```
```
@icontract.snapshot(lambda column: column.to_list(), name="old_values")
@icontract.snapshot(lambda column: str(column.dtype.base_type()), name="old_base_type")
@icontract.ensure(lambda result: result is not None)
@icontract.ensure(lambda OLD, result: len(result) == len(OLD.old_values))
@icontract.ensure(
    lambda OLD, result, ignore_spaces, ignore_case:
    [repr(x) for x in result.to_list()] == [
        (
            repr(None)
            if v is None
            else (
                repr(
                    ((v.strip() if ignore_spaces else v).upper() if ignore_case
                     else (v.strip() if ignore_spaces else v))
                )
                if str(OLD.old_base_type) in STRING_TYPE
                else repr(v)
            )
        )
        for v in OLD.old_values
    ]
)
```
[13]
===== 13 =====
```
         if ignore_spaces:
             column = column.str.strip_chars()
         if ignore_case:
-            column = column.str.to_uppercase()
-    return column+            column = None
+    return column
```
```
def normalize_string_column(
    column: pl.Series, ignore_spaces: bool, ignore_case: bool
) -> pl.Series:
    """Normalize a string column by converting to upper case and stripping whitespace.

    Parameters
    ----------
    column : pl.Series
        The column to normalize
    ignore_spaces : bool
        Whether to ignore spaces when normalizing
    ignore_case : bool
        Whether to ignore case when normalizing

    Returns
    -------
    pl.Series
        The normalized column

    Notes
    -----
    Will not operate on categorical columns.
    """
    if str(column.dtype.base_type()) in STRING_TYPE:
        if ignore_spaces:
            column = column.str.strip_chars()
        if ignore_case:
            column = None
    return column

```
