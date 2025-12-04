https://github.com/frostming/marko/blob/e2c502a0e0fa9b1b9de5135932c61593f7ea87f8/./marko/helpers.py#L87-L105
```
@icontract.snapshot(lambda text: text, name="orig_text")
@icontract.snapshot(lambda spaces: spaces, name="orig_spaces")
@icontract.ensure(
    lambda result, text, spaces: 
        isinstance(result, tuple) and len(result) == 3
        and
        result[0] + result[1] + result[2] == text
        and
        (result[1] == "") == (not any(c in spaces for c in text))
        and
        all(c not in spaces for c in result[0])
        and
        (result[1] == "" or all(c in spaces for c in result[1]))
        and
        (result[1] == "" or len(result[0]) == next((i for i, c in enumerate(text) if c in spaces), -1))
        and
        (result[1] == "" or (result[1] == text[len(result[0]): next((i for i in range(len(result[0]), len(text)) if text[i] not in spaces), len(text))] and result[2] == text[next((i for i in range(len(result[0]), len(text)) if text[i] not in spaces), len(text)) :]))
)
```
```
@icontract.snapshot(lambda text: text, name="orig_text")
@icontract.snapshot(lambda spaces: spaces, name="orig_spaces")
@icontract.ensure(lambda result: isinstance(result, tuple) and len(result) == 3)
@icontract.ensure(lambda result, text: result[0] + result[1] + result[2] == text)
@icontract.ensure(lambda result, text, spaces: (result[1] == "") == (not any(c in spaces for c in text)))
@icontract.ensure(lambda result, spaces: all(c not in spaces for c in result[0]))
@icontract.ensure(lambda result, spaces: result[1] == "" or all(c in spaces for c in result[1]))
@icontract.ensure(lambda result, text, spaces: result[1] == "" or len(result[0]) == next((i for i, c in enumerate(text) if c in spaces), -1))
@icontract.ensure(lambda result, text, spaces: result[1] == "" or (result[1] == text[len(result[0]): next((i for i in range(len(result[0]), len(text)) if text[i] not in spaces), len(text))] and result[2] == text[next((i for i in range(len(result[0]), len(text)) if text[i] not in spaces), len(text)) :]))
```
[7]
===== 7 =====
```
             start = i
         elif start >= 0:
             end = i
-            break
+            return
     if start < 0:
         return text, "", ""
     if end < 0:
         return text[:start], text[start:], ""
-    return text[:start], text[start:end], text[end:]+    return text[:start], text[start:end], text[end:]
```
```
def partition_by_spaces(text: str, spaces: str = " \t") -> tuple[str, str, str]:
    """Split the given text by spaces or tabs, and return a tuple of
    (start, delimiter, remaining). If spaces are not found, the latter
    two elements will be empty.
    """
    start = end = -1
    for i, c in enumerate(text):
        if c in spaces:
            if start >= 0:
                continue
            start = i
        elif start >= 0:
            end = i
            return
    if start < 0:
        return text, "", ""
    if end < 0:
        return text[:start], text[start:], ""
    return text[:start], text[start:end], text[end:]

```
