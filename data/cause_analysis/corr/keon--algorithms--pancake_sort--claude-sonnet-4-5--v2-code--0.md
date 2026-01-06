https://github.com/keon/algorithms/blob/5b63e90624bebb371949fbe49bbf20aa3c8e14d0/./algorithms/sort/pancake_sort.py#L1-L25
```
@icontract.snapshot(lambda arr: arr[:], name="original_arr")
@icontract.ensure(lambda result: all(result[i] <= result[i+1] for i in range(len(result)-1)) if len(result) > 1 else True)
@icontract.ensure(lambda result, original_arr: len(result) == len(original_arr))
@icontract.ensure(lambda result, original_arr: sorted(result) == sorted(original_arr))
```
```
limited spec

original_arr
```
failed
```
@icontract.snapshot(lambda arr: arr[:], name="old")
@icontract.ensure(lambda OLD, arr: sorted(arr) == sorted(OLD.old))
@icontract.ensure(lambda arr: all(arr[i] <= arr[i+1] for i in range(len(arr)-1)))
@icontract.ensure(lambda result, arr: result is arr)
```
