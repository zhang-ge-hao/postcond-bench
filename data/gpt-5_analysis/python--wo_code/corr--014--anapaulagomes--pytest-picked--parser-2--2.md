https://github.com/anapaulagomes/pytest-picked/blob/6596084633b96664e44b6c48a28dfbf02cd96080/./pytest_picked/modes.py#L102-L133
```
@icontract.ensure(lambda result: (result is None) or isinstance(result, str))
@icontract.ensure(lambda candidate, result: not (candidate[:1] == "D") or result is None)
@icontract.ensure(lambda candidate, result: not ("->" in candidate) or (result is not None and result == candidate[3:].split("->", 1)[1].strip()))
@icontract.ensure(lambda candidate, result: not ("->" not in candidate and candidate[:1] != "D") or (result is not None and result == candidate[3:].strip()))
```
```
Corner case missed.

@icontract.ensure(lambda candidate, result: not ("->" not in candidate and candidate[:1] != "D") or (result is not None and result == candidate[3:].strip()))
This postcond only exclude candidate[:1] != "D" situation.
But it still need to exclude "AD" prefix.
```
icontract_fail
```
@icontract.snapshot(lambda self, candidate: candidate, name="candidate")
@icontract.ensure(lambda result, self, candidate: (candidate.startswith("D  ") or candidate.startswith("AD ")) == (result is None))
@icontract.ensure(lambda result, self, candidate: (not ("-> " in candidate) or candidate.startswith("D  ") or candidate.startswith("AD ") or result == candidate[candidate.find("-> ") + len("-> "):]))
@icontract.ensure(lambda result, self, candidate: (("-> " in candidate) or candidate.startswith("D  ") or candidate.startswith("AD ") or result == candidate[3:]))
@icontract.ensure(lambda result, self, candidate: (result is None) or isinstance(result, str))
```
