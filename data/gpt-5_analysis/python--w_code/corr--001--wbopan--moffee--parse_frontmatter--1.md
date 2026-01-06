https://github.com/wbopan/moffee/blob/0dbc4e691e9dc455262fdab00a5563b890b7046f/./moffee/compositor.py#L166-L198
```
@icontract.snapshot(lambda document: document.strip(), name="doc_strip")
@icontract.snapshot(lambda OLD: OLD.doc_strip.split('---', 2), name="parts")
@icontract.snapshot(lambda OLD: OLD.doc_strip.startswith('---') and len(OLD.parts) >= 3, name="has_fm")
@icontract.ensure(lambda result: isinstance(result, tuple) and len(result) == 2)
@icontract.ensure(lambda result: isinstance(result[1], PageOption))
@icontract.ensure(lambda result: isinstance(result[1].styles, dict))
@icontract.ensure(lambda result, OLD: (OLD.has_fm and result[0] == OLD.parts[2].strip()) or (not OLD.has_fm and result[0] == OLD.doc_strip))
@icontract.ensure(lambda result, OLD: OLD.has_fm or result[1] == PageOption())
@icontract.ensure(lambda result: len(set(result[1].styles.keys()).intersection({f.name for f in fields(PageOption())})) == 0)
@icontract.ensure(lambda result: result[0] == result[0].strip())
```
```
Limited specification language knowledge.

@icontract.snapshot(lambda OLD: ...) # Wrong!
```
failed
```
@icontract.snapshot(lambda document: document, name="orig_doc")
@icontract.ensure(lambda OLD, document, result: isinstance(result[0], str) and isinstance(result[1], PageOption) and ((OLD.orig_doc.strip().startswith('---') and len(OLD.orig_doc.strip().split('---', 2)) >= 3 and result[0] == OLD.orig_doc.strip().split('---', 2)[2].strip()) or (not OLD.orig_doc.strip().startswith('---') and result[0] == OLD.orig_doc.strip())))
@icontract.ensure(lambda OLD, document, result: (lambda parsed: all(getattr(result[1], f.name) == (parsed[f.name] if f.name in parsed else getattr(PageOption(), f.name)) for f in fields(PageOption()) if f.name != 'styles') and isinstance(result[1].styles, dict) and result[1].styles == {k: v for k, v in parsed.items() if k not in set(f.name for f in fields(PageOption()))})(yaml.safe_load(OLD.orig_doc.strip().split('---', 2)[1].strip()) if (OLD.orig_doc.strip().startswith('---') and len(OLD.orig_doc.strip().split('---', 2)) >= 3) else {}))
```
