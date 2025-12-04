https://github.com/gouline/dbt-metabase/blob/cf581fd3bbe9472d2aaa7ed5725b8c34372089cc/./dbtmetabase/manifest.py#L351-L371
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
```
@icontract.snapshot(lambda t: dict(t), name="t_orig")
@icontract.snapshot(lambda fields: list(fields), name="fields_orig")
@icontract.ensure(lambda result: isinstance(result, dict))
@icontract.ensure(lambda OLD, result, ns: set(result.keys()) == {f for f in OLD.fields_orig if f"{ns}.{f}" in OLD.t_orig})
@icontract.ensure(lambda OLD, result, ns: all(((OLD.t_orig[f"{ns}.{field}"] is None and result[field] is NullValue) or (OLD.t_orig[f"{ns}.{field}"] is not None and result[field] == OLD.t_orig[f"{ns}.{field}"])) for field in result))
```
[0]
===== 0 =====
```
             Mapping: Field values.
         """
 
-        vals = {}
+        vals = None
         for field in fields:
             if f"{ns}.{field}" in t:
                 value = t[f"{ns}.{field}"]
                 vals[field] = value if value is not None else NullValue
-        return vals+        return vals
```
```
    @staticmethod
    def _scan_fields(
        t: Mapping, fields: Iterable[str], ns: str
    ) -> MutableMapping[str, Any]:
        """Reads meta fields from a schem object.

        Args:
            t (Mapping): Target to scan for fields.
            fields (Iterable): List of fields to accept.
            ns (str): Field namespace (separated by .).

        Returns:
            Mapping: Field values.
        """

        vals = None
        for field in fields:
            if f"{ns}.{field}" in t:
                value = t[f"{ns}.{field}"]
                vals[field] = value if value is not None else NullValue
        return vals

```
