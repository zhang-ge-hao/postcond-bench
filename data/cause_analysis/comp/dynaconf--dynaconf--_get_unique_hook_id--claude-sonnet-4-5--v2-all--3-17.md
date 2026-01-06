https://github.com/dynaconf/dynaconf/blob/09c10d1a91854894986da19fb70f1b54a47cd865/./dynaconf/loaders/__init__.py#L150-L163
```
@icontract.ensure(lambda result: isinstance(result, str))
@icontract.ensure(lambda result, hook_source: result.endswith(f"@{hook_source}"))
@icontract.ensure(lambda result: '@' in result)
@icontract.ensure(lambda hook_func, result: 
                  hook_func.__name__ != "<lambda>" and result.startswith(f"{hook_func.__name__}@") 
                  or hook_func.__name__ == "<lambda>" and result.startswith("lambda_"))
@icontract.ensure(lambda result: len(result.split('@')) == 2)
```
```
return value - primitive-like/scalar types


return value content

primitive-like/scalar types
```
passed
```
@icontract.ensure(lambda result, hook_func, hook_source: (hook_func.__name__ != "<lambda>" and result == f"{hook_func.__name__}@{hook_source}") or (hook_func.__name__ == "<lambda>" and getattr(hook_func, "__code__", None) is not None and result == f"lambda_{hash(getattr(hook_func, '__code__').co_code)}@{hook_source}") or (hook_func.__name__ == "<lambda>" and getattr(hook_func, "__code__", None) is None and result == f"lambda_{id(hook_func)}@{hook_source}"))
```
===== 17: failed =====
```
     hook_unique_id = hook_func.__name__
     if hook_unique_id == "<lambda>":
         frame_info = getattr(hook_func, "__code__", None)
-        if frame_info:
+        if frame_info is None:
             hook_unique_id = f"lambda_{hash(frame_info.co_code)}"
         else:
             hook_unique_id = f"lambda_{id(hook_func)}"
```
```
def _get_unique_hook_id(hook_func, hook_source):
    """get unique identifier for a hook function.
    in most of cases this will be the function name@source_file
    however, if the function is a lambda, it will be a hash of the code object.
    because lambda functions are not hashable itself and we can't rely on its id.
    """
    hook_unique_id = hook_func.__name__
    if hook_unique_id == "<lambda>":
        frame_info = getattr(hook_func, "__code__", None)
        if frame_info is None:
            hook_unique_id = f"lambda_{hash(frame_info.co_code)}"
        else:
            hook_unique_id = f"lambda_{id(hook_func)}"
    return f"{hook_unique_id}@{hook_source}"
```
