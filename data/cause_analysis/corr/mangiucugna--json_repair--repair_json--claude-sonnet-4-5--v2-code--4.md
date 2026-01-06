https://github.com/mangiucugna/json_repair/blob/7ca4d6de56ab3824f617e913ee5003171a044578/./src/json_repair/json_repair.py#L60-L104
```
@icontract.ensure(lambda logging, result: not logging or (isinstance(result, tuple) and len(result) == 2), "When logging is True, result must be a tuple of length 2")
@icontract.ensure(lambda return_objects, logging, result: logging or return_objects or isinstance(result, str), "When both logging and return_objects are False, result must be a string")
@icontract.ensure(lambda return_objects, logging, result: (not return_objects or logging) or not isinstance(result, str), "When return_objects is True and logging is False, result should not be a plain string (it's an object)")
```
```
hallucination on semantics

The branch is line 100 `return parsed_json`
the parsed_json could be "".
```
icontract_fail
```
@icontract.snapshot(
    lambda _KWARGS: {
        k: v
        for k, v in _KWARGS.items()
        if k
        not in [
            "json_str",
            "return_objects",
            "skip_json_loads",
            "logging",
            "json_fd",
            "chunk_length",
            "stream_stable",
        ]
    },
    name="kwargs",
)
@icontract.snapshot(
    lambda json_fd: json_fd.tell() if json_fd is not None else None,
    name="fd_pos",
)
@icontract.ensure(
    lambda result,
           json_str,
           return_objects,
           skip_json_loads,
           logging,
           json_fd,
           chunk_length,
           stream_stable,
           OLD,
           _SENTINEL=object(): (
        # 1. 先算出“理论正确”的 parsed_json
        (lambda parsed_json: (
            # 2. 用 parsed_json + return_objects/logging 推出“理论正确”的最终返回值，
            #    然后和实际的 result 做比较
            result
            == (
                (
                    (
                        (parsed_json, [])
                        if (logging and not isinstance(parsed_json, tuple))
                        else parsed_json
                    )
                    if (return_objects or logging)
                    else (
                        ""  # 避免返回仅一对引号
                        if parsed_json == ""
                        else json.dumps(parsed_json, **OLD.kwargs)
                    )
                )
            )
        ))(
            # 这里是 parsed_json 的计算逻辑：
            # - 如果 skip_json_loads=True：与实现保持一致，只走 JSONParser
            # - 否则：先尝试 json.load/json.loads；失败再走 JSONParser
            (
                # skip_json_loads=True：函数本体直接用 JSONParser，所以合同也只用 JSONParser，
                # 不再多做一遍 json.load/json.loads（大幅加速文件场景）
                JSONParser(
                    json_str,
                    json_fd,
                    logging,
                    chunk_length,
                    stream_stable,
                ).parse()
                if skip_json_loads
                else
                # skip_json_loads=False：精确模拟
                (lambda cand: (
                    # 如果 cand 不是 _SENTINEL，说明 json.load/json.loads 成功，
                    # 函数本体就会直接用 cand
                    cand
                    if cand is not _SENTINEL
                    # 否则等价于 except json.JSONDecodeError: parsed_json = parser.parse()
                    else JSONParser(
                        json_str,
                        json_fd,
                        logging,
                        chunk_length,
                        stream_stable,
                    ).parse()
                ))(
                    # cand = json.load(json_fd) 或 json.loads(json_str)，带 try/except
                    (lambda _fd, _s, _sentinel, _old_pos: (
                        lambda _ns: (
                            exec(
                                "import json\n"
                                "if _fd is not None and _old_pos is not None:\n"
                                "    _fd.seek(_old_pos)\n"
                                "try:\n"
                                "    _v = json.load(_fd) if _fd is not None else json.loads(_s)\n"
                                "except json.JSONDecodeError:\n"
                                "    _v = _sentinel\n",
                                {
                                    "json": json,
                                    "_fd": _fd,
                                    "_s": _s,
                                    "_sentinel": _sentinel,
                                    "_old_pos": _old_pos,
                                },
                                _ns,
                            )
                            or _ns["_v"]
                        )
                    )({}))(json_fd, json_str, _SENTINEL, OLD.fd_pos)
                )
            )
        )
    )
)

```
