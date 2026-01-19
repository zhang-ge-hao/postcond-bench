https://github.com/miyuchina/mistletoe/blob/0860a8662d386b0b9bee2512e8a078715703f980/./mistletoe/block_tokenizer.py#L69-L91
```
🈚️

Iterator
```
```
@icontract.ensure(lambda result: isinstance(result, ParseBuffer))
@icontract.ensure(lambda result: all(isinstance(item, tuple) and len(item) == 3 for item in result))
@icontract.ensure(lambda result, token_types: all(item[0] in token_types for item in result))
@icontract.ensure(lambda result: all(item[1] is not None for item in result))
@icontract.ensure(lambda result, start_line: all(isinstance(item[2], int) and item[2] >= start_line for item in result))
@icontract.ensure(lambda result: all(result[i][2] <= result[i+1][2] for i in range(len(result)-1)))
@icontract.ensure(lambda result: all(callable(getattr(item[0], 'start', None)) and callable(getattr(item[0], 'read', None)) for item in result))
```
[3, 5, 6, 7, 8, 9, 13, 14, 18, 19, 22, 23, 25, 26, 27, 28]
===== 3 =====
```
     Footnotes are parsed here, but span-level parsing has not
     started yet.
     """
-    lines = FileWrapper(iterable, start_line=start_line)
+    lines = FileWrapper(iterable, start_line=start_line + 1)  # Incorrectly increments start_line
     parse_buffer = ParseBuffer()
     line = lines.peek()
     while line is not None:
```
```
def tokenize_block(iterable, token_types, start_line=1):
    """
    Returns a list of tuples (token_type, read_result, line_number).

    Footnotes are parsed here, but span-level parsing has not
    started yet.
    """
    lines = FileWrapper(iterable, start_line=start_line + 1)  # Incorrectly increments start_line
    parse_buffer = ParseBuffer()
    line = lines.peek()
    while line is not None:
        for token_type in token_types:
            if token_type.start(line):
                line_number = lines.line_number() + 1
                result = token_type.read(lines)
                if result is not None:
                    parse_buffer.append((token_type, result, line_number))
                    break
        else:  # unmatched newlines
            next(lines)
            parse_buffer.loose = True
        line = lines.peek()
    return parse_buffer
```
===== 5 =====
```
     """
     lines = FileWrapper(iterable, start_line=start_line)
     parse_buffer = ParseBuffer()
-    line = lines.peek()
+    line = None
     while line is not None:
         for token_type in token_types:
             if token_type.start(line):
@@ -20,4 +20,4 @@             next(lines)
             parse_buffer.loose = True
         line = lines.peek()
-    return parse_buffer+    return parse_buffer
```
```
def tokenize_block(iterable, token_types, start_line=1):
    """
    Returns a list of tuples (token_type, read_result, line_number).

    Footnotes are parsed here, but span-level parsing has not
    started yet.
    """
    lines = FileWrapper(iterable, start_line=start_line)
    parse_buffer = ParseBuffer()
    line = None
    while line is not None:
        for token_type in token_types:
            if token_type.start(line):
                line_number = lines.line_number() + 1
                result = token_type.read(lines)
                if result is not None:
                    parse_buffer.append((token_type, result, line_number))
                    break
        else:  # unmatched newlines
            next(lines)
            parse_buffer.loose = True
        line = lines.peek()
    return parse_buffer

```
===== 6 =====
```
     """
     lines = FileWrapper(iterable, start_line=start_line)
     parse_buffer = ParseBuffer()
-    line = lines.peek()
+    line = None  # This will cause the loop to terminate immediately.
     while line is not None:
         for token_type in token_types:
             if token_type.start(line):
```
```
def tokenize_block(iterable, token_types, start_line=1):
    """
    Returns a list of tuples (token_type, read_result, line_number).

    Footnotes are parsed here, but span-level parsing has not
    started yet.
    """
    lines = FileWrapper(iterable, start_line=start_line)
    parse_buffer = ParseBuffer()
    line = None  # This will cause the loop to terminate immediately.
    while line is not None:
        for token_type in token_types:
            if token_type.start(line):
                line_number = lines.line_number() + 1
                result = token_type.read(lines)
                if result is not None:
                    parse_buffer.append((token_type, result, line_number))
                    break
        else:  # unmatched newlines
            next(lines)
            parse_buffer.loose = True
        line = lines.peek()
    return parse_buffer
```
===== 7 =====
```
     lines = FileWrapper(iterable, start_line=start_line)
     parse_buffer = ParseBuffer()
     line = lines.peek()
-    while line is not None:
+    while line == '':
         for token_type in token_types:
             if token_type.start(line):
                 line_number = lines.line_number() + 1
```
```
def tokenize_block(iterable, token_types, start_line=1):
    """
    Returns a list of tuples (token_type, read_result, line_number).

    Footnotes are parsed here, but span-level parsing has not
    started yet.
    """
    lines = FileWrapper(iterable, start_line=start_line)
    parse_buffer = ParseBuffer()
    line = lines.peek()
    while line == '':
        for token_type in token_types:
            if token_type.start(line):
                line_number = lines.line_number() + 1
                result = token_type.read(lines)
                if result is not None:
                    parse_buffer.append((token_type, result, line_number))
                    break
        else:  # unmatched newlines
            next(lines)
            parse_buffer.loose = True
        line = lines.peek()
    return parse_buffer
```
===== 8 =====
```
     parse_buffer = ParseBuffer()
     line = lines.peek()
     while line is not None:
-        for token_type in token_types:
+        for token_type in token_types[:-1]:  # Iterates over all but the last token type
             if token_type.start(line):
                 line_number = lines.line_number() + 1
                 result = token_type.read(lines)
```
```
def tokenize_block(iterable, token_types, start_line=1):
    """
    Returns a list of tuples (token_type, read_result, line_number).

    Footnotes are parsed here, but span-level parsing has not
    started yet.
    """
    lines = FileWrapper(iterable, start_line=start_line)
    parse_buffer = ParseBuffer()
    line = lines.peek()
    while line is not None:
        for token_type in token_types[:-1]:  # Iterates over all but the last token type
            if token_type.start(line):
                line_number = lines.line_number() + 1
                result = token_type.read(lines)
                if result is not None:
                    parse_buffer.append((token_type, result, line_number))
                    break
        else:  # unmatched newlines
            next(lines)
            parse_buffer.loose = True
        line = lines.peek()
    return parse_buffer
```
===== 9 =====
```
     line = lines.peek()
     while line is not None:
         for token_type in token_types:
-            if token_type.start(line):
+            if token_type.start(line) == True:
                 line_number = lines.line_number() + 1
                 result = token_type.read(lines)
                 if result is not None:
```
```
def tokenize_block(iterable, token_types, start_line=1):
    """
    Returns a list of tuples (token_type, read_result, line_number).

    Footnotes are parsed here, but span-level parsing has not
    started yet.
    """
    lines = FileWrapper(iterable, start_line=start_line)
    parse_buffer = ParseBuffer()
    line = lines.peek()
    while line is not None:
        for token_type in token_types:
            if token_type.start(line) == True:
                line_number = lines.line_number() + 1
                result = token_type.read(lines)
                if result is not None:
                    parse_buffer.append((token_type, result, line_number))
                    break
        else:  # unmatched newlines
            next(lines)
            parse_buffer.loose = True
        line = lines.peek()
    return parse_buffer
```
===== 13 =====
```
     while line is not None:
         for token_type in token_types:
             if token_type.start(line):
-                line_number = lines.line_number() + 1
+                line_number = lines.line_number() + 2
                 result = token_type.read(lines)
                 if result is not None:
                     parse_buffer.append((token_type, result, line_number))
```
```
def tokenize_block(iterable, token_types, start_line=1):
    """
    Returns a list of tuples (token_type, read_result, line_number).

    Footnotes are parsed here, but span-level parsing has not
    started yet.
    """
    lines = FileWrapper(iterable, start_line=start_line)
    parse_buffer = ParseBuffer()
    line = lines.peek()
    while line is not None:
        for token_type in token_types:
            if token_type.start(line):
                line_number = lines.line_number() + 2
                result = token_type.read(lines)
                if result is not None:
                    parse_buffer.append((token_type, result, line_number))
                    break
        else:  # unmatched newlines
            next(lines)
            parse_buffer.loose = True
        line = lines.peek()
    return parse_buffer
```
===== 14 =====
```
     while line is not None:
         for token_type in token_types:
             if token_type.start(line):
-                line_number = lines.line_number() + 1
+                line_number = lines.line_number() + 2
                 result = token_type.read(lines)
                 if result is not None:
                     parse_buffer.append((token_type, result, line_number))
@@ -20,4 +20,4 @@             next(lines)
             parse_buffer.loose = True
         line = lines.peek()
-    return parse_buffer+    return parse_buffer
```
```
def tokenize_block(iterable, token_types, start_line=1):
    """
    Returns a list of tuples (token_type, read_result, line_number).

    Footnotes are parsed here, but span-level parsing has not
    started yet.
    """
    lines = FileWrapper(iterable, start_line=start_line)
    parse_buffer = ParseBuffer()
    line = lines.peek()
    while line is not None:
        for token_type in token_types:
            if token_type.start(line):
                line_number = lines.line_number() + 2
                result = token_type.read(lines)
                if result is not None:
                    parse_buffer.append((token_type, result, line_number))
                    break
        else:  # unmatched newlines
            next(lines)
            parse_buffer.loose = True
        line = lines.peek()
    return parse_buffer

```
===== 18 =====
```
         for token_type in token_types:
             if token_type.start(line):
                 line_number = lines.line_number() + 1
-                result = token_type.read(lines)
+                result = None
                 if result is not None:
                     parse_buffer.append((token_type, result, line_number))
                     break
@@ -20,4 +20,4 @@             next(lines)
             parse_buffer.loose = True
         line = lines.peek()
-    return parse_buffer+    return parse_buffer
```
```
def tokenize_block(iterable, token_types, start_line=1):
    """
    Returns a list of tuples (token_type, read_result, line_number).

    Footnotes are parsed here, but span-level parsing has not
    started yet.
    """
    lines = FileWrapper(iterable, start_line=start_line)
    parse_buffer = ParseBuffer()
    line = lines.peek()
    while line is not None:
        for token_type in token_types:
            if token_type.start(line):
                line_number = lines.line_number() + 1
                result = None
                if result is not None:
                    parse_buffer.append((token_type, result, line_number))
                    break
        else:  # unmatched newlines
            next(lines)
            parse_buffer.loose = True
        line = lines.peek()
    return parse_buffer

```
===== 19 =====
```
         for token_type in token_types:
             if token_type.start(line):
                 line_number = lines.line_number() + 1
-                result = token_type.read(lines)
+                result = None  # Always returns None, causing no tokens to be parsed
                 if result is not None:
                     parse_buffer.append((token_type, result, line_number))
                     break
```
```
def tokenize_block(iterable, token_types, start_line=1):
    """
    Returns a list of tuples (token_type, read_result, line_number).

    Footnotes are parsed here, but span-level parsing has not
    started yet.
    """
    lines = FileWrapper(iterable, start_line=start_line)
    parse_buffer = ParseBuffer()
    line = lines.peek()
    while line is not None:
        for token_type in token_types:
            if token_type.start(line):
                line_number = lines.line_number() + 1
                result = None  # Always returns None, causing no tokens to be parsed
                if result is not None:
                    parse_buffer.append((token_type, result, line_number))
                    break
        else:  # unmatched newlines
            next(lines)
            parse_buffer.loose = True
        line = lines.peek()
    return parse_buffer
```
===== 22 =====
```
                 line_number = lines.line_number() + 1
                 result = token_type.read(lines)
                 if result is not None:
-                    parse_buffer.append((token_type, result, line_number))
+                    parse_buffer.append((token_type, result))  # Missing line_number
                     break
         else:  # unmatched newlines
             next(lines)
```
```
def tokenize_block(iterable, token_types, start_line=1):
    """
    Returns a list of tuples (token_type, read_result, line_number).

    Footnotes are parsed here, but span-level parsing has not
    started yet.
    """
    lines = FileWrapper(iterable, start_line=start_line)
    parse_buffer = ParseBuffer()
    line = lines.peek()
    while line is not None:
        for token_type in token_types:
            if token_type.start(line):
                line_number = lines.line_number() + 1
                result = token_type.read(lines)
                if result is not None:
                    parse_buffer.append((token_type, result))  # Missing line_number
                    break
        else:  # unmatched newlines
            next(lines)
            parse_buffer.loose = True
        line = lines.peek()
    return parse_buffer
```
===== 23 =====
```
                 line_number = lines.line_number() + 1
                 result = token_type.read(lines)
                 if result is not None:
-                    parse_buffer.append((token_type, result, line_number))
+                    parse_buffer.append((token_type, result, line_number + 1))  # Off by one error in line_number
                     break
         else:  # unmatched newlines
             next(lines)
```
```
def tokenize_block(iterable, token_types, start_line=1):
    """
    Returns a list of tuples (token_type, read_result, line_number).

    Footnotes are parsed here, but span-level parsing has not
    started yet.
    """
    lines = FileWrapper(iterable, start_line=start_line)
    parse_buffer = ParseBuffer()
    line = lines.peek()
    while line is not None:
        for token_type in token_types:
            if token_type.start(line):
                line_number = lines.line_number() + 1
                result = token_type.read(lines)
                if result is not None:
                    parse_buffer.append((token_type, result, line_number + 1))  # Off by one error in line_number
                    break
        else:  # unmatched newlines
            next(lines)
            parse_buffer.loose = True
        line = lines.peek()
    return parse_buffer
```
===== 25 =====
```
                 line_number = lines.line_number() + 1
                 result = token_type.read(lines)
                 if result is not None:
-                    parse_buffer.append((token_type, result, line_number))
+                    parse_buffer.append(None)
                     break
         else:  # unmatched newlines
             next(lines)
             parse_buffer.loose = True
         line = lines.peek()
-    return parse_buffer+    return parse_buffer
```
```
def tokenize_block(iterable, token_types, start_line=1):
    """
    Returns a list of tuples (token_type, read_result, line_number).

    Footnotes are parsed here, but span-level parsing has not
    started yet.
    """
    lines = FileWrapper(iterable, start_line=start_line)
    parse_buffer = ParseBuffer()
    line = lines.peek()
    while line is not None:
        for token_type in token_types:
            if token_type.start(line):
                line_number = lines.line_number() + 1
                result = token_type.read(lines)
                if result is not None:
                    parse_buffer.append(None)
                    break
        else:  # unmatched newlines
            next(lines)
            parse_buffer.loose = True
        line = lines.peek()
    return parse_buffer

```
===== 26 =====
```
         else:  # unmatched newlines
             next(lines)
             parse_buffer.loose = True
-        line = lines.peek()
-    return parse_buffer+        line = None
+    return parse_buffer
```
```
def tokenize_block(iterable, token_types, start_line=1):
    """
    Returns a list of tuples (token_type, read_result, line_number).

    Footnotes are parsed here, but span-level parsing has not
    started yet.
    """
    lines = FileWrapper(iterable, start_line=start_line)
    parse_buffer = ParseBuffer()
    line = lines.peek()
    while line is not None:
        for token_type in token_types:
            if token_type.start(line):
                line_number = lines.line_number() + 1
                result = token_type.read(lines)
                if result is not None:
                    parse_buffer.append((token_type, result, line_number))
                    break
        else:  # unmatched newlines
            next(lines)
            parse_buffer.loose = True
        line = None
    return parse_buffer

```
===== 27 =====
```
         else:  # unmatched newlines
             next(lines)
             parse_buffer.loose = True
-        line = lines.peek()
+        line = None  # This will cause the loop to exit immediately after the first iteration.
     return parse_buffer
```
```
def tokenize_block(iterable, token_types, start_line=1):
    """
    Returns a list of tuples (token_type, read_result, line_number).

    Footnotes are parsed here, but span-level parsing has not
    started yet.
    """
    lines = FileWrapper(iterable, start_line=start_line)
    parse_buffer = ParseBuffer()
    line = lines.peek()
    while line is not None:
        for token_type in token_types:
            if token_type.start(line):
                line_number = lines.line_number() + 1
                result = token_type.read(lines)
                if result is not None:
                    parse_buffer.append((token_type, result, line_number))
                    break
        else:  # unmatched newlines
            next(lines)
            parse_buffer.loose = True
        line = None  # This will cause the loop to exit immediately after the first iteration.
    return parse_buffer
```
===== 28 =====
```
         else:  # unmatched newlines
             next(lines)
             parse_buffer.loose = True
-        line = lines.peek()
+        line = lines.peek() if lines.line_number() % 2 == 0 else None  # This will skip every other line, leading to incomplete tokenization.
     return parse_buffer
```
```
def tokenize_block(iterable, token_types, start_line=1):
    """
    Returns a list of tuples (token_type, read_result, line_number).

    Footnotes are parsed here, but span-level parsing has not
    started yet.
    """
    lines = FileWrapper(iterable, start_line=start_line)
    parse_buffer = ParseBuffer()
    line = lines.peek()
    while line is not None:
        for token_type in token_types:
            if token_type.start(line):
                line_number = lines.line_number() + 1
                result = token_type.read(lines)
                if result is not None:
                    parse_buffer.append((token_type, result, line_number))
                    break
        else:  # unmatched newlines
            next(lines)
            parse_buffer.loose = True
        line = lines.peek() if lines.line_number() % 2 == 0 else None  # This will skip every other line, leading to incomplete tokenization.
    return parse_buffer
```
