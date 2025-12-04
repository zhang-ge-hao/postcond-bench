https://github.com/askui/vision-agent/blob/83137b51e4a42cd62474541d4a4fa31240876560/./src/askui/utils/str_utils.py#L33-L73
```
@icontract.snapshot(
    lambda json_data, max_length, truncate_length, tag: (
        (lambda f: f(f, json_data))(
            lambda self, jd: (
                [(jd, len(jd) > max_length)]
                if isinstance(jd, str)
                else [
                    pair
                    for v in jd.values()
                    for pair in self(self, v)
                ] if isinstance(jd, dict)
                else [
                    pair
                    for item in jd
                    for pair in self(self, item)
                ] if isinstance(jd, list)
                else []
            )
        )
    ),
    name="orig_leaves",
)
@icontract.ensure(
    lambda json_data, result:
        isinstance(json_data, dict) == isinstance(result, dict)
        and isinstance(json_data, list) == isinstance(result, list)
        and isinstance(json_data, str) == isinstance(result, str)
)
@icontract.ensure(
    lambda json_data, result:
        not isinstance(json_data, dict)
        or json_data.keys() == result.keys()
)
@icontract.ensure(
    lambda json_data, result:
        not isinstance(json_data, list)
        or len(json_data) == len(result)
)
@icontract.ensure(
    lambda OLD, result, max_length, truncate_length, tag: (
        isinstance(truncate_length, int)
        and truncate_length >= 0
        and isinstance(tag, str)
        and (lambda new_strings: (
            len(new_strings) == len(OLD.orig_leaves)
            and all(
                (
                    (not is_long and new_s == orig_s)
                    or (
                        is_long
                        and new_s.startswith(orig_s[:truncate_length])
                        and new_s.endswith("... " + tag)
                        and len(new_s)
                        == min(truncate_length, len(orig_s)) + len("... " + tag)
                    )
                )
                for (orig_s, is_long), new_s in zip(OLD.orig_leaves, new_strings)
            )
        ))(
            (lambda f: f(f, result))(
                lambda self, jd: (
                    [jd]
                    if isinstance(jd, str)
                    else [
                        s
                        for v in jd.values()
                        for s in self(self, v)
                    ] if isinstance(jd, dict)
                    else [
                        s
                        for item in jd
                        for s in self(self, item)
                    ] if isinstance(jd, list)
                    else []
                )
            )
        )
    )
)
```
```
@icontract.snapshot(lambda json_data, max_length, truncate_length, tag: (lambda f: f(f, json_data))(lambda self, jd: ({k: self(self, v) for k, v in jd.items()} if isinstance(jd, dict) else [self(self, i) for i in jd] if isinstance(jd, list) else (jd[:truncate_length] + "... " + tag if isinstance(jd, str) and len(jd) > max_length else jd))), name="expected")
@icontract.ensure(lambda OLD, result: result == OLD.expected)
```
[7, 17]
===== 7 =====
```
     """
     if isinstance(json_data, dict):
         return {
-            k: truncate_long_strings(v, max_length, truncate_length, tag)
+            k: truncate_long_strings(v, max_length, truncate_length, None)
             for k, v in json_data.items()
         }
     if isinstance(json_data, list):
@@ -38,4 +38,4 @@         ]
     if isinstance(json_data, str) and len(json_data) > max_length:
         return f"{json_data[:truncate_length]}... {tag}"
-    return json_data+    return json_data
```
```
def truncate_long_strings(
    json_data: T,
    max_length: int = 100,
    truncate_length: int = 20,
    tag: str = "[shortened]",
) -> T:
    """
    Traverse and truncate long strings in JSON data.

    Args:
        json_data: The JSON data to process. Can be a dict, list, or str.
        max_length: Maximum length of a string before truncation occurs.
        truncate_length: Number of characters to keep when truncating.
        tag: Tag to append to truncated strings.

    Returns:
        Processed JSON data with truncated long strings. Returns the same type as input.

    Examples:
        >>> truncate_long_strings({"key": "a" * 101})
        {'key': 'aaaaaaaaaaaaaaaaaaaa... [shortened]'}

        >>> truncate_long_strings(["short", "a" * 101])
        ['short', 'aaaaaaaaaaaaaaaaaaaa... [shortened]']

        >>> truncate_long_strings("a" * 101)
        'aaaaaaaaaaaaaaaaaaaa... [shortened]'
    """
    if isinstance(json_data, dict):
        return {
            k: truncate_long_strings(v, max_length, truncate_length, None)
            for k, v in json_data.items()
        }
    if isinstance(json_data, list):
        return [
            truncate_long_strings(item, max_length, truncate_length, tag)
            for item in json_data
        ]
    if isinstance(json_data, str) and len(json_data) > max_length:
        return f"{json_data[:truncate_length]}... {tag}"
    return json_data

```
===== 17 =====
```
         }
     if isinstance(json_data, list):
         return [
-            truncate_long_strings(item, max_length, truncate_length, tag)
+            truncate_long_strings(item, max_length, truncate_length, None)
             for item in json_data
         ]
     if isinstance(json_data, str) and len(json_data) > max_length:
         return f"{json_data[:truncate_length]}... {tag}"
-    return json_data+    return json_data
```
```
def truncate_long_strings(
    json_data: T,
    max_length: int = 100,
    truncate_length: int = 20,
    tag: str = "[shortened]",
) -> T:
    """
    Traverse and truncate long strings in JSON data.

    Args:
        json_data: The JSON data to process. Can be a dict, list, or str.
        max_length: Maximum length of a string before truncation occurs.
        truncate_length: Number of characters to keep when truncating.
        tag: Tag to append to truncated strings.

    Returns:
        Processed JSON data with truncated long strings. Returns the same type as input.

    Examples:
        >>> truncate_long_strings({"key": "a" * 101})
        {'key': 'aaaaaaaaaaaaaaaaaaaa... [shortened]'}

        >>> truncate_long_strings(["short", "a" * 101])
        ['short', 'aaaaaaaaaaaaaaaaaaaa... [shortened]']

        >>> truncate_long_strings("a" * 101)
        'aaaaaaaaaaaaaaaaaaaa... [shortened]'
    """
    if isinstance(json_data, dict):
        return {
            k: truncate_long_strings(v, max_length, truncate_length, tag)
            for k, v in json_data.items()
        }
    if isinstance(json_data, list):
        return [
            truncate_long_strings(item, max_length, truncate_length, None)
            for item in json_data
        ]
    if isinstance(json_data, str) and len(json_data) > max_length:
        return f"{json_data[:truncate_length]}... {tag}"
    return json_data

```
