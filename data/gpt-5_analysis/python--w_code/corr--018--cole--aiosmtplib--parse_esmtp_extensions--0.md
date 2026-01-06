https://github.com/cole/aiosmtplib/blob/70a849a81c455ba93ba5d704585825879647d5c3/./src/aiosmtplib/esmtp.py#L15-L72
```
@icontract.ensure(lambda result: isinstance(result, tuple) and len(result) == 2)
@icontract.ensure(lambda message, result: result[0] == {(m.group('ext').lower()): m.string[m.end('ext'):].strip() for line in message.split("\n")[1:] if (m := EXTENSIONS_REGEX.match(line))})
@icontract.ensure(lambda message, result: result[1] == [token for line in message.split("\n")[1:] for token in (([m2.group('auth').lower().strip()] if (m2 := OLDSTYLE_AUTH_REGEX.match(line)) else []) + ([p.strip().lower() for p in ((m1.string[m1.end('ext'):].strip()).split())] if ((m1 := EXTENSIONS_REGEX.match(line)) and (m1.group('ext').lower() == 'auth')) else []))])
@icontract.ensure(lambda result: all(t.strip().lower() in set(result[1]) for t in result[0].get('auth', '').split()))
```
```
Syntax Error.

E   SyntaxError: assignment expression cannot be used in a comprehension iterable expression
```
syntax_error
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
