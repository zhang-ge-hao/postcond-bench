https://github.com/miyuchina/mistletoe/blob/0860a8662d386b0b9bee2512e8a078715703f980/./mistletoe/block_token.py#L590-L618
```
@icontract.ensure(lambda result: (result is None) or (isinstance(result, tuple) and len(result) == 4 and isinstance(result[0], int) and isinstance(result[1], int) and isinstance(result[2], str) and isinstance(result[3], str)))
@icontract.ensure(lambda result, cls, line: (result is None) == (cls.pattern.match(line) is None))
@icontract.ensure(lambda result, cls, line: (result is None) or (re.fullmatch(r'\d{0,9}[.)]|[+\-*]', result[2]) is not None))
@icontract.ensure(lambda result: (result is None) or (0 <= result[0] <= 3))
@icontract.ensure(lambda result: (result is None) or (0 <= result[1] - result[0] - len(result[2]) <= 4))
@icontract.ensure(lambda result, cls, line: (result is None) or (lambda m: (m is not None and result[0] == len(m.group(1))))(cls.pattern.match(line)))
@icontract.ensure(lambda result, cls, line: (result is None) or (lambda m: (m is not None and result[2] == m.group(2)))(cls.pattern.match(line)))
@icontract.ensure(lambda result, cls, line: (result is None) or (lambda m: (m is not None and (lambda initial_prepend, n_spaces: result[1] == (initial_prepend - (n_spaces - 1) if n_spaces > 4 else initial_prepend))(len(m.group(0).expandtabs(4)), len(m.group(0).expandtabs(4)) - m.end(2))))(cls.pattern.match(line)))
@icontract.ensure(lambda result, cls, line: (result is None) or (lambda m: (m is not None and (lambda initial_prepend, n_spaces: result[3] == ((' ' * (n_spaces - 1) + line[m.end(0):]) if n_spaces > 4 else line[m.end(0):])))(len(m.group(0).expandtabs(4)), len(m.group(0).expandtabs(4)) - m.end(2))))(cls.pattern.match(line)))
```
```
Syntax error.


E   SyntaxError: unmatched ')'
```
syntax_error
```
@icontract.snapshot(lambda cls, line: cls.pattern.match(line), name="m")
@icontract.ensure(
    lambda OLD, result, cls, line:
        (
            OLD.m is None
            and result is None
        )
        or
        (
            OLD.m is not None
            and isinstance(result, tuple)
            and len(result) == 4
            and result[0] == len(OLD.m.group(1))
            and result[2] == OLD.m.group(2)
            and (
                (
                    (len(OLD.m.group(0).expandtabs(4)) - OLD.m.end(2)) > 4
                    and result[1] == (
                        len(OLD.m.group(0).expandtabs(4))
                        - (
                            (len(OLD.m.group(0).expandtabs(4)) - OLD.m.end(2))
                            - 1
                        )
                    )
                    and result[3] == (
                        ' ' * (
                            (len(OLD.m.group(0).expandtabs(4)) - OLD.m.end(2))
                            - 1
                        )
                        + line[OLD.m.end(0):]
                    )
                )
                or (
                    (len(OLD.m.group(0).expandtabs(4)) - OLD.m.end(2)) <= 4
                    and result[1] == len(OLD.m.group(0).expandtabs(4))
                    and result[3] == line[OLD.m.end(0):]
                )
            )
        )
)

```
