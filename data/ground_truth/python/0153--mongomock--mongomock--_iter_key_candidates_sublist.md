https://github.com/mongomock/mongomock/blob/edd20d32254179c5373b81143a0bc2e7e7fe24a6/./mongomock/filtering.py#L252-L283
```
@icontract.snapshot(lambda key: key.split('.')[0], name="first")
@icontract.snapshot(lambda key: int(key.split('.')[0]) if key.split('.')[0].lstrip("+-").isdigit() else None, name="first_int")
@icontract.snapshot(lambda key: '.'.join(key.split('.')[1:]), name="key_remainder")
@icontract.ensure(lambda OLD, result, key, doc: (OLD.first_int is None) or (OLD.first_int >= len(doc) and result == ()) or (OLD.first_int is not None and OLD.first_int < len(doc) and result == iter_key_candidates(OLD.key_remainder, doc[OLD.first_int])))
@icontract.ensure(lambda OLD, result, key, doc: (OLD.first_int is not None) or (sum(1 for x in result if x is NOTHING) == sum(1 for sd in doc if isinstance(sd, dict) and OLD.first not in sd)))
@icontract.ensure(
    lambda OLD, result, key, doc:
        not isinstance(doc, list)
        or '.' in key
        or OLD.first_int is not None
        or result == [
            (sub_doc[OLD.first] if isinstance(sub_doc, dict) and OLD.first in sub_doc else NOTHING)
            for sub_doc in doc
            if isinstance(sub_doc, dict)
        ]
)
```
```
@icontract.snapshot(lambda key: key.split('.')[0], name="first")
@icontract.snapshot(lambda key: int(key.split('.')[0]) if key.split('.')[0].lstrip("+-").isdigit() else None, name="first_int")
@icontract.snapshot(lambda key: '.'.join(key.split('.')[1:]), name="key_remainder")
@icontract.ensure(lambda OLD, result, key, doc: (OLD.first_int is None) or (OLD.first_int >= len(doc) and result == ()) or (OLD.first_int is not None and OLD.first_int < len(doc) and result == iter_key_candidates(OLD.key_remainder, doc[OLD.first_int])))
@icontract.ensure(lambda OLD, result, key, doc: (OLD.first_int is not None) or (sum(1 for x in result if x is NOTHING) == sum(1 for sd in doc if isinstance(sd, dict) and OLD.first not in sd)))
```
[10, 21]
===== 10 =====
```
     """
     key_parts = key.split('.')
     sub_key = key_parts.pop(0)
-    key_remainder = '.'.join(key_parts)
+    key_remainder = key_parts + ['extra']  # Adds an extra part to the key
     try:
         sub_key_int = int(sub_key)
     except ValueError:
```
```
def _iter_key_candidates_sublist(key, doc):
    """Iterates of candidates

    :param doc: a list to be searched for candidates for our key
    :param key: the string key to be matched
    """
    key_parts = key.split('.')
    sub_key = key_parts.pop(0)
    key_remainder = key_parts + ['extra']  # Adds an extra part to the key
    try:
        sub_key_int = int(sub_key)
    except ValueError:
        sub_key_int = None

    if sub_key_int is None:
        # subkey is not an integer...
        ret = []
        for sub_doc in doc:
            if isinstance(sub_doc, dict):
                if sub_key in sub_doc:
                    ret.extend(iter_key_candidates(key_remainder, sub_doc[sub_key]))
                else:
                    ret.append(NOTHING)
        return ret

    # subkey is an index
    if sub_key_int >= len(doc):
        return ()  # dead end
    sub_doc = doc[sub_key_int]
    if key_parts:
        return iter_key_candidates('.'.join(key_parts), sub_doc)
    return [sub_doc]
```
===== 21 =====
```
         for sub_doc in doc:
             if isinstance(sub_doc, dict):
                 if sub_key in sub_doc:
-                    ret.extend(iter_key_candidates(key_remainder, sub_doc[sub_key]))
+                    ret.extend(iter_key_candidates(key_remainder, None))
                 else:
                     ret.append(NOTHING)
         return ret
@@ -29,4 +29,4 @@     sub_doc = doc[sub_key_int]
     if key_parts:
         return iter_key_candidates('.'.join(key_parts), sub_doc)
-    return [sub_doc]+    return [sub_doc]
```
```
def _iter_key_candidates_sublist(key, doc):
    """Iterates of candidates

    :param doc: a list to be searched for candidates for our key
    :param key: the string key to be matched
    """
    key_parts = key.split('.')
    sub_key = key_parts.pop(0)
    key_remainder = '.'.join(key_parts)
    try:
        sub_key_int = int(sub_key)
    except ValueError:
        sub_key_int = None

    if sub_key_int is None:
        # subkey is not an integer...
        ret = []
        for sub_doc in doc:
            if isinstance(sub_doc, dict):
                if sub_key in sub_doc:
                    ret.extend(iter_key_candidates(key_remainder, None))
                else:
                    ret.append(NOTHING)
        return ret

    # subkey is an index
    if sub_key_int >= len(doc):
        return ()  # dead end
    sub_doc = doc[sub_key_int]
    if key_parts:
        return iter_key_candidates('.'.join(key_parts), sub_doc)
    return [sub_doc]

```
