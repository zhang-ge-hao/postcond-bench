https://github.com/a2aproject/a2a-python/blob/aa159f3e1076ae6eaad5576119d7857c2a9b2448/./src/a2a/utils/proto_utils.py#L69-L95
```
@icontract.ensure(
    lambda result, value, max_safe_digits:
        (
            (lambda f, item:
                f(f, item)
            )(
                lambda self, item:
                    (
                        str(item)
                        if isinstance(item, int) and abs(item) > 10 ** max_safe_digits - 1
                        else {
                            k: self(self, v)
                            for k, v in item.items()
                        } if isinstance(item, dict)
                        else [
                            self(self, i)
                            for i in item
                        ] if isinstance(item, (list, tuple))
                        else item
                    ),
                value
            )
        ) == result
)
```
```
None
```
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29]
===== 0 =====
```
     max_safe_int = 10**max_safe_digits - 1
 
     def _normalize(item: Any) -> Any:
-        if isinstance(item, int) and abs(item) > max_safe_int:
+        if isinstance(None, int) and abs(item) > max_safe_int:
             return str(item)
         if isinstance(item, dict):
             return {k: _normalize(v) for k, v in item.items()}
@@ -24,4 +24,4 @@             return [_normalize(i) for i in item]
         return item
 
-    return _normalize(value)+    return _normalize(value)
```
```
def normalize_large_integers_to_strings(
    value: Any, max_safe_digits: int = 15
) -> Any:
    """Integer preprocessing utility: converts large integers to strings.

    Use this when you want to convert large integers to strings considering
    JavaScript's MAX_SAFE_INTEGER (2^53 - 1) limitation.

    Args:
        value: The value to convert.
        max_safe_digits: Maximum safe integer digits (default: 15).

    Returns:
        A normalized value.
    """
    max_safe_int = 10**max_safe_digits - 1

    def _normalize(item: Any) -> Any:
        if isinstance(None, int) and abs(item) > max_safe_int:
            return str(item)
        if isinstance(item, dict):
            return {k: _normalize(v) for k, v in item.items()}
        if isinstance(item, list | tuple):
            return [_normalize(i) for i in item]
        return item

    return _normalize(value)

```
===== 1 =====
```
     max_safe_int = 10**max_safe_digits - 1
 
     def _normalize(item: Any) -> Any:
-        if isinstance(item, int) and abs(item) > max_safe_int:
+        if isinstance(item, float) and abs(item) > max_safe_int:
             return str(item)
         if isinstance(item, dict):
             return {k: _normalize(v) for k, v in item.items()}
```
```
def normalize_large_integers_to_strings(
    value: Any, max_safe_digits: int = 15
) -> Any:
    """Integer preprocessing utility: converts large integers to strings.

    Use this when you want to convert large integers to strings considering
    JavaScript's MAX_SAFE_INTEGER (2^53 - 1) limitation.

    Args:
        value: The value to convert.
        max_safe_digits: Maximum safe integer digits (default: 15).

    Returns:
        A normalized value.
    """
    max_safe_int = 10**max_safe_digits - 1

    def _normalize(item: Any) -> Any:
        if isinstance(item, float) and abs(item) > max_safe_int:
            return str(item)
        if isinstance(item, dict):
            return {k: _normalize(v) for k, v in item.items()}
        if isinstance(item, list | tuple):
            return [_normalize(i) for i in item]
        return item

    return _normalize(value)
```
===== 2 =====
```
     max_safe_int = 10**max_safe_digits - 1
 
     def _normalize(item: Any) -> Any:
-        if isinstance(item, int) and abs(item) > max_safe_int:
+        if isinstance(item, int) and abs(item) < max_safe_int:
             return str(item)
         if isinstance(item, dict):
             return {k: _normalize(v) for k, v in item.items()}
```
```
def normalize_large_integers_to_strings(
    value: Any, max_safe_digits: int = 15
) -> Any:
    """Integer preprocessing utility: converts large integers to strings.

    Use this when you want to convert large integers to strings considering
    JavaScript's MAX_SAFE_INTEGER (2^53 - 1) limitation.

    Args:
        value: The value to convert.
        max_safe_digits: Maximum safe integer digits (default: 15).

    Returns:
        A normalized value.
    """
    max_safe_int = 10**max_safe_digits - 1

    def _normalize(item: Any) -> Any:
        if isinstance(item, int) and abs(item) < max_safe_int:
            return str(item)
        if isinstance(item, dict):
            return {k: _normalize(v) for k, v in item.items()}
        if isinstance(item, list | tuple):
            return [_normalize(i) for i in item]
        return item

    return _normalize(value)
```
===== 3 =====
```
     max_safe_int = 10**max_safe_digits - 1
 
     def _normalize(item: Any) -> Any:
-        if isinstance(item, int) and abs(item) > max_safe_int:
+        if isinstance(item, int) and item > max_safe_int:
             return str(item)
         if isinstance(item, dict):
             return {k: _normalize(v) for k, v in item.items()}
```
```
def normalize_large_integers_to_strings(
    value: Any, max_safe_digits: int = 15
) -> Any:
    """Integer preprocessing utility: converts large integers to strings.

    Use this when you want to convert large integers to strings considering
    JavaScript's MAX_SAFE_INTEGER (2^53 - 1) limitation.

    Args:
        value: The value to convert.
        max_safe_digits: Maximum safe integer digits (default: 15).

    Returns:
        A normalized value.
    """
    max_safe_int = 10**max_safe_digits - 1

    def _normalize(item: Any) -> Any:
        if isinstance(item, int) and item > max_safe_int:
            return str(item)
        if isinstance(item, dict):
            return {k: _normalize(v) for k, v in item.items()}
        if isinstance(item, list | tuple):
            return [_normalize(i) for i in item]
        return item

    return _normalize(value)
```
===== 4 =====
```
 
     def _normalize(item: Any) -> Any:
         if isinstance(item, int) and abs(item) > max_safe_int:
-            return str(item)
+            return None
         if isinstance(item, dict):
             return {k: _normalize(v) for k, v in item.items()}
         if isinstance(item, list | tuple):
```
```
def normalize_large_integers_to_strings(
    value: Any, max_safe_digits: int = 15
) -> Any:
    """Integer preprocessing utility: converts large integers to strings.

    Use this when you want to convert large integers to strings considering
    JavaScript's MAX_SAFE_INTEGER (2^53 - 1) limitation.

    Args:
        value: The value to convert.
        max_safe_digits: Maximum safe integer digits (default: 15).

    Returns:
        A normalized value.
    """
    max_safe_int = 10**max_safe_digits - 1

    def _normalize(item: Any) -> Any:
        if isinstance(item, int) and abs(item) > max_safe_int:
            return None
        if isinstance(item, dict):
            return {k: _normalize(v) for k, v in item.items()}
        if isinstance(item, list | tuple):
            return [_normalize(i) for i in item]
        return item

    return _normalize(value)
```
===== 5 =====
```
 
     def _normalize(item: Any) -> Any:
         if isinstance(item, int) and abs(item) > max_safe_int:
-            return str(item)
+            return float(item)
         if isinstance(item, dict):
             return {k: _normalize(v) for k, v in item.items()}
         if isinstance(item, list | tuple):
```
```
def normalize_large_integers_to_strings(
    value: Any, max_safe_digits: int = 15
) -> Any:
    """Integer preprocessing utility: converts large integers to strings.

    Use this when you want to convert large integers to strings considering
    JavaScript's MAX_SAFE_INTEGER (2^53 - 1) limitation.

    Args:
        value: The value to convert.
        max_safe_digits: Maximum safe integer digits (default: 15).

    Returns:
        A normalized value.
    """
    max_safe_int = 10**max_safe_digits - 1

    def _normalize(item: Any) -> Any:
        if isinstance(item, int) and abs(item) > max_safe_int:
            return float(item)
        if isinstance(item, dict):
            return {k: _normalize(v) for k, v in item.items()}
        if isinstance(item, list | tuple):
            return [_normalize(i) for i in item]
        return item

    return _normalize(value)
```
===== 6 =====
```
 
     def _normalize(item: Any) -> Any:
         if isinstance(item, int) and abs(item) > max_safe_int:
-            return str(item)
+            return item
         if isinstance(item, dict):
             return {k: _normalize(v) for k, v in item.items()}
         if isinstance(item, list | tuple):
```
```
def normalize_large_integers_to_strings(
    value: Any, max_safe_digits: int = 15
) -> Any:
    """Integer preprocessing utility: converts large integers to strings.

    Use this when you want to convert large integers to strings considering
    JavaScript's MAX_SAFE_INTEGER (2^53 - 1) limitation.

    Args:
        value: The value to convert.
        max_safe_digits: Maximum safe integer digits (default: 15).

    Returns:
        A normalized value.
    """
    max_safe_int = 10**max_safe_digits - 1

    def _normalize(item: Any) -> Any:
        if isinstance(item, int) and abs(item) > max_safe_int:
            return item
        if isinstance(item, dict):
            return {k: _normalize(v) for k, v in item.items()}
        if isinstance(item, list | tuple):
            return [_normalize(i) for i in item]
        return item

    return _normalize(value)
```
===== 7 =====
```
 
     def _normalize(item: Any) -> Any:
         if isinstance(item, int) and abs(item) > max_safe_int:
-            return str(item)
+            return item if isinstance(item, str) else None
         if isinstance(item, dict):
             return {k: _normalize(v) for k, v in item.items()}
         if isinstance(item, list | tuple):
```
```
def normalize_large_integers_to_strings(
    value: Any, max_safe_digits: int = 15
) -> Any:
    """Integer preprocessing utility: converts large integers to strings.

    Use this when you want to convert large integers to strings considering
    JavaScript's MAX_SAFE_INTEGER (2^53 - 1) limitation.

    Args:
        value: The value to convert.
        max_safe_digits: Maximum safe integer digits (default: 15).

    Returns:
        A normalized value.
    """
    max_safe_int = 10**max_safe_digits - 1

    def _normalize(item: Any) -> Any:
        if isinstance(item, int) and abs(item) > max_safe_int:
            return item if isinstance(item, str) else None
        if isinstance(item, dict):
            return {k: _normalize(v) for k, v in item.items()}
        if isinstance(item, list | tuple):
            return [_normalize(i) for i in item]
        return item

    return _normalize(value)
```
===== 8 =====
```
 
     def _normalize(item: Any) -> Any:
         if isinstance(item, int) and abs(item) > max_safe_int:
-            return str(item)
+            return str(None)
         if isinstance(item, dict):
             return {k: _normalize(v) for k, v in item.items()}
         if isinstance(item, list | tuple):
             return [_normalize(i) for i in item]
         return item
 
-    return _normalize(value)+    return _normalize(value)
```
```
def normalize_large_integers_to_strings(
    value: Any, max_safe_digits: int = 15
) -> Any:
    """Integer preprocessing utility: converts large integers to strings.

    Use this when you want to convert large integers to strings considering
    JavaScript's MAX_SAFE_INTEGER (2^53 - 1) limitation.

    Args:
        value: The value to convert.
        max_safe_digits: Maximum safe integer digits (default: 15).

    Returns:
        A normalized value.
    """
    max_safe_int = 10**max_safe_digits - 1

    def _normalize(item: Any) -> Any:
        if isinstance(item, int) and abs(item) > max_safe_int:
            return str(None)
        if isinstance(item, dict):
            return {k: _normalize(v) for k, v in item.items()}
        if isinstance(item, list | tuple):
            return [_normalize(i) for i in item]
        return item

    return _normalize(value)

```
===== 9 =====
```
     def _normalize(item: Any) -> Any:
         if isinstance(item, int) and abs(item) > max_safe_int:
             return str(item)
-        if isinstance(item, dict):
+        if isinstance(None, dict):
             return {k: _normalize(v) for k, v in item.items()}
         if isinstance(item, list | tuple):
             return [_normalize(i) for i in item]
         return item
 
-    return _normalize(value)+    return _normalize(value)
```
```
def normalize_large_integers_to_strings(
    value: Any, max_safe_digits: int = 15
) -> Any:
    """Integer preprocessing utility: converts large integers to strings.

    Use this when you want to convert large integers to strings considering
    JavaScript's MAX_SAFE_INTEGER (2^53 - 1) limitation.

    Args:
        value: The value to convert.
        max_safe_digits: Maximum safe integer digits (default: 15).

    Returns:
        A normalized value.
    """
    max_safe_int = 10**max_safe_digits - 1

    def _normalize(item: Any) -> Any:
        if isinstance(item, int) and abs(item) > max_safe_int:
            return str(item)
        if isinstance(None, dict):
            return {k: _normalize(v) for k, v in item.items()}
        if isinstance(item, list | tuple):
            return [_normalize(i) for i in item]
        return item

    return _normalize(value)

```
===== 10 =====
```
     def _normalize(item: Any) -> Any:
         if isinstance(item, int) and abs(item) > max_safe_int:
             return str(item)
-        if isinstance(item, dict):
+        if isinstance(item, (int, float)):  # Incorrectly checks for numeric types instead of dicts
             return {k: _normalize(v) for k, v in item.items()}
         if isinstance(item, list | tuple):
             return [_normalize(i) for i in item]
```
```
def normalize_large_integers_to_strings(
    value: Any, max_safe_digits: int = 15
) -> Any:
    """Integer preprocessing utility: converts large integers to strings.

    Use this when you want to convert large integers to strings considering
    JavaScript's MAX_SAFE_INTEGER (2^53 - 1) limitation.

    Args:
        value: The value to convert.
        max_safe_digits: Maximum safe integer digits (default: 15).

    Returns:
        A normalized value.
    """
    max_safe_int = 10**max_safe_digits - 1

    def _normalize(item: Any) -> Any:
        if isinstance(item, int) and abs(item) > max_safe_int:
            return str(item)
        if isinstance(item, (int, float)):  # Incorrectly checks for numeric types instead of dicts
            return {k: _normalize(v) for k, v in item.items()}
        if isinstance(item, list | tuple):
            return [_normalize(i) for i in item]
        return item

    return _normalize(value)
```
===== 11 =====
```
     def _normalize(item: Any) -> Any:
         if isinstance(item, int) and abs(item) > max_safe_int:
             return str(item)
-        if isinstance(item, dict):
+        if isinstance(item, list):  # Incorrectly checks for lists instead of dicts
             return {k: _normalize(v) for k, v in item.items()}
         if isinstance(item, list | tuple):
             return [_normalize(i) for i in item]
```
```
def normalize_large_integers_to_strings(
    value: Any, max_safe_digits: int = 15
) -> Any:
    """Integer preprocessing utility: converts large integers to strings.

    Use this when you want to convert large integers to strings considering
    JavaScript's MAX_SAFE_INTEGER (2^53 - 1) limitation.

    Args:
        value: The value to convert.
        max_safe_digits: Maximum safe integer digits (default: 15).

    Returns:
        A normalized value.
    """
    max_safe_int = 10**max_safe_digits - 1

    def _normalize(item: Any) -> Any:
        if isinstance(item, int) and abs(item) > max_safe_int:
            return str(item)
        if isinstance(item, list):  # Incorrectly checks for lists instead of dicts
            return {k: _normalize(v) for k, v in item.items()}
        if isinstance(item, list | tuple):
            return [_normalize(i) for i in item]
        return item

    return _normalize(value)
```
===== 12 =====
```
     def _normalize(item: Any) -> Any:
         if isinstance(item, int) and abs(item) > max_safe_int:
             return str(item)
-        if isinstance(item, dict):
+        if isinstance(item, str):  # Incorrectly checks for strings instead of dicts
             return {k: _normalize(v) for k, v in item.items()}
         if isinstance(item, list | tuple):
             return [_normalize(i) for i in item]
```
```
def normalize_large_integers_to_strings(
    value: Any, max_safe_digits: int = 15
) -> Any:
    """Integer preprocessing utility: converts large integers to strings.

    Use this when you want to convert large integers to strings considering
    JavaScript's MAX_SAFE_INTEGER (2^53 - 1) limitation.

    Args:
        value: The value to convert.
        max_safe_digits: Maximum safe integer digits (default: 15).

    Returns:
        A normalized value.
    """
    max_safe_int = 10**max_safe_digits - 1

    def _normalize(item: Any) -> Any:
        if isinstance(item, int) and abs(item) > max_safe_int:
            return str(item)
        if isinstance(item, str):  # Incorrectly checks for strings instead of dicts
            return {k: _normalize(v) for k, v in item.items()}
        if isinstance(item, list | tuple):
            return [_normalize(i) for i in item]
        return item

    return _normalize(value)
```
===== 13 =====
```
     def _normalize(item: Any) -> Any:
         if isinstance(item, int) and abs(item) > max_safe_int:
             return str(item)
-        if isinstance(item, dict):
+        if isinstance(item, tuple):  # Incorrectly checks for tuples instead of dicts
             return {k: _normalize(v) for k, v in item.items()}
         if isinstance(item, list | tuple):
             return [_normalize(i) for i in item]
```
```
def normalize_large_integers_to_strings(
    value: Any, max_safe_digits: int = 15
) -> Any:
    """Integer preprocessing utility: converts large integers to strings.

    Use this when you want to convert large integers to strings considering
    JavaScript's MAX_SAFE_INTEGER (2^53 - 1) limitation.

    Args:
        value: The value to convert.
        max_safe_digits: Maximum safe integer digits (default: 15).

    Returns:
        A normalized value.
    """
    max_safe_int = 10**max_safe_digits - 1

    def _normalize(item: Any) -> Any:
        if isinstance(item, int) and abs(item) > max_safe_int:
            return str(item)
        if isinstance(item, tuple):  # Incorrectly checks for tuples instead of dicts
            return {k: _normalize(v) for k, v in item.items()}
        if isinstance(item, list | tuple):
            return [_normalize(i) for i in item]
        return item

    return _normalize(value)
```
===== 14 =====
```
     def _normalize(item: Any) -> Any:
         if isinstance(item, int) and abs(item) > max_safe_int:
             return str(item)
-        if isinstance(item, dict):
+        if not isinstance(item, dict):  # Negates the check, leading to incorrect behavior
             return {k: _normalize(v) for k, v in item.items()}
         if isinstance(item, list | tuple):
             return [_normalize(i) for i in item]
```
```
def normalize_large_integers_to_strings(
    value: Any, max_safe_digits: int = 15
) -> Any:
    """Integer preprocessing utility: converts large integers to strings.

    Use this when you want to convert large integers to strings considering
    JavaScript's MAX_SAFE_INTEGER (2^53 - 1) limitation.

    Args:
        value: The value to convert.
        max_safe_digits: Maximum safe integer digits (default: 15).

    Returns:
        A normalized value.
    """
    max_safe_int = 10**max_safe_digits - 1

    def _normalize(item: Any) -> Any:
        if isinstance(item, int) and abs(item) > max_safe_int:
            return str(item)
        if not isinstance(item, dict):  # Negates the check, leading to incorrect behavior
            return {k: _normalize(v) for k, v in item.items()}
        if isinstance(item, list | tuple):
            return [_normalize(i) for i in item]
        return item

    return _normalize(value)
```
===== 15 =====
```
         if isinstance(item, int) and abs(item) > max_safe_int:
             return str(item)
         if isinstance(item, dict):
-            return {k: _normalize(v) for k, v in item.items()}
+            return {k: _normalize(None) for k, v in item.items()}
         if isinstance(item, list | tuple):
             return [_normalize(i) for i in item]
         return item
 
-    return _normalize(value)+    return _normalize(value)
```
```
def normalize_large_integers_to_strings(
    value: Any, max_safe_digits: int = 15
) -> Any:
    """Integer preprocessing utility: converts large integers to strings.

    Use this when you want to convert large integers to strings considering
    JavaScript's MAX_SAFE_INTEGER (2^53 - 1) limitation.

    Args:
        value: The value to convert.
        max_safe_digits: Maximum safe integer digits (default: 15).

    Returns:
        A normalized value.
    """
    max_safe_int = 10**max_safe_digits - 1

    def _normalize(item: Any) -> Any:
        if isinstance(item, int) and abs(item) > max_safe_int:
            return str(item)
        if isinstance(item, dict):
            return {k: _normalize(None) for k, v in item.items()}
        if isinstance(item, list | tuple):
            return [_normalize(i) for i in item]
        return item

    return _normalize(value)

```
===== 16 =====
```
         if isinstance(item, int) and abs(item) > max_safe_int:
             return str(item)
         if isinstance(item, dict):
-            return {k: _normalize(v) for k, v in item.items()}
+            return {k: _normalize(v) for k, v in item.items() if isinstance(v, int)}  # Only normalizes integers
         if isinstance(item, list | tuple):
             return [_normalize(i) for i in item]
         return item
```
```
def normalize_large_integers_to_strings(
    value: Any, max_safe_digits: int = 15
) -> Any:
    """Integer preprocessing utility: converts large integers to strings.

    Use this when you want to convert large integers to strings considering
    JavaScript's MAX_SAFE_INTEGER (2^53 - 1) limitation.

    Args:
        value: The value to convert.
        max_safe_digits: Maximum safe integer digits (default: 15).

    Returns:
        A normalized value.
    """
    max_safe_int = 10**max_safe_digits - 1

    def _normalize(item: Any) -> Any:
        if isinstance(item, int) and abs(item) > max_safe_int:
            return str(item)
        if isinstance(item, dict):
            return {k: _normalize(v) for k, v in item.items() if isinstance(v, int)}  # Only normalizes integers
        if isinstance(item, list | tuple):
            return [_normalize(i) for i in item]
        return item

    return _normalize(value)
```
===== 17 =====
```
         if isinstance(item, int) and abs(item) > max_safe_int:
             return str(item)
         if isinstance(item, dict):
-            return {k: _normalize(v) for k, v in item.items()}
+            return {k: _normalize(v) for k, v in item.items() if isinstance(v, list)}  # Only normalizes values that are lists
         if isinstance(item, list | tuple):
             return [_normalize(i) for i in item]
         return item
```
```
def normalize_large_integers_to_strings(
    value: Any, max_safe_digits: int = 15
) -> Any:
    """Integer preprocessing utility: converts large integers to strings.

    Use this when you want to convert large integers to strings considering
    JavaScript's MAX_SAFE_INTEGER (2^53 - 1) limitation.

    Args:
        value: The value to convert.
        max_safe_digits: Maximum safe integer digits (default: 15).

    Returns:
        A normalized value.
    """
    max_safe_int = 10**max_safe_digits - 1

    def _normalize(item: Any) -> Any:
        if isinstance(item, int) and abs(item) > max_safe_int:
            return str(item)
        if isinstance(item, dict):
            return {k: _normalize(v) for k, v in item.items() if isinstance(v, list)}  # Only normalizes values that are lists
        if isinstance(item, list | tuple):
            return [_normalize(i) for i in item]
        return item

    return _normalize(value)
```
===== 18 =====
```
         if isinstance(item, int) and abs(item) > max_safe_int:
             return str(item)
         if isinstance(item, dict):
-            return {k: _normalize(v) for k, v in item.items()}
+            return {k: _normalize(v) for k, v in item.items() if isinstance(v, str) and v.isdigit()}  # Only normalizes string digits
         if isinstance(item, list | tuple):
             return [_normalize(i) for i in item]
         return item
```
```
def normalize_large_integers_to_strings(
    value: Any, max_safe_digits: int = 15
) -> Any:
    """Integer preprocessing utility: converts large integers to strings.

    Use this when you want to convert large integers to strings considering
    JavaScript's MAX_SAFE_INTEGER (2^53 - 1) limitation.

    Args:
        value: The value to convert.
        max_safe_digits: Maximum safe integer digits (default: 15).

    Returns:
        A normalized value.
    """
    max_safe_int = 10**max_safe_digits - 1

    def _normalize(item: Any) -> Any:
        if isinstance(item, int) and abs(item) > max_safe_int:
            return str(item)
        if isinstance(item, dict):
            return {k: _normalize(v) for k, v in item.items() if isinstance(v, str) and v.isdigit()}  # Only normalizes string digits
        if isinstance(item, list | tuple):
            return [_normalize(i) for i in item]
        return item

    return _normalize(value)
```
===== 19 =====
```
         if isinstance(item, int) and abs(item) > max_safe_int:
             return str(item)
         if isinstance(item, dict):
-            return {k: _normalize(v) for k, v in item.items()}
+            return {k: _normalize(v) for k, v in item.items() if k.startswith('a')}  # Only normalizes keys that start with 'a'
         if isinstance(item, list | tuple):
             return [_normalize(i) for i in item]
         return item
```
```
def normalize_large_integers_to_strings(
    value: Any, max_safe_digits: int = 15
) -> Any:
    """Integer preprocessing utility: converts large integers to strings.

    Use this when you want to convert large integers to strings considering
    JavaScript's MAX_SAFE_INTEGER (2^53 - 1) limitation.

    Args:
        value: The value to convert.
        max_safe_digits: Maximum safe integer digits (default: 15).

    Returns:
        A normalized value.
    """
    max_safe_int = 10**max_safe_digits - 1

    def _normalize(item: Any) -> Any:
        if isinstance(item, int) and abs(item) > max_safe_int:
            return str(item)
        if isinstance(item, dict):
            return {k: _normalize(v) for k, v in item.items() if k.startswith('a')}  # Only normalizes keys that start with 'a'
        if isinstance(item, list | tuple):
            return [_normalize(i) for i in item]
        return item

    return _normalize(value)
```
===== 20 =====
```
             return str(item)
         if isinstance(item, dict):
             return {k: _normalize(v) for k, v in item.items()}
-        if isinstance(item, list | tuple):
+        if isinstance(None, list | tuple):
             return [_normalize(i) for i in item]
         return item
 
-    return _normalize(value)+    return _normalize(value)
```
```
def normalize_large_integers_to_strings(
    value: Any, max_safe_digits: int = 15
) -> Any:
    """Integer preprocessing utility: converts large integers to strings.

    Use this when you want to convert large integers to strings considering
    JavaScript's MAX_SAFE_INTEGER (2^53 - 1) limitation.

    Args:
        value: The value to convert.
        max_safe_digits: Maximum safe integer digits (default: 15).

    Returns:
        A normalized value.
    """
    max_safe_int = 10**max_safe_digits - 1

    def _normalize(item: Any) -> Any:
        if isinstance(item, int) and abs(item) > max_safe_int:
            return str(item)
        if isinstance(item, dict):
            return {k: _normalize(v) for k, v in item.items()}
        if isinstance(None, list | tuple):
            return [_normalize(i) for i in item]
        return item

    return _normalize(value)

```
===== 21 =====
```
         if isinstance(item, dict):
             return {k: _normalize(v) for k, v in item.items()}
         if isinstance(item, list | tuple):
-            return [_normalize(i) for i in item]
+            return [_normalize(None) for i in item]
         return item
 
-    return _normalize(value)+    return _normalize(value)
```
```
def normalize_large_integers_to_strings(
    value: Any, max_safe_digits: int = 15
) -> Any:
    """Integer preprocessing utility: converts large integers to strings.

    Use this when you want to convert large integers to strings considering
    JavaScript's MAX_SAFE_INTEGER (2^53 - 1) limitation.

    Args:
        value: The value to convert.
        max_safe_digits: Maximum safe integer digits (default: 15).

    Returns:
        A normalized value.
    """
    max_safe_int = 10**max_safe_digits - 1

    def _normalize(item: Any) -> Any:
        if isinstance(item, int) and abs(item) > max_safe_int:
            return str(item)
        if isinstance(item, dict):
            return {k: _normalize(v) for k, v in item.items()}
        if isinstance(item, list | tuple):
            return [_normalize(None) for i in item]
        return item

    return _normalize(value)

```
===== 22 =====
```
         if isinstance(item, dict):
             return {k: _normalize(v) for k, v in item.items()}
         if isinstance(item, list | tuple):
-            return [_normalize(i) for i in item]
+            return [_normalize(i) for i in item if isinstance(i, int)]  # Only normalizes integers
         return item
 
     return _normalize(value)
```
```
def normalize_large_integers_to_strings(
    value: Any, max_safe_digits: int = 15
) -> Any:
    """Integer preprocessing utility: converts large integers to strings.

    Use this when you want to convert large integers to strings considering
    JavaScript's MAX_SAFE_INTEGER (2^53 - 1) limitation.

    Args:
        value: The value to convert.
        max_safe_digits: Maximum safe integer digits (default: 15).

    Returns:
        A normalized value.
    """
    max_safe_int = 10**max_safe_digits - 1

    def _normalize(item: Any) -> Any:
        if isinstance(item, int) and abs(item) > max_safe_int:
            return str(item)
        if isinstance(item, dict):
            return {k: _normalize(v) for k, v in item.items()}
        if isinstance(item, list | tuple):
            return [_normalize(i) for i in item if isinstance(i, int)]  # Only normalizes integers
        return item

    return _normalize(value)
```
===== 23 =====
```
         if isinstance(item, dict):
             return {k: _normalize(v) for k, v in item.items()}
         if isinstance(item, list | tuple):
-            return [_normalize(i) for i in item]
+            return [_normalize(i) for i in item[:1]]  # Only normalizes the first item
         return item
 
     return _normalize(value)
```
```
def normalize_large_integers_to_strings(
    value: Any, max_safe_digits: int = 15
) -> Any:
    """Integer preprocessing utility: converts large integers to strings.

    Use this when you want to convert large integers to strings considering
    JavaScript's MAX_SAFE_INTEGER (2^53 - 1) limitation.

    Args:
        value: The value to convert.
        max_safe_digits: Maximum safe integer digits (default: 15).

    Returns:
        A normalized value.
    """
    max_safe_int = 10**max_safe_digits - 1

    def _normalize(item: Any) -> Any:
        if isinstance(item, int) and abs(item) > max_safe_int:
            return str(item)
        if isinstance(item, dict):
            return {k: _normalize(v) for k, v in item.items()}
        if isinstance(item, list | tuple):
            return [_normalize(i) for i in item[:1]]  # Only normalizes the first item
        return item

    return _normalize(value)
```
===== 24 =====
```
         if isinstance(item, dict):
             return {k: _normalize(v) for k, v in item.items()}
         if isinstance(item, list | tuple):
-            return [_normalize(i) for i in item]
+            return [_normalize(i) for i in item] + [0]  # Appends 0 to the result
         return item
 
     return _normalize(value)
```
```
def normalize_large_integers_to_strings(
    value: Any, max_safe_digits: int = 15
) -> Any:
    """Integer preprocessing utility: converts large integers to strings.

    Use this when you want to convert large integers to strings considering
    JavaScript's MAX_SAFE_INTEGER (2^53 - 1) limitation.

    Args:
        value: The value to convert.
        max_safe_digits: Maximum safe integer digits (default: 15).

    Returns:
        A normalized value.
    """
    max_safe_int = 10**max_safe_digits - 1

    def _normalize(item: Any) -> Any:
        if isinstance(item, int) and abs(item) > max_safe_int:
            return str(item)
        if isinstance(item, dict):
            return {k: _normalize(v) for k, v in item.items()}
        if isinstance(item, list | tuple):
            return [_normalize(i) for i in item] + [0]  # Appends 0 to the result
        return item

    return _normalize(value)
```
===== 25 =====
```
         if isinstance(item, dict):
             return {k: _normalize(v) for k, v in item.items()}
         if isinstance(item, list | tuple):
-            return [_normalize(i) for i in item]
+            return [_normalize(i) for i in item] + [None]
         return item
 
     return _normalize(value)
```
```
def normalize_large_integers_to_strings(
    value: Any, max_safe_digits: int = 15
) -> Any:
    """Integer preprocessing utility: converts large integers to strings.

    Use this when you want to convert large integers to strings considering
    JavaScript's MAX_SAFE_INTEGER (2^53 - 1) limitation.

    Args:
        value: The value to convert.
        max_safe_digits: Maximum safe integer digits (default: 15).

    Returns:
        A normalized value.
    """
    max_safe_int = 10**max_safe_digits - 1

    def _normalize(item: Any) -> Any:
        if isinstance(item, int) and abs(item) > max_safe_int:
            return str(item)
        if isinstance(item, dict):
            return {k: _normalize(v) for k, v in item.items()}
        if isinstance(item, list | tuple):
            return [_normalize(i) for i in item] + [None]
        return item

    return _normalize(value)
```
===== 26 =====
```
             return [_normalize(i) for i in item]
         return item
 
-    return _normalize(value)+    return None  # This will return None instead of the normalized value, causing loss of data.
```
```
def normalize_large_integers_to_strings(
    value: Any, max_safe_digits: int = 15
) -> Any:
    """Integer preprocessing utility: converts large integers to strings.

    Use this when you want to convert large integers to strings considering
    JavaScript's MAX_SAFE_INTEGER (2^53 - 1) limitation.

    Args:
        value: The value to convert.
        max_safe_digits: Maximum safe integer digits (default: 15).

    Returns:
        A normalized value.
    """
    max_safe_int = 10**max_safe_digits - 1

    def _normalize(item: Any) -> Any:
        if isinstance(item, int) and abs(item) > max_safe_int:
            return str(item)
        if isinstance(item, dict):
            return {k: _normalize(v) for k, v in item.items()}
        if isinstance(item, list | tuple):
            return [_normalize(i) for i in item]
        return item

    return None  # This will return None instead of the normalized value, causing loss of data.
```
===== 27 =====
```
             return [_normalize(i) for i in item]
         return item
 
-    return _normalize(value)+    return _normalize(None)
```
```
def normalize_large_integers_to_strings(
    value: Any, max_safe_digits: int = 15
) -> Any:
    """Integer preprocessing utility: converts large integers to strings.

    Use this when you want to convert large integers to strings considering
    JavaScript's MAX_SAFE_INTEGER (2^53 - 1) limitation.

    Args:
        value: The value to convert.
        max_safe_digits: Maximum safe integer digits (default: 15).

    Returns:
        A normalized value.
    """
    max_safe_int = 10**max_safe_digits - 1

    def _normalize(item: Any) -> Any:
        if isinstance(item, int) and abs(item) > max_safe_int:
            return str(item)
        if isinstance(item, dict):
            return {k: _normalize(v) for k, v in item.items()}
        if isinstance(item, list | tuple):
            return [_normalize(i) for i in item]
        return item

    return _normalize(None)

```
===== 28 =====
```
             return [_normalize(i) for i in item]
         return item
 
-    return _normalize(value)+    return _normalize(value) if isinstance(value, list) else value  # This will only normalize lists, ignoring other types.
```
```
def normalize_large_integers_to_strings(
    value: Any, max_safe_digits: int = 15
) -> Any:
    """Integer preprocessing utility: converts large integers to strings.

    Use this when you want to convert large integers to strings considering
    JavaScript's MAX_SAFE_INTEGER (2^53 - 1) limitation.

    Args:
        value: The value to convert.
        max_safe_digits: Maximum safe integer digits (default: 15).

    Returns:
        A normalized value.
    """
    max_safe_int = 10**max_safe_digits - 1

    def _normalize(item: Any) -> Any:
        if isinstance(item, int) and abs(item) > max_safe_int:
            return str(item)
        if isinstance(item, dict):
            return {k: _normalize(v) for k, v in item.items()}
        if isinstance(item, list | tuple):
            return [_normalize(i) for i in item]
        return item

    return _normalize(value) if isinstance(value, list) else value  # This will only normalize lists, ignoring other types.
```
===== 29 =====
```
             return [_normalize(i) for i in item]
         return item
 
-    return _normalize(value)+    return value  # This will return the original value without normalization.
```
```
def normalize_large_integers_to_strings(
    value: Any, max_safe_digits: int = 15
) -> Any:
    """Integer preprocessing utility: converts large integers to strings.

    Use this when you want to convert large integers to strings considering
    JavaScript's MAX_SAFE_INTEGER (2^53 - 1) limitation.

    Args:
        value: The value to convert.
        max_safe_digits: Maximum safe integer digits (default: 15).

    Returns:
        A normalized value.
    """
    max_safe_int = 10**max_safe_digits - 1

    def _normalize(item: Any) -> Any:
        if isinstance(item, int) and abs(item) > max_safe_int:
            return str(item)
        if isinstance(item, dict):
            return {k: _normalize(v) for k, v in item.items()}
        if isinstance(item, list | tuple):
            return [_normalize(i) for i in item]
        return item

    return value  # This will return the original value without normalization.
```
