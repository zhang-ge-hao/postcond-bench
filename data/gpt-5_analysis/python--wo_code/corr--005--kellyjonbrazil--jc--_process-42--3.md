https://github.com/kellyjonbrazil/jc/blob/9fd13e698709da95f5ee505ff1fde10564544d48/./jc/parsers/iftop.py#L202-L246
```
@icontract.ensure(lambda result: isinstance(result, list))
@icontract.ensure(lambda result: all(isinstance(item, dict) for item in result))
@icontract.ensure(lambda result, proc_data: result is not proc_data)
@icontract.ensure(lambda result, proc_data: len(result) == len(proc_data))
@icontract.ensure(lambda result: all(isinstance(item.get('device'), str) and isinstance(item.get('ip_address'), str) and isinstance(item.get('mac_address'), str) for item in result))
@icontract.ensure(lambda result: all('clients' in item and isinstance(item['clients'], list) for item in result))
@icontract.ensure(lambda result: all(all(isinstance(client, dict) and isinstance(client.get('index'), int) and 'connections' in client and isinstance(client['connections'], list) for client in item.get('clients', [])) for item in result))
@icontract.ensure(lambda result: all(all(isinstance(conn, dict) and 'host_name' in conn and 'direction' in conn and 'last_2s' in conn and 'last_10s' in conn and 'last_40s' in conn and 'cumulative' in conn and isinstance(conn.get('last_2s'), int) and isinstance(conn.get('last_10s'), int) and isinstance(conn.get('last_40s'), int) and isinstance(conn.get('cumulative'), int) for conn in client.get('connections', [])) for item in result for client in item.get('clients', [])))
@icontract.ensure(lambda result: all(all(k in item and isinstance(item[k], dict) and all(isinstance(item[k].get(f), int) for f in ('last_2s', 'last_10s', 'last_40s')) for k in ('total_send_rate', 'total_receive_rate', 'total_send_and_receive_rate', 'peak_rate', 'cumulative_rate')) for item in result))
```
```
Hallucination.


@icontract.ensure(lambda result, proc_data: result is not proc_data)
However, the result is modified on proc_data locally.
```
icontract_fail
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
