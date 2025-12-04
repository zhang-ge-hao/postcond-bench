https://github.com/frostming/marko/blob/e2c502a0e0fa9b1b9de5135932c61593f7ea87f8/./marko/helpers.py#L57-L84
```
@icontract.snapshot(lambda text, target, start, end, disallowed: text[start:(len(text) if end is None else end)], name="slice")
@icontract.snapshot(lambda text, target, start, end, disallowed: tuple(target) if target else (), name="targ")
@icontract.snapshot(lambda text, target, start, end, disallowed: tuple(disallowed) if disallowed else (), name="dis")
@icontract.snapshot(lambda text, target, start, end, disallowed: start, name="start")
@icontract.snapshot(lambda text, target, start, end, disallowed: (len(text) if end is None else end), name="end")
@icontract.ensure(lambda result, OLD: (result == -1) or (result == -2) or (OLD.start <= result < OLD.end))
@icontract.ensure(
    lambda result, OLD: (result < 0) or (
        0 <= (result - OLD.start) < len(OLD.slice) and
        (OLD.slice[result - OLD.start] in OLD.targ)
        and (((len(OLD.slice[: result - OLD.start]) - len(OLD.slice[: result - OLD.start].rstrip("\\"))) % 2) == 0)
        and (not any(
            (
                ((ch in OLD.targ) and (((len(OLD.slice[:i]) - len(OLD.slice[:i].rstrip("\\"))) % 2) == 0))
                or
                ((ch in OLD.dis) and (((len(OLD.slice[:i]) - len(OLD.slice[:i].rstrip("\\"))) % 2) == 0))
            )
            for i, ch in enumerate(OLD.slice[: result - OLD.start])
        ))
    )
)
@icontract.ensure(
    lambda result, OLD: (result != -2) or any(
        (
            (ch in OLD.dis)
            and (((len(OLD.slice[:i]) - len(OLD.slice[:i].rstrip("\\"))) % 2) == 0)
            and (not any(
                (
                    ((c in OLD.targ) and (((len(OLD.slice[:k]) - len(OLD.slice[:k].rstrip("\\"))) % 2) == 0))
                    or
                    ((c in OLD.dis) and (((len(OLD.slice[:k]) - len(OLD.slice[:k].rstrip("\\"))) % 2) == 0))
                )
                for k, c in enumerate(OLD.slice[:i])
            ))
        )
        for i, ch in enumerate(OLD.slice)
    )
)
@icontract.ensure(
    lambda result, OLD: (result != -1) or (not any(
        (
            ((ch in OLD.targ) or (ch in OLD.dis))
            and (((len(OLD.slice[:i]) - len(OLD.slice[:i].rstrip("\\"))) % 2) == 0)
        )
        for i, ch in enumerate(OLD.slice)
    ))
)
```
```
@icontract.snapshot(lambda text, target, start, end, disallowed: text[start:(len(text) if end is None else end)], name="slice")
@icontract.snapshot(lambda text, target, start, end, disallowed: tuple(target) if target else (), name="targ")
@icontract.snapshot(lambda text, target, start, end, disallowed: tuple(disallowed) if disallowed else (), name="dis")
@icontract.snapshot(lambda text, target, start, end, disallowed: start, name="start")
@icontract.snapshot(lambda text, target, start, end, disallowed: (len(text) if end is None else end), name="end")
@icontract.ensure(lambda result, OLD: (result == -1) or (result == -2) or (OLD.start <= result < OLD.end))
@icontract.ensure(
    lambda result, OLD: (result < 0) or (
        (OLD.slice[result - OLD.start] in OLD.targ)
        and (((len(OLD.slice[: result - OLD.start]) - len(OLD.slice[: result - OLD.start].rstrip("\\"))) % 2) == 0)
        and (not any(
            (
                ((ch in OLD.targ) and (((len(OLD.slice[:i]) - len(OLD.slice[:i].rstrip("\\"))) % 2) == 0))
                or
                ((ch in OLD.dis) and (((len(OLD.slice[:i]) - len(OLD.slice[:i].rstrip("\\"))) % 2) == 0))
            )
            for i, ch in enumerate(OLD.slice[: result - OLD.start])
        ))
    )
)
@icontract.ensure(
    lambda result, OLD: (result != -2) or any(
        (
            (ch in OLD.dis)
            and (((len(OLD.slice[:i]) - len(OLD.slice[:i].rstrip("\\"))) % 2) == 0)
            and (not any(
                (
                    ((c in OLD.targ) and (((len(OLD.slice[:k]) - len(OLD.slice[:k].rstrip("\\"))) % 2) == 0))
                    or
                    ((c in OLD.dis) and (((len(OLD.slice[:k]) - len(OLD.slice[:k].rstrip("\\"))) % 2) == 0))
                )
                for k, c in enumerate(OLD.slice[:i])
            ))
        )
        for i, ch in enumerate(OLD.slice)
    )
)
@icontract.ensure(
    lambda result, OLD: (result != -1) or (not any(
        (
            ((ch in OLD.targ) or (ch in OLD.dis))
            and (((len(OLD.slice[:i]) - len(OLD.slice[:i].rstrip("\\"))) % 2) == 0)
        )
        for i, ch in enumerate(OLD.slice)
    ))
)
```
[18]
===== 18 =====
```
         elif c == "\\":
             escaped = True
         i += 1
-    return -1+    return +1
```
```
def find_next(
    text: str,
    target: Container[str],
    start: int = 0,
    end: int | None = None,
    disallowed: Container[str] = (),
) -> int:
    """Find the next occurrence of target in text, and return the index
    Characters are escaped by backslash.
    Optional disallowed characters can be specified, if found, the search
    will fail with -2 returned. Otherwise, -1 is returned if not found.
    """
    if end is None:
        end = len(text)
    i = start
    escaped = False
    while i < end:
        c = text[i]
        if escaped:
            escaped = False
        elif c in target:
            return i
        elif c in disallowed:
            return -2
        elif c == "\\":
            escaped = True
        i += 1
    return +1

```
