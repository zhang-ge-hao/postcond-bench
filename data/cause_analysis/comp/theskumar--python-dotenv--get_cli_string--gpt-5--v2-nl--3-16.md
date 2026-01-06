https://github.com/theskumar/python-dotenv/blob/85f43295ccb2d15d13da370954e5b85079f4a56c/./src/dotenv/__init__.py#L12-L39
```
@icontract.ensure(lambda result: isinstance(result, str))
```
```
return value - primitive-like/scalar types


return value content

primitive-like/scalar types
```
passed
```
@icontract.ensure(lambda result, path, action, key, value, quote: result == " ".join(["dotenv"] + (["-q " + quote] if quote else []) + (["-f " + path] if path else []) + (([action] + ([key] + ((['"' + value + '"'] if (value and " " in value) else ([value] if value else []))) if key else [])) if action else [])).strip())
```
===== 16: failed =====
```
         command.append(f"-q {quote}")
     if path:
         command.append(f"-f {path}")
-    if action:
+    if action in ["set", "unset"]:
         command.append(action)
         if key:
             command.append(key)
```
```
def get_cli_string(
    path: Optional[str] = None,
    action: Optional[str] = None,
    key: Optional[str] = None,
    value: Optional[str] = None,
    quote: Optional[str] = None,
):
    """Returns a string suitable for running as a shell script.

    Useful for converting a arguments passed to a fabric task
    to be passed to a `local` or `run` command.
    """
    command = ["dotenv"]
    if quote:
        command.append(f"-q {quote}")
    if path:
        command.append(f"-f {path}")
    if action in ["set", "unset"]:
        command.append(action)
        if key:
            command.append(key)
            if value:
                if " " in value:
                    command.append(f'"{value}"')
                else:
                    command.append(value)

    return " ".join(command).strip()
```
