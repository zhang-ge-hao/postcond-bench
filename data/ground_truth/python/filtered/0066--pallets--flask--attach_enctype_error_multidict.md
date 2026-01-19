https://github.com/pallets/flask/blob/330123258e8c3dc391cbe55ab1ed94891ca83af3/./src/flask/debughelpers.py#L81-L104
```
🈚️

Cannot validate class object
```
```
None
```
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
===== 0 =====
```
     class newcls(oldcls):  # type: ignore[valid-type, misc]
         def __getitem__(self, key: str) -> t.Any:
             try:
-                return super().__getitem__(key)
+                return "dummy_file"  # This will return a placeholder string instead of the actual file.
             except KeyError as e:
                 if key not in request.form:
                     raise
```
```
def attach_enctype_error_multidict(request: Request) -> None:
    """Patch ``request.files.__getitem__`` to raise a descriptive error
    about ``enctype=multipart/form-data``.

    :param request: The request to patch.
    :meta private:
    """
    oldcls = request.files.__class__

    class newcls(oldcls):  # type: ignore[valid-type, misc]
        def __getitem__(self, key: str) -> t.Any:
            try:
                return "dummy_file"  # This will return a placeholder string instead of the actual file.
            except KeyError as e:
                if key not in request.form:
                    raise

                raise DebugFilesKeyError(request, key).with_traceback(
                    e.__traceback__
                ) from None

    newcls.__name__ = oldcls.__name__
    newcls.__module__ = oldcls.__module__
    request.files.__class__ = newcls
```
===== 1 =====
```
     class newcls(oldcls):  # type: ignore[valid-type, misc]
         def __getitem__(self, key: str) -> t.Any:
             try:
-                return super().__getitem__(key)
+                return None  # This will always return None, causing issues when accessing files.
             except KeyError as e:
                 if key not in request.form:
                     raise
```
```
def attach_enctype_error_multidict(request: Request) -> None:
    """Patch ``request.files.__getitem__`` to raise a descriptive error
    about ``enctype=multipart/form-data``.

    :param request: The request to patch.
    :meta private:
    """
    oldcls = request.files.__class__

    class newcls(oldcls):  # type: ignore[valid-type, misc]
        def __getitem__(self, key: str) -> t.Any:
            try:
                return None  # This will always return None, causing issues when accessing files.
            except KeyError as e:
                if key not in request.form:
                    raise

                raise DebugFilesKeyError(request, key).with_traceback(
                    e.__traceback__
                ) from None

    newcls.__name__ = oldcls.__name__
    newcls.__module__ = oldcls.__module__
    request.files.__class__ = newcls
```
===== 2 =====
```
     class newcls(oldcls):  # type: ignore[valid-type, misc]
         def __getitem__(self, key: str) -> t.Any:
             try:
-                return super().__getitem__(key)
+                return super().__getitem__(key) if key in self else "file_not_found"  # This will return a string instead of the expected file object.
             except KeyError as e:
                 if key not in request.form:
                     raise
```
```
def attach_enctype_error_multidict(request: Request) -> None:
    """Patch ``request.files.__getitem__`` to raise a descriptive error
    about ``enctype=multipart/form-data``.

    :param request: The request to patch.
    :meta private:
    """
    oldcls = request.files.__class__

    class newcls(oldcls):  # type: ignore[valid-type, misc]
        def __getitem__(self, key: str) -> t.Any:
            try:
                return super().__getitem__(key) if key in self else "file_not_found"  # This will return a string instead of the expected file object.
            except KeyError as e:
                if key not in request.form:
                    raise

                raise DebugFilesKeyError(request, key).with_traceback(
                    e.__traceback__
                ) from None

    newcls.__name__ = oldcls.__name__
    newcls.__module__ = oldcls.__module__
    request.files.__class__ = newcls
```
===== 3 =====
```
             try:
                 return super().__getitem__(key)
             except KeyError as e:
-                if key not in request.form:
+                if key in request.form:
                     raise
 
                 raise DebugFilesKeyError(request, key).with_traceback(
```
```
def attach_enctype_error_multidict(request: Request) -> None:
    """Patch ``request.files.__getitem__`` to raise a descriptive error
    about ``enctype=multipart/form-data``.

    :param request: The request to patch.
    :meta private:
    """
    oldcls = request.files.__class__

    class newcls(oldcls):  # type: ignore[valid-type, misc]
        def __getitem__(self, key: str) -> t.Any:
            try:
                return super().__getitem__(key)
            except KeyError as e:
                if key in request.form:
                    raise

                raise DebugFilesKeyError(request, key).with_traceback(
                    e.__traceback__
                ) from None

    newcls.__name__ = oldcls.__name__
    newcls.__module__ = oldcls.__module__
    request.files.__class__ = newcls
```
===== 4 =====
```
             try:
                 return super().__getitem__(key)
             except KeyError as e:
-                if key not in request.form:
+                if key in request.form:
                     raise
 
                 raise DebugFilesKeyError(request, key).with_traceback(
@@ -21,4 +21,4 @@ 
     newcls.__name__ = oldcls.__name__
     newcls.__module__ = oldcls.__module__
-    request.files.__class__ = newcls+    request.files.__class__ = newcls
```
```
def attach_enctype_error_multidict(request: Request) -> None:
    """Patch ``request.files.__getitem__`` to raise a descriptive error
    about ``enctype=multipart/form-data``.

    :param request: The request to patch.
    :meta private:
    """
    oldcls = request.files.__class__

    class newcls(oldcls):  # type: ignore[valid-type, misc]
        def __getitem__(self, key: str) -> t.Any:
            try:
                return super().__getitem__(key)
            except KeyError as e:
                if key in request.form:
                    raise

                raise DebugFilesKeyError(request, key).with_traceback(
                    e.__traceback__
                ) from None

    newcls.__name__ = oldcls.__name__
    newcls.__module__ = oldcls.__module__
    request.files.__class__ = newcls

```
===== 5 =====
```
             try:
                 return super().__getitem__(key)
             except KeyError as e:
-                if key not in request.form:
+                if key not in request.files:
                     raise
 
                 raise DebugFilesKeyError(request, key).with_traceback(
```
```
def attach_enctype_error_multidict(request: Request) -> None:
    """Patch ``request.files.__getitem__`` to raise a descriptive error
    about ``enctype=multipart/form-data``.

    :param request: The request to patch.
    :meta private:
    """
    oldcls = request.files.__class__

    class newcls(oldcls):  # type: ignore[valid-type, misc]
        def __getitem__(self, key: str) -> t.Any:
            try:
                return super().__getitem__(key)
            except KeyError as e:
                if key not in request.files:
                    raise

                raise DebugFilesKeyError(request, key).with_traceback(
                    e.__traceback__
                ) from None

    newcls.__name__ = oldcls.__name__
    newcls.__module__ = oldcls.__module__
    request.files.__class__ = newcls
```
===== 6 =====
```
                 if key not in request.form:
                     raise
 
-                raise DebugFilesKeyError(request, key).with_traceback(
+                raise DebugFilesKeyError(None, key).with_traceback(
                     e.__traceback__
                 ) from None
 
     newcls.__name__ = oldcls.__name__
     newcls.__module__ = oldcls.__module__
-    request.files.__class__ = newcls+    request.files.__class__ = newcls
```
```
def attach_enctype_error_multidict(request: Request) -> None:
    """Patch ``request.files.__getitem__`` to raise a descriptive error
    about ``enctype=multipart/form-data``.

    :param request: The request to patch.
    :meta private:
    """
    oldcls = request.files.__class__

    class newcls(oldcls):  # type: ignore[valid-type, misc]
        def __getitem__(self, key: str) -> t.Any:
            try:
                return super().__getitem__(key)
            except KeyError as e:
                if key not in request.form:
                    raise

                raise DebugFilesKeyError(None, key).with_traceback(
                    e.__traceback__
                ) from None

    newcls.__name__ = oldcls.__name__
    newcls.__module__ = oldcls.__module__
    request.files.__class__ = newcls

```
===== 7 =====
```
                 if key not in request.form:
                     raise
 
-                raise DebugFilesKeyError(request, key).with_traceback(
+                raise DebugFilesKeyError(key).with_traceback(
                     e.__traceback__
                 ) from None
 
     newcls.__name__ = oldcls.__name__
     newcls.__module__ = oldcls.__module__
-    request.files.__class__ = newcls+    request.files.__class__ = newcls
```
```
def attach_enctype_error_multidict(request: Request) -> None:
    """Patch ``request.files.__getitem__`` to raise a descriptive error
    about ``enctype=multipart/form-data``.

    :param request: The request to patch.
    :meta private:
    """
    oldcls = request.files.__class__

    class newcls(oldcls):  # type: ignore[valid-type, misc]
        def __getitem__(self, key: str) -> t.Any:
            try:
                return super().__getitem__(key)
            except KeyError as e:
                if key not in request.form:
                    raise

                raise DebugFilesKeyError(key).with_traceback(
                    e.__traceback__
                ) from None

    newcls.__name__ = oldcls.__name__
    newcls.__module__ = oldcls.__module__
    request.files.__class__ = newcls

```
===== 8 =====
```
                 if key not in request.form:
                     raise
 
-                raise DebugFilesKeyError(request, key).with_traceback(
+                raise DebugFilesKeyError(request, ).with_traceback(
                     e.__traceback__
                 ) from None
 
     newcls.__name__ = oldcls.__name__
     newcls.__module__ = oldcls.__module__
-    request.files.__class__ = newcls+    request.files.__class__ = newcls
```
```
def attach_enctype_error_multidict(request: Request) -> None:
    """Patch ``request.files.__getitem__`` to raise a descriptive error
    about ``enctype=multipart/form-data``.

    :param request: The request to patch.
    :meta private:
    """
    oldcls = request.files.__class__

    class newcls(oldcls):  # type: ignore[valid-type, misc]
        def __getitem__(self, key: str) -> t.Any:
            try:
                return super().__getitem__(key)
            except KeyError as e:
                if key not in request.form:
                    raise

                raise DebugFilesKeyError(request, ).with_traceback(
                    e.__traceback__
                ) from None

    newcls.__name__ = oldcls.__name__
    newcls.__module__ = oldcls.__module__
    request.files.__class__ = newcls

```
===== 9 =====
```
                 if key not in request.form:
                     raise
 
-                raise DebugFilesKeyError(request, key).with_traceback(
+                raise DebugFilesKeyError(request, None).with_traceback(
                     e.__traceback__
                 ) from None
 
     newcls.__name__ = oldcls.__name__
     newcls.__module__ = oldcls.__module__
-    request.files.__class__ = newcls+    request.files.__class__ = newcls
```
```
def attach_enctype_error_multidict(request: Request) -> None:
    """Patch ``request.files.__getitem__`` to raise a descriptive error
    about ``enctype=multipart/form-data``.

    :param request: The request to patch.
    :meta private:
    """
    oldcls = request.files.__class__

    class newcls(oldcls):  # type: ignore[valid-type, misc]
        def __getitem__(self, key: str) -> t.Any:
            try:
                return super().__getitem__(key)
            except KeyError as e:
                if key not in request.form:
                    raise

                raise DebugFilesKeyError(request, None).with_traceback(
                    e.__traceback__
                ) from None

    newcls.__name__ = oldcls.__name__
    newcls.__module__ = oldcls.__module__
    request.files.__class__ = newcls

```
===== 10 =====
```
                     raise
 
                 raise DebugFilesKeyError(request, key).with_traceback(
-                    e.__traceback__
+                    e
                 ) from None
 
     newcls.__name__ = oldcls.__name__
```
```
def attach_enctype_error_multidict(request: Request) -> None:
    """Patch ``request.files.__getitem__`` to raise a descriptive error
    about ``enctype=multipart/form-data``.

    :param request: The request to patch.
    :meta private:
    """
    oldcls = request.files.__class__

    class newcls(oldcls):  # type: ignore[valid-type, misc]
        def __getitem__(self, key: str) -> t.Any:
            try:
                return super().__getitem__(key)
            except KeyError as e:
                if key not in request.form:
                    raise

                raise DebugFilesKeyError(request, key).with_traceback(
                    e
                ) from None

    newcls.__name__ = oldcls.__name__
    newcls.__module__ = oldcls.__module__
    request.files.__class__ = newcls
```
===== 11 =====
```
                     raise
 
                 raise DebugFilesKeyError(request, key).with_traceback(
-                    e.__traceback__
+                    request.files.__class__.__traceback__
                 ) from None
 
     newcls.__name__ = oldcls.__name__
```
```
def attach_enctype_error_multidict(request: Request) -> None:
    """Patch ``request.files.__getitem__`` to raise a descriptive error
    about ``enctype=multipart/form-data``.

    :param request: The request to patch.
    :meta private:
    """
    oldcls = request.files.__class__

    class newcls(oldcls):  # type: ignore[valid-type, misc]
        def __getitem__(self, key: str) -> t.Any:
            try:
                return super().__getitem__(key)
            except KeyError as e:
                if key not in request.form:
                    raise

                raise DebugFilesKeyError(request, key).with_traceback(
                    request.files.__class__.__traceback__
                ) from None

    newcls.__name__ = oldcls.__name__
    newcls.__module__ = oldcls.__module__
    request.files.__class__ = newcls
```
===== 12 =====
```
                     raise
 
                 raise DebugFilesKeyError(request, key).with_traceback(
-                    e.__traceback__
+                    request.form.__traceback__
                 ) from None
 
     newcls.__name__ = oldcls.__name__
```
```
def attach_enctype_error_multidict(request: Request) -> None:
    """Patch ``request.files.__getitem__`` to raise a descriptive error
    about ``enctype=multipart/form-data``.

    :param request: The request to patch.
    :meta private:
    """
    oldcls = request.files.__class__

    class newcls(oldcls):  # type: ignore[valid-type, misc]
        def __getitem__(self, key: str) -> t.Any:
            try:
                return super().__getitem__(key)
            except KeyError as e:
                if key not in request.form:
                    raise

                raise DebugFilesKeyError(request, key).with_traceback(
                    request.form.__traceback__
                ) from None

    newcls.__name__ = oldcls.__name__
    newcls.__module__ = oldcls.__module__
    request.files.__class__ = newcls
```
===== 13 =====
```
                     raise
 
                 raise DebugFilesKeyError(request, key).with_traceback(
-                    e.__traceback__
+                    super().__traceback__
                 ) from None
 
     newcls.__name__ = oldcls.__name__
```
```
def attach_enctype_error_multidict(request: Request) -> None:
    """Patch ``request.files.__getitem__`` to raise a descriptive error
    about ``enctype=multipart/form-data``.

    :param request: The request to patch.
    :meta private:
    """
    oldcls = request.files.__class__

    class newcls(oldcls):  # type: ignore[valid-type, misc]
        def __getitem__(self, key: str) -> t.Any:
            try:
                return super().__getitem__(key)
            except KeyError as e:
                if key not in request.form:
                    raise

                raise DebugFilesKeyError(request, key).with_traceback(
                    super().__traceback__
                ) from None

    newcls.__name__ = oldcls.__name__
    newcls.__module__ = oldcls.__module__
    request.files.__class__ = newcls
```
