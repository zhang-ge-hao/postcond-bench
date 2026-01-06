https://github.com/pallets/flask/blob/330123258e8c3dc391cbe55ab1ed94891ca83af3/./src/flask/config.py#L126-L185
```
@icontract.snapshot(lambda self: __import__('copy').deepcopy(self), name="old_self")
@icontract.snapshot(lambda prefix: [k[len(f"{prefix}_"):] for k in os.environ.keys() if k.startswith(f"{prefix}_")], name="mapped_keys")
@icontract.snapshot(lambda prefix: set(k.split("__")[0] for k in [kk[len(f"{prefix}_"):] for kk in os.environ.keys() if kk.startswith(f"{prefix}_")]), name="affected_top_keys")
@icontract.snapshot(lambda prefix: set(k for k in [kk[len(f"{prefix}_"):] for kk in os.environ.keys() if kk.startswith(f"{prefix}_")] if "__" not in k), name="simple_keys")
@icontract.snapshot(lambda prefix: [k.split("__") for k in [kk[len(f"{prefix}_"):] for kk in os.environ.keys() if kk.startswith(f"{prefix}_")] if "__" in k], name="nested_parts")
@icontract.ensure(lambda result: result is True)
@icontract.ensure(lambda self, OLD: all(k in self for k in OLD.old_self))
@icontract.ensure(lambda self, OLD: all((k in self and self[k] == OLD.old_self[k]) for k in OLD.old_self if k not in OLD.affected_top_keys))
@icontract.ensure(lambda self, OLD: set(self.keys()) - set(OLD.old_self.keys()) <= OLD.affected_top_keys)
@icontract.ensure(lambda self, OLD: OLD.simple_keys <= set(self.keys()))
@icontract.ensure(lambda self, OLD: all(((cur := self.get(parts[0], None)) is not None) and all(isinstance(cur, dict) and (cur := cur.get(p, None)) is not None for p in parts[1:-1]) and isinstance(cur, dict) and (parts[-1] in cur) for parts in OLD.nested_parts))
```
```
No direct verification.

No validation on load() results.
```
passed
```
@icontract.snapshot(lambda self, prefix, loads: dict(os.environ), name="old_env")
@icontract.ensure(lambda result: result is True)
@icontract.ensure(lambda OLD, self, prefix, loads: all((("__" not in s and s in self and self[s] == (True if v.lower() == "true" else False if v.lower() == "false" else int(v) if v.isdigit() else float(v) if (v.count(".") == 1 and all(p.isdigit() for p in v.split("."))) else (__import__("json").loads(v) if (v.startswith("[") or v.startswith("{")) else v))) or ("__" in s and (lambda cur_parts: ((cur := __import__("functools").reduce(lambda c, p: (c.get(p) if isinstance(c, dict) else None), cur_parts[:-1], self)) is not None and isinstance(cur, dict) and cur.get(cur_parts[-1]) == (True if v.lower() == "true" else False if v.lower() == "false" else int(v) if v.isdigit() else float(v) if (v.count(".") == 1 and all(p.isdigit() for p in v.split("."))) else (__import__("json").loads(v) if (v.startswith("[") or v.startswith("{")) else v))))(s.split("__")))) for k, v in OLD.old_env.items() if k.startswith(f"{prefix}_") and ((s := k.removeprefix(f"{prefix}_")) is not None)))
```
===== 15 =====
failed
```
             key = key.removeprefix(prefix)
 
             try:
-                value = loads(value)
+                value = value.upper()  # Converts the value to uppercase, losing original data
             except Exception:
                 # Keep the value as a string if loading failed.
                 pass
```
```
    def from_prefixed_env(
        self, prefix: str = "FLASK", *, loads: t.Callable[[str], t.Any] = json.loads
    ) -> bool:
        """Load any environment variables that start with ``FLASK_``,
        dropping the prefix from the env key for the config key. Values
        are passed through a loading function to attempt to convert them
        to more specific types than strings.

        Keys are loaded in :func:`sorted` order.

        The default loading function attempts to parse values as any
        valid JSON type, including dicts and lists.

        Specific items in nested dicts can be set by separating the
        keys with double underscores (``__``). If an intermediate key
        doesn't exist, it will be initialized to an empty dict.

        :param prefix: Load env vars that start with this prefix,
            separated with an underscore (``_``).
        :param loads: Pass each string value to this function and use
            the returned value as the config value. If any error is
            raised it is ignored and the value remains a string. The
            default is :func:`json.loads`.

        .. versionadded:: 2.1
        """
        prefix = f"{prefix}_"

        for key in sorted(os.environ):
            if not key.startswith(prefix):
                continue

            value = os.environ[key]
            key = key.removeprefix(prefix)

            try:
                value = value.upper()  # Converts the value to uppercase, losing original data
            except Exception:
                # Keep the value as a string if loading failed.
                pass

            if "__" not in key:
                # A non-nested key, set directly.
                self[key] = value
                continue

            # Traverse nested dictionaries with keys separated by "__".
            current = self
            *parts, tail = key.split("__")

            for part in parts:
                # If an intermediate dict does not exist, create it.
                if part not in current:
                    current[part] = {}

                current = current[part]

            current[tail] = value

        return True
```
