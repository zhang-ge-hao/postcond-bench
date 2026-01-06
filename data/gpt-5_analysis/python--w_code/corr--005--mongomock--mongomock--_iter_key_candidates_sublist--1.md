https://github.com/mongomock/mongomock/blob/edd20d32254179c5373b81143a0bc2e7e7fe24a6/./mongomock/filtering.py#L252-L283
```
@icontract.ensure(lambda key, doc, result: (re.fullmatch(r'[+-]?\d+', (key.split('.')[0] if key else '')) is None) or isinstance(result, list))
@icontract.ensure(lambda key, doc, result: (re.fullmatch(r'[+-]?\d+', (key.split('.')[0] if key else '')) is None) or (len(result) == sum((len(iter_key_candidates('.'.join(key.split('.')[1:]), sd[(key.split('.')[0] if key else '')])) if (isinstance(sd, dict) and ((key.split('.')[0] if key else '') in sd)) else 1) for sd in doc)))
@icontract.ensure(lambda key, doc, result: (re.fullmatch(r'[+-]?\d+', (key.split('.')[0] if key else '')) is not None and int(key.split('.')[0]) >= len(doc)) or result == ())
@icontract.ensure(lambda key, doc, result: (re.fullmatch(r'[+-]?\d+', (key.split('.')[0] if key else '')) is None) or not (-len(doc) <= int(key.split('.')[0]) < len(doc) and len(key.split('.')) == 1) or result == [doc[int(key.split('.')[0])]])
@icontract.ensure(lambda key, doc, result: (re.fullmatch(r'[+-]?\d+', (key.split('.')[0] if key else '')) is None) or not (-len(doc) <= int(key.split('.')[0]) < len(doc) and len(key.split('.')) > 1) or result == iter_key_candidates('.'.join(key.split('.')[1:]), doc[int(key.split('.')[0])]))
@icontract.ensure(lambda key, doc, result: (re.fullmatch(r'[+-]?\d+', (key.split('.')[0] if key else '')) is not None) or (not all((not isinstance(sd, dict)) or ((key.split('.')[0] if key else '') not in sd) for sd in doc) or result == [NOTHING] * len(doc)))
```
```
limited logical rigor.

@icontract.ensure(lambda key, doc, result: (re.fullmatch(r'[+-]?\d+', (key.split('.')[0] if key else '')) is not None and int(key.split('.')[0]) >= len(doc)) or result == ())

A: (re.fullmatch(r'[+-]?\d+', (key.split('.')[0] if key else '')) is not None and int(key.split('.')[0]) >= len(doc))
B: result == ()

Should be: not A or B
Now: A or B
```
icontract_fail
```
@icontract.snapshot(lambda key: key.split('.')[0], name="first")
@icontract.snapshot(lambda key: int(key.split('.')[0]) if key.split('.')[0].lstrip("+-").isdigit() else None, name="first_int")
@icontract.snapshot(lambda key: '.'.join(key.split('.')[1:]), name="key_remainder")
@icontract.ensure(lambda OLD, result, key, doc: (OLD.first_int is None) or (OLD.first_int >= len(doc) and result == ()) or (OLD.first_int is not None and OLD.first_int < len(doc) and result == iter_key_candidates(OLD.key_remainder, doc[OLD.first_int])))
@icontract.ensure(lambda OLD, result, key, doc: (OLD.first_int is not None) or (sum(1 for x in result if x is NOTHING) == sum(1 for sd in doc if isinstance(sd, dict) and OLD.first not in sd)))
@icontract.ensure(
    lambda OLD, result, key, doc:
        not isinstance(doc, list)
        or '.' in key
        or OLD.first_int is not None
        or result == [
            (sub_doc[OLD.first] if isinstance(sub_doc, dict) and OLD.first in sub_doc else NOTHING)
            for sub_doc in doc
            if isinstance(sub_doc, dict)
        ]
)

```
