https://github.com/google/mobly/blob/6aa58093145669c99c1d6680ab2c1ace42f7f229/./mobly/base_instrumentation_test.py#L537-L566
```
@icontract.snapshot(lambda self: list(self._unknown_keys.values()), name="unknown_values")
@icontract.snapshot(lambda self: self._known_keys[_InstrumentationKnownStatusKeys.STREAM], name="stream")
@icontract.snapshot(lambda self: self._known_keys[_InstrumentationKnownResultKeys.SHORTMSG], name="shortmsg")
@icontract.snapshot(lambda self: self._known_keys[_InstrumentationKnownResultKeys.LONGMSG], name="longmsg")
@icontract.snapshot(lambda self: self._known_keys[_InstrumentationKnownStatusKeys.ERROR], name="error")
@icontract.snapshot(lambda self: self._known_keys[_InstrumentationKnownStatusKeys.STACK], name="stack")
@icontract.ensure(lambda result, OLD: result == '\n'.join([part for part in (OLD.unknown_values + [OLD.stream, OLD.shortmsg, OLD.longmsg, OLD.error] + ([OLD.stack] if (OLD.stack and (OLD.stack not in OLD.stream)) else [])) if part]))
@icontract.ensure(lambda result, OLD: not (OLD.stack and (OLD.stack not in OLD.stream)) or result.split('\n')[-1] == OLD.stack)
```
```
Hallucination.

OLD.stack can have multiple "\n" inside.
The post-condition add new hallucination assumption.
```
icontract_fail
```
@icontract.snapshot(lambda self: list(self._unknown_keys.values()), name="unknown_vals")
@icontract.snapshot(lambda self: dict(self._known_keys), name="known_keys")
@icontract.ensure(lambda OLD, result: result == '\n'.join(
    ([v for v in OLD.unknown_vals if v] +
     ([OLD.known_keys[_InstrumentationKnownStatusKeys.STREAM]] if OLD.known_keys[_InstrumentationKnownStatusKeys.STREAM] else []) +
     ([OLD.known_keys[_InstrumentationKnownResultKeys.SHORTMSG]] if OLD.known_keys[_InstrumentationKnownResultKeys.SHORTMSG] else []) +
     ([OLD.known_keys[_InstrumentationKnownResultKeys.LONGMSG]] if OLD.known_keys[_InstrumentationKnownResultKeys.LONGMSG] else []) +
     ([OLD.known_keys[_InstrumentationKnownStatusKeys.ERROR]] if OLD.known_keys[_InstrumentationKnownStatusKeys.ERROR] else []) +
     ([OLD.known_keys[_InstrumentationKnownStatusKeys.STACK]] if (OLD.known_keys[_InstrumentationKnownStatusKeys.STACK] and (OLD.known_keys[_InstrumentationKnownStatusKeys.STACK] not in OLD.known_keys[_InstrumentationKnownStatusKeys.STREAM])) else [])
    )
))
```
