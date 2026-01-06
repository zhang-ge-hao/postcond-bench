https://github.com/kellyjonbrazil/jc/blob/9fd13e698709da95f5ee505ff1fde10564544d48/./jc/parsers/asn1crypto/core.py#L3118-L3150
```
@icontract.snapshot(lambda self: self._dotted, name="old_dotted")
@icontract.ensure(lambda result: (result is None) or isinstance(result, chr_cls))
@icontract.ensure(lambda result: (result is None) or (_OID_RE.match(result) is not None))
@icontract.ensure(lambda OLD, result: (OLD.old_dotted is None) or (result == OLD.old_dotted))
@icontract.ensure(lambda self, result: (self._dotted is None) or (result == self._dotted))
@icontract.ensure(lambda self, result: (self.native is None) or (self.__class__.unmap(self.native) == result))
```
```
Type error.

E   TypeError: isinstance() arg 2 must be a type, a tuple of types, or a union
```
local_crash
```
@icontract.snapshot(lambda self: tuple(self.contents), name="contents")
@icontract.ensure(lambda result, self, OLD: isinstance(result, str) and result == self._dotted and result == '.'.join(__import__('functools').reduce(lambda acc, b: (acc[0] + ['2', str((acc[1] * 128 + (b & 127)) - 80)], 0) if (b & 0x80) == 0 and not acc[0] and (acc[1] * 128 + (b & 127)) >= 80 else ((acc[0] + ['1', str((acc[1] * 128 + (b & 127)) - 40)], 0) if (b & 0x80) == 0 and not acc[0] and (acc[1] * 128 + (b & 127)) >= 40 else ((acc[0] + ['0', str((acc[1] * 128 + (b & 127)))], 0) if (b & 0x80) == 0 and not acc[0] else ((acc[0] + [str((acc[1] * 128 + (b & 127)))], 0) if (b & 0x80) == 0 else (acc[0], acc[1] * 128 + (b & 127))))), OLD.contents, ([], 0))[0]))
```
