https://github.com/dbcli/pgcli/blob/f46d8446a34084cc2532041619d1f08bda7213e7/./pgcli/packages/parseutils/ctes.py#L47-L91
```
🈚️

Timeout

@icontract.ensure(
    lambda sql, result: result == (
        (lambda p:
         (lambda idx_tok:
          (lambda idx, tok:
           # if not (tok and tok.ttype == CTE): return [], sql
           ([], sql) if not (tok and tok.ttype == CTE) else
           (lambda idx2_tok:
            (lambda idx2, tok2:
             ([], "") if not tok2 else
             (lambda start_pos, ctes_tok:
              (lambda ctes, first_cte_tok:
               (lambda idx_after:
                (
                    ctes,
                    "".join(str(t) for t in p.tokens[idx_after:])
                )
               )(
                   p.token_index(first_cte_tok) + 1
               )
              )(
                  # ctes
                  (lambda tok3, start_pos3:
                   (
                       [
                           cte for cte in
                           (
                               get_cte_from_token(
                                   t,
                                   start_pos3 + token_start_pos(tok3.tokens, tok3.token_index(t))
                               )
                               for t in tok3.get_identifiers()
                           )
                           if cte
                       ]
                       if isinstance(tok3, IdentifierList)
                       else (
                           [cte] if isinstance(tok3, Identifier)
                           and (cte := get_cte_from_token(tok3, start_pos3))
                           else []
                       )
                   )
                  )(ctes_tok, start_pos),
                  ctes_tok
              )
             )(
                 token_start_pos(p.tokens, idx2),
                 tok2
             )
            )(*idx2_tok)
           )( *idx_tok)
         )(p.token_next(-1, skip_ws=True, skip_cm=True))
        )(parse(sql)[0])
    )
)
)
```
```
None
```
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69]
===== 0 =====
```
 
     # Make sure the first meaningful token is "WITH" which is necessary to
     # define CTEs
-    idx, tok = p.token_next(-1, skip_ws=True, skip_cm=True)
+    idx, tok = p.token_next(+1, skip_ws=True, skip_cm=True)
     if not (tok and tok.ttype == CTE):
         return [], sql
 
@@ -42,4 +42,4 @@     # Collapse everything after the ctes into a remainder query
     remainder = "".join(str(tok) for tok in p.tokens[idx:])
 
-    return ctes, remainder+    return ctes, remainder
```
```
def extract_ctes(sql):
    """Extract constant table expresseions from a query

    Returns tuple (ctes, remainder_sql)

    ctes is a list of TableExpression namedtuples
    remainder_sql is the text from the original query after the CTEs have
    been stripped.
    """

    p = parse(sql)[0]

    # Make sure the first meaningful token is "WITH" which is necessary to
    # define CTEs
    idx, tok = p.token_next(+1, skip_ws=True, skip_cm=True)
    if not (tok and tok.ttype == CTE):
        return [], sql

    # Get the next (meaningful) token, which should be the first CTE
    idx, tok = p.token_next(idx)
    if not tok:
        return ([], "")
    start_pos = token_start_pos(p.tokens, idx)
    ctes = []

    if isinstance(tok, IdentifierList):
        # Multiple ctes
        for t in tok.get_identifiers():
            cte_start_offset = token_start_pos(tok.tokens, tok.token_index(t))
            cte = get_cte_from_token(t, start_pos + cte_start_offset)
            if not cte:
                continue
            ctes.append(cte)
    elif isinstance(tok, Identifier):
        # A single CTE
        cte = get_cte_from_token(tok, start_pos)
        if cte:
            ctes.append(cte)

    idx = p.token_index(tok) + 1

    # Collapse everything after the ctes into a remainder query
    remainder = "".join(str(tok) for tok in p.tokens[idx:])

    return ctes, remainder

```
===== 1 =====
```
 
     # Make sure the first meaningful token is "WITH" which is necessary to
     # define CTEs
-    idx, tok = p.token_next(-1, skip_ws=True, skip_cm=True)
+    idx, tok = p.token_next(-1, skip_ws=False, skip_cm=True)
     if not (tok and tok.ttype == CTE):
         return [], sql
```
```
def extract_ctes(sql):
    """Extract constant table expresseions from a query

    Returns tuple (ctes, remainder_sql)

    ctes is a list of TableExpression namedtuples
    remainder_sql is the text from the original query after the CTEs have
    been stripped.
    """

    p = parse(sql)[0]

    # Make sure the first meaningful token is "WITH" which is necessary to
    # define CTEs
    idx, tok = p.token_next(-1, skip_ws=False, skip_cm=True)
    if not (tok and tok.ttype == CTE):
        return [], sql

    # Get the next (meaningful) token, which should be the first CTE
    idx, tok = p.token_next(idx)
    if not tok:
        return ([], "")
    start_pos = token_start_pos(p.tokens, idx)
    ctes = []

    if isinstance(tok, IdentifierList):
        # Multiple ctes
        for t in tok.get_identifiers():
            cte_start_offset = token_start_pos(tok.tokens, tok.token_index(t))
            cte = get_cte_from_token(t, start_pos + cte_start_offset)
            if not cte:
                continue
            ctes.append(cte)
    elif isinstance(tok, Identifier):
        # A single CTE
        cte = get_cte_from_token(tok, start_pos)
        if cte:
            ctes.append(cte)

    idx = p.token_index(tok) + 1

    # Collapse everything after the ctes into a remainder query
    remainder = "".join(str(tok) for tok in p.tokens[idx:])

    return ctes, remainder
```
===== 2 =====
```
 
     # Make sure the first meaningful token is "WITH" which is necessary to
     # define CTEs
-    idx, tok = p.token_next(-1, skip_ws=True, skip_cm=True)
+    idx, tok = p.token_next(-1, skip_ws=False, skip_cm=True)
     if not (tok and tok.ttype == CTE):
         return [], sql
 
@@ -42,4 +42,4 @@     # Collapse everything after the ctes into a remainder query
     remainder = "".join(str(tok) for tok in p.tokens[idx:])
 
-    return ctes, remainder+    return ctes, remainder
```
```
def extract_ctes(sql):
    """Extract constant table expresseions from a query

    Returns tuple (ctes, remainder_sql)

    ctes is a list of TableExpression namedtuples
    remainder_sql is the text from the original query after the CTEs have
    been stripped.
    """

    p = parse(sql)[0]

    # Make sure the first meaningful token is "WITH" which is necessary to
    # define CTEs
    idx, tok = p.token_next(-1, skip_ws=False, skip_cm=True)
    if not (tok and tok.ttype == CTE):
        return [], sql

    # Get the next (meaningful) token, which should be the first CTE
    idx, tok = p.token_next(idx)
    if not tok:
        return ([], "")
    start_pos = token_start_pos(p.tokens, idx)
    ctes = []

    if isinstance(tok, IdentifierList):
        # Multiple ctes
        for t in tok.get_identifiers():
            cte_start_offset = token_start_pos(tok.tokens, tok.token_index(t))
            cte = get_cte_from_token(t, start_pos + cte_start_offset)
            if not cte:
                continue
            ctes.append(cte)
    elif isinstance(tok, Identifier):
        # A single CTE
        cte = get_cte_from_token(tok, start_pos)
        if cte:
            ctes.append(cte)

    idx = p.token_index(tok) + 1

    # Collapse everything after the ctes into a remainder query
    remainder = "".join(str(tok) for tok in p.tokens[idx:])

    return ctes, remainder

```
===== 3 =====
```
 
     # Make sure the first meaningful token is "WITH" which is necessary to
     # define CTEs
-    idx, tok = p.token_next(-1, skip_ws=True, skip_cm=True)
+    idx, tok = p.token_next(-1, skip_ws=None, skip_cm=True)
     if not (tok and tok.ttype == CTE):
         return [], sql
 
@@ -42,4 +42,4 @@     # Collapse everything after the ctes into a remainder query
     remainder = "".join(str(tok) for tok in p.tokens[idx:])
 
-    return ctes, remainder+    return ctes, remainder
```
```
def extract_ctes(sql):
    """Extract constant table expresseions from a query

    Returns tuple (ctes, remainder_sql)

    ctes is a list of TableExpression namedtuples
    remainder_sql is the text from the original query after the CTEs have
    been stripped.
    """

    p = parse(sql)[0]

    # Make sure the first meaningful token is "WITH" which is necessary to
    # define CTEs
    idx, tok = p.token_next(-1, skip_ws=None, skip_cm=True)
    if not (tok and tok.ttype == CTE):
        return [], sql

    # Get the next (meaningful) token, which should be the first CTE
    idx, tok = p.token_next(idx)
    if not tok:
        return ([], "")
    start_pos = token_start_pos(p.tokens, idx)
    ctes = []

    if isinstance(tok, IdentifierList):
        # Multiple ctes
        for t in tok.get_identifiers():
            cte_start_offset = token_start_pos(tok.tokens, tok.token_index(t))
            cte = get_cte_from_token(t, start_pos + cte_start_offset)
            if not cte:
                continue
            ctes.append(cte)
    elif isinstance(tok, Identifier):
        # A single CTE
        cte = get_cte_from_token(tok, start_pos)
        if cte:
            ctes.append(cte)

    idx = p.token_index(tok) + 1

    # Collapse everything after the ctes into a remainder query
    remainder = "".join(str(tok) for tok in p.tokens[idx:])

    return ctes, remainder

```
===== 4 =====
```
 
     # Make sure the first meaningful token is "WITH" which is necessary to
     # define CTEs
-    idx, tok = p.token_next(-1, skip_ws=True, skip_cm=True)
+    idx, tok = p.token_next(-1, skip_ws=True, )
     if not (tok and tok.ttype == CTE):
         return [], sql
 
@@ -42,4 +42,4 @@     # Collapse everything after the ctes into a remainder query
     remainder = "".join(str(tok) for tok in p.tokens[idx:])
 
-    return ctes, remainder+    return ctes, remainder
```
```
def extract_ctes(sql):
    """Extract constant table expresseions from a query

    Returns tuple (ctes, remainder_sql)

    ctes is a list of TableExpression namedtuples
    remainder_sql is the text from the original query after the CTEs have
    been stripped.
    """

    p = parse(sql)[0]

    # Make sure the first meaningful token is "WITH" which is necessary to
    # define CTEs
    idx, tok = p.token_next(-1, skip_ws=True, )
    if not (tok and tok.ttype == CTE):
        return [], sql

    # Get the next (meaningful) token, which should be the first CTE
    idx, tok = p.token_next(idx)
    if not tok:
        return ([], "")
    start_pos = token_start_pos(p.tokens, idx)
    ctes = []

    if isinstance(tok, IdentifierList):
        # Multiple ctes
        for t in tok.get_identifiers():
            cte_start_offset = token_start_pos(tok.tokens, tok.token_index(t))
            cte = get_cte_from_token(t, start_pos + cte_start_offset)
            if not cte:
                continue
            ctes.append(cte)
    elif isinstance(tok, Identifier):
        # A single CTE
        cte = get_cte_from_token(tok, start_pos)
        if cte:
            ctes.append(cte)

    idx = p.token_index(tok) + 1

    # Collapse everything after the ctes into a remainder query
    remainder = "".join(str(tok) for tok in p.tokens[idx:])

    return ctes, remainder

```
===== 5 =====
```
 
     # Make sure the first meaningful token is "WITH" which is necessary to
     # define CTEs
-    idx, tok = p.token_next(-1, skip_ws=True, skip_cm=True)
+    idx, tok = p.token_next(-1, skip_ws=True, skip_cm=False)
     if not (tok and tok.ttype == CTE):
         return [], sql
```
```
def extract_ctes(sql):
    """Extract constant table expresseions from a query

    Returns tuple (ctes, remainder_sql)

    ctes is a list of TableExpression namedtuples
    remainder_sql is the text from the original query after the CTEs have
    been stripped.
    """

    p = parse(sql)[0]

    # Make sure the first meaningful token is "WITH" which is necessary to
    # define CTEs
    idx, tok = p.token_next(-1, skip_ws=True, skip_cm=False)
    if not (tok and tok.ttype == CTE):
        return [], sql

    # Get the next (meaningful) token, which should be the first CTE
    idx, tok = p.token_next(idx)
    if not tok:
        return ([], "")
    start_pos = token_start_pos(p.tokens, idx)
    ctes = []

    if isinstance(tok, IdentifierList):
        # Multiple ctes
        for t in tok.get_identifiers():
            cte_start_offset = token_start_pos(tok.tokens, tok.token_index(t))
            cte = get_cte_from_token(t, start_pos + cte_start_offset)
            if not cte:
                continue
            ctes.append(cte)
    elif isinstance(tok, Identifier):
        # A single CTE
        cte = get_cte_from_token(tok, start_pos)
        if cte:
            ctes.append(cte)

    idx = p.token_index(tok) + 1

    # Collapse everything after the ctes into a remainder query
    remainder = "".join(str(tok) for tok in p.tokens[idx:])

    return ctes, remainder
```
===== 6 =====
```
 
     # Make sure the first meaningful token is "WITH" which is necessary to
     # define CTEs
-    idx, tok = p.token_next(-1, skip_ws=True, skip_cm=True)
+    idx, tok = p.token_next(-1, skip_ws=True, skip_cm=False)
     if not (tok and tok.ttype == CTE):
         return [], sql
 
@@ -42,4 +42,4 @@     # Collapse everything after the ctes into a remainder query
     remainder = "".join(str(tok) for tok in p.tokens[idx:])
 
-    return ctes, remainder+    return ctes, remainder
```
```
def extract_ctes(sql):
    """Extract constant table expresseions from a query

    Returns tuple (ctes, remainder_sql)

    ctes is a list of TableExpression namedtuples
    remainder_sql is the text from the original query after the CTEs have
    been stripped.
    """

    p = parse(sql)[0]

    # Make sure the first meaningful token is "WITH" which is necessary to
    # define CTEs
    idx, tok = p.token_next(-1, skip_ws=True, skip_cm=False)
    if not (tok and tok.ttype == CTE):
        return [], sql

    # Get the next (meaningful) token, which should be the first CTE
    idx, tok = p.token_next(idx)
    if not tok:
        return ([], "")
    start_pos = token_start_pos(p.tokens, idx)
    ctes = []

    if isinstance(tok, IdentifierList):
        # Multiple ctes
        for t in tok.get_identifiers():
            cte_start_offset = token_start_pos(tok.tokens, tok.token_index(t))
            cte = get_cte_from_token(t, start_pos + cte_start_offset)
            if not cte:
                continue
            ctes.append(cte)
    elif isinstance(tok, Identifier):
        # A single CTE
        cte = get_cte_from_token(tok, start_pos)
        if cte:
            ctes.append(cte)

    idx = p.token_index(tok) + 1

    # Collapse everything after the ctes into a remainder query
    remainder = "".join(str(tok) for tok in p.tokens[idx:])

    return ctes, remainder

```
===== 7 =====
```
 
     # Make sure the first meaningful token is "WITH" which is necessary to
     # define CTEs
-    idx, tok = p.token_next(-1, skip_ws=True, skip_cm=True)
+    idx, tok = p.token_next(-1, skip_ws=True, skip_cm=None)
     if not (tok and tok.ttype == CTE):
         return [], sql
 
@@ -42,4 +42,4 @@     # Collapse everything after the ctes into a remainder query
     remainder = "".join(str(tok) for tok in p.tokens[idx:])
 
-    return ctes, remainder+    return ctes, remainder
```
```
def extract_ctes(sql):
    """Extract constant table expresseions from a query

    Returns tuple (ctes, remainder_sql)

    ctes is a list of TableExpression namedtuples
    remainder_sql is the text from the original query after the CTEs have
    been stripped.
    """

    p = parse(sql)[0]

    # Make sure the first meaningful token is "WITH" which is necessary to
    # define CTEs
    idx, tok = p.token_next(-1, skip_ws=True, skip_cm=None)
    if not (tok and tok.ttype == CTE):
        return [], sql

    # Get the next (meaningful) token, which should be the first CTE
    idx, tok = p.token_next(idx)
    if not tok:
        return ([], "")
    start_pos = token_start_pos(p.tokens, idx)
    ctes = []

    if isinstance(tok, IdentifierList):
        # Multiple ctes
        for t in tok.get_identifiers():
            cte_start_offset = token_start_pos(tok.tokens, tok.token_index(t))
            cte = get_cte_from_token(t, start_pos + cte_start_offset)
            if not cte:
                continue
            ctes.append(cte)
    elif isinstance(tok, Identifier):
        # A single CTE
        cte = get_cte_from_token(tok, start_pos)
        if cte:
            ctes.append(cte)

    idx = p.token_index(tok) + 1

    # Collapse everything after the ctes into a remainder query
    remainder = "".join(str(tok) for tok in p.tokens[idx:])

    return ctes, remainder

```
===== 8 =====
```
 
     # Make sure the first meaningful token is "WITH" which is necessary to
     # define CTEs
-    idx, tok = p.token_next(-1, skip_ws=True, skip_cm=True)
+    idx, tok = p.token_next(-2, skip_ws=True, skip_cm=True)
     if not (tok and tok.ttype == CTE):
         return [], sql
```
```
def extract_ctes(sql):
    """Extract constant table expresseions from a query

    Returns tuple (ctes, remainder_sql)

    ctes is a list of TableExpression namedtuples
    remainder_sql is the text from the original query after the CTEs have
    been stripped.
    """

    p = parse(sql)[0]

    # Make sure the first meaningful token is "WITH" which is necessary to
    # define CTEs
    idx, tok = p.token_next(-2, skip_ws=True, skip_cm=True)
    if not (tok and tok.ttype == CTE):
        return [], sql

    # Get the next (meaningful) token, which should be the first CTE
    idx, tok = p.token_next(idx)
    if not tok:
        return ([], "")
    start_pos = token_start_pos(p.tokens, idx)
    ctes = []

    if isinstance(tok, IdentifierList):
        # Multiple ctes
        for t in tok.get_identifiers():
            cte_start_offset = token_start_pos(tok.tokens, tok.token_index(t))
            cte = get_cte_from_token(t, start_pos + cte_start_offset)
            if not cte:
                continue
            ctes.append(cte)
    elif isinstance(tok, Identifier):
        # A single CTE
        cte = get_cte_from_token(tok, start_pos)
        if cte:
            ctes.append(cte)

    idx = p.token_index(tok) + 1

    # Collapse everything after the ctes into a remainder query
    remainder = "".join(str(tok) for tok in p.tokens[idx:])

    return ctes, remainder
```
===== 9 =====
```
 
     # Make sure the first meaningful token is "WITH" which is necessary to
     # define CTEs
-    idx, tok = p.token_next(-1, skip_ws=True, skip_cm=True)
+    idx, tok = p.token_next(-2, skip_ws=True, skip_cm=True)
     if not (tok and tok.ttype == CTE):
         return [], sql
 
@@ -42,4 +42,4 @@     # Collapse everything after the ctes into a remainder query
     remainder = "".join(str(tok) for tok in p.tokens[idx:])
 
-    return ctes, remainder+    return ctes, remainder
```
```
def extract_ctes(sql):
    """Extract constant table expresseions from a query

    Returns tuple (ctes, remainder_sql)

    ctes is a list of TableExpression namedtuples
    remainder_sql is the text from the original query after the CTEs have
    been stripped.
    """

    p = parse(sql)[0]

    # Make sure the first meaningful token is "WITH" which is necessary to
    # define CTEs
    idx, tok = p.token_next(-2, skip_ws=True, skip_cm=True)
    if not (tok and tok.ttype == CTE):
        return [], sql

    # Get the next (meaningful) token, which should be the first CTE
    idx, tok = p.token_next(idx)
    if not tok:
        return ([], "")
    start_pos = token_start_pos(p.tokens, idx)
    ctes = []

    if isinstance(tok, IdentifierList):
        # Multiple ctes
        for t in tok.get_identifiers():
            cte_start_offset = token_start_pos(tok.tokens, tok.token_index(t))
            cte = get_cte_from_token(t, start_pos + cte_start_offset)
            if not cte:
                continue
            ctes.append(cte)
    elif isinstance(tok, Identifier):
        # A single CTE
        cte = get_cte_from_token(tok, start_pos)
        if cte:
            ctes.append(cte)

    idx = p.token_index(tok) + 1

    # Collapse everything after the ctes into a remainder query
    remainder = "".join(str(tok) for tok in p.tokens[idx:])

    return ctes, remainder

```
===== 10 =====
```
 
     # Make sure the first meaningful token is "WITH" which is necessary to
     # define CTEs
-    idx, tok = p.token_next(-1, skip_ws=True, skip_cm=True)
+    idx, tok = p.token_next(0, skip_ws=True, skip_cm=True)
     if not (tok and tok.ttype == CTE):
         return [], sql
```
```
def extract_ctes(sql):
    """Extract constant table expresseions from a query

    Returns tuple (ctes, remainder_sql)

    ctes is a list of TableExpression namedtuples
    remainder_sql is the text from the original query after the CTEs have
    been stripped.
    """

    p = parse(sql)[0]

    # Make sure the first meaningful token is "WITH" which is necessary to
    # define CTEs
    idx, tok = p.token_next(0, skip_ws=True, skip_cm=True)
    if not (tok and tok.ttype == CTE):
        return [], sql

    # Get the next (meaningful) token, which should be the first CTE
    idx, tok = p.token_next(idx)
    if not tok:
        return ([], "")
    start_pos = token_start_pos(p.tokens, idx)
    ctes = []

    if isinstance(tok, IdentifierList):
        # Multiple ctes
        for t in tok.get_identifiers():
            cte_start_offset = token_start_pos(tok.tokens, tok.token_index(t))
            cte = get_cte_from_token(t, start_pos + cte_start_offset)
            if not cte:
                continue
            ctes.append(cte)
    elif isinstance(tok, Identifier):
        # A single CTE
        cte = get_cte_from_token(tok, start_pos)
        if cte:
            ctes.append(cte)

    idx = p.token_index(tok) + 1

    # Collapse everything after the ctes into a remainder query
    remainder = "".join(str(tok) for tok in p.tokens[idx:])

    return ctes, remainder
```
===== 11 =====
```
 
     # Make sure the first meaningful token is "WITH" which is necessary to
     # define CTEs
-    idx, tok = p.token_next(-1, skip_ws=True, skip_cm=True)
+    idx, tok = p.token_next(1, skip_ws=True, skip_cm=True)
     if not (tok and tok.ttype == CTE):
         return [], sql
```
```
def extract_ctes(sql):
    """Extract constant table expresseions from a query

    Returns tuple (ctes, remainder_sql)

    ctes is a list of TableExpression namedtuples
    remainder_sql is the text from the original query after the CTEs have
    been stripped.
    """

    p = parse(sql)[0]

    # Make sure the first meaningful token is "WITH" which is necessary to
    # define CTEs
    idx, tok = p.token_next(1, skip_ws=True, skip_cm=True)
    if not (tok and tok.ttype == CTE):
        return [], sql

    # Get the next (meaningful) token, which should be the first CTE
    idx, tok = p.token_next(idx)
    if not tok:
        return ([], "")
    start_pos = token_start_pos(p.tokens, idx)
    ctes = []

    if isinstance(tok, IdentifierList):
        # Multiple ctes
        for t in tok.get_identifiers():
            cte_start_offset = token_start_pos(tok.tokens, tok.token_index(t))
            cte = get_cte_from_token(t, start_pos + cte_start_offset)
            if not cte:
                continue
            ctes.append(cte)
    elif isinstance(tok, Identifier):
        # A single CTE
        cte = get_cte_from_token(tok, start_pos)
        if cte:
            ctes.append(cte)

    idx = p.token_index(tok) + 1

    # Collapse everything after the ctes into a remainder query
    remainder = "".join(str(tok) for tok in p.tokens[idx:])

    return ctes, remainder
```
===== 12 =====
```
 
     # Make sure the first meaningful token is "WITH" which is necessary to
     # define CTEs
-    idx, tok = p.token_next(-1, skip_ws=True, skip_cm=True)
+    idx, tok = p.token_next(None, skip_ws=True, skip_cm=True)
     if not (tok and tok.ttype == CTE):
         return [], sql
 
@@ -42,4 +42,4 @@     # Collapse everything after the ctes into a remainder query
     remainder = "".join(str(tok) for tok in p.tokens[idx:])
 
-    return ctes, remainder+    return ctes, remainder
```
```
def extract_ctes(sql):
    """Extract constant table expresseions from a query

    Returns tuple (ctes, remainder_sql)

    ctes is a list of TableExpression namedtuples
    remainder_sql is the text from the original query after the CTEs have
    been stripped.
    """

    p = parse(sql)[0]

    # Make sure the first meaningful token is "WITH" which is necessary to
    # define CTEs
    idx, tok = p.token_next(None, skip_ws=True, skip_cm=True)
    if not (tok and tok.ttype == CTE):
        return [], sql

    # Get the next (meaningful) token, which should be the first CTE
    idx, tok = p.token_next(idx)
    if not tok:
        return ([], "")
    start_pos = token_start_pos(p.tokens, idx)
    ctes = []

    if isinstance(tok, IdentifierList):
        # Multiple ctes
        for t in tok.get_identifiers():
            cte_start_offset = token_start_pos(tok.tokens, tok.token_index(t))
            cte = get_cte_from_token(t, start_pos + cte_start_offset)
            if not cte:
                continue
            ctes.append(cte)
    elif isinstance(tok, Identifier):
        # A single CTE
        cte = get_cte_from_token(tok, start_pos)
        if cte:
            ctes.append(cte)

    idx = p.token_index(tok) + 1

    # Collapse everything after the ctes into a remainder query
    remainder = "".join(str(tok) for tok in p.tokens[idx:])

    return ctes, remainder

```
===== 13 =====
```
         return [], sql
 
     # Get the next (meaningful) token, which should be the first CTE
-    idx, tok = p.token_next(idx)
+    idx, tok = p.token_next(-1)  # This will retrieve the previous token instead of the next one
     if not tok:
         return ([], "")
     start_pos = token_start_pos(p.tokens, idx)
```
```
def extract_ctes(sql):
    """Extract constant table expresseions from a query

    Returns tuple (ctes, remainder_sql)

    ctes is a list of TableExpression namedtuples
    remainder_sql is the text from the original query after the CTEs have
    been stripped.
    """

    p = parse(sql)[0]

    # Make sure the first meaningful token is "WITH" which is necessary to
    # define CTEs
    idx, tok = p.token_next(-1, skip_ws=True, skip_cm=True)
    if not (tok and tok.ttype == CTE):
        return [], sql

    # Get the next (meaningful) token, which should be the first CTE
    idx, tok = p.token_next(-1)  # This will retrieve the previous token instead of the next one
    if not tok:
        return ([], "")
    start_pos = token_start_pos(p.tokens, idx)
    ctes = []

    if isinstance(tok, IdentifierList):
        # Multiple ctes
        for t in tok.get_identifiers():
            cte_start_offset = token_start_pos(tok.tokens, tok.token_index(t))
            cte = get_cte_from_token(t, start_pos + cte_start_offset)
            if not cte:
                continue
            ctes.append(cte)
    elif isinstance(tok, Identifier):
        # A single CTE
        cte = get_cte_from_token(tok, start_pos)
        if cte:
            ctes.append(cte)

    idx = p.token_index(tok) + 1

    # Collapse everything after the ctes into a remainder query
    remainder = "".join(str(tok) for tok in p.tokens[idx:])

    return ctes, remainder
```
===== 14 =====
```
         return [], sql
 
     # Get the next (meaningful) token, which should be the first CTE
-    idx, tok = p.token_next(idx)
+    idx, tok = p.token_next(None)
     if not tok:
         return ([], "")
     start_pos = token_start_pos(p.tokens, idx)
@@ -42,4 +42,4 @@     # Collapse everything after the ctes into a remainder query
     remainder = "".join(str(tok) for tok in p.tokens[idx:])
 
-    return ctes, remainder+    return ctes, remainder
```
```
def extract_ctes(sql):
    """Extract constant table expresseions from a query

    Returns tuple (ctes, remainder_sql)

    ctes is a list of TableExpression namedtuples
    remainder_sql is the text from the original query after the CTEs have
    been stripped.
    """

    p = parse(sql)[0]

    # Make sure the first meaningful token is "WITH" which is necessary to
    # define CTEs
    idx, tok = p.token_next(-1, skip_ws=True, skip_cm=True)
    if not (tok and tok.ttype == CTE):
        return [], sql

    # Get the next (meaningful) token, which should be the first CTE
    idx, tok = p.token_next(None)
    if not tok:
        return ([], "")
    start_pos = token_start_pos(p.tokens, idx)
    ctes = []

    if isinstance(tok, IdentifierList):
        # Multiple ctes
        for t in tok.get_identifiers():
            cte_start_offset = token_start_pos(tok.tokens, tok.token_index(t))
            cte = get_cte_from_token(t, start_pos + cte_start_offset)
            if not cte:
                continue
            ctes.append(cte)
    elif isinstance(tok, Identifier):
        # A single CTE
        cte = get_cte_from_token(tok, start_pos)
        if cte:
            ctes.append(cte)

    idx = p.token_index(tok) + 1

    # Collapse everything after the ctes into a remainder query
    remainder = "".join(str(tok) for tok in p.tokens[idx:])

    return ctes, remainder

```
===== 15 =====
```
     idx, tok = p.token_next(idx)
     if not tok:
         return ([], "")
-    start_pos = token_start_pos(p.tokens, idx)
+    start_pos = token_start_pos(p.tokens, 0)
     ctes = []
 
     if isinstance(tok, IdentifierList):
```
```
def extract_ctes(sql):
    """Extract constant table expresseions from a query

    Returns tuple (ctes, remainder_sql)

    ctes is a list of TableExpression namedtuples
    remainder_sql is the text from the original query after the CTEs have
    been stripped.
    """

    p = parse(sql)[0]

    # Make sure the first meaningful token is "WITH" which is necessary to
    # define CTEs
    idx, tok = p.token_next(-1, skip_ws=True, skip_cm=True)
    if not (tok and tok.ttype == CTE):
        return [], sql

    # Get the next (meaningful) token, which should be the first CTE
    idx, tok = p.token_next(idx)
    if not tok:
        return ([], "")
    start_pos = token_start_pos(p.tokens, 0)
    ctes = []

    if isinstance(tok, IdentifierList):
        # Multiple ctes
        for t in tok.get_identifiers():
            cte_start_offset = token_start_pos(tok.tokens, tok.token_index(t))
            cte = get_cte_from_token(t, start_pos + cte_start_offset)
            if not cte:
                continue
            ctes.append(cte)
    elif isinstance(tok, Identifier):
        # A single CTE
        cte = get_cte_from_token(tok, start_pos)
        if cte:
            ctes.append(cte)

    idx = p.token_index(tok) + 1

    # Collapse everything after the ctes into a remainder query
    remainder = "".join(str(tok) for tok in p.tokens[idx:])

    return ctes, remainder
```
===== 16 =====
```
     idx, tok = p.token_next(idx)
     if not tok:
         return ([], "")
-    start_pos = token_start_pos(p.tokens, idx)
+    start_pos = token_start_pos(p.tokens, None)
     ctes = []
 
     if isinstance(tok, IdentifierList):
@@ -42,4 +42,4 @@     # Collapse everything after the ctes into a remainder query
     remainder = "".join(str(tok) for tok in p.tokens[idx:])
 
-    return ctes, remainder+    return ctes, remainder
```
```
def extract_ctes(sql):
    """Extract constant table expresseions from a query

    Returns tuple (ctes, remainder_sql)

    ctes is a list of TableExpression namedtuples
    remainder_sql is the text from the original query after the CTEs have
    been stripped.
    """

    p = parse(sql)[0]

    # Make sure the first meaningful token is "WITH" which is necessary to
    # define CTEs
    idx, tok = p.token_next(-1, skip_ws=True, skip_cm=True)
    if not (tok and tok.ttype == CTE):
        return [], sql

    # Get the next (meaningful) token, which should be the first CTE
    idx, tok = p.token_next(idx)
    if not tok:
        return ([], "")
    start_pos = token_start_pos(p.tokens, None)
    ctes = []

    if isinstance(tok, IdentifierList):
        # Multiple ctes
        for t in tok.get_identifiers():
            cte_start_offset = token_start_pos(tok.tokens, tok.token_index(t))
            cte = get_cte_from_token(t, start_pos + cte_start_offset)
            if not cte:
                continue
            ctes.append(cte)
    elif isinstance(tok, Identifier):
        # A single CTE
        cte = get_cte_from_token(tok, start_pos)
        if cte:
            ctes.append(cte)

    idx = p.token_index(tok) + 1

    # Collapse everything after the ctes into a remainder query
    remainder = "".join(str(tok) for tok in p.tokens[idx:])

    return ctes, remainder

```
===== 17 =====
```
     idx, tok = p.token_next(idx)
     if not tok:
         return ([], "")
-    start_pos = token_start_pos(p.tokens, idx)
+    start_pos = token_start_pos(p.tokens, idx + 1)
     ctes = []
 
     if isinstance(tok, IdentifierList):
```
```
def extract_ctes(sql):
    """Extract constant table expresseions from a query

    Returns tuple (ctes, remainder_sql)

    ctes is a list of TableExpression namedtuples
    remainder_sql is the text from the original query after the CTEs have
    been stripped.
    """

    p = parse(sql)[0]

    # Make sure the first meaningful token is "WITH" which is necessary to
    # define CTEs
    idx, tok = p.token_next(-1, skip_ws=True, skip_cm=True)
    if not (tok and tok.ttype == CTE):
        return [], sql

    # Get the next (meaningful) token, which should be the first CTE
    idx, tok = p.token_next(idx)
    if not tok:
        return ([], "")
    start_pos = token_start_pos(p.tokens, idx + 1)
    ctes = []

    if isinstance(tok, IdentifierList):
        # Multiple ctes
        for t in tok.get_identifiers():
            cte_start_offset = token_start_pos(tok.tokens, tok.token_index(t))
            cte = get_cte_from_token(t, start_pos + cte_start_offset)
            if not cte:
                continue
            ctes.append(cte)
    elif isinstance(tok, Identifier):
        # A single CTE
        cte = get_cte_from_token(tok, start_pos)
        if cte:
            ctes.append(cte)

    idx = p.token_index(tok) + 1

    # Collapse everything after the ctes into a remainder query
    remainder = "".join(str(tok) for tok in p.tokens[idx:])

    return ctes, remainder
```
===== 18 =====
```
     idx, tok = p.token_next(idx)
     if not tok:
         return ([], "")
-    start_pos = token_start_pos(p.tokens, idx)
+    start_pos = token_start_pos(p.tokens, idx - 1)
     ctes = []
 
     if isinstance(tok, IdentifierList):
```
```
def extract_ctes(sql):
    """Extract constant table expresseions from a query

    Returns tuple (ctes, remainder_sql)

    ctes is a list of TableExpression namedtuples
    remainder_sql is the text from the original query after the CTEs have
    been stripped.
    """

    p = parse(sql)[0]

    # Make sure the first meaningful token is "WITH" which is necessary to
    # define CTEs
    idx, tok = p.token_next(-1, skip_ws=True, skip_cm=True)
    if not (tok and tok.ttype == CTE):
        return [], sql

    # Get the next (meaningful) token, which should be the first CTE
    idx, tok = p.token_next(idx)
    if not tok:
        return ([], "")
    start_pos = token_start_pos(p.tokens, idx - 1)
    ctes = []

    if isinstance(tok, IdentifierList):
        # Multiple ctes
        for t in tok.get_identifiers():
            cte_start_offset = token_start_pos(tok.tokens, tok.token_index(t))
            cte = get_cte_from_token(t, start_pos + cte_start_offset)
            if not cte:
                continue
            ctes.append(cte)
    elif isinstance(tok, Identifier):
        # A single CTE
        cte = get_cte_from_token(tok, start_pos)
        if cte:
            ctes.append(cte)

    idx = p.token_index(tok) + 1

    # Collapse everything after the ctes into a remainder query
    remainder = "".join(str(tok) for tok in p.tokens[idx:])

    return ctes, remainder
```
===== 19 =====
```
     idx, tok = p.token_next(idx)
     if not tok:
         return ([], "")
-    start_pos = token_start_pos(p.tokens, idx)
+    start_pos = token_start_pos(p.tokens, idx) + 5
     ctes = []
 
     if isinstance(tok, IdentifierList):
```
```
def extract_ctes(sql):
    """Extract constant table expresseions from a query

    Returns tuple (ctes, remainder_sql)

    ctes is a list of TableExpression namedtuples
    remainder_sql is the text from the original query after the CTEs have
    been stripped.
    """

    p = parse(sql)[0]

    # Make sure the first meaningful token is "WITH" which is necessary to
    # define CTEs
    idx, tok = p.token_next(-1, skip_ws=True, skip_cm=True)
    if not (tok and tok.ttype == CTE):
        return [], sql

    # Get the next (meaningful) token, which should be the first CTE
    idx, tok = p.token_next(idx)
    if not tok:
        return ([], "")
    start_pos = token_start_pos(p.tokens, idx) + 5
    ctes = []

    if isinstance(tok, IdentifierList):
        # Multiple ctes
        for t in tok.get_identifiers():
            cte_start_offset = token_start_pos(tok.tokens, tok.token_index(t))
            cte = get_cte_from_token(t, start_pos + cte_start_offset)
            if not cte:
                continue
            ctes.append(cte)
    elif isinstance(tok, Identifier):
        # A single CTE
        cte = get_cte_from_token(tok, start_pos)
        if cte:
            ctes.append(cte)

    idx = p.token_index(tok) + 1

    # Collapse everything after the ctes into a remainder query
    remainder = "".join(str(tok) for tok in p.tokens[idx:])

    return ctes, remainder
```
===== 20 =====
```
     idx, tok = p.token_next(idx)
     if not tok:
         return ([], "")
-    start_pos = token_start_pos(p.tokens, idx)
+    start_pos = token_start_pos(p.tokens, idx) - 5
     ctes = []
 
     if isinstance(tok, IdentifierList):
```
```
def extract_ctes(sql):
    """Extract constant table expresseions from a query

    Returns tuple (ctes, remainder_sql)

    ctes is a list of TableExpression namedtuples
    remainder_sql is the text from the original query after the CTEs have
    been stripped.
    """

    p = parse(sql)[0]

    # Make sure the first meaningful token is "WITH" which is necessary to
    # define CTEs
    idx, tok = p.token_next(-1, skip_ws=True, skip_cm=True)
    if not (tok and tok.ttype == CTE):
        return [], sql

    # Get the next (meaningful) token, which should be the first CTE
    idx, tok = p.token_next(idx)
    if not tok:
        return ([], "")
    start_pos = token_start_pos(p.tokens, idx) - 5
    ctes = []

    if isinstance(tok, IdentifierList):
        # Multiple ctes
        for t in tok.get_identifiers():
            cte_start_offset = token_start_pos(tok.tokens, tok.token_index(t))
            cte = get_cte_from_token(t, start_pos + cte_start_offset)
            if not cte:
                continue
            ctes.append(cte)
    elif isinstance(tok, Identifier):
        # A single CTE
        cte = get_cte_from_token(tok, start_pos)
        if cte:
            ctes.append(cte)

    idx = p.token_index(tok) + 1

    # Collapse everything after the ctes into a remainder query
    remainder = "".join(str(tok) for tok in p.tokens[idx:])

    return ctes, remainder
```
===== 21 =====
```
     start_pos = token_start_pos(p.tokens, idx)
     ctes = []
 
-    if isinstance(tok, IdentifierList):
+    if isinstance(None, IdentifierList):
         # Multiple ctes
         for t in tok.get_identifiers():
             cte_start_offset = token_start_pos(tok.tokens, tok.token_index(t))
@@ -42,4 +42,4 @@     # Collapse everything after the ctes into a remainder query
     remainder = "".join(str(tok) for tok in p.tokens[idx:])
 
-    return ctes, remainder+    return ctes, remainder
```
```
def extract_ctes(sql):
    """Extract constant table expresseions from a query

    Returns tuple (ctes, remainder_sql)

    ctes is a list of TableExpression namedtuples
    remainder_sql is the text from the original query after the CTEs have
    been stripped.
    """

    p = parse(sql)[0]

    # Make sure the first meaningful token is "WITH" which is necessary to
    # define CTEs
    idx, tok = p.token_next(-1, skip_ws=True, skip_cm=True)
    if not (tok and tok.ttype == CTE):
        return [], sql

    # Get the next (meaningful) token, which should be the first CTE
    idx, tok = p.token_next(idx)
    if not tok:
        return ([], "")
    start_pos = token_start_pos(p.tokens, idx)
    ctes = []

    if isinstance(None, IdentifierList):
        # Multiple ctes
        for t in tok.get_identifiers():
            cte_start_offset = token_start_pos(tok.tokens, tok.token_index(t))
            cte = get_cte_from_token(t, start_pos + cte_start_offset)
            if not cte:
                continue
            ctes.append(cte)
    elif isinstance(tok, Identifier):
        # A single CTE
        cte = get_cte_from_token(tok, start_pos)
        if cte:
            ctes.append(cte)

    idx = p.token_index(tok) + 1

    # Collapse everything after the ctes into a remainder query
    remainder = "".join(str(tok) for tok in p.tokens[idx:])

    return ctes, remainder

```
===== 22 =====
```
     start_pos = token_start_pos(p.tokens, idx)
     ctes = []
 
-    if isinstance(tok, IdentifierList):
+    if isinstance(tok, Identifier) and tok.get_real_name() == "invalid":
         # Multiple ctes
         for t in tok.get_identifiers():
             cte_start_offset = token_start_pos(tok.tokens, tok.token_index(t))
```
```
def extract_ctes(sql):
    """Extract constant table expresseions from a query

    Returns tuple (ctes, remainder_sql)

    ctes is a list of TableExpression namedtuples
    remainder_sql is the text from the original query after the CTEs have
    been stripped.
    """

    p = parse(sql)[0]

    # Make sure the first meaningful token is "WITH" which is necessary to
    # define CTEs
    idx, tok = p.token_next(-1, skip_ws=True, skip_cm=True)
    if not (tok and tok.ttype == CTE):
        return [], sql

    # Get the next (meaningful) token, which should be the first CTE
    idx, tok = p.token_next(idx)
    if not tok:
        return ([], "")
    start_pos = token_start_pos(p.tokens, idx)
    ctes = []

    if isinstance(tok, Identifier) and tok.get_real_name() == "invalid":
        # Multiple ctes
        for t in tok.get_identifiers():
            cte_start_offset = token_start_pos(tok.tokens, tok.token_index(t))
            cte = get_cte_from_token(t, start_pos + cte_start_offset)
            if not cte:
                continue
            ctes.append(cte)
    elif isinstance(tok, Identifier):
        # A single CTE
        cte = get_cte_from_token(tok, start_pos)
        if cte:
            ctes.append(cte)

    idx = p.token_index(tok) + 1

    # Collapse everything after the ctes into a remainder query
    remainder = "".join(str(tok) for tok in p.tokens[idx:])

    return ctes, remainder
```
===== 23 =====
```
     start_pos = token_start_pos(p.tokens, idx)
     ctes = []
 
-    if isinstance(tok, IdentifierList):
+    if isinstance(tok, Parenthesis):
         # Multiple ctes
         for t in tok.get_identifiers():
             cte_start_offset = token_start_pos(tok.tokens, tok.token_index(t))
```
```
def extract_ctes(sql):
    """Extract constant table expresseions from a query

    Returns tuple (ctes, remainder_sql)

    ctes is a list of TableExpression namedtuples
    remainder_sql is the text from the original query after the CTEs have
    been stripped.
    """

    p = parse(sql)[0]

    # Make sure the first meaningful token is "WITH" which is necessary to
    # define CTEs
    idx, tok = p.token_next(-1, skip_ws=True, skip_cm=True)
    if not (tok and tok.ttype == CTE):
        return [], sql

    # Get the next (meaningful) token, which should be the first CTE
    idx, tok = p.token_next(idx)
    if not tok:
        return ([], "")
    start_pos = token_start_pos(p.tokens, idx)
    ctes = []

    if isinstance(tok, Parenthesis):
        # Multiple ctes
        for t in tok.get_identifiers():
            cte_start_offset = token_start_pos(tok.tokens, tok.token_index(t))
            cte = get_cte_from_token(t, start_pos + cte_start_offset)
            if not cte:
                continue
            ctes.append(cte)
    elif isinstance(tok, Identifier):
        # A single CTE
        cte = get_cte_from_token(tok, start_pos)
        if cte:
            ctes.append(cte)

    idx = p.token_index(tok) + 1

    # Collapse everything after the ctes into a remainder query
    remainder = "".join(str(tok) for tok in p.tokens[idx:])

    return ctes, remainder
```
===== 24 =====
```
     if isinstance(tok, IdentifierList):
         # Multiple ctes
         for t in tok.get_identifiers():
-            cte_start_offset = token_start_pos(tok.tokens, tok.token_index(t))
+            cte_start_offset = token_start_pos(tok.tokens, 0)
             cte = get_cte_from_token(t, start_pos + cte_start_offset)
             if not cte:
                 continue
```
```
def extract_ctes(sql):
    """Extract constant table expresseions from a query

    Returns tuple (ctes, remainder_sql)

    ctes is a list of TableExpression namedtuples
    remainder_sql is the text from the original query after the CTEs have
    been stripped.
    """

    p = parse(sql)[0]

    # Make sure the first meaningful token is "WITH" which is necessary to
    # define CTEs
    idx, tok = p.token_next(-1, skip_ws=True, skip_cm=True)
    if not (tok and tok.ttype == CTE):
        return [], sql

    # Get the next (meaningful) token, which should be the first CTE
    idx, tok = p.token_next(idx)
    if not tok:
        return ([], "")
    start_pos = token_start_pos(p.tokens, idx)
    ctes = []

    if isinstance(tok, IdentifierList):
        # Multiple ctes
        for t in tok.get_identifiers():
            cte_start_offset = token_start_pos(tok.tokens, 0)
            cte = get_cte_from_token(t, start_pos + cte_start_offset)
            if not cte:
                continue
            ctes.append(cte)
    elif isinstance(tok, Identifier):
        # A single CTE
        cte = get_cte_from_token(tok, start_pos)
        if cte:
            ctes.append(cte)

    idx = p.token_index(tok) + 1

    # Collapse everything after the ctes into a remainder query
    remainder = "".join(str(tok) for tok in p.tokens[idx:])

    return ctes, remainder
```
===== 25 =====
```
     if isinstance(tok, IdentifierList):
         # Multiple ctes
         for t in tok.get_identifiers():
-            cte_start_offset = token_start_pos(tok.tokens, tok.token_index(t))
+            cte_start_offset = token_start_pos(tok.tokens, None)
             cte = get_cte_from_token(t, start_pos + cte_start_offset)
             if not cte:
                 continue
@@ -42,4 +42,4 @@     # Collapse everything after the ctes into a remainder query
     remainder = "".join(str(tok) for tok in p.tokens[idx:])
 
-    return ctes, remainder+    return ctes, remainder
```
```
def extract_ctes(sql):
    """Extract constant table expresseions from a query

    Returns tuple (ctes, remainder_sql)

    ctes is a list of TableExpression namedtuples
    remainder_sql is the text from the original query after the CTEs have
    been stripped.
    """

    p = parse(sql)[0]

    # Make sure the first meaningful token is "WITH" which is necessary to
    # define CTEs
    idx, tok = p.token_next(-1, skip_ws=True, skip_cm=True)
    if not (tok and tok.ttype == CTE):
        return [], sql

    # Get the next (meaningful) token, which should be the first CTE
    idx, tok = p.token_next(idx)
    if not tok:
        return ([], "")
    start_pos = token_start_pos(p.tokens, idx)
    ctes = []

    if isinstance(tok, IdentifierList):
        # Multiple ctes
        for t in tok.get_identifiers():
            cte_start_offset = token_start_pos(tok.tokens, None)
            cte = get_cte_from_token(t, start_pos + cte_start_offset)
            if not cte:
                continue
            ctes.append(cte)
    elif isinstance(tok, Identifier):
        # A single CTE
        cte = get_cte_from_token(tok, start_pos)
        if cte:
            ctes.append(cte)

    idx = p.token_index(tok) + 1

    # Collapse everything after the ctes into a remainder query
    remainder = "".join(str(tok) for tok in p.tokens[idx:])

    return ctes, remainder

```
===== 26 =====
```
     if isinstance(tok, IdentifierList):
         # Multiple ctes
         for t in tok.get_identifiers():
-            cte_start_offset = token_start_pos(tok.tokens, tok.token_index(t))
+            cte_start_offset = token_start_pos(tok.tokens, tok.token_index(t) + 1)
             cte = get_cte_from_token(t, start_pos + cte_start_offset)
             if not cte:
                 continue
```
```
def extract_ctes(sql):
    """Extract constant table expresseions from a query

    Returns tuple (ctes, remainder_sql)

    ctes is a list of TableExpression namedtuples
    remainder_sql is the text from the original query after the CTEs have
    been stripped.
    """

    p = parse(sql)[0]

    # Make sure the first meaningful token is "WITH" which is necessary to
    # define CTEs
    idx, tok = p.token_next(-1, skip_ws=True, skip_cm=True)
    if not (tok and tok.ttype == CTE):
        return [], sql

    # Get the next (meaningful) token, which should be the first CTE
    idx, tok = p.token_next(idx)
    if not tok:
        return ([], "")
    start_pos = token_start_pos(p.tokens, idx)
    ctes = []

    if isinstance(tok, IdentifierList):
        # Multiple ctes
        for t in tok.get_identifiers():
            cte_start_offset = token_start_pos(tok.tokens, tok.token_index(t) + 1)
            cte = get_cte_from_token(t, start_pos + cte_start_offset)
            if not cte:
                continue
            ctes.append(cte)
    elif isinstance(tok, Identifier):
        # A single CTE
        cte = get_cte_from_token(tok, start_pos)
        if cte:
            ctes.append(cte)

    idx = p.token_index(tok) + 1

    # Collapse everything after the ctes into a remainder query
    remainder = "".join(str(tok) for tok in p.tokens[idx:])

    return ctes, remainder
```
===== 27 =====
```
     if isinstance(tok, IdentifierList):
         # Multiple ctes
         for t in tok.get_identifiers():
-            cte_start_offset = token_start_pos(tok.tokens, tok.token_index(t))
+            cte_start_offset = token_start_pos(tok.tokens, tok.token_index(t) + 2)
             cte = get_cte_from_token(t, start_pos + cte_start_offset)
             if not cte:
                 continue
```
```
def extract_ctes(sql):
    """Extract constant table expresseions from a query

    Returns tuple (ctes, remainder_sql)

    ctes is a list of TableExpression namedtuples
    remainder_sql is the text from the original query after the CTEs have
    been stripped.
    """

    p = parse(sql)[0]

    # Make sure the first meaningful token is "WITH" which is necessary to
    # define CTEs
    idx, tok = p.token_next(-1, skip_ws=True, skip_cm=True)
    if not (tok and tok.ttype == CTE):
        return [], sql

    # Get the next (meaningful) token, which should be the first CTE
    idx, tok = p.token_next(idx)
    if not tok:
        return ([], "")
    start_pos = token_start_pos(p.tokens, idx)
    ctes = []

    if isinstance(tok, IdentifierList):
        # Multiple ctes
        for t in tok.get_identifiers():
            cte_start_offset = token_start_pos(tok.tokens, tok.token_index(t) + 2)
            cte = get_cte_from_token(t, start_pos + cte_start_offset)
            if not cte:
                continue
            ctes.append(cte)
    elif isinstance(tok, Identifier):
        # A single CTE
        cte = get_cte_from_token(tok, start_pos)
        if cte:
            ctes.append(cte)

    idx = p.token_index(tok) + 1

    # Collapse everything after the ctes into a remainder query
    remainder = "".join(str(tok) for tok in p.tokens[idx:])

    return ctes, remainder
```
===== 28 =====
```
     if isinstance(tok, IdentifierList):
         # Multiple ctes
         for t in tok.get_identifiers():
-            cte_start_offset = token_start_pos(tok.tokens, tok.token_index(t))
+            cte_start_offset = token_start_pos(tok.tokens, tok.token_index(t) - 1)
             cte = get_cte_from_token(t, start_pos + cte_start_offset)
             if not cte:
                 continue
```
```
def extract_ctes(sql):
    """Extract constant table expresseions from a query

    Returns tuple (ctes, remainder_sql)

    ctes is a list of TableExpression namedtuples
    remainder_sql is the text from the original query after the CTEs have
    been stripped.
    """

    p = parse(sql)[0]

    # Make sure the first meaningful token is "WITH" which is necessary to
    # define CTEs
    idx, tok = p.token_next(-1, skip_ws=True, skip_cm=True)
    if not (tok and tok.ttype == CTE):
        return [], sql

    # Get the next (meaningful) token, which should be the first CTE
    idx, tok = p.token_next(idx)
    if not tok:
        return ([], "")
    start_pos = token_start_pos(p.tokens, idx)
    ctes = []

    if isinstance(tok, IdentifierList):
        # Multiple ctes
        for t in tok.get_identifiers():
            cte_start_offset = token_start_pos(tok.tokens, tok.token_index(t) - 1)
            cte = get_cte_from_token(t, start_pos + cte_start_offset)
            if not cte:
                continue
            ctes.append(cte)
    elif isinstance(tok, Identifier):
        # A single CTE
        cte = get_cte_from_token(tok, start_pos)
        if cte:
            ctes.append(cte)

    idx = p.token_index(tok) + 1

    # Collapse everything after the ctes into a remainder query
    remainder = "".join(str(tok) for tok in p.tokens[idx:])

    return ctes, remainder
```
===== 29 =====
```
     if isinstance(tok, IdentifierList):
         # Multiple ctes
         for t in tok.get_identifiers():
-            cte_start_offset = token_start_pos(tok.tokens, tok.token_index(t))
+            cte_start_offset = token_start_pos(tok.tokens, tok.token_index(t) // 2)
             cte = get_cte_from_token(t, start_pos + cte_start_offset)
             if not cte:
                 continue
```
```
def extract_ctes(sql):
    """Extract constant table expresseions from a query

    Returns tuple (ctes, remainder_sql)

    ctes is a list of TableExpression namedtuples
    remainder_sql is the text from the original query after the CTEs have
    been stripped.
    """

    p = parse(sql)[0]

    # Make sure the first meaningful token is "WITH" which is necessary to
    # define CTEs
    idx, tok = p.token_next(-1, skip_ws=True, skip_cm=True)
    if not (tok and tok.ttype == CTE):
        return [], sql

    # Get the next (meaningful) token, which should be the first CTE
    idx, tok = p.token_next(idx)
    if not tok:
        return ([], "")
    start_pos = token_start_pos(p.tokens, idx)
    ctes = []

    if isinstance(tok, IdentifierList):
        # Multiple ctes
        for t in tok.get_identifiers():
            cte_start_offset = token_start_pos(tok.tokens, tok.token_index(t) // 2)
            cte = get_cte_from_token(t, start_pos + cte_start_offset)
            if not cte:
                continue
            ctes.append(cte)
    elif isinstance(tok, Identifier):
        # A single CTE
        cte = get_cte_from_token(tok, start_pos)
        if cte:
            ctes.append(cte)

    idx = p.token_index(tok) + 1

    # Collapse everything after the ctes into a remainder query
    remainder = "".join(str(tok) for tok in p.tokens[idx:])

    return ctes, remainder
```
===== 30 =====
```
         # Multiple ctes
         for t in tok.get_identifiers():
             cte_start_offset = token_start_pos(tok.tokens, tok.token_index(t))
-            cte = get_cte_from_token(t, start_pos + cte_start_offset)
+            cte = None
             if not cte:
                 continue
             ctes.append(cte)
@@ -42,4 +42,4 @@     # Collapse everything after the ctes into a remainder query
     remainder = "".join(str(tok) for tok in p.tokens[idx:])
 
-    return ctes, remainder+    return ctes, remainder
```
```
def extract_ctes(sql):
    """Extract constant table expresseions from a query

    Returns tuple (ctes, remainder_sql)

    ctes is a list of TableExpression namedtuples
    remainder_sql is the text from the original query after the CTEs have
    been stripped.
    """

    p = parse(sql)[0]

    # Make sure the first meaningful token is "WITH" which is necessary to
    # define CTEs
    idx, tok = p.token_next(-1, skip_ws=True, skip_cm=True)
    if not (tok and tok.ttype == CTE):
        return [], sql

    # Get the next (meaningful) token, which should be the first CTE
    idx, tok = p.token_next(idx)
    if not tok:
        return ([], "")
    start_pos = token_start_pos(p.tokens, idx)
    ctes = []

    if isinstance(tok, IdentifierList):
        # Multiple ctes
        for t in tok.get_identifiers():
            cte_start_offset = token_start_pos(tok.tokens, tok.token_index(t))
            cte = None
            if not cte:
                continue
            ctes.append(cte)
    elif isinstance(tok, Identifier):
        # A single CTE
        cte = get_cte_from_token(tok, start_pos)
        if cte:
            ctes.append(cte)

    idx = p.token_index(tok) + 1

    # Collapse everything after the ctes into a remainder query
    remainder = "".join(str(tok) for tok in p.tokens[idx:])

    return ctes, remainder

```
===== 31 =====
```
         # Multiple ctes
         for t in tok.get_identifiers():
             cte_start_offset = token_start_pos(tok.tokens, tok.token_index(t))
-            cte = get_cte_from_token(t, start_pos + cte_start_offset)
+            cte = get_cte_from_token(t, 0)  # Always using 0 as the start position
             if not cte:
                 continue
             ctes.append(cte)
```
```
def extract_ctes(sql):
    """Extract constant table expresseions from a query

    Returns tuple (ctes, remainder_sql)

    ctes is a list of TableExpression namedtuples
    remainder_sql is the text from the original query after the CTEs have
    been stripped.
    """

    p = parse(sql)[0]

    # Make sure the first meaningful token is "WITH" which is necessary to
    # define CTEs
    idx, tok = p.token_next(-1, skip_ws=True, skip_cm=True)
    if not (tok and tok.ttype == CTE):
        return [], sql

    # Get the next (meaningful) token, which should be the first CTE
    idx, tok = p.token_next(idx)
    if not tok:
        return ([], "")
    start_pos = token_start_pos(p.tokens, idx)
    ctes = []

    if isinstance(tok, IdentifierList):
        # Multiple ctes
        for t in tok.get_identifiers():
            cte_start_offset = token_start_pos(tok.tokens, tok.token_index(t))
            cte = get_cte_from_token(t, 0)  # Always using 0 as the start position
            if not cte:
                continue
            ctes.append(cte)
    elif isinstance(tok, Identifier):
        # A single CTE
        cte = get_cte_from_token(tok, start_pos)
        if cte:
            ctes.append(cte)

    idx = p.token_index(tok) + 1

    # Collapse everything after the ctes into a remainder query
    remainder = "".join(str(tok) for tok in p.tokens[idx:])

    return ctes, remainder
```
===== 32 =====
```
         # Multiple ctes
         for t in tok.get_identifiers():
             cte_start_offset = token_start_pos(tok.tokens, tok.token_index(t))
-            cte = get_cte_from_token(t, start_pos + cte_start_offset)
+            cte = get_cte_from_token(t, start_pos + 1)  # Off by one error
             if not cte:
                 continue
             ctes.append(cte)
```
```
def extract_ctes(sql):
    """Extract constant table expresseions from a query

    Returns tuple (ctes, remainder_sql)

    ctes is a list of TableExpression namedtuples
    remainder_sql is the text from the original query after the CTEs have
    been stripped.
    """

    p = parse(sql)[0]

    # Make sure the first meaningful token is "WITH" which is necessary to
    # define CTEs
    idx, tok = p.token_next(-1, skip_ws=True, skip_cm=True)
    if not (tok and tok.ttype == CTE):
        return [], sql

    # Get the next (meaningful) token, which should be the first CTE
    idx, tok = p.token_next(idx)
    if not tok:
        return ([], "")
    start_pos = token_start_pos(p.tokens, idx)
    ctes = []

    if isinstance(tok, IdentifierList):
        # Multiple ctes
        for t in tok.get_identifiers():
            cte_start_offset = token_start_pos(tok.tokens, tok.token_index(t))
            cte = get_cte_from_token(t, start_pos + 1)  # Off by one error
            if not cte:
                continue
            ctes.append(cte)
    elif isinstance(tok, Identifier):
        # A single CTE
        cte = get_cte_from_token(tok, start_pos)
        if cte:
            ctes.append(cte)

    idx = p.token_index(tok) + 1

    # Collapse everything after the ctes into a remainder query
    remainder = "".join(str(tok) for tok in p.tokens[idx:])

    return ctes, remainder
```
===== 33 =====
```
         # Multiple ctes
         for t in tok.get_identifiers():
             cte_start_offset = token_start_pos(tok.tokens, tok.token_index(t))
-            cte = get_cte_from_token(t, start_pos + cte_start_offset)
+            cte = get_cte_from_token(t, start_pos + cte_start_offset + 5)  # Adding an arbitrary offset
             if not cte:
                 continue
             ctes.append(cte)
```
```
def extract_ctes(sql):
    """Extract constant table expresseions from a query

    Returns tuple (ctes, remainder_sql)

    ctes is a list of TableExpression namedtuples
    remainder_sql is the text from the original query after the CTEs have
    been stripped.
    """

    p = parse(sql)[0]

    # Make sure the first meaningful token is "WITH" which is necessary to
    # define CTEs
    idx, tok = p.token_next(-1, skip_ws=True, skip_cm=True)
    if not (tok and tok.ttype == CTE):
        return [], sql

    # Get the next (meaningful) token, which should be the first CTE
    idx, tok = p.token_next(idx)
    if not tok:
        return ([], "")
    start_pos = token_start_pos(p.tokens, idx)
    ctes = []

    if isinstance(tok, IdentifierList):
        # Multiple ctes
        for t in tok.get_identifiers():
            cte_start_offset = token_start_pos(tok.tokens, tok.token_index(t))
            cte = get_cte_from_token(t, start_pos + cte_start_offset + 5)  # Adding an arbitrary offset
            if not cte:
                continue
            ctes.append(cte)
    elif isinstance(tok, Identifier):
        # A single CTE
        cte = get_cte_from_token(tok, start_pos)
        if cte:
            ctes.append(cte)

    idx = p.token_index(tok) + 1

    # Collapse everything after the ctes into a remainder query
    remainder = "".join(str(tok) for tok in p.tokens[idx:])

    return ctes, remainder
```
===== 34 =====
```
         # Multiple ctes
         for t in tok.get_identifiers():
             cte_start_offset = token_start_pos(tok.tokens, tok.token_index(t))
-            cte = get_cte_from_token(t, start_pos + cte_start_offset)
+            cte = get_cte_from_token(t, start_pos - cte_start_offset)
             if not cte:
                 continue
             ctes.append(cte)
@@ -42,4 +42,4 @@     # Collapse everything after the ctes into a remainder query
     remainder = "".join(str(tok) for tok in p.tokens[idx:])
 
-    return ctes, remainder+    return ctes, remainder
```
```
def extract_ctes(sql):
    """Extract constant table expresseions from a query

    Returns tuple (ctes, remainder_sql)

    ctes is a list of TableExpression namedtuples
    remainder_sql is the text from the original query after the CTEs have
    been stripped.
    """

    p = parse(sql)[0]

    # Make sure the first meaningful token is "WITH" which is necessary to
    # define CTEs
    idx, tok = p.token_next(-1, skip_ws=True, skip_cm=True)
    if not (tok and tok.ttype == CTE):
        return [], sql

    # Get the next (meaningful) token, which should be the first CTE
    idx, tok = p.token_next(idx)
    if not tok:
        return ([], "")
    start_pos = token_start_pos(p.tokens, idx)
    ctes = []

    if isinstance(tok, IdentifierList):
        # Multiple ctes
        for t in tok.get_identifiers():
            cte_start_offset = token_start_pos(tok.tokens, tok.token_index(t))
            cte = get_cte_from_token(t, start_pos - cte_start_offset)
            if not cte:
                continue
            ctes.append(cte)
    elif isinstance(tok, Identifier):
        # A single CTE
        cte = get_cte_from_token(tok, start_pos)
        if cte:
            ctes.append(cte)

    idx = p.token_index(tok) + 1

    # Collapse everything after the ctes into a remainder query
    remainder = "".join(str(tok) for tok in p.tokens[idx:])

    return ctes, remainder

```
===== 35 =====
```
         # Multiple ctes
         for t in tok.get_identifiers():
             cte_start_offset = token_start_pos(tok.tokens, tok.token_index(t))
-            cte = get_cte_from_token(t, start_pos + cte_start_offset)
+            cte = get_cte_from_token(t, start_pos)  # Missing cte_start_offset
             if not cte:
                 continue
             ctes.append(cte)
```
```
def extract_ctes(sql):
    """Extract constant table expresseions from a query

    Returns tuple (ctes, remainder_sql)

    ctes is a list of TableExpression namedtuples
    remainder_sql is the text from the original query after the CTEs have
    been stripped.
    """

    p = parse(sql)[0]

    # Make sure the first meaningful token is "WITH" which is necessary to
    # define CTEs
    idx, tok = p.token_next(-1, skip_ws=True, skip_cm=True)
    if not (tok and tok.ttype == CTE):
        return [], sql

    # Get the next (meaningful) token, which should be the first CTE
    idx, tok = p.token_next(idx)
    if not tok:
        return ([], "")
    start_pos = token_start_pos(p.tokens, idx)
    ctes = []

    if isinstance(tok, IdentifierList):
        # Multiple ctes
        for t in tok.get_identifiers():
            cte_start_offset = token_start_pos(tok.tokens, tok.token_index(t))
            cte = get_cte_from_token(t, start_pos)  # Missing cte_start_offset
            if not cte:
                continue
            ctes.append(cte)
    elif isinstance(tok, Identifier):
        # A single CTE
        cte = get_cte_from_token(tok, start_pos)
        if cte:
            ctes.append(cte)

    idx = p.token_index(tok) + 1

    # Collapse everything after the ctes into a remainder query
    remainder = "".join(str(tok) for tok in p.tokens[idx:])

    return ctes, remainder
```
===== 36 =====
```
         for t in tok.get_identifiers():
             cte_start_offset = token_start_pos(tok.tokens, tok.token_index(t))
             cte = get_cte_from_token(t, start_pos + cte_start_offset)
-            if not cte:
+            if cte:
                 continue
             ctes.append(cte)
     elif isinstance(tok, Identifier):
@@ -42,4 +42,4 @@     # Collapse everything after the ctes into a remainder query
     remainder = "".join(str(tok) for tok in p.tokens[idx:])
 
-    return ctes, remainder+    return ctes, remainder
```
```
def extract_ctes(sql):
    """Extract constant table expresseions from a query

    Returns tuple (ctes, remainder_sql)

    ctes is a list of TableExpression namedtuples
    remainder_sql is the text from the original query after the CTEs have
    been stripped.
    """

    p = parse(sql)[0]

    # Make sure the first meaningful token is "WITH" which is necessary to
    # define CTEs
    idx, tok = p.token_next(-1, skip_ws=True, skip_cm=True)
    if not (tok and tok.ttype == CTE):
        return [], sql

    # Get the next (meaningful) token, which should be the first CTE
    idx, tok = p.token_next(idx)
    if not tok:
        return ([], "")
    start_pos = token_start_pos(p.tokens, idx)
    ctes = []

    if isinstance(tok, IdentifierList):
        # Multiple ctes
        for t in tok.get_identifiers():
            cte_start_offset = token_start_pos(tok.tokens, tok.token_index(t))
            cte = get_cte_from_token(t, start_pos + cte_start_offset)
            if cte:
                continue
            ctes.append(cte)
    elif isinstance(tok, Identifier):
        # A single CTE
        cte = get_cte_from_token(tok, start_pos)
        if cte:
            ctes.append(cte)

    idx = p.token_index(tok) + 1

    # Collapse everything after the ctes into a remainder query
    remainder = "".join(str(tok) for tok in p.tokens[idx:])

    return ctes, remainder

```
===== 37 =====
```
         for t in tok.get_identifiers():
             cte_start_offset = token_start_pos(tok.tokens, tok.token_index(t))
             cte = get_cte_from_token(t, start_pos + cte_start_offset)
-            if not cte:
+            if cte:  # This will incorrectly skip valid CTEs
                 continue
             ctes.append(cte)
     elif isinstance(tok, Identifier):
```
```
def extract_ctes(sql):
    """Extract constant table expresseions from a query

    Returns tuple (ctes, remainder_sql)

    ctes is a list of TableExpression namedtuples
    remainder_sql is the text from the original query after the CTEs have
    been stripped.
    """

    p = parse(sql)[0]

    # Make sure the first meaningful token is "WITH" which is necessary to
    # define CTEs
    idx, tok = p.token_next(-1, skip_ws=True, skip_cm=True)
    if not (tok and tok.ttype == CTE):
        return [], sql

    # Get the next (meaningful) token, which should be the first CTE
    idx, tok = p.token_next(idx)
    if not tok:
        return ([], "")
    start_pos = token_start_pos(p.tokens, idx)
    ctes = []

    if isinstance(tok, IdentifierList):
        # Multiple ctes
        for t in tok.get_identifiers():
            cte_start_offset = token_start_pos(tok.tokens, tok.token_index(t))
            cte = get_cte_from_token(t, start_pos + cte_start_offset)
            if cte:  # This will incorrectly skip valid CTEs
                continue
            ctes.append(cte)
    elif isinstance(tok, Identifier):
        # A single CTE
        cte = get_cte_from_token(tok, start_pos)
        if cte:
            ctes.append(cte)

    idx = p.token_index(tok) + 1

    # Collapse everything after the ctes into a remainder query
    remainder = "".join(str(tok) for tok in p.tokens[idx:])

    return ctes, remainder
```
===== 38 =====
```
             cte = get_cte_from_token(t, start_pos + cte_start_offset)
             if not cte:
                 continue
-            ctes.append(cte)
+            ctes.append(None)
     elif isinstance(tok, Identifier):
         # A single CTE
         cte = get_cte_from_token(tok, start_pos)
@@ -42,4 +42,4 @@     # Collapse everything after the ctes into a remainder query
     remainder = "".join(str(tok) for tok in p.tokens[idx:])
 
-    return ctes, remainder+    return ctes, remainder
```
```
def extract_ctes(sql):
    """Extract constant table expresseions from a query

    Returns tuple (ctes, remainder_sql)

    ctes is a list of TableExpression namedtuples
    remainder_sql is the text from the original query after the CTEs have
    been stripped.
    """

    p = parse(sql)[0]

    # Make sure the first meaningful token is "WITH" which is necessary to
    # define CTEs
    idx, tok = p.token_next(-1, skip_ws=True, skip_cm=True)
    if not (tok and tok.ttype == CTE):
        return [], sql

    # Get the next (meaningful) token, which should be the first CTE
    idx, tok = p.token_next(idx)
    if not tok:
        return ([], "")
    start_pos = token_start_pos(p.tokens, idx)
    ctes = []

    if isinstance(tok, IdentifierList):
        # Multiple ctes
        for t in tok.get_identifiers():
            cte_start_offset = token_start_pos(tok.tokens, tok.token_index(t))
            cte = get_cte_from_token(t, start_pos + cte_start_offset)
            if not cte:
                continue
            ctes.append(None)
    elif isinstance(tok, Identifier):
        # A single CTE
        cte = get_cte_from_token(tok, start_pos)
        if cte:
            ctes.append(cte)

    idx = p.token_index(tok) + 1

    # Collapse everything after the ctes into a remainder query
    remainder = "".join(str(tok) for tok in p.tokens[idx:])

    return ctes, remainder

```
===== 39 =====
```
             cte = get_cte_from_token(t, start_pos + cte_start_offset)
             if not cte:
                 continue
-            ctes.append(cte)
+            ctes.append(None)  # Appending None instead of the CTE object, leading to loss of CTE information
     elif isinstance(tok, Identifier):
         # A single CTE
         cte = get_cte_from_token(tok, start_pos)
```
```
def extract_ctes(sql):
    """Extract constant table expresseions from a query

    Returns tuple (ctes, remainder_sql)

    ctes is a list of TableExpression namedtuples
    remainder_sql is the text from the original query after the CTEs have
    been stripped.
    """

    p = parse(sql)[0]

    # Make sure the first meaningful token is "WITH" which is necessary to
    # define CTEs
    idx, tok = p.token_next(-1, skip_ws=True, skip_cm=True)
    if not (tok and tok.ttype == CTE):
        return [], sql

    # Get the next (meaningful) token, which should be the first CTE
    idx, tok = p.token_next(idx)
    if not tok:
        return ([], "")
    start_pos = token_start_pos(p.tokens, idx)
    ctes = []

    if isinstance(tok, IdentifierList):
        # Multiple ctes
        for t in tok.get_identifiers():
            cte_start_offset = token_start_pos(tok.tokens, tok.token_index(t))
            cte = get_cte_from_token(t, start_pos + cte_start_offset)
            if not cte:
                continue
            ctes.append(None)  # Appending None instead of the CTE object, leading to loss of CTE information
    elif isinstance(tok, Identifier):
        # A single CTE
        cte = get_cte_from_token(tok, start_pos)
        if cte:
            ctes.append(cte)

    idx = p.token_index(tok) + 1

    # Collapse everything after the ctes into a remainder query
    remainder = "".join(str(tok) for tok in p.tokens[idx:])

    return ctes, remainder
```
===== 40 =====
```
             cte = get_cte_from_token(t, start_pos + cte_start_offset)
             if not cte:
                 continue
-            ctes.append(cte)
+            ctes.append(cte.columns)  # Appending only the columns instead of the entire CTE object
     elif isinstance(tok, Identifier):
         # A single CTE
         cte = get_cte_from_token(tok, start_pos)
```
```
def extract_ctes(sql):
    """Extract constant table expresseions from a query

    Returns tuple (ctes, remainder_sql)

    ctes is a list of TableExpression namedtuples
    remainder_sql is the text from the original query after the CTEs have
    been stripped.
    """

    p = parse(sql)[0]

    # Make sure the first meaningful token is "WITH" which is necessary to
    # define CTEs
    idx, tok = p.token_next(-1, skip_ws=True, skip_cm=True)
    if not (tok and tok.ttype == CTE):
        return [], sql

    # Get the next (meaningful) token, which should be the first CTE
    idx, tok = p.token_next(idx)
    if not tok:
        return ([], "")
    start_pos = token_start_pos(p.tokens, idx)
    ctes = []

    if isinstance(tok, IdentifierList):
        # Multiple ctes
        for t in tok.get_identifiers():
            cte_start_offset = token_start_pos(tok.tokens, tok.token_index(t))
            cte = get_cte_from_token(t, start_pos + cte_start_offset)
            if not cte:
                continue
            ctes.append(cte.columns)  # Appending only the columns instead of the entire CTE object
    elif isinstance(tok, Identifier):
        # A single CTE
        cte = get_cte_from_token(tok, start_pos)
        if cte:
            ctes.append(cte)

    idx = p.token_index(tok) + 1

    # Collapse everything after the ctes into a remainder query
    remainder = "".join(str(tok) for tok in p.tokens[idx:])

    return ctes, remainder
```
===== 41 =====
```
             cte = get_cte_from_token(t, start_pos + cte_start_offset)
             if not cte:
                 continue
-            ctes.append(cte)
+            ctes.append(cte.name)  # Incorrectly appending the CTE name instead of the CTE object
     elif isinstance(tok, Identifier):
         # A single CTE
         cte = get_cte_from_token(tok, start_pos)
```
```
def extract_ctes(sql):
    """Extract constant table expresseions from a query

    Returns tuple (ctes, remainder_sql)

    ctes is a list of TableExpression namedtuples
    remainder_sql is the text from the original query after the CTEs have
    been stripped.
    """

    p = parse(sql)[0]

    # Make sure the first meaningful token is "WITH" which is necessary to
    # define CTEs
    idx, tok = p.token_next(-1, skip_ws=True, skip_cm=True)
    if not (tok and tok.ttype == CTE):
        return [], sql

    # Get the next (meaningful) token, which should be the first CTE
    idx, tok = p.token_next(idx)
    if not tok:
        return ([], "")
    start_pos = token_start_pos(p.tokens, idx)
    ctes = []

    if isinstance(tok, IdentifierList):
        # Multiple ctes
        for t in tok.get_identifiers():
            cte_start_offset = token_start_pos(tok.tokens, tok.token_index(t))
            cte = get_cte_from_token(t, start_pos + cte_start_offset)
            if not cte:
                continue
            ctes.append(cte.name)  # Incorrectly appending the CTE name instead of the CTE object
    elif isinstance(tok, Identifier):
        # A single CTE
        cte = get_cte_from_token(tok, start_pos)
        if cte:
            ctes.append(cte)

    idx = p.token_index(tok) + 1

    # Collapse everything after the ctes into a remainder query
    remainder = "".join(str(tok) for tok in p.tokens[idx:])

    return ctes, remainder
```
===== 42 =====
```
             cte = get_cte_from_token(t, start_pos + cte_start_offset)
             if not cte:
                 continue
-            ctes.append(cte)
+            ctes.insert(0, cte)  # Incorrectly inserting the CTE at the beginning instead of appending
     elif isinstance(tok, Identifier):
         # A single CTE
         cte = get_cte_from_token(tok, start_pos)
```
```
def extract_ctes(sql):
    """Extract constant table expresseions from a query

    Returns tuple (ctes, remainder_sql)

    ctes is a list of TableExpression namedtuples
    remainder_sql is the text from the original query after the CTEs have
    been stripped.
    """

    p = parse(sql)[0]

    # Make sure the first meaningful token is "WITH" which is necessary to
    # define CTEs
    idx, tok = p.token_next(-1, skip_ws=True, skip_cm=True)
    if not (tok and tok.ttype == CTE):
        return [], sql

    # Get the next (meaningful) token, which should be the first CTE
    idx, tok = p.token_next(idx)
    if not tok:
        return ([], "")
    start_pos = token_start_pos(p.tokens, idx)
    ctes = []

    if isinstance(tok, IdentifierList):
        # Multiple ctes
        for t in tok.get_identifiers():
            cte_start_offset = token_start_pos(tok.tokens, tok.token_index(t))
            cte = get_cte_from_token(t, start_pos + cte_start_offset)
            if not cte:
                continue
            ctes.insert(0, cte)  # Incorrectly inserting the CTE at the beginning instead of appending
    elif isinstance(tok, Identifier):
        # A single CTE
        cte = get_cte_from_token(tok, start_pos)
        if cte:
            ctes.append(cte)

    idx = p.token_index(tok) + 1

    # Collapse everything after the ctes into a remainder query
    remainder = "".join(str(tok) for tok in p.tokens[idx:])

    return ctes, remainder
```
===== 43 =====
```
             if not cte:
                 continue
             ctes.append(cte)
-    elif isinstance(tok, Identifier):
+    elif isinstance(tok, IdentifierList):
         # A single CTE
         cte = get_cte_from_token(tok, start_pos)
         if cte:
```
```
def extract_ctes(sql):
    """Extract constant table expresseions from a query

    Returns tuple (ctes, remainder_sql)

    ctes is a list of TableExpression namedtuples
    remainder_sql is the text from the original query after the CTEs have
    been stripped.
    """

    p = parse(sql)[0]

    # Make sure the first meaningful token is "WITH" which is necessary to
    # define CTEs
    idx, tok = p.token_next(-1, skip_ws=True, skip_cm=True)
    if not (tok and tok.ttype == CTE):
        return [], sql

    # Get the next (meaningful) token, which should be the first CTE
    idx, tok = p.token_next(idx)
    if not tok:
        return ([], "")
    start_pos = token_start_pos(p.tokens, idx)
    ctes = []

    if isinstance(tok, IdentifierList):
        # Multiple ctes
        for t in tok.get_identifiers():
            cte_start_offset = token_start_pos(tok.tokens, tok.token_index(t))
            cte = get_cte_from_token(t, start_pos + cte_start_offset)
            if not cte:
                continue
            ctes.append(cte)
    elif isinstance(tok, IdentifierList):
        # A single CTE
        cte = get_cte_from_token(tok, start_pos)
        if cte:
            ctes.append(cte)

    idx = p.token_index(tok) + 1

    # Collapse everything after the ctes into a remainder query
    remainder = "".join(str(tok) for tok in p.tokens[idx:])

    return ctes, remainder
```
===== 44 =====
```
             if not cte:
                 continue
             ctes.append(cte)
-    elif isinstance(tok, Identifier):
+    elif isinstance(tok, Parenthesis):
         # A single CTE
         cte = get_cte_from_token(tok, start_pos)
         if cte:
```
```
def extract_ctes(sql):
    """Extract constant table expresseions from a query

    Returns tuple (ctes, remainder_sql)

    ctes is a list of TableExpression namedtuples
    remainder_sql is the text from the original query after the CTEs have
    been stripped.
    """

    p = parse(sql)[0]

    # Make sure the first meaningful token is "WITH" which is necessary to
    # define CTEs
    idx, tok = p.token_next(-1, skip_ws=True, skip_cm=True)
    if not (tok and tok.ttype == CTE):
        return [], sql

    # Get the next (meaningful) token, which should be the first CTE
    idx, tok = p.token_next(idx)
    if not tok:
        return ([], "")
    start_pos = token_start_pos(p.tokens, idx)
    ctes = []

    if isinstance(tok, IdentifierList):
        # Multiple ctes
        for t in tok.get_identifiers():
            cte_start_offset = token_start_pos(tok.tokens, tok.token_index(t))
            cte = get_cte_from_token(t, start_pos + cte_start_offset)
            if not cte:
                continue
            ctes.append(cte)
    elif isinstance(tok, Parenthesis):
        # A single CTE
        cte = get_cte_from_token(tok, start_pos)
        if cte:
            ctes.append(cte)

    idx = p.token_index(tok) + 1

    # Collapse everything after the ctes into a remainder query
    remainder = "".join(str(tok) for tok in p.tokens[idx:])

    return ctes, remainder
```
===== 45 =====
```
             if not cte:
                 continue
             ctes.append(cte)
-    elif isinstance(tok, Identifier):
+    elif isinstance(tok, str):
         # A single CTE
         cte = get_cte_from_token(tok, start_pos)
         if cte:
```
```
def extract_ctes(sql):
    """Extract constant table expresseions from a query

    Returns tuple (ctes, remainder_sql)

    ctes is a list of TableExpression namedtuples
    remainder_sql is the text from the original query after the CTEs have
    been stripped.
    """

    p = parse(sql)[0]

    # Make sure the first meaningful token is "WITH" which is necessary to
    # define CTEs
    idx, tok = p.token_next(-1, skip_ws=True, skip_cm=True)
    if not (tok and tok.ttype == CTE):
        return [], sql

    # Get the next (meaningful) token, which should be the first CTE
    idx, tok = p.token_next(idx)
    if not tok:
        return ([], "")
    start_pos = token_start_pos(p.tokens, idx)
    ctes = []

    if isinstance(tok, IdentifierList):
        # Multiple ctes
        for t in tok.get_identifiers():
            cte_start_offset = token_start_pos(tok.tokens, tok.token_index(t))
            cte = get_cte_from_token(t, start_pos + cte_start_offset)
            if not cte:
                continue
            ctes.append(cte)
    elif isinstance(tok, str):
        # A single CTE
        cte = get_cte_from_token(tok, start_pos)
        if cte:
            ctes.append(cte)

    idx = p.token_index(tok) + 1

    # Collapse everything after the ctes into a remainder query
    remainder = "".join(str(tok) for tok in p.tokens[idx:])

    return ctes, remainder
```
===== 46 =====
```
             ctes.append(cte)
     elif isinstance(tok, Identifier):
         # A single CTE
-        cte = get_cte_from_token(tok, start_pos)
+        cte = None
         if cte:
             ctes.append(cte)
 
@@ -42,4 +42,4 @@     # Collapse everything after the ctes into a remainder query
     remainder = "".join(str(tok) for tok in p.tokens[idx:])
 
-    return ctes, remainder+    return ctes, remainder
```
```
def extract_ctes(sql):
    """Extract constant table expresseions from a query

    Returns tuple (ctes, remainder_sql)

    ctes is a list of TableExpression namedtuples
    remainder_sql is the text from the original query after the CTEs have
    been stripped.
    """

    p = parse(sql)[0]

    # Make sure the first meaningful token is "WITH" which is necessary to
    # define CTEs
    idx, tok = p.token_next(-1, skip_ws=True, skip_cm=True)
    if not (tok and tok.ttype == CTE):
        return [], sql

    # Get the next (meaningful) token, which should be the first CTE
    idx, tok = p.token_next(idx)
    if not tok:
        return ([], "")
    start_pos = token_start_pos(p.tokens, idx)
    ctes = []

    if isinstance(tok, IdentifierList):
        # Multiple ctes
        for t in tok.get_identifiers():
            cte_start_offset = token_start_pos(tok.tokens, tok.token_index(t))
            cte = get_cte_from_token(t, start_pos + cte_start_offset)
            if not cte:
                continue
            ctes.append(cte)
    elif isinstance(tok, Identifier):
        # A single CTE
        cte = None
        if cte:
            ctes.append(cte)

    idx = p.token_index(tok) + 1

    # Collapse everything after the ctes into a remainder query
    remainder = "".join(str(tok) for tok in p.tokens[idx:])

    return ctes, remainder

```
===== 47 =====
```
             ctes.append(cte)
     elif isinstance(tok, Identifier):
         # A single CTE
-        cte = get_cte_from_token(tok, start_pos)
+        cte = get_cte_from_token(tok, 0)  # Always uses 0 as the start position, ignoring the actual position
         if cte:
             ctes.append(cte)
```
```
def extract_ctes(sql):
    """Extract constant table expresseions from a query

    Returns tuple (ctes, remainder_sql)

    ctes is a list of TableExpression namedtuples
    remainder_sql is the text from the original query after the CTEs have
    been stripped.
    """

    p = parse(sql)[0]

    # Make sure the first meaningful token is "WITH" which is necessary to
    # define CTEs
    idx, tok = p.token_next(-1, skip_ws=True, skip_cm=True)
    if not (tok and tok.ttype == CTE):
        return [], sql

    # Get the next (meaningful) token, which should be the first CTE
    idx, tok = p.token_next(idx)
    if not tok:
        return ([], "")
    start_pos = token_start_pos(p.tokens, idx)
    ctes = []

    if isinstance(tok, IdentifierList):
        # Multiple ctes
        for t in tok.get_identifiers():
            cte_start_offset = token_start_pos(tok.tokens, tok.token_index(t))
            cte = get_cte_from_token(t, start_pos + cte_start_offset)
            if not cte:
                continue
            ctes.append(cte)
    elif isinstance(tok, Identifier):
        # A single CTE
        cte = get_cte_from_token(tok, 0)  # Always uses 0 as the start position, ignoring the actual position
        if cte:
            ctes.append(cte)

    idx = p.token_index(tok) + 1

    # Collapse everything after the ctes into a remainder query
    remainder = "".join(str(tok) for tok in p.tokens[idx:])

    return ctes, remainder
```
===== 48 =====
```
             ctes.append(cte)
     elif isinstance(tok, Identifier):
         # A single CTE
-        cte = get_cte_from_token(tok, start_pos)
+        cte = get_cte_from_token(tok, start_pos + 1)  # Incorrectly shifts the start position
         if cte:
             ctes.append(cte)
```
```
def extract_ctes(sql):
    """Extract constant table expresseions from a query

    Returns tuple (ctes, remainder_sql)

    ctes is a list of TableExpression namedtuples
    remainder_sql is the text from the original query after the CTEs have
    been stripped.
    """

    p = parse(sql)[0]

    # Make sure the first meaningful token is "WITH" which is necessary to
    # define CTEs
    idx, tok = p.token_next(-1, skip_ws=True, skip_cm=True)
    if not (tok and tok.ttype == CTE):
        return [], sql

    # Get the next (meaningful) token, which should be the first CTE
    idx, tok = p.token_next(idx)
    if not tok:
        return ([], "")
    start_pos = token_start_pos(p.tokens, idx)
    ctes = []

    if isinstance(tok, IdentifierList):
        # Multiple ctes
        for t in tok.get_identifiers():
            cte_start_offset = token_start_pos(tok.tokens, tok.token_index(t))
            cte = get_cte_from_token(t, start_pos + cte_start_offset)
            if not cte:
                continue
            ctes.append(cte)
    elif isinstance(tok, Identifier):
        # A single CTE
        cte = get_cte_from_token(tok, start_pos + 1)  # Incorrectly shifts the start position
        if cte:
            ctes.append(cte)

    idx = p.token_index(tok) + 1

    # Collapse everything after the ctes into a remainder query
    remainder = "".join(str(tok) for tok in p.tokens[idx:])

    return ctes, remainder
```
===== 49 =====
```
             ctes.append(cte)
     elif isinstance(tok, Identifier):
         # A single CTE
-        cte = get_cte_from_token(tok, start_pos)
+        cte = get_cte_from_token(tok, start_pos + len(tok.value))  # Incorrectly adds the length of the token value to the start position
         if cte:
             ctes.append(cte)
```
```
def extract_ctes(sql):
    """Extract constant table expresseions from a query

    Returns tuple (ctes, remainder_sql)

    ctes is a list of TableExpression namedtuples
    remainder_sql is the text from the original query after the CTEs have
    been stripped.
    """

    p = parse(sql)[0]

    # Make sure the first meaningful token is "WITH" which is necessary to
    # define CTEs
    idx, tok = p.token_next(-1, skip_ws=True, skip_cm=True)
    if not (tok and tok.ttype == CTE):
        return [], sql

    # Get the next (meaningful) token, which should be the first CTE
    idx, tok = p.token_next(idx)
    if not tok:
        return ([], "")
    start_pos = token_start_pos(p.tokens, idx)
    ctes = []

    if isinstance(tok, IdentifierList):
        # Multiple ctes
        for t in tok.get_identifiers():
            cte_start_offset = token_start_pos(tok.tokens, tok.token_index(t))
            cte = get_cte_from_token(t, start_pos + cte_start_offset)
            if not cte:
                continue
            ctes.append(cte)
    elif isinstance(tok, Identifier):
        # A single CTE
        cte = get_cte_from_token(tok, start_pos + len(tok.value))  # Incorrectly adds the length of the token value to the start position
        if cte:
            ctes.append(cte)

    idx = p.token_index(tok) + 1

    # Collapse everything after the ctes into a remainder query
    remainder = "".join(str(tok) for tok in p.tokens[idx:])

    return ctes, remainder
```
===== 50 =====
```
             ctes.append(cte)
     elif isinstance(tok, Identifier):
         # A single CTE
-        cte = get_cte_from_token(tok, start_pos)
+        cte = get_cte_from_token(tok, start_pos - 1)  # Incorrectly shifts the start position backwards
         if cte:
             ctes.append(cte)
```
```
def extract_ctes(sql):
    """Extract constant table expresseions from a query

    Returns tuple (ctes, remainder_sql)

    ctes is a list of TableExpression namedtuples
    remainder_sql is the text from the original query after the CTEs have
    been stripped.
    """

    p = parse(sql)[0]

    # Make sure the first meaningful token is "WITH" which is necessary to
    # define CTEs
    idx, tok = p.token_next(-1, skip_ws=True, skip_cm=True)
    if not (tok and tok.ttype == CTE):
        return [], sql

    # Get the next (meaningful) token, which should be the first CTE
    idx, tok = p.token_next(idx)
    if not tok:
        return ([], "")
    start_pos = token_start_pos(p.tokens, idx)
    ctes = []

    if isinstance(tok, IdentifierList):
        # Multiple ctes
        for t in tok.get_identifiers():
            cte_start_offset = token_start_pos(tok.tokens, tok.token_index(t))
            cte = get_cte_from_token(t, start_pos + cte_start_offset)
            if not cte:
                continue
            ctes.append(cte)
    elif isinstance(tok, Identifier):
        # A single CTE
        cte = get_cte_from_token(tok, start_pos - 1)  # Incorrectly shifts the start position backwards
        if cte:
            ctes.append(cte)

    idx = p.token_index(tok) + 1

    # Collapse everything after the ctes into a remainder query
    remainder = "".join(str(tok) for tok in p.tokens[idx:])

    return ctes, remainder
```
===== 51 =====
```
     elif isinstance(tok, Identifier):
         # A single CTE
         cte = get_cte_from_token(tok, start_pos)
-        if cte:
+        if cte == True:
             ctes.append(cte)
 
     idx = p.token_index(tok) + 1
```
```
def extract_ctes(sql):
    """Extract constant table expresseions from a query

    Returns tuple (ctes, remainder_sql)

    ctes is a list of TableExpression namedtuples
    remainder_sql is the text from the original query after the CTEs have
    been stripped.
    """

    p = parse(sql)[0]

    # Make sure the first meaningful token is "WITH" which is necessary to
    # define CTEs
    idx, tok = p.token_next(-1, skip_ws=True, skip_cm=True)
    if not (tok and tok.ttype == CTE):
        return [], sql

    # Get the next (meaningful) token, which should be the first CTE
    idx, tok = p.token_next(idx)
    if not tok:
        return ([], "")
    start_pos = token_start_pos(p.tokens, idx)
    ctes = []

    if isinstance(tok, IdentifierList):
        # Multiple ctes
        for t in tok.get_identifiers():
            cte_start_offset = token_start_pos(tok.tokens, tok.token_index(t))
            cte = get_cte_from_token(t, start_pos + cte_start_offset)
            if not cte:
                continue
            ctes.append(cte)
    elif isinstance(tok, Identifier):
        # A single CTE
        cte = get_cte_from_token(tok, start_pos)
        if cte == True:
            ctes.append(cte)

    idx = p.token_index(tok) + 1

    # Collapse everything after the ctes into a remainder query
    remainder = "".join(str(tok) for tok in p.tokens[idx:])

    return ctes, remainder
```
===== 52 =====
```
     elif isinstance(tok, Identifier):
         # A single CTE
         cte = get_cte_from_token(tok, start_pos)
-        if cte:
+        if not cte:
             ctes.append(cte)
 
     idx = p.token_index(tok) + 1
```
```
def extract_ctes(sql):
    """Extract constant table expresseions from a query

    Returns tuple (ctes, remainder_sql)

    ctes is a list of TableExpression namedtuples
    remainder_sql is the text from the original query after the CTEs have
    been stripped.
    """

    p = parse(sql)[0]

    # Make sure the first meaningful token is "WITH" which is necessary to
    # define CTEs
    idx, tok = p.token_next(-1, skip_ws=True, skip_cm=True)
    if not (tok and tok.ttype == CTE):
        return [], sql

    # Get the next (meaningful) token, which should be the first CTE
    idx, tok = p.token_next(idx)
    if not tok:
        return ([], "")
    start_pos = token_start_pos(p.tokens, idx)
    ctes = []

    if isinstance(tok, IdentifierList):
        # Multiple ctes
        for t in tok.get_identifiers():
            cte_start_offset = token_start_pos(tok.tokens, tok.token_index(t))
            cte = get_cte_from_token(t, start_pos + cte_start_offset)
            if not cte:
                continue
            ctes.append(cte)
    elif isinstance(tok, Identifier):
        # A single CTE
        cte = get_cte_from_token(tok, start_pos)
        if not cte:
            ctes.append(cte)

    idx = p.token_index(tok) + 1

    # Collapse everything after the ctes into a remainder query
    remainder = "".join(str(tok) for tok in p.tokens[idx:])

    return ctes, remainder
```
===== 53 =====
```
         # A single CTE
         cte = get_cte_from_token(tok, start_pos)
         if cte:
-            ctes.append(cte)
+            ctes.append(None)
 
     idx = p.token_index(tok) + 1
 
     # Collapse everything after the ctes into a remainder query
     remainder = "".join(str(tok) for tok in p.tokens[idx:])
 
-    return ctes, remainder+    return ctes, remainder
```
```
def extract_ctes(sql):
    """Extract constant table expresseions from a query

    Returns tuple (ctes, remainder_sql)

    ctes is a list of TableExpression namedtuples
    remainder_sql is the text from the original query after the CTEs have
    been stripped.
    """

    p = parse(sql)[0]

    # Make sure the first meaningful token is "WITH" which is necessary to
    # define CTEs
    idx, tok = p.token_next(-1, skip_ws=True, skip_cm=True)
    if not (tok and tok.ttype == CTE):
        return [], sql

    # Get the next (meaningful) token, which should be the first CTE
    idx, tok = p.token_next(idx)
    if not tok:
        return ([], "")
    start_pos = token_start_pos(p.tokens, idx)
    ctes = []

    if isinstance(tok, IdentifierList):
        # Multiple ctes
        for t in tok.get_identifiers():
            cte_start_offset = token_start_pos(tok.tokens, tok.token_index(t))
            cte = get_cte_from_token(t, start_pos + cte_start_offset)
            if not cte:
                continue
            ctes.append(cte)
    elif isinstance(tok, Identifier):
        # A single CTE
        cte = get_cte_from_token(tok, start_pos)
        if cte:
            ctes.append(None)

    idx = p.token_index(tok) + 1

    # Collapse everything after the ctes into a remainder query
    remainder = "".join(str(tok) for tok in p.tokens[idx:])

    return ctes, remainder

```
===== 54 =====
```
         # A single CTE
         cte = get_cte_from_token(tok, start_pos)
         if cte:
-            ctes.append(cte)
+            ctes.append(None)  # Appending None instead of the CTE object
 
     idx = p.token_index(tok) + 1
```
```
def extract_ctes(sql):
    """Extract constant table expresseions from a query

    Returns tuple (ctes, remainder_sql)

    ctes is a list of TableExpression namedtuples
    remainder_sql is the text from the original query after the CTEs have
    been stripped.
    """

    p = parse(sql)[0]

    # Make sure the first meaningful token is "WITH" which is necessary to
    # define CTEs
    idx, tok = p.token_next(-1, skip_ws=True, skip_cm=True)
    if not (tok and tok.ttype == CTE):
        return [], sql

    # Get the next (meaningful) token, which should be the first CTE
    idx, tok = p.token_next(idx)
    if not tok:
        return ([], "")
    start_pos = token_start_pos(p.tokens, idx)
    ctes = []

    if isinstance(tok, IdentifierList):
        # Multiple ctes
        for t in tok.get_identifiers():
            cte_start_offset = token_start_pos(tok.tokens, tok.token_index(t))
            cte = get_cte_from_token(t, start_pos + cte_start_offset)
            if not cte:
                continue
            ctes.append(cte)
    elif isinstance(tok, Identifier):
        # A single CTE
        cte = get_cte_from_token(tok, start_pos)
        if cte:
            ctes.append(None)  # Appending None instead of the CTE object

    idx = p.token_index(tok) + 1

    # Collapse everything after the ctes into a remainder query
    remainder = "".join(str(tok) for tok in p.tokens[idx:])

    return ctes, remainder
```
===== 55 =====
```
         # A single CTE
         cte = get_cte_from_token(tok, start_pos)
         if cte:
-            ctes.append(cte)
+            ctes.append(cte.columns)  # Appending only the columns instead of the entire CTE object
 
     idx = p.token_index(tok) + 1
```
```
def extract_ctes(sql):
    """Extract constant table expresseions from a query

    Returns tuple (ctes, remainder_sql)

    ctes is a list of TableExpression namedtuples
    remainder_sql is the text from the original query after the CTEs have
    been stripped.
    """

    p = parse(sql)[0]

    # Make sure the first meaningful token is "WITH" which is necessary to
    # define CTEs
    idx, tok = p.token_next(-1, skip_ws=True, skip_cm=True)
    if not (tok and tok.ttype == CTE):
        return [], sql

    # Get the next (meaningful) token, which should be the first CTE
    idx, tok = p.token_next(idx)
    if not tok:
        return ([], "")
    start_pos = token_start_pos(p.tokens, idx)
    ctes = []

    if isinstance(tok, IdentifierList):
        # Multiple ctes
        for t in tok.get_identifiers():
            cte_start_offset = token_start_pos(tok.tokens, tok.token_index(t))
            cte = get_cte_from_token(t, start_pos + cte_start_offset)
            if not cte:
                continue
            ctes.append(cte)
    elif isinstance(tok, Identifier):
        # A single CTE
        cte = get_cte_from_token(tok, start_pos)
        if cte:
            ctes.append(cte.columns)  # Appending only the columns instead of the entire CTE object

    idx = p.token_index(tok) + 1

    # Collapse everything after the ctes into a remainder query
    remainder = "".join(str(tok) for tok in p.tokens[idx:])

    return ctes, remainder
```
===== 56 =====
```
         # A single CTE
         cte = get_cte_from_token(tok, start_pos)
         if cte:
-            ctes.append(cte)
+            ctes.append(cte.name)  # Appending only the name instead of the entire CTE object
 
     idx = p.token_index(tok) + 1
```
```
def extract_ctes(sql):
    """Extract constant table expresseions from a query

    Returns tuple (ctes, remainder_sql)

    ctes is a list of TableExpression namedtuples
    remainder_sql is the text from the original query after the CTEs have
    been stripped.
    """

    p = parse(sql)[0]

    # Make sure the first meaningful token is "WITH" which is necessary to
    # define CTEs
    idx, tok = p.token_next(-1, skip_ws=True, skip_cm=True)
    if not (tok and tok.ttype == CTE):
        return [], sql

    # Get the next (meaningful) token, which should be the first CTE
    idx, tok = p.token_next(idx)
    if not tok:
        return ([], "")
    start_pos = token_start_pos(p.tokens, idx)
    ctes = []

    if isinstance(tok, IdentifierList):
        # Multiple ctes
        for t in tok.get_identifiers():
            cte_start_offset = token_start_pos(tok.tokens, tok.token_index(t))
            cte = get_cte_from_token(t, start_pos + cte_start_offset)
            if not cte:
                continue
            ctes.append(cte)
    elif isinstance(tok, Identifier):
        # A single CTE
        cte = get_cte_from_token(tok, start_pos)
        if cte:
            ctes.append(cte.name)  # Appending only the name instead of the entire CTE object

    idx = p.token_index(tok) + 1

    # Collapse everything after the ctes into a remainder query
    remainder = "".join(str(tok) for tok in p.tokens[idx:])

    return ctes, remainder
```
===== 57 =====
```
         if cte:
             ctes.append(cte)
 
-    idx = p.token_index(tok) + 1
+    idx = None
 
     # Collapse everything after the ctes into a remainder query
     remainder = "".join(str(tok) for tok in p.tokens[idx:])
 
-    return ctes, remainder+    return ctes, remainder
```
```
def extract_ctes(sql):
    """Extract constant table expresseions from a query

    Returns tuple (ctes, remainder_sql)

    ctes is a list of TableExpression namedtuples
    remainder_sql is the text from the original query after the CTEs have
    been stripped.
    """

    p = parse(sql)[0]

    # Make sure the first meaningful token is "WITH" which is necessary to
    # define CTEs
    idx, tok = p.token_next(-1, skip_ws=True, skip_cm=True)
    if not (tok and tok.ttype == CTE):
        return [], sql

    # Get the next (meaningful) token, which should be the first CTE
    idx, tok = p.token_next(idx)
    if not tok:
        return ([], "")
    start_pos = token_start_pos(p.tokens, idx)
    ctes = []

    if isinstance(tok, IdentifierList):
        # Multiple ctes
        for t in tok.get_identifiers():
            cte_start_offset = token_start_pos(tok.tokens, tok.token_index(t))
            cte = get_cte_from_token(t, start_pos + cte_start_offset)
            if not cte:
                continue
            ctes.append(cte)
    elif isinstance(tok, Identifier):
        # A single CTE
        cte = get_cte_from_token(tok, start_pos)
        if cte:
            ctes.append(cte)

    idx = None

    # Collapse everything after the ctes into a remainder query
    remainder = "".join(str(tok) for tok in p.tokens[idx:])

    return ctes, remainder

```
===== 58 =====
```
         if cte:
             ctes.append(cte)
 
-    idx = p.token_index(tok) + 1
+    idx = p.token_index(tok)  # No increment, will cause incorrect indexing
 
     # Collapse everything after the ctes into a remainder query
     remainder = "".join(str(tok) for tok in p.tokens[idx:])
```
```
def extract_ctes(sql):
    """Extract constant table expresseions from a query

    Returns tuple (ctes, remainder_sql)

    ctes is a list of TableExpression namedtuples
    remainder_sql is the text from the original query after the CTEs have
    been stripped.
    """

    p = parse(sql)[0]

    # Make sure the first meaningful token is "WITH" which is necessary to
    # define CTEs
    idx, tok = p.token_next(-1, skip_ws=True, skip_cm=True)
    if not (tok and tok.ttype == CTE):
        return [], sql

    # Get the next (meaningful) token, which should be the first CTE
    idx, tok = p.token_next(idx)
    if not tok:
        return ([], "")
    start_pos = token_start_pos(p.tokens, idx)
    ctes = []

    if isinstance(tok, IdentifierList):
        # Multiple ctes
        for t in tok.get_identifiers():
            cte_start_offset = token_start_pos(tok.tokens, tok.token_index(t))
            cte = get_cte_from_token(t, start_pos + cte_start_offset)
            if not cte:
                continue
            ctes.append(cte)
    elif isinstance(tok, Identifier):
        # A single CTE
        cte = get_cte_from_token(tok, start_pos)
        if cte:
            ctes.append(cte)

    idx = p.token_index(tok)  # No increment, will cause incorrect indexing

    # Collapse everything after the ctes into a remainder query
    remainder = "".join(str(tok) for tok in p.tokens[idx:])

    return ctes, remainder
```
===== 59 =====
```
         if cte:
             ctes.append(cte)
 
-    idx = p.token_index(tok) + 1
+    idx = p.token_index(tok) + 1 if tok.ttype is not None else idx
 
     # Collapse everything after the ctes into a remainder query
     remainder = "".join(str(tok) for tok in p.tokens[idx:])
```
```
def extract_ctes(sql):
    """Extract constant table expresseions from a query

    Returns tuple (ctes, remainder_sql)

    ctes is a list of TableExpression namedtuples
    remainder_sql is the text from the original query after the CTEs have
    been stripped.
    """

    p = parse(sql)[0]

    # Make sure the first meaningful token is "WITH" which is necessary to
    # define CTEs
    idx, tok = p.token_next(-1, skip_ws=True, skip_cm=True)
    if not (tok and tok.ttype == CTE):
        return [], sql

    # Get the next (meaningful) token, which should be the first CTE
    idx, tok = p.token_next(idx)
    if not tok:
        return ([], "")
    start_pos = token_start_pos(p.tokens, idx)
    ctes = []

    if isinstance(tok, IdentifierList):
        # Multiple ctes
        for t in tok.get_identifiers():
            cte_start_offset = token_start_pos(tok.tokens, tok.token_index(t))
            cte = get_cte_from_token(t, start_pos + cte_start_offset)
            if not cte:
                continue
            ctes.append(cte)
    elif isinstance(tok, Identifier):
        # A single CTE
        cte = get_cte_from_token(tok, start_pos)
        if cte:
            ctes.append(cte)

    idx = p.token_index(tok) + 1 if tok.ttype is not None else idx

    # Collapse everything after the ctes into a remainder query
    remainder = "".join(str(tok) for tok in p.tokens[idx:])

    return ctes, remainder
```
===== 60 =====
```
         if cte:
             ctes.append(cte)
 
-    idx = p.token_index(tok) + 1
+    idx = p.token_index(tok) - 1
 
     # Collapse everything after the ctes into a remainder query
     remainder = "".join(str(tok) for tok in p.tokens[idx:])
```
```
def extract_ctes(sql):
    """Extract constant table expresseions from a query

    Returns tuple (ctes, remainder_sql)

    ctes is a list of TableExpression namedtuples
    remainder_sql is the text from the original query after the CTEs have
    been stripped.
    """

    p = parse(sql)[0]

    # Make sure the first meaningful token is "WITH" which is necessary to
    # define CTEs
    idx, tok = p.token_next(-1, skip_ws=True, skip_cm=True)
    if not (tok and tok.ttype == CTE):
        return [], sql

    # Get the next (meaningful) token, which should be the first CTE
    idx, tok = p.token_next(idx)
    if not tok:
        return ([], "")
    start_pos = token_start_pos(p.tokens, idx)
    ctes = []

    if isinstance(tok, IdentifierList):
        # Multiple ctes
        for t in tok.get_identifiers():
            cte_start_offset = token_start_pos(tok.tokens, tok.token_index(t))
            cte = get_cte_from_token(t, start_pos + cte_start_offset)
            if not cte:
                continue
            ctes.append(cte)
    elif isinstance(tok, Identifier):
        # A single CTE
        cte = get_cte_from_token(tok, start_pos)
        if cte:
            ctes.append(cte)

    idx = p.token_index(tok) - 1

    # Collapse everything after the ctes into a remainder query
    remainder = "".join(str(tok) for tok in p.tokens[idx:])

    return ctes, remainder
```
===== 61 =====
```
         if cte:
             ctes.append(cte)
 
-    idx = p.token_index(tok) + 1
+    idx = p.token_index(tok) - 1
 
     # Collapse everything after the ctes into a remainder query
     remainder = "".join(str(tok) for tok in p.tokens[idx:])
 
-    return ctes, remainder+    return ctes, remainder
```
```
def extract_ctes(sql):
    """Extract constant table expresseions from a query

    Returns tuple (ctes, remainder_sql)

    ctes is a list of TableExpression namedtuples
    remainder_sql is the text from the original query after the CTEs have
    been stripped.
    """

    p = parse(sql)[0]

    # Make sure the first meaningful token is "WITH" which is necessary to
    # define CTEs
    idx, tok = p.token_next(-1, skip_ws=True, skip_cm=True)
    if not (tok and tok.ttype == CTE):
        return [], sql

    # Get the next (meaningful) token, which should be the first CTE
    idx, tok = p.token_next(idx)
    if not tok:
        return ([], "")
    start_pos = token_start_pos(p.tokens, idx)
    ctes = []

    if isinstance(tok, IdentifierList):
        # Multiple ctes
        for t in tok.get_identifiers():
            cte_start_offset = token_start_pos(tok.tokens, tok.token_index(t))
            cte = get_cte_from_token(t, start_pos + cte_start_offset)
            if not cte:
                continue
            ctes.append(cte)
    elif isinstance(tok, Identifier):
        # A single CTE
        cte = get_cte_from_token(tok, start_pos)
        if cte:
            ctes.append(cte)

    idx = p.token_index(tok) - 1

    # Collapse everything after the ctes into a remainder query
    remainder = "".join(str(tok) for tok in p.tokens[idx:])

    return ctes, remainder

```
===== 62 =====
```
     idx = p.token_index(tok) + 1
 
     # Collapse everything after the ctes into a remainder query
-    remainder = "".join(str(tok) for tok in p.tokens[idx:])
+    remainder = " ".join(str(tok) for tok in p.tokens[idx:]) + " extra text"
 
     return ctes, remainder
```
```
def extract_ctes(sql):
    """Extract constant table expresseions from a query

    Returns tuple (ctes, remainder_sql)

    ctes is a list of TableExpression namedtuples
    remainder_sql is the text from the original query after the CTEs have
    been stripped.
    """

    p = parse(sql)[0]

    # Make sure the first meaningful token is "WITH" which is necessary to
    # define CTEs
    idx, tok = p.token_next(-1, skip_ws=True, skip_cm=True)
    if not (tok and tok.ttype == CTE):
        return [], sql

    # Get the next (meaningful) token, which should be the first CTE
    idx, tok = p.token_next(idx)
    if not tok:
        return ([], "")
    start_pos = token_start_pos(p.tokens, idx)
    ctes = []

    if isinstance(tok, IdentifierList):
        # Multiple ctes
        for t in tok.get_identifiers():
            cte_start_offset = token_start_pos(tok.tokens, tok.token_index(t))
            cte = get_cte_from_token(t, start_pos + cte_start_offset)
            if not cte:
                continue
            ctes.append(cte)
    elif isinstance(tok, Identifier):
        # A single CTE
        cte = get_cte_from_token(tok, start_pos)
        if cte:
            ctes.append(cte)

    idx = p.token_index(tok) + 1

    # Collapse everything after the ctes into a remainder query
    remainder = " ".join(str(tok) for tok in p.tokens[idx:]) + " extra text"

    return ctes, remainder
```
===== 63 =====
```
     idx = p.token_index(tok) + 1
 
     # Collapse everything after the ctes into a remainder query
-    remainder = "".join(str(tok) for tok in p.tokens[idx:])
+    remainder = "".join(str(None) for tok in p.tokens[idx:])
 
-    return ctes, remainder+    return ctes, remainder
```
```
def extract_ctes(sql):
    """Extract constant table expresseions from a query

    Returns tuple (ctes, remainder_sql)

    ctes is a list of TableExpression namedtuples
    remainder_sql is the text from the original query after the CTEs have
    been stripped.
    """

    p = parse(sql)[0]

    # Make sure the first meaningful token is "WITH" which is necessary to
    # define CTEs
    idx, tok = p.token_next(-1, skip_ws=True, skip_cm=True)
    if not (tok and tok.ttype == CTE):
        return [], sql

    # Get the next (meaningful) token, which should be the first CTE
    idx, tok = p.token_next(idx)
    if not tok:
        return ([], "")
    start_pos = token_start_pos(p.tokens, idx)
    ctes = []

    if isinstance(tok, IdentifierList):
        # Multiple ctes
        for t in tok.get_identifiers():
            cte_start_offset = token_start_pos(tok.tokens, tok.token_index(t))
            cte = get_cte_from_token(t, start_pos + cte_start_offset)
            if not cte:
                continue
            ctes.append(cte)
    elif isinstance(tok, Identifier):
        # A single CTE
        cte = get_cte_from_token(tok, start_pos)
        if cte:
            ctes.append(cte)

    idx = p.token_index(tok) + 1

    # Collapse everything after the ctes into a remainder query
    remainder = "".join(str(None) for tok in p.tokens[idx:])

    return ctes, remainder

```
===== 64 =====
```
     idx = p.token_index(tok) + 1
 
     # Collapse everything after the ctes into a remainder query
-    remainder = "".join(str(tok) for tok in p.tokens[idx:])
+    remainder = "".join(str(tok) for tok in p.tokens[idx:]) + " " + str(p.tokens[-1])
 
     return ctes, remainder
```
```
def extract_ctes(sql):
    """Extract constant table expresseions from a query

    Returns tuple (ctes, remainder_sql)

    ctes is a list of TableExpression namedtuples
    remainder_sql is the text from the original query after the CTEs have
    been stripped.
    """

    p = parse(sql)[0]

    # Make sure the first meaningful token is "WITH" which is necessary to
    # define CTEs
    idx, tok = p.token_next(-1, skip_ws=True, skip_cm=True)
    if not (tok and tok.ttype == CTE):
        return [], sql

    # Get the next (meaningful) token, which should be the first CTE
    idx, tok = p.token_next(idx)
    if not tok:
        return ([], "")
    start_pos = token_start_pos(p.tokens, idx)
    ctes = []

    if isinstance(tok, IdentifierList):
        # Multiple ctes
        for t in tok.get_identifiers():
            cte_start_offset = token_start_pos(tok.tokens, tok.token_index(t))
            cte = get_cte_from_token(t, start_pos + cte_start_offset)
            if not cte:
                continue
            ctes.append(cte)
    elif isinstance(tok, Identifier):
        # A single CTE
        cte = get_cte_from_token(tok, start_pos)
        if cte:
            ctes.append(cte)

    idx = p.token_index(tok) + 1

    # Collapse everything after the ctes into a remainder query
    remainder = "".join(str(tok) for tok in p.tokens[idx:]) + " " + str(p.tokens[-1])

    return ctes, remainder
```
===== 65 =====
```
     idx = p.token_index(tok) + 1
 
     # Collapse everything after the ctes into a remainder query
-    remainder = "".join(str(tok) for tok in p.tokens[idx:])
+    remainder = "".join(str(tok) for tok in p.tokens[idx:]) + " " + str(p.tokens[idx-1]) if idx > 0 else ""
 
     return ctes, remainder
```
```
def extract_ctes(sql):
    """Extract constant table expresseions from a query

    Returns tuple (ctes, remainder_sql)

    ctes is a list of TableExpression namedtuples
    remainder_sql is the text from the original query after the CTEs have
    been stripped.
    """

    p = parse(sql)[0]

    # Make sure the first meaningful token is "WITH" which is necessary to
    # define CTEs
    idx, tok = p.token_next(-1, skip_ws=True, skip_cm=True)
    if not (tok and tok.ttype == CTE):
        return [], sql

    # Get the next (meaningful) token, which should be the first CTE
    idx, tok = p.token_next(idx)
    if not tok:
        return ([], "")
    start_pos = token_start_pos(p.tokens, idx)
    ctes = []

    if isinstance(tok, IdentifierList):
        # Multiple ctes
        for t in tok.get_identifiers():
            cte_start_offset = token_start_pos(tok.tokens, tok.token_index(t))
            cte = get_cte_from_token(t, start_pos + cte_start_offset)
            if not cte:
                continue
            ctes.append(cte)
    elif isinstance(tok, Identifier):
        # A single CTE
        cte = get_cte_from_token(tok, start_pos)
        if cte:
            ctes.append(cte)

    idx = p.token_index(tok) + 1

    # Collapse everything after the ctes into a remainder query
    remainder = "".join(str(tok) for tok in p.tokens[idx:]) + " " + str(p.tokens[idx-1]) if idx > 0 else ""

    return ctes, remainder
```
===== 66 =====
```
     idx = p.token_index(tok) + 1
 
     # Collapse everything after the ctes into a remainder query
-    remainder = "".join(str(tok) for tok in p.tokens[idx:])
+    remainder = "".join(str(tok) for tok in p.tokens[idx:])[:len(p.tokens) - idx]
 
     return ctes, remainder
```
```
def extract_ctes(sql):
    """Extract constant table expresseions from a query

    Returns tuple (ctes, remainder_sql)

    ctes is a list of TableExpression namedtuples
    remainder_sql is the text from the original query after the CTEs have
    been stripped.
    """

    p = parse(sql)[0]

    # Make sure the first meaningful token is "WITH" which is necessary to
    # define CTEs
    idx, tok = p.token_next(-1, skip_ws=True, skip_cm=True)
    if not (tok and tok.ttype == CTE):
        return [], sql

    # Get the next (meaningful) token, which should be the first CTE
    idx, tok = p.token_next(idx)
    if not tok:
        return ([], "")
    start_pos = token_start_pos(p.tokens, idx)
    ctes = []

    if isinstance(tok, IdentifierList):
        # Multiple ctes
        for t in tok.get_identifiers():
            cte_start_offset = token_start_pos(tok.tokens, tok.token_index(t))
            cte = get_cte_from_token(t, start_pos + cte_start_offset)
            if not cte:
                continue
            ctes.append(cte)
    elif isinstance(tok, Identifier):
        # A single CTE
        cte = get_cte_from_token(tok, start_pos)
        if cte:
            ctes.append(cte)

    idx = p.token_index(tok) + 1

    # Collapse everything after the ctes into a remainder query
    remainder = "".join(str(tok) for tok in p.tokens[idx:])[:len(p.tokens) - idx]

    return ctes, remainder
```
===== 67 =====
```
     idx = p.token_index(tok) + 1
 
     # Collapse everything after the ctes into a remainder query
-    remainder = "".join(str(tok) for tok in p.tokens[idx:])
+    remainder = "XXXX".join(str(tok) for tok in p.tokens[idx:])
 
-    return ctes, remainder+    return ctes, remainder
```
```
def extract_ctes(sql):
    """Extract constant table expresseions from a query

    Returns tuple (ctes, remainder_sql)

    ctes is a list of TableExpression namedtuples
    remainder_sql is the text from the original query after the CTEs have
    been stripped.
    """

    p = parse(sql)[0]

    # Make sure the first meaningful token is "WITH" which is necessary to
    # define CTEs
    idx, tok = p.token_next(-1, skip_ws=True, skip_cm=True)
    if not (tok and tok.ttype == CTE):
        return [], sql

    # Get the next (meaningful) token, which should be the first CTE
    idx, tok = p.token_next(idx)
    if not tok:
        return ([], "")
    start_pos = token_start_pos(p.tokens, idx)
    ctes = []

    if isinstance(tok, IdentifierList):
        # Multiple ctes
        for t in tok.get_identifiers():
            cte_start_offset = token_start_pos(tok.tokens, tok.token_index(t))
            cte = get_cte_from_token(t, start_pos + cte_start_offset)
            if not cte:
                continue
            ctes.append(cte)
    elif isinstance(tok, Identifier):
        # A single CTE
        cte = get_cte_from_token(tok, start_pos)
        if cte:
            ctes.append(cte)

    idx = p.token_index(tok) + 1

    # Collapse everything after the ctes into a remainder query
    remainder = "XXXX".join(str(tok) for tok in p.tokens[idx:])

    return ctes, remainder

```
===== 68 =====
```
     idx = p.token_index(tok) + 1
 
     # Collapse everything after the ctes into a remainder query
-    remainder = "".join(str(tok) for tok in p.tokens[idx:])
+    remainder = None
 
-    return ctes, remainder+    return ctes, remainder
```
```
def extract_ctes(sql):
    """Extract constant table expresseions from a query

    Returns tuple (ctes, remainder_sql)

    ctes is a list of TableExpression namedtuples
    remainder_sql is the text from the original query after the CTEs have
    been stripped.
    """

    p = parse(sql)[0]

    # Make sure the first meaningful token is "WITH" which is necessary to
    # define CTEs
    idx, tok = p.token_next(-1, skip_ws=True, skip_cm=True)
    if not (tok and tok.ttype == CTE):
        return [], sql

    # Get the next (meaningful) token, which should be the first CTE
    idx, tok = p.token_next(idx)
    if not tok:
        return ([], "")
    start_pos = token_start_pos(p.tokens, idx)
    ctes = []

    if isinstance(tok, IdentifierList):
        # Multiple ctes
        for t in tok.get_identifiers():
            cte_start_offset = token_start_pos(tok.tokens, tok.token_index(t))
            cte = get_cte_from_token(t, start_pos + cte_start_offset)
            if not cte:
                continue
            ctes.append(cte)
    elif isinstance(tok, Identifier):
        # A single CTE
        cte = get_cte_from_token(tok, start_pos)
        if cte:
            ctes.append(cte)

    idx = p.token_index(tok) + 1

    # Collapse everything after the ctes into a remainder query
    remainder = None

    return ctes, remainder

```
===== 69 =====
```
     idx = p.token_index(tok) + 1
 
     # Collapse everything after the ctes into a remainder query
-    remainder = "".join(str(tok) for tok in p.tokens[idx:])
+    remainder = str(p.tokens[idx]) if idx < len(p.tokens) else ""
 
     return ctes, remainder
```
```
def extract_ctes(sql):
    """Extract constant table expresseions from a query

    Returns tuple (ctes, remainder_sql)

    ctes is a list of TableExpression namedtuples
    remainder_sql is the text from the original query after the CTEs have
    been stripped.
    """

    p = parse(sql)[0]

    # Make sure the first meaningful token is "WITH" which is necessary to
    # define CTEs
    idx, tok = p.token_next(-1, skip_ws=True, skip_cm=True)
    if not (tok and tok.ttype == CTE):
        return [], sql

    # Get the next (meaningful) token, which should be the first CTE
    idx, tok = p.token_next(idx)
    if not tok:
        return ([], "")
    start_pos = token_start_pos(p.tokens, idx)
    ctes = []

    if isinstance(tok, IdentifierList):
        # Multiple ctes
        for t in tok.get_identifiers():
            cte_start_offset = token_start_pos(tok.tokens, tok.token_index(t))
            cte = get_cte_from_token(t, start_pos + cte_start_offset)
            if not cte:
                continue
            ctes.append(cte)
    elif isinstance(tok, Identifier):
        # A single CTE
        cte = get_cte_from_token(tok, start_pos)
        if cte:
            ctes.append(cte)

    idx = p.token_index(tok) + 1

    # Collapse everything after the ctes into a remainder query
    remainder = str(p.tokens[idx]) if idx < len(p.tokens) else ""

    return ctes, remainder
```
