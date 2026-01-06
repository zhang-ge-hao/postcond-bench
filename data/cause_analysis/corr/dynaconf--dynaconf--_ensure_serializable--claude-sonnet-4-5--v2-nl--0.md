https://github.com/dynaconf/dynaconf/blob/09c10d1a91854894986da19fb70f1b54a47cd865/./dynaconf/utils/inspect.py#L303-L320
```
@icontract.snapshot(lambda data: isinstance(data, DataDict), name="is_dict")
@icontract.snapshot(lambda data: isinstance(data, DataList), name="is_list")
@icontract.snapshot(lambda data: len(data), name="original_length")
@icontract.ensure(lambda is_dict, result: not is_dict or isinstance(result, dict))
@icontract.ensure(lambda is_list, result: not is_list or isinstance(result, list))
@icontract.ensure(lambda result: isinstance(result, (dict, list)))
@icontract.ensure(lambda result: not isinstance(result, (DataDict, DataList)))
@icontract.ensure(lambda original_length, result: len(result) == original_length)
```
```
limited spec

original_length
```
local_crash
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
