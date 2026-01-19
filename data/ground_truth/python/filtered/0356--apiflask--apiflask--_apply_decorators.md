https://github.com/apiflask/apiflask/blob/13d2a1b51a7ec68fdcfb9c6250f2db107fcf359a/./src/apiflask/app.py#L1193-L1212
```
🈚️

return function object
```
```
None
```
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
===== 0 =====
```
         """
 
         def decorator(f):
-            @wraps(f)
+            @wraps(f, assigned=('__dict__',), updated=('__name__',))
             def wrapper(*args, **kwargs):
                 decorated_func = f
                 decorators = self.config[config_name]
```
```
    def _apply_decorators(self, config_name: str):
        """Apply the decorators to the OpenAPI endpoints at runtime.

        Arguments:
            config_name: The config name to get the list of decorators.
        """

        def decorator(f):
            @wraps(f, assigned=('__dict__',), updated=('__name__',))
            def wrapper(*args, **kwargs):
                decorated_func = f
                decorators = self.config[config_name]
                if decorators:
                    for decorator in decorators:
                        decorated_func = decorator(decorated_func)
                return decorated_func(*args, **kwargs)

            return wrapper

        return decorator
```
===== 1 =====
```
         """
 
         def decorator(f):
-            @wraps(f)
+            @wraps(f, updated=('__doc__',))
             def wrapper(*args, **kwargs):
                 decorated_func = f
                 decorators = self.config[config_name]
```
```
    def _apply_decorators(self, config_name: str):
        """Apply the decorators to the OpenAPI endpoints at runtime.

        Arguments:
            config_name: The config name to get the list of decorators.
        """

        def decorator(f):
            @wraps(f, updated=('__doc__',))
            def wrapper(*args, **kwargs):
                decorated_func = f
                decorators = self.config[config_name]
                if decorators:
                    for decorator in decorators:
                        decorated_func = decorator(decorated_func)
                return decorated_func(*args, **kwargs)

            return wrapper

        return decorator
```
===== 2 =====
```
         def decorator(f):
             @wraps(f)
             def wrapper(*args, **kwargs):
-                decorated_func = f
+                decorated_func = None
                 decorators = self.config[config_name]
                 if decorators:
                     for decorator in decorators:
@@ -17,4 +17,4 @@ 
             return wrapper
 
-        return decorator+        return decorator
```
```
    def _apply_decorators(self, config_name: str):
        """Apply the decorators to the OpenAPI endpoints at runtime.

        Arguments:
            config_name: The config name to get the list of decorators.
        """

        def decorator(f):
            @wraps(f)
            def wrapper(*args, **kwargs):
                decorated_func = None
                decorators = self.config[config_name]
                if decorators:
                    for decorator in decorators:
                        decorated_func = decorator(decorated_func)
                return decorated_func(*args, **kwargs)

            return wrapper

        return decorator

```
===== 3 =====
```
             @wraps(f)
             def wrapper(*args, **kwargs):
                 decorated_func = f
-                decorators = self.config[config_name]
+                decorators = None
                 if decorators:
                     for decorator in decorators:
                         decorated_func = decorator(decorated_func)
@@ -17,4 +17,4 @@ 
             return wrapper
 
-        return decorator+        return decorator
```
```
    def _apply_decorators(self, config_name: str):
        """Apply the decorators to the OpenAPI endpoints at runtime.

        Arguments:
            config_name: The config name to get the list of decorators.
        """

        def decorator(f):
            @wraps(f)
            def wrapper(*args, **kwargs):
                decorated_func = f
                decorators = None
                if decorators:
                    for decorator in decorators:
                        decorated_func = decorator(decorated_func)
                return decorated_func(*args, **kwargs)

            return wrapper

        return decorator

```
===== 4 =====
```
             def wrapper(*args, **kwargs):
                 decorated_func = f
                 decorators = self.config[config_name]
-                if decorators:
+                if decorators and False:
                     for decorator in decorators:
                         decorated_func = decorator(decorated_func)
                 return decorated_func(*args, **kwargs)
```
```
    def _apply_decorators(self, config_name: str):
        """Apply the decorators to the OpenAPI endpoints at runtime.

        Arguments:
            config_name: The config name to get the list of decorators.
        """

        def decorator(f):
            @wraps(f)
            def wrapper(*args, **kwargs):
                decorated_func = f
                decorators = self.config[config_name]
                if decorators and False:
                    for decorator in decorators:
                        decorated_func = decorator(decorated_func)
                return decorated_func(*args, **kwargs)

            return wrapper

        return decorator
```
===== 5 =====
```
             def wrapper(*args, **kwargs):
                 decorated_func = f
                 decorators = self.config[config_name]
-                if decorators:
+                if decorators is None:
                     for decorator in decorators:
                         decorated_func = decorator(decorated_func)
                 return decorated_func(*args, **kwargs)
```
```
    def _apply_decorators(self, config_name: str):
        """Apply the decorators to the OpenAPI endpoints at runtime.

        Arguments:
            config_name: The config name to get the list of decorators.
        """

        def decorator(f):
            @wraps(f)
            def wrapper(*args, **kwargs):
                decorated_func = f
                decorators = self.config[config_name]
                if decorators is None:
                    for decorator in decorators:
                        decorated_func = decorator(decorated_func)
                return decorated_func(*args, **kwargs)

            return wrapper

        return decorator
```
===== 6 =====
```
             def wrapper(*args, **kwargs):
                 decorated_func = f
                 decorators = self.config[config_name]
-                if decorators:
+                if len(decorators) == 0:
                     for decorator in decorators:
                         decorated_func = decorator(decorated_func)
                 return decorated_func(*args, **kwargs)
```
```
    def _apply_decorators(self, config_name: str):
        """Apply the decorators to the OpenAPI endpoints at runtime.

        Arguments:
            config_name: The config name to get the list of decorators.
        """

        def decorator(f):
            @wraps(f)
            def wrapper(*args, **kwargs):
                decorated_func = f
                decorators = self.config[config_name]
                if len(decorators) == 0:
                    for decorator in decorators:
                        decorated_func = decorator(decorated_func)
                return decorated_func(*args, **kwargs)

            return wrapper

        return decorator
```
===== 7 =====
```
             def wrapper(*args, **kwargs):
                 decorated_func = f
                 decorators = self.config[config_name]
-                if decorators:
+                if not decorators:
                     for decorator in decorators:
                         decorated_func = decorator(decorated_func)
                 return decorated_func(*args, **kwargs)
```
```
    def _apply_decorators(self, config_name: str):
        """Apply the decorators to the OpenAPI endpoints at runtime.

        Arguments:
            config_name: The config name to get the list of decorators.
        """

        def decorator(f):
            @wraps(f)
            def wrapper(*args, **kwargs):
                decorated_func = f
                decorators = self.config[config_name]
                if not decorators:
                    for decorator in decorators:
                        decorated_func = decorator(decorated_func)
                return decorated_func(*args, **kwargs)

            return wrapper

        return decorator
```
===== 8 =====
```
                 decorators = self.config[config_name]
                 if decorators:
                     for decorator in decorators:
-                        decorated_func = decorator(decorated_func)
+                        decorated_func = None
                 return decorated_func(*args, **kwargs)
 
             return wrapper
 
-        return decorator+        return decorator
```
```
    def _apply_decorators(self, config_name: str):
        """Apply the decorators to the OpenAPI endpoints at runtime.

        Arguments:
            config_name: The config name to get the list of decorators.
        """

        def decorator(f):
            @wraps(f)
            def wrapper(*args, **kwargs):
                decorated_func = f
                decorators = self.config[config_name]
                if decorators:
                    for decorator in decorators:
                        decorated_func = None
                return decorated_func(*args, **kwargs)

            return wrapper

        return decorator

```
===== 9 =====
```
                 decorators = self.config[config_name]
                 if decorators:
                     for decorator in decorators:
-                        decorated_func = decorator(decorated_func)
+                        decorated_func = decorated_func if decorated_func is not None else decorated_func
                 return decorated_func(*args, **kwargs)
 
             return wrapper
```
```
    def _apply_decorators(self, config_name: str):
        """Apply the decorators to the OpenAPI endpoints at runtime.

        Arguments:
            config_name: The config name to get the list of decorators.
        """

        def decorator(f):
            @wraps(f)
            def wrapper(*args, **kwargs):
                decorated_func = f
                decorators = self.config[config_name]
                if decorators:
                    for decorator in decorators:
                        decorated_func = decorated_func if decorated_func is not None else decorated_func
                return decorated_func(*args, **kwargs)

            return wrapper

        return decorator
```
===== 10 =====
```
                 decorators = self.config[config_name]
                 if decorators:
                     for decorator in decorators:
-                        decorated_func = decorator(decorated_func)
+                        decorated_func = decorator(decorated_func) if False else decorated_func
                 return decorated_func(*args, **kwargs)
 
             return wrapper
```
```
    def _apply_decorators(self, config_name: str):
        """Apply the decorators to the OpenAPI endpoints at runtime.

        Arguments:
            config_name: The config name to get the list of decorators.
        """

        def decorator(f):
            @wraps(f)
            def wrapper(*args, **kwargs):
                decorated_func = f
                decorators = self.config[config_name]
                if decorators:
                    for decorator in decorators:
                        decorated_func = decorator(decorated_func) if False else decorated_func
                return decorated_func(*args, **kwargs)

            return wrapper

        return decorator
```
===== 11 =====
```
                 decorators = self.config[config_name]
                 if decorators:
                     for decorator in decorators:
-                        decorated_func = decorator(decorated_func)
+                        decorated_func = decorator(decorated_func) if isinstance(decorated_func, str) else decorated_func
                 return decorated_func(*args, **kwargs)
 
             return wrapper
```
```
    def _apply_decorators(self, config_name: str):
        """Apply the decorators to the OpenAPI endpoints at runtime.

        Arguments:
            config_name: The config name to get the list of decorators.
        """

        def decorator(f):
            @wraps(f)
            def wrapper(*args, **kwargs):
                decorated_func = f
                decorators = self.config[config_name]
                if decorators:
                    for decorator in decorators:
                        decorated_func = decorator(decorated_func) if isinstance(decorated_func, str) else decorated_func
                return decorated_func(*args, **kwargs)

            return wrapper

        return decorator
```
===== 12 =====
```
                 if decorators:
                     for decorator in decorators:
                         decorated_func = decorator(decorated_func)
-                return decorated_func(*args, **kwargs)
+                return decorated_func(*args, **kwargs) and None  # Always returns None regardless of decorated_func's return value, which may lead to loss of the actual return value.
 
             return wrapper
```
```
    def _apply_decorators(self, config_name: str):
        """Apply the decorators to the OpenAPI endpoints at runtime.

        Arguments:
            config_name: The config name to get the list of decorators.
        """

        def decorator(f):
            @wraps(f)
            def wrapper(*args, **kwargs):
                decorated_func = f
                decorators = self.config[config_name]
                if decorators:
                    for decorator in decorators:
                        decorated_func = decorator(decorated_func)
                return decorated_func(*args, **kwargs) and None  # Always returns None regardless of decorated_func's return value, which may lead to loss of the actual return value.

            return wrapper

        return decorator
```
===== 13 =====
```
                 if decorators:
                     for decorator in decorators:
                         decorated_func = decorator(decorated_func)
-                return decorated_func(*args, **kwargs)
+                return decorated_func(*args, **kwargs) if args else None  # Returns None if args is empty, which may not be the intended behavior.
 
             return wrapper
```
```
    def _apply_decorators(self, config_name: str):
        """Apply the decorators to the OpenAPI endpoints at runtime.

        Arguments:
            config_name: The config name to get the list of decorators.
        """

        def decorator(f):
            @wraps(f)
            def wrapper(*args, **kwargs):
                decorated_func = f
                decorators = self.config[config_name]
                if decorators:
                    for decorator in decorators:
                        decorated_func = decorator(decorated_func)
                return decorated_func(*args, **kwargs) if args else None  # Returns None if args is empty, which may not be the intended behavior.

            return wrapper

        return decorator
```
