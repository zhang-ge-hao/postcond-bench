https://github.com/capitalone/datacompy/blob/2600d7c93f2656de63b108cdb8d37cbec8eb8bbf/./datacompy/polars.py#L1104-L1132
```
@icontract.snapshot(lambda column: column.to_list(), name="orig")
@icontract.snapshot(lambda column: str(column.dtype), name="orig_dtype")
@icontract.ensure(lambda result, column: len(result) == len(column))
@icontract.ensure(lambda result, OLD: [x is None for x in result.to_list()] == [x is None for x in OLD.orig])
@icontract.ensure(lambda result, OLD: (("Utf8" in OLD.orig_dtype) or ("String" in OLD.orig_dtype)) or result.to_list() == OLD.orig)
@icontract.ensure(lambda result, OLD: ("Categorical" not in OLD.orig_dtype) or result.to_list() == OLD.orig)
@icontract.ensure(lambda result, OLD, ignore_case, ignore_spaces: (ignore_case or ignore_spaces) or result.to_list() == OLD.orig)
@icontract.ensure(lambda result, OLD, ignore_case, ignore_spaces: (not (ignore_case and not ignore_spaces and (("Utf8" in OLD.orig_dtype) or ("String" in OLD.orig_dtype)) and ("Categorical" not in OLD.orig_dtype))) or all((r == (o.upper() if isinstance(o, str) else o)) for o, r in zip(OLD.orig, result.to_list())))
@icontract.ensure(lambda result, OLD, ignore_case, ignore_spaces: (not (ignore_spaces and not ignore_case and (("Utf8" in OLD.orig_dtype) or ("String" in OLD.orig_dtype)) and ("Categorical" not in OLD.orig_dtype))) or all((r == (__import__('re').sub(r"\s+", "", o) if isinstance(o, str) else o)) for o, r in zip(OLD.orig, result.to_list())))
@icontract.ensure(lambda result, OLD, ignore_case, ignore_spaces: (not (ignore_spaces and ignore_case and (("Utf8" in OLD.orig_dtype) or ("String" in OLD.orig_dtype)) and ("Categorical" not in OLD.orig_dtype))) or all((r == (__import__('re').sub(r"\s+", "", o).upper() if isinstance(o, str) else o)) for o, r in zip(OLD.orig, result.to_list())))
```
```
Corner case missed.

@icontract.ensure(lambda result, OLD, ignore_case, ignore_spaces:
    (ignore_case or ignore_spaces) or result.to_list() == OLD.orig
)

However, nan in the lists. In python, nan == nan is False.
Failed due to limited domain knowledge about this.
```
icontract_fail
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
