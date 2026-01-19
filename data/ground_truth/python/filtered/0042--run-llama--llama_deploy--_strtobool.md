https://github.com/run-llama/llama_deploy/blob/dbe78972b06f8d8b021da0b313bb0e4f3dc32d46/./llama_deploy/cli/config.py#L9-L24
```
🈚️

specified error process

@icontract.ensure(
    lambda result: isinstance(result, bool),
    "Return value must be a bool.",
)
@icontract.ensure(
    lambda result, val: (
        # 如果函数正常返回，输入必须在允许集合里
        val.lower() in ("y", "yes", "t", "true", "on", "1",
                        "n", "no", "f", "false", "off", "0")
    ),
    "Function must only return for known truthy/falsy strings.",
)
@icontract.ensure(
    lambda result, val: (
        # 正确逻辑：truthy 集合 -> True，其它（这里仅 falsy 集合）-> False
        (
            val.lower() in ("y", "yes", "t", "true", "on", "1")
        ) == result
    ),
    "Result must match the canonical truth mapping.",
)
```
```
@icontract.snapshot(lambda val: val, name="val_orig")
@icontract.snapshot(lambda val: val.lower(), name="val_lower")
@icontract.ensure(lambda result: isinstance(result, bool))
@icontract.ensure(lambda OLD, result: (OLD.val_lower == "y")   <= (result is True))
@icontract.ensure(lambda OLD, result: (OLD.val_lower == "yes") <= (result is True))
@icontract.ensure(lambda OLD, result: (OLD.val_lower == "t")   <= (result is True))
@icontract.ensure(lambda OLD, result: (OLD.val_lower == "true")<= (result is True))
@icontract.ensure(lambda OLD, result: (OLD.val_lower == "on")  <= (result is True))
@icontract.ensure(lambda OLD, result: (OLD.val_lower == "1")   <= (result is True))
@icontract.ensure(lambda OLD, result: (OLD.val_lower == "n")   <= (result is False))
@icontract.ensure(lambda OLD, result: (OLD.val_lower == "no")  <= (result is False))
@icontract.ensure(lambda OLD, result: (OLD.val_lower == "f")   <= (result is False))
@icontract.ensure(lambda OLD, result: (OLD.val_lower == "false")<= (result is False))
@icontract.ensure(lambda OLD, result: (OLD.val_lower == "off") <= (result is False))
@icontract.ensure(lambda OLD, result: (OLD.val_lower == "0")   <= (result is False))
@icontract.ensure(lambda OLD: OLD.val_lower in ("y", "yes", "t", "true", "on", "1", "n", "no", "f", "false", "off", "0"))
```
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
===== 0 =====
```
     are 'n', 'no', 'f', 'false', 'off', and '0'.  Raises ValueError if
     'val' is anything else.
     """
-    val = val.lower()
+    val = None
     if val in ("y", "yes", "t", "true", "on", "1"):
         return True
     elif val in ("n", "no", "f", "false", "off", "0"):
         return False
     else:
-        raise ValueError("invalid truth value %r" % (val,))+        raise ValueError("invalid truth value %r" % (val,))
```
```
def _strtobool(val: str) -> bool:
    """Convert a string representation of truth to True or False.

    Original code from distutils (MIT license).

    True values are 'y', 'yes', 't', 'true', 'on', and '1'; false values
    are 'n', 'no', 'f', 'false', 'off', and '0'.  Raises ValueError if
    'val' is anything else.
    """
    val = None
    if val in ("y", "yes", "t", "true", "on", "1"):
        return True
    elif val in ("n", "no", "f", "false", "off", "0"):
        return False
    else:
        raise ValueError("invalid truth value %r" % (val,))

```
===== 1 =====
```
     are 'n', 'no', 'f', 'false', 'off', and '0'.  Raises ValueError if
     'val' is anything else.
     """
-    val = val.lower()
+    val = val.upper()
     if val in ("y", "yes", "t", "true", "on", "1"):
         return True
     elif val in ("n", "no", "f", "false", "off", "0"):
```
```
def _strtobool(val: str) -> bool:
    """Convert a string representation of truth to True or False.

    Original code from distutils (MIT license).

    True values are 'y', 'yes', 't', 'true', 'on', and '1'; false values
    are 'n', 'no', 'f', 'false', 'off', and '0'.  Raises ValueError if
    'val' is anything else.
    """
    val = val.upper()
    if val in ("y", "yes", "t", "true", "on", "1"):
        return True
    elif val in ("n", "no", "f", "false", "off", "0"):
        return False
    else:
        raise ValueError("invalid truth value %r" % (val,))
```
===== 2 =====
```
     are 'n', 'no', 'f', 'false', 'off', and '0'.  Raises ValueError if
     'val' is anything else.
     """
-    val = val.lower()
+    val = val.upper()
     if val in ("y", "yes", "t", "true", "on", "1"):
         return True
     elif val in ("n", "no", "f", "false", "off", "0"):
         return False
     else:
-        raise ValueError("invalid truth value %r" % (val,))+        raise ValueError("invalid truth value %r" % (val,))
```
```
def _strtobool(val: str) -> bool:
    """Convert a string representation of truth to True or False.

    Original code from distutils (MIT license).

    True values are 'y', 'yes', 't', 'true', 'on', and '1'; false values
    are 'n', 'no', 'f', 'false', 'off', and '0'.  Raises ValueError if
    'val' is anything else.
    """
    val = val.upper()
    if val in ("y", "yes", "t", "true", "on", "1"):
        return True
    elif val in ("n", "no", "f", "false", "off", "0"):
        return False
    else:
        raise ValueError("invalid truth value %r" % (val,))

```
===== 3 =====
```
     are 'n', 'no', 'f', 'false', 'off', and '0'.  Raises ValueError if
     'val' is anything else.
     """
-    val = val.lower()
+    val = val[::-1]
     if val in ("y", "yes", "t", "true", "on", "1"):
         return True
     elif val in ("n", "no", "f", "false", "off", "0"):
```
```
def _strtobool(val: str) -> bool:
    """Convert a string representation of truth to True or False.

    Original code from distutils (MIT license).

    True values are 'y', 'yes', 't', 'true', 'on', and '1'; false values
    are 'n', 'no', 'f', 'false', 'off', and '0'.  Raises ValueError if
    'val' is anything else.
    """
    val = val[::-1]
    if val in ("y", "yes", "t", "true", "on", "1"):
        return True
    elif val in ("n", "no", "f", "false", "off", "0"):
        return False
    else:
        raise ValueError("invalid truth value %r" % (val,))
```
===== 4 =====
```
     'val' is anything else.
     """
     val = val.lower()
-    if val in ("y", "yes", "t", "true", "on", "1"):
+    if val in ("y", "yes", "t", "TRUE", "on", "1"):
         return True
     elif val in ("n", "no", "f", "false", "off", "0"):
         return False
     else:
-        raise ValueError("invalid truth value %r" % (val,))+        raise ValueError("invalid truth value %r" % (val,))
```
```
def _strtobool(val: str) -> bool:
    """Convert a string representation of truth to True or False.

    Original code from distutils (MIT license).

    True values are 'y', 'yes', 't', 'true', 'on', and '1'; false values
    are 'n', 'no', 'f', 'false', 'off', and '0'.  Raises ValueError if
    'val' is anything else.
    """
    val = val.lower()
    if val in ("y", "yes", "t", "TRUE", "on", "1"):
        return True
    elif val in ("n", "no", "f", "false", "off", "0"):
        return False
    else:
        raise ValueError("invalid truth value %r" % (val,))

```
===== 5 =====
```
     'val' is anything else.
     """
     val = val.lower()
-    if val in ("y", "yes", "t", "true", "on", "1"):
+    if val in ("y", "yes", "t", "XXtrueXX", "on", "1"):
         return True
     elif val in ("n", "no", "f", "false", "off", "0"):
         return False
     else:
-        raise ValueError("invalid truth value %r" % (val,))+        raise ValueError("invalid truth value %r" % (val,))
```
```
def _strtobool(val: str) -> bool:
    """Convert a string representation of truth to True or False.

    Original code from distutils (MIT license).

    True values are 'y', 'yes', 't', 'true', 'on', and '1'; false values
    are 'n', 'no', 'f', 'false', 'off', and '0'.  Raises ValueError if
    'val' is anything else.
    """
    val = val.lower()
    if val in ("y", "yes", "t", "XXtrueXX", "on", "1"):
        return True
    elif val in ("n", "no", "f", "false", "off", "0"):
        return False
    else:
        raise ValueError("invalid truth value %r" % (val,))

```
===== 6 =====
```
     'val' is anything else.
     """
     val = val.lower()
-    if val in ("y", "yes", "t", "true", "on", "1"):
+    if val not in ("y", "yes", "t", "true", "on", "1"):
         return True
     elif val in ("n", "no", "f", "false", "off", "0"):
         return False
     else:
-        raise ValueError("invalid truth value %r" % (val,))+        raise ValueError("invalid truth value %r" % (val,))
```
```
def _strtobool(val: str) -> bool:
    """Convert a string representation of truth to True or False.

    Original code from distutils (MIT license).

    True values are 'y', 'yes', 't', 'true', 'on', and '1'; false values
    are 'n', 'no', 'f', 'false', 'off', and '0'.  Raises ValueError if
    'val' is anything else.
    """
    val = val.lower()
    if val not in ("y", "yes", "t", "true", "on", "1"):
        return True
    elif val in ("n", "no", "f", "false", "off", "0"):
        return False
    else:
        raise ValueError("invalid truth value %r" % (val,))

```
===== 7 =====
```
     val = val.lower()
     if val in ("y", "yes", "t", "true", "on", "1"):
         return True
-    elif val in ("n", "no", "f", "false", "off", "0"):
+    elif val in ("n", "no", "f", "FALSE", "off", "0"):
         return False
     else:
-        raise ValueError("invalid truth value %r" % (val,))+        raise ValueError("invalid truth value %r" % (val,))
```
```
def _strtobool(val: str) -> bool:
    """Convert a string representation of truth to True or False.

    Original code from distutils (MIT license).

    True values are 'y', 'yes', 't', 'true', 'on', and '1'; false values
    are 'n', 'no', 'f', 'false', 'off', and '0'.  Raises ValueError if
    'val' is anything else.
    """
    val = val.lower()
    if val in ("y", "yes", "t", "true", "on", "1"):
        return True
    elif val in ("n", "no", "f", "FALSE", "off", "0"):
        return False
    else:
        raise ValueError("invalid truth value %r" % (val,))

```
===== 8 =====
```
     val = val.lower()
     if val in ("y", "yes", "t", "true", "on", "1"):
         return True
-    elif val in ("n", "no", "f", "false", "off", "0"):
+    elif val in ("n", "no", "f", "XXfalseXX", "off", "0"):
         return False
     else:
-        raise ValueError("invalid truth value %r" % (val,))+        raise ValueError("invalid truth value %r" % (val,))
```
```
def _strtobool(val: str) -> bool:
    """Convert a string representation of truth to True or False.

    Original code from distutils (MIT license).

    True values are 'y', 'yes', 't', 'true', 'on', and '1'; false values
    are 'n', 'no', 'f', 'false', 'off', and '0'.  Raises ValueError if
    'val' is anything else.
    """
    val = val.lower()
    if val in ("y", "yes", "t", "true", "on", "1"):
        return True
    elif val in ("n", "no", "f", "XXfalseXX", "off", "0"):
        return False
    else:
        raise ValueError("invalid truth value %r" % (val,))

```
===== 9 =====
```
     val = val.lower()
     if val in ("y", "yes", "t", "true", "on", "1"):
         return True
-    elif val in ("n", "no", "f", "false", "off", "0"):
+    elif val not in ("n", "no", "f", "false", "off", "0"):
         return False
     else:
-        raise ValueError("invalid truth value %r" % (val,))+        raise ValueError("invalid truth value %r" % (val,))
```
```
def _strtobool(val: str) -> bool:
    """Convert a string representation of truth to True or False.

    Original code from distutils (MIT license).

    True values are 'y', 'yes', 't', 'true', 'on', and '1'; false values
    are 'n', 'no', 'f', 'false', 'off', and '0'.  Raises ValueError if
    'val' is anything else.
    """
    val = val.lower()
    if val in ("y", "yes", "t", "true", "on", "1"):
        return True
    elif val not in ("n", "no", "f", "false", "off", "0"):
        return False
    else:
        raise ValueError("invalid truth value %r" % (val,))

```
