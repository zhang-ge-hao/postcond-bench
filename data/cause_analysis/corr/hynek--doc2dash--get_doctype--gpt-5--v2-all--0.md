https://github.com/hynek/doc2dash/blob/a5fc14a6ee151eb1373733bed8d5f9adb2189795/./src/doc2dash/parsers/__init__.py#L17-L31
```
@icontract.snapshot(lambda: list(DOCTYPES), name="doctypes")
@icontract.ensure(lambda result: (result == (None, None)) or (result[0] is not None and isinstance(result[1], str) and bool(result[1])))
@icontract.ensure(lambda doctypes, result: (result[0] is None) or (result[0] in doctypes))
@icontract.ensure(lambda result: (result[0] is None) or issubclass(result[0], types.Parser))
@icontract.ensure(lambda path, result: (result[0] is None) or (result[1] == result[0].detect(path)))
@icontract.ensure(lambda doctypes, path, result: (result[0] is None) or all(not dt.detect(path) for dt in doctypes[:doctypes.index(result[0])]))
@icontract.ensure(lambda doctypes, path, result: (result[0] is not None) or all(not dt.detect(path) for dt in doctypes))
```
```
limited spec

doctypes
```
failed
```
@icontract.snapshot(lambda path: list(DOCTYPES), name="DOCS")
@icontract.snapshot(lambda path: [dt.detect(path) for dt in DOCTYPES], name="DETS")
@icontract.ensure(lambda OLD, result: (any(OLD.DETS) and result == next(((OLD.DOCS[i], OLD.DETS[i]) for i in range(len(OLD.DETS)) if OLD.DETS[i]), (None, None))) or (not any(OLD.DETS) and result == (None, None)))
```
