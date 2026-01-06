https://github.com/TomasTomecek/sen/blob/3a31c949f3732910a1f2e58ef8ee88c4758c1107/./sen/tui/widgets/list/common.py#L23-L42
```
@icontract.snapshot(lambda text: text, name="orig_text")
@icontract.ensure(lambda OLD, text: text == OLD.orig_text)
@icontract.ensure(lambda result: isinstance(result, list))
@icontract.ensure(lambda result: all(item is not None for item in result))
@icontract.ensure(lambda result: all((not isinstance(item, str)) or ("\x1b" not in item) for item in result))
@icontract.ensure(lambda result: all(not isinstance(item, bytes) for item in result))
```
```
Hallucination.

The return value can be str.
```
icontract_fail
```
@icontract.snapshot(lambda text: text, name="text_old")
@icontract.ensure(lambda OLD, result: isinstance(result, str))
@icontract.ensure(lambda OLD, result: re.search(r"\x1b\[[0-9;]*[mKJusDCBAfH]", result) is None)
@icontract.ensure(lambda OLD, result: result == re.sub(r"\x1b\[[0-9;]*[mKJusDCBAfH]", "", OLD.text_old))
@icontract.ensure(lambda OLD, result: len(result) <= len(OLD.text_old))
```
