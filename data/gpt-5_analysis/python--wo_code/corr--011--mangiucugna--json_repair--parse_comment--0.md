https://github.com/mangiucugna/json_repair/blob/7ca4d6de56ab3824f617e913ee5003171a044578/./src/json_repair/parse_comment.py#L10-L71
```
@icontract.ensure(lambda result: result == "")
@icontract.ensure(lambda result: isinstance(result, str))
```
```
Insufficient Context.

Need JSONParser and JSONReturnType context.
```
icontract_fail
```
@icontract.snapshot(lambda self: self.index, name="old_index")
@icontract.snapshot(lambda self: self.get_char_at(), name="old_char")
@icontract.snapshot(lambda self: self.get_char_at(1), name="old_next_char")
@icontract.snapshot(lambda self: tuple(self.context.context), name="old_context")
@icontract.snapshot(lambda self: self.json_str, name="old_json_str")
@icontract.snapshot(lambda self: self.context.empty, name="old_empty")
@icontract.ensure(
    lambda OLD, self, result: (
        not (
            OLD.old_char == "#"
            or (OLD.old_char == "/" and OLD.old_next_char == "/")
        )
    )
    or (
        (not OLD.old_empty)
        and (
            self.index
            == (
                lambda start, term_chars, s: min(
                    (i for i in range(start, len(s)) if s[i] in term_chars),
                    default=len(s),
                )
            )(
                OLD.old_index
                + (
                    2
                    if (
                        OLD.old_char == "/"
                        and OLD.old_next_char == "/"
                    )
                    else 0
                ),
                set(
                    ["\n", "\r"]
                    + (
                        ["]"]
                        if ContextValues.ARRAY in OLD.old_context
                        else []
                    )
                    + (
                        ["}"]
                        if ContextValues.OBJECT_VALUE in OLD.old_context
                        else []
                    )
                    + (
                        [":"]
                        if ContextValues.OBJECT_KEY in OLD.old_context
                        else []
                    )
                ),
                OLD.old_json_str,
            )
        )
    )
    or (
        OLD.old_empty
        and (
            (not self.get_char_at())
            or self.get_char_at()
            in (
                ["\n", "\r"]
                + (
                    ["]"]
                    if ContextValues.ARRAY in OLD.old_context
                    else []
                )
                + (
                    ["}"]
                    if ContextValues.OBJECT_VALUE in OLD.old_context
                    else []
                )
                + (
                    [":"]
                    if ContextValues.OBJECT_KEY in OLD.old_context
                    else []
                )
            )
        )
    )
)
@icontract.ensure(
    lambda OLD, self, result: (
        not (OLD.old_char == "/" and OLD.old_next_char == "*")
    )
    or (
        (not OLD.old_empty)
        and (
            (lambda s, start: (
                (not ("*/" in s[start:]) and self.index == len(s))
                or (
                    ("*/" in s[start:])
                    and (self.index == s.find("*/", start) + 2)
                )
            ))(OLD.old_json_str, OLD.old_index + 2)
        )
    )
    or (
        OLD.old_empty
        and (
            (not self.get_char_at())
            or ("*/" in OLD.old_json_str[OLD.old_index : self.index])
        )
    )
)
@icontract.ensure(
    lambda OLD, self, result: (
        not (OLD.old_char in ("#", "/"))
    )
    or (self.index > OLD.old_index)
)
@icontract.ensure(lambda OLD, self, result: result is not None)
@icontract.ensure(lambda OLD, self, result: result != "Invalid JSON")
@icontract.ensure(lambda OLD, self, result: result != "XXXX")
@icontract.ensure(lambda OLD, self, result: result is not self.context)
@icontract.ensure(
    lambda OLD, self, result:
        OLD.old_index <= self.index <= len(OLD.old_json_str)
)
@icontract.ensure(
    lambda OLD, self, result: (
        self.index <= OLD.old_index + 1
        or OLD.old_json_str.startswith("#", OLD.old_index)
        or OLD.old_json_str.startswith("//", OLD.old_index)
        or OLD.old_json_str.startswith("/*", OLD.old_index)
    )
)
@icontract.ensure(
    lambda OLD, self, result: (
        not (
            not OLD.old_empty
            and OLD.old_char == "/"
            and OLD.old_next_char not in ("/", "*")
        )
        or self.index == OLD.old_index + 1
    )
)
@icontract.ensure(
    lambda OLD, self, result: (
        not (OLD.old_char == "/" and OLD.old_next_char == "*")
        or self.index >= min(OLD.old_index + 2, len(OLD.old_json_str))
    )
)
@icontract.ensure(
    lambda OLD, self, result: (
        not (
            OLD.old_empty
            and OLD.old_char == "/"
            and OLD.old_next_char == "*"
            and (
                (lambda s, start: (
                    (s.find("*/", start) != -1)
                    and (
                        (lambda rest: (
                            rest.lstrip() != ""
                            and rest.lstrip()[0]
                            in '{["0123456789tfn-'
                        ))(s[s.find("*/", start) + 2 :])
                    )
                ))(OLD.old_json_str, OLD.old_index + 2)
            )
        )
        or (result is not None and 
        (__import__("json").dumps(result).strip() != "" if isinstance(result, dict) else result.strip() != ""))
    )
)

```
