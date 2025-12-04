https://github.com/adamchainz/django-upgrade/blob/05589e6da630cc5b9b589e183fa7c81f0b1fbed7/./src/django_upgrade/tokens.py#L126-L156
```
@icontract.ensure(
    lambda result, tokens, i: result[1] > i and 0 <= result[1] <= len(tokens)
)
@icontract.ensure(
    lambda result, tokens, i: tokens[result[1] - 1].src == BRACES[tokens[i].src]
)
@icontract.ensure(
    lambda result, tokens, i: all(
        tokens_to_src(tokens[s:e]).strip() != "" 
        and
        (i + 1) <= s < e <= (result[1] - 1) 
        and
        isinstance(s, int) and isinstance(e, int)
        and
        (
            sum(
                1
                for k in range(i, e)
                if tokens[k].src in BRACES
            )
            - sum(
                1
                for k in range(i, e)
                if tokens[k].src in set(BRACES.values())
            )
        )
        == 1
        for s, e in result[0]
    )
)
@icontract.ensure(
    lambda result, tokens, i: all(
        tokens[e].src == "," for s, e in result[0][:-1]
    )
    if len(result[0]) >= 2
    else True
)
@icontract.ensure(
    lambda result, tokens, i: (
        not result[0]
        or tokens[result[0][-1][1]].src in {",", BRACES[tokens[i].src]}
    )
)
@icontract.ensure(
    lambda result, tokens, i: all(
        result[0][k + 1][0] == result[0][k][1] + 1
        for k in range(len(result[0]) - 1)
    )
    if len(result[0]) >= 2
    else True
)
@icontract.ensure(
    lambda result, tokens, i: isinstance(result, tuple)
    and isinstance(result[0], list)
    and all(isinstance(t, tuple) and len(t) == 2 and isinstance(t[0], int) and isinstance(t[1], int) for t in result[0])
    and isinstance(result[1], int)
    and sorted(result[0])
    == sorted(
        [
            segment
            for segment in zip(
                [i + 1]
                + [
                    comma_index + 1
                    for comma_index in range(i + 1, result[1] - 1)
                    if tokens[comma_index].src == ","
                    and (
                        sum(
                            1
                            for k in range(i, comma_index)
                            if tokens[k].src in BRACES
                        )
                        - sum(
                            1
                            for k in range(i, comma_index)
                            if tokens[k].src in set(BRACES.values())
                        )
                    )
                    == 1
                ],
                [
                    comma_index
                    for comma_index in range(i + 1, result[1] - 1)
                    if tokens[comma_index].src == ","
                    and (
                        sum(
                            1
                            for k in range(i, comma_index)
                            if tokens[k].src in BRACES
                        )
                        - sum(
                            1
                            for k in range(i, comma_index)
                            if tokens[k].src in set(BRACES.values())
                        )
                    )
                    == 1
                ]
                + [result[1] - 1],
            )
            if tokens_to_src(tokens[segment[0] : segment[1]]).strip() != ""
        ]
    )
)
```
```
@icontract.ensure(lambda result, tokens, i: isinstance(result, tuple) and isinstance(result[0], list) and isinstance(result[1], int))
@icontract.ensure(lambda result, tokens, i: result[1] > i and 0 <= result[1] <= len(tokens))
@icontract.ensure(lambda result, tokens, i: tokens[result[1] - 1].src == BRACES[tokens[i].src])
@icontract.ensure(lambda result, tokens, i: all(isinstance(s, int) and isinstance(e, int) for s, e in result[0]))
@icontract.ensure(lambda result, tokens, i: all((i + 1) <= s < e <= (result[1] - 1) for s, e in result[0]))
@icontract.ensure(lambda result, tokens, i: all(tokens_to_src(tokens[s:e]).strip() != "" for s, e in result[0]))
@icontract.ensure(lambda result, tokens, i: all(tokens[e].src == "," for s, e in result[0][:-1]) if len(result[0]) >= 2 else True)
@icontract.ensure(lambda result, tokens, i: (not result[0]) or (tokens[result[0][-1][1]].src in {",", BRACES[tokens[i].src]}))
@icontract.ensure(lambda result, tokens, i: all(result[0][k + 1][0] == result[0][k][1] + 1 for k in range(len(result[0]) - 1)) if len(result[0]) >= 2 else True)
@icontract.ensure(lambda result, tokens, i: all( (sum(1 for k in range(i, e) if tokens[k].src in BRACES) - sum(1 for k in range(i, e) if tokens[k].src in set(BRACES.values()))) == 1 for s, e in result[0]))
@icontract.ensure(lambda result, tokens, i: (lambda top_commas, arg_commas: top_commas == arg_commas and top_commas in {max(0, len(result[0]) - 1), len(result[0])})(sum(1 for k in range(i + 1, result[1] - 1) if tokens[k].src == "," and (sum(1 for t in range(i, k) if tokens[t].src in BRACES) - sum(1 for t in range(i, k) if tokens[t].src in set(BRACES.values()))) == 1), sum(1 for s, e in result[0] if tokens[e].src == ",")) )
```
[1, 16, 25, 32]
===== 1 =====
```
     args = []
     stack = [i]
     i += 1
-    arg_start = i
+    arg_start = None
 
     while stack:
         token = tokens[i]
@@ -28,4 +28,4 @@ 
         i += 1
 
-    return args, i+    return args, i
```
```
def parse_call_args(
    tokens: list[Token],
    i: int,
) -> tuple[list[tuple[int, int]], int]:
    """
    Given the index of the opening bracket of a function call, step through
    and parse its arguments into a list of tuples of start, end indices.
    Return this list plus the position of the token after.
    """
    args = []
    stack = [i]
    i += 1
    arg_start = None

    while stack:
        token = tokens[i]

        if len(stack) == 1 and token.src == ",":
            args.append((arg_start, i))
            arg_start = i + 1
        elif token.src in BRACES:
            stack.append(i)
        elif token.src == BRACES[tokens[stack[-1]].src]:
            stack.pop()
            # if we're at the end, append that argument
            if not stack and tokens_to_src(tokens[arg_start:i]).strip():
                args.append((arg_start, i))

        i += 1

    return args, i

```
===== 16 =====
```
         token = tokens[i]
 
         if len(stack) == 1 and token.src == ",":
-            args.append((arg_start, i))
+            args.append(None)
             arg_start = i + 1
         elif token.src in BRACES:
             stack.append(i)
@@ -28,4 +28,4 @@ 
         i += 1
 
-    return args, i+    return args, i
```
```
def parse_call_args(
    tokens: list[Token],
    i: int,
) -> tuple[list[tuple[int, int]], int]:
    """
    Given the index of the opening bracket of a function call, step through
    and parse its arguments into a list of tuples of start, end indices.
    Return this list plus the position of the token after.
    """
    args = []
    stack = [i]
    i += 1
    arg_start = i

    while stack:
        token = tokens[i]

        if len(stack) == 1 and token.src == ",":
            args.append(None)
            arg_start = i + 1
        elif token.src in BRACES:
            stack.append(i)
        elif token.src == BRACES[tokens[stack[-1]].src]:
            stack.pop()
            # if we're at the end, append that argument
            if not stack and tokens_to_src(tokens[arg_start:i]).strip():
                args.append((arg_start, i))

        i += 1

    return args, i

```
===== 25 =====
```
         elif token.src == BRACES[tokens[stack[-1]].src]:
             stack.pop()
             # if we're at the end, append that argument
-            if not stack and tokens_to_src(tokens[arg_start:i]).strip():
+            if stack and not tokens_to_src(tokens[arg_start:i]).strip():  # incorrect condition leading to false positives
                 args.append((arg_start, i))
 
         i += 1
```
```
def parse_call_args(
    tokens: list[Token],
    i: int,
) -> tuple[list[tuple[int, int]], int]:
    """
    Given the index of the opening bracket of a function call, step through
    and parse its arguments into a list of tuples of start, end indices.
    Return this list plus the position of the token after.
    """
    args = []
    stack = [i]
    i += 1
    arg_start = i

    while stack:
        token = tokens[i]

        if len(stack) == 1 and token.src == ",":
            args.append((arg_start, i))
            arg_start = i + 1
        elif token.src in BRACES:
            stack.append(i)
        elif token.src == BRACES[tokens[stack[-1]].src]:
            stack.pop()
            # if we're at the end, append that argument
            if stack and not tokens_to_src(tokens[arg_start:i]).strip():  # incorrect condition leading to false positives
                args.append((arg_start, i))

        i += 1

    return args, i
```
===== 32 =====
```
             stack.pop()
             # if we're at the end, append that argument
             if not stack and tokens_to_src(tokens[arg_start:i]).strip():
-                args.append((arg_start, i))
+                args.append(None)
 
         i += 1
 
-    return args, i+    return args, i
```
```
def parse_call_args(
    tokens: list[Token],
    i: int,
) -> tuple[list[tuple[int, int]], int]:
    """
    Given the index of the opening bracket of a function call, step through
    and parse its arguments into a list of tuples of start, end indices.
    Return this list plus the position of the token after.
    """
    args = []
    stack = [i]
    i += 1
    arg_start = i

    while stack:
        token = tokens[i]

        if len(stack) == 1 and token.src == ",":
            args.append((arg_start, i))
            arg_start = i + 1
        elif token.src in BRACES:
            stack.append(i)
        elif token.src == BRACES[tokens[stack[-1]].src]:
            stack.pop()
            # if we're at the end, append that argument
            if not stack and tokens_to_src(tokens[arg_start:i]).strip():
                args.append(None)

        i += 1

    return args, i

```
