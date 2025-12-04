https://github.com/pypyr/pypyr/blob/b3e8f8c6063c11e37c1c762b89b4cd8620460c79/./pypyr/cache/loadercache.py#L156-L174
```
@icontract.snapshot(lambda self, loader_name=None: {k: dict(v._pipeline_cache._cache) for k, v in self._cache.items()}, name="old_pipes")
@icontract.snapshot(lambda self, loader_name=None: {k: id(v) for k, v in self._cache.items()}, name="old_ids")
@icontract.snapshot(lambda self, loader_name=None: {k: id(v._pipeline_cache._cache) for k, v in self._cache.items()}, name="old_pipe_ids")
@icontract.ensure(lambda OLD, self, loader_name=None: set(self._cache.keys()) == set(OLD.old_pipes.keys()))
@icontract.ensure(lambda OLD, self, loader_name=None: all(id(self._cache[k]) == OLD.old_ids[k] for k in OLD.old_ids))
@icontract.ensure(lambda OLD, self, loader_name=None: (
    (bool(loader_name) and loader_name in OLD.old_pipes and
        loader_name in self._cache and 
        self._cache[loader_name]._pipeline_cache._cache == {} and
        id(self._cache[loader_name]._pipeline_cache._cache) == OLD.old_pipe_ids[loader_name] and
        all((k == loader_name) or (self._cache[k]._pipeline_cache._cache == OLD.old_pipes[k] and id(self._cache[k]._pipeline_cache._cache) == OLD.old_pipe_ids[k]) for k in OLD.old_pipes)
    )
    or
    (bool(loader_name) and loader_name not in OLD.old_pipes and
        all(self._cache[k]._pipeline_cache._cache == OLD.old_pipes[k] and id(self._cache[k]._pipeline_cache._cache) == OLD.old_pipe_ids[k] for k in OLD.old_pipes)
    )
    or
    (not bool(loader_name) and
        all(self._cache[k]._pipeline_cache._cache == {} and id(self._cache[k]._pipeline_cache._cache) == OLD.old_pipe_ids[k] for k in OLD.old_pipes)
    )
))
```
```
@icontract.snapshot(lambda self, loader_name=None: {k: dict(v._pipeline_cache._cache) for k, v in self._cache.items()}, name="old_pipes")
@icontract.snapshot(lambda self, loader_name=None: {k: id(v) for k, v in self._cache.items()}, name="old_ids")
@icontract.snapshot(lambda self, loader_name=None: {k: id(v._pipeline_cache._cache) for k, v in self._cache.items()}, name="old_pipe_ids")
@icontract.ensure(lambda OLD, self, loader_name=None: set(self._cache.keys()) == set(OLD.old_pipes.keys()))
@icontract.ensure(lambda OLD, self, loader_name=None: all(id(self._cache[k]) == OLD.old_ids[k] for k in OLD.old_ids))
@icontract.ensure(lambda OLD, self, loader_name=None: (
    (bool(loader_name) and loader_name in OLD.old_pipes and
        # the requested loader's pipeline cache must be cleared in-place
        self._cache[loader_name]._pipeline_cache._cache == {} and
        id(self._cache[loader_name]._pipeline_cache._cache) == OLD.old_pipe_ids[loader_name] and
        # all other loaders unchanged (same contents and same pipeline-cache object)
        all((k == loader_name) or (self._cache[k]._pipeline_cache._cache == OLD.old_pipes[k] and id(self._cache[k]._pipeline_cache._cache) == OLD.old_pipe_ids[k]) for k in OLD.old_pipes)
    )
    or
    (bool(loader_name) and loader_name not in OLD.old_pipes and
        # no changes when loader_name provided but missing from cache
        all(self._cache[k]._pipeline_cache._cache == OLD.old_pipes[k] and id(self._cache[k]._pipeline_cache._cache) == OLD.old_pipe_ids[k] for k in OLD.old_pipes)
    )
    or
    (not bool(loader_name) and
        # when no loader_name (falsy), all loaders must be cleared in-place
        all(self._cache[k]._pipeline_cache._cache == {} and id(self._cache[k]._pipeline_cache._cache) == OLD.old_pipe_ids[k] for k in OLD.old_pipes)
    )
))
```
[9]
===== 9 =====
```
         if loader_name:
             loader = self._cache.get(loader_name, None)
             if loader:
-                loader.clear()
+                self.clear()  # This mistakenly calls the clear method on the current instance instead of the loader.
             else:
                 logger.debug(
                     "%s not found in loader cache so there's nothing to clear",
```
```
    def clear_pipes(self, loader_name=None):
        """Clear the pipeline cache.

        Args:
            loader_name (str): Clear pipelines for this loader. If not
                specified, will iterate all loaders in the loaders cache and
                clear each of their pipelines.
        """
        if loader_name:
            loader = self._cache.get(loader_name, None)
            if loader:
                self.clear()  # This mistakenly calls the clear method on the current instance instead of the loader.
            else:
                logger.debug(
                    "%s not found in loader cache so there's nothing to clear",
                    loader_name)
        else:
            for _, loader in self._cache.items():
                loader.clear()
```
