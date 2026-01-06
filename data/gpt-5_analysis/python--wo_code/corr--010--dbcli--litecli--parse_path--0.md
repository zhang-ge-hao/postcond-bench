https://github.com/dbcli/litecli/blob/c072661298bc52b10c11e6571cc741a6d41360a7/./litecli/packages/filepaths.py#L39-L52
```
@icontract.ensure(lambda result: isinstance(result, tuple) and len(result) == 3)
@icontract.ensure(lambda result: isinstance(result[0], str) and isinstance(result[1], str) and isinstance(result[2], int))
@icontract.ensure(lambda root_dir, result: 0 <= result[2] <= len(root_dir))
@icontract.ensure(lambda root_dir, result: root_dir[result[2]:] == result[1])
@icontract.ensure(lambda root_dir, result: result[2] == len(root_dir) - len(result[1]))
@icontract.ensure(lambda root_dir, result: result[1] == os.path.basename(root_dir))
@icontract.ensure(lambda result: (os.sep not in result[1]) and (os.altsep is None or os.altsep not in result[1]))
@icontract.ensure(lambda root_dir, result: result[0] == root_dir[:result[2]])
```
```
Corner case missed.

@icontract.ensure(lambda root_dir, result: 0 <= result[2] <= len(root_dir))
However, the position can be negative.
```
icontract_fail
```
@icontract.ensure(lambda result: isinstance(result, tuple) and len(result) == 3)
@icontract.ensure(lambda result: isinstance(result[0], str) and isinstance(result[1], str) and isinstance(result[2], int))
@icontract.ensure(lambda result: result[2] == (-len(result[1]) if result[1] else 0))
@icontract.ensure(lambda result, root_dir: (not root_dir and result == ("", "", 0)) or (root_dir and (result[0] == __import__("os").path.split(root_dir)[0] and result[1] == __import__("os").path.split(root_dir)[1])))
```
