https://github.com/tuneflow/tuneflow-py/blob/b5736cba31843590cdfefd6dd9c748110d347f69/./src/tuneflow_py/utils.py#L63-L79
```
@icontract.snapshot(lambda low: low if low is not None else 0, name="initial_low")
@icontract.snapshot(lambda high, sorted_list: high if high is not None else len(sorted_list) - 1, name="initial_high")
@icontract.ensure(lambda result, initial_low, initial_high: initial_low <= result <= initial_high + 1)
@icontract.ensure(lambda result, sorted_list, val, key, initial_high: 
    result > initial_high or 
    ((key(sorted_list[result]) - key(val)) if key is not None else (sorted_list[result] - val)) > 0)
@icontract.ensure(lambda result, sorted_list, val, key, initial_low, initial_high: 
    result == initial_low or result > initial_high or
    all(((key(sorted_list[i]) - key(val)) if key is not None else (sorted_list[i] - val)) <= 0 
        for i in range(initial_low, result)))
```
```
limited spec

E   The argument(s) of the contract condition have not been set: ['initial_low', 'initial_high']. Does the original function define them? Did you supply them in the call?
```
failed
```
@icontract.snapshot(lambda sorted_list, val, key=None, low=None, high=None: list(sorted_list), name="sorted")
@icontract.snapshot(lambda sorted_list, val, key=None, low=None, high=None: (low if low is not None else 0), name="LOW")
@icontract.snapshot(lambda sorted_list, val, key=None, low=None, high=None: (high if high is not None else len(sorted_list) - 1), name="HIGH")
@icontract.ensure(lambda OLD, result: isinstance(result, int) and OLD.LOW <= result <= OLD.HIGH + 1)
@icontract.ensure(lambda OLD, result, val, key: result == (next((i for i in range(OLD.LOW, OLD.HIGH + 1) if (((key(OLD.sorted[i]) - key(val)) if key is not None else (OLD.sorted[i] - val)) > 0)), OLD.HIGH + 1)))
```
