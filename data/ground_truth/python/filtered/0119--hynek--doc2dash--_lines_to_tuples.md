https://github.com/hynek/doc2dash/blob/a5fc14a6ee151eb1373733bed8d5f9adb2189795/./src/doc2dash/parsers/intersphinx_inventory.py#L85-L111
```
🈚️

Timeout

@icontract.ensure(
    lambda result, check_exists, entries:
        result
        == {
            # 外层：role -> { name -> (uri, display_name) }
            role: {
                name: (uri2, display_name)
                # 这层从所有“合法、且文件存在”的条目中筛出当前 role 的项
                for (role2, name, uri2, display_name) in (
                    # 生成所有“合法、且文件存在”的条目：
                    # (role, name, cleaned_uri, display_name)
                    (
                        m.groups()[1],           # role
                        m.groups()[0],           # name
                        path_uri[1],             # cleaned_uri
                        m.groups()[3],           # display_name
                    )
                    for line in entries
                    # 先按 Sphinx 的格式解析行
                    for m in (_match_inv_line(line.rstrip()),)
                    if m is not None
                    # 处理 "$" 占位符并 clean up path
                    for path_uri in (
                        _clean_up_path(
                            m.groups()[2].replace("$", m.groups()[0])
                        ),
                    )
                    # 只保留 check_exists(path) 为 True 的
                    if check_exists(path_uri[0])
                )
                if role2 == role
            }
            # 外层 role 的全集：所有合法、存在的条目里的全部 role
            for role in {
                role3
                for (role3, name3, uri3, display_name3) in (
                    (
                        m.groups()[1],           # role
                        m.groups()[0],           # name
                        path_uri[1],             # cleaned_uri
                        m.groups()[3],           # display_name
                    )
                    for line in entries
                    for m in (_match_inv_line(line.rstrip()),)
                    if m is not None
                    for path_uri in (
                        _clean_up_path(
                            m.groups()[2].replace("$", m.groups()[0])
                        ),
                    )
                    if check_exists(path_uri[0])
                )
            }
        }
)
```
```
None
```
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25]
===== 0 =====
```
     """
     rv: Mapping[str, dict[str, tuple[str, str]]] = defaultdict(dict)
 
-    for line in entries:
+    for line in entries[1:]:  # Skips the first entry, which may contain important metadata
         m = _match_inv_line(line.rstrip())
         if not m:
             log.warning("intersphinx: invalid line: %r. Skipping.", line)
```
```
def _lines_to_tuples(
    check_exists: Callable[[str], bool], entries: list[str]
) -> Mapping[str, dict[str, tuple[str, str]]]:
    """
    Transform inventory lines *entries* to the required dict of dicts of
    tuples.

    Use *check_exists* callable to verify whether the indexed path exits at
    all.
    """
    rv: Mapping[str, dict[str, tuple[str, str]]] = defaultdict(dict)

    for line in entries[1:]:  # Skips the first entry, which may contain important metadata
        m = _match_inv_line(line.rstrip())
        if not m:
            log.warning("intersphinx: invalid line: %r. Skipping.", line)
            continue

        name, role, uri, display_name = m.groups()
        path, uri = _clean_up_path(uri.replace("$", name))

        if not check_exists(path):
            continue

        rv[role][name] = (uri, display_name)

    return rv
```
===== 1 =====
```
     """
     rv: Mapping[str, dict[str, tuple[str, str]]] = defaultdict(dict)
 
-    for line in entries:
+    for line in entries[:-1]:  # Skips the last entry, potentially missing data
         m = _match_inv_line(line.rstrip())
         if not m:
             log.warning("intersphinx: invalid line: %r. Skipping.", line)
```
```
def _lines_to_tuples(
    check_exists: Callable[[str], bool], entries: list[str]
) -> Mapping[str, dict[str, tuple[str, str]]]:
    """
    Transform inventory lines *entries* to the required dict of dicts of
    tuples.

    Use *check_exists* callable to verify whether the indexed path exits at
    all.
    """
    rv: Mapping[str, dict[str, tuple[str, str]]] = defaultdict(dict)

    for line in entries[:-1]:  # Skips the last entry, potentially missing data
        m = _match_inv_line(line.rstrip())
        if not m:
            log.warning("intersphinx: invalid line: %r. Skipping.", line)
            continue

        name, role, uri, display_name = m.groups()
        path, uri = _clean_up_path(uri.replace("$", name))

        if not check_exists(path):
            continue

        rv[role][name] = (uri, display_name)

    return rv
```
===== 2 =====
```
     rv: Mapping[str, dict[str, tuple[str, str]]] = defaultdict(dict)
 
     for line in entries:
-        m = _match_inv_line(line.rstrip())
+        m = None
         if not m:
             log.warning("intersphinx: invalid line: %r. Skipping.", line)
             continue
@@ -24,4 +24,4 @@ 
         rv[role][name] = (uri, display_name)
 
-    return rv+    return rv
```
```
def _lines_to_tuples(
    check_exists: Callable[[str], bool], entries: list[str]
) -> Mapping[str, dict[str, tuple[str, str]]]:
    """
    Transform inventory lines *entries* to the required dict of dicts of
    tuples.

    Use *check_exists* callable to verify whether the indexed path exits at
    all.
    """
    rv: Mapping[str, dict[str, tuple[str, str]]] = defaultdict(dict)

    for line in entries:
        m = None
        if not m:
            log.warning("intersphinx: invalid line: %r. Skipping.", line)
            continue

        name, role, uri, display_name = m.groups()
        path, uri = _clean_up_path(uri.replace("$", name))

        if not check_exists(path):
            continue

        rv[role][name] = (uri, display_name)

    return rv

```
===== 3 =====
```
     rv: Mapping[str, dict[str, tuple[str, str]]] = defaultdict(dict)
 
     for line in entries:
-        m = _match_inv_line(line.rstrip())
+        m = _match_inv_line(line.rstrip().lower())  # Lowercasing the line may cause case sensitivity issues
         if not m:
             log.warning("intersphinx: invalid line: %r. Skipping.", line)
             continue
```
```
def _lines_to_tuples(
    check_exists: Callable[[str], bool], entries: list[str]
) -> Mapping[str, dict[str, tuple[str, str]]]:
    """
    Transform inventory lines *entries* to the required dict of dicts of
    tuples.

    Use *check_exists* callable to verify whether the indexed path exits at
    all.
    """
    rv: Mapping[str, dict[str, tuple[str, str]]] = defaultdict(dict)

    for line in entries:
        m = _match_inv_line(line.rstrip().lower())  # Lowercasing the line may cause case sensitivity issues
        if not m:
            log.warning("intersphinx: invalid line: %r. Skipping.", line)
            continue

        name, role, uri, display_name = m.groups()
        path, uri = _clean_up_path(uri.replace("$", name))

        if not check_exists(path):
            continue

        rv[role][name] = (uri, display_name)

    return rv
```
===== 4 =====
```
     rv: Mapping[str, dict[str, tuple[str, str]]] = defaultdict(dict)
 
     for line in entries:
-        m = _match_inv_line(line.rstrip())
+        m = _match_inv_line(line.rstrip().replace(" ", "_"))  # Replacing spaces with underscores will break the expected format
         if not m:
             log.warning("intersphinx: invalid line: %r. Skipping.", line)
             continue
```
```
def _lines_to_tuples(
    check_exists: Callable[[str], bool], entries: list[str]
) -> Mapping[str, dict[str, tuple[str, str]]]:
    """
    Transform inventory lines *entries* to the required dict of dicts of
    tuples.

    Use *check_exists* callable to verify whether the indexed path exits at
    all.
    """
    rv: Mapping[str, dict[str, tuple[str, str]]] = defaultdict(dict)

    for line in entries:
        m = _match_inv_line(line.rstrip().replace(" ", "_"))  # Replacing spaces with underscores will break the expected format
        if not m:
            log.warning("intersphinx: invalid line: %r. Skipping.", line)
            continue

        name, role, uri, display_name = m.groups()
        path, uri = _clean_up_path(uri.replace("$", name))

        if not check_exists(path):
            continue

        rv[role][name] = (uri, display_name)

    return rv
```
===== 5 =====
```
     for line in entries:
         m = _match_inv_line(line.rstrip())
         if not m:
-            log.warning("intersphinx: invalid line: %r. Skipping.", line)
+            log.debug("Line is not valid: %r", line)
             continue
 
         name, role, uri, display_name = m.groups()
```
```
def _lines_to_tuples(
    check_exists: Callable[[str], bool], entries: list[str]
) -> Mapping[str, dict[str, tuple[str, str]]]:
    """
    Transform inventory lines *entries* to the required dict of dicts of
    tuples.

    Use *check_exists* callable to verify whether the indexed path exits at
    all.
    """
    rv: Mapping[str, dict[str, tuple[str, str]]] = defaultdict(dict)

    for line in entries:
        m = _match_inv_line(line.rstrip())
        if not m:
            log.debug("Line is not valid: %r", line)
            continue

        name, role, uri, display_name = m.groups()
        path, uri = _clean_up_path(uri.replace("$", name))

        if not check_exists(path):
            continue

        rv[role][name] = (uri, display_name)

    return rv
```
===== 6 =====
```
     for line in entries:
         m = _match_inv_line(line.rstrip())
         if not m:
-            log.warning("intersphinx: invalid line: %r. Skipping.", line)
+            log.error("Invalid line encountered: %r", line)
             continue
 
         name, role, uri, display_name = m.groups()
```
```
def _lines_to_tuples(
    check_exists: Callable[[str], bool], entries: list[str]
) -> Mapping[str, dict[str, tuple[str, str]]]:
    """
    Transform inventory lines *entries* to the required dict of dicts of
    tuples.

    Use *check_exists* callable to verify whether the indexed path exits at
    all.
    """
    rv: Mapping[str, dict[str, tuple[str, str]]] = defaultdict(dict)

    for line in entries:
        m = _match_inv_line(line.rstrip())
        if not m:
            log.error("Invalid line encountered: %r", line)
            continue

        name, role, uri, display_name = m.groups()
        path, uri = _clean_up_path(uri.replace("$", name))

        if not check_exists(path):
            continue

        rv[role][name] = (uri, display_name)

    return rv
```
===== 7 =====
```
     for line in entries:
         m = _match_inv_line(line.rstrip())
         if not m:
-            log.warning("intersphinx: invalid line: %r. Skipping.", line)
+            log.info("Skipping invalid line: %r", line)
             continue
 
         name, role, uri, display_name = m.groups()
```
```
def _lines_to_tuples(
    check_exists: Callable[[str], bool], entries: list[str]
) -> Mapping[str, dict[str, tuple[str, str]]]:
    """
    Transform inventory lines *entries* to the required dict of dicts of
    tuples.

    Use *check_exists* callable to verify whether the indexed path exits at
    all.
    """
    rv: Mapping[str, dict[str, tuple[str, str]]] = defaultdict(dict)

    for line in entries:
        m = _match_inv_line(line.rstrip())
        if not m:
            log.info("Skipping invalid line: %r", line)
            continue

        name, role, uri, display_name = m.groups()
        path, uri = _clean_up_path(uri.replace("$", name))

        if not check_exists(path):
            continue

        rv[role][name] = (uri, display_name)

    return rv
```
===== 8 =====
```
     for line in entries:
         m = _match_inv_line(line.rstrip())
         if not m:
-            log.warning("intersphinx: invalid line: %r. Skipping.", line)
+            log.warning("Ignoring line: %r", line)
             continue
 
         name, role, uri, display_name = m.groups()
```
```
def _lines_to_tuples(
    check_exists: Callable[[str], bool], entries: list[str]
) -> Mapping[str, dict[str, tuple[str, str]]]:
    """
    Transform inventory lines *entries* to the required dict of dicts of
    tuples.

    Use *check_exists* callable to verify whether the indexed path exits at
    all.
    """
    rv: Mapping[str, dict[str, tuple[str, str]]] = defaultdict(dict)

    for line in entries:
        m = _match_inv_line(line.rstrip())
        if not m:
            log.warning("Ignoring line: %r", line)
            continue

        name, role, uri, display_name = m.groups()
        path, uri = _clean_up_path(uri.replace("$", name))

        if not check_exists(path):
            continue

        rv[role][name] = (uri, display_name)

    return rv
```
===== 9 =====
```
     for line in entries:
         m = _match_inv_line(line.rstrip())
         if not m:
-            log.warning("intersphinx: invalid line: %r. Skipping.", line)
+            log.warning("Malformed line: %r", line)  # This could be misleading
             continue
 
         name, role, uri, display_name = m.groups()
```
```
def _lines_to_tuples(
    check_exists: Callable[[str], bool], entries: list[str]
) -> Mapping[str, dict[str, tuple[str, str]]]:
    """
    Transform inventory lines *entries* to the required dict of dicts of
    tuples.

    Use *check_exists* callable to verify whether the indexed path exits at
    all.
    """
    rv: Mapping[str, dict[str, tuple[str, str]]] = defaultdict(dict)

    for line in entries:
        m = _match_inv_line(line.rstrip())
        if not m:
            log.warning("Malformed line: %r", line)  # This could be misleading
            continue

        name, role, uri, display_name = m.groups()
        path, uri = _clean_up_path(uri.replace("$", name))

        if not check_exists(path):
            continue

        rv[role][name] = (uri, display_name)

    return rv
```
===== 10 =====
```
     for line in entries:
         m = _match_inv_line(line.rstrip())
         if not m:
-            log.warning("intersphinx: invalid line: %r. Skipping.", line)
+            log.warning("XXintersphinx: invalid line: %r. Skipping.XX", line)
             continue
 
         name, role, uri, display_name = m.groups()
@@ -24,4 +24,4 @@ 
         rv[role][name] = (uri, display_name)
 
-    return rv+    return rv
```
```
def _lines_to_tuples(
    check_exists: Callable[[str], bool], entries: list[str]
) -> Mapping[str, dict[str, tuple[str, str]]]:
    """
    Transform inventory lines *entries* to the required dict of dicts of
    tuples.

    Use *check_exists* callable to verify whether the indexed path exits at
    all.
    """
    rv: Mapping[str, dict[str, tuple[str, str]]] = defaultdict(dict)

    for line in entries:
        m = _match_inv_line(line.rstrip())
        if not m:
            log.warning("XXintersphinx: invalid line: %r. Skipping.XX", line)
            continue

        name, role, uri, display_name = m.groups()
        path, uri = _clean_up_path(uri.replace("$", name))

        if not check_exists(path):
            continue

        rv[role][name] = (uri, display_name)

    return rv

```
===== 11 =====
```
     for line in entries:
         m = _match_inv_line(line.rstrip())
         if not m:
-            log.warning("intersphinx: invalid line: %r. Skipping.", line)
+            log.warning("intersphinx: invalid line: %r. Skipping.", )
             continue
 
         name, role, uri, display_name = m.groups()
@@ -24,4 +24,4 @@ 
         rv[role][name] = (uri, display_name)
 
-    return rv+    return rv
```
```
def _lines_to_tuples(
    check_exists: Callable[[str], bool], entries: list[str]
) -> Mapping[str, dict[str, tuple[str, str]]]:
    """
    Transform inventory lines *entries* to the required dict of dicts of
    tuples.

    Use *check_exists* callable to verify whether the indexed path exits at
    all.
    """
    rv: Mapping[str, dict[str, tuple[str, str]]] = defaultdict(dict)

    for line in entries:
        m = _match_inv_line(line.rstrip())
        if not m:
            log.warning("intersphinx: invalid line: %r. Skipping.", )
            continue

        name, role, uri, display_name = m.groups()
        path, uri = _clean_up_path(uri.replace("$", name))

        if not check_exists(path):
            continue

        rv[role][name] = (uri, display_name)

    return rv

```
===== 12 =====
```
     for line in entries:
         m = _match_inv_line(line.rstrip())
         if not m:
-            log.warning("intersphinx: invalid line: %r. Skipping.", line)
+            log.warning("intersphinx: invalid line: %r. Skipping.", None)
             continue
 
         name, role, uri, display_name = m.groups()
@@ -24,4 +24,4 @@ 
         rv[role][name] = (uri, display_name)
 
-    return rv+    return rv
```
```
def _lines_to_tuples(
    check_exists: Callable[[str], bool], entries: list[str]
) -> Mapping[str, dict[str, tuple[str, str]]]:
    """
    Transform inventory lines *entries* to the required dict of dicts of
    tuples.

    Use *check_exists* callable to verify whether the indexed path exits at
    all.
    """
    rv: Mapping[str, dict[str, tuple[str, str]]] = defaultdict(dict)

    for line in entries:
        m = _match_inv_line(line.rstrip())
        if not m:
            log.warning("intersphinx: invalid line: %r. Skipping.", None)
            continue

        name, role, uri, display_name = m.groups()
        path, uri = _clean_up_path(uri.replace("$", name))

        if not check_exists(path):
            continue

        rv[role][name] = (uri, display_name)

    return rv

```
===== 13 =====
```
     for line in entries:
         m = _match_inv_line(line.rstrip())
         if not m:
-            log.warning("intersphinx: invalid line: %r. Skipping.", line)
+            log.warning("intersphinx: invalid line: %r. skipping.", line)
             continue
 
         name, role, uri, display_name = m.groups()
@@ -24,4 +24,4 @@ 
         rv[role][name] = (uri, display_name)
 
-    return rv+    return rv
```
```
def _lines_to_tuples(
    check_exists: Callable[[str], bool], entries: list[str]
) -> Mapping[str, dict[str, tuple[str, str]]]:
    """
    Transform inventory lines *entries* to the required dict of dicts of
    tuples.

    Use *check_exists* callable to verify whether the indexed path exits at
    all.
    """
    rv: Mapping[str, dict[str, tuple[str, str]]] = defaultdict(dict)

    for line in entries:
        m = _match_inv_line(line.rstrip())
        if not m:
            log.warning("intersphinx: invalid line: %r. skipping.", line)
            continue

        name, role, uri, display_name = m.groups()
        path, uri = _clean_up_path(uri.replace("$", name))

        if not check_exists(path):
            continue

        rv[role][name] = (uri, display_name)

    return rv

```
===== 14 =====
```
     for line in entries:
         m = _match_inv_line(line.rstrip())
         if not m:
-            log.warning("intersphinx: invalid line: %r. Skipping.", line)
+            log.warning(line)
             continue
 
         name, role, uri, display_name = m.groups()
@@ -24,4 +24,4 @@ 
         rv[role][name] = (uri, display_name)
 
-    return rv+    return rv
```
```
def _lines_to_tuples(
    check_exists: Callable[[str], bool], entries: list[str]
) -> Mapping[str, dict[str, tuple[str, str]]]:
    """
    Transform inventory lines *entries* to the required dict of dicts of
    tuples.

    Use *check_exists* callable to verify whether the indexed path exits at
    all.
    """
    rv: Mapping[str, dict[str, tuple[str, str]]] = defaultdict(dict)

    for line in entries:
        m = _match_inv_line(line.rstrip())
        if not m:
            log.warning(line)
            continue

        name, role, uri, display_name = m.groups()
        path, uri = _clean_up_path(uri.replace("$", name))

        if not check_exists(path):
            continue

        rv[role][name] = (uri, display_name)

    return rv

```
===== 15 =====
```
             continue
 
         name, role, uri, display_name = m.groups()
-        path, uri = _clean_up_path(uri.replace("$", name))
+        path, uri = _clean_up_path(uri)  # Missing replacement of "$" with name
 
         if not check_exists(path):
             continue
```
```
def _lines_to_tuples(
    check_exists: Callable[[str], bool], entries: list[str]
) -> Mapping[str, dict[str, tuple[str, str]]]:
    """
    Transform inventory lines *entries* to the required dict of dicts of
    tuples.

    Use *check_exists* callable to verify whether the indexed path exits at
    all.
    """
    rv: Mapping[str, dict[str, tuple[str, str]]] = defaultdict(dict)

    for line in entries:
        m = _match_inv_line(line.rstrip())
        if not m:
            log.warning("intersphinx: invalid line: %r. Skipping.", line)
            continue

        name, role, uri, display_name = m.groups()
        path, uri = _clean_up_path(uri)  # Missing replacement of "$" with name

        if not check_exists(path):
            continue

        rv[role][name] = (uri, display_name)

    return rv
```
===== 16 =====
```
             continue
 
         name, role, uri, display_name = m.groups()
-        path, uri = _clean_up_path(uri.replace("$", name))
+        path, uri = _clean_up_path(uri.replace("$", ""))  # Incorrectly replacing "$" with an empty string
 
         if not check_exists(path):
             continue
```
```
def _lines_to_tuples(
    check_exists: Callable[[str], bool], entries: list[str]
) -> Mapping[str, dict[str, tuple[str, str]]]:
    """
    Transform inventory lines *entries* to the required dict of dicts of
    tuples.

    Use *check_exists* callable to verify whether the indexed path exits at
    all.
    """
    rv: Mapping[str, dict[str, tuple[str, str]]] = defaultdict(dict)

    for line in entries:
        m = _match_inv_line(line.rstrip())
        if not m:
            log.warning("intersphinx: invalid line: %r. Skipping.", line)
            continue

        name, role, uri, display_name = m.groups()
        path, uri = _clean_up_path(uri.replace("$", ""))  # Incorrectly replacing "$" with an empty string

        if not check_exists(path):
            continue

        rv[role][name] = (uri, display_name)

    return rv
```
===== 17 =====
```
             continue
 
         name, role, uri, display_name = m.groups()
-        path, uri = _clean_up_path(uri.replace("$", name))
+        path, uri = _clean_up_path(uri.replace("$", f"{name}_suffix"))  # Incorrectly appending a suffix to name instead of replacing
 
         if not check_exists(path):
             continue
```
```
def _lines_to_tuples(
    check_exists: Callable[[str], bool], entries: list[str]
) -> Mapping[str, dict[str, tuple[str, str]]]:
    """
    Transform inventory lines *entries* to the required dict of dicts of
    tuples.

    Use *check_exists* callable to verify whether the indexed path exits at
    all.
    """
    rv: Mapping[str, dict[str, tuple[str, str]]] = defaultdict(dict)

    for line in entries:
        m = _match_inv_line(line.rstrip())
        if not m:
            log.warning("intersphinx: invalid line: %r. Skipping.", line)
            continue

        name, role, uri, display_name = m.groups()
        path, uri = _clean_up_path(uri.replace("$", f"{name}_suffix"))  # Incorrectly appending a suffix to name instead of replacing

        if not check_exists(path):
            continue

        rv[role][name] = (uri, display_name)

    return rv
```
===== 18 =====
```
             continue
 
         name, role, uri, display_name = m.groups()
-        path, uri = _clean_up_path(uri.replace("$", name))
+        path, uri = _clean_up_path(uri.replace("$", name.upper()))  # Replacing "$" with the uppercase version of name
 
         if not check_exists(path):
             continue
```
```
def _lines_to_tuples(
    check_exists: Callable[[str], bool], entries: list[str]
) -> Mapping[str, dict[str, tuple[str, str]]]:
    """
    Transform inventory lines *entries* to the required dict of dicts of
    tuples.

    Use *check_exists* callable to verify whether the indexed path exits at
    all.
    """
    rv: Mapping[str, dict[str, tuple[str, str]]] = defaultdict(dict)

    for line in entries:
        m = _match_inv_line(line.rstrip())
        if not m:
            log.warning("intersphinx: invalid line: %r. Skipping.", line)
            continue

        name, role, uri, display_name = m.groups()
        path, uri = _clean_up_path(uri.replace("$", name.upper()))  # Replacing "$" with the uppercase version of name

        if not check_exists(path):
            continue

        rv[role][name] = (uri, display_name)

    return rv
```
===== 19 =====
```
             continue
 
         name, role, uri, display_name = m.groups()
-        path, uri = _clean_up_path(uri.replace("$", name))
+        path, uri = _clean_up_path(uri.replace("$", name[::-1]))  # Replacing "$" with the reversed version of name
 
         if not check_exists(path):
             continue
```
```
def _lines_to_tuples(
    check_exists: Callable[[str], bool], entries: list[str]
) -> Mapping[str, dict[str, tuple[str, str]]]:
    """
    Transform inventory lines *entries* to the required dict of dicts of
    tuples.

    Use *check_exists* callable to verify whether the indexed path exits at
    all.
    """
    rv: Mapping[str, dict[str, tuple[str, str]]] = defaultdict(dict)

    for line in entries:
        m = _match_inv_line(line.rstrip())
        if not m:
            log.warning("intersphinx: invalid line: %r. Skipping.", line)
            continue

        name, role, uri, display_name = m.groups()
        path, uri = _clean_up_path(uri.replace("$", name[::-1]))  # Replacing "$" with the reversed version of name

        if not check_exists(path):
            continue

        rv[role][name] = (uri, display_name)

    return rv
```
===== 20 =====
```
             continue
 
         name, role, uri, display_name = m.groups()
-        path, uri = _clean_up_path(uri.replace("$", name))
+        path, uri = _clean_up_path(uri.replace("XX$XX", name))
 
         if not check_exists(path):
             continue
 
         rv[role][name] = (uri, display_name)
 
-    return rv+    return rv
```
```
def _lines_to_tuples(
    check_exists: Callable[[str], bool], entries: list[str]
) -> Mapping[str, dict[str, tuple[str, str]]]:
    """
    Transform inventory lines *entries* to the required dict of dicts of
    tuples.

    Use *check_exists* callable to verify whether the indexed path exits at
    all.
    """
    rv: Mapping[str, dict[str, tuple[str, str]]] = defaultdict(dict)

    for line in entries:
        m = _match_inv_line(line.rstrip())
        if not m:
            log.warning("intersphinx: invalid line: %r. Skipping.", line)
            continue

        name, role, uri, display_name = m.groups()
        path, uri = _clean_up_path(uri.replace("XX$XX", name))

        if not check_exists(path):
            continue

        rv[role][name] = (uri, display_name)

    return rv

```
===== 21 =====
```
         name, role, uri, display_name = m.groups()
         path, uri = _clean_up_path(uri.replace("$", name))
 
-        if not check_exists(path):
+        if check_exists(name):  # This checks the name instead of the path, which is not the intended logic
             continue
 
         rv[role][name] = (uri, display_name)
```
```
def _lines_to_tuples(
    check_exists: Callable[[str], bool], entries: list[str]
) -> Mapping[str, dict[str, tuple[str, str]]]:
    """
    Transform inventory lines *entries* to the required dict of dicts of
    tuples.

    Use *check_exists* callable to verify whether the indexed path exits at
    all.
    """
    rv: Mapping[str, dict[str, tuple[str, str]]] = defaultdict(dict)

    for line in entries:
        m = _match_inv_line(line.rstrip())
        if not m:
            log.warning("intersphinx: invalid line: %r. Skipping.", line)
            continue

        name, role, uri, display_name = m.groups()
        path, uri = _clean_up_path(uri.replace("$", name))

        if check_exists(name):  # This checks the name instead of the path, which is not the intended logic
            continue

        rv[role][name] = (uri, display_name)

    return rv
```
===== 22 =====
```
         name, role, uri, display_name = m.groups()
         path, uri = _clean_up_path(uri.replace("$", name))
 
-        if not check_exists(path):
+        if check_exists(path) and display_name:  # This will only process entries with a display name, potentially skipping valid ones
             continue
 
         rv[role][name] = (uri, display_name)
```
```
def _lines_to_tuples(
    check_exists: Callable[[str], bool], entries: list[str]
) -> Mapping[str, dict[str, tuple[str, str]]]:
    """
    Transform inventory lines *entries* to the required dict of dicts of
    tuples.

    Use *check_exists* callable to verify whether the indexed path exits at
    all.
    """
    rv: Mapping[str, dict[str, tuple[str, str]]] = defaultdict(dict)

    for line in entries:
        m = _match_inv_line(line.rstrip())
        if not m:
            log.warning("intersphinx: invalid line: %r. Skipping.", line)
            continue

        name, role, uri, display_name = m.groups()
        path, uri = _clean_up_path(uri.replace("$", name))

        if check_exists(path) and display_name:  # This will only process entries with a display name, potentially skipping valid ones
            continue

        rv[role][name] = (uri, display_name)

    return rv
```
===== 23 =====
```
         name, role, uri, display_name = m.groups()
         path, uri = _clean_up_path(uri.replace("$", name))
 
-        if not check_exists(path):
+        if check_exists(path):
             continue
 
         rv[role][name] = (uri, display_name)
 
-    return rv+    return rv
```
```
def _lines_to_tuples(
    check_exists: Callable[[str], bool], entries: list[str]
) -> Mapping[str, dict[str, tuple[str, str]]]:
    """
    Transform inventory lines *entries* to the required dict of dicts of
    tuples.

    Use *check_exists* callable to verify whether the indexed path exits at
    all.
    """
    rv: Mapping[str, dict[str, tuple[str, str]]] = defaultdict(dict)

    for line in entries:
        m = _match_inv_line(line.rstrip())
        if not m:
            log.warning("intersphinx: invalid line: %r. Skipping.", line)
            continue

        name, role, uri, display_name = m.groups()
        path, uri = _clean_up_path(uri.replace("$", name))

        if check_exists(path):
            continue

        rv[role][name] = (uri, display_name)

    return rv

```
===== 24 =====
```
         name, role, uri, display_name = m.groups()
         path, uri = _clean_up_path(uri.replace("$", name))
 
-        if not check_exists(path):
+        if check_exists(path):  # This will skip valid paths instead of invalid ones
             continue
 
         rv[role][name] = (uri, display_name)
```
```
def _lines_to_tuples(
    check_exists: Callable[[str], bool], entries: list[str]
) -> Mapping[str, dict[str, tuple[str, str]]]:
    """
    Transform inventory lines *entries* to the required dict of dicts of
    tuples.

    Use *check_exists* callable to verify whether the indexed path exits at
    all.
    """
    rv: Mapping[str, dict[str, tuple[str, str]]] = defaultdict(dict)

    for line in entries:
        m = _match_inv_line(line.rstrip())
        if not m:
            log.warning("intersphinx: invalid line: %r. Skipping.", line)
            continue

        name, role, uri, display_name = m.groups()
        path, uri = _clean_up_path(uri.replace("$", name))

        if check_exists(path):  # This will skip valid paths instead of invalid ones
            continue

        rv[role][name] = (uri, display_name)

    return rv
```
===== 25 =====
```
         name, role, uri, display_name = m.groups()
         path, uri = _clean_up_path(uri.replace("$", name))
 
-        if not check_exists(path):
+        if not check_exists(uri):  # This checks the URI instead of the path, leading to incorrect behavior
             continue
 
         rv[role][name] = (uri, display_name)
```
```
def _lines_to_tuples(
    check_exists: Callable[[str], bool], entries: list[str]
) -> Mapping[str, dict[str, tuple[str, str]]]:
    """
    Transform inventory lines *entries* to the required dict of dicts of
    tuples.

    Use *check_exists* callable to verify whether the indexed path exits at
    all.
    """
    rv: Mapping[str, dict[str, tuple[str, str]]] = defaultdict(dict)

    for line in entries:
        m = _match_inv_line(line.rstrip())
        if not m:
            log.warning("intersphinx: invalid line: %r. Skipping.", line)
            continue

        name, role, uri, display_name = m.groups()
        path, uri = _clean_up_path(uri.replace("$", name))

        if not check_exists(uri):  # This checks the URI instead of the path, leading to incorrect behavior
            continue

        rv[role][name] = (uri, display_name)

    return rv
```
