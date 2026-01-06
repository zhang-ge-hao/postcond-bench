https://github.com/dynaconf/dynaconf/blob/09c10d1a91854894986da19fb70f1b54a47cd865/./dynaconf/utils/inspect.py#L303-L320
```
@icontract.snapshot(lambda data: isinstance(data, DataList), name="is_dl")
@icontract.snapshot(lambda data: isinstance(data, DataDict), name="is_dd")
@icontract.snapshot(lambda data: list(data) if isinstance(data, DataList) else None, name="dl_items")
@icontract.snapshot(lambda data: [("list" if isinstance(x, DataList) else "dict" if isinstance(x, DataDict) else "other") for x in data] if isinstance(data, DataList) else None, name="dl_kinds")
@icontract.snapshot(lambda data: set(data.keys()) if isinstance(data, DataDict) else None, name="dd_keys")
@icontract.snapshot(lambda data: {k: ("list" if isinstance(data[k], DataList) else "dict" if isinstance(data[k], DataDict) else "other") for k in data.keys()} if isinstance(data, DataDict) else None, name="dd_kinds")
@icontract.ensure(lambda result: not isinstance(result, (DataList, DataDict)))
@icontract.ensure(lambda result, OLD: (not OLD.is_dl) or isinstance(result, list))
@icontract.ensure(lambda result, OLD: (not OLD.is_dd) or isinstance(result, dict))
@icontract.ensure(lambda result, OLD: (not OLD.is_dl) or (len(result) == len(OLD.dl_items)))
@icontract.ensure(lambda result, OLD: (not OLD.is_dd) or (set(result.keys()) == OLD.dd_keys))
@icontract.ensure(lambda result, OLD: (not OLD.is_dl) or all((OLD.dl_kinds[i] == "other" and result[i] is OLD.dl_items[i]) or (OLD.dl_kinds[i] == "list" and isinstance(result[i], list)) or (OLD.dl_kinds[i] == "dict" and isinstance(result[i], dict)) for i in range(len(OLD.dl_items))))
@icontract.ensure(lambda result, OLD, data: (not OLD.is_dd) or all((OLD.dd_kinds[k] == "other" and result[k] is data[k]) or (OLD.dd_kinds[k] == "list" and isinstance(result[k], list)) or (OLD.dd_kinds[k] == "dict" and isinstance(result[k], dict)) for k in OLD.dd_keys))
@icontract.ensure(lambda result, OLD: (not OLD.is_dl) or all(not isinstance(x, (DataList, DataDict)) for x in result))
@icontract.ensure(lambda result, OLD: (not OLD.is_dd) or all(not isinstance(v, (DataList, DataDict)) for v in result.values()))
```
```
Hallucination.

What is "other"?
```
icontract_fail
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
