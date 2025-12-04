https://github.com/kellyjonbrazil/jc/blob/9fd13e698709da95f5ee505ff1fde10564544d48/./jc/parsers/iftop.py#L202-L246
```
@icontract.snapshot(lambda proc_data: __import__('copy').deepcopy(proc_data), name='old')
@icontract.ensure(lambda OLD, proc_data:
    (not OLD.old and proc_data == OLD.old) or (OLD.old)
)
@icontract.ensure(lambda OLD, proc_data:
    (not OLD.old) or len(proc_data) == len(OLD.old)
)
@icontract.ensure(lambda OLD, proc_data:
    (not OLD.old) or all(
        set(o.keys()) == set(n.keys())
        for o, n in zip(OLD.old, proc_data)
    )
)
@icontract.ensure(lambda OLD, proc_data:
    (not OLD.old) or all(
        all(
            (
                k in [
                    "total_send_rate",
                    "total_receive_rate",
                    "total_send_and_receive_rate",
                    "peak_rate",
                    "cumulative_rate",
                    "clients",
                ]
            ) or (o[k] == n[k])
            for k in o
        )
        for o, n in zip(OLD.old, proc_data)
    )
)
@icontract.ensure(lambda OLD, proc_data:
    (not OLD.old) or all(
        (one_key in o) and (one_key in n)
        and isinstance(o[one_key], dict) and isinstance(n[one_key], dict)
        and set(o[one_key].keys()) == set(n[one_key].keys())
        and all(
            (
                (k not in ["last_2s", "last_10s", "last_40s", "cumulative"]
                 and n[one_key][k] == o[one_key][k])
                or
                (k in ["last_2s", "last_10s", "last_40s", "cumulative"]
                 and isinstance(n[one_key][k], int)
                 and n[one_key][k] == __import__('jc').utils.convert_size_to_int(o[one_key][k]))
            )
            for k in o[one_key]
        )
        for o, n in zip(OLD.old, proc_data)
        for one_key in [
            "total_send_rate",
            "total_receive_rate",
            "total_send_and_receive_rate",
            "peak_rate",
            "cumulative_rate",
        ]
    )
)
@icontract.ensure(lambda OLD, proc_data:
    (not OLD.old) or all(
        ("clients" not in o and "clients" not in n)
        or (
            "clients" in o and "clients" in n
            and isinstance(o["clients"], list) and isinstance(n["clients"], list)
            and len(o["clients"]) == len(n["clients"])
            and all(
                all(
                    (ck == "connections") or oc[ck] == nc[ck]
                    for ck in oc
                )
                for oc, nc in zip(o["clients"], n["clients"])
            )
        )
        for o, n in zip(OLD.old, proc_data)
    )
)
@icontract.ensure(lambda OLD, proc_data:
    (not OLD.old) or all(
        ("clients" not in o and "clients" not in n) or (
            "clients" in o and "clients" in n
            and isinstance(o["clients"], list) and isinstance(n["clients"], list)
            and len(o["clients"]) == len(n["clients"])
            and all(
                set(oc.keys()) == set(nc.keys()) and (
                    ("connections" not in oc and "connections" not in nc) or (
                        "connections" in oc and "connections" in nc
                        and isinstance(oc["connections"], list)
                        and isinstance(nc["connections"], list)
                        and len(oc["connections"]) == len(nc["connections"])
                        and all(
                            set(ocon.keys()) == set(ncon.keys())
                            and all(
                                (
                                    (ck not in ["last_2s", "last_10s", "last_40s", "cumulative"]
                                     and ncon[ck] == ocon[ck])
                                    or
                                    (ck in ["last_2s", "last_10s", "last_40s", "cumulative"]
                                     and isinstance(ncon[ck], int)
                                     and ncon[ck] == __import__('jc').utils.convert_size_to_int(ocon[ck]))
                                )
                                for ck in ocon
                            )
                            for ocon, ncon in zip(
                                oc.get("connections", []),
                                nc.get("connections", []),
                            )
                        )
                    )
                )
                for oc, nc in zip(o.get("clients", []), n.get("clients", []))
            )
        )
        for o, n in zip(OLD.old, proc_data)
    )
)
```
```
@icontract.snapshot(lambda proc_data: __import__('copy').deepcopy(proc_data), name='old')
@icontract.ensure(lambda OLD, proc_data: (not OLD.old and proc_data == OLD.old) or (OLD.old))
@icontract.ensure(lambda OLD, proc_data: (not OLD.old) or len(proc_data) == len(OLD.old))
@icontract.ensure(lambda OLD, proc_data: (not OLD.old) or all(set(o.keys()) == set(n.keys()) for o, n in zip(OLD.old, proc_data)))
@icontract.ensure(lambda OLD, proc_data: (not OLD.old) or all(
    (one_key in o) and (one_key in n) and isinstance(o[one_key], dict) and isinstance(n[one_key], dict) and set(o[one_key].keys()) == set(n[one_key].keys()) and all(
        (
            (k not in ["last_2s", "last_10s", "last_40s", "cumulative"] and n[one_key][k] == o[one_key][k])
            or
            (k in ["last_2s", "last_10s", "last_40s", "cumulative"] and isinstance(n[one_key][k], int) and n[one_key][k] == __import__('jc').utils.convert_size_to_int(o[one_key][k]))
        )
        for k in o[one_key]
    )
    for o, n in zip(OLD.old, proc_data)
    for one_key in ["total_send_rate", "total_receive_rate", "total_send_and_receive_rate", "peak_rate", "cumulative_rate"]
))
@icontract.ensure(lambda OLD, proc_data: (not OLD.old) or all(
    ("clients" not in o and "clients" not in n) or (
        "clients" in o and "clients" in n and isinstance(o["clients"], list) and isinstance(n["clients"], list) and len(o["clients"]) == len(n["clients"]) and all(
            set(oc.keys()) == set(nc.keys()) and (
                ("connections" not in oc and "connections" not in nc) or (
                    "connections" in oc and "connections" in nc and isinstance(oc["connections"], list) and isinstance(nc["connections"], list) and len(oc["connections"]) == len(nc["connections"]) and all(
                        set(ocon.keys()) == set(ncon.keys()) and all(
                            (
                                (ck not in ["last_2s", "last_10s", "last_40s", "cumulative"] and ncon[ck] == ocon[ck])
                                or
                                (ck in ["last_2s", "last_10s", "last_40s", "cumulative"] and isinstance(ncon[ck], int) and ncon[ck] == __import__('jc').utils.convert_size_to_int(ocon[ck]))
                            )
                            for ck in ocon
                        )
                        for ocon, ncon in zip(oc.get("connections", []), nc.get("connections", []))
                    )
                )
            )
            for oc, nc in zip(o.get("clients", []), n.get("clients", []))
        )
    )
    for o, n in zip(OLD.old, proc_data)
))
```
[48]
===== 48 =====
```
                         entry[entry_key][one_nesting_item_key] = jc.utils.convert_size_to_int(entry[entry_key][one_nesting_item_key])
             elif entry_key == "clients":
                 for client in entry[entry_key]:
-                    # print(f"{client=}")
+                    client["index"] = "index"  # Incorrectly assigns a string instead of an integer
                     if "connections" not in client:
                         continue
                     for connection in client["connections"]:
```
```
def _process(proc_data: List[JSONDictType], quiet: bool = False) -> List[JSONDictType]:
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (List of Dictionaries) raw structured data to process

    Returns:

        List of Dictionaries. Structured to conform to the schema.
    """
    string_to_bytes_fields = ["last_2s", "last_10s", "last_40s", "cumulative"]
    one_nesting = [
        "total_send_rate",
        "total_receive_rate",
        "total_send_and_receive_rate",
        "peak_rate",
        "cumulative_rate",
    ]

    if not proc_data:
        return proc_data
    for entry in proc_data:
        # print(f"{entry=}")
        for entry_key in entry:
            # print(f"{entry_key=}")
            if entry_key in one_nesting:
                # print(f"{entry[entry_key]=}")
                for one_nesting_item_key in entry[entry_key]:
                    # print(f"{one_nesting_item_key=}")
                    if one_nesting_item_key in string_to_bytes_fields:
                        entry[entry_key][one_nesting_item_key] = jc.utils.convert_size_to_int(entry[entry_key][one_nesting_item_key])
            elif entry_key == "clients":
                for client in entry[entry_key]:
                    client["index"] = "index"  # Incorrectly assigns a string instead of an integer
                    if "connections" not in client:
                        continue
                    for connection in client["connections"]:
                        # print(f"{connection=}")
                        for connection_key in connection:
                            # print(f"{connection_key=}")
                            if connection_key in string_to_bytes_fields:
                                connection[connection_key] = jc.utils.convert_size_to_int(connection[connection_key])
    return proc_data
```
