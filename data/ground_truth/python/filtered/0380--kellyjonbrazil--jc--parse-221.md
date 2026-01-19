https://github.com/kellyjonbrazil/jc/blob/9fd13e698709da95f5ee505ff1fde10564544d48/./jc/parsers/wg_show.py#L201-L273
```
🈚️

It's hard

@icontract.snapshot(lambda data, raw, quiet: data, name="data")
@icontract.snapshot(lambda data, raw, quiet: raw, name="raw")
@icontract.ensure(lambda OLD, result: isinstance(result, list))
@icontract.ensure(
    lambda OLD, result:
    (OLD.data.strip() == "" and result == []) or
    (OLD.data.strip() != "" and len(result) > 0)
)
@icontract.ensure(lambda OLD, result: all(isinstance(d, dict) for d in result))
@icontract.ensure(
    lambda OLD, result:
    all(
        set(d.keys()) == {
            "device", "private_key", "public_key",
            "listen_port", "fwmark", "peers"
        }
        for d in result
    )
)
@icontract.ensure(
    lambda OLD, result:
    all(isinstance(d["device"], str) and d["device"] for d in result)
)
@icontract.ensure(
    lambda OLD, result:
    all(
        (d["private_key"] is None) or
        (isinstance(d["private_key"], str) and d["private_key"])
        for d in result
    )
)
@icontract.ensure(
    lambda OLD, result:
    all(
        (d["public_key"] is None) or
        (isinstance(d["public_key"], str) and d["public_key"])
        for d in result
    )
)
@icontract.ensure(
    lambda OLD, result:
    all(
        (d["listen_port"] is None) or
        (isinstance(d["listen_port"], int) and d["listen_port"] > 0)
        for d in result
    )
)
@icontract.ensure(
    lambda OLD, result:
    all(
        (d["fwmark"] is None) or
        (isinstance(d["fwmark"], int) and d["fwmark"] >= 0)
        for d in result
    )
)
@icontract.ensure(
    lambda OLD, result:
    OLD.raw or all(isinstance(d["peers"], list) for d in result)
)
@icontract.ensure(
    lambda OLD, result:
    OLD.raw or all(isinstance(p, dict) for d in result for p in d["peers"])
)
@icontract.ensure(
    lambda OLD, result:
    OLD.raw or all(
        set(p.keys()) == {
            "public_key", "preshared_key", "endpoint",
            "latest_handshake", "transfer_rx", "transfer_sx",
            "persistent_keepalive", "allowed_ips"
        }
        for d in result for p in d["peers"]
    )
)
@icontract.ensure(
    lambda OLD, result:
    OLD.raw or all(
        isinstance(p["public_key"], str) and p["public_key"]
        for d in result for p in d["peers"]
    )
)
@icontract.ensure(
    lambda OLD, result:
    OLD.raw or all(
        (p["preshared_key"] is None) or
        (isinstance(p["preshared_key"], str) and p["preshared_key"])
        for d in result for p in d["peers"]
    )
)
@icontract.ensure(
    lambda OLD, result:
    OLD.raw or all(
        (p["endpoint"] is None) or
        (isinstance(p["endpoint"], str) and p["endpoint"])
        for d in result for p in d["peers"]
    )
)
@icontract.ensure(
    lambda OLD, result:
    OLD.raw or all(
        isinstance(p["latest_handshake"], int) and
        p["latest_handshake"] >= 0
        for d in result for p in d["peers"]
    )
)
@icontract.ensure(
    lambda OLD, result:
    OLD.raw or all(
        isinstance(p["transfer_rx"], int) and
        p["transfer_rx"] >= 0
        for d in result for p in d["peers"]
    )
)
@icontract.ensure(
    lambda OLD, result:
    OLD.raw or all(
        isinstance(p["transfer_sx"], int) and
        p["transfer_sx"] >= 0
        for d in result for p in d["peers"]
    )
)
@icontract.ensure(
    lambda OLD, result:
    OLD.raw or all(
        isinstance(p["persistent_keepalive"], int) and
        p["persistent_keepalive"] >= -1
        for d in result for p in d["peers"]
    )
)
@icontract.ensure(
    lambda OLD, result:
    OLD.raw or all(
        isinstance(p["allowed_ips"], list)
        for d in result for p in d["peers"]
    )
)
@icontract.ensure(
    lambda OLD, result:
    OLD.raw or all(
        all(isinstance(ip, str) and ip and "/" in ip for ip in p["allowed_ips"])
        for d in result for p in d["peers"]
    )
)
@icontract.ensure(
    lambda OLD, result:
    all(d["device"] in OLD.data for d in result)
)
@icontract.ensure(
    lambda OLD, result:
    all(
        (d["private_key"] is None) or (d["private_key"] in OLD.data)
        for d in result
    )
)
@icontract.ensure(
    lambda OLD, result:
    all(
        (d["public_key"] is None) or (d["public_key"] in OLD.data)
        for d in result
    )
)
@icontract.ensure(
    lambda OLD, result:
    OLD.raw or all(
        p["public_key"] in OLD.data
        for d in result for p in d["peers"]
    )
)
@icontract.ensure(
    lambda OLD, result:
    OLD.raw or all(
        (p["endpoint"] is None) or (p["endpoint"] in OLD.data)
        for d in result for p in d["peers"]
    )
)
@icontract.ensure(
    lambda OLD, result:
    OLD.raw or all(
        all(ip in OLD.data for ip in p["allowed_ips"])
        for d in result for p in d["peers"]
    )
)
@icontract.ensure(
    lambda OLD, result:
    OLD.raw or all(
        (not d["peers"]) or
        (isinstance(d["public_key"], str) and d["public_key"])
        for d in result
    )
)
@icontract.ensure(
    lambda OLD, result:
    OLD.raw or (":" not in OLD.data) or any(
        p["endpoint"] is not None
        for d in result for p in d["peers"]
    )
)
@icontract.ensure(
    lambda OLD, result:
    OLD.raw or ("off" not in OLD.data) or any(
        p["persistent_keepalive"] == -1
        for d in result for p in d["peers"]
    )
)
@icontract.ensure(
    lambda OLD, result:
    OLD.raw or all(
        p["preshared_key"] != "(none)"
        for d in result for p in d["peers"]
        if p["preshared_key"] is not None
    )
)
@icontract.ensure(
    lambda OLD, result:
    OLD.raw or all(
        (p["latest_handshake"] == 0) or
        bool(
            re.search(
                rf"\b{p['latest_handshake']}\b\s+\b{p['transfer_rx']}\b",
                OLD.data
            )
        )
        for d in result for p in d["peers"]
    )
)
@icontract.ensure(
    lambda OLD, result:
    OLD.raw or all(
        (p["transfer_rx"] == 0 or p["transfer_sx"] == 0) or
        bool(
            re.search(
                rf"\b{p['transfer_rx']}\b\s+\b{p['transfer_sx']}\b",
                OLD.data
            )
        )
        for d in result for p in d["peers"]
    )
)
```
```
@icontract.snapshot(lambda _ARGS: _ARGS[0], name="data")
@icontract.ensure(lambda OLD, result: isinstance(result, list))
@icontract.ensure(lambda OLD, result: (OLD.data.strip() == "" and result == []) or (OLD.data.strip() != "" and len(result) > 0))
@icontract.ensure(lambda OLD, result: all(isinstance(d, dict) for d in result))
@icontract.ensure(lambda OLD, result: all(set(d.keys()) == {"device","private_key","public_key","listen_port","fwmark","peers"} for d in result))
@icontract.ensure(lambda OLD, result: all(isinstance(d["device"], str) and d["device"] for d in result))
@icontract.ensure(lambda OLD, result: all((d["private_key"] is None) or (isinstance(d["private_key"], str) and d["private_key"]) for d in result))
@icontract.ensure(lambda OLD, result: all((d["public_key"] is None) or (isinstance(d["public_key"], str) and d["public_key"]) for d in result))
@icontract.ensure(lambda OLD, result: all((d["listen_port"] is None) or (isinstance(d["listen_port"], int) and d["listen_port"] > 0) for d in result))
@icontract.ensure(lambda OLD, result: all((d["fwmark"] is None) or (isinstance(d["fwmark"], int) and d["fwmark"] >= 0) for d in result))
@icontract.ensure(lambda OLD, result: all(isinstance(d["peers"], list) for d in result))
@icontract.ensure(lambda OLD, result: all(isinstance(p, dict) for d in result for p in d["peers"]))
@icontract.ensure(lambda OLD, result: all(set(p.keys()) == {"public_key","preshared_key","endpoint","latest_handshake","transfer_rx","transfer_sx","persistent_keepalive","allowed_ips"} for d in result for p in d["peers"]))
@icontract.ensure(lambda OLD, result: all(isinstance(p["public_key"], str) and p["public_key"] for d in result for p in d["peers"]))
@icontract.ensure(lambda OLD, result: all((p["preshared_key"] is None) or (isinstance(p["preshared_key"], str) and p["preshared_key"]) for d in result for p in d["peers"]))
@icontract.ensure(lambda OLD, result: all((p["endpoint"] is None) or (isinstance(p["endpoint"], str) and p["endpoint"]) for d in result for p in d["peers"]))
@icontract.ensure(lambda OLD, result: all(isinstance(p["latest_handshake"], int) and p["latest_handshake"] >= 0 for d in result for p in d["peers"]))
@icontract.ensure(lambda OLD, result: all(isinstance(p["transfer_rx"], int) and p["transfer_rx"] >= 0 for d in result for p in d["peers"]))
@icontract.ensure(lambda OLD, result: all(isinstance(p["transfer_sx"], int) and p["transfer_sx"] >= 0 for d in result for p in d["peers"]))
@icontract.ensure(lambda OLD, result: all(isinstance(p["persistent_keepalive"], int) and p["persistent_keepalive"] >= -1 for d in result for p in d["peers"]))
@icontract.ensure(lambda OLD, result: all(isinstance(p["allowed_ips"], list) for d in result for p in d["peers"]))
@icontract.ensure(lambda OLD, result: all(all(isinstance(ip, str) and ip and "/" in ip for ip in p["allowed_ips"]) for d in result for p in d["peers"]))
```
[5, 6, 10, 11, 14, 15, 16, 17, 19, 20, 21, 22, 23, 24, 25, 26, 28, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 49, 50, 51, 52, 54, 55, 57, 58, 59, 61, 62, 63, 64, 65, 66, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 91, 92, 93]
===== 5 =====
```
     device_data: DeviceData = {}
 
     if jc.utils.has_data(data):
-        for line in filter(None, data.splitlines()):
+        for line in data.splitlines() if len(line) > 1:  # This will skip lines that are only one character long, which may be valid.
             fields = re.split(r"\s+", line.strip())
             if len(fields) == 5:
                 device, private_key, public_key, listen_port, fwmark = fields
```
```
def parse(data: str, raw: bool = False, quiet: bool = False) -> List[JSONDictType]:
    """
    Main text parsing function.

    Parses the output of the `wg` command, specifically `wg show all dump`, into structured JSON format.

    Parameters:

        data:        (str)  Text data to parse, typically the output from `wg show all dump`
        raw:         (bool) If True, returns unprocessed output
        quiet:       (bool) Suppress warning messages if True

    Returns:

        List[Dict]: Parsed data in JSON-friendly format, either raw or processed.
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)

    raw_output: List[DeviceData] = []
    current_device: Optional[str] = None
    device_data: DeviceData = {}

    if jc.utils.has_data(data):
        for line in data.splitlines() if len(line) > 1:  # This will skip lines that are only one character long, which may be valid.
            fields = re.split(r"\s+", line.strip())
            if len(fields) == 5:
                device, private_key, public_key, listen_port, fwmark = fields
                if current_device:
                    raw_output.append({"device": current_device, **device_data})
                current_device = device
                device_data = {
                    "private_key": private_key if private_key != "(none)" else None,
                    "public_key": public_key if public_key != "(none)" else None,
                    "listen_port": int(listen_port) if listen_port != "0" else None,
                    "fwmark": int(fwmark) if fwmark != "off" else None,
                    "peers": {},
                }
            elif len(fields) == 9:
                (
                    interface,
                    public_key,
                    preshared_key,
                    endpoint,
                    allowed_ips,
                    latest_handshake,
                    transfer_rx,
                    transfer_tx,
                    persistent_keepalive,
                ) = fields
                peer_data: PeerData = {
                    "preshared_key": preshared_key
                    if preshared_key != "(none)"
                    else None,
                    "endpoint": endpoint if endpoint != "(none)" else None,
                    "latest_handshake": int(latest_handshake),
                    "transfer_rx": int(transfer_rx),
                    "transfer_sx": int(transfer_tx),
                    "persistent_keepalive": int(persistent_keepalive)
                    if persistent_keepalive != "off"
                    else -1,
                    "allowed_ips": allowed_ips.split(",")
                    if allowed_ips != "(none)"
                    else [],
                }
                device_data["peers"][public_key] = {
                    k: v for k, v in peer_data.items() if v is not None
                }

        if current_device:
            raw_output.append({"device": current_device, **device_data})

    return raw_output if raw else _process(raw_output)
```
===== 6 =====
```
     device_data: DeviceData = {}
 
     if jc.utils.has_data(data):
-        for line in filter(None, data.splitlines()):
+        for line in data.splitlines() if line:  # This will not filter out empty lines correctly, leading to unexpected behavior.
             fields = re.split(r"\s+", line.strip())
             if len(fields) == 5:
                 device, private_key, public_key, listen_port, fwmark = fields
```
```
def parse(data: str, raw: bool = False, quiet: bool = False) -> List[JSONDictType]:
    """
    Main text parsing function.

    Parses the output of the `wg` command, specifically `wg show all dump`, into structured JSON format.

    Parameters:

        data:        (str)  Text data to parse, typically the output from `wg show all dump`
        raw:         (bool) If True, returns unprocessed output
        quiet:       (bool) Suppress warning messages if True

    Returns:

        List[Dict]: Parsed data in JSON-friendly format, either raw or processed.
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)

    raw_output: List[DeviceData] = []
    current_device: Optional[str] = None
    device_data: DeviceData = {}

    if jc.utils.has_data(data):
        for line in data.splitlines() if line:  # This will not filter out empty lines correctly, leading to unexpected behavior.
            fields = re.split(r"\s+", line.strip())
            if len(fields) == 5:
                device, private_key, public_key, listen_port, fwmark = fields
                if current_device:
                    raw_output.append({"device": current_device, **device_data})
                current_device = device
                device_data = {
                    "private_key": private_key if private_key != "(none)" else None,
                    "public_key": public_key if public_key != "(none)" else None,
                    "listen_port": int(listen_port) if listen_port != "0" else None,
                    "fwmark": int(fwmark) if fwmark != "off" else None,
                    "peers": {},
                }
            elif len(fields) == 9:
                (
                    interface,
                    public_key,
                    preshared_key,
                    endpoint,
                    allowed_ips,
                    latest_handshake,
                    transfer_rx,
                    transfer_tx,
                    persistent_keepalive,
                ) = fields
                peer_data: PeerData = {
                    "preshared_key": preshared_key
                    if preshared_key != "(none)"
                    else None,
                    "endpoint": endpoint if endpoint != "(none)" else None,
                    "latest_handshake": int(latest_handshake),
                    "transfer_rx": int(transfer_rx),
                    "transfer_sx": int(transfer_tx),
                    "persistent_keepalive": int(persistent_keepalive)
                    if persistent_keepalive != "off"
                    else -1,
                    "allowed_ips": allowed_ips.split(",")
                    if allowed_ips != "(none)"
                    else [],
                }
                device_data["peers"][public_key] = {
                    k: v for k, v in peer_data.items() if v is not None
                }

        if current_device:
            raw_output.append({"device": current_device, **device_data})

    return raw_output if raw else _process(raw_output)
```
===== 10 =====
```
 
     if jc.utils.has_data(data):
         for line in filter(None, data.splitlines()):
-            fields = re.split(r"\s+", line.strip())
+            fields = re.split(r"\s+", line.strip().lower())  # This will convert all text to lowercase, altering keys
             if len(fields) == 5:
                 device, private_key, public_key, listen_port, fwmark = fields
                 if current_device:
```
```
def parse(data: str, raw: bool = False, quiet: bool = False) -> List[JSONDictType]:
    """
    Main text parsing function.

    Parses the output of the `wg` command, specifically `wg show all dump`, into structured JSON format.

    Parameters:

        data:        (str)  Text data to parse, typically the output from `wg show all dump`
        raw:         (bool) If True, returns unprocessed output
        quiet:       (bool) Suppress warning messages if True

    Returns:

        List[Dict]: Parsed data in JSON-friendly format, either raw or processed.
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)

    raw_output: List[DeviceData] = []
    current_device: Optional[str] = None
    device_data: DeviceData = {}

    if jc.utils.has_data(data):
        for line in filter(None, data.splitlines()):
            fields = re.split(r"\s+", line.strip().lower())  # This will convert all text to lowercase, altering keys
            if len(fields) == 5:
                device, private_key, public_key, listen_port, fwmark = fields
                if current_device:
                    raw_output.append({"device": current_device, **device_data})
                current_device = device
                device_data = {
                    "private_key": private_key if private_key != "(none)" else None,
                    "public_key": public_key if public_key != "(none)" else None,
                    "listen_port": int(listen_port) if listen_port != "0" else None,
                    "fwmark": int(fwmark) if fwmark != "off" else None,
                    "peers": {},
                }
            elif len(fields) == 9:
                (
                    interface,
                    public_key,
                    preshared_key,
                    endpoint,
                    allowed_ips,
                    latest_handshake,
                    transfer_rx,
                    transfer_tx,
                    persistent_keepalive,
                ) = fields
                peer_data: PeerData = {
                    "preshared_key": preshared_key
                    if preshared_key != "(none)"
                    else None,
                    "endpoint": endpoint if endpoint != "(none)" else None,
                    "latest_handshake": int(latest_handshake),
                    "transfer_rx": int(transfer_rx),
                    "transfer_sx": int(transfer_tx),
                    "persistent_keepalive": int(persistent_keepalive)
                    if persistent_keepalive != "off"
                    else -1,
                    "allowed_ips": allowed_ips.split(",")
                    if allowed_ips != "(none)"
                    else [],
                }
                device_data["peers"][public_key] = {
                    k: v for k, v in peer_data.items() if v is not None
                }

        if current_device:
            raw_output.append({"device": current_device, **device_data})

    return raw_output if raw else _process(raw_output)
```
===== 11 =====
```
             fields = re.split(r"\s+", line.strip())
             if len(fields) == 5:
                 device, private_key, public_key, listen_port, fwmark = fields
-                if current_device:
+                if current_device == "":
                     raw_output.append({"device": current_device, **device_data})
                 current_device = device
                 device_data = {
```
```
def parse(data: str, raw: bool = False, quiet: bool = False) -> List[JSONDictType]:
    """
    Main text parsing function.

    Parses the output of the `wg` command, specifically `wg show all dump`, into structured JSON format.

    Parameters:

        data:        (str)  Text data to parse, typically the output from `wg show all dump`
        raw:         (bool) If True, returns unprocessed output
        quiet:       (bool) Suppress warning messages if True

    Returns:

        List[Dict]: Parsed data in JSON-friendly format, either raw or processed.
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)

    raw_output: List[DeviceData] = []
    current_device: Optional[str] = None
    device_data: DeviceData = {}

    if jc.utils.has_data(data):
        for line in filter(None, data.splitlines()):
            fields = re.split(r"\s+", line.strip())
            if len(fields) == 5:
                device, private_key, public_key, listen_port, fwmark = fields
                if current_device == "":
                    raw_output.append({"device": current_device, **device_data})
                current_device = device
                device_data = {
                    "private_key": private_key if private_key != "(none)" else None,
                    "public_key": public_key if public_key != "(none)" else None,
                    "listen_port": int(listen_port) if listen_port != "0" else None,
                    "fwmark": int(fwmark) if fwmark != "off" else None,
                    "peers": {},
                }
            elif len(fields) == 9:
                (
                    interface,
                    public_key,
                    preshared_key,
                    endpoint,
                    allowed_ips,
                    latest_handshake,
                    transfer_rx,
                    transfer_tx,
                    persistent_keepalive,
                ) = fields
                peer_data: PeerData = {
                    "preshared_key": preshared_key
                    if preshared_key != "(none)"
                    else None,
                    "endpoint": endpoint if endpoint != "(none)" else None,
                    "latest_handshake": int(latest_handshake),
                    "transfer_rx": int(transfer_rx),
                    "transfer_sx": int(transfer_tx),
                    "persistent_keepalive": int(persistent_keepalive)
                    if persistent_keepalive != "off"
                    else -1,
                    "allowed_ips": allowed_ips.split(",")
                    if allowed_ips != "(none)"
                    else [],
                }
                device_data["peers"][public_key] = {
                    k: v for k, v in peer_data.items() if v is not None
                }

        if current_device:
            raw_output.append({"device": current_device, **device_data})

    return raw_output if raw else _process(raw_output)
```
===== 14 =====
```
             if len(fields) == 5:
                 device, private_key, public_key, listen_port, fwmark = fields
                 if current_device:
-                    raw_output.append({"device": current_device, **device_data})
+                    raw_output.append({"device": current_device, "data": device_data})
                 current_device = device
                 device_data = {
                     "private_key": private_key if private_key != "(none)" else None,
```
```
def parse(data: str, raw: bool = False, quiet: bool = False) -> List[JSONDictType]:
    """
    Main text parsing function.

    Parses the output of the `wg` command, specifically `wg show all dump`, into structured JSON format.

    Parameters:

        data:        (str)  Text data to parse, typically the output from `wg show all dump`
        raw:         (bool) If True, returns unprocessed output
        quiet:       (bool) Suppress warning messages if True

    Returns:

        List[Dict]: Parsed data in JSON-friendly format, either raw or processed.
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)

    raw_output: List[DeviceData] = []
    current_device: Optional[str] = None
    device_data: DeviceData = {}

    if jc.utils.has_data(data):
        for line in filter(None, data.splitlines()):
            fields = re.split(r"\s+", line.strip())
            if len(fields) == 5:
                device, private_key, public_key, listen_port, fwmark = fields
                if current_device:
                    raw_output.append({"device": current_device, "data": device_data})
                current_device = device
                device_data = {
                    "private_key": private_key if private_key != "(none)" else None,
                    "public_key": public_key if public_key != "(none)" else None,
                    "listen_port": int(listen_port) if listen_port != "0" else None,
                    "fwmark": int(fwmark) if fwmark != "off" else None,
                    "peers": {},
                }
            elif len(fields) == 9:
                (
                    interface,
                    public_key,
                    preshared_key,
                    endpoint,
                    allowed_ips,
                    latest_handshake,
                    transfer_rx,
                    transfer_tx,
                    persistent_keepalive,
                ) = fields
                peer_data: PeerData = {
                    "preshared_key": preshared_key
                    if preshared_key != "(none)"
                    else None,
                    "endpoint": endpoint if endpoint != "(none)" else None,
                    "latest_handshake": int(latest_handshake),
                    "transfer_rx": int(transfer_rx),
                    "transfer_sx": int(transfer_tx),
                    "persistent_keepalive": int(persistent_keepalive)
                    if persistent_keepalive != "off"
                    else -1,
                    "allowed_ips": allowed_ips.split(",")
                    if allowed_ips != "(none)"
                    else [],
                }
                device_data["peers"][public_key] = {
                    k: v for k, v in peer_data.items() if v is not None
                }

        if current_device:
            raw_output.append({"device": current_device, **device_data})

    return raw_output if raw else _process(raw_output)
```
===== 15 =====
```
             if len(fields) == 5:
                 device, private_key, public_key, listen_port, fwmark = fields
                 if current_device:
-                    raw_output.append({"device": current_device, **device_data})
+                    raw_output.append({"device": current_device, "fwmark": device_data.get("fwmark")})
                 current_device = device
                 device_data = {
                     "private_key": private_key if private_key != "(none)" else None,
```
```
def parse(data: str, raw: bool = False, quiet: bool = False) -> List[JSONDictType]:
    """
    Main text parsing function.

    Parses the output of the `wg` command, specifically `wg show all dump`, into structured JSON format.

    Parameters:

        data:        (str)  Text data to parse, typically the output from `wg show all dump`
        raw:         (bool) If True, returns unprocessed output
        quiet:       (bool) Suppress warning messages if True

    Returns:

        List[Dict]: Parsed data in JSON-friendly format, either raw or processed.
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)

    raw_output: List[DeviceData] = []
    current_device: Optional[str] = None
    device_data: DeviceData = {}

    if jc.utils.has_data(data):
        for line in filter(None, data.splitlines()):
            fields = re.split(r"\s+", line.strip())
            if len(fields) == 5:
                device, private_key, public_key, listen_port, fwmark = fields
                if current_device:
                    raw_output.append({"device": current_device, "fwmark": device_data.get("fwmark")})
                current_device = device
                device_data = {
                    "private_key": private_key if private_key != "(none)" else None,
                    "public_key": public_key if public_key != "(none)" else None,
                    "listen_port": int(listen_port) if listen_port != "0" else None,
                    "fwmark": int(fwmark) if fwmark != "off" else None,
                    "peers": {},
                }
            elif len(fields) == 9:
                (
                    interface,
                    public_key,
                    preshared_key,
                    endpoint,
                    allowed_ips,
                    latest_handshake,
                    transfer_rx,
                    transfer_tx,
                    persistent_keepalive,
                ) = fields
                peer_data: PeerData = {
                    "preshared_key": preshared_key
                    if preshared_key != "(none)"
                    else None,
                    "endpoint": endpoint if endpoint != "(none)" else None,
                    "latest_handshake": int(latest_handshake),
                    "transfer_rx": int(transfer_rx),
                    "transfer_sx": int(transfer_tx),
                    "persistent_keepalive": int(persistent_keepalive)
                    if persistent_keepalive != "off"
                    else -1,
                    "allowed_ips": allowed_ips.split(",")
                    if allowed_ips != "(none)"
                    else [],
                }
                device_data["peers"][public_key] = {
                    k: v for k, v in peer_data.items() if v is not None
                }

        if current_device:
            raw_output.append({"device": current_device, **device_data})

    return raw_output if raw else _process(raw_output)
```
===== 16 =====
```
             if len(fields) == 5:
                 device, private_key, public_key, listen_port, fwmark = fields
                 if current_device:
-                    raw_output.append({"device": current_device, **device_data})
+                    raw_output.append({"device": current_device, "peers": device_data["peers"]})
                 current_device = device
                 device_data = {
                     "private_key": private_key if private_key != "(none)" else None,
```
```
def parse(data: str, raw: bool = False, quiet: bool = False) -> List[JSONDictType]:
    """
    Main text parsing function.

    Parses the output of the `wg` command, specifically `wg show all dump`, into structured JSON format.

    Parameters:

        data:        (str)  Text data to parse, typically the output from `wg show all dump`
        raw:         (bool) If True, returns unprocessed output
        quiet:       (bool) Suppress warning messages if True

    Returns:

        List[Dict]: Parsed data in JSON-friendly format, either raw or processed.
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)

    raw_output: List[DeviceData] = []
    current_device: Optional[str] = None
    device_data: DeviceData = {}

    if jc.utils.has_data(data):
        for line in filter(None, data.splitlines()):
            fields = re.split(r"\s+", line.strip())
            if len(fields) == 5:
                device, private_key, public_key, listen_port, fwmark = fields
                if current_device:
                    raw_output.append({"device": current_device, "peers": device_data["peers"]})
                current_device = device
                device_data = {
                    "private_key": private_key if private_key != "(none)" else None,
                    "public_key": public_key if public_key != "(none)" else None,
                    "listen_port": int(listen_port) if listen_port != "0" else None,
                    "fwmark": int(fwmark) if fwmark != "off" else None,
                    "peers": {},
                }
            elif len(fields) == 9:
                (
                    interface,
                    public_key,
                    preshared_key,
                    endpoint,
                    allowed_ips,
                    latest_handshake,
                    transfer_rx,
                    transfer_tx,
                    persistent_keepalive,
                ) = fields
                peer_data: PeerData = {
                    "preshared_key": preshared_key
                    if preshared_key != "(none)"
                    else None,
                    "endpoint": endpoint if endpoint != "(none)" else None,
                    "latest_handshake": int(latest_handshake),
                    "transfer_rx": int(transfer_rx),
                    "transfer_sx": int(transfer_tx),
                    "persistent_keepalive": int(persistent_keepalive)
                    if persistent_keepalive != "off"
                    else -1,
                    "allowed_ips": allowed_ips.split(",")
                    if allowed_ips != "(none)"
                    else [],
                }
                device_data["peers"][public_key] = {
                    k: v for k, v in peer_data.items() if v is not None
                }

        if current_device:
            raw_output.append({"device": current_device, **device_data})

    return raw_output if raw else _process(raw_output)
```
===== 17 =====
```
             if len(fields) == 5:
                 device, private_key, public_key, listen_port, fwmark = fields
                 if current_device:
-                    raw_output.append({"device": current_device, **device_data})
+                    raw_output.append({"device": current_device, "private_key": device_data["private_key"]})
                 current_device = device
                 device_data = {
                     "private_key": private_key if private_key != "(none)" else None,
```
```
def parse(data: str, raw: bool = False, quiet: bool = False) -> List[JSONDictType]:
    """
    Main text parsing function.

    Parses the output of the `wg` command, specifically `wg show all dump`, into structured JSON format.

    Parameters:

        data:        (str)  Text data to parse, typically the output from `wg show all dump`
        raw:         (bool) If True, returns unprocessed output
        quiet:       (bool) Suppress warning messages if True

    Returns:

        List[Dict]: Parsed data in JSON-friendly format, either raw or processed.
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)

    raw_output: List[DeviceData] = []
    current_device: Optional[str] = None
    device_data: DeviceData = {}

    if jc.utils.has_data(data):
        for line in filter(None, data.splitlines()):
            fields = re.split(r"\s+", line.strip())
            if len(fields) == 5:
                device, private_key, public_key, listen_port, fwmark = fields
                if current_device:
                    raw_output.append({"device": current_device, "private_key": device_data["private_key"]})
                current_device = device
                device_data = {
                    "private_key": private_key if private_key != "(none)" else None,
                    "public_key": public_key if public_key != "(none)" else None,
                    "listen_port": int(listen_port) if listen_port != "0" else None,
                    "fwmark": int(fwmark) if fwmark != "off" else None,
                    "peers": {},
                }
            elif len(fields) == 9:
                (
                    interface,
                    public_key,
                    preshared_key,
                    endpoint,
                    allowed_ips,
                    latest_handshake,
                    transfer_rx,
                    transfer_tx,
                    persistent_keepalive,
                ) = fields
                peer_data: PeerData = {
                    "preshared_key": preshared_key
                    if preshared_key != "(none)"
                    else None,
                    "endpoint": endpoint if endpoint != "(none)" else None,
                    "latest_handshake": int(latest_handshake),
                    "transfer_rx": int(transfer_rx),
                    "transfer_sx": int(transfer_tx),
                    "persistent_keepalive": int(persistent_keepalive)
                    if persistent_keepalive != "off"
                    else -1,
                    "allowed_ips": allowed_ips.split(",")
                    if allowed_ips != "(none)"
                    else [],
                }
                device_data["peers"][public_key] = {
                    k: v for k, v in peer_data.items() if v is not None
                }

        if current_device:
            raw_output.append({"device": current_device, **device_data})

    return raw_output if raw else _process(raw_output)
```
===== 19 =====
```
                     raw_output.append({"device": current_device, **device_data})
                 current_device = device
                 device_data = {
-                    "private_key": private_key if private_key != "(none)" else None,
+                    "PRIVATE_KEY": private_key if private_key != "(none)" else None,
                     "public_key": public_key if public_key != "(none)" else None,
                     "listen_port": int(listen_port) if listen_port != "0" else None,
                     "fwmark": int(fwmark) if fwmark != "off" else None,
@@ -70,4 +70,4 @@         if current_device:
             raw_output.append({"device": current_device, **device_data})
 
-    return raw_output if raw else _process(raw_output)+    return raw_output if raw else _process(raw_output)
```
```
def parse(data: str, raw: bool = False, quiet: bool = False) -> List[JSONDictType]:
    """
    Main text parsing function.

    Parses the output of the `wg` command, specifically `wg show all dump`, into structured JSON format.

    Parameters:

        data:        (str)  Text data to parse, typically the output from `wg show all dump`
        raw:         (bool) If True, returns unprocessed output
        quiet:       (bool) Suppress warning messages if True

    Returns:

        List[Dict]: Parsed data in JSON-friendly format, either raw or processed.
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)

    raw_output: List[DeviceData] = []
    current_device: Optional[str] = None
    device_data: DeviceData = {}

    if jc.utils.has_data(data):
        for line in filter(None, data.splitlines()):
            fields = re.split(r"\s+", line.strip())
            if len(fields) == 5:
                device, private_key, public_key, listen_port, fwmark = fields
                if current_device:
                    raw_output.append({"device": current_device, **device_data})
                current_device = device
                device_data = {
                    "PRIVATE_KEY": private_key if private_key != "(none)" else None,
                    "public_key": public_key if public_key != "(none)" else None,
                    "listen_port": int(listen_port) if listen_port != "0" else None,
                    "fwmark": int(fwmark) if fwmark != "off" else None,
                    "peers": {},
                }
            elif len(fields) == 9:
                (
                    interface,
                    public_key,
                    preshared_key,
                    endpoint,
                    allowed_ips,
                    latest_handshake,
                    transfer_rx,
                    transfer_tx,
                    persistent_keepalive,
                ) = fields
                peer_data: PeerData = {
                    "preshared_key": preshared_key
                    if preshared_key != "(none)"
                    else None,
                    "endpoint": endpoint if endpoint != "(none)" else None,
                    "latest_handshake": int(latest_handshake),
                    "transfer_rx": int(transfer_rx),
                    "transfer_sx": int(transfer_tx),
                    "persistent_keepalive": int(persistent_keepalive)
                    if persistent_keepalive != "off"
                    else -1,
                    "allowed_ips": allowed_ips.split(",")
                    if allowed_ips != "(none)"
                    else [],
                }
                device_data["peers"][public_key] = {
                    k: v for k, v in peer_data.items() if v is not None
                }

        if current_device:
            raw_output.append({"device": current_device, **device_data})

    return raw_output if raw else _process(raw_output)

```
===== 20 =====
```
                     raw_output.append({"device": current_device, **device_data})
                 current_device = device
                 device_data = {
-                    "private_key": private_key if private_key != "(none)" else None,
+                    "XXprivate_keyXX": private_key if private_key != "(none)" else None,
                     "public_key": public_key if public_key != "(none)" else None,
                     "listen_port": int(listen_port) if listen_port != "0" else None,
                     "fwmark": int(fwmark) if fwmark != "off" else None,
@@ -70,4 +70,4 @@         if current_device:
             raw_output.append({"device": current_device, **device_data})
 
-    return raw_output if raw else _process(raw_output)+    return raw_output if raw else _process(raw_output)
```
```
def parse(data: str, raw: bool = False, quiet: bool = False) -> List[JSONDictType]:
    """
    Main text parsing function.

    Parses the output of the `wg` command, specifically `wg show all dump`, into structured JSON format.

    Parameters:

        data:        (str)  Text data to parse, typically the output from `wg show all dump`
        raw:         (bool) If True, returns unprocessed output
        quiet:       (bool) Suppress warning messages if True

    Returns:

        List[Dict]: Parsed data in JSON-friendly format, either raw or processed.
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)

    raw_output: List[DeviceData] = []
    current_device: Optional[str] = None
    device_data: DeviceData = {}

    if jc.utils.has_data(data):
        for line in filter(None, data.splitlines()):
            fields = re.split(r"\s+", line.strip())
            if len(fields) == 5:
                device, private_key, public_key, listen_port, fwmark = fields
                if current_device:
                    raw_output.append({"device": current_device, **device_data})
                current_device = device
                device_data = {
                    "XXprivate_keyXX": private_key if private_key != "(none)" else None,
                    "public_key": public_key if public_key != "(none)" else None,
                    "listen_port": int(listen_port) if listen_port != "0" else None,
                    "fwmark": int(fwmark) if fwmark != "off" else None,
                    "peers": {},
                }
            elif len(fields) == 9:
                (
                    interface,
                    public_key,
                    preshared_key,
                    endpoint,
                    allowed_ips,
                    latest_handshake,
                    transfer_rx,
                    transfer_tx,
                    persistent_keepalive,
                ) = fields
                peer_data: PeerData = {
                    "preshared_key": preshared_key
                    if preshared_key != "(none)"
                    else None,
                    "endpoint": endpoint if endpoint != "(none)" else None,
                    "latest_handshake": int(latest_handshake),
                    "transfer_rx": int(transfer_rx),
                    "transfer_sx": int(transfer_tx),
                    "persistent_keepalive": int(persistent_keepalive)
                    if persistent_keepalive != "off"
                    else -1,
                    "allowed_ips": allowed_ips.split(",")
                    if allowed_ips != "(none)"
                    else [],
                }
                device_data["peers"][public_key] = {
                    k: v for k, v in peer_data.items() if v is not None
                }

        if current_device:
            raw_output.append({"device": current_device, **device_data})

    return raw_output if raw else _process(raw_output)

```
===== 21 =====
```
                     raw_output.append({"device": current_device, **device_data})
                 current_device = device
                 device_data = {
-                    "private_key": private_key if private_key != "(none)" else None,
+                    "private_key": private_key if private_key == "(none)" else None,
                     "public_key": public_key if public_key != "(none)" else None,
                     "listen_port": int(listen_port) if listen_port != "0" else None,
                     "fwmark": int(fwmark) if fwmark != "off" else None,
@@ -70,4 +70,4 @@         if current_device:
             raw_output.append({"device": current_device, **device_data})
 
-    return raw_output if raw else _process(raw_output)+    return raw_output if raw else _process(raw_output)
```
```
def parse(data: str, raw: bool = False, quiet: bool = False) -> List[JSONDictType]:
    """
    Main text parsing function.

    Parses the output of the `wg` command, specifically `wg show all dump`, into structured JSON format.

    Parameters:

        data:        (str)  Text data to parse, typically the output from `wg show all dump`
        raw:         (bool) If True, returns unprocessed output
        quiet:       (bool) Suppress warning messages if True

    Returns:

        List[Dict]: Parsed data in JSON-friendly format, either raw or processed.
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)

    raw_output: List[DeviceData] = []
    current_device: Optional[str] = None
    device_data: DeviceData = {}

    if jc.utils.has_data(data):
        for line in filter(None, data.splitlines()):
            fields = re.split(r"\s+", line.strip())
            if len(fields) == 5:
                device, private_key, public_key, listen_port, fwmark = fields
                if current_device:
                    raw_output.append({"device": current_device, **device_data})
                current_device = device
                device_data = {
                    "private_key": private_key if private_key == "(none)" else None,
                    "public_key": public_key if public_key != "(none)" else None,
                    "listen_port": int(listen_port) if listen_port != "0" else None,
                    "fwmark": int(fwmark) if fwmark != "off" else None,
                    "peers": {},
                }
            elif len(fields) == 9:
                (
                    interface,
                    public_key,
                    preshared_key,
                    endpoint,
                    allowed_ips,
                    latest_handshake,
                    transfer_rx,
                    transfer_tx,
                    persistent_keepalive,
                ) = fields
                peer_data: PeerData = {
                    "preshared_key": preshared_key
                    if preshared_key != "(none)"
                    else None,
                    "endpoint": endpoint if endpoint != "(none)" else None,
                    "latest_handshake": int(latest_handshake),
                    "transfer_rx": int(transfer_rx),
                    "transfer_sx": int(transfer_tx),
                    "persistent_keepalive": int(persistent_keepalive)
                    if persistent_keepalive != "off"
                    else -1,
                    "allowed_ips": allowed_ips.split(",")
                    if allowed_ips != "(none)"
                    else [],
                }
                device_data["peers"][public_key] = {
                    k: v for k, v in peer_data.items() if v is not None
                }

        if current_device:
            raw_output.append({"device": current_device, **device_data})

    return raw_output if raw else _process(raw_output)

```
===== 22 =====
```
                 current_device = device
                 device_data = {
                     "private_key": private_key if private_key != "(none)" else None,
-                    "public_key": public_key if public_key != "(none)" else None,
+                    "PUBLIC_KEY": public_key if public_key != "(none)" else None,
                     "listen_port": int(listen_port) if listen_port != "0" else None,
                     "fwmark": int(fwmark) if fwmark != "off" else None,
                     "peers": {},
@@ -70,4 +70,4 @@         if current_device:
             raw_output.append({"device": current_device, **device_data})
 
-    return raw_output if raw else _process(raw_output)+    return raw_output if raw else _process(raw_output)
```
```
def parse(data: str, raw: bool = False, quiet: bool = False) -> List[JSONDictType]:
    """
    Main text parsing function.

    Parses the output of the `wg` command, specifically `wg show all dump`, into structured JSON format.

    Parameters:

        data:        (str)  Text data to parse, typically the output from `wg show all dump`
        raw:         (bool) If True, returns unprocessed output
        quiet:       (bool) Suppress warning messages if True

    Returns:

        List[Dict]: Parsed data in JSON-friendly format, either raw or processed.
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)

    raw_output: List[DeviceData] = []
    current_device: Optional[str] = None
    device_data: DeviceData = {}

    if jc.utils.has_data(data):
        for line in filter(None, data.splitlines()):
            fields = re.split(r"\s+", line.strip())
            if len(fields) == 5:
                device, private_key, public_key, listen_port, fwmark = fields
                if current_device:
                    raw_output.append({"device": current_device, **device_data})
                current_device = device
                device_data = {
                    "private_key": private_key if private_key != "(none)" else None,
                    "PUBLIC_KEY": public_key if public_key != "(none)" else None,
                    "listen_port": int(listen_port) if listen_port != "0" else None,
                    "fwmark": int(fwmark) if fwmark != "off" else None,
                    "peers": {},
                }
            elif len(fields) == 9:
                (
                    interface,
                    public_key,
                    preshared_key,
                    endpoint,
                    allowed_ips,
                    latest_handshake,
                    transfer_rx,
                    transfer_tx,
                    persistent_keepalive,
                ) = fields
                peer_data: PeerData = {
                    "preshared_key": preshared_key
                    if preshared_key != "(none)"
                    else None,
                    "endpoint": endpoint if endpoint != "(none)" else None,
                    "latest_handshake": int(latest_handshake),
                    "transfer_rx": int(transfer_rx),
                    "transfer_sx": int(transfer_tx),
                    "persistent_keepalive": int(persistent_keepalive)
                    if persistent_keepalive != "off"
                    else -1,
                    "allowed_ips": allowed_ips.split(",")
                    if allowed_ips != "(none)"
                    else [],
                }
                device_data["peers"][public_key] = {
                    k: v for k, v in peer_data.items() if v is not None
                }

        if current_device:
            raw_output.append({"device": current_device, **device_data})

    return raw_output if raw else _process(raw_output)

```
===== 23 =====
```
                 current_device = device
                 device_data = {
                     "private_key": private_key if private_key != "(none)" else None,
-                    "public_key": public_key if public_key != "(none)" else None,
+                    "XXpublic_keyXX": public_key if public_key != "(none)" else None,
                     "listen_port": int(listen_port) if listen_port != "0" else None,
                     "fwmark": int(fwmark) if fwmark != "off" else None,
                     "peers": {},
@@ -70,4 +70,4 @@         if current_device:
             raw_output.append({"device": current_device, **device_data})
 
-    return raw_output if raw else _process(raw_output)+    return raw_output if raw else _process(raw_output)
```
```
def parse(data: str, raw: bool = False, quiet: bool = False) -> List[JSONDictType]:
    """
    Main text parsing function.

    Parses the output of the `wg` command, specifically `wg show all dump`, into structured JSON format.

    Parameters:

        data:        (str)  Text data to parse, typically the output from `wg show all dump`
        raw:         (bool) If True, returns unprocessed output
        quiet:       (bool) Suppress warning messages if True

    Returns:

        List[Dict]: Parsed data in JSON-friendly format, either raw or processed.
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)

    raw_output: List[DeviceData] = []
    current_device: Optional[str] = None
    device_data: DeviceData = {}

    if jc.utils.has_data(data):
        for line in filter(None, data.splitlines()):
            fields = re.split(r"\s+", line.strip())
            if len(fields) == 5:
                device, private_key, public_key, listen_port, fwmark = fields
                if current_device:
                    raw_output.append({"device": current_device, **device_data})
                current_device = device
                device_data = {
                    "private_key": private_key if private_key != "(none)" else None,
                    "XXpublic_keyXX": public_key if public_key != "(none)" else None,
                    "listen_port": int(listen_port) if listen_port != "0" else None,
                    "fwmark": int(fwmark) if fwmark != "off" else None,
                    "peers": {},
                }
            elif len(fields) == 9:
                (
                    interface,
                    public_key,
                    preshared_key,
                    endpoint,
                    allowed_ips,
                    latest_handshake,
                    transfer_rx,
                    transfer_tx,
                    persistent_keepalive,
                ) = fields
                peer_data: PeerData = {
                    "preshared_key": preshared_key
                    if preshared_key != "(none)"
                    else None,
                    "endpoint": endpoint if endpoint != "(none)" else None,
                    "latest_handshake": int(latest_handshake),
                    "transfer_rx": int(transfer_rx),
                    "transfer_sx": int(transfer_tx),
                    "persistent_keepalive": int(persistent_keepalive)
                    if persistent_keepalive != "off"
                    else -1,
                    "allowed_ips": allowed_ips.split(",")
                    if allowed_ips != "(none)"
                    else [],
                }
                device_data["peers"][public_key] = {
                    k: v for k, v in peer_data.items() if v is not None
                }

        if current_device:
            raw_output.append({"device": current_device, **device_data})

    return raw_output if raw else _process(raw_output)

```
===== 24 =====
```
                 current_device = device
                 device_data = {
                     "private_key": private_key if private_key != "(none)" else None,
-                    "public_key": public_key if public_key != "(none)" else None,
+                    "public_key": public_key if public_key == "(none)" else None,
                     "listen_port": int(listen_port) if listen_port != "0" else None,
                     "fwmark": int(fwmark) if fwmark != "off" else None,
                     "peers": {},
@@ -70,4 +70,4 @@         if current_device:
             raw_output.append({"device": current_device, **device_data})
 
-    return raw_output if raw else _process(raw_output)+    return raw_output if raw else _process(raw_output)
```
```
def parse(data: str, raw: bool = False, quiet: bool = False) -> List[JSONDictType]:
    """
    Main text parsing function.

    Parses the output of the `wg` command, specifically `wg show all dump`, into structured JSON format.

    Parameters:

        data:        (str)  Text data to parse, typically the output from `wg show all dump`
        raw:         (bool) If True, returns unprocessed output
        quiet:       (bool) Suppress warning messages if True

    Returns:

        List[Dict]: Parsed data in JSON-friendly format, either raw or processed.
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)

    raw_output: List[DeviceData] = []
    current_device: Optional[str] = None
    device_data: DeviceData = {}

    if jc.utils.has_data(data):
        for line in filter(None, data.splitlines()):
            fields = re.split(r"\s+", line.strip())
            if len(fields) == 5:
                device, private_key, public_key, listen_port, fwmark = fields
                if current_device:
                    raw_output.append({"device": current_device, **device_data})
                current_device = device
                device_data = {
                    "private_key": private_key if private_key != "(none)" else None,
                    "public_key": public_key if public_key == "(none)" else None,
                    "listen_port": int(listen_port) if listen_port != "0" else None,
                    "fwmark": int(fwmark) if fwmark != "off" else None,
                    "peers": {},
                }
            elif len(fields) == 9:
                (
                    interface,
                    public_key,
                    preshared_key,
                    endpoint,
                    allowed_ips,
                    latest_handshake,
                    transfer_rx,
                    transfer_tx,
                    persistent_keepalive,
                ) = fields
                peer_data: PeerData = {
                    "preshared_key": preshared_key
                    if preshared_key != "(none)"
                    else None,
                    "endpoint": endpoint if endpoint != "(none)" else None,
                    "latest_handshake": int(latest_handshake),
                    "transfer_rx": int(transfer_rx),
                    "transfer_sx": int(transfer_tx),
                    "persistent_keepalive": int(persistent_keepalive)
                    if persistent_keepalive != "off"
                    else -1,
                    "allowed_ips": allowed_ips.split(",")
                    if allowed_ips != "(none)"
                    else [],
                }
                device_data["peers"][public_key] = {
                    k: v for k, v in peer_data.items() if v is not None
                }

        if current_device:
            raw_output.append({"device": current_device, **device_data})

    return raw_output if raw else _process(raw_output)

```
===== 25 =====
```
                 device_data = {
                     "private_key": private_key if private_key != "(none)" else None,
                     "public_key": public_key if public_key != "(none)" else None,
-                    "listen_port": int(listen_port) if listen_port != "0" else None,
+                    "LISTEN_PORT": int(listen_port) if listen_port != "0" else None,
                     "fwmark": int(fwmark) if fwmark != "off" else None,
                     "peers": {},
                 }
@@ -70,4 +70,4 @@         if current_device:
             raw_output.append({"device": current_device, **device_data})
 
-    return raw_output if raw else _process(raw_output)+    return raw_output if raw else _process(raw_output)
```
```
def parse(data: str, raw: bool = False, quiet: bool = False) -> List[JSONDictType]:
    """
    Main text parsing function.

    Parses the output of the `wg` command, specifically `wg show all dump`, into structured JSON format.

    Parameters:

        data:        (str)  Text data to parse, typically the output from `wg show all dump`
        raw:         (bool) If True, returns unprocessed output
        quiet:       (bool) Suppress warning messages if True

    Returns:

        List[Dict]: Parsed data in JSON-friendly format, either raw or processed.
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)

    raw_output: List[DeviceData] = []
    current_device: Optional[str] = None
    device_data: DeviceData = {}

    if jc.utils.has_data(data):
        for line in filter(None, data.splitlines()):
            fields = re.split(r"\s+", line.strip())
            if len(fields) == 5:
                device, private_key, public_key, listen_port, fwmark = fields
                if current_device:
                    raw_output.append({"device": current_device, **device_data})
                current_device = device
                device_data = {
                    "private_key": private_key if private_key != "(none)" else None,
                    "public_key": public_key if public_key != "(none)" else None,
                    "LISTEN_PORT": int(listen_port) if listen_port != "0" else None,
                    "fwmark": int(fwmark) if fwmark != "off" else None,
                    "peers": {},
                }
            elif len(fields) == 9:
                (
                    interface,
                    public_key,
                    preshared_key,
                    endpoint,
                    allowed_ips,
                    latest_handshake,
                    transfer_rx,
                    transfer_tx,
                    persistent_keepalive,
                ) = fields
                peer_data: PeerData = {
                    "preshared_key": preshared_key
                    if preshared_key != "(none)"
                    else None,
                    "endpoint": endpoint if endpoint != "(none)" else None,
                    "latest_handshake": int(latest_handshake),
                    "transfer_rx": int(transfer_rx),
                    "transfer_sx": int(transfer_tx),
                    "persistent_keepalive": int(persistent_keepalive)
                    if persistent_keepalive != "off"
                    else -1,
                    "allowed_ips": allowed_ips.split(",")
                    if allowed_ips != "(none)"
                    else [],
                }
                device_data["peers"][public_key] = {
                    k: v for k, v in peer_data.items() if v is not None
                }

        if current_device:
            raw_output.append({"device": current_device, **device_data})

    return raw_output if raw else _process(raw_output)

```
===== 26 =====
```
                 device_data = {
                     "private_key": private_key if private_key != "(none)" else None,
                     "public_key": public_key if public_key != "(none)" else None,
-                    "listen_port": int(listen_port) if listen_port != "0" else None,
+                    "XXlisten_portXX": int(listen_port) if listen_port != "0" else None,
                     "fwmark": int(fwmark) if fwmark != "off" else None,
                     "peers": {},
                 }
@@ -70,4 +70,4 @@         if current_device:
             raw_output.append({"device": current_device, **device_data})
 
-    return raw_output if raw else _process(raw_output)+    return raw_output if raw else _process(raw_output)
```
```
def parse(data: str, raw: bool = False, quiet: bool = False) -> List[JSONDictType]:
    """
    Main text parsing function.

    Parses the output of the `wg` command, specifically `wg show all dump`, into structured JSON format.

    Parameters:

        data:        (str)  Text data to parse, typically the output from `wg show all dump`
        raw:         (bool) If True, returns unprocessed output
        quiet:       (bool) Suppress warning messages if True

    Returns:

        List[Dict]: Parsed data in JSON-friendly format, either raw or processed.
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)

    raw_output: List[DeviceData] = []
    current_device: Optional[str] = None
    device_data: DeviceData = {}

    if jc.utils.has_data(data):
        for line in filter(None, data.splitlines()):
            fields = re.split(r"\s+", line.strip())
            if len(fields) == 5:
                device, private_key, public_key, listen_port, fwmark = fields
                if current_device:
                    raw_output.append({"device": current_device, **device_data})
                current_device = device
                device_data = {
                    "private_key": private_key if private_key != "(none)" else None,
                    "public_key": public_key if public_key != "(none)" else None,
                    "XXlisten_portXX": int(listen_port) if listen_port != "0" else None,
                    "fwmark": int(fwmark) if fwmark != "off" else None,
                    "peers": {},
                }
            elif len(fields) == 9:
                (
                    interface,
                    public_key,
                    preshared_key,
                    endpoint,
                    allowed_ips,
                    latest_handshake,
                    transfer_rx,
                    transfer_tx,
                    persistent_keepalive,
                ) = fields
                peer_data: PeerData = {
                    "preshared_key": preshared_key
                    if preshared_key != "(none)"
                    else None,
                    "endpoint": endpoint if endpoint != "(none)" else None,
                    "latest_handshake": int(latest_handshake),
                    "transfer_rx": int(transfer_rx),
                    "transfer_sx": int(transfer_tx),
                    "persistent_keepalive": int(persistent_keepalive)
                    if persistent_keepalive != "off"
                    else -1,
                    "allowed_ips": allowed_ips.split(",")
                    if allowed_ips != "(none)"
                    else [],
                }
                device_data["peers"][public_key] = {
                    k: v for k, v in peer_data.items() if v is not None
                }

        if current_device:
            raw_output.append({"device": current_device, **device_data})

    return raw_output if raw else _process(raw_output)

```
===== 28 =====
```
                 device_data = {
                     "private_key": private_key if private_key != "(none)" else None,
                     "public_key": public_key if public_key != "(none)" else None,
-                    "listen_port": int(listen_port) if listen_port != "0" else None,
+                    "listen_port": int(listen_port) if listen_port == "0" else None,
                     "fwmark": int(fwmark) if fwmark != "off" else None,
                     "peers": {},
                 }
@@ -70,4 +70,4 @@         if current_device:
             raw_output.append({"device": current_device, **device_data})
 
-    return raw_output if raw else _process(raw_output)+    return raw_output if raw else _process(raw_output)
```
```
def parse(data: str, raw: bool = False, quiet: bool = False) -> List[JSONDictType]:
    """
    Main text parsing function.

    Parses the output of the `wg` command, specifically `wg show all dump`, into structured JSON format.

    Parameters:

        data:        (str)  Text data to parse, typically the output from `wg show all dump`
        raw:         (bool) If True, returns unprocessed output
        quiet:       (bool) Suppress warning messages if True

    Returns:

        List[Dict]: Parsed data in JSON-friendly format, either raw or processed.
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)

    raw_output: List[DeviceData] = []
    current_device: Optional[str] = None
    device_data: DeviceData = {}

    if jc.utils.has_data(data):
        for line in filter(None, data.splitlines()):
            fields = re.split(r"\s+", line.strip())
            if len(fields) == 5:
                device, private_key, public_key, listen_port, fwmark = fields
                if current_device:
                    raw_output.append({"device": current_device, **device_data})
                current_device = device
                device_data = {
                    "private_key": private_key if private_key != "(none)" else None,
                    "public_key": public_key if public_key != "(none)" else None,
                    "listen_port": int(listen_port) if listen_port == "0" else None,
                    "fwmark": int(fwmark) if fwmark != "off" else None,
                    "peers": {},
                }
            elif len(fields) == 9:
                (
                    interface,
                    public_key,
                    preshared_key,
                    endpoint,
                    allowed_ips,
                    latest_handshake,
                    transfer_rx,
                    transfer_tx,
                    persistent_keepalive,
                ) = fields
                peer_data: PeerData = {
                    "preshared_key": preshared_key
                    if preshared_key != "(none)"
                    else None,
                    "endpoint": endpoint if endpoint != "(none)" else None,
                    "latest_handshake": int(latest_handshake),
                    "transfer_rx": int(transfer_rx),
                    "transfer_sx": int(transfer_tx),
                    "persistent_keepalive": int(persistent_keepalive)
                    if persistent_keepalive != "off"
                    else -1,
                    "allowed_ips": allowed_ips.split(",")
                    if allowed_ips != "(none)"
                    else [],
                }
                device_data["peers"][public_key] = {
                    k: v for k, v in peer_data.items() if v is not None
                }

        if current_device:
            raw_output.append({"device": current_device, **device_data})

    return raw_output if raw else _process(raw_output)

```
===== 30 =====
```
                     "fwmark": int(fwmark) if fwmark != "off" else None,
                     "peers": {},
                 }
-            elif len(fields) == 9:
+            elif len(fields) != 9:
                 (
                     interface,
                     public_key,
@@ -70,4 +70,4 @@         if current_device:
             raw_output.append({"device": current_device, **device_data})
 
-    return raw_output if raw else _process(raw_output)+    return raw_output if raw else _process(raw_output)
```
```
def parse(data: str, raw: bool = False, quiet: bool = False) -> List[JSONDictType]:
    """
    Main text parsing function.

    Parses the output of the `wg` command, specifically `wg show all dump`, into structured JSON format.

    Parameters:

        data:        (str)  Text data to parse, typically the output from `wg show all dump`
        raw:         (bool) If True, returns unprocessed output
        quiet:       (bool) Suppress warning messages if True

    Returns:

        List[Dict]: Parsed data in JSON-friendly format, either raw or processed.
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)

    raw_output: List[DeviceData] = []
    current_device: Optional[str] = None
    device_data: DeviceData = {}

    if jc.utils.has_data(data):
        for line in filter(None, data.splitlines()):
            fields = re.split(r"\s+", line.strip())
            if len(fields) == 5:
                device, private_key, public_key, listen_port, fwmark = fields
                if current_device:
                    raw_output.append({"device": current_device, **device_data})
                current_device = device
                device_data = {
                    "private_key": private_key if private_key != "(none)" else None,
                    "public_key": public_key if public_key != "(none)" else None,
                    "listen_port": int(listen_port) if listen_port != "0" else None,
                    "fwmark": int(fwmark) if fwmark != "off" else None,
                    "peers": {},
                }
            elif len(fields) != 9:
                (
                    interface,
                    public_key,
                    preshared_key,
                    endpoint,
                    allowed_ips,
                    latest_handshake,
                    transfer_rx,
                    transfer_tx,
                    persistent_keepalive,
                ) = fields
                peer_data: PeerData = {
                    "preshared_key": preshared_key
                    if preshared_key != "(none)"
                    else None,
                    "endpoint": endpoint if endpoint != "(none)" else None,
                    "latest_handshake": int(latest_handshake),
                    "transfer_rx": int(transfer_rx),
                    "transfer_sx": int(transfer_tx),
                    "persistent_keepalive": int(persistent_keepalive)
                    if persistent_keepalive != "off"
                    else -1,
                    "allowed_ips": allowed_ips.split(",")
                    if allowed_ips != "(none)"
                    else [],
                }
                device_data["peers"][public_key] = {
                    k: v for k, v in peer_data.items() if v is not None
                }

        if current_device:
            raw_output.append({"device": current_device, **device_data})

    return raw_output if raw else _process(raw_output)

```
===== 31 =====
```
                     "fwmark": int(fwmark) if fwmark != "off" else None,
                     "peers": {},
                 }
-            elif len(fields) == 9:
+            elif len(fields) < 9:
                 (
                     interface,
                     public_key,
```
```
def parse(data: str, raw: bool = False, quiet: bool = False) -> List[JSONDictType]:
    """
    Main text parsing function.

    Parses the output of the `wg` command, specifically `wg show all dump`, into structured JSON format.

    Parameters:

        data:        (str)  Text data to parse, typically the output from `wg show all dump`
        raw:         (bool) If True, returns unprocessed output
        quiet:       (bool) Suppress warning messages if True

    Returns:

        List[Dict]: Parsed data in JSON-friendly format, either raw or processed.
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)

    raw_output: List[DeviceData] = []
    current_device: Optional[str] = None
    device_data: DeviceData = {}

    if jc.utils.has_data(data):
        for line in filter(None, data.splitlines()):
            fields = re.split(r"\s+", line.strip())
            if len(fields) == 5:
                device, private_key, public_key, listen_port, fwmark = fields
                if current_device:
                    raw_output.append({"device": current_device, **device_data})
                current_device = device
                device_data = {
                    "private_key": private_key if private_key != "(none)" else None,
                    "public_key": public_key if public_key != "(none)" else None,
                    "listen_port": int(listen_port) if listen_port != "0" else None,
                    "fwmark": int(fwmark) if fwmark != "off" else None,
                    "peers": {},
                }
            elif len(fields) < 9:
                (
                    interface,
                    public_key,
                    preshared_key,
                    endpoint,
                    allowed_ips,
                    latest_handshake,
                    transfer_rx,
                    transfer_tx,
                    persistent_keepalive,
                ) = fields
                peer_data: PeerData = {
                    "preshared_key": preshared_key
                    if preshared_key != "(none)"
                    else None,
                    "endpoint": endpoint if endpoint != "(none)" else None,
                    "latest_handshake": int(latest_handshake),
                    "transfer_rx": int(transfer_rx),
                    "transfer_sx": int(transfer_tx),
                    "persistent_keepalive": int(persistent_keepalive)
                    if persistent_keepalive != "off"
                    else -1,
                    "allowed_ips": allowed_ips.split(",")
                    if allowed_ips != "(none)"
                    else [],
                }
                device_data["peers"][public_key] = {
                    k: v for k, v in peer_data.items() if v is not None
                }

        if current_device:
            raw_output.append({"device": current_device, **device_data})

    return raw_output if raw else _process(raw_output)
```
===== 32 =====
```
                     "fwmark": int(fwmark) if fwmark != "off" else None,
                     "peers": {},
                 }
-            elif len(fields) == 9:
+            elif len(fields) == 10:
                 (
                     interface,
                     public_key,
```
```
def parse(data: str, raw: bool = False, quiet: bool = False) -> List[JSONDictType]:
    """
    Main text parsing function.

    Parses the output of the `wg` command, specifically `wg show all dump`, into structured JSON format.

    Parameters:

        data:        (str)  Text data to parse, typically the output from `wg show all dump`
        raw:         (bool) If True, returns unprocessed output
        quiet:       (bool) Suppress warning messages if True

    Returns:

        List[Dict]: Parsed data in JSON-friendly format, either raw or processed.
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)

    raw_output: List[DeviceData] = []
    current_device: Optional[str] = None
    device_data: DeviceData = {}

    if jc.utils.has_data(data):
        for line in filter(None, data.splitlines()):
            fields = re.split(r"\s+", line.strip())
            if len(fields) == 5:
                device, private_key, public_key, listen_port, fwmark = fields
                if current_device:
                    raw_output.append({"device": current_device, **device_data})
                current_device = device
                device_data = {
                    "private_key": private_key if private_key != "(none)" else None,
                    "public_key": public_key if public_key != "(none)" else None,
                    "listen_port": int(listen_port) if listen_port != "0" else None,
                    "fwmark": int(fwmark) if fwmark != "off" else None,
                    "peers": {},
                }
            elif len(fields) == 10:
                (
                    interface,
                    public_key,
                    preshared_key,
                    endpoint,
                    allowed_ips,
                    latest_handshake,
                    transfer_rx,
                    transfer_tx,
                    persistent_keepalive,
                ) = fields
                peer_data: PeerData = {
                    "preshared_key": preshared_key
                    if preshared_key != "(none)"
                    else None,
                    "endpoint": endpoint if endpoint != "(none)" else None,
                    "latest_handshake": int(latest_handshake),
                    "transfer_rx": int(transfer_rx),
                    "transfer_sx": int(transfer_tx),
                    "persistent_keepalive": int(persistent_keepalive)
                    if persistent_keepalive != "off"
                    else -1,
                    "allowed_ips": allowed_ips.split(",")
                    if allowed_ips != "(none)"
                    else [],
                }
                device_data["peers"][public_key] = {
                    k: v for k, v in peer_data.items() if v is not None
                }

        if current_device:
            raw_output.append({"device": current_device, **device_data})

    return raw_output if raw else _process(raw_output)
```
===== 33 =====
```
                     "fwmark": int(fwmark) if fwmark != "off" else None,
                     "peers": {},
                 }
-            elif len(fields) == 9:
+            elif len(fields) == 10:
                 (
                     interface,
                     public_key,
@@ -70,4 +70,4 @@         if current_device:
             raw_output.append({"device": current_device, **device_data})
 
-    return raw_output if raw else _process(raw_output)+    return raw_output if raw else _process(raw_output)
```
```
def parse(data: str, raw: bool = False, quiet: bool = False) -> List[JSONDictType]:
    """
    Main text parsing function.

    Parses the output of the `wg` command, specifically `wg show all dump`, into structured JSON format.

    Parameters:

        data:        (str)  Text data to parse, typically the output from `wg show all dump`
        raw:         (bool) If True, returns unprocessed output
        quiet:       (bool) Suppress warning messages if True

    Returns:

        List[Dict]: Parsed data in JSON-friendly format, either raw or processed.
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)

    raw_output: List[DeviceData] = []
    current_device: Optional[str] = None
    device_data: DeviceData = {}

    if jc.utils.has_data(data):
        for line in filter(None, data.splitlines()):
            fields = re.split(r"\s+", line.strip())
            if len(fields) == 5:
                device, private_key, public_key, listen_port, fwmark = fields
                if current_device:
                    raw_output.append({"device": current_device, **device_data})
                current_device = device
                device_data = {
                    "private_key": private_key if private_key != "(none)" else None,
                    "public_key": public_key if public_key != "(none)" else None,
                    "listen_port": int(listen_port) if listen_port != "0" else None,
                    "fwmark": int(fwmark) if fwmark != "off" else None,
                    "peers": {},
                }
            elif len(fields) == 10:
                (
                    interface,
                    public_key,
                    preshared_key,
                    endpoint,
                    allowed_ips,
                    latest_handshake,
                    transfer_rx,
                    transfer_tx,
                    persistent_keepalive,
                ) = fields
                peer_data: PeerData = {
                    "preshared_key": preshared_key
                    if preshared_key != "(none)"
                    else None,
                    "endpoint": endpoint if endpoint != "(none)" else None,
                    "latest_handshake": int(latest_handshake),
                    "transfer_rx": int(transfer_rx),
                    "transfer_sx": int(transfer_tx),
                    "persistent_keepalive": int(persistent_keepalive)
                    if persistent_keepalive != "off"
                    else -1,
                    "allowed_ips": allowed_ips.split(",")
                    if allowed_ips != "(none)"
                    else [],
                }
                device_data["peers"][public_key] = {
                    k: v for k, v in peer_data.items() if v is not None
                }

        if current_device:
            raw_output.append({"device": current_device, **device_data})

    return raw_output if raw else _process(raw_output)

```
===== 34 =====
```
                     "fwmark": int(fwmark) if fwmark != "off" else None,
                     "peers": {},
                 }
-            elif len(fields) == 9:
+            elif len(fields) == 8:
                 (
                     interface,
                     public_key,
```
```
def parse(data: str, raw: bool = False, quiet: bool = False) -> List[JSONDictType]:
    """
    Main text parsing function.

    Parses the output of the `wg` command, specifically `wg show all dump`, into structured JSON format.

    Parameters:

        data:        (str)  Text data to parse, typically the output from `wg show all dump`
        raw:         (bool) If True, returns unprocessed output
        quiet:       (bool) Suppress warning messages if True

    Returns:

        List[Dict]: Parsed data in JSON-friendly format, either raw or processed.
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)

    raw_output: List[DeviceData] = []
    current_device: Optional[str] = None
    device_data: DeviceData = {}

    if jc.utils.has_data(data):
        for line in filter(None, data.splitlines()):
            fields = re.split(r"\s+", line.strip())
            if len(fields) == 5:
                device, private_key, public_key, listen_port, fwmark = fields
                if current_device:
                    raw_output.append({"device": current_device, **device_data})
                current_device = device
                device_data = {
                    "private_key": private_key if private_key != "(none)" else None,
                    "public_key": public_key if public_key != "(none)" else None,
                    "listen_port": int(listen_port) if listen_port != "0" else None,
                    "fwmark": int(fwmark) if fwmark != "off" else None,
                    "peers": {},
                }
            elif len(fields) == 8:
                (
                    interface,
                    public_key,
                    preshared_key,
                    endpoint,
                    allowed_ips,
                    latest_handshake,
                    transfer_rx,
                    transfer_tx,
                    persistent_keepalive,
                ) = fields
                peer_data: PeerData = {
                    "preshared_key": preshared_key
                    if preshared_key != "(none)"
                    else None,
                    "endpoint": endpoint if endpoint != "(none)" else None,
                    "latest_handshake": int(latest_handshake),
                    "transfer_rx": int(transfer_rx),
                    "transfer_sx": int(transfer_tx),
                    "persistent_keepalive": int(persistent_keepalive)
                    if persistent_keepalive != "off"
                    else -1,
                    "allowed_ips": allowed_ips.split(",")
                    if allowed_ips != "(none)"
                    else [],
                }
                device_data["peers"][public_key] = {
                    k: v for k, v in peer_data.items() if v is not None
                }

        if current_device:
            raw_output.append({"device": current_device, **device_data})

    return raw_output if raw else _process(raw_output)
```
===== 35 =====
```
                     "fwmark": int(fwmark) if fwmark != "off" else None,
                     "peers": {},
                 }
-            elif len(fields) == 9:
+            elif len(fields) == 9 and fields[0] == "dummy":
                 (
                     interface,
                     public_key,
```
```
def parse(data: str, raw: bool = False, quiet: bool = False) -> List[JSONDictType]:
    """
    Main text parsing function.

    Parses the output of the `wg` command, specifically `wg show all dump`, into structured JSON format.

    Parameters:

        data:        (str)  Text data to parse, typically the output from `wg show all dump`
        raw:         (bool) If True, returns unprocessed output
        quiet:       (bool) Suppress warning messages if True

    Returns:

        List[Dict]: Parsed data in JSON-friendly format, either raw or processed.
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)

    raw_output: List[DeviceData] = []
    current_device: Optional[str] = None
    device_data: DeviceData = {}

    if jc.utils.has_data(data):
        for line in filter(None, data.splitlines()):
            fields = re.split(r"\s+", line.strip())
            if len(fields) == 5:
                device, private_key, public_key, listen_port, fwmark = fields
                if current_device:
                    raw_output.append({"device": current_device, **device_data})
                current_device = device
                device_data = {
                    "private_key": private_key if private_key != "(none)" else None,
                    "public_key": public_key if public_key != "(none)" else None,
                    "listen_port": int(listen_port) if listen_port != "0" else None,
                    "fwmark": int(fwmark) if fwmark != "off" else None,
                    "peers": {},
                }
            elif len(fields) == 9 and fields[0] == "dummy":
                (
                    interface,
                    public_key,
                    preshared_key,
                    endpoint,
                    allowed_ips,
                    latest_handshake,
                    transfer_rx,
                    transfer_tx,
                    persistent_keepalive,
                ) = fields
                peer_data: PeerData = {
                    "preshared_key": preshared_key
                    if preshared_key != "(none)"
                    else None,
                    "endpoint": endpoint if endpoint != "(none)" else None,
                    "latest_handshake": int(latest_handshake),
                    "transfer_rx": int(transfer_rx),
                    "transfer_sx": int(transfer_tx),
                    "persistent_keepalive": int(persistent_keepalive)
                    if persistent_keepalive != "off"
                    else -1,
                    "allowed_ips": allowed_ips.split(",")
                    if allowed_ips != "(none)"
                    else [],
                }
                device_data["peers"][public_key] = {
                    k: v for k, v in peer_data.items() if v is not None
                }

        if current_device:
            raw_output.append({"device": current_device, **device_data})

    return raw_output if raw else _process(raw_output)
```
===== 36 =====
```
                 ) = fields
                 peer_data: PeerData = {
                     "preshared_key": preshared_key
-                    if preshared_key != "(none)"
+                    if preshared_key != "(NONE)"
                     else None,
                     "endpoint": endpoint if endpoint != "(none)" else None,
                     "latest_handshake": int(latest_handshake),
@@ -70,4 +70,4 @@         if current_device:
             raw_output.append({"device": current_device, **device_data})
 
-    return raw_output if raw else _process(raw_output)+    return raw_output if raw else _process(raw_output)
```
```
def parse(data: str, raw: bool = False, quiet: bool = False) -> List[JSONDictType]:
    """
    Main text parsing function.

    Parses the output of the `wg` command, specifically `wg show all dump`, into structured JSON format.

    Parameters:

        data:        (str)  Text data to parse, typically the output from `wg show all dump`
        raw:         (bool) If True, returns unprocessed output
        quiet:       (bool) Suppress warning messages if True

    Returns:

        List[Dict]: Parsed data in JSON-friendly format, either raw or processed.
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)

    raw_output: List[DeviceData] = []
    current_device: Optional[str] = None
    device_data: DeviceData = {}

    if jc.utils.has_data(data):
        for line in filter(None, data.splitlines()):
            fields = re.split(r"\s+", line.strip())
            if len(fields) == 5:
                device, private_key, public_key, listen_port, fwmark = fields
                if current_device:
                    raw_output.append({"device": current_device, **device_data})
                current_device = device
                device_data = {
                    "private_key": private_key if private_key != "(none)" else None,
                    "public_key": public_key if public_key != "(none)" else None,
                    "listen_port": int(listen_port) if listen_port != "0" else None,
                    "fwmark": int(fwmark) if fwmark != "off" else None,
                    "peers": {},
                }
            elif len(fields) == 9:
                (
                    interface,
                    public_key,
                    preshared_key,
                    endpoint,
                    allowed_ips,
                    latest_handshake,
                    transfer_rx,
                    transfer_tx,
                    persistent_keepalive,
                ) = fields
                peer_data: PeerData = {
                    "preshared_key": preshared_key
                    if preshared_key != "(NONE)"
                    else None,
                    "endpoint": endpoint if endpoint != "(none)" else None,
                    "latest_handshake": int(latest_handshake),
                    "transfer_rx": int(transfer_rx),
                    "transfer_sx": int(transfer_tx),
                    "persistent_keepalive": int(persistent_keepalive)
                    if persistent_keepalive != "off"
                    else -1,
                    "allowed_ips": allowed_ips.split(",")
                    if allowed_ips != "(none)"
                    else [],
                }
                device_data["peers"][public_key] = {
                    k: v for k, v in peer_data.items() if v is not None
                }

        if current_device:
            raw_output.append({"device": current_device, **device_data})

    return raw_output if raw else _process(raw_output)

```
===== 37 =====
```
                 ) = fields
                 peer_data: PeerData = {
                     "preshared_key": preshared_key
-                    if preshared_key != "(none)"
+                    if preshared_key != "XX(none)XX"
                     else None,
                     "endpoint": endpoint if endpoint != "(none)" else None,
                     "latest_handshake": int(latest_handshake),
@@ -70,4 +70,4 @@         if current_device:
             raw_output.append({"device": current_device, **device_data})
 
-    return raw_output if raw else _process(raw_output)+    return raw_output if raw else _process(raw_output)
```
```
def parse(data: str, raw: bool = False, quiet: bool = False) -> List[JSONDictType]:
    """
    Main text parsing function.

    Parses the output of the `wg` command, specifically `wg show all dump`, into structured JSON format.

    Parameters:

        data:        (str)  Text data to parse, typically the output from `wg show all dump`
        raw:         (bool) If True, returns unprocessed output
        quiet:       (bool) Suppress warning messages if True

    Returns:

        List[Dict]: Parsed data in JSON-friendly format, either raw or processed.
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)

    raw_output: List[DeviceData] = []
    current_device: Optional[str] = None
    device_data: DeviceData = {}

    if jc.utils.has_data(data):
        for line in filter(None, data.splitlines()):
            fields = re.split(r"\s+", line.strip())
            if len(fields) == 5:
                device, private_key, public_key, listen_port, fwmark = fields
                if current_device:
                    raw_output.append({"device": current_device, **device_data})
                current_device = device
                device_data = {
                    "private_key": private_key if private_key != "(none)" else None,
                    "public_key": public_key if public_key != "(none)" else None,
                    "listen_port": int(listen_port) if listen_port != "0" else None,
                    "fwmark": int(fwmark) if fwmark != "off" else None,
                    "peers": {},
                }
            elif len(fields) == 9:
                (
                    interface,
                    public_key,
                    preshared_key,
                    endpoint,
                    allowed_ips,
                    latest_handshake,
                    transfer_rx,
                    transfer_tx,
                    persistent_keepalive,
                ) = fields
                peer_data: PeerData = {
                    "preshared_key": preshared_key
                    if preshared_key != "XX(none)XX"
                    else None,
                    "endpoint": endpoint if endpoint != "(none)" else None,
                    "latest_handshake": int(latest_handshake),
                    "transfer_rx": int(transfer_rx),
                    "transfer_sx": int(transfer_tx),
                    "persistent_keepalive": int(persistent_keepalive)
                    if persistent_keepalive != "off"
                    else -1,
                    "allowed_ips": allowed_ips.split(",")
                    if allowed_ips != "(none)"
                    else [],
                }
                device_data["peers"][public_key] = {
                    k: v for k, v in peer_data.items() if v is not None
                }

        if current_device:
            raw_output.append({"device": current_device, **device_data})

    return raw_output if raw else _process(raw_output)

```
===== 38 =====
```
                 ) = fields
                 peer_data: PeerData = {
                     "preshared_key": preshared_key
-                    if preshared_key != "(none)"
+                    if preshared_key == "(none)"
                     else None,
                     "endpoint": endpoint if endpoint != "(none)" else None,
                     "latest_handshake": int(latest_handshake),
@@ -70,4 +70,4 @@         if current_device:
             raw_output.append({"device": current_device, **device_data})
 
-    return raw_output if raw else _process(raw_output)+    return raw_output if raw else _process(raw_output)
```
```
def parse(data: str, raw: bool = False, quiet: bool = False) -> List[JSONDictType]:
    """
    Main text parsing function.

    Parses the output of the `wg` command, specifically `wg show all dump`, into structured JSON format.

    Parameters:

        data:        (str)  Text data to parse, typically the output from `wg show all dump`
        raw:         (bool) If True, returns unprocessed output
        quiet:       (bool) Suppress warning messages if True

    Returns:

        List[Dict]: Parsed data in JSON-friendly format, either raw or processed.
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)

    raw_output: List[DeviceData] = []
    current_device: Optional[str] = None
    device_data: DeviceData = {}

    if jc.utils.has_data(data):
        for line in filter(None, data.splitlines()):
            fields = re.split(r"\s+", line.strip())
            if len(fields) == 5:
                device, private_key, public_key, listen_port, fwmark = fields
                if current_device:
                    raw_output.append({"device": current_device, **device_data})
                current_device = device
                device_data = {
                    "private_key": private_key if private_key != "(none)" else None,
                    "public_key": public_key if public_key != "(none)" else None,
                    "listen_port": int(listen_port) if listen_port != "0" else None,
                    "fwmark": int(fwmark) if fwmark != "off" else None,
                    "peers": {},
                }
            elif len(fields) == 9:
                (
                    interface,
                    public_key,
                    preshared_key,
                    endpoint,
                    allowed_ips,
                    latest_handshake,
                    transfer_rx,
                    transfer_tx,
                    persistent_keepalive,
                ) = fields
                peer_data: PeerData = {
                    "preshared_key": preshared_key
                    if preshared_key == "(none)"
                    else None,
                    "endpoint": endpoint if endpoint != "(none)" else None,
                    "latest_handshake": int(latest_handshake),
                    "transfer_rx": int(transfer_rx),
                    "transfer_sx": int(transfer_tx),
                    "persistent_keepalive": int(persistent_keepalive)
                    if persistent_keepalive != "off"
                    else -1,
                    "allowed_ips": allowed_ips.split(",")
                    if allowed_ips != "(none)"
                    else [],
                }
                device_data["peers"][public_key] = {
                    k: v for k, v in peer_data.items() if v is not None
                }

        if current_device:
            raw_output.append({"device": current_device, **device_data})

    return raw_output if raw else _process(raw_output)

```
===== 39 =====
```
                     "preshared_key": preshared_key
                     if preshared_key != "(none)"
                     else None,
-                    "endpoint": endpoint if endpoint != "(none)" else None,
+                    "ENDPOINT": endpoint if endpoint != "(none)" else None,
                     "latest_handshake": int(latest_handshake),
                     "transfer_rx": int(transfer_rx),
                     "transfer_sx": int(transfer_tx),
@@ -70,4 +70,4 @@         if current_device:
             raw_output.append({"device": current_device, **device_data})
 
-    return raw_output if raw else _process(raw_output)+    return raw_output if raw else _process(raw_output)
```
```
def parse(data: str, raw: bool = False, quiet: bool = False) -> List[JSONDictType]:
    """
    Main text parsing function.

    Parses the output of the `wg` command, specifically `wg show all dump`, into structured JSON format.

    Parameters:

        data:        (str)  Text data to parse, typically the output from `wg show all dump`
        raw:         (bool) If True, returns unprocessed output
        quiet:       (bool) Suppress warning messages if True

    Returns:

        List[Dict]: Parsed data in JSON-friendly format, either raw or processed.
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)

    raw_output: List[DeviceData] = []
    current_device: Optional[str] = None
    device_data: DeviceData = {}

    if jc.utils.has_data(data):
        for line in filter(None, data.splitlines()):
            fields = re.split(r"\s+", line.strip())
            if len(fields) == 5:
                device, private_key, public_key, listen_port, fwmark = fields
                if current_device:
                    raw_output.append({"device": current_device, **device_data})
                current_device = device
                device_data = {
                    "private_key": private_key if private_key != "(none)" else None,
                    "public_key": public_key if public_key != "(none)" else None,
                    "listen_port": int(listen_port) if listen_port != "0" else None,
                    "fwmark": int(fwmark) if fwmark != "off" else None,
                    "peers": {},
                }
            elif len(fields) == 9:
                (
                    interface,
                    public_key,
                    preshared_key,
                    endpoint,
                    allowed_ips,
                    latest_handshake,
                    transfer_rx,
                    transfer_tx,
                    persistent_keepalive,
                ) = fields
                peer_data: PeerData = {
                    "preshared_key": preshared_key
                    if preshared_key != "(none)"
                    else None,
                    "ENDPOINT": endpoint if endpoint != "(none)" else None,
                    "latest_handshake": int(latest_handshake),
                    "transfer_rx": int(transfer_rx),
                    "transfer_sx": int(transfer_tx),
                    "persistent_keepalive": int(persistent_keepalive)
                    if persistent_keepalive != "off"
                    else -1,
                    "allowed_ips": allowed_ips.split(",")
                    if allowed_ips != "(none)"
                    else [],
                }
                device_data["peers"][public_key] = {
                    k: v for k, v in peer_data.items() if v is not None
                }

        if current_device:
            raw_output.append({"device": current_device, **device_data})

    return raw_output if raw else _process(raw_output)

```
===== 40 =====
```
                     "preshared_key": preshared_key
                     if preshared_key != "(none)"
                     else None,
-                    "endpoint": endpoint if endpoint != "(none)" else None,
+                    "XXendpointXX": endpoint if endpoint != "(none)" else None,
                     "latest_handshake": int(latest_handshake),
                     "transfer_rx": int(transfer_rx),
                     "transfer_sx": int(transfer_tx),
@@ -70,4 +70,4 @@         if current_device:
             raw_output.append({"device": current_device, **device_data})
 
-    return raw_output if raw else _process(raw_output)+    return raw_output if raw else _process(raw_output)
```
```
def parse(data: str, raw: bool = False, quiet: bool = False) -> List[JSONDictType]:
    """
    Main text parsing function.

    Parses the output of the `wg` command, specifically `wg show all dump`, into structured JSON format.

    Parameters:

        data:        (str)  Text data to parse, typically the output from `wg show all dump`
        raw:         (bool) If True, returns unprocessed output
        quiet:       (bool) Suppress warning messages if True

    Returns:

        List[Dict]: Parsed data in JSON-friendly format, either raw or processed.
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)

    raw_output: List[DeviceData] = []
    current_device: Optional[str] = None
    device_data: DeviceData = {}

    if jc.utils.has_data(data):
        for line in filter(None, data.splitlines()):
            fields = re.split(r"\s+", line.strip())
            if len(fields) == 5:
                device, private_key, public_key, listen_port, fwmark = fields
                if current_device:
                    raw_output.append({"device": current_device, **device_data})
                current_device = device
                device_data = {
                    "private_key": private_key if private_key != "(none)" else None,
                    "public_key": public_key if public_key != "(none)" else None,
                    "listen_port": int(listen_port) if listen_port != "0" else None,
                    "fwmark": int(fwmark) if fwmark != "off" else None,
                    "peers": {},
                }
            elif len(fields) == 9:
                (
                    interface,
                    public_key,
                    preshared_key,
                    endpoint,
                    allowed_ips,
                    latest_handshake,
                    transfer_rx,
                    transfer_tx,
                    persistent_keepalive,
                ) = fields
                peer_data: PeerData = {
                    "preshared_key": preshared_key
                    if preshared_key != "(none)"
                    else None,
                    "XXendpointXX": endpoint if endpoint != "(none)" else None,
                    "latest_handshake": int(latest_handshake),
                    "transfer_rx": int(transfer_rx),
                    "transfer_sx": int(transfer_tx),
                    "persistent_keepalive": int(persistent_keepalive)
                    if persistent_keepalive != "off"
                    else -1,
                    "allowed_ips": allowed_ips.split(",")
                    if allowed_ips != "(none)"
                    else [],
                }
                device_data["peers"][public_key] = {
                    k: v for k, v in peer_data.items() if v is not None
                }

        if current_device:
            raw_output.append({"device": current_device, **device_data})

    return raw_output if raw else _process(raw_output)

```
===== 41 =====
```
                     "preshared_key": preshared_key
                     if preshared_key != "(none)"
                     else None,
-                    "endpoint": endpoint if endpoint != "(none)" else None,
+                    "endpoint": endpoint if endpoint != "(NONE)" else None,
                     "latest_handshake": int(latest_handshake),
                     "transfer_rx": int(transfer_rx),
                     "transfer_sx": int(transfer_tx),
@@ -70,4 +70,4 @@         if current_device:
             raw_output.append({"device": current_device, **device_data})
 
-    return raw_output if raw else _process(raw_output)+    return raw_output if raw else _process(raw_output)
```
```
def parse(data: str, raw: bool = False, quiet: bool = False) -> List[JSONDictType]:
    """
    Main text parsing function.

    Parses the output of the `wg` command, specifically `wg show all dump`, into structured JSON format.

    Parameters:

        data:        (str)  Text data to parse, typically the output from `wg show all dump`
        raw:         (bool) If True, returns unprocessed output
        quiet:       (bool) Suppress warning messages if True

    Returns:

        List[Dict]: Parsed data in JSON-friendly format, either raw or processed.
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)

    raw_output: List[DeviceData] = []
    current_device: Optional[str] = None
    device_data: DeviceData = {}

    if jc.utils.has_data(data):
        for line in filter(None, data.splitlines()):
            fields = re.split(r"\s+", line.strip())
            if len(fields) == 5:
                device, private_key, public_key, listen_port, fwmark = fields
                if current_device:
                    raw_output.append({"device": current_device, **device_data})
                current_device = device
                device_data = {
                    "private_key": private_key if private_key != "(none)" else None,
                    "public_key": public_key if public_key != "(none)" else None,
                    "listen_port": int(listen_port) if listen_port != "0" else None,
                    "fwmark": int(fwmark) if fwmark != "off" else None,
                    "peers": {},
                }
            elif len(fields) == 9:
                (
                    interface,
                    public_key,
                    preshared_key,
                    endpoint,
                    allowed_ips,
                    latest_handshake,
                    transfer_rx,
                    transfer_tx,
                    persistent_keepalive,
                ) = fields
                peer_data: PeerData = {
                    "preshared_key": preshared_key
                    if preshared_key != "(none)"
                    else None,
                    "endpoint": endpoint if endpoint != "(NONE)" else None,
                    "latest_handshake": int(latest_handshake),
                    "transfer_rx": int(transfer_rx),
                    "transfer_sx": int(transfer_tx),
                    "persistent_keepalive": int(persistent_keepalive)
                    if persistent_keepalive != "off"
                    else -1,
                    "allowed_ips": allowed_ips.split(",")
                    if allowed_ips != "(none)"
                    else [],
                }
                device_data["peers"][public_key] = {
                    k: v for k, v in peer_data.items() if v is not None
                }

        if current_device:
            raw_output.append({"device": current_device, **device_data})

    return raw_output if raw else _process(raw_output)

```
===== 42 =====
```
                     "preshared_key": preshared_key
                     if preshared_key != "(none)"
                     else None,
-                    "endpoint": endpoint if endpoint != "(none)" else None,
+                    "endpoint": endpoint if endpoint != "XX(none)XX" else None,
                     "latest_handshake": int(latest_handshake),
                     "transfer_rx": int(transfer_rx),
                     "transfer_sx": int(transfer_tx),
@@ -70,4 +70,4 @@         if current_device:
             raw_output.append({"device": current_device, **device_data})
 
-    return raw_output if raw else _process(raw_output)+    return raw_output if raw else _process(raw_output)
```
```
def parse(data: str, raw: bool = False, quiet: bool = False) -> List[JSONDictType]:
    """
    Main text parsing function.

    Parses the output of the `wg` command, specifically `wg show all dump`, into structured JSON format.

    Parameters:

        data:        (str)  Text data to parse, typically the output from `wg show all dump`
        raw:         (bool) If True, returns unprocessed output
        quiet:       (bool) Suppress warning messages if True

    Returns:

        List[Dict]: Parsed data in JSON-friendly format, either raw or processed.
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)

    raw_output: List[DeviceData] = []
    current_device: Optional[str] = None
    device_data: DeviceData = {}

    if jc.utils.has_data(data):
        for line in filter(None, data.splitlines()):
            fields = re.split(r"\s+", line.strip())
            if len(fields) == 5:
                device, private_key, public_key, listen_port, fwmark = fields
                if current_device:
                    raw_output.append({"device": current_device, **device_data})
                current_device = device
                device_data = {
                    "private_key": private_key if private_key != "(none)" else None,
                    "public_key": public_key if public_key != "(none)" else None,
                    "listen_port": int(listen_port) if listen_port != "0" else None,
                    "fwmark": int(fwmark) if fwmark != "off" else None,
                    "peers": {},
                }
            elif len(fields) == 9:
                (
                    interface,
                    public_key,
                    preshared_key,
                    endpoint,
                    allowed_ips,
                    latest_handshake,
                    transfer_rx,
                    transfer_tx,
                    persistent_keepalive,
                ) = fields
                peer_data: PeerData = {
                    "preshared_key": preshared_key
                    if preshared_key != "(none)"
                    else None,
                    "endpoint": endpoint if endpoint != "XX(none)XX" else None,
                    "latest_handshake": int(latest_handshake),
                    "transfer_rx": int(transfer_rx),
                    "transfer_sx": int(transfer_tx),
                    "persistent_keepalive": int(persistent_keepalive)
                    if persistent_keepalive != "off"
                    else -1,
                    "allowed_ips": allowed_ips.split(",")
                    if allowed_ips != "(none)"
                    else [],
                }
                device_data["peers"][public_key] = {
                    k: v for k, v in peer_data.items() if v is not None
                }

        if current_device:
            raw_output.append({"device": current_device, **device_data})

    return raw_output if raw else _process(raw_output)

```
===== 43 =====
```
                     "preshared_key": preshared_key
                     if preshared_key != "(none)"
                     else None,
-                    "endpoint": endpoint if endpoint != "(none)" else None,
+                    "endpoint": endpoint if endpoint == "(none)" else None,
                     "latest_handshake": int(latest_handshake),
                     "transfer_rx": int(transfer_rx),
                     "transfer_sx": int(transfer_tx),
@@ -70,4 +70,4 @@         if current_device:
             raw_output.append({"device": current_device, **device_data})
 
-    return raw_output if raw else _process(raw_output)+    return raw_output if raw else _process(raw_output)
```
```
def parse(data: str, raw: bool = False, quiet: bool = False) -> List[JSONDictType]:
    """
    Main text parsing function.

    Parses the output of the `wg` command, specifically `wg show all dump`, into structured JSON format.

    Parameters:

        data:        (str)  Text data to parse, typically the output from `wg show all dump`
        raw:         (bool) If True, returns unprocessed output
        quiet:       (bool) Suppress warning messages if True

    Returns:

        List[Dict]: Parsed data in JSON-friendly format, either raw or processed.
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)

    raw_output: List[DeviceData] = []
    current_device: Optional[str] = None
    device_data: DeviceData = {}

    if jc.utils.has_data(data):
        for line in filter(None, data.splitlines()):
            fields = re.split(r"\s+", line.strip())
            if len(fields) == 5:
                device, private_key, public_key, listen_port, fwmark = fields
                if current_device:
                    raw_output.append({"device": current_device, **device_data})
                current_device = device
                device_data = {
                    "private_key": private_key if private_key != "(none)" else None,
                    "public_key": public_key if public_key != "(none)" else None,
                    "listen_port": int(listen_port) if listen_port != "0" else None,
                    "fwmark": int(fwmark) if fwmark != "off" else None,
                    "peers": {},
                }
            elif len(fields) == 9:
                (
                    interface,
                    public_key,
                    preshared_key,
                    endpoint,
                    allowed_ips,
                    latest_handshake,
                    transfer_rx,
                    transfer_tx,
                    persistent_keepalive,
                ) = fields
                peer_data: PeerData = {
                    "preshared_key": preshared_key
                    if preshared_key != "(none)"
                    else None,
                    "endpoint": endpoint if endpoint == "(none)" else None,
                    "latest_handshake": int(latest_handshake),
                    "transfer_rx": int(transfer_rx),
                    "transfer_sx": int(transfer_tx),
                    "persistent_keepalive": int(persistent_keepalive)
                    if persistent_keepalive != "off"
                    else -1,
                    "allowed_ips": allowed_ips.split(",")
                    if allowed_ips != "(none)"
                    else [],
                }
                device_data["peers"][public_key] = {
                    k: v for k, v in peer_data.items() if v is not None
                }

        if current_device:
            raw_output.append({"device": current_device, **device_data})

    return raw_output if raw else _process(raw_output)

```
===== 44 =====
```
                     if preshared_key != "(none)"
                     else None,
                     "endpoint": endpoint if endpoint != "(none)" else None,
-                    "latest_handshake": int(latest_handshake),
+                    "LATEST_HANDSHAKE": int(latest_handshake),
                     "transfer_rx": int(transfer_rx),
                     "transfer_sx": int(transfer_tx),
                     "persistent_keepalive": int(persistent_keepalive)
@@ -70,4 +70,4 @@         if current_device:
             raw_output.append({"device": current_device, **device_data})
 
-    return raw_output if raw else _process(raw_output)+    return raw_output if raw else _process(raw_output)
```
```
def parse(data: str, raw: bool = False, quiet: bool = False) -> List[JSONDictType]:
    """
    Main text parsing function.

    Parses the output of the `wg` command, specifically `wg show all dump`, into structured JSON format.

    Parameters:

        data:        (str)  Text data to parse, typically the output from `wg show all dump`
        raw:         (bool) If True, returns unprocessed output
        quiet:       (bool) Suppress warning messages if True

    Returns:

        List[Dict]: Parsed data in JSON-friendly format, either raw or processed.
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)

    raw_output: List[DeviceData] = []
    current_device: Optional[str] = None
    device_data: DeviceData = {}

    if jc.utils.has_data(data):
        for line in filter(None, data.splitlines()):
            fields = re.split(r"\s+", line.strip())
            if len(fields) == 5:
                device, private_key, public_key, listen_port, fwmark = fields
                if current_device:
                    raw_output.append({"device": current_device, **device_data})
                current_device = device
                device_data = {
                    "private_key": private_key if private_key != "(none)" else None,
                    "public_key": public_key if public_key != "(none)" else None,
                    "listen_port": int(listen_port) if listen_port != "0" else None,
                    "fwmark": int(fwmark) if fwmark != "off" else None,
                    "peers": {},
                }
            elif len(fields) == 9:
                (
                    interface,
                    public_key,
                    preshared_key,
                    endpoint,
                    allowed_ips,
                    latest_handshake,
                    transfer_rx,
                    transfer_tx,
                    persistent_keepalive,
                ) = fields
                peer_data: PeerData = {
                    "preshared_key": preshared_key
                    if preshared_key != "(none)"
                    else None,
                    "endpoint": endpoint if endpoint != "(none)" else None,
                    "LATEST_HANDSHAKE": int(latest_handshake),
                    "transfer_rx": int(transfer_rx),
                    "transfer_sx": int(transfer_tx),
                    "persistent_keepalive": int(persistent_keepalive)
                    if persistent_keepalive != "off"
                    else -1,
                    "allowed_ips": allowed_ips.split(",")
                    if allowed_ips != "(none)"
                    else [],
                }
                device_data["peers"][public_key] = {
                    k: v for k, v in peer_data.items() if v is not None
                }

        if current_device:
            raw_output.append({"device": current_device, **device_data})

    return raw_output if raw else _process(raw_output)

```
===== 45 =====
```
                     if preshared_key != "(none)"
                     else None,
                     "endpoint": endpoint if endpoint != "(none)" else None,
-                    "latest_handshake": int(latest_handshake),
+                    "XXlatest_handshakeXX": int(latest_handshake),
                     "transfer_rx": int(transfer_rx),
                     "transfer_sx": int(transfer_tx),
                     "persistent_keepalive": int(persistent_keepalive)
@@ -70,4 +70,4 @@         if current_device:
             raw_output.append({"device": current_device, **device_data})
 
-    return raw_output if raw else _process(raw_output)+    return raw_output if raw else _process(raw_output)
```
```
def parse(data: str, raw: bool = False, quiet: bool = False) -> List[JSONDictType]:
    """
    Main text parsing function.

    Parses the output of the `wg` command, specifically `wg show all dump`, into structured JSON format.

    Parameters:

        data:        (str)  Text data to parse, typically the output from `wg show all dump`
        raw:         (bool) If True, returns unprocessed output
        quiet:       (bool) Suppress warning messages if True

    Returns:

        List[Dict]: Parsed data in JSON-friendly format, either raw or processed.
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)

    raw_output: List[DeviceData] = []
    current_device: Optional[str] = None
    device_data: DeviceData = {}

    if jc.utils.has_data(data):
        for line in filter(None, data.splitlines()):
            fields = re.split(r"\s+", line.strip())
            if len(fields) == 5:
                device, private_key, public_key, listen_port, fwmark = fields
                if current_device:
                    raw_output.append({"device": current_device, **device_data})
                current_device = device
                device_data = {
                    "private_key": private_key if private_key != "(none)" else None,
                    "public_key": public_key if public_key != "(none)" else None,
                    "listen_port": int(listen_port) if listen_port != "0" else None,
                    "fwmark": int(fwmark) if fwmark != "off" else None,
                    "peers": {},
                }
            elif len(fields) == 9:
                (
                    interface,
                    public_key,
                    preshared_key,
                    endpoint,
                    allowed_ips,
                    latest_handshake,
                    transfer_rx,
                    transfer_tx,
                    persistent_keepalive,
                ) = fields
                peer_data: PeerData = {
                    "preshared_key": preshared_key
                    if preshared_key != "(none)"
                    else None,
                    "endpoint": endpoint if endpoint != "(none)" else None,
                    "XXlatest_handshakeXX": int(latest_handshake),
                    "transfer_rx": int(transfer_rx),
                    "transfer_sx": int(transfer_tx),
                    "persistent_keepalive": int(persistent_keepalive)
                    if persistent_keepalive != "off"
                    else -1,
                    "allowed_ips": allowed_ips.split(",")
                    if allowed_ips != "(none)"
                    else [],
                }
                device_data["peers"][public_key] = {
                    k: v for k, v in peer_data.items() if v is not None
                }

        if current_device:
            raw_output.append({"device": current_device, **device_data})

    return raw_output if raw else _process(raw_output)

```
===== 46 =====
```
                     if preshared_key != "(none)"
                     else None,
                     "endpoint": endpoint if endpoint != "(none)" else None,
-                    "latest_handshake": int(latest_handshake),
+                    "latest_handshake": None,  # Incorrect: sets latest_handshake to None, losing all handshake data
                     "transfer_rx": int(transfer_rx),
                     "transfer_sx": int(transfer_tx),
                     "persistent_keepalive": int(persistent_keepalive)
```
```
def parse(data: str, raw: bool = False, quiet: bool = False) -> List[JSONDictType]:
    """
    Main text parsing function.

    Parses the output of the `wg` command, specifically `wg show all dump`, into structured JSON format.

    Parameters:

        data:        (str)  Text data to parse, typically the output from `wg show all dump`
        raw:         (bool) If True, returns unprocessed output
        quiet:       (bool) Suppress warning messages if True

    Returns:

        List[Dict]: Parsed data in JSON-friendly format, either raw or processed.
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)

    raw_output: List[DeviceData] = []
    current_device: Optional[str] = None
    device_data: DeviceData = {}

    if jc.utils.has_data(data):
        for line in filter(None, data.splitlines()):
            fields = re.split(r"\s+", line.strip())
            if len(fields) == 5:
                device, private_key, public_key, listen_port, fwmark = fields
                if current_device:
                    raw_output.append({"device": current_device, **device_data})
                current_device = device
                device_data = {
                    "private_key": private_key if private_key != "(none)" else None,
                    "public_key": public_key if public_key != "(none)" else None,
                    "listen_port": int(listen_port) if listen_port != "0" else None,
                    "fwmark": int(fwmark) if fwmark != "off" else None,
                    "peers": {},
                }
            elif len(fields) == 9:
                (
                    interface,
                    public_key,
                    preshared_key,
                    endpoint,
                    allowed_ips,
                    latest_handshake,
                    transfer_rx,
                    transfer_tx,
                    persistent_keepalive,
                ) = fields
                peer_data: PeerData = {
                    "preshared_key": preshared_key
                    if preshared_key != "(none)"
                    else None,
                    "endpoint": endpoint if endpoint != "(none)" else None,
                    "latest_handshake": None,  # Incorrect: sets latest_handshake to None, losing all handshake data
                    "transfer_rx": int(transfer_rx),
                    "transfer_sx": int(transfer_tx),
                    "persistent_keepalive": int(persistent_keepalive)
                    if persistent_keepalive != "off"
                    else -1,
                    "allowed_ips": allowed_ips.split(",")
                    if allowed_ips != "(none)"
                    else [],
                }
                device_data["peers"][public_key] = {
                    k: v for k, v in peer_data.items() if v is not None
                }

        if current_device:
            raw_output.append({"device": current_device, **device_data})

    return raw_output if raw else _process(raw_output)
```
===== 47 =====
```
                     if preshared_key != "(none)"
                     else None,
                     "endpoint": endpoint if endpoint != "(none)" else None,
-                    "latest_handshake": int(latest_handshake),
+                    "latest_handshake": int(latest_handshake) + 1,  # Incorrect: introduces an off-by-one error
                     "transfer_rx": int(transfer_rx),
                     "transfer_sx": int(transfer_tx),
                     "persistent_keepalive": int(persistent_keepalive)
```
```
def parse(data: str, raw: bool = False, quiet: bool = False) -> List[JSONDictType]:
    """
    Main text parsing function.

    Parses the output of the `wg` command, specifically `wg show all dump`, into structured JSON format.

    Parameters:

        data:        (str)  Text data to parse, typically the output from `wg show all dump`
        raw:         (bool) If True, returns unprocessed output
        quiet:       (bool) Suppress warning messages if True

    Returns:

        List[Dict]: Parsed data in JSON-friendly format, either raw or processed.
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)

    raw_output: List[DeviceData] = []
    current_device: Optional[str] = None
    device_data: DeviceData = {}

    if jc.utils.has_data(data):
        for line in filter(None, data.splitlines()):
            fields = re.split(r"\s+", line.strip())
            if len(fields) == 5:
                device, private_key, public_key, listen_port, fwmark = fields
                if current_device:
                    raw_output.append({"device": current_device, **device_data})
                current_device = device
                device_data = {
                    "private_key": private_key if private_key != "(none)" else None,
                    "public_key": public_key if public_key != "(none)" else None,
                    "listen_port": int(listen_port) if listen_port != "0" else None,
                    "fwmark": int(fwmark) if fwmark != "off" else None,
                    "peers": {},
                }
            elif len(fields) == 9:
                (
                    interface,
                    public_key,
                    preshared_key,
                    endpoint,
                    allowed_ips,
                    latest_handshake,
                    transfer_rx,
                    transfer_tx,
                    persistent_keepalive,
                ) = fields
                peer_data: PeerData = {
                    "preshared_key": preshared_key
                    if preshared_key != "(none)"
                    else None,
                    "endpoint": endpoint if endpoint != "(none)" else None,
                    "latest_handshake": int(latest_handshake) + 1,  # Incorrect: introduces an off-by-one error
                    "transfer_rx": int(transfer_rx),
                    "transfer_sx": int(transfer_tx),
                    "persistent_keepalive": int(persistent_keepalive)
                    if persistent_keepalive != "off"
                    else -1,
                    "allowed_ips": allowed_ips.split(",")
                    if allowed_ips != "(none)"
                    else [],
                }
                device_data["peers"][public_key] = {
                    k: v for k, v in peer_data.items() if v is not None
                }

        if current_device:
            raw_output.append({"device": current_device, **device_data})

    return raw_output if raw else _process(raw_output)
```
===== 49 =====
```
                     else None,
                     "endpoint": endpoint if endpoint != "(none)" else None,
                     "latest_handshake": int(latest_handshake),
-                    "transfer_rx": int(transfer_rx),
+                    "TRANSFER_RX": int(transfer_rx),
                     "transfer_sx": int(transfer_tx),
                     "persistent_keepalive": int(persistent_keepalive)
                     if persistent_keepalive != "off"
@@ -70,4 +70,4 @@         if current_device:
             raw_output.append({"device": current_device, **device_data})
 
-    return raw_output if raw else _process(raw_output)+    return raw_output if raw else _process(raw_output)
```
```
def parse(data: str, raw: bool = False, quiet: bool = False) -> List[JSONDictType]:
    """
    Main text parsing function.

    Parses the output of the `wg` command, specifically `wg show all dump`, into structured JSON format.

    Parameters:

        data:        (str)  Text data to parse, typically the output from `wg show all dump`
        raw:         (bool) If True, returns unprocessed output
        quiet:       (bool) Suppress warning messages if True

    Returns:

        List[Dict]: Parsed data in JSON-friendly format, either raw or processed.
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)

    raw_output: List[DeviceData] = []
    current_device: Optional[str] = None
    device_data: DeviceData = {}

    if jc.utils.has_data(data):
        for line in filter(None, data.splitlines()):
            fields = re.split(r"\s+", line.strip())
            if len(fields) == 5:
                device, private_key, public_key, listen_port, fwmark = fields
                if current_device:
                    raw_output.append({"device": current_device, **device_data})
                current_device = device
                device_data = {
                    "private_key": private_key if private_key != "(none)" else None,
                    "public_key": public_key if public_key != "(none)" else None,
                    "listen_port": int(listen_port) if listen_port != "0" else None,
                    "fwmark": int(fwmark) if fwmark != "off" else None,
                    "peers": {},
                }
            elif len(fields) == 9:
                (
                    interface,
                    public_key,
                    preshared_key,
                    endpoint,
                    allowed_ips,
                    latest_handshake,
                    transfer_rx,
                    transfer_tx,
                    persistent_keepalive,
                ) = fields
                peer_data: PeerData = {
                    "preshared_key": preshared_key
                    if preshared_key != "(none)"
                    else None,
                    "endpoint": endpoint if endpoint != "(none)" else None,
                    "latest_handshake": int(latest_handshake),
                    "TRANSFER_RX": int(transfer_rx),
                    "transfer_sx": int(transfer_tx),
                    "persistent_keepalive": int(persistent_keepalive)
                    if persistent_keepalive != "off"
                    else -1,
                    "allowed_ips": allowed_ips.split(",")
                    if allowed_ips != "(none)"
                    else [],
                }
                device_data["peers"][public_key] = {
                    k: v for k, v in peer_data.items() if v is not None
                }

        if current_device:
            raw_output.append({"device": current_device, **device_data})

    return raw_output if raw else _process(raw_output)

```
===== 50 =====
```
                     else None,
                     "endpoint": endpoint if endpoint != "(none)" else None,
                     "latest_handshake": int(latest_handshake),
-                    "transfer_rx": int(transfer_rx),
+                    "XXtransfer_rxXX": int(transfer_rx),
                     "transfer_sx": int(transfer_tx),
                     "persistent_keepalive": int(persistent_keepalive)
                     if persistent_keepalive != "off"
@@ -70,4 +70,4 @@         if current_device:
             raw_output.append({"device": current_device, **device_data})
 
-    return raw_output if raw else _process(raw_output)+    return raw_output if raw else _process(raw_output)
```
```
def parse(data: str, raw: bool = False, quiet: bool = False) -> List[JSONDictType]:
    """
    Main text parsing function.

    Parses the output of the `wg` command, specifically `wg show all dump`, into structured JSON format.

    Parameters:

        data:        (str)  Text data to parse, typically the output from `wg show all dump`
        raw:         (bool) If True, returns unprocessed output
        quiet:       (bool) Suppress warning messages if True

    Returns:

        List[Dict]: Parsed data in JSON-friendly format, either raw or processed.
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)

    raw_output: List[DeviceData] = []
    current_device: Optional[str] = None
    device_data: DeviceData = {}

    if jc.utils.has_data(data):
        for line in filter(None, data.splitlines()):
            fields = re.split(r"\s+", line.strip())
            if len(fields) == 5:
                device, private_key, public_key, listen_port, fwmark = fields
                if current_device:
                    raw_output.append({"device": current_device, **device_data})
                current_device = device
                device_data = {
                    "private_key": private_key if private_key != "(none)" else None,
                    "public_key": public_key if public_key != "(none)" else None,
                    "listen_port": int(listen_port) if listen_port != "0" else None,
                    "fwmark": int(fwmark) if fwmark != "off" else None,
                    "peers": {},
                }
            elif len(fields) == 9:
                (
                    interface,
                    public_key,
                    preshared_key,
                    endpoint,
                    allowed_ips,
                    latest_handshake,
                    transfer_rx,
                    transfer_tx,
                    persistent_keepalive,
                ) = fields
                peer_data: PeerData = {
                    "preshared_key": preshared_key
                    if preshared_key != "(none)"
                    else None,
                    "endpoint": endpoint if endpoint != "(none)" else None,
                    "latest_handshake": int(latest_handshake),
                    "XXtransfer_rxXX": int(transfer_rx),
                    "transfer_sx": int(transfer_tx),
                    "persistent_keepalive": int(persistent_keepalive)
                    if persistent_keepalive != "off"
                    else -1,
                    "allowed_ips": allowed_ips.split(",")
                    if allowed_ips != "(none)"
                    else [],
                }
                device_data["peers"][public_key] = {
                    k: v for k, v in peer_data.items() if v is not None
                }

        if current_device:
            raw_output.append({"device": current_device, **device_data})

    return raw_output if raw else _process(raw_output)

```
===== 51 =====
```
                     else None,
                     "endpoint": endpoint if endpoint != "(none)" else None,
                     "latest_handshake": int(latest_handshake),
-                    "transfer_rx": int(transfer_rx),
+                    "transfer_rx": None,  # Incorrectly sets transfer_rx to None, losing the actual value
                     "transfer_sx": int(transfer_tx),
                     "persistent_keepalive": int(persistent_keepalive)
                     if persistent_keepalive != "off"
```
```
def parse(data: str, raw: bool = False, quiet: bool = False) -> List[JSONDictType]:
    """
    Main text parsing function.

    Parses the output of the `wg` command, specifically `wg show all dump`, into structured JSON format.

    Parameters:

        data:        (str)  Text data to parse, typically the output from `wg show all dump`
        raw:         (bool) If True, returns unprocessed output
        quiet:       (bool) Suppress warning messages if True

    Returns:

        List[Dict]: Parsed data in JSON-friendly format, either raw or processed.
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)

    raw_output: List[DeviceData] = []
    current_device: Optional[str] = None
    device_data: DeviceData = {}

    if jc.utils.has_data(data):
        for line in filter(None, data.splitlines()):
            fields = re.split(r"\s+", line.strip())
            if len(fields) == 5:
                device, private_key, public_key, listen_port, fwmark = fields
                if current_device:
                    raw_output.append({"device": current_device, **device_data})
                current_device = device
                device_data = {
                    "private_key": private_key if private_key != "(none)" else None,
                    "public_key": public_key if public_key != "(none)" else None,
                    "listen_port": int(listen_port) if listen_port != "0" else None,
                    "fwmark": int(fwmark) if fwmark != "off" else None,
                    "peers": {},
                }
            elif len(fields) == 9:
                (
                    interface,
                    public_key,
                    preshared_key,
                    endpoint,
                    allowed_ips,
                    latest_handshake,
                    transfer_rx,
                    transfer_tx,
                    persistent_keepalive,
                ) = fields
                peer_data: PeerData = {
                    "preshared_key": preshared_key
                    if preshared_key != "(none)"
                    else None,
                    "endpoint": endpoint if endpoint != "(none)" else None,
                    "latest_handshake": int(latest_handshake),
                    "transfer_rx": None,  # Incorrectly sets transfer_rx to None, losing the actual value
                    "transfer_sx": int(transfer_tx),
                    "persistent_keepalive": int(persistent_keepalive)
                    if persistent_keepalive != "off"
                    else -1,
                    "allowed_ips": allowed_ips.split(",")
                    if allowed_ips != "(none)"
                    else [],
                }
                device_data["peers"][public_key] = {
                    k: v for k, v in peer_data.items() if v is not None
                }

        if current_device:
            raw_output.append({"device": current_device, **device_data})

    return raw_output if raw else _process(raw_output)
```
===== 52 =====
```
                     else None,
                     "endpoint": endpoint if endpoint != "(none)" else None,
                     "latest_handshake": int(latest_handshake),
-                    "transfer_rx": int(transfer_rx),
+                    "transfer_rx": int(transfer_rx) + 1,  # Incorrectly increments the value by 1, introducing an error
                     "transfer_sx": int(transfer_tx),
                     "persistent_keepalive": int(persistent_keepalive)
                     if persistent_keepalive != "off"
```
```
def parse(data: str, raw: bool = False, quiet: bool = False) -> List[JSONDictType]:
    """
    Main text parsing function.

    Parses the output of the `wg` command, specifically `wg show all dump`, into structured JSON format.

    Parameters:

        data:        (str)  Text data to parse, typically the output from `wg show all dump`
        raw:         (bool) If True, returns unprocessed output
        quiet:       (bool) Suppress warning messages if True

    Returns:

        List[Dict]: Parsed data in JSON-friendly format, either raw or processed.
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)

    raw_output: List[DeviceData] = []
    current_device: Optional[str] = None
    device_data: DeviceData = {}

    if jc.utils.has_data(data):
        for line in filter(None, data.splitlines()):
            fields = re.split(r"\s+", line.strip())
            if len(fields) == 5:
                device, private_key, public_key, listen_port, fwmark = fields
                if current_device:
                    raw_output.append({"device": current_device, **device_data})
                current_device = device
                device_data = {
                    "private_key": private_key if private_key != "(none)" else None,
                    "public_key": public_key if public_key != "(none)" else None,
                    "listen_port": int(listen_port) if listen_port != "0" else None,
                    "fwmark": int(fwmark) if fwmark != "off" else None,
                    "peers": {},
                }
            elif len(fields) == 9:
                (
                    interface,
                    public_key,
                    preshared_key,
                    endpoint,
                    allowed_ips,
                    latest_handshake,
                    transfer_rx,
                    transfer_tx,
                    persistent_keepalive,
                ) = fields
                peer_data: PeerData = {
                    "preshared_key": preshared_key
                    if preshared_key != "(none)"
                    else None,
                    "endpoint": endpoint if endpoint != "(none)" else None,
                    "latest_handshake": int(latest_handshake),
                    "transfer_rx": int(transfer_rx) + 1,  # Incorrectly increments the value by 1, introducing an error
                    "transfer_sx": int(transfer_tx),
                    "persistent_keepalive": int(persistent_keepalive)
                    if persistent_keepalive != "off"
                    else -1,
                    "allowed_ips": allowed_ips.split(",")
                    if allowed_ips != "(none)"
                    else [],
                }
                device_data["peers"][public_key] = {
                    k: v for k, v in peer_data.items() if v is not None
                }

        if current_device:
            raw_output.append({"device": current_device, **device_data})

    return raw_output if raw else _process(raw_output)
```
===== 54 =====
```
                     "endpoint": endpoint if endpoint != "(none)" else None,
                     "latest_handshake": int(latest_handshake),
                     "transfer_rx": int(transfer_rx),
-                    "transfer_sx": int(transfer_tx),
+                    "TRANSFER_SX": int(transfer_tx),
                     "persistent_keepalive": int(persistent_keepalive)
                     if persistent_keepalive != "off"
                     else -1,
@@ -70,4 +70,4 @@         if current_device:
             raw_output.append({"device": current_device, **device_data})
 
-    return raw_output if raw else _process(raw_output)+    return raw_output if raw else _process(raw_output)
```
```
def parse(data: str, raw: bool = False, quiet: bool = False) -> List[JSONDictType]:
    """
    Main text parsing function.

    Parses the output of the `wg` command, specifically `wg show all dump`, into structured JSON format.

    Parameters:

        data:        (str)  Text data to parse, typically the output from `wg show all dump`
        raw:         (bool) If True, returns unprocessed output
        quiet:       (bool) Suppress warning messages if True

    Returns:

        List[Dict]: Parsed data in JSON-friendly format, either raw or processed.
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)

    raw_output: List[DeviceData] = []
    current_device: Optional[str] = None
    device_data: DeviceData = {}

    if jc.utils.has_data(data):
        for line in filter(None, data.splitlines()):
            fields = re.split(r"\s+", line.strip())
            if len(fields) == 5:
                device, private_key, public_key, listen_port, fwmark = fields
                if current_device:
                    raw_output.append({"device": current_device, **device_data})
                current_device = device
                device_data = {
                    "private_key": private_key if private_key != "(none)" else None,
                    "public_key": public_key if public_key != "(none)" else None,
                    "listen_port": int(listen_port) if listen_port != "0" else None,
                    "fwmark": int(fwmark) if fwmark != "off" else None,
                    "peers": {},
                }
            elif len(fields) == 9:
                (
                    interface,
                    public_key,
                    preshared_key,
                    endpoint,
                    allowed_ips,
                    latest_handshake,
                    transfer_rx,
                    transfer_tx,
                    persistent_keepalive,
                ) = fields
                peer_data: PeerData = {
                    "preshared_key": preshared_key
                    if preshared_key != "(none)"
                    else None,
                    "endpoint": endpoint if endpoint != "(none)" else None,
                    "latest_handshake": int(latest_handshake),
                    "transfer_rx": int(transfer_rx),
                    "TRANSFER_SX": int(transfer_tx),
                    "persistent_keepalive": int(persistent_keepalive)
                    if persistent_keepalive != "off"
                    else -1,
                    "allowed_ips": allowed_ips.split(",")
                    if allowed_ips != "(none)"
                    else [],
                }
                device_data["peers"][public_key] = {
                    k: v for k, v in peer_data.items() if v is not None
                }

        if current_device:
            raw_output.append({"device": current_device, **device_data})

    return raw_output if raw else _process(raw_output)

```
===== 55 =====
```
                     "endpoint": endpoint if endpoint != "(none)" else None,
                     "latest_handshake": int(latest_handshake),
                     "transfer_rx": int(transfer_rx),
-                    "transfer_sx": int(transfer_tx),
+                    "XXtransfer_sxXX": int(transfer_tx),
                     "persistent_keepalive": int(persistent_keepalive)
                     if persistent_keepalive != "off"
                     else -1,
@@ -70,4 +70,4 @@         if current_device:
             raw_output.append({"device": current_device, **device_data})
 
-    return raw_output if raw else _process(raw_output)+    return raw_output if raw else _process(raw_output)
```
```
def parse(data: str, raw: bool = False, quiet: bool = False) -> List[JSONDictType]:
    """
    Main text parsing function.

    Parses the output of the `wg` command, specifically `wg show all dump`, into structured JSON format.

    Parameters:

        data:        (str)  Text data to parse, typically the output from `wg show all dump`
        raw:         (bool) If True, returns unprocessed output
        quiet:       (bool) Suppress warning messages if True

    Returns:

        List[Dict]: Parsed data in JSON-friendly format, either raw or processed.
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)

    raw_output: List[DeviceData] = []
    current_device: Optional[str] = None
    device_data: DeviceData = {}

    if jc.utils.has_data(data):
        for line in filter(None, data.splitlines()):
            fields = re.split(r"\s+", line.strip())
            if len(fields) == 5:
                device, private_key, public_key, listen_port, fwmark = fields
                if current_device:
                    raw_output.append({"device": current_device, **device_data})
                current_device = device
                device_data = {
                    "private_key": private_key if private_key != "(none)" else None,
                    "public_key": public_key if public_key != "(none)" else None,
                    "listen_port": int(listen_port) if listen_port != "0" else None,
                    "fwmark": int(fwmark) if fwmark != "off" else None,
                    "peers": {},
                }
            elif len(fields) == 9:
                (
                    interface,
                    public_key,
                    preshared_key,
                    endpoint,
                    allowed_ips,
                    latest_handshake,
                    transfer_rx,
                    transfer_tx,
                    persistent_keepalive,
                ) = fields
                peer_data: PeerData = {
                    "preshared_key": preshared_key
                    if preshared_key != "(none)"
                    else None,
                    "endpoint": endpoint if endpoint != "(none)" else None,
                    "latest_handshake": int(latest_handshake),
                    "transfer_rx": int(transfer_rx),
                    "XXtransfer_sxXX": int(transfer_tx),
                    "persistent_keepalive": int(persistent_keepalive)
                    if persistent_keepalive != "off"
                    else -1,
                    "allowed_ips": allowed_ips.split(",")
                    if allowed_ips != "(none)"
                    else [],
                }
                device_data["peers"][public_key] = {
                    k: v for k, v in peer_data.items() if v is not None
                }

        if current_device:
            raw_output.append({"device": current_device, **device_data})

    return raw_output if raw else _process(raw_output)

```
===== 57 =====
```
                     "endpoint": endpoint if endpoint != "(none)" else None,
                     "latest_handshake": int(latest_handshake),
                     "transfer_rx": int(transfer_rx),
-                    "transfer_sx": int(transfer_tx),
+                    "transfer_sx": None,  # Assigns None, which is not valid for the expected integer type
                     "persistent_keepalive": int(persistent_keepalive)
                     if persistent_keepalive != "off"
                     else -1,
```
```
def parse(data: str, raw: bool = False, quiet: bool = False) -> List[JSONDictType]:
    """
    Main text parsing function.

    Parses the output of the `wg` command, specifically `wg show all dump`, into structured JSON format.

    Parameters:

        data:        (str)  Text data to parse, typically the output from `wg show all dump`
        raw:         (bool) If True, returns unprocessed output
        quiet:       (bool) Suppress warning messages if True

    Returns:

        List[Dict]: Parsed data in JSON-friendly format, either raw or processed.
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)

    raw_output: List[DeviceData] = []
    current_device: Optional[str] = None
    device_data: DeviceData = {}

    if jc.utils.has_data(data):
        for line in filter(None, data.splitlines()):
            fields = re.split(r"\s+", line.strip())
            if len(fields) == 5:
                device, private_key, public_key, listen_port, fwmark = fields
                if current_device:
                    raw_output.append({"device": current_device, **device_data})
                current_device = device
                device_data = {
                    "private_key": private_key if private_key != "(none)" else None,
                    "public_key": public_key if public_key != "(none)" else None,
                    "listen_port": int(listen_port) if listen_port != "0" else None,
                    "fwmark": int(fwmark) if fwmark != "off" else None,
                    "peers": {},
                }
            elif len(fields) == 9:
                (
                    interface,
                    public_key,
                    preshared_key,
                    endpoint,
                    allowed_ips,
                    latest_handshake,
                    transfer_rx,
                    transfer_tx,
                    persistent_keepalive,
                ) = fields
                peer_data: PeerData = {
                    "preshared_key": preshared_key
                    if preshared_key != "(none)"
                    else None,
                    "endpoint": endpoint if endpoint != "(none)" else None,
                    "latest_handshake": int(latest_handshake),
                    "transfer_rx": int(transfer_rx),
                    "transfer_sx": None,  # Assigns None, which is not valid for the expected integer type
                    "persistent_keepalive": int(persistent_keepalive)
                    if persistent_keepalive != "off"
                    else -1,
                    "allowed_ips": allowed_ips.split(",")
                    if allowed_ips != "(none)"
                    else [],
                }
                device_data["peers"][public_key] = {
                    k: v for k, v in peer_data.items() if v is not None
                }

        if current_device:
            raw_output.append({"device": current_device, **device_data})

    return raw_output if raw else _process(raw_output)
```
===== 58 =====
```
                     "endpoint": endpoint if endpoint != "(none)" else None,
                     "latest_handshake": int(latest_handshake),
                     "transfer_rx": int(transfer_rx),
-                    "transfer_sx": int(transfer_tx),
+                    "transfer_sx": int(transfer_rx),  # Incorrectly assigns transfer_rx to transfer_sx
                     "persistent_keepalive": int(persistent_keepalive)
                     if persistent_keepalive != "off"
                     else -1,
```
```
def parse(data: str, raw: bool = False, quiet: bool = False) -> List[JSONDictType]:
    """
    Main text parsing function.

    Parses the output of the `wg` command, specifically `wg show all dump`, into structured JSON format.

    Parameters:

        data:        (str)  Text data to parse, typically the output from `wg show all dump`
        raw:         (bool) If True, returns unprocessed output
        quiet:       (bool) Suppress warning messages if True

    Returns:

        List[Dict]: Parsed data in JSON-friendly format, either raw or processed.
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)

    raw_output: List[DeviceData] = []
    current_device: Optional[str] = None
    device_data: DeviceData = {}

    if jc.utils.has_data(data):
        for line in filter(None, data.splitlines()):
            fields = re.split(r"\s+", line.strip())
            if len(fields) == 5:
                device, private_key, public_key, listen_port, fwmark = fields
                if current_device:
                    raw_output.append({"device": current_device, **device_data})
                current_device = device
                device_data = {
                    "private_key": private_key if private_key != "(none)" else None,
                    "public_key": public_key if public_key != "(none)" else None,
                    "listen_port": int(listen_port) if listen_port != "0" else None,
                    "fwmark": int(fwmark) if fwmark != "off" else None,
                    "peers": {},
                }
            elif len(fields) == 9:
                (
                    interface,
                    public_key,
                    preshared_key,
                    endpoint,
                    allowed_ips,
                    latest_handshake,
                    transfer_rx,
                    transfer_tx,
                    persistent_keepalive,
                ) = fields
                peer_data: PeerData = {
                    "preshared_key": preshared_key
                    if preshared_key != "(none)"
                    else None,
                    "endpoint": endpoint if endpoint != "(none)" else None,
                    "latest_handshake": int(latest_handshake),
                    "transfer_rx": int(transfer_rx),
                    "transfer_sx": int(transfer_rx),  # Incorrectly assigns transfer_rx to transfer_sx
                    "persistent_keepalive": int(persistent_keepalive)
                    if persistent_keepalive != "off"
                    else -1,
                    "allowed_ips": allowed_ips.split(",")
                    if allowed_ips != "(none)"
                    else [],
                }
                device_data["peers"][public_key] = {
                    k: v for k, v in peer_data.items() if v is not None
                }

        if current_device:
            raw_output.append({"device": current_device, **device_data})

    return raw_output if raw else _process(raw_output)
```
===== 59 =====
```
                     "endpoint": endpoint if endpoint != "(none)" else None,
                     "latest_handshake": int(latest_handshake),
                     "transfer_rx": int(transfer_rx),
-                    "transfer_sx": int(transfer_tx),
+                    "transfer_sx": int(transfer_tx) + 1,  # Introduces an off-by-one error in the transfer_sx value
                     "persistent_keepalive": int(persistent_keepalive)
                     if persistent_keepalive != "off"
                     else -1,
```
```
def parse(data: str, raw: bool = False, quiet: bool = False) -> List[JSONDictType]:
    """
    Main text parsing function.

    Parses the output of the `wg` command, specifically `wg show all dump`, into structured JSON format.

    Parameters:

        data:        (str)  Text data to parse, typically the output from `wg show all dump`
        raw:         (bool) If True, returns unprocessed output
        quiet:       (bool) Suppress warning messages if True

    Returns:

        List[Dict]: Parsed data in JSON-friendly format, either raw or processed.
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)

    raw_output: List[DeviceData] = []
    current_device: Optional[str] = None
    device_data: DeviceData = {}

    if jc.utils.has_data(data):
        for line in filter(None, data.splitlines()):
            fields = re.split(r"\s+", line.strip())
            if len(fields) == 5:
                device, private_key, public_key, listen_port, fwmark = fields
                if current_device:
                    raw_output.append({"device": current_device, **device_data})
                current_device = device
                device_data = {
                    "private_key": private_key if private_key != "(none)" else None,
                    "public_key": public_key if public_key != "(none)" else None,
                    "listen_port": int(listen_port) if listen_port != "0" else None,
                    "fwmark": int(fwmark) if fwmark != "off" else None,
                    "peers": {},
                }
            elif len(fields) == 9:
                (
                    interface,
                    public_key,
                    preshared_key,
                    endpoint,
                    allowed_ips,
                    latest_handshake,
                    transfer_rx,
                    transfer_tx,
                    persistent_keepalive,
                ) = fields
                peer_data: PeerData = {
                    "preshared_key": preshared_key
                    if preshared_key != "(none)"
                    else None,
                    "endpoint": endpoint if endpoint != "(none)" else None,
                    "latest_handshake": int(latest_handshake),
                    "transfer_rx": int(transfer_rx),
                    "transfer_sx": int(transfer_tx) + 1,  # Introduces an off-by-one error in the transfer_sx value
                    "persistent_keepalive": int(persistent_keepalive)
                    if persistent_keepalive != "off"
                    else -1,
                    "allowed_ips": allowed_ips.split(",")
                    if allowed_ips != "(none)"
                    else [],
                }
                device_data["peers"][public_key] = {
                    k: v for k, v in peer_data.items() if v is not None
                }

        if current_device:
            raw_output.append({"device": current_device, **device_data})

    return raw_output if raw else _process(raw_output)
```
===== 61 =====
```
                     "latest_handshake": int(latest_handshake),
                     "transfer_rx": int(transfer_rx),
                     "transfer_sx": int(transfer_tx),
-                    "persistent_keepalive": int(persistent_keepalive)
+                    "persistent_keepalive": None if persistent_keepalive == "off" else int(persistent_keepalive),
                     if persistent_keepalive != "off"
                     else -1,
                     "allowed_ips": allowed_ips.split(",")
```
```
def parse(data: str, raw: bool = False, quiet: bool = False) -> List[JSONDictType]:
    """
    Main text parsing function.

    Parses the output of the `wg` command, specifically `wg show all dump`, into structured JSON format.

    Parameters:

        data:        (str)  Text data to parse, typically the output from `wg show all dump`
        raw:         (bool) If True, returns unprocessed output
        quiet:       (bool) Suppress warning messages if True

    Returns:

        List[Dict]: Parsed data in JSON-friendly format, either raw or processed.
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)

    raw_output: List[DeviceData] = []
    current_device: Optional[str] = None
    device_data: DeviceData = {}

    if jc.utils.has_data(data):
        for line in filter(None, data.splitlines()):
            fields = re.split(r"\s+", line.strip())
            if len(fields) == 5:
                device, private_key, public_key, listen_port, fwmark = fields
                if current_device:
                    raw_output.append({"device": current_device, **device_data})
                current_device = device
                device_data = {
                    "private_key": private_key if private_key != "(none)" else None,
                    "public_key": public_key if public_key != "(none)" else None,
                    "listen_port": int(listen_port) if listen_port != "0" else None,
                    "fwmark": int(fwmark) if fwmark != "off" else None,
                    "peers": {},
                }
            elif len(fields) == 9:
                (
                    interface,
                    public_key,
                    preshared_key,
                    endpoint,
                    allowed_ips,
                    latest_handshake,
                    transfer_rx,
                    transfer_tx,
                    persistent_keepalive,
                ) = fields
                peer_data: PeerData = {
                    "preshared_key": preshared_key
                    if preshared_key != "(none)"
                    else None,
                    "endpoint": endpoint if endpoint != "(none)" else None,
                    "latest_handshake": int(latest_handshake),
                    "transfer_rx": int(transfer_rx),
                    "transfer_sx": int(transfer_tx),
                    "persistent_keepalive": None if persistent_keepalive == "off" else int(persistent_keepalive),
                    if persistent_keepalive != "off"
                    else -1,
                    "allowed_ips": allowed_ips.split(",")
                    if allowed_ips != "(none)"
                    else [],
                }
                device_data["peers"][public_key] = {
                    k: v for k, v in peer_data.items() if v is not None
                }

        if current_device:
            raw_output.append({"device": current_device, **device_data})

    return raw_output if raw else _process(raw_output)
```
===== 62 =====
```
                     "latest_handshake": int(latest_handshake),
                     "transfer_rx": int(transfer_rx),
                     "transfer_sx": int(transfer_tx),
-                    "persistent_keepalive": int(persistent_keepalive)
+                    "persistent_keepalive": float(persistent_keepalive) if persistent_keepalive != "off" else -1,
                     if persistent_keepalive != "off"
                     else -1,
                     "allowed_ips": allowed_ips.split(",")
```
```
def parse(data: str, raw: bool = False, quiet: bool = False) -> List[JSONDictType]:
    """
    Main text parsing function.

    Parses the output of the `wg` command, specifically `wg show all dump`, into structured JSON format.

    Parameters:

        data:        (str)  Text data to parse, typically the output from `wg show all dump`
        raw:         (bool) If True, returns unprocessed output
        quiet:       (bool) Suppress warning messages if True

    Returns:

        List[Dict]: Parsed data in JSON-friendly format, either raw or processed.
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)

    raw_output: List[DeviceData] = []
    current_device: Optional[str] = None
    device_data: DeviceData = {}

    if jc.utils.has_data(data):
        for line in filter(None, data.splitlines()):
            fields = re.split(r"\s+", line.strip())
            if len(fields) == 5:
                device, private_key, public_key, listen_port, fwmark = fields
                if current_device:
                    raw_output.append({"device": current_device, **device_data})
                current_device = device
                device_data = {
                    "private_key": private_key if private_key != "(none)" else None,
                    "public_key": public_key if public_key != "(none)" else None,
                    "listen_port": int(listen_port) if listen_port != "0" else None,
                    "fwmark": int(fwmark) if fwmark != "off" else None,
                    "peers": {},
                }
            elif len(fields) == 9:
                (
                    interface,
                    public_key,
                    preshared_key,
                    endpoint,
                    allowed_ips,
                    latest_handshake,
                    transfer_rx,
                    transfer_tx,
                    persistent_keepalive,
                ) = fields
                peer_data: PeerData = {
                    "preshared_key": preshared_key
                    if preshared_key != "(none)"
                    else None,
                    "endpoint": endpoint if endpoint != "(none)" else None,
                    "latest_handshake": int(latest_handshake),
                    "transfer_rx": int(transfer_rx),
                    "transfer_sx": int(transfer_tx),
                    "persistent_keepalive": float(persistent_keepalive) if persistent_keepalive != "off" else -1,
                    if persistent_keepalive != "off"
                    else -1,
                    "allowed_ips": allowed_ips.split(",")
                    if allowed_ips != "(none)"
                    else [],
                }
                device_data["peers"][public_key] = {
                    k: v for k, v in peer_data.items() if v is not None
                }

        if current_device:
            raw_output.append({"device": current_device, **device_data})

    return raw_output if raw else _process(raw_output)
```
===== 63 =====
```
                     "latest_handshake": int(latest_handshake),
                     "transfer_rx": int(transfer_rx),
                     "transfer_sx": int(transfer_tx),
-                    "persistent_keepalive": int(persistent_keepalive)
+                    "persistent_keepalive": int(persistent_keepalive) if persistent_keepalive != "off" else 0,
                     if persistent_keepalive != "off"
                     else -1,
                     "allowed_ips": allowed_ips.split(",")
```
```
def parse(data: str, raw: bool = False, quiet: bool = False) -> List[JSONDictType]:
    """
    Main text parsing function.

    Parses the output of the `wg` command, specifically `wg show all dump`, into structured JSON format.

    Parameters:

        data:        (str)  Text data to parse, typically the output from `wg show all dump`
        raw:         (bool) If True, returns unprocessed output
        quiet:       (bool) Suppress warning messages if True

    Returns:

        List[Dict]: Parsed data in JSON-friendly format, either raw or processed.
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)

    raw_output: List[DeviceData] = []
    current_device: Optional[str] = None
    device_data: DeviceData = {}

    if jc.utils.has_data(data):
        for line in filter(None, data.splitlines()):
            fields = re.split(r"\s+", line.strip())
            if len(fields) == 5:
                device, private_key, public_key, listen_port, fwmark = fields
                if current_device:
                    raw_output.append({"device": current_device, **device_data})
                current_device = device
                device_data = {
                    "private_key": private_key if private_key != "(none)" else None,
                    "public_key": public_key if public_key != "(none)" else None,
                    "listen_port": int(listen_port) if listen_port != "0" else None,
                    "fwmark": int(fwmark) if fwmark != "off" else None,
                    "peers": {},
                }
            elif len(fields) == 9:
                (
                    interface,
                    public_key,
                    preshared_key,
                    endpoint,
                    allowed_ips,
                    latest_handshake,
                    transfer_rx,
                    transfer_tx,
                    persistent_keepalive,
                ) = fields
                peer_data: PeerData = {
                    "preshared_key": preshared_key
                    if preshared_key != "(none)"
                    else None,
                    "endpoint": endpoint if endpoint != "(none)" else None,
                    "latest_handshake": int(latest_handshake),
                    "transfer_rx": int(transfer_rx),
                    "transfer_sx": int(transfer_tx),
                    "persistent_keepalive": int(persistent_keepalive) if persistent_keepalive != "off" else 0,
                    if persistent_keepalive != "off"
                    else -1,
                    "allowed_ips": allowed_ips.split(",")
                    if allowed_ips != "(none)"
                    else [],
                }
                device_data["peers"][public_key] = {
                    k: v for k, v in peer_data.items() if v is not None
                }

        if current_device:
            raw_output.append({"device": current_device, **device_data})

    return raw_output if raw else _process(raw_output)
```
===== 64 =====
```
                     "latest_handshake": int(latest_handshake),
                     "transfer_rx": int(transfer_rx),
                     "transfer_sx": int(transfer_tx),
-                    "persistent_keepalive": int(persistent_keepalive)
+                    "persistent_keepalive": int(persistent_keepalive) if persistent_keepalive.isdigit() else -1,
                     if persistent_keepalive != "off"
                     else -1,
                     "allowed_ips": allowed_ips.split(",")
```
```
def parse(data: str, raw: bool = False, quiet: bool = False) -> List[JSONDictType]:
    """
    Main text parsing function.

    Parses the output of the `wg` command, specifically `wg show all dump`, into structured JSON format.

    Parameters:

        data:        (str)  Text data to parse, typically the output from `wg show all dump`
        raw:         (bool) If True, returns unprocessed output
        quiet:       (bool) Suppress warning messages if True

    Returns:

        List[Dict]: Parsed data in JSON-friendly format, either raw or processed.
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)

    raw_output: List[DeviceData] = []
    current_device: Optional[str] = None
    device_data: DeviceData = {}

    if jc.utils.has_data(data):
        for line in filter(None, data.splitlines()):
            fields = re.split(r"\s+", line.strip())
            if len(fields) == 5:
                device, private_key, public_key, listen_port, fwmark = fields
                if current_device:
                    raw_output.append({"device": current_device, **device_data})
                current_device = device
                device_data = {
                    "private_key": private_key if private_key != "(none)" else None,
                    "public_key": public_key if public_key != "(none)" else None,
                    "listen_port": int(listen_port) if listen_port != "0" else None,
                    "fwmark": int(fwmark) if fwmark != "off" else None,
                    "peers": {},
                }
            elif len(fields) == 9:
                (
                    interface,
                    public_key,
                    preshared_key,
                    endpoint,
                    allowed_ips,
                    latest_handshake,
                    transfer_rx,
                    transfer_tx,
                    persistent_keepalive,
                ) = fields
                peer_data: PeerData = {
                    "preshared_key": preshared_key
                    if preshared_key != "(none)"
                    else None,
                    "endpoint": endpoint if endpoint != "(none)" else None,
                    "latest_handshake": int(latest_handshake),
                    "transfer_rx": int(transfer_rx),
                    "transfer_sx": int(transfer_tx),
                    "persistent_keepalive": int(persistent_keepalive) if persistent_keepalive.isdigit() else -1,
                    if persistent_keepalive != "off"
                    else -1,
                    "allowed_ips": allowed_ips.split(",")
                    if allowed_ips != "(none)"
                    else [],
                }
                device_data["peers"][public_key] = {
                    k: v for k, v in peer_data.items() if v is not None
                }

        if current_device:
            raw_output.append({"device": current_device, **device_data})

    return raw_output if raw else _process(raw_output)
```
===== 65 =====
```
                     "latest_handshake": int(latest_handshake),
                     "transfer_rx": int(transfer_rx),
                     "transfer_sx": int(transfer_tx),
-                    "persistent_keepalive": int(persistent_keepalive)
+                    "persistent_keepalive": persistent_keepalive if persistent_keepalive != "off" else None,
                     if persistent_keepalive != "off"
                     else -1,
                     "allowed_ips": allowed_ips.split(",")
```
```
def parse(data: str, raw: bool = False, quiet: bool = False) -> List[JSONDictType]:
    """
    Main text parsing function.

    Parses the output of the `wg` command, specifically `wg show all dump`, into structured JSON format.

    Parameters:

        data:        (str)  Text data to parse, typically the output from `wg show all dump`
        raw:         (bool) If True, returns unprocessed output
        quiet:       (bool) Suppress warning messages if True

    Returns:

        List[Dict]: Parsed data in JSON-friendly format, either raw or processed.
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)

    raw_output: List[DeviceData] = []
    current_device: Optional[str] = None
    device_data: DeviceData = {}

    if jc.utils.has_data(data):
        for line in filter(None, data.splitlines()):
            fields = re.split(r"\s+", line.strip())
            if len(fields) == 5:
                device, private_key, public_key, listen_port, fwmark = fields
                if current_device:
                    raw_output.append({"device": current_device, **device_data})
                current_device = device
                device_data = {
                    "private_key": private_key if private_key != "(none)" else None,
                    "public_key": public_key if public_key != "(none)" else None,
                    "listen_port": int(listen_port) if listen_port != "0" else None,
                    "fwmark": int(fwmark) if fwmark != "off" else None,
                    "peers": {},
                }
            elif len(fields) == 9:
                (
                    interface,
                    public_key,
                    preshared_key,
                    endpoint,
                    allowed_ips,
                    latest_handshake,
                    transfer_rx,
                    transfer_tx,
                    persistent_keepalive,
                ) = fields
                peer_data: PeerData = {
                    "preshared_key": preshared_key
                    if preshared_key != "(none)"
                    else None,
                    "endpoint": endpoint if endpoint != "(none)" else None,
                    "latest_handshake": int(latest_handshake),
                    "transfer_rx": int(transfer_rx),
                    "transfer_sx": int(transfer_tx),
                    "persistent_keepalive": persistent_keepalive if persistent_keepalive != "off" else None,
                    if persistent_keepalive != "off"
                    else -1,
                    "allowed_ips": allowed_ips.split(",")
                    if allowed_ips != "(none)"
                    else [],
                }
                device_data["peers"][public_key] = {
                    k: v for k, v in peer_data.items() if v is not None
                }

        if current_device:
            raw_output.append({"device": current_device, **device_data})

    return raw_output if raw else _process(raw_output)
```
===== 66 =====
```
                     "transfer_sx": int(transfer_tx),
                     "persistent_keepalive": int(persistent_keepalive)
                     if persistent_keepalive != "off"
-                    else -1,
+                    else +1,
                     "allowed_ips": allowed_ips.split(",")
                     if allowed_ips != "(none)"
                     else [],
@@ -70,4 +70,4 @@         if current_device:
             raw_output.append({"device": current_device, **device_data})
 
-    return raw_output if raw else _process(raw_output)+    return raw_output if raw else _process(raw_output)
```
```
def parse(data: str, raw: bool = False, quiet: bool = False) -> List[JSONDictType]:
    """
    Main text parsing function.

    Parses the output of the `wg` command, specifically `wg show all dump`, into structured JSON format.

    Parameters:

        data:        (str)  Text data to parse, typically the output from `wg show all dump`
        raw:         (bool) If True, returns unprocessed output
        quiet:       (bool) Suppress warning messages if True

    Returns:

        List[Dict]: Parsed data in JSON-friendly format, either raw or processed.
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)

    raw_output: List[DeviceData] = []
    current_device: Optional[str] = None
    device_data: DeviceData = {}

    if jc.utils.has_data(data):
        for line in filter(None, data.splitlines()):
            fields = re.split(r"\s+", line.strip())
            if len(fields) == 5:
                device, private_key, public_key, listen_port, fwmark = fields
                if current_device:
                    raw_output.append({"device": current_device, **device_data})
                current_device = device
                device_data = {
                    "private_key": private_key if private_key != "(none)" else None,
                    "public_key": public_key if public_key != "(none)" else None,
                    "listen_port": int(listen_port) if listen_port != "0" else None,
                    "fwmark": int(fwmark) if fwmark != "off" else None,
                    "peers": {},
                }
            elif len(fields) == 9:
                (
                    interface,
                    public_key,
                    preshared_key,
                    endpoint,
                    allowed_ips,
                    latest_handshake,
                    transfer_rx,
                    transfer_tx,
                    persistent_keepalive,
                ) = fields
                peer_data: PeerData = {
                    "preshared_key": preshared_key
                    if preshared_key != "(none)"
                    else None,
                    "endpoint": endpoint if endpoint != "(none)" else None,
                    "latest_handshake": int(latest_handshake),
                    "transfer_rx": int(transfer_rx),
                    "transfer_sx": int(transfer_tx),
                    "persistent_keepalive": int(persistent_keepalive)
                    if persistent_keepalive != "off"
                    else +1,
                    "allowed_ips": allowed_ips.split(",")
                    if allowed_ips != "(none)"
                    else [],
                }
                device_data["peers"][public_key] = {
                    k: v for k, v in peer_data.items() if v is not None
                }

        if current_device:
            raw_output.append({"device": current_device, **device_data})

    return raw_output if raw else _process(raw_output)

```
===== 68 =====
```
                     "persistent_keepalive": int(persistent_keepalive)
                     if persistent_keepalive != "off"
                     else -1,
-                    "allowed_ips": allowed_ips.split(",")
+                    "ALLOWED_IPS": allowed_ips.split(",")
                     if allowed_ips != "(none)"
                     else [],
                 }
@@ -70,4 +70,4 @@         if current_device:
             raw_output.append({"device": current_device, **device_data})
 
-    return raw_output if raw else _process(raw_output)+    return raw_output if raw else _process(raw_output)
```
```
def parse(data: str, raw: bool = False, quiet: bool = False) -> List[JSONDictType]:
    """
    Main text parsing function.

    Parses the output of the `wg` command, specifically `wg show all dump`, into structured JSON format.

    Parameters:

        data:        (str)  Text data to parse, typically the output from `wg show all dump`
        raw:         (bool) If True, returns unprocessed output
        quiet:       (bool) Suppress warning messages if True

    Returns:

        List[Dict]: Parsed data in JSON-friendly format, either raw or processed.
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)

    raw_output: List[DeviceData] = []
    current_device: Optional[str] = None
    device_data: DeviceData = {}

    if jc.utils.has_data(data):
        for line in filter(None, data.splitlines()):
            fields = re.split(r"\s+", line.strip())
            if len(fields) == 5:
                device, private_key, public_key, listen_port, fwmark = fields
                if current_device:
                    raw_output.append({"device": current_device, **device_data})
                current_device = device
                device_data = {
                    "private_key": private_key if private_key != "(none)" else None,
                    "public_key": public_key if public_key != "(none)" else None,
                    "listen_port": int(listen_port) if listen_port != "0" else None,
                    "fwmark": int(fwmark) if fwmark != "off" else None,
                    "peers": {},
                }
            elif len(fields) == 9:
                (
                    interface,
                    public_key,
                    preshared_key,
                    endpoint,
                    allowed_ips,
                    latest_handshake,
                    transfer_rx,
                    transfer_tx,
                    persistent_keepalive,
                ) = fields
                peer_data: PeerData = {
                    "preshared_key": preshared_key
                    if preshared_key != "(none)"
                    else None,
                    "endpoint": endpoint if endpoint != "(none)" else None,
                    "latest_handshake": int(latest_handshake),
                    "transfer_rx": int(transfer_rx),
                    "transfer_sx": int(transfer_tx),
                    "persistent_keepalive": int(persistent_keepalive)
                    if persistent_keepalive != "off"
                    else -1,
                    "ALLOWED_IPS": allowed_ips.split(",")
                    if allowed_ips != "(none)"
                    else [],
                }
                device_data["peers"][public_key] = {
                    k: v for k, v in peer_data.items() if v is not None
                }

        if current_device:
            raw_output.append({"device": current_device, **device_data})

    return raw_output if raw else _process(raw_output)

```
===== 69 =====
```
                     "persistent_keepalive": int(persistent_keepalive)
                     if persistent_keepalive != "off"
                     else -1,
-                    "allowed_ips": allowed_ips.split(",")
+                    "XXallowed_ipsXX": allowed_ips.split(",")
                     if allowed_ips != "(none)"
                     else [],
                 }
@@ -70,4 +70,4 @@         if current_device:
             raw_output.append({"device": current_device, **device_data})
 
-    return raw_output if raw else _process(raw_output)+    return raw_output if raw else _process(raw_output)
```
```
def parse(data: str, raw: bool = False, quiet: bool = False) -> List[JSONDictType]:
    """
    Main text parsing function.

    Parses the output of the `wg` command, specifically `wg show all dump`, into structured JSON format.

    Parameters:

        data:        (str)  Text data to parse, typically the output from `wg show all dump`
        raw:         (bool) If True, returns unprocessed output
        quiet:       (bool) Suppress warning messages if True

    Returns:

        List[Dict]: Parsed data in JSON-friendly format, either raw or processed.
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)

    raw_output: List[DeviceData] = []
    current_device: Optional[str] = None
    device_data: DeviceData = {}

    if jc.utils.has_data(data):
        for line in filter(None, data.splitlines()):
            fields = re.split(r"\s+", line.strip())
            if len(fields) == 5:
                device, private_key, public_key, listen_port, fwmark = fields
                if current_device:
                    raw_output.append({"device": current_device, **device_data})
                current_device = device
                device_data = {
                    "private_key": private_key if private_key != "(none)" else None,
                    "public_key": public_key if public_key != "(none)" else None,
                    "listen_port": int(listen_port) if listen_port != "0" else None,
                    "fwmark": int(fwmark) if fwmark != "off" else None,
                    "peers": {},
                }
            elif len(fields) == 9:
                (
                    interface,
                    public_key,
                    preshared_key,
                    endpoint,
                    allowed_ips,
                    latest_handshake,
                    transfer_rx,
                    transfer_tx,
                    persistent_keepalive,
                ) = fields
                peer_data: PeerData = {
                    "preshared_key": preshared_key
                    if preshared_key != "(none)"
                    else None,
                    "endpoint": endpoint if endpoint != "(none)" else None,
                    "latest_handshake": int(latest_handshake),
                    "transfer_rx": int(transfer_rx),
                    "transfer_sx": int(transfer_tx),
                    "persistent_keepalive": int(persistent_keepalive)
                    if persistent_keepalive != "off"
                    else -1,
                    "XXallowed_ipsXX": allowed_ips.split(",")
                    if allowed_ips != "(none)"
                    else [],
                }
                device_data["peers"][public_key] = {
                    k: v for k, v in peer_data.items() if v is not None
                }

        if current_device:
            raw_output.append({"device": current_device, **device_data})

    return raw_output if raw else _process(raw_output)

```
===== 70 =====
```
                     "persistent_keepalive": int(persistent_keepalive)
                     if persistent_keepalive != "off"
                     else -1,
-                    "allowed_ips": allowed_ips.split(",")
+                    "allowed_ips": [ip.strip() for ip in allowed_ips.split(",") if ip.strip()],  # Filters out empty strings
                     if allowed_ips != "(none)"
                     else [],
                 }
```
```
def parse(data: str, raw: bool = False, quiet: bool = False) -> List[JSONDictType]:
    """
    Main text parsing function.

    Parses the output of the `wg` command, specifically `wg show all dump`, into structured JSON format.

    Parameters:

        data:        (str)  Text data to parse, typically the output from `wg show all dump`
        raw:         (bool) If True, returns unprocessed output
        quiet:       (bool) Suppress warning messages if True

    Returns:

        List[Dict]: Parsed data in JSON-friendly format, either raw or processed.
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)

    raw_output: List[DeviceData] = []
    current_device: Optional[str] = None
    device_data: DeviceData = {}

    if jc.utils.has_data(data):
        for line in filter(None, data.splitlines()):
            fields = re.split(r"\s+", line.strip())
            if len(fields) == 5:
                device, private_key, public_key, listen_port, fwmark = fields
                if current_device:
                    raw_output.append({"device": current_device, **device_data})
                current_device = device
                device_data = {
                    "private_key": private_key if private_key != "(none)" else None,
                    "public_key": public_key if public_key != "(none)" else None,
                    "listen_port": int(listen_port) if listen_port != "0" else None,
                    "fwmark": int(fwmark) if fwmark != "off" else None,
                    "peers": {},
                }
            elif len(fields) == 9:
                (
                    interface,
                    public_key,
                    preshared_key,
                    endpoint,
                    allowed_ips,
                    latest_handshake,
                    transfer_rx,
                    transfer_tx,
                    persistent_keepalive,
                ) = fields
                peer_data: PeerData = {
                    "preshared_key": preshared_key
                    if preshared_key != "(none)"
                    else None,
                    "endpoint": endpoint if endpoint != "(none)" else None,
                    "latest_handshake": int(latest_handshake),
                    "transfer_rx": int(transfer_rx),
                    "transfer_sx": int(transfer_tx),
                    "persistent_keepalive": int(persistent_keepalive)
                    if persistent_keepalive != "off"
                    else -1,
                    "allowed_ips": [ip.strip() for ip in allowed_ips.split(",") if ip.strip()],  # Filters out empty strings
                    if allowed_ips != "(none)"
                    else [],
                }
                device_data["peers"][public_key] = {
                    k: v for k, v in peer_data.items() if v is not None
                }

        if current_device:
            raw_output.append({"device": current_device, **device_data})

    return raw_output if raw else _process(raw_output)
```
===== 71 =====
```
                     "persistent_keepalive": int(persistent_keepalive)
                     if persistent_keepalive != "off"
                     else -1,
-                    "allowed_ips": allowed_ips.split(",")
+                    "allowed_ips": allowed_ips.split(",") + ["0.0.0.0/0"],  # Incorrectly adds a default route
                     if allowed_ips != "(none)"
                     else [],
                 }
```
```
def parse(data: str, raw: bool = False, quiet: bool = False) -> List[JSONDictType]:
    """
    Main text parsing function.

    Parses the output of the `wg` command, specifically `wg show all dump`, into structured JSON format.

    Parameters:

        data:        (str)  Text data to parse, typically the output from `wg show all dump`
        raw:         (bool) If True, returns unprocessed output
        quiet:       (bool) Suppress warning messages if True

    Returns:

        List[Dict]: Parsed data in JSON-friendly format, either raw or processed.
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)

    raw_output: List[DeviceData] = []
    current_device: Optional[str] = None
    device_data: DeviceData = {}

    if jc.utils.has_data(data):
        for line in filter(None, data.splitlines()):
            fields = re.split(r"\s+", line.strip())
            if len(fields) == 5:
                device, private_key, public_key, listen_port, fwmark = fields
                if current_device:
                    raw_output.append({"device": current_device, **device_data})
                current_device = device
                device_data = {
                    "private_key": private_key if private_key != "(none)" else None,
                    "public_key": public_key if public_key != "(none)" else None,
                    "listen_port": int(listen_port) if listen_port != "0" else None,
                    "fwmark": int(fwmark) if fwmark != "off" else None,
                    "peers": {},
                }
            elif len(fields) == 9:
                (
                    interface,
                    public_key,
                    preshared_key,
                    endpoint,
                    allowed_ips,
                    latest_handshake,
                    transfer_rx,
                    transfer_tx,
                    persistent_keepalive,
                ) = fields
                peer_data: PeerData = {
                    "preshared_key": preshared_key
                    if preshared_key != "(none)"
                    else None,
                    "endpoint": endpoint if endpoint != "(none)" else None,
                    "latest_handshake": int(latest_handshake),
                    "transfer_rx": int(transfer_rx),
                    "transfer_sx": int(transfer_tx),
                    "persistent_keepalive": int(persistent_keepalive)
                    if persistent_keepalive != "off"
                    else -1,
                    "allowed_ips": allowed_ips.split(",") + ["0.0.0.0/0"],  # Incorrectly adds a default route
                    if allowed_ips != "(none)"
                    else [],
                }
                device_data["peers"][public_key] = {
                    k: v for k, v in peer_data.items() if v is not None
                }

        if current_device:
            raw_output.append({"device": current_device, **device_data})

    return raw_output if raw else _process(raw_output)
```
===== 72 =====
```
                     "persistent_keepalive": int(persistent_keepalive)
                     if persistent_keepalive != "off"
                     else -1,
-                    "allowed_ips": allowed_ips.split(",")
+                    "allowed_ips": allowed_ips.split(",") if allowed_ips else [],
                     if allowed_ips != "(none)"
                     else [],
                 }
```
```
def parse(data: str, raw: bool = False, quiet: bool = False) -> List[JSONDictType]:
    """
    Main text parsing function.

    Parses the output of the `wg` command, specifically `wg show all dump`, into structured JSON format.

    Parameters:

        data:        (str)  Text data to parse, typically the output from `wg show all dump`
        raw:         (bool) If True, returns unprocessed output
        quiet:       (bool) Suppress warning messages if True

    Returns:

        List[Dict]: Parsed data in JSON-friendly format, either raw or processed.
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)

    raw_output: List[DeviceData] = []
    current_device: Optional[str] = None
    device_data: DeviceData = {}

    if jc.utils.has_data(data):
        for line in filter(None, data.splitlines()):
            fields = re.split(r"\s+", line.strip())
            if len(fields) == 5:
                device, private_key, public_key, listen_port, fwmark = fields
                if current_device:
                    raw_output.append({"device": current_device, **device_data})
                current_device = device
                device_data = {
                    "private_key": private_key if private_key != "(none)" else None,
                    "public_key": public_key if public_key != "(none)" else None,
                    "listen_port": int(listen_port) if listen_port != "0" else None,
                    "fwmark": int(fwmark) if fwmark != "off" else None,
                    "peers": {},
                }
            elif len(fields) == 9:
                (
                    interface,
                    public_key,
                    preshared_key,
                    endpoint,
                    allowed_ips,
                    latest_handshake,
                    transfer_rx,
                    transfer_tx,
                    persistent_keepalive,
                ) = fields
                peer_data: PeerData = {
                    "preshared_key": preshared_key
                    if preshared_key != "(none)"
                    else None,
                    "endpoint": endpoint if endpoint != "(none)" else None,
                    "latest_handshake": int(latest_handshake),
                    "transfer_rx": int(transfer_rx),
                    "transfer_sx": int(transfer_tx),
                    "persistent_keepalive": int(persistent_keepalive)
                    if persistent_keepalive != "off"
                    else -1,
                    "allowed_ips": allowed_ips.split(",") if allowed_ips else [],
                    if allowed_ips != "(none)"
                    else [],
                }
                device_data["peers"][public_key] = {
                    k: v for k, v in peer_data.items() if v is not None
                }

        if current_device:
            raw_output.append({"device": current_device, **device_data})

    return raw_output if raw else _process(raw_output)
```
===== 73 =====
```
                     "persistent_keepalive": int(persistent_keepalive)
                     if persistent_keepalive != "off"
                     else -1,
-                    "allowed_ips": allowed_ips.split(",")
+                    "allowed_ips": allowed_ips.split(",")[:-1],  # Incorrectly removes the last IP
                     if allowed_ips != "(none)"
                     else [],
                 }
```
```
def parse(data: str, raw: bool = False, quiet: bool = False) -> List[JSONDictType]:
    """
    Main text parsing function.

    Parses the output of the `wg` command, specifically `wg show all dump`, into structured JSON format.

    Parameters:

        data:        (str)  Text data to parse, typically the output from `wg show all dump`
        raw:         (bool) If True, returns unprocessed output
        quiet:       (bool) Suppress warning messages if True

    Returns:

        List[Dict]: Parsed data in JSON-friendly format, either raw or processed.
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)

    raw_output: List[DeviceData] = []
    current_device: Optional[str] = None
    device_data: DeviceData = {}

    if jc.utils.has_data(data):
        for line in filter(None, data.splitlines()):
            fields = re.split(r"\s+", line.strip())
            if len(fields) == 5:
                device, private_key, public_key, listen_port, fwmark = fields
                if current_device:
                    raw_output.append({"device": current_device, **device_data})
                current_device = device
                device_data = {
                    "private_key": private_key if private_key != "(none)" else None,
                    "public_key": public_key if public_key != "(none)" else None,
                    "listen_port": int(listen_port) if listen_port != "0" else None,
                    "fwmark": int(fwmark) if fwmark != "off" else None,
                    "peers": {},
                }
            elif len(fields) == 9:
                (
                    interface,
                    public_key,
                    preshared_key,
                    endpoint,
                    allowed_ips,
                    latest_handshake,
                    transfer_rx,
                    transfer_tx,
                    persistent_keepalive,
                ) = fields
                peer_data: PeerData = {
                    "preshared_key": preshared_key
                    if preshared_key != "(none)"
                    else None,
                    "endpoint": endpoint if endpoint != "(none)" else None,
                    "latest_handshake": int(latest_handshake),
                    "transfer_rx": int(transfer_rx),
                    "transfer_sx": int(transfer_tx),
                    "persistent_keepalive": int(persistent_keepalive)
                    if persistent_keepalive != "off"
                    else -1,
                    "allowed_ips": allowed_ips.split(",")[:-1],  # Incorrectly removes the last IP
                    if allowed_ips != "(none)"
                    else [],
                }
                device_data["peers"][public_key] = {
                    k: v for k, v in peer_data.items() if v is not None
                }

        if current_device:
            raw_output.append({"device": current_device, **device_data})

    return raw_output if raw else _process(raw_output)
```
===== 74 =====
```
                     "persistent_keepalive": int(persistent_keepalive)
                     if persistent_keepalive != "off"
                     else -1,
-                    "allowed_ips": allowed_ips.split(",")
+                    "allowed_ips": allowed_ips.split(";"),
                     if allowed_ips != "(none)"
                     else [],
                 }
```
```
def parse(data: str, raw: bool = False, quiet: bool = False) -> List[JSONDictType]:
    """
    Main text parsing function.

    Parses the output of the `wg` command, specifically `wg show all dump`, into structured JSON format.

    Parameters:

        data:        (str)  Text data to parse, typically the output from `wg show all dump`
        raw:         (bool) If True, returns unprocessed output
        quiet:       (bool) Suppress warning messages if True

    Returns:

        List[Dict]: Parsed data in JSON-friendly format, either raw or processed.
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)

    raw_output: List[DeviceData] = []
    current_device: Optional[str] = None
    device_data: DeviceData = {}

    if jc.utils.has_data(data):
        for line in filter(None, data.splitlines()):
            fields = re.split(r"\s+", line.strip())
            if len(fields) == 5:
                device, private_key, public_key, listen_port, fwmark = fields
                if current_device:
                    raw_output.append({"device": current_device, **device_data})
                current_device = device
                device_data = {
                    "private_key": private_key if private_key != "(none)" else None,
                    "public_key": public_key if public_key != "(none)" else None,
                    "listen_port": int(listen_port) if listen_port != "0" else None,
                    "fwmark": int(fwmark) if fwmark != "off" else None,
                    "peers": {},
                }
            elif len(fields) == 9:
                (
                    interface,
                    public_key,
                    preshared_key,
                    endpoint,
                    allowed_ips,
                    latest_handshake,
                    transfer_rx,
                    transfer_tx,
                    persistent_keepalive,
                ) = fields
                peer_data: PeerData = {
                    "preshared_key": preshared_key
                    if preshared_key != "(none)"
                    else None,
                    "endpoint": endpoint if endpoint != "(none)" else None,
                    "latest_handshake": int(latest_handshake),
                    "transfer_rx": int(transfer_rx),
                    "transfer_sx": int(transfer_tx),
                    "persistent_keepalive": int(persistent_keepalive)
                    if persistent_keepalive != "off"
                    else -1,
                    "allowed_ips": allowed_ips.split(";"),
                    if allowed_ips != "(none)"
                    else [],
                }
                device_data["peers"][public_key] = {
                    k: v for k, v in peer_data.items() if v is not None
                }

        if current_device:
            raw_output.append({"device": current_device, **device_data})

    return raw_output if raw else _process(raw_output)
```
===== 75 =====
```
                     if persistent_keepalive != "off"
                     else -1,
                     "allowed_ips": allowed_ips.split(",")
-                    if allowed_ips != "(none)"
+                    if allowed_ips == "(none)"
                     else [],
                 }
                 device_data["peers"][public_key] = {
@@ -70,4 +70,4 @@         if current_device:
             raw_output.append({"device": current_device, **device_data})
 
-    return raw_output if raw else _process(raw_output)+    return raw_output if raw else _process(raw_output)
```
```
def parse(data: str, raw: bool = False, quiet: bool = False) -> List[JSONDictType]:
    """
    Main text parsing function.

    Parses the output of the `wg` command, specifically `wg show all dump`, into structured JSON format.

    Parameters:

        data:        (str)  Text data to parse, typically the output from `wg show all dump`
        raw:         (bool) If True, returns unprocessed output
        quiet:       (bool) Suppress warning messages if True

    Returns:

        List[Dict]: Parsed data in JSON-friendly format, either raw or processed.
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)

    raw_output: List[DeviceData] = []
    current_device: Optional[str] = None
    device_data: DeviceData = {}

    if jc.utils.has_data(data):
        for line in filter(None, data.splitlines()):
            fields = re.split(r"\s+", line.strip())
            if len(fields) == 5:
                device, private_key, public_key, listen_port, fwmark = fields
                if current_device:
                    raw_output.append({"device": current_device, **device_data})
                current_device = device
                device_data = {
                    "private_key": private_key if private_key != "(none)" else None,
                    "public_key": public_key if public_key != "(none)" else None,
                    "listen_port": int(listen_port) if listen_port != "0" else None,
                    "fwmark": int(fwmark) if fwmark != "off" else None,
                    "peers": {},
                }
            elif len(fields) == 9:
                (
                    interface,
                    public_key,
                    preshared_key,
                    endpoint,
                    allowed_ips,
                    latest_handshake,
                    transfer_rx,
                    transfer_tx,
                    persistent_keepalive,
                ) = fields
                peer_data: PeerData = {
                    "preshared_key": preshared_key
                    if preshared_key != "(none)"
                    else None,
                    "endpoint": endpoint if endpoint != "(none)" else None,
                    "latest_handshake": int(latest_handshake),
                    "transfer_rx": int(transfer_rx),
                    "transfer_sx": int(transfer_tx),
                    "persistent_keepalive": int(persistent_keepalive)
                    if persistent_keepalive != "off"
                    else -1,
                    "allowed_ips": allowed_ips.split(",")
                    if allowed_ips == "(none)"
                    else [],
                }
                device_data["peers"][public_key] = {
                    k: v for k, v in peer_data.items() if v is not None
                }

        if current_device:
            raw_output.append({"device": current_device, **device_data})

    return raw_output if raw else _process(raw_output)

```
===== 76 =====
```
                     else [],
                 }
                 device_data["peers"][public_key] = {
-                    k: v for k, v in peer_data.items() if v is not None
+                    device_data["peers"][public_key] = peer_data  # Direct assignment without filtering None values
                 }
 
         if current_device:
```
```
def parse(data: str, raw: bool = False, quiet: bool = False) -> List[JSONDictType]:
    """
    Main text parsing function.

    Parses the output of the `wg` command, specifically `wg show all dump`, into structured JSON format.

    Parameters:

        data:        (str)  Text data to parse, typically the output from `wg show all dump`
        raw:         (bool) If True, returns unprocessed output
        quiet:       (bool) Suppress warning messages if True

    Returns:

        List[Dict]: Parsed data in JSON-friendly format, either raw or processed.
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)

    raw_output: List[DeviceData] = []
    current_device: Optional[str] = None
    device_data: DeviceData = {}

    if jc.utils.has_data(data):
        for line in filter(None, data.splitlines()):
            fields = re.split(r"\s+", line.strip())
            if len(fields) == 5:
                device, private_key, public_key, listen_port, fwmark = fields
                if current_device:
                    raw_output.append({"device": current_device, **device_data})
                current_device = device
                device_data = {
                    "private_key": private_key if private_key != "(none)" else None,
                    "public_key": public_key if public_key != "(none)" else None,
                    "listen_port": int(listen_port) if listen_port != "0" else None,
                    "fwmark": int(fwmark) if fwmark != "off" else None,
                    "peers": {},
                }
            elif len(fields) == 9:
                (
                    interface,
                    public_key,
                    preshared_key,
                    endpoint,
                    allowed_ips,
                    latest_handshake,
                    transfer_rx,
                    transfer_tx,
                    persistent_keepalive,
                ) = fields
                peer_data: PeerData = {
                    "preshared_key": preshared_key
                    if preshared_key != "(none)"
                    else None,
                    "endpoint": endpoint if endpoint != "(none)" else None,
                    "latest_handshake": int(latest_handshake),
                    "transfer_rx": int(transfer_rx),
                    "transfer_sx": int(transfer_tx),
                    "persistent_keepalive": int(persistent_keepalive)
                    if persistent_keepalive != "off"
                    else -1,
                    "allowed_ips": allowed_ips.split(",")
                    if allowed_ips != "(none)"
                    else [],
                }
                device_data["peers"][public_key] = {
                    device_data["peers"][public_key] = peer_data  # Direct assignment without filtering None values
                }

        if current_device:
            raw_output.append({"device": current_device, **device_data})

    return raw_output if raw else _process(raw_output)
```
===== 77 =====
```
                     else [],
                 }
                 device_data["peers"][public_key] = {
-                    k: v for k, v in peer_data.items() if v is not None
+                    device_data["peers"][public_key] = {k: v for k, v in peer_data.items() if isinstance(v, int)}  # Only includes integer values, omitting strings
                 }
 
         if current_device:
```
```
def parse(data: str, raw: bool = False, quiet: bool = False) -> List[JSONDictType]:
    """
    Main text parsing function.

    Parses the output of the `wg` command, specifically `wg show all dump`, into structured JSON format.

    Parameters:

        data:        (str)  Text data to parse, typically the output from `wg show all dump`
        raw:         (bool) If True, returns unprocessed output
        quiet:       (bool) Suppress warning messages if True

    Returns:

        List[Dict]: Parsed data in JSON-friendly format, either raw or processed.
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)

    raw_output: List[DeviceData] = []
    current_device: Optional[str] = None
    device_data: DeviceData = {}

    if jc.utils.has_data(data):
        for line in filter(None, data.splitlines()):
            fields = re.split(r"\s+", line.strip())
            if len(fields) == 5:
                device, private_key, public_key, listen_port, fwmark = fields
                if current_device:
                    raw_output.append({"device": current_device, **device_data})
                current_device = device
                device_data = {
                    "private_key": private_key if private_key != "(none)" else None,
                    "public_key": public_key if public_key != "(none)" else None,
                    "listen_port": int(listen_port) if listen_port != "0" else None,
                    "fwmark": int(fwmark) if fwmark != "off" else None,
                    "peers": {},
                }
            elif len(fields) == 9:
                (
                    interface,
                    public_key,
                    preshared_key,
                    endpoint,
                    allowed_ips,
                    latest_handshake,
                    transfer_rx,
                    transfer_tx,
                    persistent_keepalive,
                ) = fields
                peer_data: PeerData = {
                    "preshared_key": preshared_key
                    if preshared_key != "(none)"
                    else None,
                    "endpoint": endpoint if endpoint != "(none)" else None,
                    "latest_handshake": int(latest_handshake),
                    "transfer_rx": int(transfer_rx),
                    "transfer_sx": int(transfer_tx),
                    "persistent_keepalive": int(persistent_keepalive)
                    if persistent_keepalive != "off"
                    else -1,
                    "allowed_ips": allowed_ips.split(",")
                    if allowed_ips != "(none)"
                    else [],
                }
                device_data["peers"][public_key] = {
                    device_data["peers"][public_key] = {k: v for k, v in peer_data.items() if isinstance(v, int)}  # Only includes integer values, omitting strings
                }

        if current_device:
            raw_output.append({"device": current_device, **device_data})

    return raw_output if raw else _process(raw_output)
```
===== 78 =====
```
                     else [],
                 }
                 device_data["peers"][public_key] = {
-                    k: v for k, v in peer_data.items() if v is not None
+                    device_data["peers"][public_key] = {k: v for k, v in peer_data.items() if k != "preshared_key"}  # Excludes the preshared_key field entirely
                 }
 
         if current_device:
```
```
def parse(data: str, raw: bool = False, quiet: bool = False) -> List[JSONDictType]:
    """
    Main text parsing function.

    Parses the output of the `wg` command, specifically `wg show all dump`, into structured JSON format.

    Parameters:

        data:        (str)  Text data to parse, typically the output from `wg show all dump`
        raw:         (bool) If True, returns unprocessed output
        quiet:       (bool) Suppress warning messages if True

    Returns:

        List[Dict]: Parsed data in JSON-friendly format, either raw or processed.
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)

    raw_output: List[DeviceData] = []
    current_device: Optional[str] = None
    device_data: DeviceData = {}

    if jc.utils.has_data(data):
        for line in filter(None, data.splitlines()):
            fields = re.split(r"\s+", line.strip())
            if len(fields) == 5:
                device, private_key, public_key, listen_port, fwmark = fields
                if current_device:
                    raw_output.append({"device": current_device, **device_data})
                current_device = device
                device_data = {
                    "private_key": private_key if private_key != "(none)" else None,
                    "public_key": public_key if public_key != "(none)" else None,
                    "listen_port": int(listen_port) if listen_port != "0" else None,
                    "fwmark": int(fwmark) if fwmark != "off" else None,
                    "peers": {},
                }
            elif len(fields) == 9:
                (
                    interface,
                    public_key,
                    preshared_key,
                    endpoint,
                    allowed_ips,
                    latest_handshake,
                    transfer_rx,
                    transfer_tx,
                    persistent_keepalive,
                ) = fields
                peer_data: PeerData = {
                    "preshared_key": preshared_key
                    if preshared_key != "(none)"
                    else None,
                    "endpoint": endpoint if endpoint != "(none)" else None,
                    "latest_handshake": int(latest_handshake),
                    "transfer_rx": int(transfer_rx),
                    "transfer_sx": int(transfer_tx),
                    "persistent_keepalive": int(persistent_keepalive)
                    if persistent_keepalive != "off"
                    else -1,
                    "allowed_ips": allowed_ips.split(",")
                    if allowed_ips != "(none)"
                    else [],
                }
                device_data["peers"][public_key] = {
                    device_data["peers"][public_key] = {k: v for k, v in peer_data.items() if k != "preshared_key"}  # Excludes the preshared_key field entirely
                }

        if current_device:
            raw_output.append({"device": current_device, **device_data})

    return raw_output if raw else _process(raw_output)
```
===== 79 =====
```
                     else [],
                 }
                 device_data["peers"][public_key] = {
-                    k: v for k, v in peer_data.items() if v is not None
+                    device_data["peers"][public_key] = {k: v for k, v in peer_data.items() if v is None}  # Only includes None values, resulting in empty dictionaries
                 }
 
         if current_device:
```
```
def parse(data: str, raw: bool = False, quiet: bool = False) -> List[JSONDictType]:
    """
    Main text parsing function.

    Parses the output of the `wg` command, specifically `wg show all dump`, into structured JSON format.

    Parameters:

        data:        (str)  Text data to parse, typically the output from `wg show all dump`
        raw:         (bool) If True, returns unprocessed output
        quiet:       (bool) Suppress warning messages if True

    Returns:

        List[Dict]: Parsed data in JSON-friendly format, either raw or processed.
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)

    raw_output: List[DeviceData] = []
    current_device: Optional[str] = None
    device_data: DeviceData = {}

    if jc.utils.has_data(data):
        for line in filter(None, data.splitlines()):
            fields = re.split(r"\s+", line.strip())
            if len(fields) == 5:
                device, private_key, public_key, listen_port, fwmark = fields
                if current_device:
                    raw_output.append({"device": current_device, **device_data})
                current_device = device
                device_data = {
                    "private_key": private_key if private_key != "(none)" else None,
                    "public_key": public_key if public_key != "(none)" else None,
                    "listen_port": int(listen_port) if listen_port != "0" else None,
                    "fwmark": int(fwmark) if fwmark != "off" else None,
                    "peers": {},
                }
            elif len(fields) == 9:
                (
                    interface,
                    public_key,
                    preshared_key,
                    endpoint,
                    allowed_ips,
                    latest_handshake,
                    transfer_rx,
                    transfer_tx,
                    persistent_keepalive,
                ) = fields
                peer_data: PeerData = {
                    "preshared_key": preshared_key
                    if preshared_key != "(none)"
                    else None,
                    "endpoint": endpoint if endpoint != "(none)" else None,
                    "latest_handshake": int(latest_handshake),
                    "transfer_rx": int(transfer_rx),
                    "transfer_sx": int(transfer_tx),
                    "persistent_keepalive": int(persistent_keepalive)
                    if persistent_keepalive != "off"
                    else -1,
                    "allowed_ips": allowed_ips.split(",")
                    if allowed_ips != "(none)"
                    else [],
                }
                device_data["peers"][public_key] = {
                    device_data["peers"][public_key] = {k: v for k, v in peer_data.items() if v is None}  # Only includes None values, resulting in empty dictionaries
                }

        if current_device:
            raw_output.append({"device": current_device, **device_data})

    return raw_output if raw else _process(raw_output)
```
===== 80 =====
```
                     else [],
                 }
                 device_data["peers"][public_key] = {
-                    k: v for k, v in peer_data.items() if v is not None
+                    device_data["peers"][public_key] = {k: v for k, v in peer_data.items()}  # Includes None values in the dictionary
                 }
 
         if current_device:
```
```
def parse(data: str, raw: bool = False, quiet: bool = False) -> List[JSONDictType]:
    """
    Main text parsing function.

    Parses the output of the `wg` command, specifically `wg show all dump`, into structured JSON format.

    Parameters:

        data:        (str)  Text data to parse, typically the output from `wg show all dump`
        raw:         (bool) If True, returns unprocessed output
        quiet:       (bool) Suppress warning messages if True

    Returns:

        List[Dict]: Parsed data in JSON-friendly format, either raw or processed.
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)

    raw_output: List[DeviceData] = []
    current_device: Optional[str] = None
    device_data: DeviceData = {}

    if jc.utils.has_data(data):
        for line in filter(None, data.splitlines()):
            fields = re.split(r"\s+", line.strip())
            if len(fields) == 5:
                device, private_key, public_key, listen_port, fwmark = fields
                if current_device:
                    raw_output.append({"device": current_device, **device_data})
                current_device = device
                device_data = {
                    "private_key": private_key if private_key != "(none)" else None,
                    "public_key": public_key if public_key != "(none)" else None,
                    "listen_port": int(listen_port) if listen_port != "0" else None,
                    "fwmark": int(fwmark) if fwmark != "off" else None,
                    "peers": {},
                }
            elif len(fields) == 9:
                (
                    interface,
                    public_key,
                    preshared_key,
                    endpoint,
                    allowed_ips,
                    latest_handshake,
                    transfer_rx,
                    transfer_tx,
                    persistent_keepalive,
                ) = fields
                peer_data: PeerData = {
                    "preshared_key": preshared_key
                    if preshared_key != "(none)"
                    else None,
                    "endpoint": endpoint if endpoint != "(none)" else None,
                    "latest_handshake": int(latest_handshake),
                    "transfer_rx": int(transfer_rx),
                    "transfer_sx": int(transfer_tx),
                    "persistent_keepalive": int(persistent_keepalive)
                    if persistent_keepalive != "off"
                    else -1,
                    "allowed_ips": allowed_ips.split(",")
                    if allowed_ips != "(none)"
                    else [],
                }
                device_data["peers"][public_key] = {
                    device_data["peers"][public_key] = {k: v for k, v in peer_data.items()}  # Includes None values in the dictionary
                }

        if current_device:
            raw_output.append({"device": current_device, **device_data})

    return raw_output if raw else _process(raw_output)
```
===== 81 =====
```
                     else [],
                 }
                 device_data["peers"][public_key] = {
-                    k: v for k, v in peer_data.items() if v is not None
+                    k: v for k, v in peer_data.items() if v is None
                 }
 
         if current_device:
             raw_output.append({"device": current_device, **device_data})
 
-    return raw_output if raw else _process(raw_output)+    return raw_output if raw else _process(raw_output)
```
```
def parse(data: str, raw: bool = False, quiet: bool = False) -> List[JSONDictType]:
    """
    Main text parsing function.

    Parses the output of the `wg` command, specifically `wg show all dump`, into structured JSON format.

    Parameters:

        data:        (str)  Text data to parse, typically the output from `wg show all dump`
        raw:         (bool) If True, returns unprocessed output
        quiet:       (bool) Suppress warning messages if True

    Returns:

        List[Dict]: Parsed data in JSON-friendly format, either raw or processed.
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)

    raw_output: List[DeviceData] = []
    current_device: Optional[str] = None
    device_data: DeviceData = {}

    if jc.utils.has_data(data):
        for line in filter(None, data.splitlines()):
            fields = re.split(r"\s+", line.strip())
            if len(fields) == 5:
                device, private_key, public_key, listen_port, fwmark = fields
                if current_device:
                    raw_output.append({"device": current_device, **device_data})
                current_device = device
                device_data = {
                    "private_key": private_key if private_key != "(none)" else None,
                    "public_key": public_key if public_key != "(none)" else None,
                    "listen_port": int(listen_port) if listen_port != "0" else None,
                    "fwmark": int(fwmark) if fwmark != "off" else None,
                    "peers": {},
                }
            elif len(fields) == 9:
                (
                    interface,
                    public_key,
                    preshared_key,
                    endpoint,
                    allowed_ips,
                    latest_handshake,
                    transfer_rx,
                    transfer_tx,
                    persistent_keepalive,
                ) = fields
                peer_data: PeerData = {
                    "preshared_key": preshared_key
                    if preshared_key != "(none)"
                    else None,
                    "endpoint": endpoint if endpoint != "(none)" else None,
                    "latest_handshake": int(latest_handshake),
                    "transfer_rx": int(transfer_rx),
                    "transfer_sx": int(transfer_tx),
                    "persistent_keepalive": int(persistent_keepalive)
                    if persistent_keepalive != "off"
                    else -1,
                    "allowed_ips": allowed_ips.split(",")
                    if allowed_ips != "(none)"
                    else [],
                }
                device_data["peers"][public_key] = {
                    k: v for k, v in peer_data.items() if v is None
                }

        if current_device:
            raw_output.append({"device": current_device, **device_data})

    return raw_output if raw else _process(raw_output)

```
===== 82 =====
```
                     k: v for k, v in peer_data.items() if v is not None
                 }
 
-        if current_device:
+        if current_device == "":
             raw_output.append({"device": current_device, **device_data})
 
     return raw_output if raw else _process(raw_output)
```
```
def parse(data: str, raw: bool = False, quiet: bool = False) -> List[JSONDictType]:
    """
    Main text parsing function.

    Parses the output of the `wg` command, specifically `wg show all dump`, into structured JSON format.

    Parameters:

        data:        (str)  Text data to parse, typically the output from `wg show all dump`
        raw:         (bool) If True, returns unprocessed output
        quiet:       (bool) Suppress warning messages if True

    Returns:

        List[Dict]: Parsed data in JSON-friendly format, either raw or processed.
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)

    raw_output: List[DeviceData] = []
    current_device: Optional[str] = None
    device_data: DeviceData = {}

    if jc.utils.has_data(data):
        for line in filter(None, data.splitlines()):
            fields = re.split(r"\s+", line.strip())
            if len(fields) == 5:
                device, private_key, public_key, listen_port, fwmark = fields
                if current_device:
                    raw_output.append({"device": current_device, **device_data})
                current_device = device
                device_data = {
                    "private_key": private_key if private_key != "(none)" else None,
                    "public_key": public_key if public_key != "(none)" else None,
                    "listen_port": int(listen_port) if listen_port != "0" else None,
                    "fwmark": int(fwmark) if fwmark != "off" else None,
                    "peers": {},
                }
            elif len(fields) == 9:
                (
                    interface,
                    public_key,
                    preshared_key,
                    endpoint,
                    allowed_ips,
                    latest_handshake,
                    transfer_rx,
                    transfer_tx,
                    persistent_keepalive,
                ) = fields
                peer_data: PeerData = {
                    "preshared_key": preshared_key
                    if preshared_key != "(none)"
                    else None,
                    "endpoint": endpoint if endpoint != "(none)" else None,
                    "latest_handshake": int(latest_handshake),
                    "transfer_rx": int(transfer_rx),
                    "transfer_sx": int(transfer_tx),
                    "persistent_keepalive": int(persistent_keepalive)
                    if persistent_keepalive != "off"
                    else -1,
                    "allowed_ips": allowed_ips.split(",")
                    if allowed_ips != "(none)"
                    else [],
                }
                device_data["peers"][public_key] = {
                    k: v for k, v in peer_data.items() if v is not None
                }

        if current_device == "":
            raw_output.append({"device": current_device, **device_data})

    return raw_output if raw else _process(raw_output)
```
===== 83 =====
```
                     k: v for k, v in peer_data.items() if v is not None
                 }
 
-        if current_device:
+        if current_device is None:
             raw_output.append({"device": current_device, **device_data})
 
     return raw_output if raw else _process(raw_output)
```
```
def parse(data: str, raw: bool = False, quiet: bool = False) -> List[JSONDictType]:
    """
    Main text parsing function.

    Parses the output of the `wg` command, specifically `wg show all dump`, into structured JSON format.

    Parameters:

        data:        (str)  Text data to parse, typically the output from `wg show all dump`
        raw:         (bool) If True, returns unprocessed output
        quiet:       (bool) Suppress warning messages if True

    Returns:

        List[Dict]: Parsed data in JSON-friendly format, either raw or processed.
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)

    raw_output: List[DeviceData] = []
    current_device: Optional[str] = None
    device_data: DeviceData = {}

    if jc.utils.has_data(data):
        for line in filter(None, data.splitlines()):
            fields = re.split(r"\s+", line.strip())
            if len(fields) == 5:
                device, private_key, public_key, listen_port, fwmark = fields
                if current_device:
                    raw_output.append({"device": current_device, **device_data})
                current_device = device
                device_data = {
                    "private_key": private_key if private_key != "(none)" else None,
                    "public_key": public_key if public_key != "(none)" else None,
                    "listen_port": int(listen_port) if listen_port != "0" else None,
                    "fwmark": int(fwmark) if fwmark != "off" else None,
                    "peers": {},
                }
            elif len(fields) == 9:
                (
                    interface,
                    public_key,
                    preshared_key,
                    endpoint,
                    allowed_ips,
                    latest_handshake,
                    transfer_rx,
                    transfer_tx,
                    persistent_keepalive,
                ) = fields
                peer_data: PeerData = {
                    "preshared_key": preshared_key
                    if preshared_key != "(none)"
                    else None,
                    "endpoint": endpoint if endpoint != "(none)" else None,
                    "latest_handshake": int(latest_handshake),
                    "transfer_rx": int(transfer_rx),
                    "transfer_sx": int(transfer_tx),
                    "persistent_keepalive": int(persistent_keepalive)
                    if persistent_keepalive != "off"
                    else -1,
                    "allowed_ips": allowed_ips.split(",")
                    if allowed_ips != "(none)"
                    else [],
                }
                device_data["peers"][public_key] = {
                    k: v for k, v in peer_data.items() if v is not None
                }

        if current_device is None:
            raw_output.append({"device": current_device, **device_data})

    return raw_output if raw else _process(raw_output)
```
===== 84 =====
```
                     k: v for k, v in peer_data.items() if v is not None
                 }
 
-        if current_device:
+        if not current_device:
             raw_output.append({"device": current_device, **device_data})
 
     return raw_output if raw else _process(raw_output)
```
```
def parse(data: str, raw: bool = False, quiet: bool = False) -> List[JSONDictType]:
    """
    Main text parsing function.

    Parses the output of the `wg` command, specifically `wg show all dump`, into structured JSON format.

    Parameters:

        data:        (str)  Text data to parse, typically the output from `wg show all dump`
        raw:         (bool) If True, returns unprocessed output
        quiet:       (bool) Suppress warning messages if True

    Returns:

        List[Dict]: Parsed data in JSON-friendly format, either raw or processed.
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)

    raw_output: List[DeviceData] = []
    current_device: Optional[str] = None
    device_data: DeviceData = {}

    if jc.utils.has_data(data):
        for line in filter(None, data.splitlines()):
            fields = re.split(r"\s+", line.strip())
            if len(fields) == 5:
                device, private_key, public_key, listen_port, fwmark = fields
                if current_device:
                    raw_output.append({"device": current_device, **device_data})
                current_device = device
                device_data = {
                    "private_key": private_key if private_key != "(none)" else None,
                    "public_key": public_key if public_key != "(none)" else None,
                    "listen_port": int(listen_port) if listen_port != "0" else None,
                    "fwmark": int(fwmark) if fwmark != "off" else None,
                    "peers": {},
                }
            elif len(fields) == 9:
                (
                    interface,
                    public_key,
                    preshared_key,
                    endpoint,
                    allowed_ips,
                    latest_handshake,
                    transfer_rx,
                    transfer_tx,
                    persistent_keepalive,
                ) = fields
                peer_data: PeerData = {
                    "preshared_key": preshared_key
                    if preshared_key != "(none)"
                    else None,
                    "endpoint": endpoint if endpoint != "(none)" else None,
                    "latest_handshake": int(latest_handshake),
                    "transfer_rx": int(transfer_rx),
                    "transfer_sx": int(transfer_tx),
                    "persistent_keepalive": int(persistent_keepalive)
                    if persistent_keepalive != "off"
                    else -1,
                    "allowed_ips": allowed_ips.split(",")
                    if allowed_ips != "(none)"
                    else [],
                }
                device_data["peers"][public_key] = {
                    k: v for k, v in peer_data.items() if v is not None
                }

        if not current_device:
            raw_output.append({"device": current_device, **device_data})

    return raw_output if raw else _process(raw_output)
```
===== 85 =====
```
                 }
 
         if current_device:
-            raw_output.append({"device": current_device, **device_data})
+            raw_output.append({"device": current_device, "data": device_data})
 
     return raw_output if raw else _process(raw_output)
```
```
def parse(data: str, raw: bool = False, quiet: bool = False) -> List[JSONDictType]:
    """
    Main text parsing function.

    Parses the output of the `wg` command, specifically `wg show all dump`, into structured JSON format.

    Parameters:

        data:        (str)  Text data to parse, typically the output from `wg show all dump`
        raw:         (bool) If True, returns unprocessed output
        quiet:       (bool) Suppress warning messages if True

    Returns:

        List[Dict]: Parsed data in JSON-friendly format, either raw or processed.
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)

    raw_output: List[DeviceData] = []
    current_device: Optional[str] = None
    device_data: DeviceData = {}

    if jc.utils.has_data(data):
        for line in filter(None, data.splitlines()):
            fields = re.split(r"\s+", line.strip())
            if len(fields) == 5:
                device, private_key, public_key, listen_port, fwmark = fields
                if current_device:
                    raw_output.append({"device": current_device, **device_data})
                current_device = device
                device_data = {
                    "private_key": private_key if private_key != "(none)" else None,
                    "public_key": public_key if public_key != "(none)" else None,
                    "listen_port": int(listen_port) if listen_port != "0" else None,
                    "fwmark": int(fwmark) if fwmark != "off" else None,
                    "peers": {},
                }
            elif len(fields) == 9:
                (
                    interface,
                    public_key,
                    preshared_key,
                    endpoint,
                    allowed_ips,
                    latest_handshake,
                    transfer_rx,
                    transfer_tx,
                    persistent_keepalive,
                ) = fields
                peer_data: PeerData = {
                    "preshared_key": preshared_key
                    if preshared_key != "(none)"
                    else None,
                    "endpoint": endpoint if endpoint != "(none)" else None,
                    "latest_handshake": int(latest_handshake),
                    "transfer_rx": int(transfer_rx),
                    "transfer_sx": int(transfer_tx),
                    "persistent_keepalive": int(persistent_keepalive)
                    if persistent_keepalive != "off"
                    else -1,
                    "allowed_ips": allowed_ips.split(",")
                    if allowed_ips != "(none)"
                    else [],
                }
                device_data["peers"][public_key] = {
                    k: v for k, v in peer_data.items() if v is not None
                }

        if current_device:
            raw_output.append({"device": current_device, "data": device_data})

    return raw_output if raw else _process(raw_output)
```
===== 86 =====
```
                 }
 
         if current_device:
-            raw_output.append({"device": current_device, **device_data})
+            raw_output.append({"device": current_device, "fwmark": device_data.get("fwmark")})
 
     return raw_output if raw else _process(raw_output)
```
```
def parse(data: str, raw: bool = False, quiet: bool = False) -> List[JSONDictType]:
    """
    Main text parsing function.

    Parses the output of the `wg` command, specifically `wg show all dump`, into structured JSON format.

    Parameters:

        data:        (str)  Text data to parse, typically the output from `wg show all dump`
        raw:         (bool) If True, returns unprocessed output
        quiet:       (bool) Suppress warning messages if True

    Returns:

        List[Dict]: Parsed data in JSON-friendly format, either raw or processed.
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)

    raw_output: List[DeviceData] = []
    current_device: Optional[str] = None
    device_data: DeviceData = {}

    if jc.utils.has_data(data):
        for line in filter(None, data.splitlines()):
            fields = re.split(r"\s+", line.strip())
            if len(fields) == 5:
                device, private_key, public_key, listen_port, fwmark = fields
                if current_device:
                    raw_output.append({"device": current_device, **device_data})
                current_device = device
                device_data = {
                    "private_key": private_key if private_key != "(none)" else None,
                    "public_key": public_key if public_key != "(none)" else None,
                    "listen_port": int(listen_port) if listen_port != "0" else None,
                    "fwmark": int(fwmark) if fwmark != "off" else None,
                    "peers": {},
                }
            elif len(fields) == 9:
                (
                    interface,
                    public_key,
                    preshared_key,
                    endpoint,
                    allowed_ips,
                    latest_handshake,
                    transfer_rx,
                    transfer_tx,
                    persistent_keepalive,
                ) = fields
                peer_data: PeerData = {
                    "preshared_key": preshared_key
                    if preshared_key != "(none)"
                    else None,
                    "endpoint": endpoint if endpoint != "(none)" else None,
                    "latest_handshake": int(latest_handshake),
                    "transfer_rx": int(transfer_rx),
                    "transfer_sx": int(transfer_tx),
                    "persistent_keepalive": int(persistent_keepalive)
                    if persistent_keepalive != "off"
                    else -1,
                    "allowed_ips": allowed_ips.split(",")
                    if allowed_ips != "(none)"
                    else [],
                }
                device_data["peers"][public_key] = {
                    k: v for k, v in peer_data.items() if v is not None
                }

        if current_device:
            raw_output.append({"device": current_device, "fwmark": device_data.get("fwmark")})

    return raw_output if raw else _process(raw_output)
```
===== 87 =====
```
                 }
 
         if current_device:
-            raw_output.append({"device": current_device, **device_data})
+            raw_output.append({"device": current_device, "peers": device_data["peers"]})
 
     return raw_output if raw else _process(raw_output)
```
```
def parse(data: str, raw: bool = False, quiet: bool = False) -> List[JSONDictType]:
    """
    Main text parsing function.

    Parses the output of the `wg` command, specifically `wg show all dump`, into structured JSON format.

    Parameters:

        data:        (str)  Text data to parse, typically the output from `wg show all dump`
        raw:         (bool) If True, returns unprocessed output
        quiet:       (bool) Suppress warning messages if True

    Returns:

        List[Dict]: Parsed data in JSON-friendly format, either raw or processed.
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)

    raw_output: List[DeviceData] = []
    current_device: Optional[str] = None
    device_data: DeviceData = {}

    if jc.utils.has_data(data):
        for line in filter(None, data.splitlines()):
            fields = re.split(r"\s+", line.strip())
            if len(fields) == 5:
                device, private_key, public_key, listen_port, fwmark = fields
                if current_device:
                    raw_output.append({"device": current_device, **device_data})
                current_device = device
                device_data = {
                    "private_key": private_key if private_key != "(none)" else None,
                    "public_key": public_key if public_key != "(none)" else None,
                    "listen_port": int(listen_port) if listen_port != "0" else None,
                    "fwmark": int(fwmark) if fwmark != "off" else None,
                    "peers": {},
                }
            elif len(fields) == 9:
                (
                    interface,
                    public_key,
                    preshared_key,
                    endpoint,
                    allowed_ips,
                    latest_handshake,
                    transfer_rx,
                    transfer_tx,
                    persistent_keepalive,
                ) = fields
                peer_data: PeerData = {
                    "preshared_key": preshared_key
                    if preshared_key != "(none)"
                    else None,
                    "endpoint": endpoint if endpoint != "(none)" else None,
                    "latest_handshake": int(latest_handshake),
                    "transfer_rx": int(transfer_rx),
                    "transfer_sx": int(transfer_tx),
                    "persistent_keepalive": int(persistent_keepalive)
                    if persistent_keepalive != "off"
                    else -1,
                    "allowed_ips": allowed_ips.split(",")
                    if allowed_ips != "(none)"
                    else [],
                }
                device_data["peers"][public_key] = {
                    k: v for k, v in peer_data.items() if v is not None
                }

        if current_device:
            raw_output.append({"device": current_device, "peers": device_data["peers"]})

    return raw_output if raw else _process(raw_output)
```
===== 88 =====
```
                 }
 
         if current_device:
-            raw_output.append({"device": current_device, **device_data})
+            raw_output.append({"device": current_device, "private_key": device_data.get("private_key")})
 
     return raw_output if raw else _process(raw_output)
```
```
def parse(data: str, raw: bool = False, quiet: bool = False) -> List[JSONDictType]:
    """
    Main text parsing function.

    Parses the output of the `wg` command, specifically `wg show all dump`, into structured JSON format.

    Parameters:

        data:        (str)  Text data to parse, typically the output from `wg show all dump`
        raw:         (bool) If True, returns unprocessed output
        quiet:       (bool) Suppress warning messages if True

    Returns:

        List[Dict]: Parsed data in JSON-friendly format, either raw or processed.
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)

    raw_output: List[DeviceData] = []
    current_device: Optional[str] = None
    device_data: DeviceData = {}

    if jc.utils.has_data(data):
        for line in filter(None, data.splitlines()):
            fields = re.split(r"\s+", line.strip())
            if len(fields) == 5:
                device, private_key, public_key, listen_port, fwmark = fields
                if current_device:
                    raw_output.append({"device": current_device, **device_data})
                current_device = device
                device_data = {
                    "private_key": private_key if private_key != "(none)" else None,
                    "public_key": public_key if public_key != "(none)" else None,
                    "listen_port": int(listen_port) if listen_port != "0" else None,
                    "fwmark": int(fwmark) if fwmark != "off" else None,
                    "peers": {},
                }
            elif len(fields) == 9:
                (
                    interface,
                    public_key,
                    preshared_key,
                    endpoint,
                    allowed_ips,
                    latest_handshake,
                    transfer_rx,
                    transfer_tx,
                    persistent_keepalive,
                ) = fields
                peer_data: PeerData = {
                    "preshared_key": preshared_key
                    if preshared_key != "(none)"
                    else None,
                    "endpoint": endpoint if endpoint != "(none)" else None,
                    "latest_handshake": int(latest_handshake),
                    "transfer_rx": int(transfer_rx),
                    "transfer_sx": int(transfer_tx),
                    "persistent_keepalive": int(persistent_keepalive)
                    if persistent_keepalive != "off"
                    else -1,
                    "allowed_ips": allowed_ips.split(",")
                    if allowed_ips != "(none)"
                    else [],
                }
                device_data["peers"][public_key] = {
                    k: v for k, v in peer_data.items() if v is not None
                }

        if current_device:
            raw_output.append({"device": current_device, "private_key": device_data.get("private_key")})

    return raw_output if raw else _process(raw_output)
```
===== 89 =====
```
                 }
 
         if current_device:
-            raw_output.append({"device": current_device, **device_data})
+            raw_output.append({"device": current_device, **{k: v for k, v in device_data.items() if k != "peers"}})
 
     return raw_output if raw else _process(raw_output)
```
```
def parse(data: str, raw: bool = False, quiet: bool = False) -> List[JSONDictType]:
    """
    Main text parsing function.

    Parses the output of the `wg` command, specifically `wg show all dump`, into structured JSON format.

    Parameters:

        data:        (str)  Text data to parse, typically the output from `wg show all dump`
        raw:         (bool) If True, returns unprocessed output
        quiet:       (bool) Suppress warning messages if True

    Returns:

        List[Dict]: Parsed data in JSON-friendly format, either raw or processed.
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)

    raw_output: List[DeviceData] = []
    current_device: Optional[str] = None
    device_data: DeviceData = {}

    if jc.utils.has_data(data):
        for line in filter(None, data.splitlines()):
            fields = re.split(r"\s+", line.strip())
            if len(fields) == 5:
                device, private_key, public_key, listen_port, fwmark = fields
                if current_device:
                    raw_output.append({"device": current_device, **device_data})
                current_device = device
                device_data = {
                    "private_key": private_key if private_key != "(none)" else None,
                    "public_key": public_key if public_key != "(none)" else None,
                    "listen_port": int(listen_port) if listen_port != "0" else None,
                    "fwmark": int(fwmark) if fwmark != "off" else None,
                    "peers": {},
                }
            elif len(fields) == 9:
                (
                    interface,
                    public_key,
                    preshared_key,
                    endpoint,
                    allowed_ips,
                    latest_handshake,
                    transfer_rx,
                    transfer_tx,
                    persistent_keepalive,
                ) = fields
                peer_data: PeerData = {
                    "preshared_key": preshared_key
                    if preshared_key != "(none)"
                    else None,
                    "endpoint": endpoint if endpoint != "(none)" else None,
                    "latest_handshake": int(latest_handshake),
                    "transfer_rx": int(transfer_rx),
                    "transfer_sx": int(transfer_tx),
                    "persistent_keepalive": int(persistent_keepalive)
                    if persistent_keepalive != "off"
                    else -1,
                    "allowed_ips": allowed_ips.split(",")
                    if allowed_ips != "(none)"
                    else [],
                }
                device_data["peers"][public_key] = {
                    k: v for k, v in peer_data.items() if v is not None
                }

        if current_device:
            raw_output.append({"device": current_device, **{k: v for k, v in device_data.items() if k != "peers"}})

    return raw_output if raw else _process(raw_output)
```
===== 91 =====
```
         if current_device:
             raw_output.append({"device": current_device, **device_data})
 
-    return raw_output if raw else _process(raw_output)+    return raw_output if not raw else _process(raw_output)
```
```
def parse(data: str, raw: bool = False, quiet: bool = False) -> List[JSONDictType]:
    """
    Main text parsing function.

    Parses the output of the `wg` command, specifically `wg show all dump`, into structured JSON format.

    Parameters:

        data:        (str)  Text data to parse, typically the output from `wg show all dump`
        raw:         (bool) If True, returns unprocessed output
        quiet:       (bool) Suppress warning messages if True

    Returns:

        List[Dict]: Parsed data in JSON-friendly format, either raw or processed.
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)

    raw_output: List[DeviceData] = []
    current_device: Optional[str] = None
    device_data: DeviceData = {}

    if jc.utils.has_data(data):
        for line in filter(None, data.splitlines()):
            fields = re.split(r"\s+", line.strip())
            if len(fields) == 5:
                device, private_key, public_key, listen_port, fwmark = fields
                if current_device:
                    raw_output.append({"device": current_device, **device_data})
                current_device = device
                device_data = {
                    "private_key": private_key if private_key != "(none)" else None,
                    "public_key": public_key if public_key != "(none)" else None,
                    "listen_port": int(listen_port) if listen_port != "0" else None,
                    "fwmark": int(fwmark) if fwmark != "off" else None,
                    "peers": {},
                }
            elif len(fields) == 9:
                (
                    interface,
                    public_key,
                    preshared_key,
                    endpoint,
                    allowed_ips,
                    latest_handshake,
                    transfer_rx,
                    transfer_tx,
                    persistent_keepalive,
                ) = fields
                peer_data: PeerData = {
                    "preshared_key": preshared_key
                    if preshared_key != "(none)"
                    else None,
                    "endpoint": endpoint if endpoint != "(none)" else None,
                    "latest_handshake": int(latest_handshake),
                    "transfer_rx": int(transfer_rx),
                    "transfer_sx": int(transfer_tx),
                    "persistent_keepalive": int(persistent_keepalive)
                    if persistent_keepalive != "off"
                    else -1,
                    "allowed_ips": allowed_ips.split(",")
                    if allowed_ips != "(none)"
                    else [],
                }
                device_data["peers"][public_key] = {
                    k: v for k, v in peer_data.items() if v is not None
                }

        if current_device:
            raw_output.append({"device": current_device, **device_data})

    return raw_output if not raw else _process(raw_output)
```
===== 92 =====
```
         if current_device:
             raw_output.append({"device": current_device, **device_data})
 
-    return raw_output if raw else _process(raw_output)+    return raw_output if raw else None
```
```
def parse(data: str, raw: bool = False, quiet: bool = False) -> List[JSONDictType]:
    """
    Main text parsing function.

    Parses the output of the `wg` command, specifically `wg show all dump`, into structured JSON format.

    Parameters:

        data:        (str)  Text data to parse, typically the output from `wg show all dump`
        raw:         (bool) If True, returns unprocessed output
        quiet:       (bool) Suppress warning messages if True

    Returns:

        List[Dict]: Parsed data in JSON-friendly format, either raw or processed.
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)

    raw_output: List[DeviceData] = []
    current_device: Optional[str] = None
    device_data: DeviceData = {}

    if jc.utils.has_data(data):
        for line in filter(None, data.splitlines()):
            fields = re.split(r"\s+", line.strip())
            if len(fields) == 5:
                device, private_key, public_key, listen_port, fwmark = fields
                if current_device:
                    raw_output.append({"device": current_device, **device_data})
                current_device = device
                device_data = {
                    "private_key": private_key if private_key != "(none)" else None,
                    "public_key": public_key if public_key != "(none)" else None,
                    "listen_port": int(listen_port) if listen_port != "0" else None,
                    "fwmark": int(fwmark) if fwmark != "off" else None,
                    "peers": {},
                }
            elif len(fields) == 9:
                (
                    interface,
                    public_key,
                    preshared_key,
                    endpoint,
                    allowed_ips,
                    latest_handshake,
                    transfer_rx,
                    transfer_tx,
                    persistent_keepalive,
                ) = fields
                peer_data: PeerData = {
                    "preshared_key": preshared_key
                    if preshared_key != "(none)"
                    else None,
                    "endpoint": endpoint if endpoint != "(none)" else None,
                    "latest_handshake": int(latest_handshake),
                    "transfer_rx": int(transfer_rx),
                    "transfer_sx": int(transfer_tx),
                    "persistent_keepalive": int(persistent_keepalive)
                    if persistent_keepalive != "off"
                    else -1,
                    "allowed_ips": allowed_ips.split(",")
                    if allowed_ips != "(none)"
                    else [],
                }
                device_data["peers"][public_key] = {
                    k: v for k, v in peer_data.items() if v is not None
                }

        if current_device:
            raw_output.append({"device": current_device, **device_data})

    return raw_output if raw else None
```
===== 93 =====
```
         if current_device:
             raw_output.append({"device": current_device, **device_data})
 
-    return raw_output if raw else _process(raw_output)+    return raw_output if raw else _process(raw_output) + [{}]
```
```
def parse(data: str, raw: bool = False, quiet: bool = False) -> List[JSONDictType]:
    """
    Main text parsing function.

    Parses the output of the `wg` command, specifically `wg show all dump`, into structured JSON format.

    Parameters:

        data:        (str)  Text data to parse, typically the output from `wg show all dump`
        raw:         (bool) If True, returns unprocessed output
        quiet:       (bool) Suppress warning messages if True

    Returns:

        List[Dict]: Parsed data in JSON-friendly format, either raw or processed.
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)

    raw_output: List[DeviceData] = []
    current_device: Optional[str] = None
    device_data: DeviceData = {}

    if jc.utils.has_data(data):
        for line in filter(None, data.splitlines()):
            fields = re.split(r"\s+", line.strip())
            if len(fields) == 5:
                device, private_key, public_key, listen_port, fwmark = fields
                if current_device:
                    raw_output.append({"device": current_device, **device_data})
                current_device = device
                device_data = {
                    "private_key": private_key if private_key != "(none)" else None,
                    "public_key": public_key if public_key != "(none)" else None,
                    "listen_port": int(listen_port) if listen_port != "0" else None,
                    "fwmark": int(fwmark) if fwmark != "off" else None,
                    "peers": {},
                }
            elif len(fields) == 9:
                (
                    interface,
                    public_key,
                    preshared_key,
                    endpoint,
                    allowed_ips,
                    latest_handshake,
                    transfer_rx,
                    transfer_tx,
                    persistent_keepalive,
                ) = fields
                peer_data: PeerData = {
                    "preshared_key": preshared_key
                    if preshared_key != "(none)"
                    else None,
                    "endpoint": endpoint if endpoint != "(none)" else None,
                    "latest_handshake": int(latest_handshake),
                    "transfer_rx": int(transfer_rx),
                    "transfer_sx": int(transfer_tx),
                    "persistent_keepalive": int(persistent_keepalive)
                    if persistent_keepalive != "off"
                    else -1,
                    "allowed_ips": allowed_ips.split(",")
                    if allowed_ips != "(none)"
                    else [],
                }
                device_data["peers"][public_key] = {
                    k: v for k, v in peer_data.items() if v is not None
                }

        if current_device:
            raw_output.append({"device": current_device, **device_data})

    return raw_output if raw else _process(raw_output) + [{}]
```
