https://github.com/mangiucugna/json_repair/blob/7ca4d6de56ab3824f617e913ee5003171a044578/./src/json_repair/parse_comment.py#L10-L71
```
@icontract.snapshot(lambda self: self.index, name="idx0")
@icontract.snapshot(lambda self: self.context.empty, name="empty0")
@icontract.snapshot(lambda self: self.get_char_at(), name="c0")
@icontract.snapshot(lambda self: self.get_char_at(1), name="c1")
@icontract.ensure(lambda OLD, result: OLD.empty0 or result == "")
@icontract.ensure(lambda OLD, self: OLD.empty0 or self.index >= OLD.idx0)
@icontract.ensure(lambda OLD, self: OLD.empty0 or (OLD.c0 in ["#", "/"] or self.index == OLD.idx0))
@icontract.ensure(lambda OLD, self: (self.index == OLD.idx0 + 1) if (not OLD.empty0 and OLD.c0 == "/" and (OLD.c1 not in ["*", "/"])) else True)
@icontract.ensure(lambda OLD, self: (self.index > OLD.idx0) if (not OLD.empty0 and OLD.c0 == "#") else True)
@icontract.ensure(lambda OLD, self: (self.index > OLD.idx0) if (not OLD.empty0 and OLD.c0 == "/" and (OLD.c1 in ["*", "/"])) else True)
@icontract.ensure(lambda OLD, self: OLD.empty0 or (self.context.empty == False))
```
```
No direct verification.
```
passed
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
===== 32 =====
failed
```
             comment = "/*"
             self.index += 2  # Skip '/*'
             while True:
-                char = self.get_char_at()
+                char = None
                 if not char:
                     self.log("Reached end-of-string while parsing block comment; unclosed block comment.")
                     break
@@ -59,4 +59,4 @@     if self.context.empty:
         return self.parse_json()
     else:
-        return ""+        return ""
```
```
def parse_comment(self: "JSONParser") -> JSONReturnType:
    """
    Parse code-like comments:

    - "# comment": A line comment that continues until a newline.
    - "// comment": A line comment that continues until a newline.
    - "/* comment */": A block comment that continues until the closing delimiter "*/".

    The comment is skipped over and an empty string is returned so that comments do not interfere
    with the actual JSON elements.
    """
    char = self.get_char_at()
    termination_characters = ["\n", "\r"]
    if ContextValues.ARRAY in self.context.context:
        termination_characters.append("]")
    if ContextValues.OBJECT_VALUE in self.context.context:
        termination_characters.append("}")
    if ContextValues.OBJECT_KEY in self.context.context:
        termination_characters.append(":")
    # Line comment starting with #
    if char == "#":
        comment = ""
        while char and char not in termination_characters:
            comment += char
            self.index += 1
            char = self.get_char_at()
        self.log(f"Found line comment: {comment}, ignoring")
    # Comments starting with '/'
    elif char == "/":
        next_char = self.get_char_at(1)
        # Handle line comment starting with //
        if next_char == "/":
            comment = "//"
            self.index += 2  # Skip both slashes.
            char = self.get_char_at()
            while char and char not in termination_characters:
                comment += char
                self.index += 1
                char = self.get_char_at()
            self.log(f"Found line comment: {comment}, ignoring")
        # Handle block comment starting with /*
        elif next_char == "*":
            comment = "/*"
            self.index += 2  # Skip '/*'
            while True:
                char = None
                if not char:
                    self.log("Reached end-of-string while parsing block comment; unclosed block comment.")
                    break
                comment += char
                self.index += 1
                if comment.endswith("*/"):
                    break
            self.log(f"Found block comment: {comment}, ignoring")
        else:
            # Skip standalone '/' characters that are not part of a comment
            # to avoid getting stuck in an infinite loop
            self.index += 1
    if self.context.empty:
        return self.parse_json()
    else:
        return ""

```
