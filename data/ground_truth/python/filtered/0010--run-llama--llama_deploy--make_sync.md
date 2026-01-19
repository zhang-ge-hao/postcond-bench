https://github.com/run-llama/llama_deploy/blob/dbe78972b06f8d8b021da0b313bb0e4f3dc32d46/./llama_deploy/client/models/model.py#L59-L80
```
🈚️

class object
```
```
None
```
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31]
===== 0 =====
```
         func: Callable[_P, AsyncGenerator[_G, None]], /, *args: Any, **kwargs: Any
     ) -> Callable[_P, list[_G]]:
         def new_func(*fargs: Any, **fkwargs: Any) -> list[_G]:
-            return asyncio.run(_async_gen_to_list(func(*fargs, **fkwargs)))
+            return _async_gen_to_list(func(*fargs, **fkwargs))
 
         return new_func
```
```
def make_sync(_class: type[T]) -> Any:
    """Wraps the methods of the given model class so that they can be called without `await`."""

    class ModelWrapper(_class):  # type: ignore
        _instance_is_sync: bool = True

    def generator_wrapper(
        func: Callable[_P, AsyncGenerator[_G, None]], /, *args: Any, **kwargs: Any
    ) -> Callable[_P, list[_G]]:
        def new_func(*fargs: Any, **fkwargs: Any) -> list[_G]:
            return _async_gen_to_list(func(*fargs, **fkwargs))

        return new_func

    for name, method in _class.__dict__.items():
        # Only wrap async public methods
        if inspect.isasyncgenfunction(method):
            setattr(ModelWrapper, name, generator_wrapper(method))
        elif asyncio.iscoroutinefunction(method) and not name.startswith("_"):
            setattr(ModelWrapper, name, async_to_sync(method))

    return ModelWrapper
```
===== 1 =====
```
         func: Callable[_P, AsyncGenerator[_G, None]], /, *args: Any, **kwargs: Any
     ) -> Callable[_P, list[_G]]:
         def new_func(*fargs: Any, **fkwargs: Any) -> list[_G]:
-            return asyncio.run(_async_gen_to_list(func(*fargs, **fkwargs)))
+            return asyncio.run(None)
 
         return new_func
 
@@ -19,4 +19,4 @@         elif asyncio.iscoroutinefunction(method) and not name.startswith("_"):
             setattr(ModelWrapper, name, async_to_sync(method))
 
-    return ModelWrapper+    return ModelWrapper
```
```
def make_sync(_class: type[T]) -> Any:
    """Wraps the methods of the given model class so that they can be called without `await`."""

    class ModelWrapper(_class):  # type: ignore
        _instance_is_sync: bool = True

    def generator_wrapper(
        func: Callable[_P, AsyncGenerator[_G, None]], /, *args: Any, **kwargs: Any
    ) -> Callable[_P, list[_G]]:
        def new_func(*fargs: Any, **fkwargs: Any) -> list[_G]:
            return asyncio.run(None)

        return new_func

    for name, method in _class.__dict__.items():
        # Only wrap async public methods
        if inspect.isasyncgenfunction(method):
            setattr(ModelWrapper, name, generator_wrapper(method))
        elif asyncio.iscoroutinefunction(method) and not name.startswith("_"):
            setattr(ModelWrapper, name, async_to_sync(method))

    return ModelWrapper

```
===== 2 =====
```
         func: Callable[_P, AsyncGenerator[_G, None]], /, *args: Any, **kwargs: Any
     ) -> Callable[_P, list[_G]]:
         def new_func(*fargs: Any, **fkwargs: Any) -> list[_G]:
-            return asyncio.run(_async_gen_to_list(func(*fargs, **fkwargs)))
+            return asyncio.run(_async_gen_to_list(None))
 
         return new_func
 
@@ -19,4 +19,4 @@         elif asyncio.iscoroutinefunction(method) and not name.startswith("_"):
             setattr(ModelWrapper, name, async_to_sync(method))
 
-    return ModelWrapper+    return ModelWrapper
```
```
def make_sync(_class: type[T]) -> Any:
    """Wraps the methods of the given model class so that they can be called without `await`."""

    class ModelWrapper(_class):  # type: ignore
        _instance_is_sync: bool = True

    def generator_wrapper(
        func: Callable[_P, AsyncGenerator[_G, None]], /, *args: Any, **kwargs: Any
    ) -> Callable[_P, list[_G]]:
        def new_func(*fargs: Any, **fkwargs: Any) -> list[_G]:
            return asyncio.run(_async_gen_to_list(None))

        return new_func

    for name, method in _class.__dict__.items():
        # Only wrap async public methods
        if inspect.isasyncgenfunction(method):
            setattr(ModelWrapper, name, generator_wrapper(method))
        elif asyncio.iscoroutinefunction(method) and not name.startswith("_"):
            setattr(ModelWrapper, name, async_to_sync(method))

    return ModelWrapper

```
===== 3 =====
```
         func: Callable[_P, AsyncGenerator[_G, None]], /, *args: Any, **kwargs: Any
     ) -> Callable[_P, list[_G]]:
         def new_func(*fargs: Any, **fkwargs: Any) -> list[_G]:
-            return asyncio.run(_async_gen_to_list(func(*fargs, **fkwargs)))
+            return asyncio.run(_async_gen_to_list(func(**fkwargs)))
 
         return new_func
 
@@ -19,4 +19,4 @@         elif asyncio.iscoroutinefunction(method) and not name.startswith("_"):
             setattr(ModelWrapper, name, async_to_sync(method))
 
-    return ModelWrapper+    return ModelWrapper
```
```
def make_sync(_class: type[T]) -> Any:
    """Wraps the methods of the given model class so that they can be called without `await`."""

    class ModelWrapper(_class):  # type: ignore
        _instance_is_sync: bool = True

    def generator_wrapper(
        func: Callable[_P, AsyncGenerator[_G, None]], /, *args: Any, **kwargs: Any
    ) -> Callable[_P, list[_G]]:
        def new_func(*fargs: Any, **fkwargs: Any) -> list[_G]:
            return asyncio.run(_async_gen_to_list(func(**fkwargs)))

        return new_func

    for name, method in _class.__dict__.items():
        # Only wrap async public methods
        if inspect.isasyncgenfunction(method):
            setattr(ModelWrapper, name, generator_wrapper(method))
        elif asyncio.iscoroutinefunction(method) and not name.startswith("_"):
            setattr(ModelWrapper, name, async_to_sync(method))

    return ModelWrapper

```
===== 4 =====
```
         func: Callable[_P, AsyncGenerator[_G, None]], /, *args: Any, **kwargs: Any
     ) -> Callable[_P, list[_G]]:
         def new_func(*fargs: Any, **fkwargs: Any) -> list[_G]:
-            return asyncio.run(_async_gen_to_list(func(*fargs, **fkwargs)))
+            return asyncio.run(_async_gen_to_list(func(*fargs, **fkwargs)))[:1]
 
         return new_func
```
```
def make_sync(_class: type[T]) -> Any:
    """Wraps the methods of the given model class so that they can be called without `await`."""

    class ModelWrapper(_class):  # type: ignore
        _instance_is_sync: bool = True

    def generator_wrapper(
        func: Callable[_P, AsyncGenerator[_G, None]], /, *args: Any, **kwargs: Any
    ) -> Callable[_P, list[_G]]:
        def new_func(*fargs: Any, **fkwargs: Any) -> list[_G]:
            return asyncio.run(_async_gen_to_list(func(*fargs, **fkwargs)))[:1]

        return new_func

    for name, method in _class.__dict__.items():
        # Only wrap async public methods
        if inspect.isasyncgenfunction(method):
            setattr(ModelWrapper, name, generator_wrapper(method))
        elif asyncio.iscoroutinefunction(method) and not name.startswith("_"):
            setattr(ModelWrapper, name, async_to_sync(method))

    return ModelWrapper
```
===== 5 =====
```
         func: Callable[_P, AsyncGenerator[_G, None]], /, *args: Any, **kwargs: Any
     ) -> Callable[_P, list[_G]]:
         def new_func(*fargs: Any, **fkwargs: Any) -> list[_G]:
-            return asyncio.run(_async_gen_to_list(func(*fargs, **fkwargs)))
+            return asyncio.run(func(*fargs, **fkwargs))
 
         return new_func
```
```
def make_sync(_class: type[T]) -> Any:
    """Wraps the methods of the given model class so that they can be called without `await`."""

    class ModelWrapper(_class):  # type: ignore
        _instance_is_sync: bool = True

    def generator_wrapper(
        func: Callable[_P, AsyncGenerator[_G, None]], /, *args: Any, **kwargs: Any
    ) -> Callable[_P, list[_G]]:
        def new_func(*fargs: Any, **fkwargs: Any) -> list[_G]:
            return asyncio.run(func(*fargs, **fkwargs))

        return new_func

    for name, method in _class.__dict__.items():
        # Only wrap async public methods
        if inspect.isasyncgenfunction(method):
            setattr(ModelWrapper, name, generator_wrapper(method))
        elif asyncio.iscoroutinefunction(method) and not name.startswith("_"):
            setattr(ModelWrapper, name, async_to_sync(method))

    return ModelWrapper
```
===== 6 =====
```
 
     for name, method in _class.__dict__.items():
         # Only wrap async public methods
-        if inspect.isasyncgenfunction(method):
+        if inspect.isasyncgenfunction(None):
             setattr(ModelWrapper, name, generator_wrapper(method))
         elif asyncio.iscoroutinefunction(method) and not name.startswith("_"):
             setattr(ModelWrapper, name, async_to_sync(method))
 
-    return ModelWrapper+    return ModelWrapper
```
```
def make_sync(_class: type[T]) -> Any:
    """Wraps the methods of the given model class so that they can be called without `await`."""

    class ModelWrapper(_class):  # type: ignore
        _instance_is_sync: bool = True

    def generator_wrapper(
        func: Callable[_P, AsyncGenerator[_G, None]], /, *args: Any, **kwargs: Any
    ) -> Callable[_P, list[_G]]:
        def new_func(*fargs: Any, **fkwargs: Any) -> list[_G]:
            return asyncio.run(_async_gen_to_list(func(*fargs, **fkwargs)))

        return new_func

    for name, method in _class.__dict__.items():
        # Only wrap async public methods
        if inspect.isasyncgenfunction(None):
            setattr(ModelWrapper, name, generator_wrapper(method))
        elif asyncio.iscoroutinefunction(method) and not name.startswith("_"):
            setattr(ModelWrapper, name, async_to_sync(method))

    return ModelWrapper

```
===== 7 =====
```
 
     for name, method in _class.__dict__.items():
         # Only wrap async public methods
-        if inspect.isasyncgenfunction(method):
+        if inspect.isasyncgenfunction(method) and name.startswith("_"):  # This will only wrap private async generator methods.
             setattr(ModelWrapper, name, generator_wrapper(method))
         elif asyncio.iscoroutinefunction(method) and not name.startswith("_"):
             setattr(ModelWrapper, name, async_to_sync(method))
```
```
def make_sync(_class: type[T]) -> Any:
    """Wraps the methods of the given model class so that they can be called without `await`."""

    class ModelWrapper(_class):  # type: ignore
        _instance_is_sync: bool = True

    def generator_wrapper(
        func: Callable[_P, AsyncGenerator[_G, None]], /, *args: Any, **kwargs: Any
    ) -> Callable[_P, list[_G]]:
        def new_func(*fargs: Any, **fkwargs: Any) -> list[_G]:
            return asyncio.run(_async_gen_to_list(func(*fargs, **fkwargs)))

        return new_func

    for name, method in _class.__dict__.items():
        # Only wrap async public methods
        if inspect.isasyncgenfunction(method) and name.startswith("_"):  # This will only wrap private async generator methods.
            setattr(ModelWrapper, name, generator_wrapper(method))
        elif asyncio.iscoroutinefunction(method) and not name.startswith("_"):
            setattr(ModelWrapper, name, async_to_sync(method))

    return ModelWrapper
```
===== 8 =====
```
 
     for name, method in _class.__dict__.items():
         # Only wrap async public methods
-        if inspect.isasyncgenfunction(method):
+        if inspect.isasyncgenfunction(method) or inspect.iscoroutinefunction(method):  # This will wrap both async generators and async functions, leading to incorrect behavior.
             setattr(ModelWrapper, name, generator_wrapper(method))
         elif asyncio.iscoroutinefunction(method) and not name.startswith("_"):
             setattr(ModelWrapper, name, async_to_sync(method))
```
```
def make_sync(_class: type[T]) -> Any:
    """Wraps the methods of the given model class so that they can be called without `await`."""

    class ModelWrapper(_class):  # type: ignore
        _instance_is_sync: bool = True

    def generator_wrapper(
        func: Callable[_P, AsyncGenerator[_G, None]], /, *args: Any, **kwargs: Any
    ) -> Callable[_P, list[_G]]:
        def new_func(*fargs: Any, **fkwargs: Any) -> list[_G]:
            return asyncio.run(_async_gen_to_list(func(*fargs, **fkwargs)))

        return new_func

    for name, method in _class.__dict__.items():
        # Only wrap async public methods
        if inspect.isasyncgenfunction(method) or inspect.iscoroutinefunction(method):  # This will wrap both async generators and async functions, leading to incorrect behavior.
            setattr(ModelWrapper, name, generator_wrapper(method))
        elif asyncio.iscoroutinefunction(method) and not name.startswith("_"):
            setattr(ModelWrapper, name, async_to_sync(method))

    return ModelWrapper
```
===== 9 =====
```
 
     for name, method in _class.__dict__.items():
         # Only wrap async public methods
-        if inspect.isasyncgenfunction(method):
+        if inspect.iscoroutinefunction(method) and name.endswith("Async"):  # This will only wrap methods with names ending in 'Async'.
             setattr(ModelWrapper, name, generator_wrapper(method))
         elif asyncio.iscoroutinefunction(method) and not name.startswith("_"):
             setattr(ModelWrapper, name, async_to_sync(method))
```
```
def make_sync(_class: type[T]) -> Any:
    """Wraps the methods of the given model class so that they can be called without `await`."""

    class ModelWrapper(_class):  # type: ignore
        _instance_is_sync: bool = True

    def generator_wrapper(
        func: Callable[_P, AsyncGenerator[_G, None]], /, *args: Any, **kwargs: Any
    ) -> Callable[_P, list[_G]]:
        def new_func(*fargs: Any, **fkwargs: Any) -> list[_G]:
            return asyncio.run(_async_gen_to_list(func(*fargs, **fkwargs)))

        return new_func

    for name, method in _class.__dict__.items():
        # Only wrap async public methods
        if inspect.iscoroutinefunction(method) and name.endswith("Async"):  # This will only wrap methods with names ending in 'Async'.
            setattr(ModelWrapper, name, generator_wrapper(method))
        elif asyncio.iscoroutinefunction(method) and not name.startswith("_"):
            setattr(ModelWrapper, name, async_to_sync(method))

    return ModelWrapper
```
===== 10 =====
```
 
     for name, method in _class.__dict__.items():
         # Only wrap async public methods
-        if inspect.isasyncgenfunction(method):
+        if inspect.isfunction(method):  # This will wrap all regular functions, not just async ones.
             setattr(ModelWrapper, name, generator_wrapper(method))
         elif asyncio.iscoroutinefunction(method) and not name.startswith("_"):
             setattr(ModelWrapper, name, async_to_sync(method))
```
```
def make_sync(_class: type[T]) -> Any:
    """Wraps the methods of the given model class so that they can be called without `await`."""

    class ModelWrapper(_class):  # type: ignore
        _instance_is_sync: bool = True

    def generator_wrapper(
        func: Callable[_P, AsyncGenerator[_G, None]], /, *args: Any, **kwargs: Any
    ) -> Callable[_P, list[_G]]:
        def new_func(*fargs: Any, **fkwargs: Any) -> list[_G]:
            return asyncio.run(_async_gen_to_list(func(*fargs, **fkwargs)))

        return new_func

    for name, method in _class.__dict__.items():
        # Only wrap async public methods
        if inspect.isfunction(method):  # This will wrap all regular functions, not just async ones.
            setattr(ModelWrapper, name, generator_wrapper(method))
        elif asyncio.iscoroutinefunction(method) and not name.startswith("_"):
            setattr(ModelWrapper, name, async_to_sync(method))

    return ModelWrapper
```
===== 11 =====
```
 
     for name, method in _class.__dict__.items():
         # Only wrap async public methods
-        if inspect.isasyncgenfunction(method):
+        if not inspect.iscoroutinefunction(method):  # This will skip wrapping async functions entirely.
             setattr(ModelWrapper, name, generator_wrapper(method))
         elif asyncio.iscoroutinefunction(method) and not name.startswith("_"):
             setattr(ModelWrapper, name, async_to_sync(method))
```
```
def make_sync(_class: type[T]) -> Any:
    """Wraps the methods of the given model class so that they can be called without `await`."""

    class ModelWrapper(_class):  # type: ignore
        _instance_is_sync: bool = True

    def generator_wrapper(
        func: Callable[_P, AsyncGenerator[_G, None]], /, *args: Any, **kwargs: Any
    ) -> Callable[_P, list[_G]]:
        def new_func(*fargs: Any, **fkwargs: Any) -> list[_G]:
            return asyncio.run(_async_gen_to_list(func(*fargs, **fkwargs)))

        return new_func

    for name, method in _class.__dict__.items():
        # Only wrap async public methods
        if not inspect.iscoroutinefunction(method):  # This will skip wrapping async functions entirely.
            setattr(ModelWrapper, name, generator_wrapper(method))
        elif asyncio.iscoroutinefunction(method) and not name.startswith("_"):
            setattr(ModelWrapper, name, async_to_sync(method))

    return ModelWrapper
```
===== 12 =====
```
     for name, method in _class.__dict__.items():
         # Only wrap async public methods
         if inspect.isasyncgenfunction(method):
-            setattr(ModelWrapper, name, generator_wrapper(method))
+            setattr(ModelWrapper, name, None)
         elif asyncio.iscoroutinefunction(method) and not name.startswith("_"):
             setattr(ModelWrapper, name, async_to_sync(method))
 
-    return ModelWrapper+    return ModelWrapper
```
```
def make_sync(_class: type[T]) -> Any:
    """Wraps the methods of the given model class so that they can be called without `await`."""

    class ModelWrapper(_class):  # type: ignore
        _instance_is_sync: bool = True

    def generator_wrapper(
        func: Callable[_P, AsyncGenerator[_G, None]], /, *args: Any, **kwargs: Any
    ) -> Callable[_P, list[_G]]:
        def new_func(*fargs: Any, **fkwargs: Any) -> list[_G]:
            return asyncio.run(_async_gen_to_list(func(*fargs, **fkwargs)))

        return new_func

    for name, method in _class.__dict__.items():
        # Only wrap async public methods
        if inspect.isasyncgenfunction(method):
            setattr(ModelWrapper, name, None)
        elif asyncio.iscoroutinefunction(method) and not name.startswith("_"):
            setattr(ModelWrapper, name, async_to_sync(method))

    return ModelWrapper

```
===== 13 =====
```
     for name, method in _class.__dict__.items():
         # Only wrap async public methods
         if inspect.isasyncgenfunction(method):
-            setattr(ModelWrapper, name, generator_wrapper(method))
+            setattr(ModelWrapper, name, async_to_sync(method) if name.endswith("Async") else method)
         elif asyncio.iscoroutinefunction(method) and not name.startswith("_"):
             setattr(ModelWrapper, name, async_to_sync(method))
```
```
def make_sync(_class: type[T]) -> Any:
    """Wraps the methods of the given model class so that they can be called without `await`."""

    class ModelWrapper(_class):  # type: ignore
        _instance_is_sync: bool = True

    def generator_wrapper(
        func: Callable[_P, AsyncGenerator[_G, None]], /, *args: Any, **kwargs: Any
    ) -> Callable[_P, list[_G]]:
        def new_func(*fargs: Any, **fkwargs: Any) -> list[_G]:
            return asyncio.run(_async_gen_to_list(func(*fargs, **fkwargs)))

        return new_func

    for name, method in _class.__dict__.items():
        # Only wrap async public methods
        if inspect.isasyncgenfunction(method):
            setattr(ModelWrapper, name, async_to_sync(method) if name.endswith("Async") else method)
        elif asyncio.iscoroutinefunction(method) and not name.startswith("_"):
            setattr(ModelWrapper, name, async_to_sync(method))

    return ModelWrapper
```
===== 14 =====
```
     for name, method in _class.__dict__.items():
         # Only wrap async public methods
         if inspect.isasyncgenfunction(method):
-            setattr(ModelWrapper, name, generator_wrapper(method))
+            setattr(ModelWrapper, name, generator_wrapper(None))
         elif asyncio.iscoroutinefunction(method) and not name.startswith("_"):
             setattr(ModelWrapper, name, async_to_sync(method))
 
-    return ModelWrapper+    return ModelWrapper
```
```
def make_sync(_class: type[T]) -> Any:
    """Wraps the methods of the given model class so that they can be called without `await`."""

    class ModelWrapper(_class):  # type: ignore
        _instance_is_sync: bool = True

    def generator_wrapper(
        func: Callable[_P, AsyncGenerator[_G, None]], /, *args: Any, **kwargs: Any
    ) -> Callable[_P, list[_G]]:
        def new_func(*fargs: Any, **fkwargs: Any) -> list[_G]:
            return asyncio.run(_async_gen_to_list(func(*fargs, **fkwargs)))

        return new_func

    for name, method in _class.__dict__.items():
        # Only wrap async public methods
        if inspect.isasyncgenfunction(method):
            setattr(ModelWrapper, name, generator_wrapper(None))
        elif asyncio.iscoroutinefunction(method) and not name.startswith("_"):
            setattr(ModelWrapper, name, async_to_sync(method))

    return ModelWrapper

```
===== 15 =====
```
     for name, method in _class.__dict__.items():
         # Only wrap async public methods
         if inspect.isasyncgenfunction(method):
-            setattr(ModelWrapper, name, generator_wrapper(method))
+            setattr(ModelWrapper, name, generator_wrapper(method) if name == "some_specific_method" else method)
         elif asyncio.iscoroutinefunction(method) and not name.startswith("_"):
             setattr(ModelWrapper, name, async_to_sync(method))
```
```
def make_sync(_class: type[T]) -> Any:
    """Wraps the methods of the given model class so that they can be called without `await`."""

    class ModelWrapper(_class):  # type: ignore
        _instance_is_sync: bool = True

    def generator_wrapper(
        func: Callable[_P, AsyncGenerator[_G, None]], /, *args: Any, **kwargs: Any
    ) -> Callable[_P, list[_G]]:
        def new_func(*fargs: Any, **fkwargs: Any) -> list[_G]:
            return asyncio.run(_async_gen_to_list(func(*fargs, **fkwargs)))

        return new_func

    for name, method in _class.__dict__.items():
        # Only wrap async public methods
        if inspect.isasyncgenfunction(method):
            setattr(ModelWrapper, name, generator_wrapper(method) if name == "some_specific_method" else method)
        elif asyncio.iscoroutinefunction(method) and not name.startswith("_"):
            setattr(ModelWrapper, name, async_to_sync(method))

    return ModelWrapper
```
===== 16 =====
```
     for name, method in _class.__dict__.items():
         # Only wrap async public methods
         if inspect.isasyncgenfunction(method):
-            setattr(ModelWrapper, name, generator_wrapper(method))
+            setattr(ModelWrapper, name, generator_wrapper(method) if name.startswith("list") else method)
         elif asyncio.iscoroutinefunction(method) and not name.startswith("_"):
             setattr(ModelWrapper, name, async_to_sync(method))
```
```
def make_sync(_class: type[T]) -> Any:
    """Wraps the methods of the given model class so that they can be called without `await`."""

    class ModelWrapper(_class):  # type: ignore
        _instance_is_sync: bool = True

    def generator_wrapper(
        func: Callable[_P, AsyncGenerator[_G, None]], /, *args: Any, **kwargs: Any
    ) -> Callable[_P, list[_G]]:
        def new_func(*fargs: Any, **fkwargs: Any) -> list[_G]:
            return asyncio.run(_async_gen_to_list(func(*fargs, **fkwargs)))

        return new_func

    for name, method in _class.__dict__.items():
        # Only wrap async public methods
        if inspect.isasyncgenfunction(method):
            setattr(ModelWrapper, name, generator_wrapper(method) if name.startswith("list") else method)
        elif asyncio.iscoroutinefunction(method) and not name.startswith("_"):
            setattr(ModelWrapper, name, async_to_sync(method))

    return ModelWrapper
```
===== 17 =====
```
     for name, method in _class.__dict__.items():
         # Only wrap async public methods
         if inspect.isasyncgenfunction(method):
-            setattr(ModelWrapper, name, generator_wrapper(method))
+            setattr(ModelWrapper, name, lambda *args, **kwargs: asyncio.run(method(*args, **kwargs)))
         elif asyncio.iscoroutinefunction(method) and not name.startswith("_"):
             setattr(ModelWrapper, name, async_to_sync(method))
```
```
def make_sync(_class: type[T]) -> Any:
    """Wraps the methods of the given model class so that they can be called without `await`."""

    class ModelWrapper(_class):  # type: ignore
        _instance_is_sync: bool = True

    def generator_wrapper(
        func: Callable[_P, AsyncGenerator[_G, None]], /, *args: Any, **kwargs: Any
    ) -> Callable[_P, list[_G]]:
        def new_func(*fargs: Any, **fkwargs: Any) -> list[_G]:
            return asyncio.run(_async_gen_to_list(func(*fargs, **fkwargs)))

        return new_func

    for name, method in _class.__dict__.items():
        # Only wrap async public methods
        if inspect.isasyncgenfunction(method):
            setattr(ModelWrapper, name, lambda *args, **kwargs: asyncio.run(method(*args, **kwargs)))
        elif asyncio.iscoroutinefunction(method) and not name.startswith("_"):
            setattr(ModelWrapper, name, async_to_sync(method))

    return ModelWrapper
```
===== 18 =====
```
     for name, method in _class.__dict__.items():
         # Only wrap async public methods
         if inspect.isasyncgenfunction(method):
-            setattr(ModelWrapper, name, generator_wrapper(method))
+            setattr(ModelWrapper, name, lambda *fargs, **fkwargs: generator_wrapper(method)(*fargs, **fkwargs))
         elif asyncio.iscoroutinefunction(method) and not name.startswith("_"):
             setattr(ModelWrapper, name, async_to_sync(method))
```
```
def make_sync(_class: type[T]) -> Any:
    """Wraps the methods of the given model class so that they can be called without `await`."""

    class ModelWrapper(_class):  # type: ignore
        _instance_is_sync: bool = True

    def generator_wrapper(
        func: Callable[_P, AsyncGenerator[_G, None]], /, *args: Any, **kwargs: Any
    ) -> Callable[_P, list[_G]]:
        def new_func(*fargs: Any, **fkwargs: Any) -> list[_G]:
            return asyncio.run(_async_gen_to_list(func(*fargs, **fkwargs)))

        return new_func

    for name, method in _class.__dict__.items():
        # Only wrap async public methods
        if inspect.isasyncgenfunction(method):
            setattr(ModelWrapper, name, lambda *fargs, **fkwargs: generator_wrapper(method)(*fargs, **fkwargs))
        elif asyncio.iscoroutinefunction(method) and not name.startswith("_"):
            setattr(ModelWrapper, name, async_to_sync(method))

    return ModelWrapper
```
===== 19 =====
```
         # Only wrap async public methods
         if inspect.isasyncgenfunction(method):
             setattr(ModelWrapper, name, generator_wrapper(method))
-        elif asyncio.iscoroutinefunction(method) and not name.startswith("_"):
+        elif asyncio.iscoroutinefunction(None) and not name.startswith("_"):
             setattr(ModelWrapper, name, async_to_sync(method))
 
-    return ModelWrapper+    return ModelWrapper
```
```
def make_sync(_class: type[T]) -> Any:
    """Wraps the methods of the given model class so that they can be called without `await`."""

    class ModelWrapper(_class):  # type: ignore
        _instance_is_sync: bool = True

    def generator_wrapper(
        func: Callable[_P, AsyncGenerator[_G, None]], /, *args: Any, **kwargs: Any
    ) -> Callable[_P, list[_G]]:
        def new_func(*fargs: Any, **fkwargs: Any) -> list[_G]:
            return asyncio.run(_async_gen_to_list(func(*fargs, **fkwargs)))

        return new_func

    for name, method in _class.__dict__.items():
        # Only wrap async public methods
        if inspect.isasyncgenfunction(method):
            setattr(ModelWrapper, name, generator_wrapper(method))
        elif asyncio.iscoroutinefunction(None) and not name.startswith("_"):
            setattr(ModelWrapper, name, async_to_sync(method))

    return ModelWrapper

```
===== 20 =====
```
         # Only wrap async public methods
         if inspect.isasyncgenfunction(method):
             setattr(ModelWrapper, name, generator_wrapper(method))
-        elif asyncio.iscoroutinefunction(method) and not name.startswith("_"):
+        elif asyncio.iscoroutinefunction(method) and name == "list":
             setattr(ModelWrapper, name, async_to_sync(method))
 
     return ModelWrapper
```
```
def make_sync(_class: type[T]) -> Any:
    """Wraps the methods of the given model class so that they can be called without `await`."""

    class ModelWrapper(_class):  # type: ignore
        _instance_is_sync: bool = True

    def generator_wrapper(
        func: Callable[_P, AsyncGenerator[_G, None]], /, *args: Any, **kwargs: Any
    ) -> Callable[_P, list[_G]]:
        def new_func(*fargs: Any, **fkwargs: Any) -> list[_G]:
            return asyncio.run(_async_gen_to_list(func(*fargs, **fkwargs)))

        return new_func

    for name, method in _class.__dict__.items():
        # Only wrap async public methods
        if inspect.isasyncgenfunction(method):
            setattr(ModelWrapper, name, generator_wrapper(method))
        elif asyncio.iscoroutinefunction(method) and name == "list":
            setattr(ModelWrapper, name, async_to_sync(method))

    return ModelWrapper
```
===== 21 =====
```
         # Only wrap async public methods
         if inspect.isasyncgenfunction(method):
             setattr(ModelWrapper, name, generator_wrapper(method))
-        elif asyncio.iscoroutinefunction(method) and not name.startswith("_"):
+        elif asyncio.iscoroutinefunction(method) and name.endswith("_"):
             setattr(ModelWrapper, name, async_to_sync(method))
 
     return ModelWrapper
```
```
def make_sync(_class: type[T]) -> Any:
    """Wraps the methods of the given model class so that they can be called without `await`."""

    class ModelWrapper(_class):  # type: ignore
        _instance_is_sync: bool = True

    def generator_wrapper(
        func: Callable[_P, AsyncGenerator[_G, None]], /, *args: Any, **kwargs: Any
    ) -> Callable[_P, list[_G]]:
        def new_func(*fargs: Any, **fkwargs: Any) -> list[_G]:
            return asyncio.run(_async_gen_to_list(func(*fargs, **fkwargs)))

        return new_func

    for name, method in _class.__dict__.items():
        # Only wrap async public methods
        if inspect.isasyncgenfunction(method):
            setattr(ModelWrapper, name, generator_wrapper(method))
        elif asyncio.iscoroutinefunction(method) and name.endswith("_"):
            setattr(ModelWrapper, name, async_to_sync(method))

    return ModelWrapper
```
===== 22 =====
```
         # Only wrap async public methods
         if inspect.isasyncgenfunction(method):
             setattr(ModelWrapper, name, generator_wrapper(method))
-        elif asyncio.iscoroutinefunction(method) and not name.startswith("_"):
+        elif asyncio.iscoroutinefunction(method) and name.startswith("_"):
             setattr(ModelWrapper, name, async_to_sync(method))
 
     return ModelWrapper
```
```
def make_sync(_class: type[T]) -> Any:
    """Wraps the methods of the given model class so that they can be called without `await`."""

    class ModelWrapper(_class):  # type: ignore
        _instance_is_sync: bool = True

    def generator_wrapper(
        func: Callable[_P, AsyncGenerator[_G, None]], /, *args: Any, **kwargs: Any
    ) -> Callable[_P, list[_G]]:
        def new_func(*fargs: Any, **fkwargs: Any) -> list[_G]:
            return asyncio.run(_async_gen_to_list(func(*fargs, **fkwargs)))

        return new_func

    for name, method in _class.__dict__.items():
        # Only wrap async public methods
        if inspect.isasyncgenfunction(method):
            setattr(ModelWrapper, name, generator_wrapper(method))
        elif asyncio.iscoroutinefunction(method) and name.startswith("_"):
            setattr(ModelWrapper, name, async_to_sync(method))

    return ModelWrapper
```
===== 23 =====
```
         # Only wrap async public methods
         if inspect.isasyncgenfunction(method):
             setattr(ModelWrapper, name, generator_wrapper(method))
-        elif asyncio.iscoroutinefunction(method) and not name.startswith("_"):
+        elif asyncio.iscoroutinefunction(method) and name.startswith("_"):
             setattr(ModelWrapper, name, async_to_sync(method))
 
-    return ModelWrapper+    return ModelWrapper
```
```
def make_sync(_class: type[T]) -> Any:
    """Wraps the methods of the given model class so that they can be called without `await`."""

    class ModelWrapper(_class):  # type: ignore
        _instance_is_sync: bool = True

    def generator_wrapper(
        func: Callable[_P, AsyncGenerator[_G, None]], /, *args: Any, **kwargs: Any
    ) -> Callable[_P, list[_G]]:
        def new_func(*fargs: Any, **fkwargs: Any) -> list[_G]:
            return asyncio.run(_async_gen_to_list(func(*fargs, **fkwargs)))

        return new_func

    for name, method in _class.__dict__.items():
        # Only wrap async public methods
        if inspect.isasyncgenfunction(method):
            setattr(ModelWrapper, name, generator_wrapper(method))
        elif asyncio.iscoroutinefunction(method) and name.startswith("_"):
            setattr(ModelWrapper, name, async_to_sync(method))

    return ModelWrapper

```
===== 24 =====
```
         # Only wrap async public methods
         if inspect.isasyncgenfunction(method):
             setattr(ModelWrapper, name, generator_wrapper(method))
-        elif asyncio.iscoroutinefunction(method) and not name.startswith("_"):
+        elif asyncio.iscoroutinefunction(method) or not name.startswith("_"):
             setattr(ModelWrapper, name, async_to_sync(method))
 
-    return ModelWrapper+    return ModelWrapper
```
```
def make_sync(_class: type[T]) -> Any:
    """Wraps the methods of the given model class so that they can be called without `await`."""

    class ModelWrapper(_class):  # type: ignore
        _instance_is_sync: bool = True

    def generator_wrapper(
        func: Callable[_P, AsyncGenerator[_G, None]], /, *args: Any, **kwargs: Any
    ) -> Callable[_P, list[_G]]:
        def new_func(*fargs: Any, **fkwargs: Any) -> list[_G]:
            return asyncio.run(_async_gen_to_list(func(*fargs, **fkwargs)))

        return new_func

    for name, method in _class.__dict__.items():
        # Only wrap async public methods
        if inspect.isasyncgenfunction(method):
            setattr(ModelWrapper, name, generator_wrapper(method))
        elif asyncio.iscoroutinefunction(method) or not name.startswith("_"):
            setattr(ModelWrapper, name, async_to_sync(method))

    return ModelWrapper

```
===== 25 =====
```
         # Only wrap async public methods
         if inspect.isasyncgenfunction(method):
             setattr(ModelWrapper, name, generator_wrapper(method))
-        elif asyncio.iscoroutinefunction(method) and not name.startswith("_"):
+        elif not asyncio.iscoroutinefunction(method):
             setattr(ModelWrapper, name, async_to_sync(method))
 
     return ModelWrapper
```
```
def make_sync(_class: type[T]) -> Any:
    """Wraps the methods of the given model class so that they can be called without `await`."""

    class ModelWrapper(_class):  # type: ignore
        _instance_is_sync: bool = True

    def generator_wrapper(
        func: Callable[_P, AsyncGenerator[_G, None]], /, *args: Any, **kwargs: Any
    ) -> Callable[_P, list[_G]]:
        def new_func(*fargs: Any, **fkwargs: Any) -> list[_G]:
            return asyncio.run(_async_gen_to_list(func(*fargs, **fkwargs)))

        return new_func

    for name, method in _class.__dict__.items():
        # Only wrap async public methods
        if inspect.isasyncgenfunction(method):
            setattr(ModelWrapper, name, generator_wrapper(method))
        elif not asyncio.iscoroutinefunction(method):
            setattr(ModelWrapper, name, async_to_sync(method))

    return ModelWrapper
```
===== 26 =====
```
         if inspect.isasyncgenfunction(method):
             setattr(ModelWrapper, name, generator_wrapper(method))
         elif asyncio.iscoroutinefunction(method) and not name.startswith("_"):
-            setattr(ModelWrapper, name, async_to_sync(method))
+            setattr(ModelWrapper, name, None)
 
-    return ModelWrapper+    return ModelWrapper
```
```
def make_sync(_class: type[T]) -> Any:
    """Wraps the methods of the given model class so that they can be called without `await`."""

    class ModelWrapper(_class):  # type: ignore
        _instance_is_sync: bool = True

    def generator_wrapper(
        func: Callable[_P, AsyncGenerator[_G, None]], /, *args: Any, **kwargs: Any
    ) -> Callable[_P, list[_G]]:
        def new_func(*fargs: Any, **fkwargs: Any) -> list[_G]:
            return asyncio.run(_async_gen_to_list(func(*fargs, **fkwargs)))

        return new_func

    for name, method in _class.__dict__.items():
        # Only wrap async public methods
        if inspect.isasyncgenfunction(method):
            setattr(ModelWrapper, name, generator_wrapper(method))
        elif asyncio.iscoroutinefunction(method) and not name.startswith("_"):
            setattr(ModelWrapper, name, None)

    return ModelWrapper

```
===== 27 =====
```
         if inspect.isasyncgenfunction(method):
             setattr(ModelWrapper, name, generator_wrapper(method))
         elif asyncio.iscoroutinefunction(method) and not name.startswith("_"):
-            setattr(ModelWrapper, name, async_to_sync(method))
+            setattr(ModelWrapper, name, async_to_sync(None))
 
-    return ModelWrapper+    return ModelWrapper
```
```
def make_sync(_class: type[T]) -> Any:
    """Wraps the methods of the given model class so that they can be called without `await`."""

    class ModelWrapper(_class):  # type: ignore
        _instance_is_sync: bool = True

    def generator_wrapper(
        func: Callable[_P, AsyncGenerator[_G, None]], /, *args: Any, **kwargs: Any
    ) -> Callable[_P, list[_G]]:
        def new_func(*fargs: Any, **fkwargs: Any) -> list[_G]:
            return asyncio.run(_async_gen_to_list(func(*fargs, **fkwargs)))

        return new_func

    for name, method in _class.__dict__.items():
        # Only wrap async public methods
        if inspect.isasyncgenfunction(method):
            setattr(ModelWrapper, name, generator_wrapper(method))
        elif asyncio.iscoroutinefunction(method) and not name.startswith("_"):
            setattr(ModelWrapper, name, async_to_sync(None))

    return ModelWrapper

```
===== 28 =====
```
         if inspect.isasyncgenfunction(method):
             setattr(ModelWrapper, name, generator_wrapper(method))
         elif asyncio.iscoroutinefunction(method) and not name.startswith("_"):
-            setattr(ModelWrapper, name, async_to_sync(method))
+            setattr(ModelWrapper, name, async_to_sync(method) if name == "get" else method)
 
     return ModelWrapper
```
```
def make_sync(_class: type[T]) -> Any:
    """Wraps the methods of the given model class so that they can be called without `await`."""

    class ModelWrapper(_class):  # type: ignore
        _instance_is_sync: bool = True

    def generator_wrapper(
        func: Callable[_P, AsyncGenerator[_G, None]], /, *args: Any, **kwargs: Any
    ) -> Callable[_P, list[_G]]:
        def new_func(*fargs: Any, **fkwargs: Any) -> list[_G]:
            return asyncio.run(_async_gen_to_list(func(*fargs, **fkwargs)))

        return new_func

    for name, method in _class.__dict__.items():
        # Only wrap async public methods
        if inspect.isasyncgenfunction(method):
            setattr(ModelWrapper, name, generator_wrapper(method))
        elif asyncio.iscoroutinefunction(method) and not name.startswith("_"):
            setattr(ModelWrapper, name, async_to_sync(method) if name == "get" else method)

    return ModelWrapper
```
===== 29 =====
```
         if inspect.isasyncgenfunction(method):
             setattr(ModelWrapper, name, generator_wrapper(method))
         elif asyncio.iscoroutinefunction(method) and not name.startswith("_"):
-            setattr(ModelWrapper, name, async_to_sync(method))
+            setattr(ModelWrapper, name, async_to_sync(method) if name.startswith("get") else method)
 
     return ModelWrapper
```
```
def make_sync(_class: type[T]) -> Any:
    """Wraps the methods of the given model class so that they can be called without `await`."""

    class ModelWrapper(_class):  # type: ignore
        _instance_is_sync: bool = True

    def generator_wrapper(
        func: Callable[_P, AsyncGenerator[_G, None]], /, *args: Any, **kwargs: Any
    ) -> Callable[_P, list[_G]]:
        def new_func(*fargs: Any, **fkwargs: Any) -> list[_G]:
            return asyncio.run(_async_gen_to_list(func(*fargs, **fkwargs)))

        return new_func

    for name, method in _class.__dict__.items():
        # Only wrap async public methods
        if inspect.isasyncgenfunction(method):
            setattr(ModelWrapper, name, generator_wrapper(method))
        elif asyncio.iscoroutinefunction(method) and not name.startswith("_"):
            setattr(ModelWrapper, name, async_to_sync(method) if name.startswith("get") else method)

    return ModelWrapper
```
===== 30 =====
```
         if inspect.isasyncgenfunction(method):
             setattr(ModelWrapper, name, generator_wrapper(method))
         elif asyncio.iscoroutinefunction(method) and not name.startswith("_"):
-            setattr(ModelWrapper, name, async_to_sync(method))
+            setattr(ModelWrapper, name, lambda *args, **kwargs: method(*args, **kwargs))
 
     return ModelWrapper
```
```
def make_sync(_class: type[T]) -> Any:
    """Wraps the methods of the given model class so that they can be called without `await`."""

    class ModelWrapper(_class):  # type: ignore
        _instance_is_sync: bool = True

    def generator_wrapper(
        func: Callable[_P, AsyncGenerator[_G, None]], /, *args: Any, **kwargs: Any
    ) -> Callable[_P, list[_G]]:
        def new_func(*fargs: Any, **fkwargs: Any) -> list[_G]:
            return asyncio.run(_async_gen_to_list(func(*fargs, **fkwargs)))

        return new_func

    for name, method in _class.__dict__.items():
        # Only wrap async public methods
        if inspect.isasyncgenfunction(method):
            setattr(ModelWrapper, name, generator_wrapper(method))
        elif asyncio.iscoroutinefunction(method) and not name.startswith("_"):
            setattr(ModelWrapper, name, lambda *args, **kwargs: method(*args, **kwargs))

    return ModelWrapper
```
===== 31 =====
```
         if inspect.isasyncgenfunction(method):
             setattr(ModelWrapper, name, generator_wrapper(method))
         elif asyncio.iscoroutinefunction(method) and not name.startswith("_"):
-            setattr(ModelWrapper, name, async_to_sync(method))
+            setattr(ModelWrapper, name, method)  # Directly assigning the method without wrapping
 
     return ModelWrapper
```
```
def make_sync(_class: type[T]) -> Any:
    """Wraps the methods of the given model class so that they can be called without `await`."""

    class ModelWrapper(_class):  # type: ignore
        _instance_is_sync: bool = True

    def generator_wrapper(
        func: Callable[_P, AsyncGenerator[_G, None]], /, *args: Any, **kwargs: Any
    ) -> Callable[_P, list[_G]]:
        def new_func(*fargs: Any, **fkwargs: Any) -> list[_G]:
            return asyncio.run(_async_gen_to_list(func(*fargs, **fkwargs)))

        return new_func

    for name, method in _class.__dict__.items():
        # Only wrap async public methods
        if inspect.isasyncgenfunction(method):
            setattr(ModelWrapper, name, generator_wrapper(method))
        elif asyncio.iscoroutinefunction(method) and not name.startswith("_"):
            setattr(ModelWrapper, name, method)  # Directly assigning the method without wrapping

    return ModelWrapper
```
