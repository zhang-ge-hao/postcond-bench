https://github.com/pallets/flask/blob/330123258e8c3dc391cbe55ab1ed94891ca83af3/./src/flask/app.py#L1271-L1296
```
🈚️

function object related

@icontract.ensure(lambda result: True)
```
```
None
```
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31]
===== 0 =====
```
         value is handled as if it was the return value from the view, and
         further request handling is stopped.
         """
-        names = (None, *reversed(request.blueprints))
+        names = (None, *request.blueprints)
 
         for name in names:
             if name in self.url_value_preprocessors:
```
```
    def preprocess_request(self) -> ft.ResponseReturnValue | None:
        """Called before the request is dispatched. Calls
        :attr:`url_value_preprocessors` registered with the app and the
        current blueprint (if any). Then calls :attr:`before_request_funcs`
        registered with the app and the blueprint.

        If any :meth:`before_request` handler returns a non-None value, the
        value is handled as if it was the return value from the view, and
        further request handling is stopped.
        """
        names = (None, *request.blueprints)

        for name in names:
            if name in self.url_value_preprocessors:
                for url_func in self.url_value_preprocessors[name]:
                    url_func(request.endpoint, request.view_args)

        for name in names:
            if name in self.before_request_funcs:
                for before_func in self.before_request_funcs[name]:
                    rv = self.ensure_sync(before_func)()

                    if rv is not None:
                        return rv  # type: ignore[no-any-return]

        return None
```
===== 1 =====
```
         value is handled as if it was the return value from the view, and
         further request handling is stopped.
         """
-        names = (None, *reversed(request.blueprints))
+        names = (None, *request.blueprints, "default")
 
         for name in names:
             if name in self.url_value_preprocessors:
```
```
    def preprocess_request(self) -> ft.ResponseReturnValue | None:
        """Called before the request is dispatched. Calls
        :attr:`url_value_preprocessors` registered with the app and the
        current blueprint (if any). Then calls :attr:`before_request_funcs`
        registered with the app and the blueprint.

        If any :meth:`before_request` handler returns a non-None value, the
        value is handled as if it was the return value from the view, and
        further request handling is stopped.
        """
        names = (None, *request.blueprints, "default")

        for name in names:
            if name in self.url_value_preprocessors:
                for url_func in self.url_value_preprocessors[name]:
                    url_func(request.endpoint, request.view_args)

        for name in names:
            if name in self.before_request_funcs:
                for before_func in self.before_request_funcs[name]:
                    rv = self.ensure_sync(before_func)()

                    if rv is not None:
                        return rv  # type: ignore[no-any-return]

        return None
```
===== 2 =====
```
         """
         names = (None, *reversed(request.blueprints))
 
-        for name in names:
+        for name in self.after_request_funcs:
             if name in self.url_value_preprocessors:
                 for url_func in self.url_value_preprocessors[name]:
                     url_func(request.endpoint, request.view_args)
```
```
    def preprocess_request(self) -> ft.ResponseReturnValue | None:
        """Called before the request is dispatched. Calls
        :attr:`url_value_preprocessors` registered with the app and the
        current blueprint (if any). Then calls :attr:`before_request_funcs`
        registered with the app and the blueprint.

        If any :meth:`before_request` handler returns a non-None value, the
        value is handled as if it was the return value from the view, and
        further request handling is stopped.
        """
        names = (None, *reversed(request.blueprints))

        for name in self.after_request_funcs:
            if name in self.url_value_preprocessors:
                for url_func in self.url_value_preprocessors[name]:
                    url_func(request.endpoint, request.view_args)

        for name in names:
            if name in self.before_request_funcs:
                for before_func in self.before_request_funcs[name]:
                    rv = self.ensure_sync(before_func)()

                    if rv is not None:
                        return rv  # type: ignore[no-any-return]

        return None
```
===== 3 =====
```
         """
         names = (None, *reversed(request.blueprints))
 
-        for name in names:
+        for name in self.shell_context_processors:
             if name in self.url_value_preprocessors:
                 for url_func in self.url_value_preprocessors[name]:
                     url_func(request.endpoint, request.view_args)
```
```
    def preprocess_request(self) -> ft.ResponseReturnValue | None:
        """Called before the request is dispatched. Calls
        :attr:`url_value_preprocessors` registered with the app and the
        current blueprint (if any). Then calls :attr:`before_request_funcs`
        registered with the app and the blueprint.

        If any :meth:`before_request` handler returns a non-None value, the
        value is handled as if it was the return value from the view, and
        further request handling is stopped.
        """
        names = (None, *reversed(request.blueprints))

        for name in self.shell_context_processors:
            if name in self.url_value_preprocessors:
                for url_func in self.url_value_preprocessors[name]:
                    url_func(request.endpoint, request.view_args)

        for name in names:
            if name in self.before_request_funcs:
                for before_func in self.before_request_funcs[name]:
                    rv = self.ensure_sync(before_func)()

                    if rv is not None:
                        return rv  # type: ignore[no-any-return]

        return None
```
===== 4 =====
```
         """
         names = (None, *reversed(request.blueprints))
 
-        for name in names:
+        for name in self.teardown_request_funcs:
             if name in self.url_value_preprocessors:
                 for url_func in self.url_value_preprocessors[name]:
                     url_func(request.endpoint, request.view_args)
```
```
    def preprocess_request(self) -> ft.ResponseReturnValue | None:
        """Called before the request is dispatched. Calls
        :attr:`url_value_preprocessors` registered with the app and the
        current blueprint (if any). Then calls :attr:`before_request_funcs`
        registered with the app and the blueprint.

        If any :meth:`before_request` handler returns a non-None value, the
        value is handled as if it was the return value from the view, and
        further request handling is stopped.
        """
        names = (None, *reversed(request.blueprints))

        for name in self.teardown_request_funcs:
            if name in self.url_value_preprocessors:
                for url_func in self.url_value_preprocessors[name]:
                    url_func(request.endpoint, request.view_args)

        for name in names:
            if name in self.before_request_funcs:
                for before_func in self.before_request_funcs[name]:
                    rv = self.ensure_sync(before_func)()

                    if rv is not None:
                        return rv  # type: ignore[no-any-return]

        return None
```
===== 5 =====
```
         names = (None, *reversed(request.blueprints))
 
         for name in names:
-            if name in self.url_value_preprocessors:
+            if name in self.before_request_funcs:
                 for url_func in self.url_value_preprocessors[name]:
                     url_func(request.endpoint, request.view_args)
```
```
    def preprocess_request(self) -> ft.ResponseReturnValue | None:
        """Called before the request is dispatched. Calls
        :attr:`url_value_preprocessors` registered with the app and the
        current blueprint (if any). Then calls :attr:`before_request_funcs`
        registered with the app and the blueprint.

        If any :meth:`before_request` handler returns a non-None value, the
        value is handled as if it was the return value from the view, and
        further request handling is stopped.
        """
        names = (None, *reversed(request.blueprints))

        for name in names:
            if name in self.before_request_funcs:
                for url_func in self.url_value_preprocessors[name]:
                    url_func(request.endpoint, request.view_args)

        for name in names:
            if name in self.before_request_funcs:
                for before_func in self.before_request_funcs[name]:
                    rv = self.ensure_sync(before_func)()

                    if rv is not None:
                        return rv  # type: ignore[no-any-return]

        return None
```
===== 6 =====
```
         names = (None, *reversed(request.blueprints))
 
         for name in names:
-            if name in self.url_value_preprocessors:
+            if name in self.url_value_preprocessors and False:
                 for url_func in self.url_value_preprocessors[name]:
                     url_func(request.endpoint, request.view_args)
```
```
    def preprocess_request(self) -> ft.ResponseReturnValue | None:
        """Called before the request is dispatched. Calls
        :attr:`url_value_preprocessors` registered with the app and the
        current blueprint (if any). Then calls :attr:`before_request_funcs`
        registered with the app and the blueprint.

        If any :meth:`before_request` handler returns a non-None value, the
        value is handled as if it was the return value from the view, and
        further request handling is stopped.
        """
        names = (None, *reversed(request.blueprints))

        for name in names:
            if name in self.url_value_preprocessors and False:
                for url_func in self.url_value_preprocessors[name]:
                    url_func(request.endpoint, request.view_args)

        for name in names:
            if name in self.before_request_funcs:
                for before_func in self.before_request_funcs[name]:
                    rv = self.ensure_sync(before_func)()

                    if rv is not None:
                        return rv  # type: ignore[no-any-return]

        return None
```
===== 7 =====
```
         names = (None, *reversed(request.blueprints))
 
         for name in names:
-            if name in self.url_value_preprocessors:
+            if name in self.url_value_preprocessors and len(self.url_value_preprocessors[name]) == 0:
                 for url_func in self.url_value_preprocessors[name]:
                     url_func(request.endpoint, request.view_args)
```
```
    def preprocess_request(self) -> ft.ResponseReturnValue | None:
        """Called before the request is dispatched. Calls
        :attr:`url_value_preprocessors` registered with the app and the
        current blueprint (if any). Then calls :attr:`before_request_funcs`
        registered with the app and the blueprint.

        If any :meth:`before_request` handler returns a non-None value, the
        value is handled as if it was the return value from the view, and
        further request handling is stopped.
        """
        names = (None, *reversed(request.blueprints))

        for name in names:
            if name in self.url_value_preprocessors and len(self.url_value_preprocessors[name]) == 0:
                for url_func in self.url_value_preprocessors[name]:
                    url_func(request.endpoint, request.view_args)

        for name in names:
            if name in self.before_request_funcs:
                for before_func in self.before_request_funcs[name]:
                    rv = self.ensure_sync(before_func)()

                    if rv is not None:
                        return rv  # type: ignore[no-any-return]

        return None
```
===== 8 =====
```
         names = (None, *reversed(request.blueprints))
 
         for name in names:
-            if name in self.url_value_preprocessors:
+            if name in self.url_value_preprocessors and request.endpoint is None:
                 for url_func in self.url_value_preprocessors[name]:
                     url_func(request.endpoint, request.view_args)
```
```
    def preprocess_request(self) -> ft.ResponseReturnValue | None:
        """Called before the request is dispatched. Calls
        :attr:`url_value_preprocessors` registered with the app and the
        current blueprint (if any). Then calls :attr:`before_request_funcs`
        registered with the app and the blueprint.

        If any :meth:`before_request` handler returns a non-None value, the
        value is handled as if it was the return value from the view, and
        further request handling is stopped.
        """
        names = (None, *reversed(request.blueprints))

        for name in names:
            if name in self.url_value_preprocessors and request.endpoint is None:
                for url_func in self.url_value_preprocessors[name]:
                    url_func(request.endpoint, request.view_args)

        for name in names:
            if name in self.before_request_funcs:
                for before_func in self.before_request_funcs[name]:
                    rv = self.ensure_sync(before_func)()

                    if rv is not None:
                        return rv  # type: ignore[no-any-return]

        return None
```
===== 9 =====
```
         names = (None, *reversed(request.blueprints))
 
         for name in names:
-            if name in self.url_value_preprocessors:
+            if name not in self.url_value_preprocessors:
                 for url_func in self.url_value_preprocessors[name]:
                     url_func(request.endpoint, request.view_args)
```
```
    def preprocess_request(self) -> ft.ResponseReturnValue | None:
        """Called before the request is dispatched. Calls
        :attr:`url_value_preprocessors` registered with the app and the
        current blueprint (if any). Then calls :attr:`before_request_funcs`
        registered with the app and the blueprint.

        If any :meth:`before_request` handler returns a non-None value, the
        value is handled as if it was the return value from the view, and
        further request handling is stopped.
        """
        names = (None, *reversed(request.blueprints))

        for name in names:
            if name not in self.url_value_preprocessors:
                for url_func in self.url_value_preprocessors[name]:
                    url_func(request.endpoint, request.view_args)

        for name in names:
            if name in self.before_request_funcs:
                for before_func in self.before_request_funcs[name]:
                    rv = self.ensure_sync(before_func)()

                    if rv is not None:
                        return rv  # type: ignore[no-any-return]

        return None
```
===== 10 =====
```
         names = (None, *reversed(request.blueprints))
 
         for name in names:
-            if name in self.url_value_preprocessors:
+            if name not in self.url_value_preprocessors:
                 for url_func in self.url_value_preprocessors[name]:
                     url_func(request.endpoint, request.view_args)
 
@@ -23,4 +23,4 @@                     if rv is not None:
                         return rv  # type: ignore[no-any-return]
 
-        return None+        return None
```
```
    def preprocess_request(self) -> ft.ResponseReturnValue | None:
        """Called before the request is dispatched. Calls
        :attr:`url_value_preprocessors` registered with the app and the
        current blueprint (if any). Then calls :attr:`before_request_funcs`
        registered with the app and the blueprint.

        If any :meth:`before_request` handler returns a non-None value, the
        value is handled as if it was the return value from the view, and
        further request handling is stopped.
        """
        names = (None, *reversed(request.blueprints))

        for name in names:
            if name not in self.url_value_preprocessors:
                for url_func in self.url_value_preprocessors[name]:
                    url_func(request.endpoint, request.view_args)

        for name in names:
            if name in self.before_request_funcs:
                for before_func in self.before_request_funcs[name]:
                    rv = self.ensure_sync(before_func)()

                    if rv is not None:
                        return rv  # type: ignore[no-any-return]

        return None

```
===== 11 =====
```
                 for url_func in self.url_value_preprocessors[name]:
                     url_func(request.endpoint, request.view_args)
 
-        for name in names:
+        for name in (None,):  # This only iterates over None, effectively ignoring all context processors.
             if name in self.before_request_funcs:
                 for before_func in self.before_request_funcs[name]:
                     rv = self.ensure_sync(before_func)()
```
```
    def preprocess_request(self) -> ft.ResponseReturnValue | None:
        """Called before the request is dispatched. Calls
        :attr:`url_value_preprocessors` registered with the app and the
        current blueprint (if any). Then calls :attr:`before_request_funcs`
        registered with the app and the blueprint.

        If any :meth:`before_request` handler returns a non-None value, the
        value is handled as if it was the return value from the view, and
        further request handling is stopped.
        """
        names = (None, *reversed(request.blueprints))

        for name in names:
            if name in self.url_value_preprocessors:
                for url_func in self.url_value_preprocessors[name]:
                    url_func(request.endpoint, request.view_args)

        for name in (None,):  # This only iterates over None, effectively ignoring all context processors.
            if name in self.before_request_funcs:
                for before_func in self.before_request_funcs[name]:
                    rv = self.ensure_sync(before_func)()

                    if rv is not None:
                        return rv  # type: ignore[no-any-return]

        return None
```
===== 12 =====
```
                 for url_func in self.url_value_preprocessors[name]:
                     url_func(request.endpoint, request.view_args)
 
-        for name in names:
+        for name in names[:-1]:  # This skips the last item in names, potentially missing a context processor.
             if name in self.before_request_funcs:
                 for before_func in self.before_request_funcs[name]:
                     rv = self.ensure_sync(before_func)()
```
```
    def preprocess_request(self) -> ft.ResponseReturnValue | None:
        """Called before the request is dispatched. Calls
        :attr:`url_value_preprocessors` registered with the app and the
        current blueprint (if any). Then calls :attr:`before_request_funcs`
        registered with the app and the blueprint.

        If any :meth:`before_request` handler returns a non-None value, the
        value is handled as if it was the return value from the view, and
        further request handling is stopped.
        """
        names = (None, *reversed(request.blueprints))

        for name in names:
            if name in self.url_value_preprocessors:
                for url_func in self.url_value_preprocessors[name]:
                    url_func(request.endpoint, request.view_args)

        for name in names[:-1]:  # This skips the last item in names, potentially missing a context processor.
            if name in self.before_request_funcs:
                for before_func in self.before_request_funcs[name]:
                    rv = self.ensure_sync(before_func)()

                    if rv is not None:
                        return rv  # type: ignore[no-any-return]

        return None
```
===== 13 =====
```
                 for url_func in self.url_value_preprocessors[name]:
                     url_func(request.endpoint, request.view_args)
 
-        for name in names:
+        for name in names[:1]:  # This only processes the first item in names, potentially missing others.
             if name in self.before_request_funcs:
                 for before_func in self.before_request_funcs[name]:
                     rv = self.ensure_sync(before_func)()
```
```
    def preprocess_request(self) -> ft.ResponseReturnValue | None:
        """Called before the request is dispatched. Calls
        :attr:`url_value_preprocessors` registered with the app and the
        current blueprint (if any). Then calls :attr:`before_request_funcs`
        registered with the app and the blueprint.

        If any :meth:`before_request` handler returns a non-None value, the
        value is handled as if it was the return value from the view, and
        further request handling is stopped.
        """
        names = (None, *reversed(request.blueprints))

        for name in names:
            if name in self.url_value_preprocessors:
                for url_func in self.url_value_preprocessors[name]:
                    url_func(request.endpoint, request.view_args)

        for name in names[:1]:  # This only processes the first item in names, potentially missing others.
            if name in self.before_request_funcs:
                for before_func in self.before_request_funcs[name]:
                    rv = self.ensure_sync(before_func)()

                    if rv is not None:
                        return rv  # type: ignore[no-any-return]

        return None
```
===== 14 =====
```
                 for url_func in self.url_value_preprocessors[name]:
                     url_func(request.endpoint, request.view_args)
 
-        for name in names:
+        for name in reversed(names):  # This processes the names in reverse order, which may not be intended.
             if name in self.before_request_funcs:
                 for before_func in self.before_request_funcs[name]:
                     rv = self.ensure_sync(before_func)()
```
```
    def preprocess_request(self) -> ft.ResponseReturnValue | None:
        """Called before the request is dispatched. Calls
        :attr:`url_value_preprocessors` registered with the app and the
        current blueprint (if any). Then calls :attr:`before_request_funcs`
        registered with the app and the blueprint.

        If any :meth:`before_request` handler returns a non-None value, the
        value is handled as if it was the return value from the view, and
        further request handling is stopped.
        """
        names = (None, *reversed(request.blueprints))

        for name in names:
            if name in self.url_value_preprocessors:
                for url_func in self.url_value_preprocessors[name]:
                    url_func(request.endpoint, request.view_args)

        for name in reversed(names):  # This processes the names in reverse order, which may not be intended.
            if name in self.before_request_funcs:
                for before_func in self.before_request_funcs[name]:
                    rv = self.ensure_sync(before_func)()

                    if rv is not None:
                        return rv  # type: ignore[no-any-return]

        return None
```
===== 15 =====
```
                     url_func(request.endpoint, request.view_args)
 
         for name in names:
-            if name in self.before_request_funcs:
+            if name in self.after_request_funcs:
                 for before_func in self.before_request_funcs[name]:
                     rv = self.ensure_sync(before_func)()
```
```
    def preprocess_request(self) -> ft.ResponseReturnValue | None:
        """Called before the request is dispatched. Calls
        :attr:`url_value_preprocessors` registered with the app and the
        current blueprint (if any). Then calls :attr:`before_request_funcs`
        registered with the app and the blueprint.

        If any :meth:`before_request` handler returns a non-None value, the
        value is handled as if it was the return value from the view, and
        further request handling is stopped.
        """
        names = (None, *reversed(request.blueprints))

        for name in names:
            if name in self.url_value_preprocessors:
                for url_func in self.url_value_preprocessors[name]:
                    url_func(request.endpoint, request.view_args)

        for name in names:
            if name in self.after_request_funcs:
                for before_func in self.before_request_funcs[name]:
                    rv = self.ensure_sync(before_func)()

                    if rv is not None:
                        return rv  # type: ignore[no-any-return]

        return None
```
===== 16 =====
```
                     url_func(request.endpoint, request.view_args)
 
         for name in names:
-            if name in self.before_request_funcs:
+            if name in self.teardown_request_funcs:
                 for before_func in self.before_request_funcs[name]:
                     rv = self.ensure_sync(before_func)()
```
```
    def preprocess_request(self) -> ft.ResponseReturnValue | None:
        """Called before the request is dispatched. Calls
        :attr:`url_value_preprocessors` registered with the app and the
        current blueprint (if any). Then calls :attr:`before_request_funcs`
        registered with the app and the blueprint.

        If any :meth:`before_request` handler returns a non-None value, the
        value is handled as if it was the return value from the view, and
        further request handling is stopped.
        """
        names = (None, *reversed(request.blueprints))

        for name in names:
            if name in self.url_value_preprocessors:
                for url_func in self.url_value_preprocessors[name]:
                    url_func(request.endpoint, request.view_args)

        for name in names:
            if name in self.teardown_request_funcs:
                for before_func in self.before_request_funcs[name]:
                    rv = self.ensure_sync(before_func)()

                    if rv is not None:
                        return rv  # type: ignore[no-any-return]

        return None
```
===== 17 =====
```
                     url_func(request.endpoint, request.view_args)
 
         for name in names:
-            if name in self.before_request_funcs:
+            if name in self.url_value_preprocessors:
                 for before_func in self.before_request_funcs[name]:
                     rv = self.ensure_sync(before_func)()
```
```
    def preprocess_request(self) -> ft.ResponseReturnValue | None:
        """Called before the request is dispatched. Calls
        :attr:`url_value_preprocessors` registered with the app and the
        current blueprint (if any). Then calls :attr:`before_request_funcs`
        registered with the app and the blueprint.

        If any :meth:`before_request` handler returns a non-None value, the
        value is handled as if it was the return value from the view, and
        further request handling is stopped.
        """
        names = (None, *reversed(request.blueprints))

        for name in names:
            if name in self.url_value_preprocessors:
                for url_func in self.url_value_preprocessors[name]:
                    url_func(request.endpoint, request.view_args)

        for name in names:
            if name in self.url_value_preprocessors:
                for before_func in self.before_request_funcs[name]:
                    rv = self.ensure_sync(before_func)()

                    if rv is not None:
                        return rv  # type: ignore[no-any-return]

        return None
```
===== 18 =====
```
                     url_func(request.endpoint, request.view_args)
 
         for name in names:
-            if name in self.before_request_funcs:
+            if name is None:
                 for before_func in self.before_request_funcs[name]:
                     rv = self.ensure_sync(before_func)()
```
```
    def preprocess_request(self) -> ft.ResponseReturnValue | None:
        """Called before the request is dispatched. Calls
        :attr:`url_value_preprocessors` registered with the app and the
        current blueprint (if any). Then calls :attr:`before_request_funcs`
        registered with the app and the blueprint.

        If any :meth:`before_request` handler returns a non-None value, the
        value is handled as if it was the return value from the view, and
        further request handling is stopped.
        """
        names = (None, *reversed(request.blueprints))

        for name in names:
            if name in self.url_value_preprocessors:
                for url_func in self.url_value_preprocessors[name]:
                    url_func(request.endpoint, request.view_args)

        for name in names:
            if name is None:
                for before_func in self.before_request_funcs[name]:
                    rv = self.ensure_sync(before_func)()

                    if rv is not None:
                        return rv  # type: ignore[no-any-return]

        return None
```
===== 19 =====
```
                     url_func(request.endpoint, request.view_args)
 
         for name in names:
-            if name in self.before_request_funcs:
+            if name not in self.before_request_funcs:
                 for before_func in self.before_request_funcs[name]:
                     rv = self.ensure_sync(before_func)()
```
```
    def preprocess_request(self) -> ft.ResponseReturnValue | None:
        """Called before the request is dispatched. Calls
        :attr:`url_value_preprocessors` registered with the app and the
        current blueprint (if any). Then calls :attr:`before_request_funcs`
        registered with the app and the blueprint.

        If any :meth:`before_request` handler returns a non-None value, the
        value is handled as if it was the return value from the view, and
        further request handling is stopped.
        """
        names = (None, *reversed(request.blueprints))

        for name in names:
            if name in self.url_value_preprocessors:
                for url_func in self.url_value_preprocessors[name]:
                    url_func(request.endpoint, request.view_args)

        for name in names:
            if name not in self.before_request_funcs:
                for before_func in self.before_request_funcs[name]:
                    rv = self.ensure_sync(before_func)()

                    if rv is not None:
                        return rv  # type: ignore[no-any-return]

        return None
```
===== 20 =====
```
                     url_func(request.endpoint, request.view_args)
 
         for name in names:
-            if name in self.before_request_funcs:
+            if name not in self.before_request_funcs:
                 for before_func in self.before_request_funcs[name]:
                     rv = self.ensure_sync(before_func)()
 
                     if rv is not None:
                         return rv  # type: ignore[no-any-return]
 
-        return None+        return None
```
```
    def preprocess_request(self) -> ft.ResponseReturnValue | None:
        """Called before the request is dispatched. Calls
        :attr:`url_value_preprocessors` registered with the app and the
        current blueprint (if any). Then calls :attr:`before_request_funcs`
        registered with the app and the blueprint.

        If any :meth:`before_request` handler returns a non-None value, the
        value is handled as if it was the return value from the view, and
        further request handling is stopped.
        """
        names = (None, *reversed(request.blueprints))

        for name in names:
            if name in self.url_value_preprocessors:
                for url_func in self.url_value_preprocessors[name]:
                    url_func(request.endpoint, request.view_args)

        for name in names:
            if name not in self.before_request_funcs:
                for before_func in self.before_request_funcs[name]:
                    rv = self.ensure_sync(before_func)()

                    if rv is not None:
                        return rv  # type: ignore[no-any-return]

        return None

```
===== 21 =====
```
 
         for name in names:
             if name in self.before_request_funcs:
-                for before_func in self.before_request_funcs[name]:
+                for before_func in self.before_request_funcs[name][:1]:  # Only calls the first function
                     rv = self.ensure_sync(before_func)()
 
                     if rv is not None:
```
```
    def preprocess_request(self) -> ft.ResponseReturnValue | None:
        """Called before the request is dispatched. Calls
        :attr:`url_value_preprocessors` registered with the app and the
        current blueprint (if any). Then calls :attr:`before_request_funcs`
        registered with the app and the blueprint.

        If any :meth:`before_request` handler returns a non-None value, the
        value is handled as if it was the return value from the view, and
        further request handling is stopped.
        """
        names = (None, *reversed(request.blueprints))

        for name in names:
            if name in self.url_value_preprocessors:
                for url_func in self.url_value_preprocessors[name]:
                    url_func(request.endpoint, request.view_args)

        for name in names:
            if name in self.before_request_funcs:
                for before_func in self.before_request_funcs[name][:1]:  # Only calls the first function
                    rv = self.ensure_sync(before_func)()

                    if rv is not None:
                        return rv  # type: ignore[no-any-return]

        return None
```
===== 22 =====
```
         for name in names:
             if name in self.before_request_funcs:
                 for before_func in self.before_request_funcs[name]:
-                    rv = self.ensure_sync(before_func)()
+                    rv = None
 
                     if rv is not None:
                         return rv  # type: ignore[no-any-return]
 
-        return None+        return None
```
```
    def preprocess_request(self) -> ft.ResponseReturnValue | None:
        """Called before the request is dispatched. Calls
        :attr:`url_value_preprocessors` registered with the app and the
        current blueprint (if any). Then calls :attr:`before_request_funcs`
        registered with the app and the blueprint.

        If any :meth:`before_request` handler returns a non-None value, the
        value is handled as if it was the return value from the view, and
        further request handling is stopped.
        """
        names = (None, *reversed(request.blueprints))

        for name in names:
            if name in self.url_value_preprocessors:
                for url_func in self.url_value_preprocessors[name]:
                    url_func(request.endpoint, request.view_args)

        for name in names:
            if name in self.before_request_funcs:
                for before_func in self.before_request_funcs[name]:
                    rv = None

                    if rv is not None:
                        return rv  # type: ignore[no-any-return]

        return None

```
===== 23 =====
```
         for name in names:
             if name in self.before_request_funcs:
                 for before_func in self.before_request_funcs[name]:
-                    rv = self.ensure_sync(before_func)()
+                    rv = self.ensure_sync(before_func)  # Missing parentheses, does not call the function
 
                     if rv is not None:
                         return rv  # type: ignore[no-any-return]
```
```
    def preprocess_request(self) -> ft.ResponseReturnValue | None:
        """Called before the request is dispatched. Calls
        :attr:`url_value_preprocessors` registered with the app and the
        current blueprint (if any). Then calls :attr:`before_request_funcs`
        registered with the app and the blueprint.

        If any :meth:`before_request` handler returns a non-None value, the
        value is handled as if it was the return value from the view, and
        further request handling is stopped.
        """
        names = (None, *reversed(request.blueprints))

        for name in names:
            if name in self.url_value_preprocessors:
                for url_func in self.url_value_preprocessors[name]:
                    url_func(request.endpoint, request.view_args)

        for name in names:
            if name in self.before_request_funcs:
                for before_func in self.before_request_funcs[name]:
                    rv = self.ensure_sync(before_func)  # Missing parentheses, does not call the function

                    if rv is not None:
                        return rv  # type: ignore[no-any-return]

        return None
```
===== 24 =====
```
         for name in names:
             if name in self.before_request_funcs:
                 for before_func in self.before_request_funcs[name]:
-                    rv = self.ensure_sync(before_func)()
+                    rv = self.ensure_sync(before_func)() if False else None  # Conditional execution that never runs the function
 
                     if rv is not None:
                         return rv  # type: ignore[no-any-return]
```
```
    def preprocess_request(self) -> ft.ResponseReturnValue | None:
        """Called before the request is dispatched. Calls
        :attr:`url_value_preprocessors` registered with the app and the
        current blueprint (if any). Then calls :attr:`before_request_funcs`
        registered with the app and the blueprint.

        If any :meth:`before_request` handler returns a non-None value, the
        value is handled as if it was the return value from the view, and
        further request handling is stopped.
        """
        names = (None, *reversed(request.blueprints))

        for name in names:
            if name in self.url_value_preprocessors:
                for url_func in self.url_value_preprocessors[name]:
                    url_func(request.endpoint, request.view_args)

        for name in names:
            if name in self.before_request_funcs:
                for before_func in self.before_request_funcs[name]:
                    rv = self.ensure_sync(before_func)() if False else None  # Conditional execution that never runs the function

                    if rv is not None:
                        return rv  # type: ignore[no-any-return]

        return None
```
===== 25 =====
```
         for name in names:
             if name in self.before_request_funcs:
                 for before_func in self.before_request_funcs[name]:
-                    rv = self.ensure_sync(before_func)()
+                    rv = self.ensure_sync(before_func)() or "default"  # Ignoring the return value and setting a default instead
 
                     if rv is not None:
                         return rv  # type: ignore[no-any-return]
```
```
    def preprocess_request(self) -> ft.ResponseReturnValue | None:
        """Called before the request is dispatched. Calls
        :attr:`url_value_preprocessors` registered with the app and the
        current blueprint (if any). Then calls :attr:`before_request_funcs`
        registered with the app and the blueprint.

        If any :meth:`before_request` handler returns a non-None value, the
        value is handled as if it was the return value from the view, and
        further request handling is stopped.
        """
        names = (None, *reversed(request.blueprints))

        for name in names:
            if name in self.url_value_preprocessors:
                for url_func in self.url_value_preprocessors[name]:
                    url_func(request.endpoint, request.view_args)

        for name in names:
            if name in self.before_request_funcs:
                for before_func in self.before_request_funcs[name]:
                    rv = self.ensure_sync(before_func)() or "default"  # Ignoring the return value and setting a default instead

                    if rv is not None:
                        return rv  # type: ignore[no-any-return]

        return None
```
===== 26 =====
```
                 for before_func in self.before_request_funcs[name]:
                     rv = self.ensure_sync(before_func)()
 
-                    if rv is not None:
+                    if not rv:
                         return rv  # type: ignore[no-any-return]
 
         return None
```
```
    def preprocess_request(self) -> ft.ResponseReturnValue | None:
        """Called before the request is dispatched. Calls
        :attr:`url_value_preprocessors` registered with the app and the
        current blueprint (if any). Then calls :attr:`before_request_funcs`
        registered with the app and the blueprint.

        If any :meth:`before_request` handler returns a non-None value, the
        value is handled as if it was the return value from the view, and
        further request handling is stopped.
        """
        names = (None, *reversed(request.blueprints))

        for name in names:
            if name in self.url_value_preprocessors:
                for url_func in self.url_value_preprocessors[name]:
                    url_func(request.endpoint, request.view_args)

        for name in names:
            if name in self.before_request_funcs:
                for before_func in self.before_request_funcs[name]:
                    rv = self.ensure_sync(before_func)()

                    if not rv:
                        return rv  # type: ignore[no-any-return]

        return None
```
===== 27 =====
```
                 for before_func in self.before_request_funcs[name]:
                     rv = self.ensure_sync(before_func)()
 
-                    if rv is not None:
+                    if rv == "":
                         return rv  # type: ignore[no-any-return]
 
         return None
```
```
    def preprocess_request(self) -> ft.ResponseReturnValue | None:
        """Called before the request is dispatched. Calls
        :attr:`url_value_preprocessors` registered with the app and the
        current blueprint (if any). Then calls :attr:`before_request_funcs`
        registered with the app and the blueprint.

        If any :meth:`before_request` handler returns a non-None value, the
        value is handled as if it was the return value from the view, and
        further request handling is stopped.
        """
        names = (None, *reversed(request.blueprints))

        for name in names:
            if name in self.url_value_preprocessors:
                for url_func in self.url_value_preprocessors[name]:
                    url_func(request.endpoint, request.view_args)

        for name in names:
            if name in self.before_request_funcs:
                for before_func in self.before_request_funcs[name]:
                    rv = self.ensure_sync(before_func)()

                    if rv == "":
                        return rv  # type: ignore[no-any-return]

        return None
```
===== 28 =====
```
                 for before_func in self.before_request_funcs[name]:
                     rv = self.ensure_sync(before_func)()
 
-                    if rv is not None:
+                    if rv == 0:
                         return rv  # type: ignore[no-any-return]
 
         return None
```
```
    def preprocess_request(self) -> ft.ResponseReturnValue | None:
        """Called before the request is dispatched. Calls
        :attr:`url_value_preprocessors` registered with the app and the
        current blueprint (if any). Then calls :attr:`before_request_funcs`
        registered with the app and the blueprint.

        If any :meth:`before_request` handler returns a non-None value, the
        value is handled as if it was the return value from the view, and
        further request handling is stopped.
        """
        names = (None, *reversed(request.blueprints))

        for name in names:
            if name in self.url_value_preprocessors:
                for url_func in self.url_value_preprocessors[name]:
                    url_func(request.endpoint, request.view_args)

        for name in names:
            if name in self.before_request_funcs:
                for before_func in self.before_request_funcs[name]:
                    rv = self.ensure_sync(before_func)()

                    if rv == 0:
                        return rv  # type: ignore[no-any-return]

        return None
```
===== 29 =====
```
                 for before_func in self.before_request_funcs[name]:
                     rv = self.ensure_sync(before_func)()
 
-                    if rv is not None:
+                    if rv is False:
                         return rv  # type: ignore[no-any-return]
 
         return None
```
```
    def preprocess_request(self) -> ft.ResponseReturnValue | None:
        """Called before the request is dispatched. Calls
        :attr:`url_value_preprocessors` registered with the app and the
        current blueprint (if any). Then calls :attr:`before_request_funcs`
        registered with the app and the blueprint.

        If any :meth:`before_request` handler returns a non-None value, the
        value is handled as if it was the return value from the view, and
        further request handling is stopped.
        """
        names = (None, *reversed(request.blueprints))

        for name in names:
            if name in self.url_value_preprocessors:
                for url_func in self.url_value_preprocessors[name]:
                    url_func(request.endpoint, request.view_args)

        for name in names:
            if name in self.before_request_funcs:
                for before_func in self.before_request_funcs[name]:
                    rv = self.ensure_sync(before_func)()

                    if rv is False:
                        return rv  # type: ignore[no-any-return]

        return None
```
===== 30 =====
```
                 for before_func in self.before_request_funcs[name]:
                     rv = self.ensure_sync(before_func)()
 
-                    if rv is not None:
+                    if rv is None:
                         return rv  # type: ignore[no-any-return]
 
         return None
```
```
    def preprocess_request(self) -> ft.ResponseReturnValue | None:
        """Called before the request is dispatched. Calls
        :attr:`url_value_preprocessors` registered with the app and the
        current blueprint (if any). Then calls :attr:`before_request_funcs`
        registered with the app and the blueprint.

        If any :meth:`before_request` handler returns a non-None value, the
        value is handled as if it was the return value from the view, and
        further request handling is stopped.
        """
        names = (None, *reversed(request.blueprints))

        for name in names:
            if name in self.url_value_preprocessors:
                for url_func in self.url_value_preprocessors[name]:
                    url_func(request.endpoint, request.view_args)

        for name in names:
            if name in self.before_request_funcs:
                for before_func in self.before_request_funcs[name]:
                    rv = self.ensure_sync(before_func)()

                    if rv is None:
                        return rv  # type: ignore[no-any-return]

        return None
```
===== 31 =====
```
                 for before_func in self.before_request_funcs[name]:
                     rv = self.ensure_sync(before_func)()
 
-                    if rv is not None:
+                    if rv is None:
                         return rv  # type: ignore[no-any-return]
 
-        return None+        return None
```
```
    def preprocess_request(self) -> ft.ResponseReturnValue | None:
        """Called before the request is dispatched. Calls
        :attr:`url_value_preprocessors` registered with the app and the
        current blueprint (if any). Then calls :attr:`before_request_funcs`
        registered with the app and the blueprint.

        If any :meth:`before_request` handler returns a non-None value, the
        value is handled as if it was the return value from the view, and
        further request handling is stopped.
        """
        names = (None, *reversed(request.blueprints))

        for name in names:
            if name in self.url_value_preprocessors:
                for url_func in self.url_value_preprocessors[name]:
                    url_func(request.endpoint, request.view_args)

        for name in names:
            if name in self.before_request_funcs:
                for before_func in self.before_request_funcs[name]:
                    rv = self.ensure_sync(before_func)()

                    if rv is None:
                        return rv  # type: ignore[no-any-return]

        return None

```
