https://github.com/dbcli/pgcli/blob/f46d8446a34084cc2532041619d1f08bda7213e7/./pgcli/packages/parseutils/utils.py#L118-L138
```
🈚️

Timeout

@icontract.ensure(
    lambda word, result:
        # 先在一个匿名 lambda 里算出“正确”返回值的 value（字符串或 None）
        (lambda expected_value:
            # 如果期望是 None，则实际也必须是 None
            (expected_value is None and result is None)
            # 否则，实际结果必须是 Identifier 且 value 一致
            or (
                expected_value is not None
                and isinstance(result, Identifier)
                and result.value == expected_value
            )
        )(
            # ——下面这个大表达式就是“正确版本 parse_partial_identifier 的逻辑”，
            # 但只返回 Identifier.value（或 None），不直接返回 Identifier 本身。
            (lambda w:
                (lambda p:
                    (
                        # 情况一：当前 parse 结果只有一个 token 且就是 Identifier
                        p.tokens[0].value
                        if len(p.tokens) == 1 and isinstance(p.tokens[0], Identifier)
                        else
                        # 情况二：存在未匹配的双引号，需要补一个 '"' 再重新 parse
                        (lambda err_tok:
                            (
                                (lambda p2:
                                    p2.tokens[0].value
                                    if len(p2.tokens) == 1 and isinstance(p2.tokens[0], Identifier)
                                    else None
                                )(sqlparse.parse(w + '"')[0])
                                if err_tok  # 有 Error('"')，说明有未闭合的 "
                                else None   # 否则就直接返回 None
                            )
                        )(p.token_next_by(m=(Error, '"'))[1])
                    )
                )(sqlparse.parse(w)[0])
            )(word)
        )
)
```
```
None
```
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
===== 0 =====
```
     """
 
     p = sqlparse.parse(word)[0]
-    n_tok = len(p.tokens)
+    n_tok = 0  # Sets n_tok to 0, ignoring the actual number of tokens
     if n_tok == 1 and isinstance(p.tokens[0], Identifier):
         return p.tokens[0]
     elif p.token_next_by(m=(Error, '"'))[1]:
```
```
def parse_partial_identifier(word):
    """Attempt to parse a (partially typed) word as an identifier

    word may include a schema qualification, like `schema_name.partial_name`
    or `schema_name.` There may also be unclosed quotation marks, like
    `"schema`, or `schema."partial_name`

    :param word: string representing a (partially complete) identifier
    :return: sqlparse.sql.Identifier, or None
    """

    p = sqlparse.parse(word)[0]
    n_tok = 0  # Sets n_tok to 0, ignoring the actual number of tokens
    if n_tok == 1 and isinstance(p.tokens[0], Identifier):
        return p.tokens[0]
    elif p.token_next_by(m=(Error, '"'))[1]:
        # An unmatched double quote, e.g. '"foo', 'foo."', or 'foo."bar'
        # Close the double quote, then reparse
        return parse_partial_identifier(word + '"')
    else:
        return None
```
===== 1 =====
```
     """
 
     p = sqlparse.parse(word)[0]
-    n_tok = len(p.tokens)
+    n_tok = None
     if n_tok == 1 and isinstance(p.tokens[0], Identifier):
         return p.tokens[0]
     elif p.token_next_by(m=(Error, '"'))[1]:
@@ -18,4 +18,4 @@         # Close the double quote, then reparse
         return parse_partial_identifier(word + '"')
     else:
-        return None+        return None
```
```
def parse_partial_identifier(word):
    """Attempt to parse a (partially typed) word as an identifier

    word may include a schema qualification, like `schema_name.partial_name`
    or `schema_name.` There may also be unclosed quotation marks, like
    `"schema`, or `schema."partial_name`

    :param word: string representing a (partially complete) identifier
    :return: sqlparse.sql.Identifier, or None
    """

    p = sqlparse.parse(word)[0]
    n_tok = None
    if n_tok == 1 and isinstance(p.tokens[0], Identifier):
        return p.tokens[0]
    elif p.token_next_by(m=(Error, '"'))[1]:
        # An unmatched double quote, e.g. '"foo', 'foo."', or 'foo."bar'
        # Close the double quote, then reparse
        return parse_partial_identifier(word + '"')
    else:
        return None

```
===== 2 =====
```
     """
 
     p = sqlparse.parse(word)[0]
-    n_tok = len(p.tokens)
+    n_tok = len(p.tokens) + 1  # Incorrectly adds 1 to the count
     if n_tok == 1 and isinstance(p.tokens[0], Identifier):
         return p.tokens[0]
     elif p.token_next_by(m=(Error, '"'))[1]:
```
```
def parse_partial_identifier(word):
    """Attempt to parse a (partially typed) word as an identifier

    word may include a schema qualification, like `schema_name.partial_name`
    or `schema_name.` There may also be unclosed quotation marks, like
    `"schema`, or `schema."partial_name`

    :param word: string representing a (partially complete) identifier
    :return: sqlparse.sql.Identifier, or None
    """

    p = sqlparse.parse(word)[0]
    n_tok = len(p.tokens) + 1  # Incorrectly adds 1 to the count
    if n_tok == 1 and isinstance(p.tokens[0], Identifier):
        return p.tokens[0]
    elif p.token_next_by(m=(Error, '"'))[1]:
        # An unmatched double quote, e.g. '"foo', 'foo."', or 'foo."bar'
        # Close the double quote, then reparse
        return parse_partial_identifier(word + '"')
    else:
        return None
```
===== 3 =====
```
     """
 
     p = sqlparse.parse(word)[0]
-    n_tok = len(p.tokens)
+    n_tok = len(p.tokens) - 1  # Incorrectly subtracts 1 from the count
     if n_tok == 1 and isinstance(p.tokens[0], Identifier):
         return p.tokens[0]
     elif p.token_next_by(m=(Error, '"'))[1]:
```
```
def parse_partial_identifier(word):
    """Attempt to parse a (partially typed) word as an identifier

    word may include a schema qualification, like `schema_name.partial_name`
    or `schema_name.` There may also be unclosed quotation marks, like
    `"schema`, or `schema."partial_name`

    :param word: string representing a (partially complete) identifier
    :return: sqlparse.sql.Identifier, or None
    """

    p = sqlparse.parse(word)[0]
    n_tok = len(p.tokens) - 1  # Incorrectly subtracts 1 from the count
    if n_tok == 1 and isinstance(p.tokens[0], Identifier):
        return p.tokens[0]
    elif p.token_next_by(m=(Error, '"'))[1]:
        # An unmatched double quote, e.g. '"foo', 'foo."', or 'foo."bar'
        # Close the double quote, then reparse
        return parse_partial_identifier(word + '"')
    else:
        return None
```
===== 4 =====
```
     """
 
     p = sqlparse.parse(word)[0]
-    n_tok = len(p.tokens)
+    n_tok = len(p.tokens) // 2  # Incorrectly divides the count by 2
     if n_tok == 1 and isinstance(p.tokens[0], Identifier):
         return p.tokens[0]
     elif p.token_next_by(m=(Error, '"'))[1]:
```
```
def parse_partial_identifier(word):
    """Attempt to parse a (partially typed) word as an identifier

    word may include a schema qualification, like `schema_name.partial_name`
    or `schema_name.` There may also be unclosed quotation marks, like
    `"schema`, or `schema."partial_name`

    :param word: string representing a (partially complete) identifier
    :return: sqlparse.sql.Identifier, or None
    """

    p = sqlparse.parse(word)[0]
    n_tok = len(p.tokens) // 2  # Incorrectly divides the count by 2
    if n_tok == 1 and isinstance(p.tokens[0], Identifier):
        return p.tokens[0]
    elif p.token_next_by(m=(Error, '"'))[1]:
        # An unmatched double quote, e.g. '"foo', 'foo."', or 'foo."bar'
        # Close the double quote, then reparse
        return parse_partial_identifier(word + '"')
    else:
        return None
```
===== 5 =====
```
 
     p = sqlparse.parse(word)[0]
     n_tok = len(p.tokens)
-    if n_tok == 1 and isinstance(p.tokens[0], Identifier):
+    if n_tok != 1 and isinstance(p.tokens[0], Identifier):
         return p.tokens[0]
     elif p.token_next_by(m=(Error, '"'))[1]:
         # An unmatched double quote, e.g. '"foo', 'foo."', or 'foo."bar'
         # Close the double quote, then reparse
         return parse_partial_identifier(word + '"')
     else:
-        return None+        return None
```
```
def parse_partial_identifier(word):
    """Attempt to parse a (partially typed) word as an identifier

    word may include a schema qualification, like `schema_name.partial_name`
    or `schema_name.` There may also be unclosed quotation marks, like
    `"schema`, or `schema."partial_name`

    :param word: string representing a (partially complete) identifier
    :return: sqlparse.sql.Identifier, or None
    """

    p = sqlparse.parse(word)[0]
    n_tok = len(p.tokens)
    if n_tok != 1 and isinstance(p.tokens[0], Identifier):
        return p.tokens[0]
    elif p.token_next_by(m=(Error, '"'))[1]:
        # An unmatched double quote, e.g. '"foo', 'foo."', or 'foo."bar'
        # Close the double quote, then reparse
        return parse_partial_identifier(word + '"')
    else:
        return None

```
===== 6 =====
```
 
     p = sqlparse.parse(word)[0]
     n_tok = len(p.tokens)
-    if n_tok == 1 and isinstance(p.tokens[0], Identifier):
+    if n_tok == 0 and isinstance(p.tokens[0], Identifier):
         return p.tokens[0]
     elif p.token_next_by(m=(Error, '"'))[1]:
         # An unmatched double quote, e.g. '"foo', 'foo."', or 'foo."bar'
```
```
def parse_partial_identifier(word):
    """Attempt to parse a (partially typed) word as an identifier

    word may include a schema qualification, like `schema_name.partial_name`
    or `schema_name.` There may also be unclosed quotation marks, like
    `"schema`, or `schema."partial_name`

    :param word: string representing a (partially complete) identifier
    :return: sqlparse.sql.Identifier, or None
    """

    p = sqlparse.parse(word)[0]
    n_tok = len(p.tokens)
    if n_tok == 0 and isinstance(p.tokens[0], Identifier):
        return p.tokens[0]
    elif p.token_next_by(m=(Error, '"'))[1]:
        # An unmatched double quote, e.g. '"foo', 'foo."', or 'foo."bar'
        # Close the double quote, then reparse
        return parse_partial_identifier(word + '"')
    else:
        return None
```
===== 7 =====
```
 
     p = sqlparse.parse(word)[0]
     n_tok = len(p.tokens)
-    if n_tok == 1 and isinstance(p.tokens[0], Identifier):
+    if n_tok == 1 and isinstance(None, Identifier):
         return p.tokens[0]
     elif p.token_next_by(m=(Error, '"'))[1]:
         # An unmatched double quote, e.g. '"foo', 'foo."', or 'foo."bar'
         # Close the double quote, then reparse
         return parse_partial_identifier(word + '"')
     else:
-        return None+        return None
```
```
def parse_partial_identifier(word):
    """Attempt to parse a (partially typed) word as an identifier

    word may include a schema qualification, like `schema_name.partial_name`
    or `schema_name.` There may also be unclosed quotation marks, like
    `"schema`, or `schema."partial_name`

    :param word: string representing a (partially complete) identifier
    :return: sqlparse.sql.Identifier, or None
    """

    p = sqlparse.parse(word)[0]
    n_tok = len(p.tokens)
    if n_tok == 1 and isinstance(None, Identifier):
        return p.tokens[0]
    elif p.token_next_by(m=(Error, '"'))[1]:
        # An unmatched double quote, e.g. '"foo', 'foo."', or 'foo."bar'
        # Close the double quote, then reparse
        return parse_partial_identifier(word + '"')
    else:
        return None

```
===== 8 =====
```
 
     p = sqlparse.parse(word)[0]
     n_tok = len(p.tokens)
-    if n_tok == 1 and isinstance(p.tokens[0], Identifier):
+    if n_tok == 1 and isinstance(p.tokens[0], Identifier) and p.tokens[0].value == "":
         return p.tokens[0]
     elif p.token_next_by(m=(Error, '"'))[1]:
         # An unmatched double quote, e.g. '"foo', 'foo."', or 'foo."bar'
```
```
def parse_partial_identifier(word):
    """Attempt to parse a (partially typed) word as an identifier

    word may include a schema qualification, like `schema_name.partial_name`
    or `schema_name.` There may also be unclosed quotation marks, like
    `"schema`, or `schema."partial_name`

    :param word: string representing a (partially complete) identifier
    :return: sqlparse.sql.Identifier, or None
    """

    p = sqlparse.parse(word)[0]
    n_tok = len(p.tokens)
    if n_tok == 1 and isinstance(p.tokens[0], Identifier) and p.tokens[0].value == "":
        return p.tokens[0]
    elif p.token_next_by(m=(Error, '"'))[1]:
        # An unmatched double quote, e.g. '"foo', 'foo."', or 'foo."bar'
        # Close the double quote, then reparse
        return parse_partial_identifier(word + '"')
    else:
        return None
```
===== 9 =====
```
 
     p = sqlparse.parse(word)[0]
     n_tok = len(p.tokens)
-    if n_tok == 1 and isinstance(p.tokens[0], Identifier):
+    if n_tok == 1 and isinstance(p.tokens[0], str):
         return p.tokens[0]
     elif p.token_next_by(m=(Error, '"'))[1]:
         # An unmatched double quote, e.g. '"foo', 'foo."', or 'foo."bar'
```
```
def parse_partial_identifier(word):
    """Attempt to parse a (partially typed) word as an identifier

    word may include a schema qualification, like `schema_name.partial_name`
    or `schema_name.` There may also be unclosed quotation marks, like
    `"schema`, or `schema."partial_name`

    :param word: string representing a (partially complete) identifier
    :return: sqlparse.sql.Identifier, or None
    """

    p = sqlparse.parse(word)[0]
    n_tok = len(p.tokens)
    if n_tok == 1 and isinstance(p.tokens[0], str):
        return p.tokens[0]
    elif p.token_next_by(m=(Error, '"'))[1]:
        # An unmatched double quote, e.g. '"foo', 'foo."', or 'foo."bar'
        # Close the double quote, then reparse
        return parse_partial_identifier(word + '"')
    else:
        return None
```
===== 10 =====
```
 
     p = sqlparse.parse(word)[0]
     n_tok = len(p.tokens)
-    if n_tok == 1 and isinstance(p.tokens[0], Identifier):
+    if n_tok == 1 and not isinstance(p.tokens[0], Identifier):
         return p.tokens[0]
     elif p.token_next_by(m=(Error, '"'))[1]:
         # An unmatched double quote, e.g. '"foo', 'foo."', or 'foo."bar'
```
```
def parse_partial_identifier(word):
    """Attempt to parse a (partially typed) word as an identifier

    word may include a schema qualification, like `schema_name.partial_name`
    or `schema_name.` There may also be unclosed quotation marks, like
    `"schema`, or `schema."partial_name`

    :param word: string representing a (partially complete) identifier
    :return: sqlparse.sql.Identifier, or None
    """

    p = sqlparse.parse(word)[0]
    n_tok = len(p.tokens)
    if n_tok == 1 and not isinstance(p.tokens[0], Identifier):
        return p.tokens[0]
    elif p.token_next_by(m=(Error, '"'))[1]:
        # An unmatched double quote, e.g. '"foo', 'foo."', or 'foo."bar'
        # Close the double quote, then reparse
        return parse_partial_identifier(word + '"')
    else:
        return None
```
===== 11 =====
```
 
     p = sqlparse.parse(word)[0]
     n_tok = len(p.tokens)
-    if n_tok == 1 and isinstance(p.tokens[0], Identifier):
+    if n_tok == 1 or isinstance(p.tokens[0], Identifier):
         return p.tokens[0]
     elif p.token_next_by(m=(Error, '"'))[1]:
         # An unmatched double quote, e.g. '"foo', 'foo."', or 'foo."bar'
         # Close the double quote, then reparse
         return parse_partial_identifier(word + '"')
     else:
-        return None+        return None
```
```
def parse_partial_identifier(word):
    """Attempt to parse a (partially typed) word as an identifier

    word may include a schema qualification, like `schema_name.partial_name`
    or `schema_name.` There may also be unclosed quotation marks, like
    `"schema`, or `schema."partial_name`

    :param word: string representing a (partially complete) identifier
    :return: sqlparse.sql.Identifier, or None
    """

    p = sqlparse.parse(word)[0]
    n_tok = len(p.tokens)
    if n_tok == 1 or isinstance(p.tokens[0], Identifier):
        return p.tokens[0]
    elif p.token_next_by(m=(Error, '"'))[1]:
        # An unmatched double quote, e.g. '"foo', 'foo."', or 'foo."bar'
        # Close the double quote, then reparse
        return parse_partial_identifier(word + '"')
    else:
        return None

```
===== 12 =====
```
 
     p = sqlparse.parse(word)[0]
     n_tok = len(p.tokens)
-    if n_tok == 1 and isinstance(p.tokens[0], Identifier):
+    if n_tok == 2 and isinstance(p.tokens[0], Identifier):
         return p.tokens[0]
     elif p.token_next_by(m=(Error, '"'))[1]:
         # An unmatched double quote, e.g. '"foo', 'foo."', or 'foo."bar'
         # Close the double quote, then reparse
         return parse_partial_identifier(word + '"')
     else:
-        return None+        return None
```
```
def parse_partial_identifier(word):
    """Attempt to parse a (partially typed) word as an identifier

    word may include a schema qualification, like `schema_name.partial_name`
    or `schema_name.` There may also be unclosed quotation marks, like
    `"schema`, or `schema."partial_name`

    :param word: string representing a (partially complete) identifier
    :return: sqlparse.sql.Identifier, or None
    """

    p = sqlparse.parse(word)[0]
    n_tok = len(p.tokens)
    if n_tok == 2 and isinstance(p.tokens[0], Identifier):
        return p.tokens[0]
    elif p.token_next_by(m=(Error, '"'))[1]:
        # An unmatched double quote, e.g. '"foo', 'foo."', or 'foo."bar'
        # Close the double quote, then reparse
        return parse_partial_identifier(word + '"')
    else:
        return None

```
===== 13 =====
```
 
     p = sqlparse.parse(word)[0]
     n_tok = len(p.tokens)
-    if n_tok == 1 and isinstance(p.tokens[0], Identifier):
+    if n_tok > 1 and isinstance(p.tokens[0], Identifier):
         return p.tokens[0]
     elif p.token_next_by(m=(Error, '"'))[1]:
         # An unmatched double quote, e.g. '"foo', 'foo."', or 'foo."bar'
```
```
def parse_partial_identifier(word):
    """Attempt to parse a (partially typed) word as an identifier

    word may include a schema qualification, like `schema_name.partial_name`
    or `schema_name.` There may also be unclosed quotation marks, like
    `"schema`, or `schema."partial_name`

    :param word: string representing a (partially complete) identifier
    :return: sqlparse.sql.Identifier, or None
    """

    p = sqlparse.parse(word)[0]
    n_tok = len(p.tokens)
    if n_tok > 1 and isinstance(p.tokens[0], Identifier):
        return p.tokens[0]
    elif p.token_next_by(m=(Error, '"'))[1]:
        # An unmatched double quote, e.g. '"foo', 'foo."', or 'foo."bar'
        # Close the double quote, then reparse
        return parse_partial_identifier(word + '"')
    else:
        return None
```
===== 14 =====
```
     n_tok = len(p.tokens)
     if n_tok == 1 and isinstance(p.tokens[0], Identifier):
         return p.tokens[0]
-    elif p.token_next_by(m=(Error, '"'))[1]:
+    elif p.token_next_by(m=(Error, "'"))[1]:  # Checks for unmatched single quotes instead of double quotes
         # An unmatched double quote, e.g. '"foo', 'foo."', or 'foo."bar'
         # Close the double quote, then reparse
         return parse_partial_identifier(word + '"')
```
```
def parse_partial_identifier(word):
    """Attempt to parse a (partially typed) word as an identifier

    word may include a schema qualification, like `schema_name.partial_name`
    or `schema_name.` There may also be unclosed quotation marks, like
    `"schema`, or `schema."partial_name`

    :param word: string representing a (partially complete) identifier
    :return: sqlparse.sql.Identifier, or None
    """

    p = sqlparse.parse(word)[0]
    n_tok = len(p.tokens)
    if n_tok == 1 and isinstance(p.tokens[0], Identifier):
        return p.tokens[0]
    elif p.token_next_by(m=(Error, "'"))[1]:  # Checks for unmatched single quotes instead of double quotes
        # An unmatched double quote, e.g. '"foo', 'foo."', or 'foo."bar'
        # Close the double quote, then reparse
        return parse_partial_identifier(word + '"')
    else:
        return None
```
===== 15 =====
```
     n_tok = len(p.tokens)
     if n_tok == 1 and isinstance(p.tokens[0], Identifier):
         return p.tokens[0]
-    elif p.token_next_by(m=(Error, '"'))[1]:
+    elif p.token_next_by(m=(Error, 'XX"XX'))[1]:
         # An unmatched double quote, e.g. '"foo', 'foo."', or 'foo."bar'
         # Close the double quote, then reparse
         return parse_partial_identifier(word + '"')
     else:
-        return None+        return None
```
```
def parse_partial_identifier(word):
    """Attempt to parse a (partially typed) word as an identifier

    word may include a schema qualification, like `schema_name.partial_name`
    or `schema_name.` There may also be unclosed quotation marks, like
    `"schema`, or `schema."partial_name`

    :param word: string representing a (partially complete) identifier
    :return: sqlparse.sql.Identifier, or None
    """

    p = sqlparse.parse(word)[0]
    n_tok = len(p.tokens)
    if n_tok == 1 and isinstance(p.tokens[0], Identifier):
        return p.tokens[0]
    elif p.token_next_by(m=(Error, 'XX"XX'))[1]:
        # An unmatched double quote, e.g. '"foo', 'foo."', or 'foo."bar'
        # Close the double quote, then reparse
        return parse_partial_identifier(word + '"')
    else:
        return None

```
===== 16 =====
```
     n_tok = len(p.tokens)
     if n_tok == 1 and isinstance(p.tokens[0], Identifier):
         return p.tokens[0]
-    elif p.token_next_by(m=(Error, '"'))[1]:
+    elif p.token_next_by(m=None)[1]:
         # An unmatched double quote, e.g. '"foo', 'foo."', or 'foo."bar'
         # Close the double quote, then reparse
         return parse_partial_identifier(word + '"')
     else:
-        return None+        return None
```
```
def parse_partial_identifier(word):
    """Attempt to parse a (partially typed) word as an identifier

    word may include a schema qualification, like `schema_name.partial_name`
    or `schema_name.` There may also be unclosed quotation marks, like
    `"schema`, or `schema."partial_name`

    :param word: string representing a (partially complete) identifier
    :return: sqlparse.sql.Identifier, or None
    """

    p = sqlparse.parse(word)[0]
    n_tok = len(p.tokens)
    if n_tok == 1 and isinstance(p.tokens[0], Identifier):
        return p.tokens[0]
    elif p.token_next_by(m=None)[1]:
        # An unmatched double quote, e.g. '"foo', 'foo."', or 'foo."bar'
        # Close the double quote, then reparse
        return parse_partial_identifier(word + '"')
    else:
        return None

```
