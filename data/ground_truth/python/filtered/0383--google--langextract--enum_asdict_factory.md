https://github.com/google/langextract/blob/6e36c378994121c2b8d9a25b32cff149d9bfc61c/./langextract/data_lib.py#L27-L54
```
🈚️

Iterator
```
```
@icontract.snapshot(lambda items: list(items))
@icontract.ensure(lambda OLD, result: set(result.keys()) == {k for k, _ in OLD.items if not k.startswith("_")})
@icontract.ensure(lambda OLD, result: all((not dataclasses.is_dataclass(v)) or result[k] == dataclasses.asdict(v, dict_factory=enum_asdict_factory) for k, v in OLD.items if not k.startswith("_")))
@icontract.ensure(lambda OLD, result: all((not isinstance(v, enum.Enum)) or result[k] == v.value for k, v in OLD.items if not k.startswith("_")))
@icontract.ensure(lambda OLD, result: all((not (isinstance(v, numbers.Integral) and not isinstance(v, bool))) or (isinstance(result[k], int) and result[k] == int(v)) for k, v in OLD.items if not k.startswith("_")))
@icontract.ensure(lambda OLD, result: all((dataclasses.is_dataclass(v) or isinstance(v, enum.Enum) or (isinstance(v, numbers.Integral) and not isinstance(v, bool))) or result[k] == v for k, v in OLD.items if not k.startswith("_")))
```
[0, 1, 2]
===== 0 =====
```
   """
   result: dict[str, Any] = {}
   for key, value in items:
-    # Skip internal fields.
+    if isinstance(value, list):
+      continue
     if key.startswith("_"):
       continue
     if dataclasses.is_dataclass(value):
```
```
def enum_asdict_factory(items: Iterable[tuple[str, Any]]) -> dict[str, Any]:
  """Custom dict_factory for dataclasses.asdict.

  Recursively converts dataclass instances, converts enum values to their
  underlying values, converts integral numeric types to int, and skips any
  field whose name starts with an underscore.

  Args:
    items: An iterable of (key, value) pairs from fields of a dataclass.

  Returns:
    A mapping of field names to their values, with special handling for
    dataclasses, enums, and numeric types.
  """
  result: dict[str, Any] = {}
  for key, value in items:
    if isinstance(value, list):
      continue
    if key.startswith("_"):
      continue
    if dataclasses.is_dataclass(value):
      result[key] = dataclasses.asdict(value, dict_factory=enum_asdict_factory)
    elif isinstance(value, enum.Enum):
      result[key] = value.value
    elif isinstance(value, numbers.Integral) and not isinstance(value, bool):
      result[key] = int(value)
    else:
      result[key] = value
  return result
```
===== 1 =====
```
   """
   result: dict[str, Any] = {}
   for key, value in items:
-    # Skip internal fields.
+    if isinstance(value, str):
+      continue
     if key.startswith("_"):
       continue
     if dataclasses.is_dataclass(value):
```
```
def enum_asdict_factory(items: Iterable[tuple[str, Any]]) -> dict[str, Any]:
  """Custom dict_factory for dataclasses.asdict.

  Recursively converts dataclass instances, converts enum values to their
  underlying values, converts integral numeric types to int, and skips any
  field whose name starts with an underscore.

  Args:
    items: An iterable of (key, value) pairs from fields of a dataclass.

  Returns:
    A mapping of field names to their values, with special handling for
    dataclasses, enums, and numeric types.
  """
  result: dict[str, Any] = {}
  for key, value in items:
    if isinstance(value, str):
      continue
    if key.startswith("_"):
      continue
    if dataclasses.is_dataclass(value):
      result[key] = dataclasses.asdict(value, dict_factory=enum_asdict_factory)
    elif isinstance(value, enum.Enum):
      result[key] = value.value
    elif isinstance(value, numbers.Integral) and not isinstance(value, bool):
      result[key] = int(value)
    else:
      result[key] = value
  return result
```
===== 2 =====
```
   """
   result: dict[str, Any] = {}
   for key, value in items:
-    # Skip internal fields.
+    if key in ["extractions", "text"]:
+      continue
     if key.startswith("_"):
       continue
     if dataclasses.is_dataclass(value):
```
```
def enum_asdict_factory(items: Iterable[tuple[str, Any]]) -> dict[str, Any]:
  """Custom dict_factory for dataclasses.asdict.

  Recursively converts dataclass instances, converts enum values to their
  underlying values, converts integral numeric types to int, and skips any
  field whose name starts with an underscore.

  Args:
    items: An iterable of (key, value) pairs from fields of a dataclass.

  Returns:
    A mapping of field names to their values, with special handling for
    dataclasses, enums, and numeric types.
  """
  result: dict[str, Any] = {}
  for key, value in items:
    if key in ["extractions", "text"]:
      continue
    if key.startswith("_"):
      continue
    if dataclasses.is_dataclass(value):
      result[key] = dataclasses.asdict(value, dict_factory=enum_asdict_factory)
    elif isinstance(value, enum.Enum):
      result[key] = value.value
    elif isinstance(value, numbers.Integral) and not isinstance(value, bool):
      result[key] = int(value)
    else:
      result[key] = value
  return result
```
