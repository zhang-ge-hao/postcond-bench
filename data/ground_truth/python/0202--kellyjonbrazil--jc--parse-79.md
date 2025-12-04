https://github.com/kellyjonbrazil/jc/blob/9fd13e698709da95f5ee505ff1fde10564544d48/./jc/parsers/lsattr.py#L110-L162
```
@icontract.snapshot(lambda data: list(filter(None, data.splitlines())), name="cleandata")
@icontract.snapshot(lambda data: [line for line in list(filter(None, data.splitlines())) if not line.endswith(':') and not line.startswith(ERROR_PREFIX)], name="processable")
@icontract.snapshot(lambda data: ATTRIBUTES, name="ATTRIBUTES")
@icontract.ensure(
    lambda result, data, OLD: 
        (
            (not jc.utils.has_data(data) and result == []) or (jc.utils.has_data(data) and len(result) == len(OLD.processable))
        ) and 
        all(isinstance(r, dict) for r in result)
        and
        all(isinstance(k, str) for r in result for k in r.keys())
        and
        all(isinstance(r.get('file'), str) and r.get('file') == p.split()[-1] for r, p in zip(result, OLD.processable))
        and
        all(all((r.get(OLD.ATTRIBUTES.get(c)) is True) if OLD.ATTRIBUTES.get(c) else True for c in p.split()[0]) for r, p in zip(result, OLD.processable))
)
```
```
@icontract.snapshot(lambda data: list(filter(None, data.splitlines())), name="cleandata")
@icontract.snapshot(lambda data: [line for line in list(filter(None, data.splitlines())) if not line.endswith(':') and not line.startswith(ERROR_PREFIX)], name="processable")
@icontract.snapshot(lambda data: ATTRIBUTES, name="ATTRIBUTES")
@icontract.ensure(lambda result, data, OLD: (not jc.utils.has_data(data) and result == []) or (jc.utils.has_data(data) and len(result) == len(OLD.processable)))
@icontract.ensure(lambda result, OLD: all(isinstance(r, dict) for r in result))
@icontract.ensure(lambda result, OLD: all(isinstance(k, str) for r in result for k in r.keys()))
@icontract.ensure(lambda result, OLD: all(isinstance(r.get('file'), str) and r.get('file') == p.split()[-1] for r, p in zip(result, OLD.processable)))
@icontract.ensure(lambda result, OLD: all(all((r.get(OLD.ATTRIBUTES.get(c)) is True) if OLD.ATTRIBUTES.get(c) else True for c in p.split()[0]) for r, p in zip(result, OLD.processable)))
```
[24]
===== 24 =====
```
                 line_output[attribute_key] = True
 
         if line_output:
-            output.append(line_output)
+            output.append(None)
 
-    return output+    return output
```
```
def parse(
    data: str,
    raw: bool = False,
    quiet: bool = False
) -> List[JSONDictType]:
    """
    Main text parsing function

    Parameters:

        data:        (string)  text data to parse
        quiet:       (boolean) suppress warning messages if True

    Returns:

        List of Dictionaries. Raw or processed structured data.
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)

    output: List = []

    cleandata = list(filter(None, data.splitlines()))

    if not jc.utils.has_data(data):
        return output

    for line in cleandata:
        # -R flag returns the output in the format:
        # Folder:
        #   attributes file_in_folder
        if line.endswith(':'):
            continue

        # lsattr: Operation not supported ....
        if line.startswith(ERROR_PREFIX):
            continue

        line_output: Dict = {}

        # attributes file
        # --------------e----- /etc/passwd
        attributes, file = line.split()
        line_output['file'] = file
        for attribute in list(attributes):
            attribute_key = ATTRIBUTES.get(attribute)
            if attribute_key:
                line_output[attribute_key] = True

        if line_output:
            output.append(None)

    return output

```
