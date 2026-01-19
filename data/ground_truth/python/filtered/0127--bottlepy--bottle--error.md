https://github.com/bottlepy/bottle/blob/3d0ace47fe8e5ac5177b49597bd8ff872ff08d7b/./bottle.py#L915-L935
```
🈚️

local crash
wrong originally

@icontract.snapshot(lambda self: dict(self.error_handler), name="old_error_handler")
@icontract.ensure(
    lambda self, code, callback, result, OLD:
        (
            # 分支1：callback 为真值 => 直接注册 handler
            callback
            and
            (lambda code_int, base_handler:
                (lambda expected_cb:
                    # 在 base_handler 上按“正确逻辑”写入期望的 handler
                    (base_handler.update({code_int: expected_cb}) or True)
                    # 然后比较：返回值和 error_handler 都必须与期望一致
                    and result is expected_cb
                    and self.error_handler == base_handler
                )(load(callback) if isinstance(callback, str) else callback)
            )(int(code), dict(OLD.old_error_handler))
        )
        or
        (
            # 分支2：callback 为假值 => 只返回 decorator，不改动 error_handler
            (not callback)
            and self.error_handler == OLD.old_error_handler
            and callable(result)
        )
)
```
```
None
```
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
===== 0 =====
```
         """
 
         def decorator(callback):
-            if isinstance(callback, str): callback = load(callback)
+            if isinstance(callback, ): callback = load(callback)
             self.error_handler[int(code)] = callback
             return callback
 
-        return decorator(callback) if callback else decorator+        return decorator(callback) if callback else decorator
```
```
    def error(self, code=500, callback=None):
        """ Register an output handler for a HTTP error code. Can
            be used as a decorator or called directly ::

                def error_handler_500(error):
                    return 'error_handler_500'

                app.error(code=500, callback=error_handler_500)

                @app.error(404)
                def error_handler_404(error):
                    return 'error_handler_404'

        """

        def decorator(callback):
            if isinstance(callback, ): callback = load(callback)
            self.error_handler[int(code)] = callback
            return callback

        return decorator(callback) if callback else decorator

```
===== 1 =====
```
         """
 
         def decorator(callback):
-            if isinstance(callback, str): callback = load(callback)
+            if isinstance(callback, None): callback = load(callback)
             self.error_handler[int(code)] = callback
             return callback
 
-        return decorator(callback) if callback else decorator+        return decorator(callback) if callback else decorator
```
```
    def error(self, code=500, callback=None):
        """ Register an output handler for a HTTP error code. Can
            be used as a decorator or called directly ::

                def error_handler_500(error):
                    return 'error_handler_500'

                app.error(code=500, callback=error_handler_500)

                @app.error(404)
                def error_handler_404(error):
                    return 'error_handler_404'

        """

        def decorator(callback):
            if isinstance(callback, None): callback = load(callback)
            self.error_handler[int(code)] = callback
            return callback

        return decorator(callback) if callback else decorator

```
===== 2 =====
```
         """
 
         def decorator(callback):
-            if isinstance(callback, str): callback = load(callback)
+            if isinstance(str): callback = load(callback)
             self.error_handler[int(code)] = callback
             return callback
 
-        return decorator(callback) if callback else decorator+        return decorator(callback) if callback else decorator
```
```
    def error(self, code=500, callback=None):
        """ Register an output handler for a HTTP error code. Can
            be used as a decorator or called directly ::

                def error_handler_500(error):
                    return 'error_handler_500'

                app.error(code=500, callback=error_handler_500)

                @app.error(404)
                def error_handler_404(error):
                    return 'error_handler_404'

        """

        def decorator(callback):
            if isinstance(str): callback = load(callback)
            self.error_handler[int(code)] = callback
            return callback

        return decorator(callback) if callback else decorator

```
===== 3 =====
```
 
         def decorator(callback):
             if isinstance(callback, str): callback = load(callback)
-            self.error_handler[int(code)] = callback
+            self.error_handler[int(None)] = callback
             return callback
 
-        return decorator(callback) if callback else decorator+        return decorator(callback) if callback else decorator
```
```
    def error(self, code=500, callback=None):
        """ Register an output handler for a HTTP error code. Can
            be used as a decorator or called directly ::

                def error_handler_500(error):
                    return 'error_handler_500'

                app.error(code=500, callback=error_handler_500)

                @app.error(404)
                def error_handler_404(error):
                    return 'error_handler_404'

        """

        def decorator(callback):
            if isinstance(callback, str): callback = load(callback)
            self.error_handler[int(None)] = callback
            return callback

        return decorator(callback) if callback else decorator

```
===== 4 =====
```
 
         def decorator(callback):
             if isinstance(callback, str): callback = load(callback)
-            self.error_handler[int(code)] = callback
+            self.error_handler[int(code)] = None
             return callback
 
-        return decorator(callback) if callback else decorator+        return decorator(callback) if callback else decorator
```
```
    def error(self, code=500, callback=None):
        """ Register an output handler for a HTTP error code. Can
            be used as a decorator or called directly ::

                def error_handler_500(error):
                    return 'error_handler_500'

                app.error(code=500, callback=error_handler_500)

                @app.error(404)
                def error_handler_404(error):
                    return 'error_handler_404'

        """

        def decorator(callback):
            if isinstance(callback, str): callback = load(callback)
            self.error_handler[int(code)] = None
            return callback

        return decorator(callback) if callback else decorator

```
===== 5 =====
```
 
         def decorator(callback):
             if isinstance(callback, str): callback = load(callback)
-            self.error_handler[int(code)] = callback
+            self.error_handler[int(code)] = None  # Incorrect: assigns None instead of the callback, causing handlers to fail.
             return callback
 
         return decorator(callback) if callback else decorator
```
```
    def error(self, code=500, callback=None):
        """ Register an output handler for a HTTP error code. Can
            be used as a decorator or called directly ::

                def error_handler_500(error):
                    return 'error_handler_500'

                app.error(code=500, callback=error_handler_500)

                @app.error(404)
                def error_handler_404(error):
                    return 'error_handler_404'

        """

        def decorator(callback):
            if isinstance(callback, str): callback = load(callback)
            self.error_handler[int(code)] = None  # Incorrect: assigns None instead of the callback, causing handlers to fail.
            return callback

        return decorator(callback) if callback else decorator
```
===== 6 =====
```
 
         def decorator(callback):
             if isinstance(callback, str): callback = load(callback)
-            self.error_handler[int(code)] = callback
+            self.error_handler[int(code)] = callback if code != 500 else None  # Incorrect: skips setting the handler for 500 errors.
             return callback
 
         return decorator(callback) if callback else decorator
```
```
    def error(self, code=500, callback=None):
        """ Register an output handler for a HTTP error code. Can
            be used as a decorator or called directly ::

                def error_handler_500(error):
                    return 'error_handler_500'

                app.error(code=500, callback=error_handler_500)

                @app.error(404)
                def error_handler_404(error):
                    return 'error_handler_404'

        """

        def decorator(callback):
            if isinstance(callback, str): callback = load(callback)
            self.error_handler[int(code)] = callback if code != 500 else None  # Incorrect: skips setting the handler for 500 errors.
            return callback

        return decorator(callback) if callback else decorator
```
===== 7 =====
```
             self.error_handler[int(code)] = callback
             return callback
 
-        return decorator(callback) if callback else decorator+        return decorator(None) if callback else decorator
```
```
    def error(self, code=500, callback=None):
        """ Register an output handler for a HTTP error code. Can
            be used as a decorator or called directly ::

                def error_handler_500(error):
                    return 'error_handler_500'

                app.error(code=500, callback=error_handler_500)

                @app.error(404)
                def error_handler_404(error):
                    return 'error_handler_404'

        """

        def decorator(callback):
            if isinstance(callback, str): callback = load(callback)
            self.error_handler[int(code)] = callback
            return callback

        return decorator(None) if callback else decorator

```
===== 8 =====
```
             self.error_handler[int(code)] = callback
             return callback
 
-        return decorator(callback) if callback else decorator+        return decorator(callback) if callback == '' else decorator
```
```
    def error(self, code=500, callback=None):
        """ Register an output handler for a HTTP error code. Can
            be used as a decorator or called directly ::

                def error_handler_500(error):
                    return 'error_handler_500'

                app.error(code=500, callback=error_handler_500)

                @app.error(404)
                def error_handler_404(error):
                    return 'error_handler_404'

        """

        def decorator(callback):
            if isinstance(callback, str): callback = load(callback)
            self.error_handler[int(code)] = callback
            return callback

        return decorator(callback) if callback == '' else decorator
```
===== 9 =====
```
             self.error_handler[int(code)] = callback
             return callback
 
-        return decorator(callback) if callback else decorator+        return decorator(callback) if callback and isinstance(callback, dict) else decorator
```
```
    def error(self, code=500, callback=None):
        """ Register an output handler for a HTTP error code. Can
            be used as a decorator or called directly ::

                def error_handler_500(error):
                    return 'error_handler_500'

                app.error(code=500, callback=error_handler_500)

                @app.error(404)
                def error_handler_404(error):
                    return 'error_handler_404'

        """

        def decorator(callback):
            if isinstance(callback, str): callback = load(callback)
            self.error_handler[int(code)] = callback
            return callback

        return decorator(callback) if callback and isinstance(callback, dict) else decorator
```
===== 10 =====
```
             self.error_handler[int(code)] = callback
             return callback
 
-        return decorator(callback) if callback else decorator+        return decorator(callback) if callback is None else decorator
```
```
    def error(self, code=500, callback=None):
        """ Register an output handler for a HTTP error code. Can
            be used as a decorator or called directly ::

                def error_handler_500(error):
                    return 'error_handler_500'

                app.error(code=500, callback=error_handler_500)

                @app.error(404)
                def error_handler_404(error):
                    return 'error_handler_404'

        """

        def decorator(callback):
            if isinstance(callback, str): callback = load(callback)
            self.error_handler[int(code)] = callback
            return callback

        return decorator(callback) if callback is None else decorator
```
===== 11 =====
```
             self.error_handler[int(code)] = callback
             return callback
 
-        return decorator(callback) if callback else decorator+        return decorator(callback) if isinstance(callback, str) else decorator
```
```
    def error(self, code=500, callback=None):
        """ Register an output handler for a HTTP error code. Can
            be used as a decorator or called directly ::

                def error_handler_500(error):
                    return 'error_handler_500'

                app.error(code=500, callback=error_handler_500)

                @app.error(404)
                def error_handler_404(error):
                    return 'error_handler_404'

        """

        def decorator(callback):
            if isinstance(callback, str): callback = load(callback)
            self.error_handler[int(code)] = callback
            return callback

        return decorator(callback) if isinstance(callback, str) else decorator
```
===== 12 =====
```
             self.error_handler[int(code)] = callback
             return callback
 
-        return decorator(callback) if callback else decorator+        return decorator(callback) if not callback else decorator
```
```
    def error(self, code=500, callback=None):
        """ Register an output handler for a HTTP error code. Can
            be used as a decorator or called directly ::

                def error_handler_500(error):
                    return 'error_handler_500'

                app.error(code=500, callback=error_handler_500)

                @app.error(404)
                def error_handler_404(error):
                    return 'error_handler_404'

        """

        def decorator(callback):
            if isinstance(callback, str): callback = load(callback)
            self.error_handler[int(code)] = callback
            return callback

        return decorator(callback) if not callback else decorator
```
