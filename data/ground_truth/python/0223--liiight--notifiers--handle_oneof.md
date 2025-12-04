https://github.com/liiight/notifiers/blob/351c048eb1d8fefae7d638cf1ac667a69815c79a/./notifiers_cli/utils/dynamic_click.py#L25-L47
```
@icontract.snapshot(lambda oneof_schema: (lambda l: [x for i,x in enumerate(l) if x not in l[:i]])([s["type"] for s in oneof_schema]), name="unique_types")
@icontract.snapshot(lambda oneof_schema: [t for t in (lambda l: [x for i,x in enumerate(l) if x not in l[:i]])([s["type"] for s in oneof_schema]) if t in SCHEMA_BASE_MAP], name="primitives_order")
@icontract.snapshot(lambda oneof_schema: next((s.get("items", {}).get("type") for s in oneof_schema if s.get("type") == "array" and isinstance(s.get("items"), dict) and "type" in s.get("items")), None), name="array_items_type")
@icontract.snapshot(lambda oneof_schema: {s["type"]: s.get("title") for s in oneof_schema}, name="type_to_title")
@icontract.ensure(
    lambda result, OLD: 
        isinstance(result, tuple) and len(result) == 3
        and
        (result[0] is None or result[0] in set(SCHEMA_BASE_MAP.values()))
        and
        (not OLD.primitives_order) == (result[0] is None and result[1] is False and result[2] is None)
        and
        ((not OLD.primitives_order) or (result[0] == SCHEMA_BASE_MAP[OLD.primitives_order[0]]))
        and
        ((not OLD.primitives_order) or (result[2] == OLD.type_to_title.get(OLD.primitives_order[0])))
        and
        ((not OLD.primitives_order) or (result[1] is (OLD.array_items_type == OLD.primitives_order[0])))
)
```
```
@icontract.snapshot(lambda oneof_schema: (lambda l: [x for i,x in enumerate(l) if x not in l[:i]])([s["type"] for s in oneof_schema]), name="unique_types")
@icontract.snapshot(lambda oneof_schema: [t for t in (lambda l: [x for i,x in enumerate(l) if x not in l[:i]])([s["type"] for s in oneof_schema]) if t in SCHEMA_BASE_MAP], name="primitives_order")
@icontract.snapshot(lambda oneof_schema: next((s.get("items", {}).get("type") for s in oneof_schema if s.get("type") == "array" and isinstance(s.get("items"), dict) and "type" in s.get("items")), None), name="array_items_type")
@icontract.snapshot(lambda oneof_schema: {s["type"]: s.get("title") for s in oneof_schema}, name="type_to_title")
@icontract.ensure(lambda result, OLD: isinstance(result, tuple) and len(result) == 3)
@icontract.ensure(lambda result, OLD: result[0] is None or result[0] in set(SCHEMA_BASE_MAP.values()))
@icontract.ensure(lambda result, OLD: (not OLD.primitives_order) == (result[0] is None and result[1] is False and result[2] is None))
@icontract.ensure(lambda result, OLD: (not OLD.primitives_order) or (result[0] == SCHEMA_BASE_MAP[OLD.primitives_order[0]]))
@icontract.ensure(lambda result, OLD: (not OLD.primitives_order) or (result[2] == OLD.type_to_title.get(OLD.primitives_order[0])))
@icontract.ensure(lambda result, OLD: (not OLD.primitives_order) or (result[1] is (OLD.array_items_type == OLD.primitives_order[0])))
```
[10]
===== 10 =====
```
             # Found a match to a primitive type
             click_type = SCHEMA_BASE_MAP[key]
             description = value.get("title")
-            break
-    return click_type, multiple, description+            return
+    return click_type, multiple, description
```
```
def handle_oneof(oneof_schema: list) -> tuple:
    """
    Custom handle of `oneOf` JSON schema validator. Tried to match primitive type and see if it should be allowed
     to be passed multiple timns into a command

    :param oneof_schema: `oneOf` JSON schema
    :return: Tuple of :class:`click.ParamType`, ``multiple`` flag and ``description`` of option
    """
    oneof_dict = {schema["type"]: schema for schema in oneof_schema}
    click_type = None
    multiple = False
    description = None
    for key, value in oneof_dict.items():
        if key == "array":
            continue
        if key in SCHEMA_BASE_MAP:
            if oneof_dict.get("array") and oneof_dict["array"]["items"]["type"] == key:
                multiple = True
            # Found a match to a primitive type
            click_type = SCHEMA_BASE_MAP[key]
            description = value.get("title")
            return
    return click_type, multiple, description

```
