https://github.com/kellyjonbrazil/jc/blob/9fd13e698709da95f5ee505ff1fde10564544d48/./jc/parsers/df.py#L174-L197
```
@icontract.snapshot(lambda header: header, name="old_header")
@icontract.snapshot(lambda line: line, name="old_line")
@icontract.ensure(lambda OLD, header: header == OLD.old_header)
@icontract.ensure(lambda OLD, line: line == OLD.old_line)
```
```
No direct verification.

Only evaluate object is local modified.
No restriction on return value.
```
passed
```
@icontract.snapshot(lambda header, line: line.split()[0], name="filesystem_expected")
@icontract.snapshot(lambda header, line: (len(header[10:]) - len(header[10:].lstrip(' '))) + 9, name="filesystem_col_len_expected")
@icontract.snapshot(lambda header, line: hashlib.sha256(line.split()[0].encode('utf-8')).hexdigest()[: (len(header[10:]) - len(header[10:].lstrip(' '))) + 9], name="filesystem_hash_expected")
@icontract.ensure(lambda OLD, result: (result == (None, None)) if len(OLD.filesystem_expected) <= OLD.filesystem_col_len_expected else result == (OLD.filesystem_hash_expected, OLD.filesystem_expected))
```
===== 17 =====
failed
```
     space_count = 0
     for char in header[10:]:
         if char == ' ':
-            space_count += 1
+            space_count -= 1
             continue
 
         break
@@ -21,4 +21,4 @@         truncated_hash = hashlib.sha256(filesystem_field.encode('utf-8')).hexdigest()[:filesystem_col_len]
         return truncated_hash, filesystem_field
 
-    return None, None+    return None, None
```
```
def _long_filesystem_hash(header, line):
    """
    Returns truncated hash and value of the filesystem field if it is too
    long for the column.
    """
    filesystem_field = line.split()[0]

    # get length of filesystem column
    space_count = 0
    for char in header[10:]:
        if char == ' ':
            space_count -= 1
            continue

        break

    filesystem_col_len = space_count + 9

    # return the hash and value if the field data is longer than the column length
    if len(filesystem_field) > filesystem_col_len:
        truncated_hash = hashlib.sha256(filesystem_field.encode('utf-8')).hexdigest()[:filesystem_col_len]
        return truncated_hash, filesystem_field

    return None, None

```
