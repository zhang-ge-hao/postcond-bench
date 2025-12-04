https://github.com/falconry/falcon/blob/34b7d15d602e1b459cc65a1506a49730067938f2/./falcon/util/mediatypes.py#L42-L63
```
@icontract.ensure(lambda result: isinstance(result, tuple) and len(result) == 2)
@icontract.ensure(lambda result: isinstance(result[0], str))
@icontract.ensure(lambda result: isinstance(result[1], dict))
@icontract.ensure(lambda result, line: result[0] == line.split(';', 1)[0].strip())
@icontract.ensure(
    lambda result: all(
        isinstance(k, str) and k == k.lower() and k != '' for k in result[1].keys()
    )
)
@icontract.ensure(lambda result: all(isinstance(v, str) for v in result[1].values()))
@icontract.ensure(
    lambda result,
           line,
           _parse=_parse_param_old_stdlib,
           unquote=lambda raw: (
               raw[1:-1].replace('\\\\', '\\').replace('\\"', '"')
               if len(raw) >= 2 and raw[0] == raw[-1] == '"'
               else raw
           ): (
        (parts := tuple(_parse(';' + line))) is not None
        and result[0] == parts[0]
        and result[1]
        == {
            p.split('=', 1)[0].strip().lower(): 
                unquote(p.split('=', 1)[1].strip())
            for p in parts[1:]
            if '=' in p
        }
    )
)
```
```
@icontract.ensure(lambda result: isinstance(result, tuple) and len(result) == 2)
@icontract.ensure(lambda result: isinstance(result[0], str))
@icontract.ensure(lambda result: isinstance(result[1], dict))
@icontract.ensure(lambda result, line: result[0] == line.split(';', 1)[0].strip())
@icontract.ensure(lambda result: all(isinstance(k, str) and k == k.lower() and k != '' for k in result[1].keys()))
@icontract.ensure(lambda result: all(isinstance(v, str) for v in result[1].values()))
@icontract.ensure(lambda result, line: ('=' not in line) or (len(result[1]) > 0))
@icontract.ensure(lambda result, line: all(k in line.lower() for k in result[1].keys()))
```
[0, 1, 13, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 44, 45, 46, 47]
===== 0 =====
```
         This method has been copied (almost) verbatim from CPython 3.8 stdlib.
         It is slated for removal from the stdlib in 3.13.
     """
-    parts = _parse_param_old_stdlib(';' + line)
+    parts = _parse_param_old_stdlib(';' + line + ';')  # Adds an extra semicolon, which may lead to incorrect parsing
     key = parts.__next__()
     pdict: Dict[str, str] = {}
     for p in parts:
```
```
def _parse_header_old_stdlib(line: str) -> Tuple[str, Dict[str, str]]:
    """Parse a Content-type like header.

    Return the main content-type and a dictionary of options.

    Note:
        This method has been copied (almost) verbatim from CPython 3.8 stdlib.
        It is slated for removal from the stdlib in 3.13.
    """
    parts = _parse_param_old_stdlib(';' + line + ';')  # Adds an extra semicolon, which may lead to incorrect parsing
    key = parts.__next__()
    pdict: Dict[str, str] = {}
    for p in parts:
        i = p.find('=')
        if i >= 0:
            name = p[:i].strip().lower()
            value = p[i + 1 :].strip()
            if len(value) >= 2 and value[0] == value[-1] == '"':
                value = value[1:-1]
                value = value.replace('\\\\', '\\').replace('\\"', '"')
            pdict[name] = value
    return key, pdict
```
===== 1 =====
```
         This method has been copied (almost) verbatim from CPython 3.8 stdlib.
         It is slated for removal from the stdlib in 3.13.
     """
-    parts = _parse_param_old_stdlib(';' + line)
+    parts = _parse_param_old_stdlib(';' + line.lower())  # Converts the entire line to lowercase, affecting case-sensitive parameters
     key = parts.__next__()
     pdict: Dict[str, str] = {}
     for p in parts:
```
```
def _parse_header_old_stdlib(line: str) -> Tuple[str, Dict[str, str]]:
    """Parse a Content-type like header.

    Return the main content-type and a dictionary of options.

    Note:
        This method has been copied (almost) verbatim from CPython 3.8 stdlib.
        It is slated for removal from the stdlib in 3.13.
    """
    parts = _parse_param_old_stdlib(';' + line.lower())  # Converts the entire line to lowercase, affecting case-sensitive parameters
    key = parts.__next__()
    pdict: Dict[str, str] = {}
    for p in parts:
        i = p.find('=')
        if i >= 0:
            name = p[:i].strip().lower()
            value = p[i + 1 :].strip()
            if len(value) >= 2 and value[0] == value[-1] == '"':
                value = value[1:-1]
                value = value.replace('\\\\', '\\').replace('\\"', '"')
            pdict[name] = value
    return key, pdict
```
===== 13 =====
```
     for p in parts:
         i = p.find('=')
         if i >= 0:
-            name = p[:i].strip().lower()
+            name = None
             value = p[i + 1 :].strip()
             if len(value) >= 2 and value[0] == value[-1] == '"':
                 value = value[1:-1]
                 value = value.replace('\\\\', '\\').replace('\\"', '"')
             pdict[name] = value
-    return key, pdict+    return key, pdict
```
```
def _parse_header_old_stdlib(line: str) -> Tuple[str, Dict[str, str]]:
    """Parse a Content-type like header.

    Return the main content-type and a dictionary of options.

    Note:
        This method has been copied (almost) verbatim from CPython 3.8 stdlib.
        It is slated for removal from the stdlib in 3.13.
    """
    parts = _parse_param_old_stdlib(';' + line)
    key = parts.__next__()
    pdict: Dict[str, str] = {}
    for p in parts:
        i = p.find('=')
        if i >= 0:
            name = None
            value = p[i + 1 :].strip()
            if len(value) >= 2 and value[0] == value[-1] == '"':
                value = value[1:-1]
                value = value.replace('\\\\', '\\').replace('\\"', '"')
            pdict[name] = value
    return key, pdict

```
===== 20 =====
```
         i = p.find('=')
         if i >= 0:
             name = p[:i].strip().lower()
-            value = p[i + 1 :].strip()
+            value = p[i + 1 :].strip() + 'extra'  # Appends 'extra' to the value, introducing incorrect data.
             if len(value) >= 2 and value[0] == value[-1] == '"':
                 value = value[1:-1]
                 value = value.replace('\\\\', '\\').replace('\\"', '"')
```
```
def _parse_header_old_stdlib(line: str) -> Tuple[str, Dict[str, str]]:
    """Parse a Content-type like header.

    Return the main content-type and a dictionary of options.

    Note:
        This method has been copied (almost) verbatim from CPython 3.8 stdlib.
        It is slated for removal from the stdlib in 3.13.
    """
    parts = _parse_param_old_stdlib(';' + line)
    key = parts.__next__()
    pdict: Dict[str, str] = {}
    for p in parts:
        i = p.find('=')
        if i >= 0:
            name = p[:i].strip().lower()
            value = p[i + 1 :].strip() + 'extra'  # Appends 'extra' to the value, introducing incorrect data.
            if len(value) >= 2 and value[0] == value[-1] == '"':
                value = value[1:-1]
                value = value.replace('\\\\', '\\').replace('\\"', '"')
            pdict[name] = value
    return key, pdict
```
===== 21 =====
```
         i = p.find('=')
         if i >= 0:
             name = p[:i].strip().lower()
-            value = p[i + 1 :].strip()
+            value = p[i + 1 :].strip() if p[i + 1 :].strip() else 'default'  # Sets a default value if the parsed value is empty, which may not be desired.
             if len(value) >= 2 and value[0] == value[-1] == '"':
                 value = value[1:-1]
                 value = value.replace('\\\\', '\\').replace('\\"', '"')
```
```
def _parse_header_old_stdlib(line: str) -> Tuple[str, Dict[str, str]]:
    """Parse a Content-type like header.

    Return the main content-type and a dictionary of options.

    Note:
        This method has been copied (almost) verbatim from CPython 3.8 stdlib.
        It is slated for removal from the stdlib in 3.13.
    """
    parts = _parse_param_old_stdlib(';' + line)
    key = parts.__next__()
    pdict: Dict[str, str] = {}
    for p in parts:
        i = p.find('=')
        if i >= 0:
            name = p[:i].strip().lower()
            value = p[i + 1 :].strip() if p[i + 1 :].strip() else 'default'  # Sets a default value if the parsed value is empty, which may not be desired.
            if len(value) >= 2 and value[0] == value[-1] == '"':
                value = value[1:-1]
                value = value.replace('\\\\', '\\').replace('\\"', '"')
            pdict[name] = value
    return key, pdict
```
===== 22 =====
```
         i = p.find('=')
         if i >= 0:
             name = p[:i].strip().lower()
-            value = p[i + 1 :].strip()
+            value = p[i + 1 :].strip().replace(' ', '_')  # Replaces spaces with underscores, altering the intended value format.
             if len(value) >= 2 and value[0] == value[-1] == '"':
                 value = value[1:-1]
                 value = value.replace('\\\\', '\\').replace('\\"', '"')
```
```
def _parse_header_old_stdlib(line: str) -> Tuple[str, Dict[str, str]]:
    """Parse a Content-type like header.

    Return the main content-type and a dictionary of options.

    Note:
        This method has been copied (almost) verbatim from CPython 3.8 stdlib.
        It is slated for removal from the stdlib in 3.13.
    """
    parts = _parse_param_old_stdlib(';' + line)
    key = parts.__next__()
    pdict: Dict[str, str] = {}
    for p in parts:
        i = p.find('=')
        if i >= 0:
            name = p[:i].strip().lower()
            value = p[i + 1 :].strip().replace(' ', '_')  # Replaces spaces with underscores, altering the intended value format.
            if len(value) >= 2 and value[0] == value[-1] == '"':
                value = value[1:-1]
                value = value.replace('\\\\', '\\').replace('\\"', '"')
            pdict[name] = value
    return key, pdict
```
===== 23 =====
```
         i = p.find('=')
         if i >= 0:
             name = p[:i].strip().lower()
-            value = p[i + 1 :].strip()
+            value = p[i + 1 :].strip().upper()  # Converts the value to uppercase, which may not be intended.
             if len(value) >= 2 and value[0] == value[-1] == '"':
                 value = value[1:-1]
                 value = value.replace('\\\\', '\\').replace('\\"', '"')
```
```
def _parse_header_old_stdlib(line: str) -> Tuple[str, Dict[str, str]]:
    """Parse a Content-type like header.

    Return the main content-type and a dictionary of options.

    Note:
        This method has been copied (almost) verbatim from CPython 3.8 stdlib.
        It is slated for removal from the stdlib in 3.13.
    """
    parts = _parse_param_old_stdlib(';' + line)
    key = parts.__next__()
    pdict: Dict[str, str] = {}
    for p in parts:
        i = p.find('=')
        if i >= 0:
            name = p[:i].strip().lower()
            value = p[i + 1 :].strip().upper()  # Converts the value to uppercase, which may not be intended.
            if len(value) >= 2 and value[0] == value[-1] == '"':
                value = value[1:-1]
                value = value.replace('\\\\', '\\').replace('\\"', '"')
            pdict[name] = value
    return key, pdict
```
===== 24 =====
```
         i = p.find('=')
         if i >= 0:
             name = p[:i].strip().lower()
-            value = p[i + 1 :].strip()
+            value = p[i + 1 :].strip()[:5]  # Truncates the value to the first 5 characters, potentially losing important data.
             if len(value) >= 2 and value[0] == value[-1] == '"':
                 value = value[1:-1]
                 value = value.replace('\\\\', '\\').replace('\\"', '"')
```
```
def _parse_header_old_stdlib(line: str) -> Tuple[str, Dict[str, str]]:
    """Parse a Content-type like header.

    Return the main content-type and a dictionary of options.

    Note:
        This method has been copied (almost) verbatim from CPython 3.8 stdlib.
        It is slated for removal from the stdlib in 3.13.
    """
    parts = _parse_param_old_stdlib(';' + line)
    key = parts.__next__()
    pdict: Dict[str, str] = {}
    for p in parts:
        i = p.find('=')
        if i >= 0:
            name = p[:i].strip().lower()
            value = p[i + 1 :].strip()[:5]  # Truncates the value to the first 5 characters, potentially losing important data.
            if len(value) >= 2 and value[0] == value[-1] == '"':
                value = value[1:-1]
                value = value.replace('\\\\', '\\').replace('\\"', '"')
            pdict[name] = value
    return key, pdict
```
===== 25 =====
```
         i = p.find('=')
         if i >= 0:
             name = p[:i].strip().lower()
-            value = p[i + 1 :].strip()
+            value = p[i + 2 :].strip()
             if len(value) >= 2 and value[0] == value[-1] == '"':
                 value = value[1:-1]
                 value = value.replace('\\\\', '\\').replace('\\"', '"')
             pdict[name] = value
-    return key, pdict+    return key, pdict
```
```
def _parse_header_old_stdlib(line: str) -> Tuple[str, Dict[str, str]]:
    """Parse a Content-type like header.

    Return the main content-type and a dictionary of options.

    Note:
        This method has been copied (almost) verbatim from CPython 3.8 stdlib.
        It is slated for removal from the stdlib in 3.13.
    """
    parts = _parse_param_old_stdlib(';' + line)
    key = parts.__next__()
    pdict: Dict[str, str] = {}
    for p in parts:
        i = p.find('=')
        if i >= 0:
            name = p[:i].strip().lower()
            value = p[i + 2 :].strip()
            if len(value) >= 2 and value[0] == value[-1] == '"':
                value = value[1:-1]
                value = value.replace('\\\\', '\\').replace('\\"', '"')
            pdict[name] = value
    return key, pdict

```
===== 26 =====
```
         i = p.find('=')
         if i >= 0:
             name = p[:i].strip().lower()
-            value = p[i + 1 :].strip()
+            value = p[i - 1 :].strip()
             if len(value) >= 2 and value[0] == value[-1] == '"':
                 value = value[1:-1]
                 value = value.replace('\\\\', '\\').replace('\\"', '"')
             pdict[name] = value
-    return key, pdict+    return key, pdict
```
```
def _parse_header_old_stdlib(line: str) -> Tuple[str, Dict[str, str]]:
    """Parse a Content-type like header.

    Return the main content-type and a dictionary of options.

    Note:
        This method has been copied (almost) verbatim from CPython 3.8 stdlib.
        It is slated for removal from the stdlib in 3.13.
    """
    parts = _parse_param_old_stdlib(';' + line)
    key = parts.__next__()
    pdict: Dict[str, str] = {}
    for p in parts:
        i = p.find('=')
        if i >= 0:
            name = p[:i].strip().lower()
            value = p[i - 1 :].strip()
            if len(value) >= 2 and value[0] == value[-1] == '"':
                value = value[1:-1]
                value = value.replace('\\\\', '\\').replace('\\"', '"')
            pdict[name] = value
    return key, pdict

```
===== 27 =====
```
         if i >= 0:
             name = p[:i].strip().lower()
             value = p[i + 1 :].strip()
-            if len(value) >= 2 and value[0] == value[-1] == '"':
+            if len(value) == 0 or value[0] == value[-1] == '"':
                 value = value[1:-1]
                 value = value.replace('\\\\', '\\').replace('\\"', '"')
             pdict[name] = value
```
```
def _parse_header_old_stdlib(line: str) -> Tuple[str, Dict[str, str]]:
    """Parse a Content-type like header.

    Return the main content-type and a dictionary of options.

    Note:
        This method has been copied (almost) verbatim from CPython 3.8 stdlib.
        It is slated for removal from the stdlib in 3.13.
    """
    parts = _parse_param_old_stdlib(';' + line)
    key = parts.__next__()
    pdict: Dict[str, str] = {}
    for p in parts:
        i = p.find('=')
        if i >= 0:
            name = p[:i].strip().lower()
            value = p[i + 1 :].strip()
            if len(value) == 0 or value[0] == value[-1] == '"':
                value = value[1:-1]
                value = value.replace('\\\\', '\\').replace('\\"', '"')
            pdict[name] = value
    return key, pdict
```
===== 28 =====
```
         if i >= 0:
             name = p[:i].strip().lower()
             value = p[i + 1 :].strip()
-            if len(value) >= 2 and value[0] == value[-1] == '"':
+            if len(value) > 2 and value[0] == value[-1] == '"':
                 value = value[1:-1]
                 value = value.replace('\\\\', '\\').replace('\\"', '"')
             pdict[name] = value
```
```
def _parse_header_old_stdlib(line: str) -> Tuple[str, Dict[str, str]]:
    """Parse a Content-type like header.

    Return the main content-type and a dictionary of options.

    Note:
        This method has been copied (almost) verbatim from CPython 3.8 stdlib.
        It is slated for removal from the stdlib in 3.13.
    """
    parts = _parse_param_old_stdlib(';' + line)
    key = parts.__next__()
    pdict: Dict[str, str] = {}
    for p in parts:
        i = p.find('=')
        if i >= 0:
            name = p[:i].strip().lower()
            value = p[i + 1 :].strip()
            if len(value) > 2 and value[0] == value[-1] == '"':
                value = value[1:-1]
                value = value.replace('\\\\', '\\').replace('\\"', '"')
            pdict[name] = value
    return key, pdict
```
===== 29 =====
```
         if i >= 0:
             name = p[:i].strip().lower()
             value = p[i + 1 :].strip()
-            if len(value) >= 2 and value[0] == value[-1] == '"':
+            if len(value) > 2 and value[0] == value[-1] == '"':
                 value = value[1:-1]
                 value = value.replace('\\\\', '\\').replace('\\"', '"')
             pdict[name] = value
-    return key, pdict+    return key, pdict
```
```
def _parse_header_old_stdlib(line: str) -> Tuple[str, Dict[str, str]]:
    """Parse a Content-type like header.

    Return the main content-type and a dictionary of options.

    Note:
        This method has been copied (almost) verbatim from CPython 3.8 stdlib.
        It is slated for removal from the stdlib in 3.13.
    """
    parts = _parse_param_old_stdlib(';' + line)
    key = parts.__next__()
    pdict: Dict[str, str] = {}
    for p in parts:
        i = p.find('=')
        if i >= 0:
            name = p[:i].strip().lower()
            value = p[i + 1 :].strip()
            if len(value) > 2 and value[0] == value[-1] == '"':
                value = value[1:-1]
                value = value.replace('\\\\', '\\').replace('\\"', '"')
            pdict[name] = value
    return key, pdict

```
===== 30 =====
```
         if i >= 0:
             name = p[:i].strip().lower()
             value = p[i + 1 :].strip()
-            if len(value) >= 2 and value[0] == value[-1] == '"':
+            if len(value) >= 2 and value[0] != value[-1] == '"':
                 value = value[1:-1]
                 value = value.replace('\\\\', '\\').replace('\\"', '"')
             pdict[name] = value
-    return key, pdict+    return key, pdict
```
```
def _parse_header_old_stdlib(line: str) -> Tuple[str, Dict[str, str]]:
    """Parse a Content-type like header.

    Return the main content-type and a dictionary of options.

    Note:
        This method has been copied (almost) verbatim from CPython 3.8 stdlib.
        It is slated for removal from the stdlib in 3.13.
    """
    parts = _parse_param_old_stdlib(';' + line)
    key = parts.__next__()
    pdict: Dict[str, str] = {}
    for p in parts:
        i = p.find('=')
        if i >= 0:
            name = p[:i].strip().lower()
            value = p[i + 1 :].strip()
            if len(value) >= 2 and value[0] != value[-1] == '"':
                value = value[1:-1]
                value = value.replace('\\\\', '\\').replace('\\"', '"')
            pdict[name] = value
    return key, pdict

```
===== 31 =====
```
         if i >= 0:
             name = p[:i].strip().lower()
             value = p[i + 1 :].strip()
-            if len(value) >= 2 and value[0] == value[-1] == '"':
+            if len(value) >= 2 and value[0] == '"' and value[-1] == "'":
                 value = value[1:-1]
                 value = value.replace('\\\\', '\\').replace('\\"', '"')
             pdict[name] = value
```
```
def _parse_header_old_stdlib(line: str) -> Tuple[str, Dict[str, str]]:
    """Parse a Content-type like header.

    Return the main content-type and a dictionary of options.

    Note:
        This method has been copied (almost) verbatim from CPython 3.8 stdlib.
        It is slated for removal from the stdlib in 3.13.
    """
    parts = _parse_param_old_stdlib(';' + line)
    key = parts.__next__()
    pdict: Dict[str, str] = {}
    for p in parts:
        i = p.find('=')
        if i >= 0:
            name = p[:i].strip().lower()
            value = p[i + 1 :].strip()
            if len(value) >= 2 and value[0] == '"' and value[-1] == "'":
                value = value[1:-1]
                value = value.replace('\\\\', '\\').replace('\\"', '"')
            pdict[name] = value
    return key, pdict
```
===== 32 =====
```
         if i >= 0:
             name = p[:i].strip().lower()
             value = p[i + 1 :].strip()
-            if len(value) >= 2 and value[0] == value[-1] == '"':
+            if len(value) >= 2 and value[0] == value[+1] == '"':
                 value = value[1:-1]
                 value = value.replace('\\\\', '\\').replace('\\"', '"')
             pdict[name] = value
-    return key, pdict+    return key, pdict
```
```
def _parse_header_old_stdlib(line: str) -> Tuple[str, Dict[str, str]]:
    """Parse a Content-type like header.

    Return the main content-type and a dictionary of options.

    Note:
        This method has been copied (almost) verbatim from CPython 3.8 stdlib.
        It is slated for removal from the stdlib in 3.13.
    """
    parts = _parse_param_old_stdlib(';' + line)
    key = parts.__next__()
    pdict: Dict[str, str] = {}
    for p in parts:
        i = p.find('=')
        if i >= 0:
            name = p[:i].strip().lower()
            value = p[i + 1 :].strip()
            if len(value) >= 2 and value[0] == value[+1] == '"':
                value = value[1:-1]
                value = value.replace('\\\\', '\\').replace('\\"', '"')
            pdict[name] = value
    return key, pdict

```
===== 33 =====
```
         if i >= 0:
             name = p[:i].strip().lower()
             value = p[i + 1 :].strip()
-            if len(value) >= 2 and value[0] == value[-1] == '"':
+            if len(value) >= 2 and value[0] == value[-1] != '"':
                 value = value[1:-1]
                 value = value.replace('\\\\', '\\').replace('\\"', '"')
             pdict[name] = value
```
```
def _parse_header_old_stdlib(line: str) -> Tuple[str, Dict[str, str]]:
    """Parse a Content-type like header.

    Return the main content-type and a dictionary of options.

    Note:
        This method has been copied (almost) verbatim from CPython 3.8 stdlib.
        It is slated for removal from the stdlib in 3.13.
    """
    parts = _parse_param_old_stdlib(';' + line)
    key = parts.__next__()
    pdict: Dict[str, str] = {}
    for p in parts:
        i = p.find('=')
        if i >= 0:
            name = p[:i].strip().lower()
            value = p[i + 1 :].strip()
            if len(value) >= 2 and value[0] == value[-1] != '"':
                value = value[1:-1]
                value = value.replace('\\\\', '\\').replace('\\"', '"')
            pdict[name] = value
    return key, pdict
```
===== 34 =====
```
         if i >= 0:
             name = p[:i].strip().lower()
             value = p[i + 1 :].strip()
-            if len(value) >= 2 and value[0] == value[-1] == '"':
+            if len(value) >= 2 and value[0] == value[-1] != '"':
                 value = value[1:-1]
                 value = value.replace('\\\\', '\\').replace('\\"', '"')
             pdict[name] = value
-    return key, pdict+    return key, pdict
```
```
def _parse_header_old_stdlib(line: str) -> Tuple[str, Dict[str, str]]:
    """Parse a Content-type like header.

    Return the main content-type and a dictionary of options.

    Note:
        This method has been copied (almost) verbatim from CPython 3.8 stdlib.
        It is slated for removal from the stdlib in 3.13.
    """
    parts = _parse_param_old_stdlib(';' + line)
    key = parts.__next__()
    pdict: Dict[str, str] = {}
    for p in parts:
        i = p.find('=')
        if i >= 0:
            name = p[:i].strip().lower()
            value = p[i + 1 :].strip()
            if len(value) >= 2 and value[0] == value[-1] != '"':
                value = value[1:-1]
                value = value.replace('\\\\', '\\').replace('\\"', '"')
            pdict[name] = value
    return key, pdict

```
===== 35 =====
```
         if i >= 0:
             name = p[:i].strip().lower()
             value = p[i + 1 :].strip()
-            if len(value) >= 2 and value[0] == value[-1] == '"':
+            if len(value) >= 2 and value[0] == value[-1] == 'XX"XX':
                 value = value[1:-1]
                 value = value.replace('\\\\', '\\').replace('\\"', '"')
             pdict[name] = value
-    return key, pdict+    return key, pdict
```
```
def _parse_header_old_stdlib(line: str) -> Tuple[str, Dict[str, str]]:
    """Parse a Content-type like header.

    Return the main content-type and a dictionary of options.

    Note:
        This method has been copied (almost) verbatim from CPython 3.8 stdlib.
        It is slated for removal from the stdlib in 3.13.
    """
    parts = _parse_param_old_stdlib(';' + line)
    key = parts.__next__()
    pdict: Dict[str, str] = {}
    for p in parts:
        i = p.find('=')
        if i >= 0:
            name = p[:i].strip().lower()
            value = p[i + 1 :].strip()
            if len(value) >= 2 and value[0] == value[-1] == 'XX"XX':
                value = value[1:-1]
                value = value.replace('\\\\', '\\').replace('\\"', '"')
            pdict[name] = value
    return key, pdict

```
===== 36 =====
```
         if i >= 0:
             name = p[:i].strip().lower()
             value = p[i + 1 :].strip()
-            if len(value) >= 2 and value[0] == value[-1] == '"':
+            if len(value) >= 2 and value[0] == value[-2] == '"':
                 value = value[1:-1]
                 value = value.replace('\\\\', '\\').replace('\\"', '"')
             pdict[name] = value
-    return key, pdict+    return key, pdict
```
```
def _parse_header_old_stdlib(line: str) -> Tuple[str, Dict[str, str]]:
    """Parse a Content-type like header.

    Return the main content-type and a dictionary of options.

    Note:
        This method has been copied (almost) verbatim from CPython 3.8 stdlib.
        It is slated for removal from the stdlib in 3.13.
    """
    parts = _parse_param_old_stdlib(';' + line)
    key = parts.__next__()
    pdict: Dict[str, str] = {}
    for p in parts:
        i = p.find('=')
        if i >= 0:
            name = p[:i].strip().lower()
            value = p[i + 1 :].strip()
            if len(value) >= 2 and value[0] == value[-2] == '"':
                value = value[1:-1]
                value = value.replace('\\\\', '\\').replace('\\"', '"')
            pdict[name] = value
    return key, pdict

```
===== 37 =====
```
         if i >= 0:
             name = p[:i].strip().lower()
             value = p[i + 1 :].strip()
-            if len(value) >= 2 and value[0] == value[-1] == '"':
+            if len(value) >= 2 and value[0] == value[1] == '"':
                 value = value[1:-1]
                 value = value.replace('\\\\', '\\').replace('\\"', '"')
             pdict[name] = value
```
```
def _parse_header_old_stdlib(line: str) -> Tuple[str, Dict[str, str]]:
    """Parse a Content-type like header.

    Return the main content-type and a dictionary of options.

    Note:
        This method has been copied (almost) verbatim from CPython 3.8 stdlib.
        It is slated for removal from the stdlib in 3.13.
    """
    parts = _parse_param_old_stdlib(';' + line)
    key = parts.__next__()
    pdict: Dict[str, str] = {}
    for p in parts:
        i = p.find('=')
        if i >= 0:
            name = p[:i].strip().lower()
            value = p[i + 1 :].strip()
            if len(value) >= 2 and value[0] == value[1] == '"':
                value = value[1:-1]
                value = value.replace('\\\\', '\\').replace('\\"', '"')
            pdict[name] = value
    return key, pdict
```
===== 38 =====
```
         if i >= 0:
             name = p[:i].strip().lower()
             value = p[i + 1 :].strip()
-            if len(value) >= 2 and value[0] == value[-1] == '"':
+            if len(value) >= 2 and value[1] == value[-1] == '"':
                 value = value[1:-1]
                 value = value.replace('\\\\', '\\').replace('\\"', '"')
             pdict[name] = value
-    return key, pdict+    return key, pdict
```
```
def _parse_header_old_stdlib(line: str) -> Tuple[str, Dict[str, str]]:
    """Parse a Content-type like header.

    Return the main content-type and a dictionary of options.

    Note:
        This method has been copied (almost) verbatim from CPython 3.8 stdlib.
        It is slated for removal from the stdlib in 3.13.
    """
    parts = _parse_param_old_stdlib(';' + line)
    key = parts.__next__()
    pdict: Dict[str, str] = {}
    for p in parts:
        i = p.find('=')
        if i >= 0:
            name = p[:i].strip().lower()
            value = p[i + 1 :].strip()
            if len(value) >= 2 and value[1] == value[-1] == '"':
                value = value[1:-1]
                value = value.replace('\\\\', '\\').replace('\\"', '"')
            pdict[name] = value
    return key, pdict

```
===== 39 =====
```
         if i >= 0:
             name = p[:i].strip().lower()
             value = p[i + 1 :].strip()
-            if len(value) >= 2 and value[0] == value[-1] == '"':
+            if len(value) >= 3 and value[0] == value[-1] == '"':
                 value = value[1:-1]
                 value = value.replace('\\\\', '\\').replace('\\"', '"')
             pdict[name] = value
-    return key, pdict+    return key, pdict
```
```
def _parse_header_old_stdlib(line: str) -> Tuple[str, Dict[str, str]]:
    """Parse a Content-type like header.

    Return the main content-type and a dictionary of options.

    Note:
        This method has been copied (almost) verbatim from CPython 3.8 stdlib.
        It is slated for removal from the stdlib in 3.13.
    """
    parts = _parse_param_old_stdlib(';' + line)
    key = parts.__next__()
    pdict: Dict[str, str] = {}
    for p in parts:
        i = p.find('=')
        if i >= 0:
            name = p[:i].strip().lower()
            value = p[i + 1 :].strip()
            if len(value) >= 3 and value[0] == value[-1] == '"':
                value = value[1:-1]
                value = value.replace('\\\\', '\\').replace('\\"', '"')
            pdict[name] = value
    return key, pdict

```
===== 40 =====
```
             name = p[:i].strip().lower()
             value = p[i + 1 :].strip()
             if len(value) >= 2 and value[0] == value[-1] == '"':
-                value = value[1:-1]
+                value = value[1:+1]
                 value = value.replace('\\\\', '\\').replace('\\"', '"')
             pdict[name] = value
-    return key, pdict+    return key, pdict
```
```
def _parse_header_old_stdlib(line: str) -> Tuple[str, Dict[str, str]]:
    """Parse a Content-type like header.

    Return the main content-type and a dictionary of options.

    Note:
        This method has been copied (almost) verbatim from CPython 3.8 stdlib.
        It is slated for removal from the stdlib in 3.13.
    """
    parts = _parse_param_old_stdlib(';' + line)
    key = parts.__next__()
    pdict: Dict[str, str] = {}
    for p in parts:
        i = p.find('=')
        if i >= 0:
            name = p[:i].strip().lower()
            value = p[i + 1 :].strip()
            if len(value) >= 2 and value[0] == value[-1] == '"':
                value = value[1:+1]
                value = value.replace('\\\\', '\\').replace('\\"', '"')
            pdict[name] = value
    return key, pdict

```
===== 41 =====
```
             name = p[:i].strip().lower()
             value = p[i + 1 :].strip()
             if len(value) >= 2 and value[0] == value[-1] == '"':
-                value = value[1:-1]
+                value = value[1:-2]
                 value = value.replace('\\\\', '\\').replace('\\"', '"')
             pdict[name] = value
-    return key, pdict+    return key, pdict
```
```
def _parse_header_old_stdlib(line: str) -> Tuple[str, Dict[str, str]]:
    """Parse a Content-type like header.

    Return the main content-type and a dictionary of options.

    Note:
        This method has been copied (almost) verbatim from CPython 3.8 stdlib.
        It is slated for removal from the stdlib in 3.13.
    """
    parts = _parse_param_old_stdlib(';' + line)
    key = parts.__next__()
    pdict: Dict[str, str] = {}
    for p in parts:
        i = p.find('=')
        if i >= 0:
            name = p[:i].strip().lower()
            value = p[i + 1 :].strip()
            if len(value) >= 2 and value[0] == value[-1] == '"':
                value = value[1:-2]
                value = value.replace('\\\\', '\\').replace('\\"', '"')
            pdict[name] = value
    return key, pdict

```
===== 42 =====
```
             name = p[:i].strip().lower()
             value = p[i + 1 :].strip()
             if len(value) >= 2 and value[0] == value[-1] == '"':
-                value = value[1:-1]
+                value = value[2:-1]
                 value = value.replace('\\\\', '\\').replace('\\"', '"')
             pdict[name] = value
-    return key, pdict+    return key, pdict
```
```
def _parse_header_old_stdlib(line: str) -> Tuple[str, Dict[str, str]]:
    """Parse a Content-type like header.

    Return the main content-type and a dictionary of options.

    Note:
        This method has been copied (almost) verbatim from CPython 3.8 stdlib.
        It is slated for removal from the stdlib in 3.13.
    """
    parts = _parse_param_old_stdlib(';' + line)
    key = parts.__next__()
    pdict: Dict[str, str] = {}
    for p in parts:
        i = p.find('=')
        if i >= 0:
            name = p[:i].strip().lower()
            value = p[i + 1 :].strip()
            if len(value) >= 2 and value[0] == value[-1] == '"':
                value = value[2:-1]
                value = value.replace('\\\\', '\\').replace('\\"', '"')
            pdict[name] = value
    return key, pdict

```
===== 44 =====
```
             value = p[i + 1 :].strip()
             if len(value) >= 2 and value[0] == value[-1] == '"':
                 value = value[1:-1]
-                value = value.replace('\\\\', '\\').replace('\\"', '"')
+                value = value.replace('\\\\', '\\').replace('XX\\"XX', '"')
             pdict[name] = value
-    return key, pdict+    return key, pdict
```
```
def _parse_header_old_stdlib(line: str) -> Tuple[str, Dict[str, str]]:
    """Parse a Content-type like header.

    Return the main content-type and a dictionary of options.

    Note:
        This method has been copied (almost) verbatim from CPython 3.8 stdlib.
        It is slated for removal from the stdlib in 3.13.
    """
    parts = _parse_param_old_stdlib(';' + line)
    key = parts.__next__()
    pdict: Dict[str, str] = {}
    for p in parts:
        i = p.find('=')
        if i >= 0:
            name = p[:i].strip().lower()
            value = p[i + 1 :].strip()
            if len(value) >= 2 and value[0] == value[-1] == '"':
                value = value[1:-1]
                value = value.replace('\\\\', '\\').replace('XX\\"XX', '"')
            pdict[name] = value
    return key, pdict

```
===== 45 =====
```
             value = p[i + 1 :].strip()
             if len(value) >= 2 and value[0] == value[-1] == '"':
                 value = value[1:-1]
-                value = value.replace('\\\\', '\\').replace('\\"', '"')
+                value = value.replace('\\\\', '\\').replace('\\"', '')
             pdict[name] = value
     return key, pdict
```
```
def _parse_header_old_stdlib(line: str) -> Tuple[str, Dict[str, str]]:
    """Parse a Content-type like header.

    Return the main content-type and a dictionary of options.

    Note:
        This method has been copied (almost) verbatim from CPython 3.8 stdlib.
        It is slated for removal from the stdlib in 3.13.
    """
    parts = _parse_param_old_stdlib(';' + line)
    key = parts.__next__()
    pdict: Dict[str, str] = {}
    for p in parts:
        i = p.find('=')
        if i >= 0:
            name = p[:i].strip().lower()
            value = p[i + 1 :].strip()
            if len(value) >= 2 and value[0] == value[-1] == '"':
                value = value[1:-1]
                value = value.replace('\\\\', '\\').replace('\\"', '')
            pdict[name] = value
    return key, pdict
```
===== 46 =====
```
             value = p[i + 1 :].strip()
             if len(value) >= 2 and value[0] == value[-1] == '"':
                 value = value[1:-1]
-                value = value.replace('\\\\', '\\').replace('\\"', '"')
+                value = value.replace('\\\\', '\\').replace('\\"', 'XX"XX')
             pdict[name] = value
-    return key, pdict+    return key, pdict
```
```
def _parse_header_old_stdlib(line: str) -> Tuple[str, Dict[str, str]]:
    """Parse a Content-type like header.

    Return the main content-type and a dictionary of options.

    Note:
        This method has been copied (almost) verbatim from CPython 3.8 stdlib.
        It is slated for removal from the stdlib in 3.13.
    """
    parts = _parse_param_old_stdlib(';' + line)
    key = parts.__next__()
    pdict: Dict[str, str] = {}
    for p in parts:
        i = p.find('=')
        if i >= 0:
            name = p[:i].strip().lower()
            value = p[i + 1 :].strip()
            if len(value) >= 2 and value[0] == value[-1] == '"':
                value = value[1:-1]
                value = value.replace('\\\\', '\\').replace('\\"', 'XX"XX')
            pdict[name] = value
    return key, pdict

```
===== 47 =====
```
             value = p[i + 1 :].strip()
             if len(value) >= 2 and value[0] == value[-1] == '"':
                 value = value[1:-1]
-                value = value.replace('\\\\', '\\').replace('\\"', '"')
+                value = value.replace('\\\\', '\\').replace('\\"', '\\')
             pdict[name] = value
     return key, pdict
```
```
def _parse_header_old_stdlib(line: str) -> Tuple[str, Dict[str, str]]:
    """Parse a Content-type like header.

    Return the main content-type and a dictionary of options.

    Note:
        This method has been copied (almost) verbatim from CPython 3.8 stdlib.
        It is slated for removal from the stdlib in 3.13.
    """
    parts = _parse_param_old_stdlib(';' + line)
    key = parts.__next__()
    pdict: Dict[str, str] = {}
    for p in parts:
        i = p.find('=')
        if i >= 0:
            name = p[:i].strip().lower()
            value = p[i + 1 :].strip()
            if len(value) >= 2 and value[0] == value[-1] == '"':
                value = value[1:-1]
                value = value.replace('\\\\', '\\').replace('\\"', '\\')
            pdict[name] = value
    return key, pdict
```
