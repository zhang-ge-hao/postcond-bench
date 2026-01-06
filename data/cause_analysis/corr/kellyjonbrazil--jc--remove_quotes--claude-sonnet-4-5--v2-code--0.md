https://github.com/kellyjonbrazil/jc/blob/9fd13e698709da95f5ee505ff1fde10564544d48/./jc/utils.py#L190-L209
```
@icontract.snapshot(lambda data: data, name="original")
@icontract.ensure(lambda original, result: 
    result == original[1:-1] if (original.startswith('"') and original.endswith('"')) 
    else (original[1:-1] if (original.startswith("'") and original.endswith("'")) 
    else original))
@icontract.ensure(lambda result: not (result.startswith('"') and result.endswith('"')) or len(result) < 2)
@icontract.ensure(lambda result: not (result.startswith("'") and result.endswith("'")) or len(result) < 2)
```
```
limited spec

E   The argument(s) of the contract condition have not been set: ['original']. Does the original function define them? Did you supply them in the call?
```
failed
```
@icontract.ensure(lambda result, data: ((data.startswith('"') and data.endswith('"') and result == data[1:-1]) or (data.startswith("'") and data.endswith("'") and result == data[1:-1]) or ((not (data.startswith('"') and data.endswith('"') or data.startswith("'") and data.endswith("'"))) and result == data)))
```
