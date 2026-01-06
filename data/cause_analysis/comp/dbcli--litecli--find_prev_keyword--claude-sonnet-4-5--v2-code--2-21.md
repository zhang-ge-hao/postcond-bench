https://github.com/dbcli/litecli/blob/c072661298bc52b10c11e6571cc741a6d41360a7/./litecli/packages/parseutils.py#L169-L200
```
@icontract.ensure(lambda result: isinstance(result, tuple) and len(result) == 2)
@icontract.ensure(lambda sql, result: not sql.strip() or result[0] is not None or result[1] == "")
@icontract.ensure(lambda result: (result[0] is None) == (result[1] == ""))
@icontract.ensure(lambda result: result[0] is None or result[1].endswith(result[0].value))
@icontract.ensure(lambda result: result[0] is None or (result[0].value == "(" or (result[0].is_keyword and result[0].value.upper() not in ("AND", "OR", "NOT", "BETWEEN"))))
```
```
return value - built-in container of scalars


return value content

built-in container of scalars
```
passed
```
@icontract.snapshot(lambda sql: [(t.value, bool(getattr(t, "is_keyword", False))) for t in sqlparse.parse(sql)[0].flatten()] if sql and sql.strip() else [], name="flattened_info")
@icontract.ensure(lambda OLD, result, sql: (not sql.strip() and result == (None, "")) or (sql.strip() and (
    (any((val == "(" or (is_kw and val.upper() not in ("AND", "OR", "NOT", "BETWEEN"))) for val, is_kw in OLD.flattened_info) and
     result[0] is not None and
     result[0].value == OLD.flattened_info[max(i for i in range(len(OLD.flattened_info)) if (OLD.flattened_info[i][0] == "(" or (OLD.flattened_info[i][1] and OLD.flattened_info[i][0].upper() not in ("AND", "OR", "NOT", "BETWEEN"))))][0] and
     isinstance(result[1], str) and
     result[1] == "".join(OLD.flattened_info[i][0] for i in range(0, max(i for i in range(len(OLD.flattened_info)) if (OLD.flattened_info[i][0] == "(" or (OLD.flattened_info[i][1] and OLD.flattened_info[i][0].upper() not in ("AND", "OR", "NOT", "BETWEEN")))) + 1)))
    or
    (not any((val == "(" or (is_kw and val.upper() not in ("AND", "OR", "NOT", "BETWEEN"))) for val, is_kw in OLD.flattened_info) and result == (None, ""))
)))
```
===== 21: failed =====
```
             # Combine the string values of all tokens in the original list
             # up to and including the target keyword token t, to produce a
             # query string with everything after the keyword token removed
-            text = "".join(tok.value for tok in flattened[: idx + 1])
+            text = " ".join(tok.value for tok in flattened[: idx + 1])
             return t, text
 
     return None, ""
```
```
def find_prev_keyword(sql):
    """Find the last sql keyword in an SQL statement

    Returns the value of the last keyword, and the text of the query with
    everything after the last keyword stripped
    """
    if not sql.strip():
        return None, ""

    parsed = sqlparse.parse(sql)[0]
    flattened = list(parsed.flatten())

    logical_operators = ("AND", "OR", "NOT", "BETWEEN")

    for t in reversed(flattened):
        if t.value == "(" or (t.is_keyword and (t.value.upper() not in logical_operators)):
            # Find the location of token t in the original parsed statement
            # We can't use parsed.token_index(t) because t may be a child token
            # inside a TokenList, in which case token_index thows an error
            # Minimal example:
            #   p = sqlparse.parse('select * from foo where bar')
            #   t = list(p.flatten())[-3]  # The "Where" token
            #   p.token_index(t)  # Throws ValueError: not in list
            idx = flattened.index(t)

            # Combine the string values of all tokens in the original list
            # up to and including the target keyword token t, to produce a
            # query string with everything after the keyword token removed
            text = " ".join(tok.value for tok in flattened[: idx + 1])
            return t, text

    return None, ""
```
