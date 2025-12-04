https://github.com/adamchainz/django-upgrade/blob/05589e6da630cc5b9b589e183fa7c81f0b1fbed7/./src/django_upgrade/fixers/mail_api_kwargs.py#L149-L174
```
@icontract.snapshot(lambda tokens: tokens[:], name="old_tokens")
@icontract.snapshot(
    lambda tokens, i: parse_call_args(
        tokens, find(tokens, i, name=OP, src="(")
    )[0],
    name="old_func_args",
)
@icontract.snapshot(lambda api_config: api_config.new_kwargs[:], name="new_kwargs")
@icontract.snapshot(lambda num_posargs: num_posargs, name="num_posargs")
@icontract.snapshot(
    lambda convertible_posargs: convertible_posargs,
    name="convertible_posargs",
)
@icontract.snapshot(lambda tokens: len(tokens), name="old_len")
@icontract.ensure(
    lambda OLD, tokens, api_config, num_posargs, convertible_posargs:
        len(tokens) == OLD.old_len + OLD.convertible_posargs
        and
        all(
            any(getattr(t, "src", None) == f"{k}=" for t in tokens)
            for k in OLD.new_kwargs[
                OLD.num_posargs - OLD.convertible_posargs - api_config.new_posargs : OLD.num_posargs - api_config.new_posargs
            ]
        )
        and
        all(
            not any(getattr(t, "src", None) == f"{k}=" for t in tokens)
            for k in (
                OLD.new_kwargs[: OLD.num_posargs - OLD.convertible_posargs - api_config.new_posargs]
                + OLD.new_kwargs[OLD.num_posargs - api_config.new_posargs :]
            )
        )
        and
        (
        all(
            sum(
                1
                for t in tokens
                if getattr(t, "src", None)
                == f"{OLD.new_kwargs[argindex - api_config.new_posargs]}="
            )
            == 1
            for argindex in range(
                OLD.num_posargs - OLD.convertible_posargs,
                OLD.num_posargs,
            )
        )
        and
        all(
            not any(
                getattr(t, "src", None) == f"{kw}="
                for t in tokens
            )
            for kw in (
                set(OLD.new_kwargs)
                - {
                    OLD.new_kwargs[argindex - api_config.new_posargs]
                    for argindex in range(
                        OLD.num_posargs - OLD.convertible_posargs,
                        OLD.num_posargs,
                    )
                }
            )
        )
    )
    and
    all(
        (
            (
                lambda kw_name: (
                    (lambda kw_pos: (
                        (lambda start, end: (
                            (lambda arg_slice: (
                                (lambda first_sig: (
                                    (lambda leading_ws: (
                                        kw_pos
                                        <= tokens.index(first_sig)
                                        and
                                        all(tokens.index(ws_tok) < kw_pos for ws_tok in leading_ws)
                                    ))(
                                        [
                                            tok
                                            for offset, tok in enumerate(arg_slice)
                                            if tok.name in ("UNIMPORTANT_WS", "NL")
                                            and all(
                                                prev_tok.name in ("UNIMPORTANT_WS", "NL")
                                                for prev_tok in arg_slice[:offset]
                                            )
                                        ]
                                    )
                                ))(
                                    [
                                        tok
                                        for tok in arg_slice
                                        if tok.name not in ("UNIMPORTANT_WS", "NL")
                                    ][0]
                                )
                            ))(
                                OLD.old_tokens[start:end]
                            )
                        ))(*OLD.old_func_args[argindex])
                    ))(
                        [
                            idx
                            for idx, t in enumerate(tokens)
                            if getattr(t, "src", None) == f"{kw_name}="
                        ][0]
                    )
                )
            )(
                OLD.new_kwargs[argindex - api_config.new_posargs]
            )
        )
        for argindex in range(
            OLD.num_posargs - OLD.convertible_posargs,
            OLD.num_posargs,
        )
    )
)
```
```
@icontract.snapshot(lambda tokens: tokens[:], name="old_tokens")
@icontract.snapshot(lambda tokens, i: parse_call_args(tokens, find(tokens, i, name=OP, src="("))[0], name="old_func_args")
@icontract.snapshot(lambda api_config: api_config.new_kwargs[:], name="new_kwargs")
@icontract.snapshot(lambda num_posargs: num_posargs, name="num_posargs")
@icontract.snapshot(lambda convertible_posargs: convertible_posargs, name="convertible_posargs")
@icontract.ensure(
    lambda OLD, tokens, api_config, num_posargs, convertible_posargs:
        all(
            any(getattr(t, "src", None) == f"{k}=" for t in tokens)
            for k in OLD.new_kwargs[
                OLD.num_posargs - OLD.convertible_posargs - api_config.new_posargs : OLD.num_posargs - api_config.new_posargs
            ]
        )
)
@icontract.ensure(
    lambda OLD, tokens, api_config, num_posargs, convertible_posargs:
        all(
            not any(getattr(t, "src", None) == f"{k}=" for t in tokens)
            for k in (
                OLD.new_kwargs[: OLD.num_posargs - OLD.convertible_posargs - api_config.new_posargs]
                + OLD.new_kwargs[OLD.num_posargs - api_config.new_posargs :]
            )
        )
)
```
[15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28]
===== 15 =====
```
         arg_start, arg_end = func_args[argindex]
 
         actual_arg_start = arg_start
-        while actual_arg_start < arg_end and tokens[actual_arg_start].name in (
+        while actual_arg_start < arg_end and tokens[actual_arg_start].name not in (
             "UNIMPORTANT_WS",
             "NL",
         ):
```
```
def migrate_api_args(
    tokens: list[Token],
    i: int,
    *,
    api_config: APIConfig,
    num_posargs: int,
    convertible_posargs: int,
) -> None:
    """
    Convert excess positional arguments to keyword arguments for email functions.
    Only converts arguments beyond the allowed positional count.
    """
    open_idx = find(tokens, i, name=OP, src="(")
    func_args, _close_idx = parse_call_args(tokens, open_idx)

    for argindex in range(num_posargs - 1, num_posargs - convertible_posargs - 1, -1):
        kwarg = api_config.new_kwargs[argindex - api_config.new_posargs]
        arg_start, arg_end = func_args[argindex]

        actual_arg_start = arg_start
        while actual_arg_start < arg_end and tokens[actual_arg_start].name not in (
            "UNIMPORTANT_WS",
            "NL",
        ):
            actual_arg_start += 1
        tokens.insert(actual_arg_start, Token(name=CODE, src=f"{kwarg}="))
```
===== 16 =====
```
         arg_start, arg_end = func_args[argindex]
 
         actual_arg_start = arg_start
-        while actual_arg_start < arg_end and tokens[actual_arg_start].name in (
+        while actual_arg_start < arg_end and tokens[actual_arg_start].name not in (
             "UNIMPORTANT_WS",
             "NL",
         ):
             actual_arg_start += 1
-        tokens.insert(actual_arg_start, Token(name=CODE, src=f"{kwarg}="))+        tokens.insert(actual_arg_start, Token(name=CODE, src=f"{kwarg}="))
```
```
def migrate_api_args(
    tokens: list[Token],
    i: int,
    *,
    api_config: APIConfig,
    num_posargs: int,
    convertible_posargs: int,
) -> None:
    """
    Convert excess positional arguments to keyword arguments for email functions.
    Only converts arguments beyond the allowed positional count.
    """
    open_idx = find(tokens, i, name=OP, src="(")
    func_args, _close_idx = parse_call_args(tokens, open_idx)

    for argindex in range(num_posargs - 1, num_posargs - convertible_posargs - 1, -1):
        kwarg = api_config.new_kwargs[argindex - api_config.new_posargs]
        arg_start, arg_end = func_args[argindex]

        actual_arg_start = arg_start
        while actual_arg_start < arg_end and tokens[actual_arg_start].name not in (
            "UNIMPORTANT_WS",
            "NL",
        ):
            actual_arg_start += 1
        tokens.insert(actual_arg_start, Token(name=CODE, src=f"{kwarg}="))

```
===== 17 =====
```
         arg_start, arg_end = func_args[argindex]
 
         actual_arg_start = arg_start
-        while actual_arg_start < arg_end and tokens[actual_arg_start].name in (
+        while actual_arg_start < arg_end or tokens[actual_arg_start].name in (
             "UNIMPORTANT_WS",
             "NL",
         ):
             actual_arg_start += 1
-        tokens.insert(actual_arg_start, Token(name=CODE, src=f"{kwarg}="))+        tokens.insert(actual_arg_start, Token(name=CODE, src=f"{kwarg}="))
```
```
def migrate_api_args(
    tokens: list[Token],
    i: int,
    *,
    api_config: APIConfig,
    num_posargs: int,
    convertible_posargs: int,
) -> None:
    """
    Convert excess positional arguments to keyword arguments for email functions.
    Only converts arguments beyond the allowed positional count.
    """
    open_idx = find(tokens, i, name=OP, src="(")
    func_args, _close_idx = parse_call_args(tokens, open_idx)

    for argindex in range(num_posargs - 1, num_posargs - convertible_posargs - 1, -1):
        kwarg = api_config.new_kwargs[argindex - api_config.new_posargs]
        arg_start, arg_end = func_args[argindex]

        actual_arg_start = arg_start
        while actual_arg_start < arg_end or tokens[actual_arg_start].name in (
            "UNIMPORTANT_WS",
            "NL",
        ):
            actual_arg_start += 1
        tokens.insert(actual_arg_start, Token(name=CODE, src=f"{kwarg}="))

```
===== 18 =====
```
 
         actual_arg_start = arg_start
         while actual_arg_start < arg_end and tokens[actual_arg_start].name in (
-            "UNIMPORTANT_WS",
+            "COMMENT",
             "NL",
         ):
             actual_arg_start += 1
```
```
def migrate_api_args(
    tokens: list[Token],
    i: int,
    *,
    api_config: APIConfig,
    num_posargs: int,
    convertible_posargs: int,
) -> None:
    """
    Convert excess positional arguments to keyword arguments for email functions.
    Only converts arguments beyond the allowed positional count.
    """
    open_idx = find(tokens, i, name=OP, src="(")
    func_args, _close_idx = parse_call_args(tokens, open_idx)

    for argindex in range(num_posargs - 1, num_posargs - convertible_posargs - 1, -1):
        kwarg = api_config.new_kwargs[argindex - api_config.new_posargs]
        arg_start, arg_end = func_args[argindex]

        actual_arg_start = arg_start
        while actual_arg_start < arg_end and tokens[actual_arg_start].name in (
            "COMMENT",
            "NL",
        ):
            actual_arg_start += 1
        tokens.insert(actual_arg_start, Token(name=CODE, src=f"{kwarg}="))
```
===== 19 =====
```
 
         actual_arg_start = arg_start
         while actual_arg_start < arg_end and tokens[actual_arg_start].name in (
-            "UNIMPORTANT_WS",
+            "DEDENT",
             "NL",
         ):
             actual_arg_start += 1
```
```
def migrate_api_args(
    tokens: list[Token],
    i: int,
    *,
    api_config: APIConfig,
    num_posargs: int,
    convertible_posargs: int,
) -> None:
    """
    Convert excess positional arguments to keyword arguments for email functions.
    Only converts arguments beyond the allowed positional count.
    """
    open_idx = find(tokens, i, name=OP, src="(")
    func_args, _close_idx = parse_call_args(tokens, open_idx)

    for argindex in range(num_posargs - 1, num_posargs - convertible_posargs - 1, -1):
        kwarg = api_config.new_kwargs[argindex - api_config.new_posargs]
        arg_start, arg_end = func_args[argindex]

        actual_arg_start = arg_start
        while actual_arg_start < arg_end and tokens[actual_arg_start].name in (
            "DEDENT",
            "NL",
        ):
            actual_arg_start += 1
        tokens.insert(actual_arg_start, Token(name=CODE, src=f"{kwarg}="))
```
===== 20 =====
```
 
         actual_arg_start = arg_start
         while actual_arg_start < arg_end and tokens[actual_arg_start].name in (
-            "UNIMPORTANT_WS",
+            "INDENT",
             "NL",
         ):
             actual_arg_start += 1
```
```
def migrate_api_args(
    tokens: list[Token],
    i: int,
    *,
    api_config: APIConfig,
    num_posargs: int,
    convertible_posargs: int,
) -> None:
    """
    Convert excess positional arguments to keyword arguments for email functions.
    Only converts arguments beyond the allowed positional count.
    """
    open_idx = find(tokens, i, name=OP, src="(")
    func_args, _close_idx = parse_call_args(tokens, open_idx)

    for argindex in range(num_posargs - 1, num_posargs - convertible_posargs - 1, -1):
        kwarg = api_config.new_kwargs[argindex - api_config.new_posargs]
        arg_start, arg_end = func_args[argindex]

        actual_arg_start = arg_start
        while actual_arg_start < arg_end and tokens[actual_arg_start].name in (
            "INDENT",
            "NL",
        ):
            actual_arg_start += 1
        tokens.insert(actual_arg_start, Token(name=CODE, src=f"{kwarg}="))
```
===== 21 =====
```
 
         actual_arg_start = arg_start
         while actual_arg_start < arg_end and tokens[actual_arg_start].name in (
-            "UNIMPORTANT_WS",
+            "NEWLINE",
             "NL",
         ):
             actual_arg_start += 1
```
```
def migrate_api_args(
    tokens: list[Token],
    i: int,
    *,
    api_config: APIConfig,
    num_posargs: int,
    convertible_posargs: int,
) -> None:
    """
    Convert excess positional arguments to keyword arguments for email functions.
    Only converts arguments beyond the allowed positional count.
    """
    open_idx = find(tokens, i, name=OP, src="(")
    func_args, _close_idx = parse_call_args(tokens, open_idx)

    for argindex in range(num_posargs - 1, num_posargs - convertible_posargs - 1, -1):
        kwarg = api_config.new_kwargs[argindex - api_config.new_posargs]
        arg_start, arg_end = func_args[argindex]

        actual_arg_start = arg_start
        while actual_arg_start < arg_end and tokens[actual_arg_start].name in (
            "NEWLINE",
            "NL",
        ):
            actual_arg_start += 1
        tokens.insert(actual_arg_start, Token(name=CODE, src=f"{kwarg}="))
```
===== 22 =====
```
 
         actual_arg_start = arg_start
         while actual_arg_start < arg_end and tokens[actual_arg_start].name in (
-            "UNIMPORTANT_WS",
+            "SPACE",
             "NL",
         ):
             actual_arg_start += 1
```
```
def migrate_api_args(
    tokens: list[Token],
    i: int,
    *,
    api_config: APIConfig,
    num_posargs: int,
    convertible_posargs: int,
) -> None:
    """
    Convert excess positional arguments to keyword arguments for email functions.
    Only converts arguments beyond the allowed positional count.
    """
    open_idx = find(tokens, i, name=OP, src="(")
    func_args, _close_idx = parse_call_args(tokens, open_idx)

    for argindex in range(num_posargs - 1, num_posargs - convertible_posargs - 1, -1):
        kwarg = api_config.new_kwargs[argindex - api_config.new_posargs]
        arg_start, arg_end = func_args[argindex]

        actual_arg_start = arg_start
        while actual_arg_start < arg_end and tokens[actual_arg_start].name in (
            "SPACE",
            "NL",
        ):
            actual_arg_start += 1
        tokens.insert(actual_arg_start, Token(name=CODE, src=f"{kwarg}="))
```
===== 23 =====
```
 
         actual_arg_start = arg_start
         while actual_arg_start < arg_end and tokens[actual_arg_start].name in (
-            "UNIMPORTANT_WS",
+            "XXUNIMPORTANT_WSXX",
             "NL",
         ):
             actual_arg_start += 1
-        tokens.insert(actual_arg_start, Token(name=CODE, src=f"{kwarg}="))+        tokens.insert(actual_arg_start, Token(name=CODE, src=f"{kwarg}="))
```
```
def migrate_api_args(
    tokens: list[Token],
    i: int,
    *,
    api_config: APIConfig,
    num_posargs: int,
    convertible_posargs: int,
) -> None:
    """
    Convert excess positional arguments to keyword arguments for email functions.
    Only converts arguments beyond the allowed positional count.
    """
    open_idx = find(tokens, i, name=OP, src="(")
    func_args, _close_idx = parse_call_args(tokens, open_idx)

    for argindex in range(num_posargs - 1, num_posargs - convertible_posargs - 1, -1):
        kwarg = api_config.new_kwargs[argindex - api_config.new_posargs]
        arg_start, arg_end = func_args[argindex]

        actual_arg_start = arg_start
        while actual_arg_start < arg_end and tokens[actual_arg_start].name in (
            "XXUNIMPORTANT_WSXX",
            "NL",
        ):
            actual_arg_start += 1
        tokens.insert(actual_arg_start, Token(name=CODE, src=f"{kwarg}="))

```
===== 24 =====
```
 
         actual_arg_start = arg_start
         while actual_arg_start < arg_end and tokens[actual_arg_start].name in (
-            "UNIMPORTANT_WS",
+            "unimportant_ws",
             "NL",
         ):
             actual_arg_start += 1
-        tokens.insert(actual_arg_start, Token(name=CODE, src=f"{kwarg}="))+        tokens.insert(actual_arg_start, Token(name=CODE, src=f"{kwarg}="))
```
```
def migrate_api_args(
    tokens: list[Token],
    i: int,
    *,
    api_config: APIConfig,
    num_posargs: int,
    convertible_posargs: int,
) -> None:
    """
    Convert excess positional arguments to keyword arguments for email functions.
    Only converts arguments beyond the allowed positional count.
    """
    open_idx = find(tokens, i, name=OP, src="(")
    func_args, _close_idx = parse_call_args(tokens, open_idx)

    for argindex in range(num_posargs - 1, num_posargs - convertible_posargs - 1, -1):
        kwarg = api_config.new_kwargs[argindex - api_config.new_posargs]
        arg_start, arg_end = func_args[argindex]

        actual_arg_start = arg_start
        while actual_arg_start < arg_end and tokens[actual_arg_start].name in (
            "unimportant_ws",
            "NL",
        ):
            actual_arg_start += 1
        tokens.insert(actual_arg_start, Token(name=CODE, src=f"{kwarg}="))

```
===== 25 =====
```
         actual_arg_start = arg_start
         while actual_arg_start < arg_end and tokens[actual_arg_start].name in (
             "UNIMPORTANT_WS",
-            "NL",
+            "XXNLXX",
         ):
             actual_arg_start += 1
-        tokens.insert(actual_arg_start, Token(name=CODE, src=f"{kwarg}="))+        tokens.insert(actual_arg_start, Token(name=CODE, src=f"{kwarg}="))
```
```
def migrate_api_args(
    tokens: list[Token],
    i: int,
    *,
    api_config: APIConfig,
    num_posargs: int,
    convertible_posargs: int,
) -> None:
    """
    Convert excess positional arguments to keyword arguments for email functions.
    Only converts arguments beyond the allowed positional count.
    """
    open_idx = find(tokens, i, name=OP, src="(")
    func_args, _close_idx = parse_call_args(tokens, open_idx)

    for argindex in range(num_posargs - 1, num_posargs - convertible_posargs - 1, -1):
        kwarg = api_config.new_kwargs[argindex - api_config.new_posargs]
        arg_start, arg_end = func_args[argindex]

        actual_arg_start = arg_start
        while actual_arg_start < arg_end and tokens[actual_arg_start].name in (
            "UNIMPORTANT_WS",
            "XXNLXX",
        ):
            actual_arg_start += 1
        tokens.insert(actual_arg_start, Token(name=CODE, src=f"{kwarg}="))

```
===== 26 =====
```
         actual_arg_start = arg_start
         while actual_arg_start < arg_end and tokens[actual_arg_start].name in (
             "UNIMPORTANT_WS",
-            "NL",
+            "nl",
         ):
             actual_arg_start += 1
-        tokens.insert(actual_arg_start, Token(name=CODE, src=f"{kwarg}="))+        tokens.insert(actual_arg_start, Token(name=CODE, src=f"{kwarg}="))
```
```
def migrate_api_args(
    tokens: list[Token],
    i: int,
    *,
    api_config: APIConfig,
    num_posargs: int,
    convertible_posargs: int,
) -> None:
    """
    Convert excess positional arguments to keyword arguments for email functions.
    Only converts arguments beyond the allowed positional count.
    """
    open_idx = find(tokens, i, name=OP, src="(")
    func_args, _close_idx = parse_call_args(tokens, open_idx)

    for argindex in range(num_posargs - 1, num_posargs - convertible_posargs - 1, -1):
        kwarg = api_config.new_kwargs[argindex - api_config.new_posargs]
        arg_start, arg_end = func_args[argindex]

        actual_arg_start = arg_start
        while actual_arg_start < arg_end and tokens[actual_arg_start].name in (
            "UNIMPORTANT_WS",
            "nl",
        ):
            actual_arg_start += 1
        tokens.insert(actual_arg_start, Token(name=CODE, src=f"{kwarg}="))

```
===== 27 =====
```
             "UNIMPORTANT_WS",
             "NL",
         ):
-            actual_arg_start += 1
-        tokens.insert(actual_arg_start, Token(name=CODE, src=f"{kwarg}="))+            actual_arg_start += 2
+        tokens.insert(actual_arg_start, Token(name=CODE, src=f"{kwarg}="))
```
```
def migrate_api_args(
    tokens: list[Token],
    i: int,
    *,
    api_config: APIConfig,
    num_posargs: int,
    convertible_posargs: int,
) -> None:
    """
    Convert excess positional arguments to keyword arguments for email functions.
    Only converts arguments beyond the allowed positional count.
    """
    open_idx = find(tokens, i, name=OP, src="(")
    func_args, _close_idx = parse_call_args(tokens, open_idx)

    for argindex in range(num_posargs - 1, num_posargs - convertible_posargs - 1, -1):
        kwarg = api_config.new_kwargs[argindex - api_config.new_posargs]
        arg_start, arg_end = func_args[argindex]

        actual_arg_start = arg_start
        while actual_arg_start < arg_end and tokens[actual_arg_start].name in (
            "UNIMPORTANT_WS",
            "NL",
        ):
            actual_arg_start += 2
        tokens.insert(actual_arg_start, Token(name=CODE, src=f"{kwarg}="))

```
===== 28 =====
```
             "UNIMPORTANT_WS",
             "NL",
         ):
-            actual_arg_start += 1
-        tokens.insert(actual_arg_start, Token(name=CODE, src=f"{kwarg}="))+            actual_arg_start -= 1
+        tokens.insert(actual_arg_start, Token(name=CODE, src=f"{kwarg}="))
```
```
def migrate_api_args(
    tokens: list[Token],
    i: int,
    *,
    api_config: APIConfig,
    num_posargs: int,
    convertible_posargs: int,
) -> None:
    """
    Convert excess positional arguments to keyword arguments for email functions.
    Only converts arguments beyond the allowed positional count.
    """
    open_idx = find(tokens, i, name=OP, src="(")
    func_args, _close_idx = parse_call_args(tokens, open_idx)

    for argindex in range(num_posargs - 1, num_posargs - convertible_posargs - 1, -1):
        kwarg = api_config.new_kwargs[argindex - api_config.new_posargs]
        arg_start, arg_end = func_args[argindex]

        actual_arg_start = arg_start
        while actual_arg_start < arg_end and tokens[actual_arg_start].name in (
            "UNIMPORTANT_WS",
            "NL",
        ):
            actual_arg_start -= 1
        tokens.insert(actual_arg_start, Token(name=CODE, src=f"{kwarg}="))

```
