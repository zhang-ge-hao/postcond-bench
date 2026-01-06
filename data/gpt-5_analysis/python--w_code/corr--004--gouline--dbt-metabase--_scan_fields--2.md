https://github.com/gouline/dbt-metabase/blob/cf581fd3bbe9472d2aaa7ed5725b8c34372089cc/./dbtmetabase/manifest.py#L351-L371
```
@icontract.snapshot(lambda fields: list(fields), name="fields_list")
@icontract.ensure(lambda result, OLD, t, ns: set(result.keys()) == {f for f in OLD.fields_list if f"{ns}.{f}" in t})
@icontract.ensure(lambda result, t, ns: all((f"{ns}.{k}" in t) and (result[k] == (t[f"{ns}.{k}"] if t[f"{ns}.{k}"] is not None else NullValue)) for k in result))
@icontract.ensure(lambda result: all(v is not None for v in result.values()))
```
```
Hallucination.

Post-conds failed on understanding NullValue, while the definition of NullValue is in another file and does not included in the prompt.

https://github.com/gouline/dbt-metabase/blob/cf581fd3bbe9472d2aaa7ed5725b8c34372089cc/dbtmetabase/format.py#L64

This hallucination might be fixed by adding cross-file context.
```
icontract_fail
```
@icontract.snapshot(lambda t: dict(t), name="t_orig")
@icontract.snapshot(lambda fields: list(fields), name="fields_orig")
@icontract.ensure(
    lambda OLD, result, ns: 
        result is not None and isinstance(result, dict)
        and
        set(result.keys()) == {f for f in OLD.fields_orig if f"{ns}.{f}" in OLD.t_orig}
        and
        all(((OLD.t_orig[f"{ns}.{field}"] is None and result[field] is NullValue) or (OLD.t_orig[f"{ns}.{field}"] is not None and result[field] == OLD.t_orig[f"{ns}.{field}"])) for field in result)
)

```
