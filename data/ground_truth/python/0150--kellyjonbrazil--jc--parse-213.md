https://github.com/kellyjonbrazil/jc/blob/9fd13e698709da95f5ee505ff1fde10564544d48/./jc/parsers/uptime.py#L145-L186
```
@icontract.ensure(
    lambda data, raw, quiet, result:
        (not raw)
        or result == (
            (lambda expected_raw_output:
                expected_raw_output
            )(
                (lambda parts, has_data, has_user:
                    {} if not has_data else (
                        (
                            {
                                'time': parts[0],
                                'uptime': ' '.join(parts[2:-7]).rstrip(','),
                                'users': parts[-7],
                                'load_1m': parts[-3].rstrip(','),
                                'load_5m': parts[-2].rstrip(','),
                                'load_15m': parts[-1],
                            }
                        ) if has_user else (
                            {
                                'time': parts[0],
                                'uptime': ' '.join(parts[2:-5]).rstrip(','),
                                'load_1m': parts[-3].rstrip(','),
                                'load_5m': parts[-2].rstrip(','),
                                'load_15m': parts[-1],
                            }
                        )
                    )
                )(
                    data.split(),
                    jc.utils.has_data(data),
                    'user' in data
                )
            )
        )
)
@icontract.ensure(
    lambda data, raw, quiet, result:
        raw
        or result == (
            (lambda expected_raw_output:
                _process(expected_raw_output)
            )(
                (lambda parts, has_data, has_user:
                    {} if not has_data else (
                        (
                            {
                                'time': parts[0],
                                'uptime': ' '.join(parts[2:-7]).rstrip(','),
                                'users': parts[-7],
                                'load_1m': parts[-3].rstrip(','),
                                'load_5m': parts[-2].rstrip(','),
                                'load_15m': parts[-1],
                            }
                        ) if has_user else (
                            {
                                'time': parts[0],
                                'uptime': ' '.join(parts[2:-5]).rstrip(','),
                                'load_1m': parts[-3].rstrip(','),
                                'load_5m': parts[-2].rstrip(','),
                                'load_15m': parts[-1],
                            }
                        )
                    )
                )(
                    data.split(),
                    jc.utils.has_data(data),
                    'user' in data
                )
            )
        )
)
```
```
@icontract.snapshot(lambda data: data.split(), name="tokens")
@icontract.snapshot(lambda data: ('user' in data), name="has_user")
@icontract.ensure(lambda result, data, raw, OLD: True if not (data and data.strip() and raw) else (isinstance(result, dict) and {'time','uptime','load_1m','load_5m','load_15m'}.issubset(set(result.keys())) and ((OLD.has_user and 'users' in result) or (not OLD.has_user and 'users' not in result)) and result['time'] == OLD.tokens[0] and result['load_1m'] == OLD.tokens[-3].rstrip(',') and result['load_5m'] == OLD.tokens[-2].rstrip(',') and result['load_15m'] == OLD.tokens[-1] and (result['uptime'] == ' '.join(OLD.tokens[2:-7]).rstrip(',') if OLD.has_user else result['uptime'] == ' '.join(OLD.tokens[2:-6]).rstrip(','))))
@icontract.ensure(lambda result, data, raw, OLD: True if not (data and data.strip() and not raw) else result != dict([('time', OLD.tokens[0]), ('uptime', (' '.join(OLD.tokens[2:-7]).rstrip(',') if OLD.has_user else ' '.join(OLD.tokens[2:-6]).rstrip(','))), ('load_1m', OLD.tokens[-3].rstrip(',')), ('load_5m', OLD.tokens[-2].rstrip(',')), ('load_15m', OLD.tokens[-1])] + ([('users', OLD.tokens[-7])] if OLD.has_user else [])))
```
[4, 5, 13, 21, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 60]
===== 4 =====
```
     raw_output = {}
 
     if jc.utils.has_data(data):
-        if 'user' in data:
+        if len(data.split()) > 5:  # This introduces a faulty condition that may skip valid data based on length.
             # standard uptime output
             time, _, *uptime, users, _, _, _, load_1m, load_5m, load_15m = data.split()
```
```
def parse(data, raw=False, quiet=False):
    """
    Main text parsing function

    Parameters:

        data:        (string)  text data to parse
        raw:         (boolean) unprocessed output if True
        quiet:       (boolean) suppress warning messages if True

    Returns:

        Dictionary. Raw or processed structured data
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)

    raw_output = {}

    if jc.utils.has_data(data):
        if len(data.split()) > 5:  # This introduces a faulty condition that may skip valid data based on length.
            # standard uptime output
            time, _, *uptime, users, _, _, _, load_1m, load_5m, load_15m = data.split()

            raw_output['time'] = time
            raw_output['uptime'] = ' '.join(uptime).rstrip(',')
            raw_output['users'] = users
            raw_output['load_1m'] = load_1m.rstrip(',')
            raw_output['load_5m'] = load_5m.rstrip(',')
            raw_output['load_15m'] = load_15m

        else:
            # users information missing (e.g. busybox)
            time, _, *uptime, _, _, load_1m, load_5m, load_15m = data.split()

            raw_output['time'] = time
            raw_output['uptime'] = ' '.join(uptime).rstrip(',')
            raw_output['load_1m'] = load_1m.rstrip(',')
            raw_output['load_5m'] = load_5m.rstrip(',')
            raw_output['load_15m'] = load_15m

    return raw_output if raw else _process(raw_output)
```
===== 5 =====
```
     if jc.utils.has_data(data):
         if 'user' in data:
             # standard uptime output
-            time, _, *uptime, users, _, _, _, load_1m, load_5m, load_15m = data.split()
+            time, _, *uptime, _, users, _, _, load_1m, load_5m, load_15m = data.split()
 
             raw_output['time'] = time
             raw_output['uptime'] = ' '.join(uptime).rstrip(',')
```
```
def parse(data, raw=False, quiet=False):
    """
    Main text parsing function

    Parameters:

        data:        (string)  text data to parse
        raw:         (boolean) unprocessed output if True
        quiet:       (boolean) suppress warning messages if True

    Returns:

        Dictionary. Raw or processed structured data
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)

    raw_output = {}

    if jc.utils.has_data(data):
        if 'user' in data:
            # standard uptime output
            time, _, *uptime, _, users, _, _, load_1m, load_5m, load_15m = data.split()

            raw_output['time'] = time
            raw_output['uptime'] = ' '.join(uptime).rstrip(',')
            raw_output['users'] = users
            raw_output['load_1m'] = load_1m.rstrip(',')
            raw_output['load_5m'] = load_5m.rstrip(',')
            raw_output['load_15m'] = load_15m

        else:
            # users information missing (e.g. busybox)
            time, _, *uptime, _, _, load_1m, load_5m, load_15m = data.split()

            raw_output['time'] = time
            raw_output['uptime'] = ' '.join(uptime).rstrip(',')
            raw_output['load_1m'] = load_1m.rstrip(',')
            raw_output['load_5m'] = load_5m.rstrip(',')
            raw_output['load_15m'] = load_15m

    return raw_output if raw else _process(raw_output)
```
===== 13 =====
```
             time, _, *uptime, users, _, _, _, load_1m, load_5m, load_15m = data.split()
 
             raw_output['time'] = time
-            raw_output['uptime'] = ' '.join(uptime).rstrip(',')
+            raw_output['uptime'] = ' '.join(uptime).replace(',', '')  # Removes all commas
             raw_output['users'] = users
             raw_output['load_1m'] = load_1m.rstrip(',')
             raw_output['load_5m'] = load_5m.rstrip(',')
```
```
def parse(data, raw=False, quiet=False):
    """
    Main text parsing function

    Parameters:

        data:        (string)  text data to parse
        raw:         (boolean) unprocessed output if True
        quiet:       (boolean) suppress warning messages if True

    Returns:

        Dictionary. Raw or processed structured data
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)

    raw_output = {}

    if jc.utils.has_data(data):
        if 'user' in data:
            # standard uptime output
            time, _, *uptime, users, _, _, _, load_1m, load_5m, load_15m = data.split()

            raw_output['time'] = time
            raw_output['uptime'] = ' '.join(uptime).replace(',', '')  # Removes all commas
            raw_output['users'] = users
            raw_output['load_1m'] = load_1m.rstrip(',')
            raw_output['load_5m'] = load_5m.rstrip(',')
            raw_output['load_15m'] = load_15m

        else:
            # users information missing (e.g. busybox)
            time, _, *uptime, _, _, load_1m, load_5m, load_15m = data.split()

            raw_output['time'] = time
            raw_output['uptime'] = ' '.join(uptime).rstrip(',')
            raw_output['load_1m'] = load_1m.rstrip(',')
            raw_output['load_5m'] = load_5m.rstrip(',')
            raw_output['load_15m'] = load_15m

    return raw_output if raw else _process(raw_output)
```
===== 21 =====
```
 
             raw_output['time'] = time
             raw_output['uptime'] = ' '.join(uptime).rstrip(',')
-            raw_output['users'] = users
+            raw_output['users'] = None
             raw_output['load_1m'] = load_1m.rstrip(',')
             raw_output['load_5m'] = load_5m.rstrip(',')
             raw_output['load_15m'] = load_15m
@@ -39,4 +39,4 @@             raw_output['load_5m'] = load_5m.rstrip(',')
             raw_output['load_15m'] = load_15m
 
-    return raw_output if raw else _process(raw_output)+    return raw_output if raw else _process(raw_output)
```
```
def parse(data, raw=False, quiet=False):
    """
    Main text parsing function

    Parameters:

        data:        (string)  text data to parse
        raw:         (boolean) unprocessed output if True
        quiet:       (boolean) suppress warning messages if True

    Returns:

        Dictionary. Raw or processed structured data
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)

    raw_output = {}

    if jc.utils.has_data(data):
        if 'user' in data:
            # standard uptime output
            time, _, *uptime, users, _, _, _, load_1m, load_5m, load_15m = data.split()

            raw_output['time'] = time
            raw_output['uptime'] = ' '.join(uptime).rstrip(',')
            raw_output['users'] = None
            raw_output['load_1m'] = load_1m.rstrip(',')
            raw_output['load_5m'] = load_5m.rstrip(',')
            raw_output['load_15m'] = load_15m

        else:
            # users information missing (e.g. busybox)
            time, _, *uptime, _, _, load_1m, load_5m, load_15m = data.split()

            raw_output['time'] = time
            raw_output['uptime'] = ' '.join(uptime).rstrip(',')
            raw_output['load_1m'] = load_1m.rstrip(',')
            raw_output['load_5m'] = load_5m.rstrip(',')
            raw_output['load_15m'] = load_15m

    return raw_output if raw else _process(raw_output)

```
===== 35 =====
```
 
         else:
             # users information missing (e.g. busybox)
-            time, _, *uptime, _, _, load_1m, load_5m, load_15m = data.split()
+            time, _, *uptime, _, _, load_1m, load_5m, load_15m, users = data.split()
 
             raw_output['time'] = time
             raw_output['uptime'] = ' '.join(uptime).rstrip(',')
```
```
def parse(data, raw=False, quiet=False):
    """
    Main text parsing function

    Parameters:

        data:        (string)  text data to parse
        raw:         (boolean) unprocessed output if True
        quiet:       (boolean) suppress warning messages if True

    Returns:

        Dictionary. Raw or processed structured data
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)

    raw_output = {}

    if jc.utils.has_data(data):
        if 'user' in data:
            # standard uptime output
            time, _, *uptime, users, _, _, _, load_1m, load_5m, load_15m = data.split()

            raw_output['time'] = time
            raw_output['uptime'] = ' '.join(uptime).rstrip(',')
            raw_output['users'] = users
            raw_output['load_1m'] = load_1m.rstrip(',')
            raw_output['load_5m'] = load_5m.rstrip(',')
            raw_output['load_15m'] = load_15m

        else:
            # users information missing (e.g. busybox)
            time, _, *uptime, _, _, load_1m, load_5m, load_15m, users = data.split()

            raw_output['time'] = time
            raw_output['uptime'] = ' '.join(uptime).rstrip(',')
            raw_output['load_1m'] = load_1m.rstrip(',')
            raw_output['load_5m'] = load_5m.rstrip(',')
            raw_output['load_15m'] = load_15m

    return raw_output if raw else _process(raw_output)
```
===== 36 =====
```
 
         else:
             # users information missing (e.g. busybox)
-            time, _, *uptime, _, _, load_1m, load_5m, load_15m = data.split()
+            time, _, *uptime, users, _, _, load_1m, load_5m, load_15m, extra = data.split()
 
             raw_output['time'] = time
             raw_output['uptime'] = ' '.join(uptime).rstrip(',')
```
```
def parse(data, raw=False, quiet=False):
    """
    Main text parsing function

    Parameters:

        data:        (string)  text data to parse
        raw:         (boolean) unprocessed output if True
        quiet:       (boolean) suppress warning messages if True

    Returns:

        Dictionary. Raw or processed structured data
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)

    raw_output = {}

    if jc.utils.has_data(data):
        if 'user' in data:
            # standard uptime output
            time, _, *uptime, users, _, _, _, load_1m, load_5m, load_15m = data.split()

            raw_output['time'] = time
            raw_output['uptime'] = ' '.join(uptime).rstrip(',')
            raw_output['users'] = users
            raw_output['load_1m'] = load_1m.rstrip(',')
            raw_output['load_5m'] = load_5m.rstrip(',')
            raw_output['load_15m'] = load_15m

        else:
            # users information missing (e.g. busybox)
            time, _, *uptime, users, _, _, load_1m, load_5m, load_15m, extra = data.split()

            raw_output['time'] = time
            raw_output['uptime'] = ' '.join(uptime).rstrip(',')
            raw_output['load_1m'] = load_1m.rstrip(',')
            raw_output['load_5m'] = load_5m.rstrip(',')
            raw_output['load_15m'] = load_15m

    return raw_output if raw else _process(raw_output)
```
===== 37 =====
```
             # users information missing (e.g. busybox)
             time, _, *uptime, _, _, load_1m, load_5m, load_15m = data.split()
 
-            raw_output['time'] = time
+            raw_output['TIME'] = time
             raw_output['uptime'] = ' '.join(uptime).rstrip(',')
             raw_output['load_1m'] = load_1m.rstrip(',')
             raw_output['load_5m'] = load_5m.rstrip(',')
             raw_output['load_15m'] = load_15m
 
-    return raw_output if raw else _process(raw_output)+    return raw_output if raw else _process(raw_output)
```
```
def parse(data, raw=False, quiet=False):
    """
    Main text parsing function

    Parameters:

        data:        (string)  text data to parse
        raw:         (boolean) unprocessed output if True
        quiet:       (boolean) suppress warning messages if True

    Returns:

        Dictionary. Raw or processed structured data
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)

    raw_output = {}

    if jc.utils.has_data(data):
        if 'user' in data:
            # standard uptime output
            time, _, *uptime, users, _, _, _, load_1m, load_5m, load_15m = data.split()

            raw_output['time'] = time
            raw_output['uptime'] = ' '.join(uptime).rstrip(',')
            raw_output['users'] = users
            raw_output['load_1m'] = load_1m.rstrip(',')
            raw_output['load_5m'] = load_5m.rstrip(',')
            raw_output['load_15m'] = load_15m

        else:
            # users information missing (e.g. busybox)
            time, _, *uptime, _, _, load_1m, load_5m, load_15m = data.split()

            raw_output['TIME'] = time
            raw_output['uptime'] = ' '.join(uptime).rstrip(',')
            raw_output['load_1m'] = load_1m.rstrip(',')
            raw_output['load_5m'] = load_5m.rstrip(',')
            raw_output['load_15m'] = load_15m

    return raw_output if raw else _process(raw_output)

```
===== 38 =====
```
             # users information missing (e.g. busybox)
             time, _, *uptime, _, _, load_1m, load_5m, load_15m = data.split()
 
-            raw_output['time'] = time
+            raw_output['XXtimeXX'] = time
             raw_output['uptime'] = ' '.join(uptime).rstrip(',')
             raw_output['load_1m'] = load_1m.rstrip(',')
             raw_output['load_5m'] = load_5m.rstrip(',')
             raw_output['load_15m'] = load_15m
 
-    return raw_output if raw else _process(raw_output)+    return raw_output if raw else _process(raw_output)
```
```
def parse(data, raw=False, quiet=False):
    """
    Main text parsing function

    Parameters:

        data:        (string)  text data to parse
        raw:         (boolean) unprocessed output if True
        quiet:       (boolean) suppress warning messages if True

    Returns:

        Dictionary. Raw or processed structured data
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)

    raw_output = {}

    if jc.utils.has_data(data):
        if 'user' in data:
            # standard uptime output
            time, _, *uptime, users, _, _, _, load_1m, load_5m, load_15m = data.split()

            raw_output['time'] = time
            raw_output['uptime'] = ' '.join(uptime).rstrip(',')
            raw_output['users'] = users
            raw_output['load_1m'] = load_1m.rstrip(',')
            raw_output['load_5m'] = load_5m.rstrip(',')
            raw_output['load_15m'] = load_15m

        else:
            # users information missing (e.g. busybox)
            time, _, *uptime, _, _, load_1m, load_5m, load_15m = data.split()

            raw_output['XXtimeXX'] = time
            raw_output['uptime'] = ' '.join(uptime).rstrip(',')
            raw_output['load_1m'] = load_1m.rstrip(',')
            raw_output['load_5m'] = load_5m.rstrip(',')
            raw_output['load_15m'] = load_15m

    return raw_output if raw else _process(raw_output)

```
===== 39 =====
```
             time, _, *uptime, _, _, load_1m, load_5m, load_15m = data.split()
 
             raw_output['time'] = time
-            raw_output['uptime'] = ' '.join(uptime).rstrip(',')
+            raw_output['UPTIME'] = ' '.join(uptime).rstrip(',')
             raw_output['load_1m'] = load_1m.rstrip(',')
             raw_output['load_5m'] = load_5m.rstrip(',')
             raw_output['load_15m'] = load_15m
 
-    return raw_output if raw else _process(raw_output)+    return raw_output if raw else _process(raw_output)
```
```
def parse(data, raw=False, quiet=False):
    """
    Main text parsing function

    Parameters:

        data:        (string)  text data to parse
        raw:         (boolean) unprocessed output if True
        quiet:       (boolean) suppress warning messages if True

    Returns:

        Dictionary. Raw or processed structured data
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)

    raw_output = {}

    if jc.utils.has_data(data):
        if 'user' in data:
            # standard uptime output
            time, _, *uptime, users, _, _, _, load_1m, load_5m, load_15m = data.split()

            raw_output['time'] = time
            raw_output['uptime'] = ' '.join(uptime).rstrip(',')
            raw_output['users'] = users
            raw_output['load_1m'] = load_1m.rstrip(',')
            raw_output['load_5m'] = load_5m.rstrip(',')
            raw_output['load_15m'] = load_15m

        else:
            # users information missing (e.g. busybox)
            time, _, *uptime, _, _, load_1m, load_5m, load_15m = data.split()

            raw_output['time'] = time
            raw_output['UPTIME'] = ' '.join(uptime).rstrip(',')
            raw_output['load_1m'] = load_1m.rstrip(',')
            raw_output['load_5m'] = load_5m.rstrip(',')
            raw_output['load_15m'] = load_15m

    return raw_output if raw else _process(raw_output)

```
===== 40 =====
```
             time, _, *uptime, _, _, load_1m, load_5m, load_15m = data.split()
 
             raw_output['time'] = time
-            raw_output['uptime'] = ' '.join(uptime).rstrip(',')
+            raw_output['XXuptimeXX'] = ' '.join(uptime).rstrip(',')
             raw_output['load_1m'] = load_1m.rstrip(',')
             raw_output['load_5m'] = load_5m.rstrip(',')
             raw_output['load_15m'] = load_15m
 
-    return raw_output if raw else _process(raw_output)+    return raw_output if raw else _process(raw_output)
```
```
def parse(data, raw=False, quiet=False):
    """
    Main text parsing function

    Parameters:

        data:        (string)  text data to parse
        raw:         (boolean) unprocessed output if True
        quiet:       (boolean) suppress warning messages if True

    Returns:

        Dictionary. Raw or processed structured data
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)

    raw_output = {}

    if jc.utils.has_data(data):
        if 'user' in data:
            # standard uptime output
            time, _, *uptime, users, _, _, _, load_1m, load_5m, load_15m = data.split()

            raw_output['time'] = time
            raw_output['uptime'] = ' '.join(uptime).rstrip(',')
            raw_output['users'] = users
            raw_output['load_1m'] = load_1m.rstrip(',')
            raw_output['load_5m'] = load_5m.rstrip(',')
            raw_output['load_15m'] = load_15m

        else:
            # users information missing (e.g. busybox)
            time, _, *uptime, _, _, load_1m, load_5m, load_15m = data.split()

            raw_output['time'] = time
            raw_output['XXuptimeXX'] = ' '.join(uptime).rstrip(',')
            raw_output['load_1m'] = load_1m.rstrip(',')
            raw_output['load_5m'] = load_5m.rstrip(',')
            raw_output['load_15m'] = load_15m

    return raw_output if raw else _process(raw_output)

```
===== 41 =====
```
             time, _, *uptime, _, _, load_1m, load_5m, load_15m = data.split()
 
             raw_output['time'] = time
-            raw_output['uptime'] = ' '.join(uptime).rstrip(',')
+            raw_output['uptime'] = ' '.join(uptime)  # Missing rstrip, may leave a trailing comma
             raw_output['load_1m'] = load_1m.rstrip(',')
             raw_output['load_5m'] = load_5m.rstrip(',')
             raw_output['load_15m'] = load_15m
```
```
def parse(data, raw=False, quiet=False):
    """
    Main text parsing function

    Parameters:

        data:        (string)  text data to parse
        raw:         (boolean) unprocessed output if True
        quiet:       (boolean) suppress warning messages if True

    Returns:

        Dictionary. Raw or processed structured data
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)

    raw_output = {}

    if jc.utils.has_data(data):
        if 'user' in data:
            # standard uptime output
            time, _, *uptime, users, _, _, _, load_1m, load_5m, load_15m = data.split()

            raw_output['time'] = time
            raw_output['uptime'] = ' '.join(uptime).rstrip(',')
            raw_output['users'] = users
            raw_output['load_1m'] = load_1m.rstrip(',')
            raw_output['load_5m'] = load_5m.rstrip(',')
            raw_output['load_15m'] = load_15m

        else:
            # users information missing (e.g. busybox)
            time, _, *uptime, _, _, load_1m, load_5m, load_15m = data.split()

            raw_output['time'] = time
            raw_output['uptime'] = ' '.join(uptime)  # Missing rstrip, may leave a trailing comma
            raw_output['load_1m'] = load_1m.rstrip(',')
            raw_output['load_5m'] = load_5m.rstrip(',')
            raw_output['load_15m'] = load_15m

    return raw_output if raw else _process(raw_output)
```
===== 42 =====
```
             time, _, *uptime, _, _, load_1m, load_5m, load_15m = data.split()
 
             raw_output['time'] = time
-            raw_output['uptime'] = ' '.join(uptime).rstrip(',')
+            raw_output['uptime'] = ' '.join(uptime).lstrip(',')
             raw_output['load_1m'] = load_1m.rstrip(',')
             raw_output['load_5m'] = load_5m.rstrip(',')
             raw_output['load_15m'] = load_15m
 
-    return raw_output if raw else _process(raw_output)+    return raw_output if raw else _process(raw_output)
```
```
def parse(data, raw=False, quiet=False):
    """
    Main text parsing function

    Parameters:

        data:        (string)  text data to parse
        raw:         (boolean) unprocessed output if True
        quiet:       (boolean) suppress warning messages if True

    Returns:

        Dictionary. Raw or processed structured data
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)

    raw_output = {}

    if jc.utils.has_data(data):
        if 'user' in data:
            # standard uptime output
            time, _, *uptime, users, _, _, _, load_1m, load_5m, load_15m = data.split()

            raw_output['time'] = time
            raw_output['uptime'] = ' '.join(uptime).rstrip(',')
            raw_output['users'] = users
            raw_output['load_1m'] = load_1m.rstrip(',')
            raw_output['load_5m'] = load_5m.rstrip(',')
            raw_output['load_15m'] = load_15m

        else:
            # users information missing (e.g. busybox)
            time, _, *uptime, _, _, load_1m, load_5m, load_15m = data.split()

            raw_output['time'] = time
            raw_output['uptime'] = ' '.join(uptime).lstrip(',')
            raw_output['load_1m'] = load_1m.rstrip(',')
            raw_output['load_5m'] = load_5m.rstrip(',')
            raw_output['load_15m'] = load_15m

    return raw_output if raw else _process(raw_output)

```
===== 43 =====
```
             time, _, *uptime, _, _, load_1m, load_5m, load_15m = data.split()
 
             raw_output['time'] = time
-            raw_output['uptime'] = ' '.join(uptime).rstrip(',')
+            raw_output['uptime'] = ' '.join(uptime).rstrip(None)
             raw_output['load_1m'] = load_1m.rstrip(',')
             raw_output['load_5m'] = load_5m.rstrip(',')
             raw_output['load_15m'] = load_15m
 
-    return raw_output if raw else _process(raw_output)+    return raw_output if raw else _process(raw_output)
```
```
def parse(data, raw=False, quiet=False):
    """
    Main text parsing function

    Parameters:

        data:        (string)  text data to parse
        raw:         (boolean) unprocessed output if True
        quiet:       (boolean) suppress warning messages if True

    Returns:

        Dictionary. Raw or processed structured data
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)

    raw_output = {}

    if jc.utils.has_data(data):
        if 'user' in data:
            # standard uptime output
            time, _, *uptime, users, _, _, _, load_1m, load_5m, load_15m = data.split()

            raw_output['time'] = time
            raw_output['uptime'] = ' '.join(uptime).rstrip(',')
            raw_output['users'] = users
            raw_output['load_1m'] = load_1m.rstrip(',')
            raw_output['load_5m'] = load_5m.rstrip(',')
            raw_output['load_15m'] = load_15m

        else:
            # users information missing (e.g. busybox)
            time, _, *uptime, _, _, load_1m, load_5m, load_15m = data.split()

            raw_output['time'] = time
            raw_output['uptime'] = ' '.join(uptime).rstrip(None)
            raw_output['load_1m'] = load_1m.rstrip(',')
            raw_output['load_5m'] = load_5m.rstrip(',')
            raw_output['load_15m'] = load_15m

    return raw_output if raw else _process(raw_output)

```
===== 44 =====
```
             time, _, *uptime, _, _, load_1m, load_5m, load_15m = data.split()
 
             raw_output['time'] = time
-            raw_output['uptime'] = ' '.join(uptime).rstrip(',')
+            raw_output['uptime'] = ' '.join(uptime).strip()  # Uses strip instead of rstrip, which may remove leading spaces
             raw_output['load_1m'] = load_1m.rstrip(',')
             raw_output['load_5m'] = load_5m.rstrip(',')
             raw_output['load_15m'] = load_15m
```
```
def parse(data, raw=False, quiet=False):
    """
    Main text parsing function

    Parameters:

        data:        (string)  text data to parse
        raw:         (boolean) unprocessed output if True
        quiet:       (boolean) suppress warning messages if True

    Returns:

        Dictionary. Raw or processed structured data
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)

    raw_output = {}

    if jc.utils.has_data(data):
        if 'user' in data:
            # standard uptime output
            time, _, *uptime, users, _, _, _, load_1m, load_5m, load_15m = data.split()

            raw_output['time'] = time
            raw_output['uptime'] = ' '.join(uptime).rstrip(',')
            raw_output['users'] = users
            raw_output['load_1m'] = load_1m.rstrip(',')
            raw_output['load_5m'] = load_5m.rstrip(',')
            raw_output['load_15m'] = load_15m

        else:
            # users information missing (e.g. busybox)
            time, _, *uptime, _, _, load_1m, load_5m, load_15m = data.split()

            raw_output['time'] = time
            raw_output['uptime'] = ' '.join(uptime).strip()  # Uses strip instead of rstrip, which may remove leading spaces
            raw_output['load_1m'] = load_1m.rstrip(',')
            raw_output['load_5m'] = load_5m.rstrip(',')
            raw_output['load_15m'] = load_15m

    return raw_output if raw else _process(raw_output)
```
===== 45 =====
```
             time, _, *uptime, _, _, load_1m, load_5m, load_15m = data.split()
 
             raw_output['time'] = time
-            raw_output['uptime'] = ' '.join(uptime).rstrip(',')
+            raw_output['uptime'] = 'XX XX'.join(uptime).rstrip(',')
             raw_output['load_1m'] = load_1m.rstrip(',')
             raw_output['load_5m'] = load_5m.rstrip(',')
             raw_output['load_15m'] = load_15m
 
-    return raw_output if raw else _process(raw_output)+    return raw_output if raw else _process(raw_output)
```
```
def parse(data, raw=False, quiet=False):
    """
    Main text parsing function

    Parameters:

        data:        (string)  text data to parse
        raw:         (boolean) unprocessed output if True
        quiet:       (boolean) suppress warning messages if True

    Returns:

        Dictionary. Raw or processed structured data
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)

    raw_output = {}

    if jc.utils.has_data(data):
        if 'user' in data:
            # standard uptime output
            time, _, *uptime, users, _, _, _, load_1m, load_5m, load_15m = data.split()

            raw_output['time'] = time
            raw_output['uptime'] = ' '.join(uptime).rstrip(',')
            raw_output['users'] = users
            raw_output['load_1m'] = load_1m.rstrip(',')
            raw_output['load_5m'] = load_5m.rstrip(',')
            raw_output['load_15m'] = load_15m

        else:
            # users information missing (e.g. busybox)
            time, _, *uptime, _, _, load_1m, load_5m, load_15m = data.split()

            raw_output['time'] = time
            raw_output['uptime'] = 'XX XX'.join(uptime).rstrip(',')
            raw_output['load_1m'] = load_1m.rstrip(',')
            raw_output['load_5m'] = load_5m.rstrip(',')
            raw_output['load_15m'] = load_15m

    return raw_output if raw else _process(raw_output)

```
===== 46 =====
```
             time, _, *uptime, _, _, load_1m, load_5m, load_15m = data.split()
 
             raw_output['time'] = time
-            raw_output['uptime'] = ' '.join(uptime).rstrip(',')
+            raw_output['uptime'] = uptime[0]  # Only assigns the first element, losing the rest of the uptime information
             raw_output['load_1m'] = load_1m.rstrip(',')
             raw_output['load_5m'] = load_5m.rstrip(',')
             raw_output['load_15m'] = load_15m
```
```
def parse(data, raw=False, quiet=False):
    """
    Main text parsing function

    Parameters:

        data:        (string)  text data to parse
        raw:         (boolean) unprocessed output if True
        quiet:       (boolean) suppress warning messages if True

    Returns:

        Dictionary. Raw or processed structured data
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)

    raw_output = {}

    if jc.utils.has_data(data):
        if 'user' in data:
            # standard uptime output
            time, _, *uptime, users, _, _, _, load_1m, load_5m, load_15m = data.split()

            raw_output['time'] = time
            raw_output['uptime'] = ' '.join(uptime).rstrip(',')
            raw_output['users'] = users
            raw_output['load_1m'] = load_1m.rstrip(',')
            raw_output['load_5m'] = load_5m.rstrip(',')
            raw_output['load_15m'] = load_15m

        else:
            # users information missing (e.g. busybox)
            time, _, *uptime, _, _, load_1m, load_5m, load_15m = data.split()

            raw_output['time'] = time
            raw_output['uptime'] = uptime[0]  # Only assigns the first element, losing the rest of the uptime information
            raw_output['load_1m'] = load_1m.rstrip(',')
            raw_output['load_5m'] = load_5m.rstrip(',')
            raw_output['load_15m'] = load_15m

    return raw_output if raw else _process(raw_output)
```
===== 47 =====
```
 
             raw_output['time'] = time
             raw_output['uptime'] = ' '.join(uptime).rstrip(',')
-            raw_output['load_1m'] = load_1m.rstrip(',')
+            raw_output['LOAD_1M'] = load_1m.rstrip(',')
             raw_output['load_5m'] = load_5m.rstrip(',')
             raw_output['load_15m'] = load_15m
 
-    return raw_output if raw else _process(raw_output)+    return raw_output if raw else _process(raw_output)
```
```
def parse(data, raw=False, quiet=False):
    """
    Main text parsing function

    Parameters:

        data:        (string)  text data to parse
        raw:         (boolean) unprocessed output if True
        quiet:       (boolean) suppress warning messages if True

    Returns:

        Dictionary. Raw or processed structured data
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)

    raw_output = {}

    if jc.utils.has_data(data):
        if 'user' in data:
            # standard uptime output
            time, _, *uptime, users, _, _, _, load_1m, load_5m, load_15m = data.split()

            raw_output['time'] = time
            raw_output['uptime'] = ' '.join(uptime).rstrip(',')
            raw_output['users'] = users
            raw_output['load_1m'] = load_1m.rstrip(',')
            raw_output['load_5m'] = load_5m.rstrip(',')
            raw_output['load_15m'] = load_15m

        else:
            # users information missing (e.g. busybox)
            time, _, *uptime, _, _, load_1m, load_5m, load_15m = data.split()

            raw_output['time'] = time
            raw_output['uptime'] = ' '.join(uptime).rstrip(',')
            raw_output['LOAD_1M'] = load_1m.rstrip(',')
            raw_output['load_5m'] = load_5m.rstrip(',')
            raw_output['load_15m'] = load_15m

    return raw_output if raw else _process(raw_output)

```
===== 48 =====
```
 
             raw_output['time'] = time
             raw_output['uptime'] = ' '.join(uptime).rstrip(',')
-            raw_output['load_1m'] = load_1m.rstrip(',')
+            raw_output['XXload_1mXX'] = load_1m.rstrip(',')
             raw_output['load_5m'] = load_5m.rstrip(',')
             raw_output['load_15m'] = load_15m
 
-    return raw_output if raw else _process(raw_output)+    return raw_output if raw else _process(raw_output)
```
```
def parse(data, raw=False, quiet=False):
    """
    Main text parsing function

    Parameters:

        data:        (string)  text data to parse
        raw:         (boolean) unprocessed output if True
        quiet:       (boolean) suppress warning messages if True

    Returns:

        Dictionary. Raw or processed structured data
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)

    raw_output = {}

    if jc.utils.has_data(data):
        if 'user' in data:
            # standard uptime output
            time, _, *uptime, users, _, _, _, load_1m, load_5m, load_15m = data.split()

            raw_output['time'] = time
            raw_output['uptime'] = ' '.join(uptime).rstrip(',')
            raw_output['users'] = users
            raw_output['load_1m'] = load_1m.rstrip(',')
            raw_output['load_5m'] = load_5m.rstrip(',')
            raw_output['load_15m'] = load_15m

        else:
            # users information missing (e.g. busybox)
            time, _, *uptime, _, _, load_1m, load_5m, load_15m = data.split()

            raw_output['time'] = time
            raw_output['uptime'] = ' '.join(uptime).rstrip(',')
            raw_output['XXload_1mXX'] = load_1m.rstrip(',')
            raw_output['load_5m'] = load_5m.rstrip(',')
            raw_output['load_15m'] = load_15m

    return raw_output if raw else _process(raw_output)

```
===== 49 =====
```
 
             raw_output['time'] = time
             raw_output['uptime'] = ' '.join(uptime).rstrip(',')
-            raw_output['load_1m'] = load_1m.rstrip(',')
+            raw_output['load_1m'] = None
             raw_output['load_5m'] = load_5m.rstrip(',')
             raw_output['load_15m'] = load_15m
 
-    return raw_output if raw else _process(raw_output)+    return raw_output if raw else _process(raw_output)
```
```
def parse(data, raw=False, quiet=False):
    """
    Main text parsing function

    Parameters:

        data:        (string)  text data to parse
        raw:         (boolean) unprocessed output if True
        quiet:       (boolean) suppress warning messages if True

    Returns:

        Dictionary. Raw or processed structured data
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)

    raw_output = {}

    if jc.utils.has_data(data):
        if 'user' in data:
            # standard uptime output
            time, _, *uptime, users, _, _, _, load_1m, load_5m, load_15m = data.split()

            raw_output['time'] = time
            raw_output['uptime'] = ' '.join(uptime).rstrip(',')
            raw_output['users'] = users
            raw_output['load_1m'] = load_1m.rstrip(',')
            raw_output['load_5m'] = load_5m.rstrip(',')
            raw_output['load_15m'] = load_15m

        else:
            # users information missing (e.g. busybox)
            time, _, *uptime, _, _, load_1m, load_5m, load_15m = data.split()

            raw_output['time'] = time
            raw_output['uptime'] = ' '.join(uptime).rstrip(',')
            raw_output['load_1m'] = None
            raw_output['load_5m'] = load_5m.rstrip(',')
            raw_output['load_15m'] = load_15m

    return raw_output if raw else _process(raw_output)

```
===== 50 =====
```
 
             raw_output['time'] = time
             raw_output['uptime'] = ' '.join(uptime).rstrip(',')
-            raw_output['load_1m'] = load_1m.rstrip(',')
+            raw_output['load_1m'] = None  # Assigning None instead of the actual value
             raw_output['load_5m'] = load_5m.rstrip(',')
             raw_output['load_15m'] = load_15m
```
```
def parse(data, raw=False, quiet=False):
    """
    Main text parsing function

    Parameters:

        data:        (string)  text data to parse
        raw:         (boolean) unprocessed output if True
        quiet:       (boolean) suppress warning messages if True

    Returns:

        Dictionary. Raw or processed structured data
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)

    raw_output = {}

    if jc.utils.has_data(data):
        if 'user' in data:
            # standard uptime output
            time, _, *uptime, users, _, _, _, load_1m, load_5m, load_15m = data.split()

            raw_output['time'] = time
            raw_output['uptime'] = ' '.join(uptime).rstrip(',')
            raw_output['users'] = users
            raw_output['load_1m'] = load_1m.rstrip(',')
            raw_output['load_5m'] = load_5m.rstrip(',')
            raw_output['load_15m'] = load_15m

        else:
            # users information missing (e.g. busybox)
            time, _, *uptime, _, _, load_1m, load_5m, load_15m = data.split()

            raw_output['time'] = time
            raw_output['uptime'] = ' '.join(uptime).rstrip(',')
            raw_output['load_1m'] = None  # Assigning None instead of the actual value
            raw_output['load_5m'] = load_5m.rstrip(',')
            raw_output['load_15m'] = load_15m

    return raw_output if raw else _process(raw_output)
```
===== 51 =====
```
             raw_output['time'] = time
             raw_output['uptime'] = ' '.join(uptime).rstrip(',')
             raw_output['load_1m'] = load_1m.rstrip(',')
-            raw_output['load_5m'] = load_5m.rstrip(',')
+            raw_output['LOAD_5M'] = load_5m.rstrip(',')
             raw_output['load_15m'] = load_15m
 
-    return raw_output if raw else _process(raw_output)+    return raw_output if raw else _process(raw_output)
```
```
def parse(data, raw=False, quiet=False):
    """
    Main text parsing function

    Parameters:

        data:        (string)  text data to parse
        raw:         (boolean) unprocessed output if True
        quiet:       (boolean) suppress warning messages if True

    Returns:

        Dictionary. Raw or processed structured data
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)

    raw_output = {}

    if jc.utils.has_data(data):
        if 'user' in data:
            # standard uptime output
            time, _, *uptime, users, _, _, _, load_1m, load_5m, load_15m = data.split()

            raw_output['time'] = time
            raw_output['uptime'] = ' '.join(uptime).rstrip(',')
            raw_output['users'] = users
            raw_output['load_1m'] = load_1m.rstrip(',')
            raw_output['load_5m'] = load_5m.rstrip(',')
            raw_output['load_15m'] = load_15m

        else:
            # users information missing (e.g. busybox)
            time, _, *uptime, _, _, load_1m, load_5m, load_15m = data.split()

            raw_output['time'] = time
            raw_output['uptime'] = ' '.join(uptime).rstrip(',')
            raw_output['load_1m'] = load_1m.rstrip(',')
            raw_output['LOAD_5M'] = load_5m.rstrip(',')
            raw_output['load_15m'] = load_15m

    return raw_output if raw else _process(raw_output)

```
===== 52 =====
```
             raw_output['time'] = time
             raw_output['uptime'] = ' '.join(uptime).rstrip(',')
             raw_output['load_1m'] = load_1m.rstrip(',')
-            raw_output['load_5m'] = load_5m.rstrip(',')
+            raw_output['XXload_5mXX'] = load_5m.rstrip(',')
             raw_output['load_15m'] = load_15m
 
-    return raw_output if raw else _process(raw_output)+    return raw_output if raw else _process(raw_output)
```
```
def parse(data, raw=False, quiet=False):
    """
    Main text parsing function

    Parameters:

        data:        (string)  text data to parse
        raw:         (boolean) unprocessed output if True
        quiet:       (boolean) suppress warning messages if True

    Returns:

        Dictionary. Raw or processed structured data
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)

    raw_output = {}

    if jc.utils.has_data(data):
        if 'user' in data:
            # standard uptime output
            time, _, *uptime, users, _, _, _, load_1m, load_5m, load_15m = data.split()

            raw_output['time'] = time
            raw_output['uptime'] = ' '.join(uptime).rstrip(',')
            raw_output['users'] = users
            raw_output['load_1m'] = load_1m.rstrip(',')
            raw_output['load_5m'] = load_5m.rstrip(',')
            raw_output['load_15m'] = load_15m

        else:
            # users information missing (e.g. busybox)
            time, _, *uptime, _, _, load_1m, load_5m, load_15m = data.split()

            raw_output['time'] = time
            raw_output['uptime'] = ' '.join(uptime).rstrip(',')
            raw_output['load_1m'] = load_1m.rstrip(',')
            raw_output['XXload_5mXX'] = load_5m.rstrip(',')
            raw_output['load_15m'] = load_15m

    return raw_output if raw else _process(raw_output)

```
===== 53 =====
```
             raw_output['time'] = time
             raw_output['uptime'] = ' '.join(uptime).rstrip(',')
             raw_output['load_1m'] = load_1m.rstrip(',')
-            raw_output['load_5m'] = load_5m.rstrip(',')
+            raw_output['load_5m'] = None
             raw_output['load_15m'] = load_15m
 
     return raw_output if raw else _process(raw_output)
```
```
def parse(data, raw=False, quiet=False):
    """
    Main text parsing function

    Parameters:

        data:        (string)  text data to parse
        raw:         (boolean) unprocessed output if True
        quiet:       (boolean) suppress warning messages if True

    Returns:

        Dictionary. Raw or processed structured data
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)

    raw_output = {}

    if jc.utils.has_data(data):
        if 'user' in data:
            # standard uptime output
            time, _, *uptime, users, _, _, _, load_1m, load_5m, load_15m = data.split()

            raw_output['time'] = time
            raw_output['uptime'] = ' '.join(uptime).rstrip(',')
            raw_output['users'] = users
            raw_output['load_1m'] = load_1m.rstrip(',')
            raw_output['load_5m'] = load_5m.rstrip(',')
            raw_output['load_15m'] = load_15m

        else:
            # users information missing (e.g. busybox)
            time, _, *uptime, _, _, load_1m, load_5m, load_15m = data.split()

            raw_output['time'] = time
            raw_output['uptime'] = ' '.join(uptime).rstrip(',')
            raw_output['load_1m'] = load_1m.rstrip(',')
            raw_output['load_5m'] = None
            raw_output['load_15m'] = load_15m

    return raw_output if raw else _process(raw_output)
```
===== 54 =====
```
             raw_output['time'] = time
             raw_output['uptime'] = ' '.join(uptime).rstrip(',')
             raw_output['load_1m'] = load_1m.rstrip(',')
-            raw_output['load_5m'] = load_5m.rstrip(',')
+            raw_output['load_5m'] = None
             raw_output['load_15m'] = load_15m
 
-    return raw_output if raw else _process(raw_output)+    return raw_output if raw else _process(raw_output)
```
```
def parse(data, raw=False, quiet=False):
    """
    Main text parsing function

    Parameters:

        data:        (string)  text data to parse
        raw:         (boolean) unprocessed output if True
        quiet:       (boolean) suppress warning messages if True

    Returns:

        Dictionary. Raw or processed structured data
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)

    raw_output = {}

    if jc.utils.has_data(data):
        if 'user' in data:
            # standard uptime output
            time, _, *uptime, users, _, _, _, load_1m, load_5m, load_15m = data.split()

            raw_output['time'] = time
            raw_output['uptime'] = ' '.join(uptime).rstrip(',')
            raw_output['users'] = users
            raw_output['load_1m'] = load_1m.rstrip(',')
            raw_output['load_5m'] = load_5m.rstrip(',')
            raw_output['load_15m'] = load_15m

        else:
            # users information missing (e.g. busybox)
            time, _, *uptime, _, _, load_1m, load_5m, load_15m = data.split()

            raw_output['time'] = time
            raw_output['uptime'] = ' '.join(uptime).rstrip(',')
            raw_output['load_1m'] = load_1m.rstrip(',')
            raw_output['load_5m'] = None
            raw_output['load_15m'] = load_15m

    return raw_output if raw else _process(raw_output)

```
===== 55 =====
```
             raw_output['uptime'] = ' '.join(uptime).rstrip(',')
             raw_output['load_1m'] = load_1m.rstrip(',')
             raw_output['load_5m'] = load_5m.rstrip(',')
-            raw_output['load_15m'] = load_15m
+            raw_output['LOAD_15M'] = load_15m
 
-    return raw_output if raw else _process(raw_output)+    return raw_output if raw else _process(raw_output)
```
```
def parse(data, raw=False, quiet=False):
    """
    Main text parsing function

    Parameters:

        data:        (string)  text data to parse
        raw:         (boolean) unprocessed output if True
        quiet:       (boolean) suppress warning messages if True

    Returns:

        Dictionary. Raw or processed structured data
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)

    raw_output = {}

    if jc.utils.has_data(data):
        if 'user' in data:
            # standard uptime output
            time, _, *uptime, users, _, _, _, load_1m, load_5m, load_15m = data.split()

            raw_output['time'] = time
            raw_output['uptime'] = ' '.join(uptime).rstrip(',')
            raw_output['users'] = users
            raw_output['load_1m'] = load_1m.rstrip(',')
            raw_output['load_5m'] = load_5m.rstrip(',')
            raw_output['load_15m'] = load_15m

        else:
            # users information missing (e.g. busybox)
            time, _, *uptime, _, _, load_1m, load_5m, load_15m = data.split()

            raw_output['time'] = time
            raw_output['uptime'] = ' '.join(uptime).rstrip(',')
            raw_output['load_1m'] = load_1m.rstrip(',')
            raw_output['load_5m'] = load_5m.rstrip(',')
            raw_output['LOAD_15M'] = load_15m

    return raw_output if raw else _process(raw_output)

```
===== 56 =====
```
             raw_output['uptime'] = ' '.join(uptime).rstrip(',')
             raw_output['load_1m'] = load_1m.rstrip(',')
             raw_output['load_5m'] = load_5m.rstrip(',')
-            raw_output['load_15m'] = load_15m
+            raw_output['XXload_15mXX'] = load_15m
 
-    return raw_output if raw else _process(raw_output)+    return raw_output if raw else _process(raw_output)
```
```
def parse(data, raw=False, quiet=False):
    """
    Main text parsing function

    Parameters:

        data:        (string)  text data to parse
        raw:         (boolean) unprocessed output if True
        quiet:       (boolean) suppress warning messages if True

    Returns:

        Dictionary. Raw or processed structured data
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)

    raw_output = {}

    if jc.utils.has_data(data):
        if 'user' in data:
            # standard uptime output
            time, _, *uptime, users, _, _, _, load_1m, load_5m, load_15m = data.split()

            raw_output['time'] = time
            raw_output['uptime'] = ' '.join(uptime).rstrip(',')
            raw_output['users'] = users
            raw_output['load_1m'] = load_1m.rstrip(',')
            raw_output['load_5m'] = load_5m.rstrip(',')
            raw_output['load_15m'] = load_15m

        else:
            # users information missing (e.g. busybox)
            time, _, *uptime, _, _, load_1m, load_5m, load_15m = data.split()

            raw_output['time'] = time
            raw_output['uptime'] = ' '.join(uptime).rstrip(',')
            raw_output['load_1m'] = load_1m.rstrip(',')
            raw_output['load_5m'] = load_5m.rstrip(',')
            raw_output['XXload_15mXX'] = load_15m

    return raw_output if raw else _process(raw_output)

```
===== 57 =====
```
             raw_output['uptime'] = ' '.join(uptime).rstrip(',')
             raw_output['load_1m'] = load_1m.rstrip(',')
             raw_output['load_5m'] = load_5m.rstrip(',')
-            raw_output['load_15m'] = load_15m
+            raw_output['load_15m'] = None
 
-    return raw_output if raw else _process(raw_output)+    return raw_output if raw else _process(raw_output)
```
```
def parse(data, raw=False, quiet=False):
    """
    Main text parsing function

    Parameters:

        data:        (string)  text data to parse
        raw:         (boolean) unprocessed output if True
        quiet:       (boolean) suppress warning messages if True

    Returns:

        Dictionary. Raw or processed structured data
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)

    raw_output = {}

    if jc.utils.has_data(data):
        if 'user' in data:
            # standard uptime output
            time, _, *uptime, users, _, _, _, load_1m, load_5m, load_15m = data.split()

            raw_output['time'] = time
            raw_output['uptime'] = ' '.join(uptime).rstrip(',')
            raw_output['users'] = users
            raw_output['load_1m'] = load_1m.rstrip(',')
            raw_output['load_5m'] = load_5m.rstrip(',')
            raw_output['load_15m'] = load_15m

        else:
            # users information missing (e.g. busybox)
            time, _, *uptime, _, _, load_1m, load_5m, load_15m = data.split()

            raw_output['time'] = time
            raw_output['uptime'] = ' '.join(uptime).rstrip(',')
            raw_output['load_1m'] = load_1m.rstrip(',')
            raw_output['load_5m'] = load_5m.rstrip(',')
            raw_output['load_15m'] = None

    return raw_output if raw else _process(raw_output)

```
===== 60 =====
```
             raw_output['load_5m'] = load_5m.rstrip(',')
             raw_output['load_15m'] = load_15m
 
-    return raw_output if raw else _process(raw_output)+    return raw_output if raw else None
```
```
def parse(data, raw=False, quiet=False):
    """
    Main text parsing function

    Parameters:

        data:        (string)  text data to parse
        raw:         (boolean) unprocessed output if True
        quiet:       (boolean) suppress warning messages if True

    Returns:

        Dictionary. Raw or processed structured data
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)

    raw_output = {}

    if jc.utils.has_data(data):
        if 'user' in data:
            # standard uptime output
            time, _, *uptime, users, _, _, _, load_1m, load_5m, load_15m = data.split()

            raw_output['time'] = time
            raw_output['uptime'] = ' '.join(uptime).rstrip(',')
            raw_output['users'] = users
            raw_output['load_1m'] = load_1m.rstrip(',')
            raw_output['load_5m'] = load_5m.rstrip(',')
            raw_output['load_15m'] = load_15m

        else:
            # users information missing (e.g. busybox)
            time, _, *uptime, _, _, load_1m, load_5m, load_15m = data.split()

            raw_output['time'] = time
            raw_output['uptime'] = ' '.join(uptime).rstrip(',')
            raw_output['load_1m'] = load_1m.rstrip(',')
            raw_output['load_5m'] = load_5m.rstrip(',')
            raw_output['load_15m'] = load_15m

    return raw_output if raw else None
```
