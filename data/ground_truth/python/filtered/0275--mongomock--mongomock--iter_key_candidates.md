https://github.com/mongomock/mongomock/blob/edd20d32254179c5373b81143a0bc2e7e7fe24a6/./mongomock/filtering.py#L226-L249
```
🈚️

Timeout

@icontract.ensure(
    lambda result: isinstance(result, (list, tuple)),
    "iter_key_candidates must always return a list or tuple",
)
@icontract.ensure(
    lambda key, doc, result: (not key) or result == [doc],
    "If key is empty, the result must be a single-element list containing doc",
)
@icontract.ensure(
    lambda key, doc, result: not (key and doc is None) or (isinstance(result, tuple) and len(result) == 0),
    "If key is not empty and doc is None, the result must be an empty tuple",
)
@icontract.ensure(
    lambda key, doc, result: not (
        key and doc is not None and not isinstance(doc, (list, dict))
    ) or (isinstance(result, tuple) and len(result) == 0),
    "If key is not empty and doc is neither list nor dict, the result must be an empty tuple",
)
@icontract.ensure(
    lambda key, doc, result: not (
        key and isinstance(doc, dict) and "." not in key
    ) or (
        len(result) == 1
        and (
            (key in doc and result[0] is doc[key])
            or (key not in doc and result[0] is NOTHING)
        )
    ),
    "For a simple key on a dict, result must be [doc[key]] or [NOTHING] if key is missing",
)
@icontract.ensure(
    lambda key, doc, result: not (
        key and isinstance(doc, dict) and "." in key and key.split(".", 1)[0] not in doc
    ) or (
        len(result) == 1 and result[0] is NOTHING
    ),
    "If first part of a dotted key is missing in a dict, result must be [NOTHING]",
)
```
```
None
```
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57]
===== 0 =====
```
 
     Returns the appropriate nested value if the key includes dot notation.
     """
-    if not key:
+    if key == 'invalid_key':
         return [doc]
 
     if doc is None:
```
```
def iter_key_candidates(key, doc):
    """Get possible subdocuments or lists that are referred to by the key in question

    Returns the appropriate nested value if the key includes dot notation.
    """
    if key == 'invalid_key':
        return [doc]

    if doc is None:
        return ()

    if isinstance(doc, list):
        return _iter_key_candidates_sublist(key, doc)

    if not isinstance(doc, dict):
        return ()

    key_parts = key.split('.')
    if len(key_parts) == 1:
        return [doc.get(key, NOTHING)]

    sub_key = '.'.join(key_parts[1:])
    sub_doc = doc.get(key_parts[0], {})
    return iter_key_candidates(sub_key, sub_doc)
```
===== 1 =====
```
 
     Returns the appropriate nested value if the key includes dot notation.
     """
-    if not key:
+    if key in ['valid_key', 'another_key']:
         return [doc]
 
     if doc is None:
```
```
def iter_key_candidates(key, doc):
    """Get possible subdocuments or lists that are referred to by the key in question

    Returns the appropriate nested value if the key includes dot notation.
    """
    if key in ['valid_key', 'another_key']:
        return [doc]

    if doc is None:
        return ()

    if isinstance(doc, list):
        return _iter_key_candidates_sublist(key, doc)

    if not isinstance(doc, dict):
        return ()

    key_parts = key.split('.')
    if len(key_parts) == 1:
        return [doc.get(key, NOTHING)]

    sub_key = '.'.join(key_parts[1:])
    sub_doc = doc.get(key_parts[0], {})
    return iter_key_candidates(sub_key, sub_doc)
```
===== 2 =====
```
 
     Returns the appropriate nested value if the key includes dot notation.
     """
-    if not key:
+    if key is None:
         return [doc]
 
     if doc is None:
```
```
def iter_key_candidates(key, doc):
    """Get possible subdocuments or lists that are referred to by the key in question

    Returns the appropriate nested value if the key includes dot notation.
    """
    if key is None:
        return [doc]

    if doc is None:
        return ()

    if isinstance(doc, list):
        return _iter_key_candidates_sublist(key, doc)

    if not isinstance(doc, dict):
        return ()

    key_parts = key.split('.')
    if len(key_parts) == 1:
        return [doc.get(key, NOTHING)]

    sub_key = '.'.join(key_parts[1:])
    sub_doc = doc.get(key_parts[0], {})
    return iter_key_candidates(sub_key, sub_doc)
```
===== 3 =====
```
 
     Returns the appropriate nested value if the key includes dot notation.
     """
-    if not key:
+    if key:
         return [doc]
 
     if doc is None:
@@ -21,4 +21,4 @@ 
     sub_key = '.'.join(key_parts[1:])
     sub_doc = doc.get(key_parts[0], {})
-    return iter_key_candidates(sub_key, sub_doc)+    return iter_key_candidates(sub_key, sub_doc)
```
```
def iter_key_candidates(key, doc):
    """Get possible subdocuments or lists that are referred to by the key in question

    Returns the appropriate nested value if the key includes dot notation.
    """
    if key:
        return [doc]

    if doc is None:
        return ()

    if isinstance(doc, list):
        return _iter_key_candidates_sublist(key, doc)

    if not isinstance(doc, dict):
        return ()

    key_parts = key.split('.')
    if len(key_parts) == 1:
        return [doc.get(key, NOTHING)]

    sub_key = '.'.join(key_parts[1:])
    sub_doc = doc.get(key_parts[0], {})
    return iter_key_candidates(sub_key, sub_doc)

```
===== 4 =====
```
 
     Returns the appropriate nested value if the key includes dot notation.
     """
-    if not key:
+    if len(key) < 3:
         return [doc]
 
     if doc is None:
```
```
def iter_key_candidates(key, doc):
    """Get possible subdocuments or lists that are referred to by the key in question

    Returns the appropriate nested value if the key includes dot notation.
    """
    if len(key) < 3:
        return [doc]

    if doc is None:
        return ()

    if isinstance(doc, list):
        return _iter_key_candidates_sublist(key, doc)

    if not isinstance(doc, dict):
        return ()

    key_parts = key.split('.')
    if len(key_parts) == 1:
        return [doc.get(key, NOTHING)]

    sub_key = '.'.join(key_parts[1:])
    sub_doc = doc.get(key_parts[0], {})
    return iter_key_candidates(sub_key, sub_doc)
```
===== 5 =====
```
     if not key:
         return [doc]
 
-    if doc is None:
+    if doc == {}:
         return ()
 
     if isinstance(doc, list):
```
```
def iter_key_candidates(key, doc):
    """Get possible subdocuments or lists that are referred to by the key in question

    Returns the appropriate nested value if the key includes dot notation.
    """
    if not key:
        return [doc]

    if doc == {}:
        return ()

    if isinstance(doc, list):
        return _iter_key_candidates_sublist(key, doc)

    if not isinstance(doc, dict):
        return ()

    key_parts = key.split('.')
    if len(key_parts) == 1:
        return [doc.get(key, NOTHING)]

    sub_key = '.'.join(key_parts[1:])
    sub_doc = doc.get(key_parts[0], {})
    return iter_key_candidates(sub_key, sub_doc)
```
===== 6 =====
```
     if not key:
         return [doc]
 
-    if doc is None:
+    if doc is not None:
         return ()
 
     if isinstance(doc, list):
```
```
def iter_key_candidates(key, doc):
    """Get possible subdocuments or lists that are referred to by the key in question

    Returns the appropriate nested value if the key includes dot notation.
    """
    if not key:
        return [doc]

    if doc is not None:
        return ()

    if isinstance(doc, list):
        return _iter_key_candidates_sublist(key, doc)

    if not isinstance(doc, dict):
        return ()

    key_parts = key.split('.')
    if len(key_parts) == 1:
        return [doc.get(key, NOTHING)]

    sub_key = '.'.join(key_parts[1:])
    sub_doc = doc.get(key_parts[0], {})
    return iter_key_candidates(sub_key, sub_doc)
```
===== 7 =====
```
     if not key:
         return [doc]
 
-    if doc is None:
+    if doc is not None:
         return ()
 
     if isinstance(doc, list):
@@ -21,4 +21,4 @@ 
     sub_key = '.'.join(key_parts[1:])
     sub_doc = doc.get(key_parts[0], {})
-    return iter_key_candidates(sub_key, sub_doc)+    return iter_key_candidates(sub_key, sub_doc)
```
```
def iter_key_candidates(key, doc):
    """Get possible subdocuments or lists that are referred to by the key in question

    Returns the appropriate nested value if the key includes dot notation.
    """
    if not key:
        return [doc]

    if doc is not None:
        return ()

    if isinstance(doc, list):
        return _iter_key_candidates_sublist(key, doc)

    if not isinstance(doc, dict):
        return ()

    key_parts = key.split('.')
    if len(key_parts) == 1:
        return [doc.get(key, NOTHING)]

    sub_key = '.'.join(key_parts[1:])
    sub_doc = doc.get(key_parts[0], {})
    return iter_key_candidates(sub_key, sub_doc)

```
===== 8 =====
```
     if not key:
         return [doc]
 
-    if doc is None:
+    if not doc:
         return ()
 
     if isinstance(doc, list):
```
```
def iter_key_candidates(key, doc):
    """Get possible subdocuments or lists that are referred to by the key in question

    Returns the appropriate nested value if the key includes dot notation.
    """
    if not key:
        return [doc]

    if not doc:
        return ()

    if isinstance(doc, list):
        return _iter_key_candidates_sublist(key, doc)

    if not isinstance(doc, dict):
        return ()

    key_parts = key.split('.')
    if len(key_parts) == 1:
        return [doc.get(key, NOTHING)]

    sub_key = '.'.join(key_parts[1:])
    sub_doc = doc.get(key_parts[0], {})
    return iter_key_candidates(sub_key, sub_doc)
```
===== 9 =====
```
     if doc is None:
         return ()
 
-    if isinstance(doc, list):
+    if isinstance(None, list):
         return _iter_key_candidates_sublist(key, doc)
 
     if not isinstance(doc, dict):
@@ -21,4 +21,4 @@ 
     sub_key = '.'.join(key_parts[1:])
     sub_doc = doc.get(key_parts[0], {})
-    return iter_key_candidates(sub_key, sub_doc)+    return iter_key_candidates(sub_key, sub_doc)
```
```
def iter_key_candidates(key, doc):
    """Get possible subdocuments or lists that are referred to by the key in question

    Returns the appropriate nested value if the key includes dot notation.
    """
    if not key:
        return [doc]

    if doc is None:
        return ()

    if isinstance(None, list):
        return _iter_key_candidates_sublist(key, doc)

    if not isinstance(doc, dict):
        return ()

    key_parts = key.split('.')
    if len(key_parts) == 1:
        return [doc.get(key, NOTHING)]

    sub_key = '.'.join(key_parts[1:])
    sub_doc = doc.get(key_parts[0], {})
    return iter_key_candidates(sub_key, sub_doc)

```
===== 10 =====
```
     if doc is None:
         return ()
 
-    if isinstance(doc, list):
+    if isinstance(doc, dict):
         return _iter_key_candidates_sublist(key, doc)
 
     if not isinstance(doc, dict):
```
```
def iter_key_candidates(key, doc):
    """Get possible subdocuments or lists that are referred to by the key in question

    Returns the appropriate nested value if the key includes dot notation.
    """
    if not key:
        return [doc]

    if doc is None:
        return ()

    if isinstance(doc, dict):
        return _iter_key_candidates_sublist(key, doc)

    if not isinstance(doc, dict):
        return ()

    key_parts = key.split('.')
    if len(key_parts) == 1:
        return [doc.get(key, NOTHING)]

    sub_key = '.'.join(key_parts[1:])
    sub_doc = doc.get(key_parts[0], {})
    return iter_key_candidates(sub_key, sub_doc)
```
===== 11 =====
```
     if doc is None:
         return ()
 
-    if isinstance(doc, list):
+    if isinstance(doc, str):
         return _iter_key_candidates_sublist(key, doc)
 
     if not isinstance(doc, dict):
```
```
def iter_key_candidates(key, doc):
    """Get possible subdocuments or lists that are referred to by the key in question

    Returns the appropriate nested value if the key includes dot notation.
    """
    if not key:
        return [doc]

    if doc is None:
        return ()

    if isinstance(doc, str):
        return _iter_key_candidates_sublist(key, doc)

    if not isinstance(doc, dict):
        return ()

    key_parts = key.split('.')
    if len(key_parts) == 1:
        return [doc.get(key, NOTHING)]

    sub_key = '.'.join(key_parts[1:])
    sub_doc = doc.get(key_parts[0], {})
    return iter_key_candidates(sub_key, sub_doc)
```
===== 12 =====
```
     if doc is None:
         return ()
 
-    if isinstance(doc, list):
+    if not isinstance(doc, list):
         return _iter_key_candidates_sublist(key, doc)
 
     if not isinstance(doc, dict):
```
```
def iter_key_candidates(key, doc):
    """Get possible subdocuments or lists that are referred to by the key in question

    Returns the appropriate nested value if the key includes dot notation.
    """
    if not key:
        return [doc]

    if doc is None:
        return ()

    if not isinstance(doc, list):
        return _iter_key_candidates_sublist(key, doc)

    if not isinstance(doc, dict):
        return ()

    key_parts = key.split('.')
    if len(key_parts) == 1:
        return [doc.get(key, NOTHING)]

    sub_key = '.'.join(key_parts[1:])
    sub_doc = doc.get(key_parts[0], {})
    return iter_key_candidates(sub_key, sub_doc)
```
===== 13 =====
```
         return ()
 
     if isinstance(doc, list):
-        return _iter_key_candidates_sublist(key, doc)
+        return _iter_key_candidates_sublist(key, doc) if isinstance(doc, dict) else [NOTHING]
 
     if not isinstance(doc, dict):
         return ()
```
```
def iter_key_candidates(key, doc):
    """Get possible subdocuments or lists that are referred to by the key in question

    Returns the appropriate nested value if the key includes dot notation.
    """
    if not key:
        return [doc]

    if doc is None:
        return ()

    if isinstance(doc, list):
        return _iter_key_candidates_sublist(key, doc) if isinstance(doc, dict) else [NOTHING]

    if not isinstance(doc, dict):
        return ()

    key_parts = key.split('.')
    if len(key_parts) == 1:
        return [doc.get(key, NOTHING)]

    sub_key = '.'.join(key_parts[1:])
    sub_doc = doc.get(key_parts[0], {})
    return iter_key_candidates(sub_key, sub_doc)
```
===== 14 =====
```
         return ()
 
     if isinstance(doc, list):
-        return _iter_key_candidates_sublist(key, doc)
+        return _iter_key_candidates_sublist(key, doc) if key in doc else ()
 
     if not isinstance(doc, dict):
         return ()
```
```
def iter_key_candidates(key, doc):
    """Get possible subdocuments or lists that are referred to by the key in question

    Returns the appropriate nested value if the key includes dot notation.
    """
    if not key:
        return [doc]

    if doc is None:
        return ()

    if isinstance(doc, list):
        return _iter_key_candidates_sublist(key, doc) if key in doc else ()

    if not isinstance(doc, dict):
        return ()

    key_parts = key.split('.')
    if len(key_parts) == 1:
        return [doc.get(key, NOTHING)]

    sub_key = '.'.join(key_parts[1:])
    sub_doc = doc.get(key_parts[0], {})
    return iter_key_candidates(sub_key, sub_doc)
```
===== 15 =====
```
         return ()
 
     if isinstance(doc, list):
-        return _iter_key_candidates_sublist(key, doc)
+        return _iter_key_candidates_sublist(key, doc) if key.startswith('a') else ()
 
     if not isinstance(doc, dict):
         return ()
```
```
def iter_key_candidates(key, doc):
    """Get possible subdocuments or lists that are referred to by the key in question

    Returns the appropriate nested value if the key includes dot notation.
    """
    if not key:
        return [doc]

    if doc is None:
        return ()

    if isinstance(doc, list):
        return _iter_key_candidates_sublist(key, doc) if key.startswith('a') else ()

    if not isinstance(doc, dict):
        return ()

    key_parts = key.split('.')
    if len(key_parts) == 1:
        return [doc.get(key, NOTHING)]

    sub_key = '.'.join(key_parts[1:])
    sub_doc = doc.get(key_parts[0], {})
    return iter_key_candidates(sub_key, sub_doc)
```
===== 16 =====
```
     if isinstance(doc, list):
         return _iter_key_candidates_sublist(key, doc)
 
-    if not isinstance(doc, dict):
+    if isinstance(doc, dict):
         return ()
 
     key_parts = key.split('.')
@@ -21,4 +21,4 @@ 
     sub_key = '.'.join(key_parts[1:])
     sub_doc = doc.get(key_parts[0], {})
-    return iter_key_candidates(sub_key, sub_doc)+    return iter_key_candidates(sub_key, sub_doc)
```
```
def iter_key_candidates(key, doc):
    """Get possible subdocuments or lists that are referred to by the key in question

    Returns the appropriate nested value if the key includes dot notation.
    """
    if not key:
        return [doc]

    if doc is None:
        return ()

    if isinstance(doc, list):
        return _iter_key_candidates_sublist(key, doc)

    if isinstance(doc, dict):
        return ()

    key_parts = key.split('.')
    if len(key_parts) == 1:
        return [doc.get(key, NOTHING)]

    sub_key = '.'.join(key_parts[1:])
    sub_doc = doc.get(key_parts[0], {})
    return iter_key_candidates(sub_key, sub_doc)

```
===== 17 =====
```
     if isinstance(doc, list):
         return _iter_key_candidates_sublist(key, doc)
 
-    if not isinstance(doc, dict):
+    if not isinstance(None, dict):
         return ()
 
     key_parts = key.split('.')
@@ -21,4 +21,4 @@ 
     sub_key = '.'.join(key_parts[1:])
     sub_doc = doc.get(key_parts[0], {})
-    return iter_key_candidates(sub_key, sub_doc)+    return iter_key_candidates(sub_key, sub_doc)
```
```
def iter_key_candidates(key, doc):
    """Get possible subdocuments or lists that are referred to by the key in question

    Returns the appropriate nested value if the key includes dot notation.
    """
    if not key:
        return [doc]

    if doc is None:
        return ()

    if isinstance(doc, list):
        return _iter_key_candidates_sublist(key, doc)

    if not isinstance(None, dict):
        return ()

    key_parts = key.split('.')
    if len(key_parts) == 1:
        return [doc.get(key, NOTHING)]

    sub_key = '.'.join(key_parts[1:])
    sub_doc = doc.get(key_parts[0], {})
    return iter_key_candidates(sub_key, sub_doc)

```
===== 18 =====
```
     if not isinstance(doc, dict):
         return ()
 
-    key_parts = key.split('.')
+    key_parts = [key]  # Treats the entire key as a single element in a list
     if len(key_parts) == 1:
         return [doc.get(key, NOTHING)]
```
```
def iter_key_candidates(key, doc):
    """Get possible subdocuments or lists that are referred to by the key in question

    Returns the appropriate nested value if the key includes dot notation.
    """
    if not key:
        return [doc]

    if doc is None:
        return ()

    if isinstance(doc, list):
        return _iter_key_candidates_sublist(key, doc)

    if not isinstance(doc, dict):
        return ()

    key_parts = [key]  # Treats the entire key as a single element in a list
    if len(key_parts) == 1:
        return [doc.get(key, NOTHING)]

    sub_key = '.'.join(key_parts[1:])
    sub_doc = doc.get(key_parts[0], {})
    return iter_key_candidates(sub_key, sub_doc)
```
===== 19 =====
```
     if not isinstance(doc, dict):
         return ()
 
-    key_parts = key.split('.')
+    key_parts = key.split(',')  # Incorrectly splits by commas instead of dots
     if len(key_parts) == 1:
         return [doc.get(key, NOTHING)]
```
```
def iter_key_candidates(key, doc):
    """Get possible subdocuments or lists that are referred to by the key in question

    Returns the appropriate nested value if the key includes dot notation.
    """
    if not key:
        return [doc]

    if doc is None:
        return ()

    if isinstance(doc, list):
        return _iter_key_candidates_sublist(key, doc)

    if not isinstance(doc, dict):
        return ()

    key_parts = key.split(',')  # Incorrectly splits by commas instead of dots
    if len(key_parts) == 1:
        return [doc.get(key, NOTHING)]

    sub_key = '.'.join(key_parts[1:])
    sub_doc = doc.get(key_parts[0], {})
    return iter_key_candidates(sub_key, sub_doc)
```
===== 20 =====
```
     if not isinstance(doc, dict):
         return ()
 
-    key_parts = key.split('.')
+    key_parts = key.split('.')[::-1]  # Reverses the order of the key parts
     if len(key_parts) == 1:
         return [doc.get(key, NOTHING)]
```
```
def iter_key_candidates(key, doc):
    """Get possible subdocuments or lists that are referred to by the key in question

    Returns the appropriate nested value if the key includes dot notation.
    """
    if not key:
        return [doc]

    if doc is None:
        return ()

    if isinstance(doc, list):
        return _iter_key_candidates_sublist(key, doc)

    if not isinstance(doc, dict):
        return ()

    key_parts = key.split('.')[::-1]  # Reverses the order of the key parts
    if len(key_parts) == 1:
        return [doc.get(key, NOTHING)]

    sub_key = '.'.join(key_parts[1:])
    sub_doc = doc.get(key_parts[0], {})
    return iter_key_candidates(sub_key, sub_doc)
```
===== 21 =====
```
     if not isinstance(doc, dict):
         return ()
 
-    key_parts = key.split('.')
+    key_parts = key.split('XX.XX')
     if len(key_parts) == 1:
         return [doc.get(key, NOTHING)]
 
     sub_key = '.'.join(key_parts[1:])
     sub_doc = doc.get(key_parts[0], {})
-    return iter_key_candidates(sub_key, sub_doc)+    return iter_key_candidates(sub_key, sub_doc)
```
```
def iter_key_candidates(key, doc):
    """Get possible subdocuments or lists that are referred to by the key in question

    Returns the appropriate nested value if the key includes dot notation.
    """
    if not key:
        return [doc]

    if doc is None:
        return ()

    if isinstance(doc, list):
        return _iter_key_candidates_sublist(key, doc)

    if not isinstance(doc, dict):
        return ()

    key_parts = key.split('XX.XX')
    if len(key_parts) == 1:
        return [doc.get(key, NOTHING)]

    sub_key = '.'.join(key_parts[1:])
    sub_doc = doc.get(key_parts[0], {})
    return iter_key_candidates(sub_key, sub_doc)

```
===== 22 =====
```
     if not isinstance(doc, dict):
         return ()
 
-    key_parts = key.split('.')
+    key_parts = key.split(None)
     if len(key_parts) == 1:
         return [doc.get(key, NOTHING)]
 
     sub_key = '.'.join(key_parts[1:])
     sub_doc = doc.get(key_parts[0], {})
-    return iter_key_candidates(sub_key, sub_doc)+    return iter_key_candidates(sub_key, sub_doc)
```
```
def iter_key_candidates(key, doc):
    """Get possible subdocuments or lists that are referred to by the key in question

    Returns the appropriate nested value if the key includes dot notation.
    """
    if not key:
        return [doc]

    if doc is None:
        return ()

    if isinstance(doc, list):
        return _iter_key_candidates_sublist(key, doc)

    if not isinstance(doc, dict):
        return ()

    key_parts = key.split(None)
    if len(key_parts) == 1:
        return [doc.get(key, NOTHING)]

    sub_key = '.'.join(key_parts[1:])
    sub_doc = doc.get(key_parts[0], {})
    return iter_key_candidates(sub_key, sub_doc)

```
===== 23 =====
```
         return ()
 
     key_parts = key.split('.')
-    if len(key_parts) == 1:
+    if key_parts[0] != 'valid_key':
         return [doc.get(key, NOTHING)]
 
     sub_key = '.'.join(key_parts[1:])
```
```
def iter_key_candidates(key, doc):
    """Get possible subdocuments or lists that are referred to by the key in question

    Returns the appropriate nested value if the key includes dot notation.
    """
    if not key:
        return [doc]

    if doc is None:
        return ()

    if isinstance(doc, list):
        return _iter_key_candidates_sublist(key, doc)

    if not isinstance(doc, dict):
        return ()

    key_parts = key.split('.')
    if key_parts[0] != 'valid_key':
        return [doc.get(key, NOTHING)]

    sub_key = '.'.join(key_parts[1:])
    sub_doc = doc.get(key_parts[0], {})
    return iter_key_candidates(sub_key, sub_doc)
```
===== 24 =====
```
         return ()
 
     key_parts = key.split('.')
-    if len(key_parts) == 1:
+    if key_parts[0] == '':
         return [doc.get(key, NOTHING)]
 
     sub_key = '.'.join(key_parts[1:])
```
```
def iter_key_candidates(key, doc):
    """Get possible subdocuments or lists that are referred to by the key in question

    Returns the appropriate nested value if the key includes dot notation.
    """
    if not key:
        return [doc]

    if doc is None:
        return ()

    if isinstance(doc, list):
        return _iter_key_candidates_sublist(key, doc)

    if not isinstance(doc, dict):
        return ()

    key_parts = key.split('.')
    if key_parts[0] == '':
        return [doc.get(key, NOTHING)]

    sub_key = '.'.join(key_parts[1:])
    sub_doc = doc.get(key_parts[0], {})
    return iter_key_candidates(sub_key, sub_doc)
```
===== 25 =====
```
         return ()
 
     key_parts = key.split('.')
-    if len(key_parts) == 1:
+    if len(key_parts) != 1:
         return [doc.get(key, NOTHING)]
 
     sub_key = '.'.join(key_parts[1:])
     sub_doc = doc.get(key_parts[0], {})
-    return iter_key_candidates(sub_key, sub_doc)+    return iter_key_candidates(sub_key, sub_doc)
```
```
def iter_key_candidates(key, doc):
    """Get possible subdocuments or lists that are referred to by the key in question

    Returns the appropriate nested value if the key includes dot notation.
    """
    if not key:
        return [doc]

    if doc is None:
        return ()

    if isinstance(doc, list):
        return _iter_key_candidates_sublist(key, doc)

    if not isinstance(doc, dict):
        return ()

    key_parts = key.split('.')
    if len(key_parts) != 1:
        return [doc.get(key, NOTHING)]

    sub_key = '.'.join(key_parts[1:])
    sub_doc = doc.get(key_parts[0], {})
    return iter_key_candidates(sub_key, sub_doc)

```
===== 26 =====
```
         return ()
 
     key_parts = key.split('.')
-    if len(key_parts) == 1:
+    if len(key_parts) == 0:
         return [doc.get(key, NOTHING)]
 
     sub_key = '.'.join(key_parts[1:])
```
```
def iter_key_candidates(key, doc):
    """Get possible subdocuments or lists that are referred to by the key in question

    Returns the appropriate nested value if the key includes dot notation.
    """
    if not key:
        return [doc]

    if doc is None:
        return ()

    if isinstance(doc, list):
        return _iter_key_candidates_sublist(key, doc)

    if not isinstance(doc, dict):
        return ()

    key_parts = key.split('.')
    if len(key_parts) == 0:
        return [doc.get(key, NOTHING)]

    sub_key = '.'.join(key_parts[1:])
    sub_doc = doc.get(key_parts[0], {})
    return iter_key_candidates(sub_key, sub_doc)
```
===== 27 =====
```
         return ()
 
     key_parts = key.split('.')
-    if len(key_parts) == 1:
+    if len(key_parts) == 2:
         return [doc.get(key, NOTHING)]
 
     sub_key = '.'.join(key_parts[1:])
```
```
def iter_key_candidates(key, doc):
    """Get possible subdocuments or lists that are referred to by the key in question

    Returns the appropriate nested value if the key includes dot notation.
    """
    if not key:
        return [doc]

    if doc is None:
        return ()

    if isinstance(doc, list):
        return _iter_key_candidates_sublist(key, doc)

    if not isinstance(doc, dict):
        return ()

    key_parts = key.split('.')
    if len(key_parts) == 2:
        return [doc.get(key, NOTHING)]

    sub_key = '.'.join(key_parts[1:])
    sub_doc = doc.get(key_parts[0], {})
    return iter_key_candidates(sub_key, sub_doc)
```
===== 28 =====
```
         return ()
 
     key_parts = key.split('.')
-    if len(key_parts) == 1:
+    if len(key_parts) == 2:
         return [doc.get(key, NOTHING)]
 
     sub_key = '.'.join(key_parts[1:])
     sub_doc = doc.get(key_parts[0], {})
-    return iter_key_candidates(sub_key, sub_doc)+    return iter_key_candidates(sub_key, sub_doc)
```
```
def iter_key_candidates(key, doc):
    """Get possible subdocuments or lists that are referred to by the key in question

    Returns the appropriate nested value if the key includes dot notation.
    """
    if not key:
        return [doc]

    if doc is None:
        return ()

    if isinstance(doc, list):
        return _iter_key_candidates_sublist(key, doc)

    if not isinstance(doc, dict):
        return ()

    key_parts = key.split('.')
    if len(key_parts) == 2:
        return [doc.get(key, NOTHING)]

    sub_key = '.'.join(key_parts[1:])
    sub_doc = doc.get(key_parts[0], {})
    return iter_key_candidates(sub_key, sub_doc)

```
===== 29 =====
```
         return ()
 
     key_parts = key.split('.')
-    if len(key_parts) == 1:
+    if len(key_parts) > 1:
         return [doc.get(key, NOTHING)]
 
     sub_key = '.'.join(key_parts[1:])
```
```
def iter_key_candidates(key, doc):
    """Get possible subdocuments or lists that are referred to by the key in question

    Returns the appropriate nested value if the key includes dot notation.
    """
    if not key:
        return [doc]

    if doc is None:
        return ()

    if isinstance(doc, list):
        return _iter_key_candidates_sublist(key, doc)

    if not isinstance(doc, dict):
        return ()

    key_parts = key.split('.')
    if len(key_parts) > 1:
        return [doc.get(key, NOTHING)]

    sub_key = '.'.join(key_parts[1:])
    sub_doc = doc.get(key_parts[0], {})
    return iter_key_candidates(sub_key, sub_doc)
```
===== 30 =====
```
 
     key_parts = key.split('.')
     if len(key_parts) == 1:
-        return [doc.get(key, NOTHING)]
+        return [doc.get(NOTHING)]
 
     sub_key = '.'.join(key_parts[1:])
     sub_doc = doc.get(key_parts[0], {})
-    return iter_key_candidates(sub_key, sub_doc)+    return iter_key_candidates(sub_key, sub_doc)
```
```
def iter_key_candidates(key, doc):
    """Get possible subdocuments or lists that are referred to by the key in question

    Returns the appropriate nested value if the key includes dot notation.
    """
    if not key:
        return [doc]

    if doc is None:
        return ()

    if isinstance(doc, list):
        return _iter_key_candidates_sublist(key, doc)

    if not isinstance(doc, dict):
        return ()

    key_parts = key.split('.')
    if len(key_parts) == 1:
        return [doc.get(NOTHING)]

    sub_key = '.'.join(key_parts[1:])
    sub_doc = doc.get(key_parts[0], {})
    return iter_key_candidates(sub_key, sub_doc)

```
===== 31 =====
```
 
     key_parts = key.split('.')
     if len(key_parts) == 1:
-        return [doc.get(key, NOTHING)]
+        return [doc.get(None, NOTHING)]
 
     sub_key = '.'.join(key_parts[1:])
     sub_doc = doc.get(key_parts[0], {})
-    return iter_key_candidates(sub_key, sub_doc)+    return iter_key_candidates(sub_key, sub_doc)
```
```
def iter_key_candidates(key, doc):
    """Get possible subdocuments or lists that are referred to by the key in question

    Returns the appropriate nested value if the key includes dot notation.
    """
    if not key:
        return [doc]

    if doc is None:
        return ()

    if isinstance(doc, list):
        return _iter_key_candidates_sublist(key, doc)

    if not isinstance(doc, dict):
        return ()

    key_parts = key.split('.')
    if len(key_parts) == 1:
        return [doc.get(None, NOTHING)]

    sub_key = '.'.join(key_parts[1:])
    sub_doc = doc.get(key_parts[0], {})
    return iter_key_candidates(sub_key, sub_doc)

```
===== 32 =====
```
 
     key_parts = key.split('.')
     if len(key_parts) == 1:
-        return [doc.get(key, NOTHING)]
+        return [doc.get(key, 'default_value')]
 
     sub_key = '.'.join(key_parts[1:])
     sub_doc = doc.get(key_parts[0], {})
```
```
def iter_key_candidates(key, doc):
    """Get possible subdocuments or lists that are referred to by the key in question

    Returns the appropriate nested value if the key includes dot notation.
    """
    if not key:
        return [doc]

    if doc is None:
        return ()

    if isinstance(doc, list):
        return _iter_key_candidates_sublist(key, doc)

    if not isinstance(doc, dict):
        return ()

    key_parts = key.split('.')
    if len(key_parts) == 1:
        return [doc.get(key, 'default_value')]

    sub_key = '.'.join(key_parts[1:])
    sub_doc = doc.get(key_parts[0], {})
    return iter_key_candidates(sub_key, sub_doc)
```
===== 33 =====
```
 
     key_parts = key.split('.')
     if len(key_parts) == 1:
-        return [doc.get(key, NOTHING)]
+        return [doc.get(key, )]
 
     sub_key = '.'.join(key_parts[1:])
     sub_doc = doc.get(key_parts[0], {})
-    return iter_key_candidates(sub_key, sub_doc)+    return iter_key_candidates(sub_key, sub_doc)
```
```
def iter_key_candidates(key, doc):
    """Get possible subdocuments or lists that are referred to by the key in question

    Returns the appropriate nested value if the key includes dot notation.
    """
    if not key:
        return [doc]

    if doc is None:
        return ()

    if isinstance(doc, list):
        return _iter_key_candidates_sublist(key, doc)

    if not isinstance(doc, dict):
        return ()

    key_parts = key.split('.')
    if len(key_parts) == 1:
        return [doc.get(key, )]

    sub_key = '.'.join(key_parts[1:])
    sub_doc = doc.get(key_parts[0], {})
    return iter_key_candidates(sub_key, sub_doc)

```
===== 34 =====
```
 
     key_parts = key.split('.')
     if len(key_parts) == 1:
-        return [doc.get(key, NOTHING)]
+        return [doc.get(key, None)]
 
     sub_key = '.'.join(key_parts[1:])
     sub_doc = doc.get(key_parts[0], {})
```
```
def iter_key_candidates(key, doc):
    """Get possible subdocuments or lists that are referred to by the key in question

    Returns the appropriate nested value if the key includes dot notation.
    """
    if not key:
        return [doc]

    if doc is None:
        return ()

    if isinstance(doc, list):
        return _iter_key_candidates_sublist(key, doc)

    if not isinstance(doc, dict):
        return ()

    key_parts = key.split('.')
    if len(key_parts) == 1:
        return [doc.get(key, None)]

    sub_key = '.'.join(key_parts[1:])
    sub_doc = doc.get(key_parts[0], {})
    return iter_key_candidates(sub_key, sub_doc)
```
===== 35 =====
```
 
     key_parts = key.split('.')
     if len(key_parts) == 1:
-        return [doc.get(key, NOTHING)]
+        return [doc.get(key, None)]
 
     sub_key = '.'.join(key_parts[1:])
     sub_doc = doc.get(key_parts[0], {})
-    return iter_key_candidates(sub_key, sub_doc)+    return iter_key_candidates(sub_key, sub_doc)
```
```
def iter_key_candidates(key, doc):
    """Get possible subdocuments or lists that are referred to by the key in question

    Returns the appropriate nested value if the key includes dot notation.
    """
    if not key:
        return [doc]

    if doc is None:
        return ()

    if isinstance(doc, list):
        return _iter_key_candidates_sublist(key, doc)

    if not isinstance(doc, dict):
        return ()

    key_parts = key.split('.')
    if len(key_parts) == 1:
        return [doc.get(key, None)]

    sub_key = '.'.join(key_parts[1:])
    sub_doc = doc.get(key_parts[0], {})
    return iter_key_candidates(sub_key, sub_doc)

```
===== 36 =====
```
 
     key_parts = key.split('.')
     if len(key_parts) == 1:
-        return [doc.get(key, NOTHING)]
+        return [doc.get(key, {})]
 
     sub_key = '.'.join(key_parts[1:])
     sub_doc = doc.get(key_parts[0], {})
```
```
def iter_key_candidates(key, doc):
    """Get possible subdocuments or lists that are referred to by the key in question

    Returns the appropriate nested value if the key includes dot notation.
    """
    if not key:
        return [doc]

    if doc is None:
        return ()

    if isinstance(doc, list):
        return _iter_key_candidates_sublist(key, doc)

    if not isinstance(doc, dict):
        return ()

    key_parts = key.split('.')
    if len(key_parts) == 1:
        return [doc.get(key, {})]

    sub_key = '.'.join(key_parts[1:])
    sub_doc = doc.get(key_parts[0], {})
    return iter_key_candidates(sub_key, sub_doc)
```
===== 37 =====
```
 
     key_parts = key.split('.')
     if len(key_parts) == 1:
-        return [doc.get(key, NOTHING)]
+        return [doc[key]] if key in doc else []
 
     sub_key = '.'.join(key_parts[1:])
     sub_doc = doc.get(key_parts[0], {})
```
```
def iter_key_candidates(key, doc):
    """Get possible subdocuments or lists that are referred to by the key in question

    Returns the appropriate nested value if the key includes dot notation.
    """
    if not key:
        return [doc]

    if doc is None:
        return ()

    if isinstance(doc, list):
        return _iter_key_candidates_sublist(key, doc)

    if not isinstance(doc, dict):
        return ()

    key_parts = key.split('.')
    if len(key_parts) == 1:
        return [doc[key]] if key in doc else []

    sub_key = '.'.join(key_parts[1:])
    sub_doc = doc.get(key_parts[0], {})
    return iter_key_candidates(sub_key, sub_doc)
```
===== 38 =====
```
     if len(key_parts) == 1:
         return [doc.get(key, NOTHING)]
 
-    sub_key = '.'.join(key_parts[1:])
+    sub_key = '.'.join(key_parts[2:])
     sub_doc = doc.get(key_parts[0], {})
-    return iter_key_candidates(sub_key, sub_doc)+    return iter_key_candidates(sub_key, sub_doc)
```
```
def iter_key_candidates(key, doc):
    """Get possible subdocuments or lists that are referred to by the key in question

    Returns the appropriate nested value if the key includes dot notation.
    """
    if not key:
        return [doc]

    if doc is None:
        return ()

    if isinstance(doc, list):
        return _iter_key_candidates_sublist(key, doc)

    if not isinstance(doc, dict):
        return ()

    key_parts = key.split('.')
    if len(key_parts) == 1:
        return [doc.get(key, NOTHING)]

    sub_key = '.'.join(key_parts[2:])
    sub_doc = doc.get(key_parts[0], {})
    return iter_key_candidates(sub_key, sub_doc)

```
===== 39 =====
```
     if len(key_parts) == 1:
         return [doc.get(key, NOTHING)]
 
-    sub_key = '.'.join(key_parts[1:])
+    sub_key = 'XX.XX'.join(key_parts[1:])
     sub_doc = doc.get(key_parts[0], {})
-    return iter_key_candidates(sub_key, sub_doc)+    return iter_key_candidates(sub_key, sub_doc)
```
```
def iter_key_candidates(key, doc):
    """Get possible subdocuments or lists that are referred to by the key in question

    Returns the appropriate nested value if the key includes dot notation.
    """
    if not key:
        return [doc]

    if doc is None:
        return ()

    if isinstance(doc, list):
        return _iter_key_candidates_sublist(key, doc)

    if not isinstance(doc, dict):
        return ()

    key_parts = key.split('.')
    if len(key_parts) == 1:
        return [doc.get(key, NOTHING)]

    sub_key = 'XX.XX'.join(key_parts[1:])
    sub_doc = doc.get(key_parts[0], {})
    return iter_key_candidates(sub_key, sub_doc)

```
===== 40 =====
```
     if len(key_parts) == 1:
         return [doc.get(key, NOTHING)]
 
-    sub_key = '.'.join(key_parts[1:])
+    sub_key = None
     sub_doc = doc.get(key_parts[0], {})
-    return iter_key_candidates(sub_key, sub_doc)+    return iter_key_candidates(sub_key, sub_doc)
```
```
def iter_key_candidates(key, doc):
    """Get possible subdocuments or lists that are referred to by the key in question

    Returns the appropriate nested value if the key includes dot notation.
    """
    if not key:
        return [doc]

    if doc is None:
        return ()

    if isinstance(doc, list):
        return _iter_key_candidates_sublist(key, doc)

    if not isinstance(doc, dict):
        return ()

    key_parts = key.split('.')
    if len(key_parts) == 1:
        return [doc.get(key, NOTHING)]

    sub_key = None
    sub_doc = doc.get(key_parts[0], {})
    return iter_key_candidates(sub_key, sub_doc)

```
===== 41 =====
```
     if len(key_parts) == 1:
         return [doc.get(key, NOTHING)]
 
-    sub_key = '.'.join(key_parts[1:])
+    sub_key = key_parts[-1]  # Only takes the last part of the key
     sub_doc = doc.get(key_parts[0], {})
     return iter_key_candidates(sub_key, sub_doc)
```
```
def iter_key_candidates(key, doc):
    """Get possible subdocuments or lists that are referred to by the key in question

    Returns the appropriate nested value if the key includes dot notation.
    """
    if not key:
        return [doc]

    if doc is None:
        return ()

    if isinstance(doc, list):
        return _iter_key_candidates_sublist(key, doc)

    if not isinstance(doc, dict):
        return ()

    key_parts = key.split('.')
    if len(key_parts) == 1:
        return [doc.get(key, NOTHING)]

    sub_key = key_parts[-1]  # Only takes the last part of the key
    sub_doc = doc.get(key_parts[0], {})
    return iter_key_candidates(sub_key, sub_doc)
```
===== 42 =====
```
     if len(key_parts) == 1:
         return [doc.get(key, NOTHING)]
 
-    sub_key = '.'.join(key_parts[1:])
+    sub_key = key_parts[0]  # Incorrectly keeps the first part instead of the remainder
     sub_doc = doc.get(key_parts[0], {})
     return iter_key_candidates(sub_key, sub_doc)
```
```
def iter_key_candidates(key, doc):
    """Get possible subdocuments or lists that are referred to by the key in question

    Returns the appropriate nested value if the key includes dot notation.
    """
    if not key:
        return [doc]

    if doc is None:
        return ()

    if isinstance(doc, list):
        return _iter_key_candidates_sublist(key, doc)

    if not isinstance(doc, dict):
        return ()

    key_parts = key.split('.')
    if len(key_parts) == 1:
        return [doc.get(key, NOTHING)]

    sub_key = key_parts[0]  # Incorrectly keeps the first part instead of the remainder
    sub_doc = doc.get(key_parts[0], {})
    return iter_key_candidates(sub_key, sub_doc)
```
===== 43 =====
```
     if len(key_parts) == 1:
         return [doc.get(key, NOTHING)]
 
-    sub_key = '.'.join(key_parts[1:])
+    sub_key = key_parts[1] if len(key_parts) > 1 else ''
     sub_doc = doc.get(key_parts[0], {})
     return iter_key_candidates(sub_key, sub_doc)
```
```
def iter_key_candidates(key, doc):
    """Get possible subdocuments or lists that are referred to by the key in question

    Returns the appropriate nested value if the key includes dot notation.
    """
    if not key:
        return [doc]

    if doc is None:
        return ()

    if isinstance(doc, list):
        return _iter_key_candidates_sublist(key, doc)

    if not isinstance(doc, dict):
        return ()

    key_parts = key.split('.')
    if len(key_parts) == 1:
        return [doc.get(key, NOTHING)]

    sub_key = key_parts[1] if len(key_parts) > 1 else ''
    sub_doc = doc.get(key_parts[0], {})
    return iter_key_candidates(sub_key, sub_doc)
```
===== 44 =====
```
         return [doc.get(key, NOTHING)]
 
     sub_key = '.'.join(key_parts[1:])
-    sub_doc = doc.get(key_parts[0], {})
-    return iter_key_candidates(sub_key, sub_doc)+    sub_doc = None
+    return iter_key_candidates(sub_key, sub_doc)
```
```
def iter_key_candidates(key, doc):
    """Get possible subdocuments or lists that are referred to by the key in question

    Returns the appropriate nested value if the key includes dot notation.
    """
    if not key:
        return [doc]

    if doc is None:
        return ()

    if isinstance(doc, list):
        return _iter_key_candidates_sublist(key, doc)

    if not isinstance(doc, dict):
        return ()

    key_parts = key.split('.')
    if len(key_parts) == 1:
        return [doc.get(key, NOTHING)]

    sub_key = '.'.join(key_parts[1:])
    sub_doc = None
    return iter_key_candidates(sub_key, sub_doc)

```
===== 45 =====
```
         return [doc.get(key, NOTHING)]
 
     sub_key = '.'.join(key_parts[1:])
-    sub_doc = doc.get(key_parts[0], {})
-    return iter_key_candidates(sub_key, sub_doc)+    sub_doc = doc.get(None, {})
+    return iter_key_candidates(sub_key, sub_doc)
```
```
def iter_key_candidates(key, doc):
    """Get possible subdocuments or lists that are referred to by the key in question

    Returns the appropriate nested value if the key includes dot notation.
    """
    if not key:
        return [doc]

    if doc is None:
        return ()

    if isinstance(doc, list):
        return _iter_key_candidates_sublist(key, doc)

    if not isinstance(doc, dict):
        return ()

    key_parts = key.split('.')
    if len(key_parts) == 1:
        return [doc.get(key, NOTHING)]

    sub_key = '.'.join(key_parts[1:])
    sub_doc = doc.get(None, {})
    return iter_key_candidates(sub_key, sub_doc)

```
===== 46 =====
```
         return [doc.get(key, NOTHING)]
 
     sub_key = '.'.join(key_parts[1:])
-    sub_doc = doc.get(key_parts[0], {})
-    return iter_key_candidates(sub_key, sub_doc)+    sub_doc = doc.get(key_parts[0], )
+    return iter_key_candidates(sub_key, sub_doc)
```
```
def iter_key_candidates(key, doc):
    """Get possible subdocuments or lists that are referred to by the key in question

    Returns the appropriate nested value if the key includes dot notation.
    """
    if not key:
        return [doc]

    if doc is None:
        return ()

    if isinstance(doc, list):
        return _iter_key_candidates_sublist(key, doc)

    if not isinstance(doc, dict):
        return ()

    key_parts = key.split('.')
    if len(key_parts) == 1:
        return [doc.get(key, NOTHING)]

    sub_key = '.'.join(key_parts[1:])
    sub_doc = doc.get(key_parts[0], )
    return iter_key_candidates(sub_key, sub_doc)

```
===== 47 =====
```
         return [doc.get(key, NOTHING)]
 
     sub_key = '.'.join(key_parts[1:])
-    sub_doc = doc.get(key_parts[0], {})
+    sub_doc = doc.get(key_parts[0], NOTHING)
     return iter_key_candidates(sub_key, sub_doc)
```
```
def iter_key_candidates(key, doc):
    """Get possible subdocuments or lists that are referred to by the key in question

    Returns the appropriate nested value if the key includes dot notation.
    """
    if not key:
        return [doc]

    if doc is None:
        return ()

    if isinstance(doc, list):
        return _iter_key_candidates_sublist(key, doc)

    if not isinstance(doc, dict):
        return ()

    key_parts = key.split('.')
    if len(key_parts) == 1:
        return [doc.get(key, NOTHING)]

    sub_key = '.'.join(key_parts[1:])
    sub_doc = doc.get(key_parts[0], NOTHING)
    return iter_key_candidates(sub_key, sub_doc)
```
===== 48 =====
```
         return [doc.get(key, NOTHING)]
 
     sub_key = '.'.join(key_parts[1:])
-    sub_doc = doc.get(key_parts[0], {})
+    sub_doc = doc.get(key_parts[0], None)
     return iter_key_candidates(sub_key, sub_doc)
```
```
def iter_key_candidates(key, doc):
    """Get possible subdocuments or lists that are referred to by the key in question

    Returns the appropriate nested value if the key includes dot notation.
    """
    if not key:
        return [doc]

    if doc is None:
        return ()

    if isinstance(doc, list):
        return _iter_key_candidates_sublist(key, doc)

    if not isinstance(doc, dict):
        return ()

    key_parts = key.split('.')
    if len(key_parts) == 1:
        return [doc.get(key, NOTHING)]

    sub_key = '.'.join(key_parts[1:])
    sub_doc = doc.get(key_parts[0], None)
    return iter_key_candidates(sub_key, sub_doc)
```
===== 49 =====
```
         return [doc.get(key, NOTHING)]
 
     sub_key = '.'.join(key_parts[1:])
-    sub_doc = doc.get(key_parts[0], {})
-    return iter_key_candidates(sub_key, sub_doc)+    sub_doc = doc.get(key_parts[0], None)
+    return iter_key_candidates(sub_key, sub_doc)
```
```
def iter_key_candidates(key, doc):
    """Get possible subdocuments or lists that are referred to by the key in question

    Returns the appropriate nested value if the key includes dot notation.
    """
    if not key:
        return [doc]

    if doc is None:
        return ()

    if isinstance(doc, list):
        return _iter_key_candidates_sublist(key, doc)

    if not isinstance(doc, dict):
        return ()

    key_parts = key.split('.')
    if len(key_parts) == 1:
        return [doc.get(key, NOTHING)]

    sub_key = '.'.join(key_parts[1:])
    sub_doc = doc.get(key_parts[0], None)
    return iter_key_candidates(sub_key, sub_doc)

```
===== 50 =====
```
         return [doc.get(key, NOTHING)]
 
     sub_key = '.'.join(key_parts[1:])
-    sub_doc = doc.get(key_parts[0], {})
+    sub_doc = doc.get(key_parts[0], [])  # Defaulting to an empty list instead of a dict
     return iter_key_candidates(sub_key, sub_doc)
```
```
def iter_key_candidates(key, doc):
    """Get possible subdocuments or lists that are referred to by the key in question

    Returns the appropriate nested value if the key includes dot notation.
    """
    if not key:
        return [doc]

    if doc is None:
        return ()

    if isinstance(doc, list):
        return _iter_key_candidates_sublist(key, doc)

    if not isinstance(doc, dict):
        return ()

    key_parts = key.split('.')
    if len(key_parts) == 1:
        return [doc.get(key, NOTHING)]

    sub_key = '.'.join(key_parts[1:])
    sub_doc = doc.get(key_parts[0], [])  # Defaulting to an empty list instead of a dict
    return iter_key_candidates(sub_key, sub_doc)
```
===== 51 =====
```
         return [doc.get(key, NOTHING)]
 
     sub_key = '.'.join(key_parts[1:])
-    sub_doc = doc.get(key_parts[0], {})
-    return iter_key_candidates(sub_key, sub_doc)+    sub_doc = doc.get(key_parts[1], {})
+    return iter_key_candidates(sub_key, sub_doc)
```
```
def iter_key_candidates(key, doc):
    """Get possible subdocuments or lists that are referred to by the key in question

    Returns the appropriate nested value if the key includes dot notation.
    """
    if not key:
        return [doc]

    if doc is None:
        return ()

    if isinstance(doc, list):
        return _iter_key_candidates_sublist(key, doc)

    if not isinstance(doc, dict):
        return ()

    key_parts = key.split('.')
    if len(key_parts) == 1:
        return [doc.get(key, NOTHING)]

    sub_key = '.'.join(key_parts[1:])
    sub_doc = doc.get(key_parts[1], {})
    return iter_key_candidates(sub_key, sub_doc)

```
===== 52 =====
```
 
     sub_key = '.'.join(key_parts[1:])
     sub_doc = doc.get(key_parts[0], {})
-    return iter_key_candidates(sub_key, sub_doc)+    return [iter_key_candidates(sub_key, sub_doc)]
```
```
def iter_key_candidates(key, doc):
    """Get possible subdocuments or lists that are referred to by the key in question

    Returns the appropriate nested value if the key includes dot notation.
    """
    if not key:
        return [doc]

    if doc is None:
        return ()

    if isinstance(doc, list):
        return _iter_key_candidates_sublist(key, doc)

    if not isinstance(doc, dict):
        return ()

    key_parts = key.split('.')
    if len(key_parts) == 1:
        return [doc.get(key, NOTHING)]

    sub_key = '.'.join(key_parts[1:])
    sub_doc = doc.get(key_parts[0], {})
    return [iter_key_candidates(sub_key, sub_doc)]
```
===== 53 =====
```
 
     sub_key = '.'.join(key_parts[1:])
     sub_doc = doc.get(key_parts[0], {})
-    return iter_key_candidates(sub_key, sub_doc)+    return iter_key_candidates(None, sub_doc)
```
```
def iter_key_candidates(key, doc):
    """Get possible subdocuments or lists that are referred to by the key in question

    Returns the appropriate nested value if the key includes dot notation.
    """
    if not key:
        return [doc]

    if doc is None:
        return ()

    if isinstance(doc, list):
        return _iter_key_candidates_sublist(key, doc)

    if not isinstance(doc, dict):
        return ()

    key_parts = key.split('.')
    if len(key_parts) == 1:
        return [doc.get(key, NOTHING)]

    sub_key = '.'.join(key_parts[1:])
    sub_doc = doc.get(key_parts[0], {})
    return iter_key_candidates(None, sub_doc)

```
===== 54 =====
```
 
     sub_key = '.'.join(key_parts[1:])
     sub_doc = doc.get(key_parts[0], {})
-    return iter_key_candidates(sub_key, sub_doc)+    return iter_key_candidates(key_parts[0], sub_doc)
```
```
def iter_key_candidates(key, doc):
    """Get possible subdocuments or lists that are referred to by the key in question

    Returns the appropriate nested value if the key includes dot notation.
    """
    if not key:
        return [doc]

    if doc is None:
        return ()

    if isinstance(doc, list):
        return _iter_key_candidates_sublist(key, doc)

    if not isinstance(doc, dict):
        return ()

    key_parts = key.split('.')
    if len(key_parts) == 1:
        return [doc.get(key, NOTHING)]

    sub_key = '.'.join(key_parts[1:])
    sub_doc = doc.get(key_parts[0], {})
    return iter_key_candidates(key_parts[0], sub_doc)
```
===== 55 =====
```
 
     sub_key = '.'.join(key_parts[1:])
     sub_doc = doc.get(key_parts[0], {})
-    return iter_key_candidates(sub_key, sub_doc)+    return iter_key_candidates(sub_key, None)
```
```
def iter_key_candidates(key, doc):
    """Get possible subdocuments or lists that are referred to by the key in question

    Returns the appropriate nested value if the key includes dot notation.
    """
    if not key:
        return [doc]

    if doc is None:
        return ()

    if isinstance(doc, list):
        return _iter_key_candidates_sublist(key, doc)

    if not isinstance(doc, dict):
        return ()

    key_parts = key.split('.')
    if len(key_parts) == 1:
        return [doc.get(key, NOTHING)]

    sub_key = '.'.join(key_parts[1:])
    sub_doc = doc.get(key_parts[0], {})
    return iter_key_candidates(sub_key, None)

```
===== 56 =====
```
 
     sub_key = '.'.join(key_parts[1:])
     sub_doc = doc.get(key_parts[0], {})
-    return iter_key_candidates(sub_key, sub_doc)+    return iter_key_candidates(sub_key, doc)
```
```
def iter_key_candidates(key, doc):
    """Get possible subdocuments or lists that are referred to by the key in question

    Returns the appropriate nested value if the key includes dot notation.
    """
    if not key:
        return [doc]

    if doc is None:
        return ()

    if isinstance(doc, list):
        return _iter_key_candidates_sublist(key, doc)

    if not isinstance(doc, dict):
        return ()

    key_parts = key.split('.')
    if len(key_parts) == 1:
        return [doc.get(key, NOTHING)]

    sub_key = '.'.join(key_parts[1:])
    sub_doc = doc.get(key_parts[0], {})
    return iter_key_candidates(sub_key, doc)
```
===== 57 =====
```
 
     sub_key = '.'.join(key_parts[1:])
     sub_doc = doc.get(key_parts[0], {})
-    return iter_key_candidates(sub_key, sub_doc)+    return iter_key_candidates(sub_key, sub_doc) if isinstance(sub_doc, dict) else ()
```
```
def iter_key_candidates(key, doc):
    """Get possible subdocuments or lists that are referred to by the key in question

    Returns the appropriate nested value if the key includes dot notation.
    """
    if not key:
        return [doc]

    if doc is None:
        return ()

    if isinstance(doc, list):
        return _iter_key_candidates_sublist(key, doc)

    if not isinstance(doc, dict):
        return ()

    key_parts = key.split('.')
    if len(key_parts) == 1:
        return [doc.get(key, NOTHING)]

    sub_key = '.'.join(key_parts[1:])
    sub_doc = doc.get(key_parts[0], {})
    return iter_key_candidates(sub_key, sub_doc) if isinstance(sub_doc, dict) else ()
```
