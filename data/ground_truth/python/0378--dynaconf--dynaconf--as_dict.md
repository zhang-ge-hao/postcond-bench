https://github.com/dynaconf/dynaconf/blob/09c10d1a91854894986da19fb70f1b54a47cd865/./dynaconf/base.py#L346-L359
```
@icontract.snapshot(lambda self: self.store, name="old_store_obj")
@icontract.snapshot(lambda self: self.store.to_dict().copy(), name="old_store")
@icontract.snapshot(lambda env: env, name="in_env")
@icontract.ensure(lambda result: isinstance(result, dict))
@icontract.ensure(lambda OLD, self: self.store.to_dict() == OLD.old_store)
@icontract.ensure(lambda OLD, result: result is not OLD.old_store_obj)
@icontract.ensure(lambda OLD, result, internal: (result == OLD.old_store) if internal else True)
@icontract.ensure(lambda OLD, result, internal: all((k not in result) for k in UPPER_DEFAULT_SETTINGS) if not internal else True)
@icontract.ensure(lambda OLD, result, internal: all((k in result and result[k] == OLD.old_store[k]) for k in OLD.old_store.keys() if (internal or k not in UPPER_DEFAULT_SETTINGS)))
@icontract.ensure(lambda OLD, result: set(result.keys()).issubset(set(OLD.old_store.keys())))
```
```
@icontract.snapshot(lambda self: self.store, name="old_store_obj")
@icontract.snapshot(lambda self: self.store.to_dict().copy(), name="old_store")
@icontract.snapshot(lambda env: env, name="in_env")
@icontract.ensure(lambda result: isinstance(result, dict))
@icontract.ensure(lambda OLD, self: self.store.to_dict() == OLD.old_store)
@icontract.ensure(lambda OLD, result: result is not OLD.old_store_obj)
@icontract.ensure(lambda OLD, result, internal: (result == OLD.old_store) if internal else True)
@icontract.ensure(lambda OLD, result, internal: all((k not in result) for k in UPPER_DEFAULT_SETTINGS) if not internal else True)
@icontract.ensure(lambda OLD, result, internal: all((k in result and result[k] == OLD.old_store[k]) for k in OLD.old_store.keys() if (internal or k not in UPPER_DEFAULT_SETTINGS)))
@icontract.ensure(lambda OLD, result: set(result.keys()).issubset(set(OLD.old_store.keys())))
```
[0]
===== 0 =====
```
         :param env: Str env name, default self.current_env `DEVELOPMENT`
         :param internal: bool - should include dynaconf internal vars?
         """
-        ctx_mgr = suppress() if env is None else self.using_env(env)
+        ctx_mgr = suppress() if env is None else self.using_env(None)
         with ctx_mgr:
             data = self.store.to_dict().copy()
             # if not internal remove internal settings
             if not internal:
                 for name in UPPER_DEFAULT_SETTINGS:
                     data.pop(name, None)
-            return data+            return data
```
```
    def as_dict(self, env=None, internal=False):
        """Returns a dictionary with set key and values.

        :param env: Str env name, default self.current_env `DEVELOPMENT`
        :param internal: bool - should include dynaconf internal vars?
        """
        ctx_mgr = suppress() if env is None else self.using_env(None)
        with ctx_mgr:
            data = self.store.to_dict().copy()
            # if not internal remove internal settings
            if not internal:
                for name in UPPER_DEFAULT_SETTINGS:
                    data.pop(name, None)
            return data

```
