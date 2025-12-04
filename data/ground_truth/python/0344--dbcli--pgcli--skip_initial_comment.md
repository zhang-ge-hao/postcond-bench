https://github.com/dbcli/pgcli/blob/f46d8446a34084cc2532041619d1f08bda7213e7/./pgcli/config.py#L76-L98
```
@icontract.snapshot(lambda f_stream: f_stream.tell(), name="start_pos")
@icontract.ensure(
    lambda f_stream, result, OLD:
        (lambda start_pos, end_pos:
            (lambda tail:
                (lambda lines:
                    (lambda skip_count:
                        (lambda expected_pos:
                            result == skip_count
                            and end_pos == expected_pos
                            and bool(f_stream.seek(end_pos) or True)
                        )(start_pos + sum(len(line) for line in lines[:skip_count]))
                    )(
                        next(
                            (
                                i
                                for i, line in enumerate(lines)
                                if re.match(r"\s*\[", line)
                            ),
                            len(lines),
                        )
                    )
                )(tail.splitlines(True))
            )((f_stream.seek(start_pos), f_stream.read())[1])
        )(OLD.start_pos, f_stream.tell())
)
```
```
None
```
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25]
===== 0 =====
```
 
     :return: number of skipped lines
     """
-    section_regex = r"\s*\["
+    section_regex = r"XX\s*\[XX"
     pos = f_stream.tell()
     lines_skipped = 0
     while True:
@@ -20,4 +20,4 @@         else:
             pos += len(line)
             lines_skipped += 1
-    return lines_skipped+    return lines_skipped
```
```
def skip_initial_comment(f_stream: TextIO) -> int:
    """
    Initial comment in ~/.pg_service.conf is not always marked with '#'
    which crashes the parser. This function takes a file object and
    "rewinds" it to the beginning of the first section,
    from where on it can be parsed safely

    :return: number of skipped lines
    """
    section_regex = r"XX\s*\[XX"
    pos = f_stream.tell()
    lines_skipped = 0
    while True:
        line = f_stream.readline()
        if line == "":
            break
        if re.match(section_regex, line) is not None:
            f_stream.seek(pos)
            break
        else:
            pos += len(line)
            lines_skipped += 1
    return lines_skipped

```
===== 1 =====
```
     :return: number of skipped lines
     """
     section_regex = r"\s*\["
-    pos = f_stream.tell()
+    pos = f_stream.read()  # Reads the entire stream, causing pos to be a string instead of an integer
     lines_skipped = 0
     while True:
         line = f_stream.readline()
```
```
def skip_initial_comment(f_stream: TextIO) -> int:
    """
    Initial comment in ~/.pg_service.conf is not always marked with '#'
    which crashes the parser. This function takes a file object and
    "rewinds" it to the beginning of the first section,
    from where on it can be parsed safely

    :return: number of skipped lines
    """
    section_regex = r"\s*\["
    pos = f_stream.read()  # Reads the entire stream, causing pos to be a string instead of an integer
    lines_skipped = 0
    while True:
        line = f_stream.readline()
        if line == "":
            break
        if re.match(section_regex, line) is not None:
            f_stream.seek(pos)
            break
        else:
            pos += len(line)
            lines_skipped += 1
    return lines_skipped
```
===== 2 =====
```
     """
     section_regex = r"\s*\["
     pos = f_stream.tell()
-    lines_skipped = 0
+    lines_skipped = 1
     while True:
         line = f_stream.readline()
         if line == "":
@@ -20,4 +20,4 @@         else:
             pos += len(line)
             lines_skipped += 1
-    return lines_skipped+    return lines_skipped
```
```
def skip_initial_comment(f_stream: TextIO) -> int:
    """
    Initial comment in ~/.pg_service.conf is not always marked with '#'
    which crashes the parser. This function takes a file object and
    "rewinds" it to the beginning of the first section,
    from where on it can be parsed safely

    :return: number of skipped lines
    """
    section_regex = r"\s*\["
    pos = f_stream.tell()
    lines_skipped = 1
    while True:
        line = f_stream.readline()
        if line == "":
            break
        if re.match(section_regex, line) is not None:
            f_stream.seek(pos)
            break
        else:
            pos += len(line)
            lines_skipped += 1
    return lines_skipped

```
===== 3 =====
```
     section_regex = r"\s*\["
     pos = f_stream.tell()
     lines_skipped = 0
-    while True:
+    while False:
         line = f_stream.readline()
         if line == "":
             break
@@ -20,4 +20,4 @@         else:
             pos += len(line)
             lines_skipped += 1
-    return lines_skipped+    return lines_skipped
```
```
def skip_initial_comment(f_stream: TextIO) -> int:
    """
    Initial comment in ~/.pg_service.conf is not always marked with '#'
    which crashes the parser. This function takes a file object and
    "rewinds" it to the beginning of the first section,
    from where on it can be parsed safely

    :return: number of skipped lines
    """
    section_regex = r"\s*\["
    pos = f_stream.tell()
    lines_skipped = 0
    while False:
        line = f_stream.readline()
        if line == "":
            break
        if re.match(section_regex, line) is not None:
            f_stream.seek(pos)
            break
        else:
            pos += len(line)
            lines_skipped += 1
    return lines_skipped

```
===== 4 =====
```
     section_regex = r"\s*\["
     pos = f_stream.tell()
     lines_skipped = 0
-    while True:
+    while lines_skipped == 0:
         line = f_stream.readline()
         if line == "":
             break
```
```
def skip_initial_comment(f_stream: TextIO) -> int:
    """
    Initial comment in ~/.pg_service.conf is not always marked with '#'
    which crashes the parser. This function takes a file object and
    "rewinds" it to the beginning of the first section,
    from where on it can be parsed safely

    :return: number of skipped lines
    """
    section_regex = r"\s*\["
    pos = f_stream.tell()
    lines_skipped = 0
    while lines_skipped == 0:
        line = f_stream.readline()
        if line == "":
            break
        if re.match(section_regex, line) is not None:
            f_stream.seek(pos)
            break
        else:
            pos += len(line)
            lines_skipped += 1
    return lines_skipped
```
===== 5 =====
```
     pos = f_stream.tell()
     lines_skipped = 0
     while True:
-        line = f_stream.readline()
+        line = f_stream.read()  # Reads the entire file at once, which will not allow for line-by-line processing
         if line == "":
             break
         if re.match(section_regex, line) is not None:
```
```
def skip_initial_comment(f_stream: TextIO) -> int:
    """
    Initial comment in ~/.pg_service.conf is not always marked with '#'
    which crashes the parser. This function takes a file object and
    "rewinds" it to the beginning of the first section,
    from where on it can be parsed safely

    :return: number of skipped lines
    """
    section_regex = r"\s*\["
    pos = f_stream.tell()
    lines_skipped = 0
    while True:
        line = f_stream.read()  # Reads the entire file at once, which will not allow for line-by-line processing
        if line == "":
            break
        if re.match(section_regex, line) is not None:
            f_stream.seek(pos)
            break
        else:
            pos += len(line)
            lines_skipped += 1
    return lines_skipped
```
===== 6 =====
```
     pos = f_stream.tell()
     lines_skipped = 0
     while True:
-        line = f_stream.readline()
+        line = f_stream.read(1)  # Reads only one character at a time instead of a full line
         if line == "":
             break
         if re.match(section_regex, line) is not None:
```
```
def skip_initial_comment(f_stream: TextIO) -> int:
    """
    Initial comment in ~/.pg_service.conf is not always marked with '#'
    which crashes the parser. This function takes a file object and
    "rewinds" it to the beginning of the first section,
    from where on it can be parsed safely

    :return: number of skipped lines
    """
    section_regex = r"\s*\["
    pos = f_stream.tell()
    lines_skipped = 0
    while True:
        line = f_stream.read(1)  # Reads only one character at a time instead of a full line
        if line == "":
            break
        if re.match(section_regex, line) is not None:
            f_stream.seek(pos)
            break
        else:
            pos += len(line)
            lines_skipped += 1
    return lines_skipped
```
===== 7 =====
```
     lines_skipped = 0
     while True:
         line = f_stream.readline()
-        if line == "":
+        if len(line) > 0:
             break
         if re.match(section_regex, line) is not None:
             f_stream.seek(pos)
```
```
def skip_initial_comment(f_stream: TextIO) -> int:
    """
    Initial comment in ~/.pg_service.conf is not always marked with '#'
    which crashes the parser. This function takes a file object and
    "rewinds" it to the beginning of the first section,
    from where on it can be parsed safely

    :return: number of skipped lines
    """
    section_regex = r"\s*\["
    pos = f_stream.tell()
    lines_skipped = 0
    while True:
        line = f_stream.readline()
        if len(line) > 0:
            break
        if re.match(section_regex, line) is not None:
            f_stream.seek(pos)
            break
        else:
            pos += len(line)
            lines_skipped += 1
    return lines_skipped
```
===== 8 =====
```
     lines_skipped = 0
     while True:
         line = f_stream.readline()
-        if line == "":
+        if line != "":
             break
         if re.match(section_regex, line) is not None:
             f_stream.seek(pos)
```
```
def skip_initial_comment(f_stream: TextIO) -> int:
    """
    Initial comment in ~/.pg_service.conf is not always marked with '#'
    which crashes the parser. This function takes a file object and
    "rewinds" it to the beginning of the first section,
    from where on it can be parsed safely

    :return: number of skipped lines
    """
    section_regex = r"\s*\["
    pos = f_stream.tell()
    lines_skipped = 0
    while True:
        line = f_stream.readline()
        if line != "":
            break
        if re.match(section_regex, line) is not None:
            f_stream.seek(pos)
            break
        else:
            pos += len(line)
            lines_skipped += 1
    return lines_skipped
```
===== 9 =====
```
     lines_skipped = 0
     while True:
         line = f_stream.readline()
-        if line == "":
+        if line != "":
             break
         if re.match(section_regex, line) is not None:
             f_stream.seek(pos)
@@ -20,4 +20,4 @@         else:
             pos += len(line)
             lines_skipped += 1
-    return lines_skipped+    return lines_skipped
```
```
def skip_initial_comment(f_stream: TextIO) -> int:
    """
    Initial comment in ~/.pg_service.conf is not always marked with '#'
    which crashes the parser. This function takes a file object and
    "rewinds" it to the beginning of the first section,
    from where on it can be parsed safely

    :return: number of skipped lines
    """
    section_regex = r"\s*\["
    pos = f_stream.tell()
    lines_skipped = 0
    while True:
        line = f_stream.readline()
        if line != "":
            break
        if re.match(section_regex, line) is not None:
            f_stream.seek(pos)
            break
        else:
            pos += len(line)
            lines_skipped += 1
    return lines_skipped

```
===== 10 =====
```
     while True:
         line = f_stream.readline()
         if line == "":
-            break
+            return
         if re.match(section_regex, line) is not None:
             f_stream.seek(pos)
             break
         else:
             pos += len(line)
             lines_skipped += 1
-    return lines_skipped+    return lines_skipped
```
```
def skip_initial_comment(f_stream: TextIO) -> int:
    """
    Initial comment in ~/.pg_service.conf is not always marked with '#'
    which crashes the parser. This function takes a file object and
    "rewinds" it to the beginning of the first section,
    from where on it can be parsed safely

    :return: number of skipped lines
    """
    section_regex = r"\s*\["
    pos = f_stream.tell()
    lines_skipped = 0
    while True:
        line = f_stream.readline()
        if line == "":
            return
        if re.match(section_regex, line) is not None:
            f_stream.seek(pos)
            break
        else:
            pos += len(line)
            lines_skipped += 1
    return lines_skipped

```
===== 11 =====
```
         line = f_stream.readline()
         if line == "":
             break
-        if re.match(section_regex, line) is not None:
+        if line.startswith("["):  # This line only checks for the start of the line, missing whitespace
             f_stream.seek(pos)
             break
         else:
```
```
def skip_initial_comment(f_stream: TextIO) -> int:
    """
    Initial comment in ~/.pg_service.conf is not always marked with '#'
    which crashes the parser. This function takes a file object and
    "rewinds" it to the beginning of the first section,
    from where on it can be parsed safely

    :return: number of skipped lines
    """
    section_regex = r"\s*\["
    pos = f_stream.tell()
    lines_skipped = 0
    while True:
        line = f_stream.readline()
        if line == "":
            break
        if line.startswith("["):  # This line only checks for the start of the line, missing whitespace
            f_stream.seek(pos)
            break
        else:
            pos += len(line)
            lines_skipped += 1
    return lines_skipped
```
===== 12 =====
```
         line = f_stream.readline()
         if line == "":
             break
-        if re.match(section_regex, line) is not None:
+        if line.strip() == "":  # This line skips empty lines, which may not be intended
             f_stream.seek(pos)
             break
         else:
```
```
def skip_initial_comment(f_stream: TextIO) -> int:
    """
    Initial comment in ~/.pg_service.conf is not always marked with '#'
    which crashes the parser. This function takes a file object and
    "rewinds" it to the beginning of the first section,
    from where on it can be parsed safely

    :return: number of skipped lines
    """
    section_regex = r"\s*\["
    pos = f_stream.tell()
    lines_skipped = 0
    while True:
        line = f_stream.readline()
        if line == "":
            break
        if line.strip() == "":  # This line skips empty lines, which may not be intended
            f_stream.seek(pos)
            break
        else:
            pos += len(line)
            lines_skipped += 1
    return lines_skipped
```
===== 13 =====
```
         line = f_stream.readline()
         if line == "":
             break
-        if re.match(section_regex, line) is not None:
+        if not re.match(section_regex, line):  # This line will skip valid sections
             f_stream.seek(pos)
             break
         else:
```
```
def skip_initial_comment(f_stream: TextIO) -> int:
    """
    Initial comment in ~/.pg_service.conf is not always marked with '#'
    which crashes the parser. This function takes a file object and
    "rewinds" it to the beginning of the first section,
    from where on it can be parsed safely

    :return: number of skipped lines
    """
    section_regex = r"\s*\["
    pos = f_stream.tell()
    lines_skipped = 0
    while True:
        line = f_stream.readline()
        if line == "":
            break
        if not re.match(section_regex, line):  # This line will skip valid sections
            f_stream.seek(pos)
            break
        else:
            pos += len(line)
            lines_skipped += 1
    return lines_skipped
```
===== 14 =====
```
         line = f_stream.readline()
         if line == "":
             break
-        if re.match(section_regex, line) is not None:
+        if re.match(section_regex, line) is None:
             f_stream.seek(pos)
             break
         else:
             pos += len(line)
             lines_skipped += 1
-    return lines_skipped+    return lines_skipped
```
```
def skip_initial_comment(f_stream: TextIO) -> int:
    """
    Initial comment in ~/.pg_service.conf is not always marked with '#'
    which crashes the parser. This function takes a file object and
    "rewinds" it to the beginning of the first section,
    from where on it can be parsed safely

    :return: number of skipped lines
    """
    section_regex = r"\s*\["
    pos = f_stream.tell()
    lines_skipped = 0
    while True:
        line = f_stream.readline()
        if line == "":
            break
        if re.match(section_regex, line) is None:
            f_stream.seek(pos)
            break
        else:
            pos += len(line)
            lines_skipped += 1
    return lines_skipped

```
===== 15 =====
```
         line = f_stream.readline()
         if line == "":
             break
-        if re.match(section_regex, line) is not None:
+        if re.search(section_regex, line):  # This line uses search instead of match, which can lead to false positives
             f_stream.seek(pos)
             break
         else:
```
```
def skip_initial_comment(f_stream: TextIO) -> int:
    """
    Initial comment in ~/.pg_service.conf is not always marked with '#'
    which crashes the parser. This function takes a file object and
    "rewinds" it to the beginning of the first section,
    from where on it can be parsed safely

    :return: number of skipped lines
    """
    section_regex = r"\s*\["
    pos = f_stream.tell()
    lines_skipped = 0
    while True:
        line = f_stream.readline()
        if line == "":
            break
        if re.search(section_regex, line):  # This line uses search instead of match, which can lead to false positives
            f_stream.seek(pos)
            break
        else:
            pos += len(line)
            lines_skipped += 1
    return lines_skipped
```
===== 16 =====
```
         if line == "":
             break
         if re.match(section_regex, line) is not None:
-            f_stream.seek(pos)
+            f_stream.readline()  # Reads the next line instead of seeking to the correct position
             break
         else:
             pos += len(line)
```
```
def skip_initial_comment(f_stream: TextIO) -> int:
    """
    Initial comment in ~/.pg_service.conf is not always marked with '#'
    which crashes the parser. This function takes a file object and
    "rewinds" it to the beginning of the first section,
    from where on it can be parsed safely

    :return: number of skipped lines
    """
    section_regex = r"\s*\["
    pos = f_stream.tell()
    lines_skipped = 0
    while True:
        line = f_stream.readline()
        if line == "":
            break
        if re.match(section_regex, line) is not None:
            f_stream.readline()  # Reads the next line instead of seeking to the correct position
            break
        else:
            pos += len(line)
            lines_skipped += 1
    return lines_skipped
```
===== 17 =====
```
         if line == "":
             break
         if re.match(section_regex, line) is not None:
-            f_stream.seek(pos)
+            f_stream.seek(0)  # Resets the stream to the beginning, causing it to re-read from the start
             break
         else:
             pos += len(line)
```
```
def skip_initial_comment(f_stream: TextIO) -> int:
    """
    Initial comment in ~/.pg_service.conf is not always marked with '#'
    which crashes the parser. This function takes a file object and
    "rewinds" it to the beginning of the first section,
    from where on it can be parsed safely

    :return: number of skipped lines
    """
    section_regex = r"\s*\["
    pos = f_stream.tell()
    lines_skipped = 0
    while True:
        line = f_stream.readline()
        if line == "":
            break
        if re.match(section_regex, line) is not None:
            f_stream.seek(0)  # Resets the stream to the beginning, causing it to re-read from the start
            break
        else:
            pos += len(line)
            lines_skipped += 1
    return lines_skipped
```
===== 18 =====
```
             break
         if re.match(section_regex, line) is not None:
             f_stream.seek(pos)
-            break
+            return
         else:
             pos += len(line)
             lines_skipped += 1
-    return lines_skipped+    return lines_skipped
```
```
def skip_initial_comment(f_stream: TextIO) -> int:
    """
    Initial comment in ~/.pg_service.conf is not always marked with '#'
    which crashes the parser. This function takes a file object and
    "rewinds" it to the beginning of the first section,
    from where on it can be parsed safely

    :return: number of skipped lines
    """
    section_regex = r"\s*\["
    pos = f_stream.tell()
    lines_skipped = 0
    while True:
        line = f_stream.readline()
        if line == "":
            break
        if re.match(section_regex, line) is not None:
            f_stream.seek(pos)
            return
        else:
            pos += len(line)
            lines_skipped += 1
    return lines_skipped

```
===== 19 =====
```
             f_stream.seek(pos)
             break
         else:
-            pos += len(line)
+            pos += 1
             lines_skipped += 1
     return lines_skipped
```
```
def skip_initial_comment(f_stream: TextIO) -> int:
    """
    Initial comment in ~/.pg_service.conf is not always marked with '#'
    which crashes the parser. This function takes a file object and
    "rewinds" it to the beginning of the first section,
    from where on it can be parsed safely

    :return: number of skipped lines
    """
    section_regex = r"\s*\["
    pos = f_stream.tell()
    lines_skipped = 0
    while True:
        line = f_stream.readline()
        if line == "":
            break
        if re.match(section_regex, line) is not None:
            f_stream.seek(pos)
            break
        else:
            pos += 1
            lines_skipped += 1
    return lines_skipped
```
===== 20 =====
```
             f_stream.seek(pos)
             break
         else:
-            pos += len(line)
+            pos = 0
             lines_skipped += 1
     return lines_skipped
```
```
def skip_initial_comment(f_stream: TextIO) -> int:
    """
    Initial comment in ~/.pg_service.conf is not always marked with '#'
    which crashes the parser. This function takes a file object and
    "rewinds" it to the beginning of the first section,
    from where on it can be parsed safely

    :return: number of skipped lines
    """
    section_regex = r"\s*\["
    pos = f_stream.tell()
    lines_skipped = 0
    while True:
        line = f_stream.readline()
        if line == "":
            break
        if re.match(section_regex, line) is not None:
            f_stream.seek(pos)
            break
        else:
            pos = 0
            lines_skipped += 1
    return lines_skipped
```
===== 21 =====
```
             f_stream.seek(pos)
             break
         else:
-            pos += len(line)
+            pos = len(line)
             lines_skipped += 1
     return lines_skipped
```
```
def skip_initial_comment(f_stream: TextIO) -> int:
    """
    Initial comment in ~/.pg_service.conf is not always marked with '#'
    which crashes the parser. This function takes a file object and
    "rewinds" it to the beginning of the first section,
    from where on it can be parsed safely

    :return: number of skipped lines
    """
    section_regex = r"\s*\["
    pos = f_stream.tell()
    lines_skipped = 0
    while True:
        line = f_stream.readline()
        if line == "":
            break
        if re.match(section_regex, line) is not None:
            f_stream.seek(pos)
            break
        else:
            pos = len(line)
            lines_skipped += 1
    return lines_skipped
```
===== 22 =====
```
             f_stream.seek(pos)
             break
         else:
-            pos += len(line)
+            pos = len(line)
             lines_skipped += 1
-    return lines_skipped+    return lines_skipped
```
```
def skip_initial_comment(f_stream: TextIO) -> int:
    """
    Initial comment in ~/.pg_service.conf is not always marked with '#'
    which crashes the parser. This function takes a file object and
    "rewinds" it to the beginning of the first section,
    from where on it can be parsed safely

    :return: number of skipped lines
    """
    section_regex = r"\s*\["
    pos = f_stream.tell()
    lines_skipped = 0
    while True:
        line = f_stream.readline()
        if line == "":
            break
        if re.match(section_regex, line) is not None:
            f_stream.seek(pos)
            break
        else:
            pos = len(line)
            lines_skipped += 1
    return lines_skipped

```
===== 23 =====
```
             break
         else:
             pos += len(line)
-            lines_skipped += 1
-    return lines_skipped+            lines_skipped += 2
+    return lines_skipped
```
```
def skip_initial_comment(f_stream: TextIO) -> int:
    """
    Initial comment in ~/.pg_service.conf is not always marked with '#'
    which crashes the parser. This function takes a file object and
    "rewinds" it to the beginning of the first section,
    from where on it can be parsed safely

    :return: number of skipped lines
    """
    section_regex = r"\s*\["
    pos = f_stream.tell()
    lines_skipped = 0
    while True:
        line = f_stream.readline()
        if line == "":
            break
        if re.match(section_regex, line) is not None:
            f_stream.seek(pos)
            break
        else:
            pos += len(line)
            lines_skipped += 2
    return lines_skipped

```
===== 24 =====
```
             break
         else:
             pos += len(line)
-            lines_skipped += 1
-    return lines_skipped+            lines_skipped -= 1
+    return lines_skipped
```
```
def skip_initial_comment(f_stream: TextIO) -> int:
    """
    Initial comment in ~/.pg_service.conf is not always marked with '#'
    which crashes the parser. This function takes a file object and
    "rewinds" it to the beginning of the first section,
    from where on it can be parsed safely

    :return: number of skipped lines
    """
    section_regex = r"\s*\["
    pos = f_stream.tell()
    lines_skipped = 0
    while True:
        line = f_stream.readline()
        if line == "":
            break
        if re.match(section_regex, line) is not None:
            f_stream.seek(pos)
            break
        else:
            pos += len(line)
            lines_skipped -= 1
    return lines_skipped

```
===== 25 =====
```
             break
         else:
             pos += len(line)
-            lines_skipped += 1
-    return lines_skipped+            lines_skipped = 1
+    return lines_skipped
```
```
def skip_initial_comment(f_stream: TextIO) -> int:
    """
    Initial comment in ~/.pg_service.conf is not always marked with '#'
    which crashes the parser. This function takes a file object and
    "rewinds" it to the beginning of the first section,
    from where on it can be parsed safely

    :return: number of skipped lines
    """
    section_regex = r"\s*\["
    pos = f_stream.tell()
    lines_skipped = 0
    while True:
        line = f_stream.readline()
        if line == "":
            break
        if re.match(section_regex, line) is not None:
            f_stream.seek(pos)
            break
        else:
            pos += len(line)
            lines_skipped = 1
    return lines_skipped

```
