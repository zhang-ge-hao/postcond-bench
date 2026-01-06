https://github.com/daavoo/pyntcloud/blob/8368c6a22f8060aeafacf2964276e8704d732145/./src/pyntcloud/utils/array.py#L4-L50
```
@icontract.snapshot(lambda arrays: [np.asarray(x) for x in arrays], name="arrs")
@icontract.snapshot(lambda OLD: tuple(len(a) for a in OLD.arrs), name="shape")
@icontract.snapshot(lambda OLD: None if len(OLD.arrs) == 0 else np.indices(OLD.shape).reshape(len(OLD.arrs), -1).T, name="ix")
@icontract.ensure(lambda out, result: (out is None) or (result is out))
@icontract.ensure(lambda result: result.ndim == 2)
@icontract.ensure(lambda arrays, result: result.shape[1] == len(arrays))
@icontract.ensure(lambda arrays, OLD, result: (len(arrays) == 0) or (result.shape[0] == int(np.prod(OLD.shape))))
@icontract.ensure(lambda arrays, OLD, result: (len(arrays) == 0) or (result.dtype == OLD.arrs[0].dtype))
@icontract.ensure(lambda arrays, OLD, result: (len(arrays) == 0) or np.array_equal(result, np.column_stack([OLD.arrs[n][OLD.ix[:, n]] for n in range(len(arrays))])))
```
```
Limited specification language knowledge.

E   The argument(s) of the snapshot have not been set: ['OLD']. Does the original function define them? Did you supply them in the call?
```
failed
```
@icontract.snapshot(lambda arrays: [np.asarray(x) for x in arrays], name="orig_arrays")
@icontract.ensure(lambda result, arrays, OLD: isinstance(result, np.ndarray))
@icontract.ensure(lambda result, arrays, OLD: result.ndim == 2)
@icontract.ensure(lambda result, arrays, OLD: result.shape[1] == len(OLD.orig_arrays))
@icontract.ensure(lambda result, arrays, OLD: result.shape[0] == int(np.prod([len(a) for a in OLD.orig_arrays])))
@icontract.ensure(lambda result, arrays, OLD: result.dtype == np.asarray(OLD.orig_arrays[0]).dtype)
@icontract.ensure(lambda result, arrays, OLD: np.array_equal(result, np.vstack([v.ravel() for v in np.meshgrid(*[np.asarray(a) for a in OLD.orig_arrays], indexing='ij')]).T))
```
