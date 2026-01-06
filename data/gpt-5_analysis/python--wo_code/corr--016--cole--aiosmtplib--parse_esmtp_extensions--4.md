https://github.com/cole/aiosmtplib/blob/70a849a81c455ba93ba5d704585825879647d5c3/./src/aiosmtplib/esmtp.py#L15-L72
```
@icontract.ensure(lambda result: isinstance(result, tuple) and len(result) == 2)
@icontract.ensure(lambda result: isinstance(result[0], dict))
@icontract.ensure(lambda result: isinstance(result[1], list))
@icontract.ensure(lambda result: all(isinstance(k, str) for k in result[0].keys()))
@icontract.ensure(lambda result: all(isinstance(v, str) for v in result[0].values()))
@icontract.ensure(lambda result: all('\n' not in v and '\r' not in v for v in result[0].values()))
@icontract.ensure(lambda result: all(re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9\-]*', k) is not None for k in result[0].keys()))
@icontract.ensure(lambda result: all(isinstance(m, str) and len(m) > 0 for m in result[1]))
@icontract.ensure(lambda result: all(re.fullmatch(r'[A-Za-z0-9_][A-Za-z0-9_\-]*', m) is not None for m in result[1]))
@icontract.ensure(lambda result: len({m.lower() for m in result[1]}) == len(result[1]))
@icontract.ensure(lambda result, message: (re.search(r'(?i)\bauth(?:\b|=)', message) is not None) or len(result[1]) == 0)
@icontract.ensure(lambda result, message: all(re.search(r'(?i)\b' + re.escape(k) + r'\b', message) is not None for k in result[0].keys()) if result[0] else True)
@icontract.ensure(lambda result, message: all(re.search(r'(?i)\b' + re.escape(m) + r'\b', message) is not None for m in result[1]) if result[1] else True)
```
```
Hallucination.


```
icontract_fail
```
@icontract.snapshot(lambda message: message.split("\n"), name="lines")
@icontract.snapshot(lambda message: message.split("\n")[0], name="first")
@icontract.ensure(
    lambda result:
    isinstance(result, tuple)
    and isinstance(result[0], dict)
    and isinstance(result[1], list)
)
@icontract.ensure(
    lambda result:
    all(isinstance(k, str) and k == k.lower() for k in result[0].keys())
)
@icontract.ensure(
    lambda result:
    all(isinstance(v, str) for v in result[0].values())
)
@icontract.ensure(
    lambda result:
    all(isinstance(a, str) and a == a.strip() and a == a.lower() for a in result[1])
)
@icontract.ensure(
    lambda OLD, result:
    result[0]
    == {
        m.group("ext").lower(): line[m.end("ext") :].strip()
        for line in OLD.lines[1:]
        for m in [EXTENSIONS_REGEX.match(line)]
        if m is not None
    }
)
@icontract.ensure(
    lambda OLD, result:
    set(result[1])
    == {
        OLDSTYLE_AUTH_REGEX.match(line).group("auth").lower().strip()
        for line in OLD.lines[1:]
        if OLDSTYLE_AUTH_REGEX.match(line) is not None
    }.union(
        {
            param.strip().lower()
            for line in OLD.lines[1:]
            for m in [EXTENSIONS_REGEX.match(line)]
            if m is not None and m.group("ext").lower() == "auth"
            for param in line[m.end("ext") :].strip().split()
            if param.strip()
        }
    )
)
@icontract.ensure(
    lambda OLD, result:
    (OLD.first.strip() not in result[0].keys())
    and (OLD.first.strip() not in result[0].values())
    and (OLD.first.strip() not in result[1])
)

```
