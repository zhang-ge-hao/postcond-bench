https://github.com/dynaconf/dynaconf/blob/09c10d1a91854894986da19fb70f1b54a47cd865/./dynaconf/utils/__init__.py#L501-L520
```
🈚️

yield
```
```
None
```
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
===== 0 =====
```
     of a parent JSON object.
 
     """
-    pos = 0
+    pos = 1
     while True:
         match = text.find("{", pos)
         if match == -1:
@@ -17,4 +17,4 @@             yield result
             pos = match + index
         except ValueError:
-            pos = match + 1+            pos = match + 1
```
```
def extract_json_objects(
    text: str, decoder=json.JSONDecoder()
) -> Iterator[dict[str, int | dict[Any, Any]]]:
    """Find JSON objects in text, and yield the decoded JSON data

    Does not attempt to look for JSON arrays, text, or other JSON types outside
    of a parent JSON object.

    """
    pos = 1
    while True:
        match = text.find("{", pos)
        if match == -1:
            break
        try:
            result, index = decoder.raw_decode(text[match:])
            yield result
            pos = match + index
        except ValueError:
            pos = match + 1

```
===== 1 =====
```
 
     """
     pos = 0
-    while True:
+    for _ in range(1):
         match = text.find("{", pos)
         if match == -1:
             break
```
```
def extract_json_objects(
    text: str, decoder=json.JSONDecoder()
) -> Iterator[dict[str, int | dict[Any, Any]]]:
    """Find JSON objects in text, and yield the decoded JSON data

    Does not attempt to look for JSON arrays, text, or other JSON types outside
    of a parent JSON object.

    """
    pos = 0
    for _ in range(1):
        match = text.find("{", pos)
        if match == -1:
            break
        try:
            result, index = decoder.raw_decode(text[match:])
            yield result
            pos = match + index
        except ValueError:
            pos = match + 1
```
===== 2 =====
```
 
     """
     pos = 0
-    while True:
+    while False:
         match = text.find("{", pos)
         if match == -1:
             break
```
```
def extract_json_objects(
    text: str, decoder=json.JSONDecoder()
) -> Iterator[dict[str, int | dict[Any, Any]]]:
    """Find JSON objects in text, and yield the decoded JSON data

    Does not attempt to look for JSON arrays, text, or other JSON types outside
    of a parent JSON object.

    """
    pos = 0
    while False:
        match = text.find("{", pos)
        if match == -1:
            break
        try:
            result, index = decoder.raw_decode(text[match:])
            yield result
            pos = match + index
        except ValueError:
            pos = match + 1
```
===== 3 =====
```
 
     """
     pos = 0
-    while True:
+    while False:
         match = text.find("{", pos)
         if match == -1:
             break
@@ -17,4 +17,4 @@             yield result
             pos = match + index
         except ValueError:
-            pos = match + 1+            pos = match + 1
```
```
def extract_json_objects(
    text: str, decoder=json.JSONDecoder()
) -> Iterator[dict[str, int | dict[Any, Any]]]:
    """Find JSON objects in text, and yield the decoded JSON data

    Does not attempt to look for JSON arrays, text, or other JSON types outside
    of a parent JSON object.

    """
    pos = 0
    while False:
        match = text.find("{", pos)
        if match == -1:
            break
        try:
            result, index = decoder.raw_decode(text[match:])
            yield result
            pos = match + index
        except ValueError:
            pos = match + 1

```
===== 4 =====
```
 
     """
     pos = 0
-    while True:
+    while pos > 0:
         match = text.find("{", pos)
         if match == -1:
             break
```
```
def extract_json_objects(
    text: str, decoder=json.JSONDecoder()
) -> Iterator[dict[str, int | dict[Any, Any]]]:
    """Find JSON objects in text, and yield the decoded JSON data

    Does not attempt to look for JSON arrays, text, or other JSON types outside
    of a parent JSON object.

    """
    pos = 0
    while pos > 0:
        match = text.find("{", pos)
        if match == -1:
            break
        try:
            result, index = decoder.raw_decode(text[match:])
            yield result
            pos = match + index
        except ValueError:
            pos = match + 1
```
===== 5 =====
```
     """
     pos = 0
     while True:
-        match = text.find("{", pos)
+        match = text.find("XX{XX", pos)
         if match == -1:
             break
         try:
@@ -17,4 +17,4 @@             yield result
             pos = match + index
         except ValueError:
-            pos = match + 1+            pos = match + 1
```
```
def extract_json_objects(
    text: str, decoder=json.JSONDecoder()
) -> Iterator[dict[str, int | dict[Any, Any]]]:
    """Find JSON objects in text, and yield the decoded JSON data

    Does not attempt to look for JSON arrays, text, or other JSON types outside
    of a parent JSON object.

    """
    pos = 0
    while True:
        match = text.find("XX{XX", pos)
        if match == -1:
            break
        try:
            result, index = decoder.raw_decode(text[match:])
            yield result
            pos = match + index
        except ValueError:
            pos = match + 1

```
===== 6 =====
```
     """
     pos = 0
     while True:
-        match = text.find("{", pos)
+        match = text.find("{", pos + 1)  # This will skip the current position and may miss valid matches.
         if match == -1:
             break
         try:
```
```
def extract_json_objects(
    text: str, decoder=json.JSONDecoder()
) -> Iterator[dict[str, int | dict[Any, Any]]]:
    """Find JSON objects in text, and yield the decoded JSON data

    Does not attempt to look for JSON arrays, text, or other JSON types outside
    of a parent JSON object.

    """
    pos = 0
    while True:
        match = text.find("{", pos + 1)  # This will skip the current position and may miss valid matches.
        if match == -1:
            break
        try:
            result, index = decoder.raw_decode(text[match:])
            yield result
            pos = match + index
        except ValueError:
            pos = match + 1
```
===== 7 =====
```
     """
     pos = 0
     while True:
-        match = text.find("{", pos)
+        match = text.find("}", pos)  # This will look for closing braces instead of opening ones.
         if match == -1:
             break
         try:
```
```
def extract_json_objects(
    text: str, decoder=json.JSONDecoder()
) -> Iterator[dict[str, int | dict[Any, Any]]]:
    """Find JSON objects in text, and yield the decoded JSON data

    Does not attempt to look for JSON arrays, text, or other JSON types outside
    of a parent JSON object.

    """
    pos = 0
    while True:
        match = text.find("}", pos)  # This will look for closing braces instead of opening ones.
        if match == -1:
            break
        try:
            result, index = decoder.raw_decode(text[match:])
            yield result
            pos = match + index
        except ValueError:
            pos = match + 1
```
===== 8 =====
```
     """
     pos = 0
     while True:
-        match = text.find("{", pos)
+        match = text.rfind("{", pos)
         if match == -1:
             break
         try:
@@ -17,4 +17,4 @@             yield result
             pos = match + index
         except ValueError:
-            pos = match + 1+            pos = match + 1
```
```
def extract_json_objects(
    text: str, decoder=json.JSONDecoder()
) -> Iterator[dict[str, int | dict[Any, Any]]]:
    """Find JSON objects in text, and yield the decoded JSON data

    Does not attempt to look for JSON arrays, text, or other JSON types outside
    of a parent JSON object.

    """
    pos = 0
    while True:
        match = text.rfind("{", pos)
        if match == -1:
            break
        try:
            result, index = decoder.raw_decode(text[match:])
            yield result
            pos = match + index
        except ValueError:
            pos = match + 1

```
===== 9 =====
```
     """
     pos = 0
     while True:
-        match = text.find("{", pos)
+        match = text.rfind("{", pos)  # This will search for the last occurrence of '{' before the current position.
         if match == -1:
             break
         try:
```
```
def extract_json_objects(
    text: str, decoder=json.JSONDecoder()
) -> Iterator[dict[str, int | dict[Any, Any]]]:
    """Find JSON objects in text, and yield the decoded JSON data

    Does not attempt to look for JSON arrays, text, or other JSON types outside
    of a parent JSON object.

    """
    pos = 0
    while True:
        match = text.rfind("{", pos)  # This will search for the last occurrence of '{' before the current position.
        if match == -1:
            break
        try:
            result, index = decoder.raw_decode(text[match:])
            yield result
            pos = match + index
        except ValueError:
            pos = match + 1
```
