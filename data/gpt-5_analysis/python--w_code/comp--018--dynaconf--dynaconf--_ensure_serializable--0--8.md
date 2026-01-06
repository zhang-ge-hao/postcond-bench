https://github.com/dynaconf/dynaconf/blob/09c10d1a91854894986da19fb70f1b54a47cd865/./dynaconf/utils/inspect.py#L303-L320
```
@icontract.ensure(lambda result, data: not isinstance(data, (DataList, list)) or isinstance(result, list))
@icontract.ensure(lambda result, data: not isinstance(data, (DataList, list)) or len(result) == len(data))
@icontract.ensure(lambda result, data: not isinstance(data, (DataList, list)) or all(not isinstance(x, (DataList, DataDict)) for x in result))
@icontract.ensure(lambda result, data: not isinstance(data, (DataList, list)) or all(isinstance(x, (list, dict, int, bool, float, str)) for x in result))
@icontract.ensure(lambda result, data: not isinstance(data, (DataDict, dict)) or isinstance(result, dict))
@icontract.ensure(lambda result, data: not isinstance(data, (DataDict, dict)) or set(result.keys()) == set(data.keys()))
@icontract.ensure(lambda result, data: not isinstance(data, (DataDict, dict)) or all(not isinstance(v, (DataList, DataDict)) for v in result.values()))
@icontract.ensure(lambda result, data: not isinstance(data, (DataDict, dict)) or all(isinstance(v, (list, dict, int, bool, float, str)) for v in result.values()))
@icontract.ensure(lambda result, data: isinstance(data, (DataList, list, DataDict, dict)) or isinstance(result, (int, bool, float, str)))
@icontract.ensure(lambda result, data: not (not isinstance(data, (DataList, list, DataDict, dict)) and isinstance(data, (int, bool, float))) or result == data)
@icontract.ensure(lambda result, data: not (not isinstance(data, (DataList, list, DataDict, dict)) and not isinstance(data, (int, bool, float))) or result == str(data))
```
```
Type Error.

E   AttributeError: 'str' object has no attribute 'values'
```
passed
```
@icontract.snapshot(lambda data: data, name="OLD_data")
@icontract.ensure(lambda OLD, result, data: (
    (
        isinstance(OLD.OLD_data, (DataList, list))
        and isinstance(result, list)
        and len(result) == len(OLD.OLD_data)
        and all(
            (
                isinstance(OLD.OLD_data[i], (DataList, list)) and isinstance(result[i], list)
            )
            or (
                isinstance(OLD.OLD_data[i], (DataDict, dict)) and isinstance(result[i], dict)
            )
            or (
                isinstance(OLD.OLD_data[i], (int, bool, float)) and result[i] == OLD.OLD_data[i]
            )
            or (
                not isinstance(OLD.OLD_data[i], (DataList, list, DataDict, dict, int, bool, float))
                and isinstance(result[i], str)
                and result[i] == str(OLD.OLD_data[i])
            )
            for i in range(len(result))
        )
    )
    or
    (
        isinstance(OLD.OLD_data, (DataDict, dict))
        and isinstance(result, dict)
        and set(result.keys()) == set(OLD.OLD_data.keys())
        and all(
            (
                isinstance(OLD.OLD_data[k], (DataList, list)) and isinstance(result[k], list)
            )
            or (
                isinstance(OLD.OLD_data[k], (DataDict, dict)) and isinstance(result[k], dict)
            )
            or (
                isinstance(OLD.OLD_data[k], (int, bool, float)) and result[k] == OLD.OLD_data[k]
            )
            or (
                not isinstance(OLD.OLD_data[k], (DataList, list, DataDict, dict, int, bool, float))
                and isinstance(result[k], str)
                and result[k] == str(OLD.OLD_data[k])
            )
            for k in result.keys()
        )
    )
    or
    (
        not isinstance(OLD.OLD_data, (DataList, list, DataDict, dict))
        and (
            (isinstance(OLD.OLD_data, (int, bool, float)) and result == OLD.OLD_data)
            or (not isinstance(OLD.OLD_data, (int, bool, float)) and isinstance(result, str) and result == str(OLD.OLD_data))
        )
    )
))
```
===== 8 =====
local_crash
```
     """
     if isinstance(data, (DataList, list)):
         return [_ensure_serializable(v) for v in data]
-    elif isinstance(data, (DataDict, dict)):
+    elif isinstance(None, (DataDict, dict)):
         return {
             k: _ensure_serializable(v)
             for k, v in data.items()  # type: ignore
         }
     else:
-        return data if isinstance(data, (int, bool, float)) else str(data)+        return data if isinstance(data, (int, bool, float)) else str(data)
```
```
def _ensure_serializable(data: DataList | DataDict) -> dict | list:
    """
    Converts box dict or list types to regular python dict or list
    Bypasses other values.
    {
        "foo": [1,2,3, {"a": "A", "b": "B"}],
        "bar": {"a": "A", "b": [1,2,3]},
    }
    """
    if isinstance(data, (DataList, list)):
        return [_ensure_serializable(v) for v in data]
    elif isinstance(None, (DataDict, dict)):
        return {
            k: _ensure_serializable(v)
            for k, v in data.items()  # type: ignore
        }
    else:
        return data if isinstance(data, (int, bool, float)) else str(data)

```
