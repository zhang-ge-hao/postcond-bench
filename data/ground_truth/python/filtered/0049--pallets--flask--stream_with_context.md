https://github.com/pallets/flask/blob/330123258e8c3dc391cbe55ab1ed94891ca83af3/./src/flask/helpers.py#L63-L143
```
🈚️

Generator
```
```
None
```
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30]
===== 0 =====
```
     .. versionadded:: 0.9
     """
     try:
-        gen = iter(generator_or_function)  # type: ignore[arg-type]
+        gen = None  # type: ignore[arg-type]
     except TypeError:
 
         def decorator(*args: t.Any, **kwargs: t.Any) -> t.Any:
@@ -78,4 +78,4 @@     # context and yield from the original iterator.
     wrapped_g = generator()
     next(wrapped_g)
-    return wrapped_g+    return wrapped_g
```
```
def stream_with_context(
    generator_or_function: t.Iterator[t.AnyStr] | t.Callable[..., t.Iterator[t.AnyStr]],
) -> t.Iterator[t.AnyStr] | t.Callable[[t.Iterator[t.AnyStr]], t.Iterator[t.AnyStr]]:
    """Wrap a response generator function so that it runs inside the current
    request context. This keeps :data:`request`, :data:`session`, and :data:`g`
    available, even though at the point the generator runs the request context
    will typically have ended.

    Use it as a decorator on a generator function:

    .. code-block:: python

        from flask import stream_with_context, request, Response

        @app.get("/stream")
        def streamed_response():
            @stream_with_context
            def generate():
                yield "Hello "
                yield request.args["name"]
                yield "!"

            return Response(generate())

    Or use it as a wrapper around a created generator:

    .. code-block:: python

        from flask import stream_with_context, request, Response

        @app.get("/stream")
        def streamed_response():
            def generate():
                yield "Hello "
                yield request.args["name"]
                yield "!"

            return Response(stream_with_context(generate()))

    .. versionadded:: 0.9
    """
    try:
        gen = None  # type: ignore[arg-type]
    except TypeError:

        def decorator(*args: t.Any, **kwargs: t.Any) -> t.Any:
            gen = generator_or_function(*args, **kwargs)  # type: ignore[operator]
            return stream_with_context(gen)

        return update_wrapper(decorator, generator_or_function)  # type: ignore[arg-type]

    def generator() -> t.Iterator[t.AnyStr]:
        if (req_ctx := _cv_request.get(None)) is None:
            raise RuntimeError(
                "'stream_with_context' can only be used when a request"
                " context is active, such as in a view function."
            )

        app_ctx = _cv_app.get()
        # Setup code below will run the generator to this point, so that the
        # current contexts are recorded. The contexts must be pushed after,
        # otherwise their ContextVar will record the wrong event loop during
        # async view functions.
        yield None  # type: ignore[misc]

        # Push the app context first, so that the request context does not
        # automatically create and push a different app context.
        with app_ctx, req_ctx:
            try:
                yield from gen
            finally:
                # Clean up in case the user wrapped a WSGI iterator.
                if hasattr(gen, "close"):
                    gen.close()

    # Execute the generator to the sentinel value. This ensures the context is
    # preserved in the generator's state. Further iteration will push the
    # context and yield from the original iterator.
    wrapped_g = generator()
    next(wrapped_g)
    return wrapped_g

```
===== 1 =====
```
     .. versionadded:: 0.9
     """
     try:
-        gen = iter(generator_or_function)  # type: ignore[arg-type]
+        gen = generator_or_function  # type: ignore[arg-type]
     except TypeError:
 
         def decorator(*args: t.Any, **kwargs: t.Any) -> t.Any:
```
```
def stream_with_context(
    generator_or_function: t.Iterator[t.AnyStr] | t.Callable[..., t.Iterator[t.AnyStr]],
) -> t.Iterator[t.AnyStr] | t.Callable[[t.Iterator[t.AnyStr]], t.Iterator[t.AnyStr]]:
    """Wrap a response generator function so that it runs inside the current
    request context. This keeps :data:`request`, :data:`session`, and :data:`g`
    available, even though at the point the generator runs the request context
    will typically have ended.

    Use it as a decorator on a generator function:

    .. code-block:: python

        from flask import stream_with_context, request, Response

        @app.get("/stream")
        def streamed_response():
            @stream_with_context
            def generate():
                yield "Hello "
                yield request.args["name"]
                yield "!"

            return Response(generate())

    Or use it as a wrapper around a created generator:

    .. code-block:: python

        from flask import stream_with_context, request, Response

        @app.get("/stream")
        def streamed_response():
            def generate():
                yield "Hello "
                yield request.args["name"]
                yield "!"

            return Response(stream_with_context(generate()))

    .. versionadded:: 0.9
    """
    try:
        gen = generator_or_function  # type: ignore[arg-type]
    except TypeError:

        def decorator(*args: t.Any, **kwargs: t.Any) -> t.Any:
            gen = generator_or_function(*args, **kwargs)  # type: ignore[operator]
            return stream_with_context(gen)

        return update_wrapper(decorator, generator_or_function)  # type: ignore[arg-type]

    def generator() -> t.Iterator[t.AnyStr]:
        if (req_ctx := _cv_request.get(None)) is None:
            raise RuntimeError(
                "'stream_with_context' can only be used when a request"
                " context is active, such as in a view function."
            )

        app_ctx = _cv_app.get()
        # Setup code below will run the generator to this point, so that the
        # current contexts are recorded. The contexts must be pushed after,
        # otherwise their ContextVar will record the wrong event loop during
        # async view functions.
        yield None  # type: ignore[misc]

        # Push the app context first, so that the request context does not
        # automatically create and push a different app context.
        with app_ctx, req_ctx:
            try:
                yield from gen
            finally:
                # Clean up in case the user wrapped a WSGI iterator.
                if hasattr(gen, "close"):
                    gen.close()

    # Execute the generator to the sentinel value. This ensures the context is
    # preserved in the generator's state. Further iteration will push the
    # context and yield from the original iterator.
    wrapped_g = generator()
    next(wrapped_g)
    return wrapped_g
```
===== 2 =====
```
     .. versionadded:: 0.9
     """
     try:
-        gen = iter(generator_or_function)  # type: ignore[arg-type]
+        gen = generator_or_function()  # type: ignore[arg-type]
     except TypeError:
 
         def decorator(*args: t.Any, **kwargs: t.Any) -> t.Any:
```
```
def stream_with_context(
    generator_or_function: t.Iterator[t.AnyStr] | t.Callable[..., t.Iterator[t.AnyStr]],
) -> t.Iterator[t.AnyStr] | t.Callable[[t.Iterator[t.AnyStr]], t.Iterator[t.AnyStr]]:
    """Wrap a response generator function so that it runs inside the current
    request context. This keeps :data:`request`, :data:`session`, and :data:`g`
    available, even though at the point the generator runs the request context
    will typically have ended.

    Use it as a decorator on a generator function:

    .. code-block:: python

        from flask import stream_with_context, request, Response

        @app.get("/stream")
        def streamed_response():
            @stream_with_context
            def generate():
                yield "Hello "
                yield request.args["name"]
                yield "!"

            return Response(generate())

    Or use it as a wrapper around a created generator:

    .. code-block:: python

        from flask import stream_with_context, request, Response

        @app.get("/stream")
        def streamed_response():
            def generate():
                yield "Hello "
                yield request.args["name"]
                yield "!"

            return Response(stream_with_context(generate()))

    .. versionadded:: 0.9
    """
    try:
        gen = generator_or_function()  # type: ignore[arg-type]
    except TypeError:

        def decorator(*args: t.Any, **kwargs: t.Any) -> t.Any:
            gen = generator_or_function(*args, **kwargs)  # type: ignore[operator]
            return stream_with_context(gen)

        return update_wrapper(decorator, generator_or_function)  # type: ignore[arg-type]

    def generator() -> t.Iterator[t.AnyStr]:
        if (req_ctx := _cv_request.get(None)) is None:
            raise RuntimeError(
                "'stream_with_context' can only be used when a request"
                " context is active, such as in a view function."
            )

        app_ctx = _cv_app.get()
        # Setup code below will run the generator to this point, so that the
        # current contexts are recorded. The contexts must be pushed after,
        # otherwise their ContextVar will record the wrong event loop during
        # async view functions.
        yield None  # type: ignore[misc]

        # Push the app context first, so that the request context does not
        # automatically create and push a different app context.
        with app_ctx, req_ctx:
            try:
                yield from gen
            finally:
                # Clean up in case the user wrapped a WSGI iterator.
                if hasattr(gen, "close"):
                    gen.close()

    # Execute the generator to the sentinel value. This ensures the context is
    # preserved in the generator's state. Further iteration will push the
    # context and yield from the original iterator.
    wrapped_g = generator()
    next(wrapped_g)
    return wrapped_g
```
===== 3 =====
```
     .. versionadded:: 0.9
     """
     try:
-        gen = iter(generator_or_function)  # type: ignore[arg-type]
+        gen = iter(None)  # type: ignore[arg-type]
     except TypeError:
 
         def decorator(*args: t.Any, **kwargs: t.Any) -> t.Any:
@@ -78,4 +78,4 @@     # context and yield from the original iterator.
     wrapped_g = generator()
     next(wrapped_g)
-    return wrapped_g+    return wrapped_g
```
```
def stream_with_context(
    generator_or_function: t.Iterator[t.AnyStr] | t.Callable[..., t.Iterator[t.AnyStr]],
) -> t.Iterator[t.AnyStr] | t.Callable[[t.Iterator[t.AnyStr]], t.Iterator[t.AnyStr]]:
    """Wrap a response generator function so that it runs inside the current
    request context. This keeps :data:`request`, :data:`session`, and :data:`g`
    available, even though at the point the generator runs the request context
    will typically have ended.

    Use it as a decorator on a generator function:

    .. code-block:: python

        from flask import stream_with_context, request, Response

        @app.get("/stream")
        def streamed_response():
            @stream_with_context
            def generate():
                yield "Hello "
                yield request.args["name"]
                yield "!"

            return Response(generate())

    Or use it as a wrapper around a created generator:

    .. code-block:: python

        from flask import stream_with_context, request, Response

        @app.get("/stream")
        def streamed_response():
            def generate():
                yield "Hello "
                yield request.args["name"]
                yield "!"

            return Response(stream_with_context(generate()))

    .. versionadded:: 0.9
    """
    try:
        gen = iter(None)  # type: ignore[arg-type]
    except TypeError:

        def decorator(*args: t.Any, **kwargs: t.Any) -> t.Any:
            gen = generator_or_function(*args, **kwargs)  # type: ignore[operator]
            return stream_with_context(gen)

        return update_wrapper(decorator, generator_or_function)  # type: ignore[arg-type]

    def generator() -> t.Iterator[t.AnyStr]:
        if (req_ctx := _cv_request.get(None)) is None:
            raise RuntimeError(
                "'stream_with_context' can only be used when a request"
                " context is active, such as in a view function."
            )

        app_ctx = _cv_app.get()
        # Setup code below will run the generator to this point, so that the
        # current contexts are recorded. The contexts must be pushed after,
        # otherwise their ContextVar will record the wrong event loop during
        # async view functions.
        yield None  # type: ignore[misc]

        # Push the app context first, so that the request context does not
        # automatically create and push a different app context.
        with app_ctx, req_ctx:
            try:
                yield from gen
            finally:
                # Clean up in case the user wrapped a WSGI iterator.
                if hasattr(gen, "close"):
                    gen.close()

    # Execute the generator to the sentinel value. This ensures the context is
    # preserved in the generator's state. Further iteration will push the
    # context and yield from the original iterator.
    wrapped_g = generator()
    next(wrapped_g)
    return wrapped_g

```
===== 4 =====
```
     .. versionadded:: 0.9
     """
     try:
-        gen = iter(generator_or_function)  # type: ignore[arg-type]
+        gen = list(generator_or_function)  # type: ignore[arg-type]
     except TypeError:
 
         def decorator(*args: t.Any, **kwargs: t.Any) -> t.Any:
```
```
def stream_with_context(
    generator_or_function: t.Iterator[t.AnyStr] | t.Callable[..., t.Iterator[t.AnyStr]],
) -> t.Iterator[t.AnyStr] | t.Callable[[t.Iterator[t.AnyStr]], t.Iterator[t.AnyStr]]:
    """Wrap a response generator function so that it runs inside the current
    request context. This keeps :data:`request`, :data:`session`, and :data:`g`
    available, even though at the point the generator runs the request context
    will typically have ended.

    Use it as a decorator on a generator function:

    .. code-block:: python

        from flask import stream_with_context, request, Response

        @app.get("/stream")
        def streamed_response():
            @stream_with_context
            def generate():
                yield "Hello "
                yield request.args["name"]
                yield "!"

            return Response(generate())

    Or use it as a wrapper around a created generator:

    .. code-block:: python

        from flask import stream_with_context, request, Response

        @app.get("/stream")
        def streamed_response():
            def generate():
                yield "Hello "
                yield request.args["name"]
                yield "!"

            return Response(stream_with_context(generate()))

    .. versionadded:: 0.9
    """
    try:
        gen = list(generator_or_function)  # type: ignore[arg-type]
    except TypeError:

        def decorator(*args: t.Any, **kwargs: t.Any) -> t.Any:
            gen = generator_or_function(*args, **kwargs)  # type: ignore[operator]
            return stream_with_context(gen)

        return update_wrapper(decorator, generator_or_function)  # type: ignore[arg-type]

    def generator() -> t.Iterator[t.AnyStr]:
        if (req_ctx := _cv_request.get(None)) is None:
            raise RuntimeError(
                "'stream_with_context' can only be used when a request"
                " context is active, such as in a view function."
            )

        app_ctx = _cv_app.get()
        # Setup code below will run the generator to this point, so that the
        # current contexts are recorded. The contexts must be pushed after,
        # otherwise their ContextVar will record the wrong event loop during
        # async view functions.
        yield None  # type: ignore[misc]

        # Push the app context first, so that the request context does not
        # automatically create and push a different app context.
        with app_ctx, req_ctx:
            try:
                yield from gen
            finally:
                # Clean up in case the user wrapped a WSGI iterator.
                if hasattr(gen, "close"):
                    gen.close()

    # Execute the generator to the sentinel value. This ensures the context is
    # preserved in the generator's state. Further iteration will push the
    # context and yield from the original iterator.
    wrapped_g = generator()
    next(wrapped_g)
    return wrapped_g
```
===== 5 =====
```
     except TypeError:
 
         def decorator(*args: t.Any, **kwargs: t.Any) -> t.Any:
-            gen = generator_or_function(*args, **kwargs)  # type: ignore[operator]
+            gen = None  # type: ignore[operator]
             return stream_with_context(gen)
 
         return update_wrapper(decorator, generator_or_function)  # type: ignore[arg-type]
@@ -78,4 +78,4 @@     # context and yield from the original iterator.
     wrapped_g = generator()
     next(wrapped_g)
-    return wrapped_g+    return wrapped_g
```
```
def stream_with_context(
    generator_or_function: t.Iterator[t.AnyStr] | t.Callable[..., t.Iterator[t.AnyStr]],
) -> t.Iterator[t.AnyStr] | t.Callable[[t.Iterator[t.AnyStr]], t.Iterator[t.AnyStr]]:
    """Wrap a response generator function so that it runs inside the current
    request context. This keeps :data:`request`, :data:`session`, and :data:`g`
    available, even though at the point the generator runs the request context
    will typically have ended.

    Use it as a decorator on a generator function:

    .. code-block:: python

        from flask import stream_with_context, request, Response

        @app.get("/stream")
        def streamed_response():
            @stream_with_context
            def generate():
                yield "Hello "
                yield request.args["name"]
                yield "!"

            return Response(generate())

    Or use it as a wrapper around a created generator:

    .. code-block:: python

        from flask import stream_with_context, request, Response

        @app.get("/stream")
        def streamed_response():
            def generate():
                yield "Hello "
                yield request.args["name"]
                yield "!"

            return Response(stream_with_context(generate()))

    .. versionadded:: 0.9
    """
    try:
        gen = iter(generator_or_function)  # type: ignore[arg-type]
    except TypeError:

        def decorator(*args: t.Any, **kwargs: t.Any) -> t.Any:
            gen = None  # type: ignore[operator]
            return stream_with_context(gen)

        return update_wrapper(decorator, generator_or_function)  # type: ignore[arg-type]

    def generator() -> t.Iterator[t.AnyStr]:
        if (req_ctx := _cv_request.get(None)) is None:
            raise RuntimeError(
                "'stream_with_context' can only be used when a request"
                " context is active, such as in a view function."
            )

        app_ctx = _cv_app.get()
        # Setup code below will run the generator to this point, so that the
        # current contexts are recorded. The contexts must be pushed after,
        # otherwise their ContextVar will record the wrong event loop during
        # async view functions.
        yield None  # type: ignore[misc]

        # Push the app context first, so that the request context does not
        # automatically create and push a different app context.
        with app_ctx, req_ctx:
            try:
                yield from gen
            finally:
                # Clean up in case the user wrapped a WSGI iterator.
                if hasattr(gen, "close"):
                    gen.close()

    # Execute the generator to the sentinel value. This ensures the context is
    # preserved in the generator's state. Further iteration will push the
    # context and yield from the original iterator.
    wrapped_g = generator()
    next(wrapped_g)
    return wrapped_g

```
===== 6 =====
```
     except TypeError:
 
         def decorator(*args: t.Any, **kwargs: t.Any) -> t.Any:
-            gen = generator_or_function(*args, **kwargs)  # type: ignore[operator]
+            gen = generator_or_function(**kwargs)  # type: ignore[operator]
             return stream_with_context(gen)
 
         return update_wrapper(decorator, generator_or_function)  # type: ignore[arg-type]
@@ -78,4 +78,4 @@     # context and yield from the original iterator.
     wrapped_g = generator()
     next(wrapped_g)
-    return wrapped_g+    return wrapped_g
```
```
def stream_with_context(
    generator_or_function: t.Iterator[t.AnyStr] | t.Callable[..., t.Iterator[t.AnyStr]],
) -> t.Iterator[t.AnyStr] | t.Callable[[t.Iterator[t.AnyStr]], t.Iterator[t.AnyStr]]:
    """Wrap a response generator function so that it runs inside the current
    request context. This keeps :data:`request`, :data:`session`, and :data:`g`
    available, even though at the point the generator runs the request context
    will typically have ended.

    Use it as a decorator on a generator function:

    .. code-block:: python

        from flask import stream_with_context, request, Response

        @app.get("/stream")
        def streamed_response():
            @stream_with_context
            def generate():
                yield "Hello "
                yield request.args["name"]
                yield "!"

            return Response(generate())

    Or use it as a wrapper around a created generator:

    .. code-block:: python

        from flask import stream_with_context, request, Response

        @app.get("/stream")
        def streamed_response():
            def generate():
                yield "Hello "
                yield request.args["name"]
                yield "!"

            return Response(stream_with_context(generate()))

    .. versionadded:: 0.9
    """
    try:
        gen = iter(generator_or_function)  # type: ignore[arg-type]
    except TypeError:

        def decorator(*args: t.Any, **kwargs: t.Any) -> t.Any:
            gen = generator_or_function(**kwargs)  # type: ignore[operator]
            return stream_with_context(gen)

        return update_wrapper(decorator, generator_or_function)  # type: ignore[arg-type]

    def generator() -> t.Iterator[t.AnyStr]:
        if (req_ctx := _cv_request.get(None)) is None:
            raise RuntimeError(
                "'stream_with_context' can only be used when a request"
                " context is active, such as in a view function."
            )

        app_ctx = _cv_app.get()
        # Setup code below will run the generator to this point, so that the
        # current contexts are recorded. The contexts must be pushed after,
        # otherwise their ContextVar will record the wrong event loop during
        # async view functions.
        yield None  # type: ignore[misc]

        # Push the app context first, so that the request context does not
        # automatically create and push a different app context.
        with app_ctx, req_ctx:
            try:
                yield from gen
            finally:
                # Clean up in case the user wrapped a WSGI iterator.
                if hasattr(gen, "close"):
                    gen.close()

    # Execute the generator to the sentinel value. This ensures the context is
    # preserved in the generator's state. Further iteration will push the
    # context and yield from the original iterator.
    wrapped_g = generator()
    next(wrapped_g)
    return wrapped_g

```
===== 7 =====
```
     except TypeError:
 
         def decorator(*args: t.Any, **kwargs: t.Any) -> t.Any:
-            gen = generator_or_function(*args, **kwargs)  # type: ignore[operator]
+            gen = generator_or_function(*args, **kwargs) if args else None  # type: ignore[operator]
             return stream_with_context(gen)
 
         return update_wrapper(decorator, generator_or_function)  # type: ignore[arg-type]
```
```
def stream_with_context(
    generator_or_function: t.Iterator[t.AnyStr] | t.Callable[..., t.Iterator[t.AnyStr]],
) -> t.Iterator[t.AnyStr] | t.Callable[[t.Iterator[t.AnyStr]], t.Iterator[t.AnyStr]]:
    """Wrap a response generator function so that it runs inside the current
    request context. This keeps :data:`request`, :data:`session`, and :data:`g`
    available, even though at the point the generator runs the request context
    will typically have ended.

    Use it as a decorator on a generator function:

    .. code-block:: python

        from flask import stream_with_context, request, Response

        @app.get("/stream")
        def streamed_response():
            @stream_with_context
            def generate():
                yield "Hello "
                yield request.args["name"]
                yield "!"

            return Response(generate())

    Or use it as a wrapper around a created generator:

    .. code-block:: python

        from flask import stream_with_context, request, Response

        @app.get("/stream")
        def streamed_response():
            def generate():
                yield "Hello "
                yield request.args["name"]
                yield "!"

            return Response(stream_with_context(generate()))

    .. versionadded:: 0.9
    """
    try:
        gen = iter(generator_or_function)  # type: ignore[arg-type]
    except TypeError:

        def decorator(*args: t.Any, **kwargs: t.Any) -> t.Any:
            gen = generator_or_function(*args, **kwargs) if args else None  # type: ignore[operator]
            return stream_with_context(gen)

        return update_wrapper(decorator, generator_or_function)  # type: ignore[arg-type]

    def generator() -> t.Iterator[t.AnyStr]:
        if (req_ctx := _cv_request.get(None)) is None:
            raise RuntimeError(
                "'stream_with_context' can only be used when a request"
                " context is active, such as in a view function."
            )

        app_ctx = _cv_app.get()
        # Setup code below will run the generator to this point, so that the
        # current contexts are recorded. The contexts must be pushed after,
        # otherwise their ContextVar will record the wrong event loop during
        # async view functions.
        yield None  # type: ignore[misc]

        # Push the app context first, so that the request context does not
        # automatically create and push a different app context.
        with app_ctx, req_ctx:
            try:
                yield from gen
            finally:
                # Clean up in case the user wrapped a WSGI iterator.
                if hasattr(gen, "close"):
                    gen.close()

    # Execute the generator to the sentinel value. This ensures the context is
    # preserved in the generator's state. Further iteration will push the
    # context and yield from the original iterator.
    wrapped_g = generator()
    next(wrapped_g)
    return wrapped_g
```
===== 8 =====
```
 
         def decorator(*args: t.Any, **kwargs: t.Any) -> t.Any:
             gen = generator_or_function(*args, **kwargs)  # type: ignore[operator]
-            return stream_with_context(gen)
+            return gen  # This returns the original generator without wrapping it in the context.
 
         return update_wrapper(decorator, generator_or_function)  # type: ignore[arg-type]
```
```
def stream_with_context(
    generator_or_function: t.Iterator[t.AnyStr] | t.Callable[..., t.Iterator[t.AnyStr]],
) -> t.Iterator[t.AnyStr] | t.Callable[[t.Iterator[t.AnyStr]], t.Iterator[t.AnyStr]]:
    """Wrap a response generator function so that it runs inside the current
    request context. This keeps :data:`request`, :data:`session`, and :data:`g`
    available, even though at the point the generator runs the request context
    will typically have ended.

    Use it as a decorator on a generator function:

    .. code-block:: python

        from flask import stream_with_context, request, Response

        @app.get("/stream")
        def streamed_response():
            @stream_with_context
            def generate():
                yield "Hello "
                yield request.args["name"]
                yield "!"

            return Response(generate())

    Or use it as a wrapper around a created generator:

    .. code-block:: python

        from flask import stream_with_context, request, Response

        @app.get("/stream")
        def streamed_response():
            def generate():
                yield "Hello "
                yield request.args["name"]
                yield "!"

            return Response(stream_with_context(generate()))

    .. versionadded:: 0.9
    """
    try:
        gen = iter(generator_or_function)  # type: ignore[arg-type]
    except TypeError:

        def decorator(*args: t.Any, **kwargs: t.Any) -> t.Any:
            gen = generator_or_function(*args, **kwargs)  # type: ignore[operator]
            return gen  # This returns the original generator without wrapping it in the context.

        return update_wrapper(decorator, generator_or_function)  # type: ignore[arg-type]

    def generator() -> t.Iterator[t.AnyStr]:
        if (req_ctx := _cv_request.get(None)) is None:
            raise RuntimeError(
                "'stream_with_context' can only be used when a request"
                " context is active, such as in a view function."
            )

        app_ctx = _cv_app.get()
        # Setup code below will run the generator to this point, so that the
        # current contexts are recorded. The contexts must be pushed after,
        # otherwise their ContextVar will record the wrong event loop during
        # async view functions.
        yield None  # type: ignore[misc]

        # Push the app context first, so that the request context does not
        # automatically create and push a different app context.
        with app_ctx, req_ctx:
            try:
                yield from gen
            finally:
                # Clean up in case the user wrapped a WSGI iterator.
                if hasattr(gen, "close"):
                    gen.close()

    # Execute the generator to the sentinel value. This ensures the context is
    # preserved in the generator's state. Further iteration will push the
    # context and yield from the original iterator.
    wrapped_g = generator()
    next(wrapped_g)
    return wrapped_g
```
===== 9 =====
```
 
         def decorator(*args: t.Any, **kwargs: t.Any) -> t.Any:
             gen = generator_or_function(*args, **kwargs)  # type: ignore[operator]
-            return stream_with_context(gen)
+            return iter(gen)  # This creates a new iterator from the generator, losing the context.
 
         return update_wrapper(decorator, generator_or_function)  # type: ignore[arg-type]
```
```
def stream_with_context(
    generator_or_function: t.Iterator[t.AnyStr] | t.Callable[..., t.Iterator[t.AnyStr]],
) -> t.Iterator[t.AnyStr] | t.Callable[[t.Iterator[t.AnyStr]], t.Iterator[t.AnyStr]]:
    """Wrap a response generator function so that it runs inside the current
    request context. This keeps :data:`request`, :data:`session`, and :data:`g`
    available, even though at the point the generator runs the request context
    will typically have ended.

    Use it as a decorator on a generator function:

    .. code-block:: python

        from flask import stream_with_context, request, Response

        @app.get("/stream")
        def streamed_response():
            @stream_with_context
            def generate():
                yield "Hello "
                yield request.args["name"]
                yield "!"

            return Response(generate())

    Or use it as a wrapper around a created generator:

    .. code-block:: python

        from flask import stream_with_context, request, Response

        @app.get("/stream")
        def streamed_response():
            def generate():
                yield "Hello "
                yield request.args["name"]
                yield "!"

            return Response(stream_with_context(generate()))

    .. versionadded:: 0.9
    """
    try:
        gen = iter(generator_or_function)  # type: ignore[arg-type]
    except TypeError:

        def decorator(*args: t.Any, **kwargs: t.Any) -> t.Any:
            gen = generator_or_function(*args, **kwargs)  # type: ignore[operator]
            return iter(gen)  # This creates a new iterator from the generator, losing the context.

        return update_wrapper(decorator, generator_or_function)  # type: ignore[arg-type]

    def generator() -> t.Iterator[t.AnyStr]:
        if (req_ctx := _cv_request.get(None)) is None:
            raise RuntimeError(
                "'stream_with_context' can only be used when a request"
                " context is active, such as in a view function."
            )

        app_ctx = _cv_app.get()
        # Setup code below will run the generator to this point, so that the
        # current contexts are recorded. The contexts must be pushed after,
        # otherwise their ContextVar will record the wrong event loop during
        # async view functions.
        yield None  # type: ignore[misc]

        # Push the app context first, so that the request context does not
        # automatically create and push a different app context.
        with app_ctx, req_ctx:
            try:
                yield from gen
            finally:
                # Clean up in case the user wrapped a WSGI iterator.
                if hasattr(gen, "close"):
                    gen.close()

    # Execute the generator to the sentinel value. This ensures the context is
    # preserved in the generator's state. Further iteration will push the
    # context and yield from the original iterator.
    wrapped_g = generator()
    next(wrapped_g)
    return wrapped_g
```
===== 10 =====
```
 
         def decorator(*args: t.Any, **kwargs: t.Any) -> t.Any:
             gen = generator_or_function(*args, **kwargs)  # type: ignore[operator]
-            return stream_with_context(gen)
+            return stream_with_context(None)
 
         return update_wrapper(decorator, generator_or_function)  # type: ignore[arg-type]
 
@@ -78,4 +78,4 @@     # context and yield from the original iterator.
     wrapped_g = generator()
     next(wrapped_g)
-    return wrapped_g+    return wrapped_g
```
```
def stream_with_context(
    generator_or_function: t.Iterator[t.AnyStr] | t.Callable[..., t.Iterator[t.AnyStr]],
) -> t.Iterator[t.AnyStr] | t.Callable[[t.Iterator[t.AnyStr]], t.Iterator[t.AnyStr]]:
    """Wrap a response generator function so that it runs inside the current
    request context. This keeps :data:`request`, :data:`session`, and :data:`g`
    available, even though at the point the generator runs the request context
    will typically have ended.

    Use it as a decorator on a generator function:

    .. code-block:: python

        from flask import stream_with_context, request, Response

        @app.get("/stream")
        def streamed_response():
            @stream_with_context
            def generate():
                yield "Hello "
                yield request.args["name"]
                yield "!"

            return Response(generate())

    Or use it as a wrapper around a created generator:

    .. code-block:: python

        from flask import stream_with_context, request, Response

        @app.get("/stream")
        def streamed_response():
            def generate():
                yield "Hello "
                yield request.args["name"]
                yield "!"

            return Response(stream_with_context(generate()))

    .. versionadded:: 0.9
    """
    try:
        gen = iter(generator_or_function)  # type: ignore[arg-type]
    except TypeError:

        def decorator(*args: t.Any, **kwargs: t.Any) -> t.Any:
            gen = generator_or_function(*args, **kwargs)  # type: ignore[operator]
            return stream_with_context(None)

        return update_wrapper(decorator, generator_or_function)  # type: ignore[arg-type]

    def generator() -> t.Iterator[t.AnyStr]:
        if (req_ctx := _cv_request.get(None)) is None:
            raise RuntimeError(
                "'stream_with_context' can only be used when a request"
                " context is active, such as in a view function."
            )

        app_ctx = _cv_app.get()
        # Setup code below will run the generator to this point, so that the
        # current contexts are recorded. The contexts must be pushed after,
        # otherwise their ContextVar will record the wrong event loop during
        # async view functions.
        yield None  # type: ignore[misc]

        # Push the app context first, so that the request context does not
        # automatically create and push a different app context.
        with app_ctx, req_ctx:
            try:
                yield from gen
            finally:
                # Clean up in case the user wrapped a WSGI iterator.
                if hasattr(gen, "close"):
                    gen.close()

    # Execute the generator to the sentinel value. This ensures the context is
    # preserved in the generator's state. Further iteration will push the
    # context and yield from the original iterator.
    wrapped_g = generator()
    next(wrapped_g)
    return wrapped_g

```
===== 11 =====
```
 
         def decorator(*args: t.Any, **kwargs: t.Any) -> t.Any:
             gen = generator_or_function(*args, **kwargs)  # type: ignore[operator]
-            return stream_with_context(gen)
+            return stream_with_context(None)  # This passes None, which will not yield any values.
 
         return update_wrapper(decorator, generator_or_function)  # type: ignore[arg-type]
```
```
def stream_with_context(
    generator_or_function: t.Iterator[t.AnyStr] | t.Callable[..., t.Iterator[t.AnyStr]],
) -> t.Iterator[t.AnyStr] | t.Callable[[t.Iterator[t.AnyStr]], t.Iterator[t.AnyStr]]:
    """Wrap a response generator function so that it runs inside the current
    request context. This keeps :data:`request`, :data:`session`, and :data:`g`
    available, even though at the point the generator runs the request context
    will typically have ended.

    Use it as a decorator on a generator function:

    .. code-block:: python

        from flask import stream_with_context, request, Response

        @app.get("/stream")
        def streamed_response():
            @stream_with_context
            def generate():
                yield "Hello "
                yield request.args["name"]
                yield "!"

            return Response(generate())

    Or use it as a wrapper around a created generator:

    .. code-block:: python

        from flask import stream_with_context, request, Response

        @app.get("/stream")
        def streamed_response():
            def generate():
                yield "Hello "
                yield request.args["name"]
                yield "!"

            return Response(stream_with_context(generate()))

    .. versionadded:: 0.9
    """
    try:
        gen = iter(generator_or_function)  # type: ignore[arg-type]
    except TypeError:

        def decorator(*args: t.Any, **kwargs: t.Any) -> t.Any:
            gen = generator_or_function(*args, **kwargs)  # type: ignore[operator]
            return stream_with_context(None)  # This passes None, which will not yield any values.

        return update_wrapper(decorator, generator_or_function)  # type: ignore[arg-type]

    def generator() -> t.Iterator[t.AnyStr]:
        if (req_ctx := _cv_request.get(None)) is None:
            raise RuntimeError(
                "'stream_with_context' can only be used when a request"
                " context is active, such as in a view function."
            )

        app_ctx = _cv_app.get()
        # Setup code below will run the generator to this point, so that the
        # current contexts are recorded. The contexts must be pushed after,
        # otherwise their ContextVar will record the wrong event loop during
        # async view functions.
        yield None  # type: ignore[misc]

        # Push the app context first, so that the request context does not
        # automatically create and push a different app context.
        with app_ctx, req_ctx:
            try:
                yield from gen
            finally:
                # Clean up in case the user wrapped a WSGI iterator.
                if hasattr(gen, "close"):
                    gen.close()

    # Execute the generator to the sentinel value. This ensures the context is
    # preserved in the generator's state. Further iteration will push the
    # context and yield from the original iterator.
    wrapped_g = generator()
    next(wrapped_g)
    return wrapped_g
```
===== 12 =====
```
 
         def decorator(*args: t.Any, **kwargs: t.Any) -> t.Any:
             gen = generator_or_function(*args, **kwargs)  # type: ignore[operator]
-            return stream_with_context(gen)
+            return stream_with_context([])  # This incorrectly wraps an empty list instead of the generator.
 
         return update_wrapper(decorator, generator_or_function)  # type: ignore[arg-type]
```
```
def stream_with_context(
    generator_or_function: t.Iterator[t.AnyStr] | t.Callable[..., t.Iterator[t.AnyStr]],
) -> t.Iterator[t.AnyStr] | t.Callable[[t.Iterator[t.AnyStr]], t.Iterator[t.AnyStr]]:
    """Wrap a response generator function so that it runs inside the current
    request context. This keeps :data:`request`, :data:`session`, and :data:`g`
    available, even though at the point the generator runs the request context
    will typically have ended.

    Use it as a decorator on a generator function:

    .. code-block:: python

        from flask import stream_with_context, request, Response

        @app.get("/stream")
        def streamed_response():
            @stream_with_context
            def generate():
                yield "Hello "
                yield request.args["name"]
                yield "!"

            return Response(generate())

    Or use it as a wrapper around a created generator:

    .. code-block:: python

        from flask import stream_with_context, request, Response

        @app.get("/stream")
        def streamed_response():
            def generate():
                yield "Hello "
                yield request.args["name"]
                yield "!"

            return Response(stream_with_context(generate()))

    .. versionadded:: 0.9
    """
    try:
        gen = iter(generator_or_function)  # type: ignore[arg-type]
    except TypeError:

        def decorator(*args: t.Any, **kwargs: t.Any) -> t.Any:
            gen = generator_or_function(*args, **kwargs)  # type: ignore[operator]
            return stream_with_context([])  # This incorrectly wraps an empty list instead of the generator.

        return update_wrapper(decorator, generator_or_function)  # type: ignore[arg-type]

    def generator() -> t.Iterator[t.AnyStr]:
        if (req_ctx := _cv_request.get(None)) is None:
            raise RuntimeError(
                "'stream_with_context' can only be used when a request"
                " context is active, such as in a view function."
            )

        app_ctx = _cv_app.get()
        # Setup code below will run the generator to this point, so that the
        # current contexts are recorded. The contexts must be pushed after,
        # otherwise their ContextVar will record the wrong event loop during
        # async view functions.
        yield None  # type: ignore[misc]

        # Push the app context first, so that the request context does not
        # automatically create and push a different app context.
        with app_ctx, req_ctx:
            try:
                yield from gen
            finally:
                # Clean up in case the user wrapped a WSGI iterator.
                if hasattr(gen, "close"):
                    gen.close()

    # Execute the generator to the sentinel value. This ensures the context is
    # preserved in the generator's state. Further iteration will push the
    # context and yield from the original iterator.
    wrapped_g = generator()
    next(wrapped_g)
    return wrapped_g
```
===== 13 =====
```
                 " context is active, such as in a view function."
             )
 
-        app_ctx = _cv_app.get()
+        app_ctx = None
         # Setup code below will run the generator to this point, so that the
         # current contexts are recorded. The contexts must be pushed after,
         # otherwise their ContextVar will record the wrong event loop during
@@ -78,4 +78,4 @@     # context and yield from the original iterator.
     wrapped_g = generator()
     next(wrapped_g)
-    return wrapped_g+    return wrapped_g
```
```
def stream_with_context(
    generator_or_function: t.Iterator[t.AnyStr] | t.Callable[..., t.Iterator[t.AnyStr]],
) -> t.Iterator[t.AnyStr] | t.Callable[[t.Iterator[t.AnyStr]], t.Iterator[t.AnyStr]]:
    """Wrap a response generator function so that it runs inside the current
    request context. This keeps :data:`request`, :data:`session`, and :data:`g`
    available, even though at the point the generator runs the request context
    will typically have ended.

    Use it as a decorator on a generator function:

    .. code-block:: python

        from flask import stream_with_context, request, Response

        @app.get("/stream")
        def streamed_response():
            @stream_with_context
            def generate():
                yield "Hello "
                yield request.args["name"]
                yield "!"

            return Response(generate())

    Or use it as a wrapper around a created generator:

    .. code-block:: python

        from flask import stream_with_context, request, Response

        @app.get("/stream")
        def streamed_response():
            def generate():
                yield "Hello "
                yield request.args["name"]
                yield "!"

            return Response(stream_with_context(generate()))

    .. versionadded:: 0.9
    """
    try:
        gen = iter(generator_or_function)  # type: ignore[arg-type]
    except TypeError:

        def decorator(*args: t.Any, **kwargs: t.Any) -> t.Any:
            gen = generator_or_function(*args, **kwargs)  # type: ignore[operator]
            return stream_with_context(gen)

        return update_wrapper(decorator, generator_or_function)  # type: ignore[arg-type]

    def generator() -> t.Iterator[t.AnyStr]:
        if (req_ctx := _cv_request.get(None)) is None:
            raise RuntimeError(
                "'stream_with_context' can only be used when a request"
                " context is active, such as in a view function."
            )

        app_ctx = None
        # Setup code below will run the generator to this point, so that the
        # current contexts are recorded. The contexts must be pushed after,
        # otherwise their ContextVar will record the wrong event loop during
        # async view functions.
        yield None  # type: ignore[misc]

        # Push the app context first, so that the request context does not
        # automatically create and push a different app context.
        with app_ctx, req_ctx:
            try:
                yield from gen
            finally:
                # Clean up in case the user wrapped a WSGI iterator.
                if hasattr(gen, "close"):
                    gen.close()

    # Execute the generator to the sentinel value. This ensures the context is
    # preserved in the generator's state. Further iteration will push the
    # context and yield from the original iterator.
    wrapped_g = generator()
    next(wrapped_g)
    return wrapped_g

```
===== 14 =====
```
                 " context is active, such as in a view function."
             )
 
-        app_ctx = _cv_app.get()
+        app_ctx = None  # This will lead to a RuntimeError later when used
         # Setup code below will run the generator to this point, so that the
         # current contexts are recorded. The contexts must be pushed after,
         # otherwise their ContextVar will record the wrong event loop during
```
```
def stream_with_context(
    generator_or_function: t.Iterator[t.AnyStr] | t.Callable[..., t.Iterator[t.AnyStr]],
) -> t.Iterator[t.AnyStr] | t.Callable[[t.Iterator[t.AnyStr]], t.Iterator[t.AnyStr]]:
    """Wrap a response generator function so that it runs inside the current
    request context. This keeps :data:`request`, :data:`session`, and :data:`g`
    available, even though at the point the generator runs the request context
    will typically have ended.

    Use it as a decorator on a generator function:

    .. code-block:: python

        from flask import stream_with_context, request, Response

        @app.get("/stream")
        def streamed_response():
            @stream_with_context
            def generate():
                yield "Hello "
                yield request.args["name"]
                yield "!"

            return Response(generate())

    Or use it as a wrapper around a created generator:

    .. code-block:: python

        from flask import stream_with_context, request, Response

        @app.get("/stream")
        def streamed_response():
            def generate():
                yield "Hello "
                yield request.args["name"]
                yield "!"

            return Response(stream_with_context(generate()))

    .. versionadded:: 0.9
    """
    try:
        gen = iter(generator_or_function)  # type: ignore[arg-type]
    except TypeError:

        def decorator(*args: t.Any, **kwargs: t.Any) -> t.Any:
            gen = generator_or_function(*args, **kwargs)  # type: ignore[operator]
            return stream_with_context(gen)

        return update_wrapper(decorator, generator_or_function)  # type: ignore[arg-type]

    def generator() -> t.Iterator[t.AnyStr]:
        if (req_ctx := _cv_request.get(None)) is None:
            raise RuntimeError(
                "'stream_with_context' can only be used when a request"
                " context is active, such as in a view function."
            )

        app_ctx = None  # This will lead to a RuntimeError later when used
        # Setup code below will run the generator to this point, so that the
        # current contexts are recorded. The contexts must be pushed after,
        # otherwise their ContextVar will record the wrong event loop during
        # async view functions.
        yield None  # type: ignore[misc]

        # Push the app context first, so that the request context does not
        # automatically create and push a different app context.
        with app_ctx, req_ctx:
            try:
                yield from gen
            finally:
                # Clean up in case the user wrapped a WSGI iterator.
                if hasattr(gen, "close"):
                    gen.close()

    # Execute the generator to the sentinel value. This ensures the context is
    # preserved in the generator's state. Further iteration will push the
    # context and yield from the original iterator.
    wrapped_g = generator()
    next(wrapped_g)
    return wrapped_g
```
===== 15 =====
```
                 " context is active, such as in a view function."
             )
 
-        app_ctx = _cv_app.get()
+        app_ctx = _cv_app.get() if False else None  # This will always result in None
         # Setup code below will run the generator to this point, so that the
         # current contexts are recorded. The contexts must be pushed after,
         # otherwise their ContextVar will record the wrong event loop during
```
```
def stream_with_context(
    generator_or_function: t.Iterator[t.AnyStr] | t.Callable[..., t.Iterator[t.AnyStr]],
) -> t.Iterator[t.AnyStr] | t.Callable[[t.Iterator[t.AnyStr]], t.Iterator[t.AnyStr]]:
    """Wrap a response generator function so that it runs inside the current
    request context. This keeps :data:`request`, :data:`session`, and :data:`g`
    available, even though at the point the generator runs the request context
    will typically have ended.

    Use it as a decorator on a generator function:

    .. code-block:: python

        from flask import stream_with_context, request, Response

        @app.get("/stream")
        def streamed_response():
            @stream_with_context
            def generate():
                yield "Hello "
                yield request.args["name"]
                yield "!"

            return Response(generate())

    Or use it as a wrapper around a created generator:

    .. code-block:: python

        from flask import stream_with_context, request, Response

        @app.get("/stream")
        def streamed_response():
            def generate():
                yield "Hello "
                yield request.args["name"]
                yield "!"

            return Response(stream_with_context(generate()))

    .. versionadded:: 0.9
    """
    try:
        gen = iter(generator_or_function)  # type: ignore[arg-type]
    except TypeError:

        def decorator(*args: t.Any, **kwargs: t.Any) -> t.Any:
            gen = generator_or_function(*args, **kwargs)  # type: ignore[operator]
            return stream_with_context(gen)

        return update_wrapper(decorator, generator_or_function)  # type: ignore[arg-type]

    def generator() -> t.Iterator[t.AnyStr]:
        if (req_ctx := _cv_request.get(None)) is None:
            raise RuntimeError(
                "'stream_with_context' can only be used when a request"
                " context is active, such as in a view function."
            )

        app_ctx = _cv_app.get() if False else None  # This will always result in None
        # Setup code below will run the generator to this point, so that the
        # current contexts are recorded. The contexts must be pushed after,
        # otherwise their ContextVar will record the wrong event loop during
        # async view functions.
        yield None  # type: ignore[misc]

        # Push the app context first, so that the request context does not
        # automatically create and push a different app context.
        with app_ctx, req_ctx:
            try:
                yield from gen
            finally:
                # Clean up in case the user wrapped a WSGI iterator.
                if hasattr(gen, "close"):
                    gen.close()

    # Execute the generator to the sentinel value. This ensures the context is
    # preserved in the generator's state. Further iteration will push the
    # context and yield from the original iterator.
    wrapped_g = generator()
    next(wrapped_g)
    return wrapped_g
```
===== 16 =====
```
                 yield from gen
             finally:
                 # Clean up in case the user wrapped a WSGI iterator.
-                if hasattr(gen, "close"):
+                if hasattr("close"):
                     gen.close()
 
     # Execute the generator to the sentinel value. This ensures the context is
@@ -78,4 +78,4 @@     # context and yield from the original iterator.
     wrapped_g = generator()
     next(wrapped_g)
-    return wrapped_g+    return wrapped_g
```
```
def stream_with_context(
    generator_or_function: t.Iterator[t.AnyStr] | t.Callable[..., t.Iterator[t.AnyStr]],
) -> t.Iterator[t.AnyStr] | t.Callable[[t.Iterator[t.AnyStr]], t.Iterator[t.AnyStr]]:
    """Wrap a response generator function so that it runs inside the current
    request context. This keeps :data:`request`, :data:`session`, and :data:`g`
    available, even though at the point the generator runs the request context
    will typically have ended.

    Use it as a decorator on a generator function:

    .. code-block:: python

        from flask import stream_with_context, request, Response

        @app.get("/stream")
        def streamed_response():
            @stream_with_context
            def generate():
                yield "Hello "
                yield request.args["name"]
                yield "!"

            return Response(generate())

    Or use it as a wrapper around a created generator:

    .. code-block:: python

        from flask import stream_with_context, request, Response

        @app.get("/stream")
        def streamed_response():
            def generate():
                yield "Hello "
                yield request.args["name"]
                yield "!"

            return Response(stream_with_context(generate()))

    .. versionadded:: 0.9
    """
    try:
        gen = iter(generator_or_function)  # type: ignore[arg-type]
    except TypeError:

        def decorator(*args: t.Any, **kwargs: t.Any) -> t.Any:
            gen = generator_or_function(*args, **kwargs)  # type: ignore[operator]
            return stream_with_context(gen)

        return update_wrapper(decorator, generator_or_function)  # type: ignore[arg-type]

    def generator() -> t.Iterator[t.AnyStr]:
        if (req_ctx := _cv_request.get(None)) is None:
            raise RuntimeError(
                "'stream_with_context' can only be used when a request"
                " context is active, such as in a view function."
            )

        app_ctx = _cv_app.get()
        # Setup code below will run the generator to this point, so that the
        # current contexts are recorded. The contexts must be pushed after,
        # otherwise their ContextVar will record the wrong event loop during
        # async view functions.
        yield None  # type: ignore[misc]

        # Push the app context first, so that the request context does not
        # automatically create and push a different app context.
        with app_ctx, req_ctx:
            try:
                yield from gen
            finally:
                # Clean up in case the user wrapped a WSGI iterator.
                if hasattr("close"):
                    gen.close()

    # Execute the generator to the sentinel value. This ensures the context is
    # preserved in the generator's state. Further iteration will push the
    # context and yield from the original iterator.
    wrapped_g = generator()
    next(wrapped_g)
    return wrapped_g

```
===== 17 =====
```
                 yield from gen
             finally:
                 # Clean up in case the user wrapped a WSGI iterator.
-                if hasattr(gen, "close"):
+                if hasattr(None, "close"):
                     gen.close()
 
     # Execute the generator to the sentinel value. This ensures the context is
@@ -78,4 +78,4 @@     # context and yield from the original iterator.
     wrapped_g = generator()
     next(wrapped_g)
-    return wrapped_g+    return wrapped_g
```
```
def stream_with_context(
    generator_or_function: t.Iterator[t.AnyStr] | t.Callable[..., t.Iterator[t.AnyStr]],
) -> t.Iterator[t.AnyStr] | t.Callable[[t.Iterator[t.AnyStr]], t.Iterator[t.AnyStr]]:
    """Wrap a response generator function so that it runs inside the current
    request context. This keeps :data:`request`, :data:`session`, and :data:`g`
    available, even though at the point the generator runs the request context
    will typically have ended.

    Use it as a decorator on a generator function:

    .. code-block:: python

        from flask import stream_with_context, request, Response

        @app.get("/stream")
        def streamed_response():
            @stream_with_context
            def generate():
                yield "Hello "
                yield request.args["name"]
                yield "!"

            return Response(generate())

    Or use it as a wrapper around a created generator:

    .. code-block:: python

        from flask import stream_with_context, request, Response

        @app.get("/stream")
        def streamed_response():
            def generate():
                yield "Hello "
                yield request.args["name"]
                yield "!"

            return Response(stream_with_context(generate()))

    .. versionadded:: 0.9
    """
    try:
        gen = iter(generator_or_function)  # type: ignore[arg-type]
    except TypeError:

        def decorator(*args: t.Any, **kwargs: t.Any) -> t.Any:
            gen = generator_or_function(*args, **kwargs)  # type: ignore[operator]
            return stream_with_context(gen)

        return update_wrapper(decorator, generator_or_function)  # type: ignore[arg-type]

    def generator() -> t.Iterator[t.AnyStr]:
        if (req_ctx := _cv_request.get(None)) is None:
            raise RuntimeError(
                "'stream_with_context' can only be used when a request"
                " context is active, such as in a view function."
            )

        app_ctx = _cv_app.get()
        # Setup code below will run the generator to this point, so that the
        # current contexts are recorded. The contexts must be pushed after,
        # otherwise their ContextVar will record the wrong event loop during
        # async view functions.
        yield None  # type: ignore[misc]

        # Push the app context first, so that the request context does not
        # automatically create and push a different app context.
        with app_ctx, req_ctx:
            try:
                yield from gen
            finally:
                # Clean up in case the user wrapped a WSGI iterator.
                if hasattr(None, "close"):
                    gen.close()

    # Execute the generator to the sentinel value. This ensures the context is
    # preserved in the generator's state. Further iteration will push the
    # context and yield from the original iterator.
    wrapped_g = generator()
    next(wrapped_g)
    return wrapped_g

```
===== 18 =====
```
                 yield from gen
             finally:
                 # Clean up in case the user wrapped a WSGI iterator.
-                if hasattr(gen, "close"):
+                if hasattr(gen, "CLOSE"):
                     gen.close()
 
     # Execute the generator to the sentinel value. This ensures the context is
@@ -78,4 +78,4 @@     # context and yield from the original iterator.
     wrapped_g = generator()
     next(wrapped_g)
-    return wrapped_g+    return wrapped_g
```
```
def stream_with_context(
    generator_or_function: t.Iterator[t.AnyStr] | t.Callable[..., t.Iterator[t.AnyStr]],
) -> t.Iterator[t.AnyStr] | t.Callable[[t.Iterator[t.AnyStr]], t.Iterator[t.AnyStr]]:
    """Wrap a response generator function so that it runs inside the current
    request context. This keeps :data:`request`, :data:`session`, and :data:`g`
    available, even though at the point the generator runs the request context
    will typically have ended.

    Use it as a decorator on a generator function:

    .. code-block:: python

        from flask import stream_with_context, request, Response

        @app.get("/stream")
        def streamed_response():
            @stream_with_context
            def generate():
                yield "Hello "
                yield request.args["name"]
                yield "!"

            return Response(generate())

    Or use it as a wrapper around a created generator:

    .. code-block:: python

        from flask import stream_with_context, request, Response

        @app.get("/stream")
        def streamed_response():
            def generate():
                yield "Hello "
                yield request.args["name"]
                yield "!"

            return Response(stream_with_context(generate()))

    .. versionadded:: 0.9
    """
    try:
        gen = iter(generator_or_function)  # type: ignore[arg-type]
    except TypeError:

        def decorator(*args: t.Any, **kwargs: t.Any) -> t.Any:
            gen = generator_or_function(*args, **kwargs)  # type: ignore[operator]
            return stream_with_context(gen)

        return update_wrapper(decorator, generator_or_function)  # type: ignore[arg-type]

    def generator() -> t.Iterator[t.AnyStr]:
        if (req_ctx := _cv_request.get(None)) is None:
            raise RuntimeError(
                "'stream_with_context' can only be used when a request"
                " context is active, such as in a view function."
            )

        app_ctx = _cv_app.get()
        # Setup code below will run the generator to this point, so that the
        # current contexts are recorded. The contexts must be pushed after,
        # otherwise their ContextVar will record the wrong event loop during
        # async view functions.
        yield None  # type: ignore[misc]

        # Push the app context first, so that the request context does not
        # automatically create and push a different app context.
        with app_ctx, req_ctx:
            try:
                yield from gen
            finally:
                # Clean up in case the user wrapped a WSGI iterator.
                if hasattr(gen, "CLOSE"):
                    gen.close()

    # Execute the generator to the sentinel value. This ensures the context is
    # preserved in the generator's state. Further iteration will push the
    # context and yield from the original iterator.
    wrapped_g = generator()
    next(wrapped_g)
    return wrapped_g

```
===== 19 =====
```
                 yield from gen
             finally:
                 # Clean up in case the user wrapped a WSGI iterator.
-                if hasattr(gen, "close"):
+                if hasattr(gen, "XXcloseXX"):
                     gen.close()
 
     # Execute the generator to the sentinel value. This ensures the context is
@@ -78,4 +78,4 @@     # context and yield from the original iterator.
     wrapped_g = generator()
     next(wrapped_g)
-    return wrapped_g+    return wrapped_g
```
```
def stream_with_context(
    generator_or_function: t.Iterator[t.AnyStr] | t.Callable[..., t.Iterator[t.AnyStr]],
) -> t.Iterator[t.AnyStr] | t.Callable[[t.Iterator[t.AnyStr]], t.Iterator[t.AnyStr]]:
    """Wrap a response generator function so that it runs inside the current
    request context. This keeps :data:`request`, :data:`session`, and :data:`g`
    available, even though at the point the generator runs the request context
    will typically have ended.

    Use it as a decorator on a generator function:

    .. code-block:: python

        from flask import stream_with_context, request, Response

        @app.get("/stream")
        def streamed_response():
            @stream_with_context
            def generate():
                yield "Hello "
                yield request.args["name"]
                yield "!"

            return Response(generate())

    Or use it as a wrapper around a created generator:

    .. code-block:: python

        from flask import stream_with_context, request, Response

        @app.get("/stream")
        def streamed_response():
            def generate():
                yield "Hello "
                yield request.args["name"]
                yield "!"

            return Response(stream_with_context(generate()))

    .. versionadded:: 0.9
    """
    try:
        gen = iter(generator_or_function)  # type: ignore[arg-type]
    except TypeError:

        def decorator(*args: t.Any, **kwargs: t.Any) -> t.Any:
            gen = generator_or_function(*args, **kwargs)  # type: ignore[operator]
            return stream_with_context(gen)

        return update_wrapper(decorator, generator_or_function)  # type: ignore[arg-type]

    def generator() -> t.Iterator[t.AnyStr]:
        if (req_ctx := _cv_request.get(None)) is None:
            raise RuntimeError(
                "'stream_with_context' can only be used when a request"
                " context is active, such as in a view function."
            )

        app_ctx = _cv_app.get()
        # Setup code below will run the generator to this point, so that the
        # current contexts are recorded. The contexts must be pushed after,
        # otherwise their ContextVar will record the wrong event loop during
        # async view functions.
        yield None  # type: ignore[misc]

        # Push the app context first, so that the request context does not
        # automatically create and push a different app context.
        with app_ctx, req_ctx:
            try:
                yield from gen
            finally:
                # Clean up in case the user wrapped a WSGI iterator.
                if hasattr(gen, "XXcloseXX"):
                    gen.close()

    # Execute the generator to the sentinel value. This ensures the context is
    # preserved in the generator's state. Further iteration will push the
    # context and yield from the original iterator.
    wrapped_g = generator()
    next(wrapped_g)
    return wrapped_g

```
===== 20 =====
```
                 yield from gen
             finally:
                 # Clean up in case the user wrapped a WSGI iterator.
-                if hasattr(gen, "close"):
+                if hasattr(gen, "close") and gen == "some_string":
                     gen.close()
 
     # Execute the generator to the sentinel value. This ensures the context is
```
```
def stream_with_context(
    generator_or_function: t.Iterator[t.AnyStr] | t.Callable[..., t.Iterator[t.AnyStr]],
) -> t.Iterator[t.AnyStr] | t.Callable[[t.Iterator[t.AnyStr]], t.Iterator[t.AnyStr]]:
    """Wrap a response generator function so that it runs inside the current
    request context. This keeps :data:`request`, :data:`session`, and :data:`g`
    available, even though at the point the generator runs the request context
    will typically have ended.

    Use it as a decorator on a generator function:

    .. code-block:: python

        from flask import stream_with_context, request, Response

        @app.get("/stream")
        def streamed_response():
            @stream_with_context
            def generate():
                yield "Hello "
                yield request.args["name"]
                yield "!"

            return Response(generate())

    Or use it as a wrapper around a created generator:

    .. code-block:: python

        from flask import stream_with_context, request, Response

        @app.get("/stream")
        def streamed_response():
            def generate():
                yield "Hello "
                yield request.args["name"]
                yield "!"

            return Response(stream_with_context(generate()))

    .. versionadded:: 0.9
    """
    try:
        gen = iter(generator_or_function)  # type: ignore[arg-type]
    except TypeError:

        def decorator(*args: t.Any, **kwargs: t.Any) -> t.Any:
            gen = generator_or_function(*args, **kwargs)  # type: ignore[operator]
            return stream_with_context(gen)

        return update_wrapper(decorator, generator_or_function)  # type: ignore[arg-type]

    def generator() -> t.Iterator[t.AnyStr]:
        if (req_ctx := _cv_request.get(None)) is None:
            raise RuntimeError(
                "'stream_with_context' can only be used when a request"
                " context is active, such as in a view function."
            )

        app_ctx = _cv_app.get()
        # Setup code below will run the generator to this point, so that the
        # current contexts are recorded. The contexts must be pushed after,
        # otherwise their ContextVar will record the wrong event loop during
        # async view functions.
        yield None  # type: ignore[misc]

        # Push the app context first, so that the request context does not
        # automatically create and push a different app context.
        with app_ctx, req_ctx:
            try:
                yield from gen
            finally:
                # Clean up in case the user wrapped a WSGI iterator.
                if hasattr(gen, "close") and gen == "some_string":
                    gen.close()

    # Execute the generator to the sentinel value. This ensures the context is
    # preserved in the generator's state. Further iteration will push the
    # context and yield from the original iterator.
    wrapped_g = generator()
    next(wrapped_g)
    return wrapped_g
```
===== 21 =====
```
                 yield from gen
             finally:
                 # Clean up in case the user wrapped a WSGI iterator.
-                if hasattr(gen, "close"):
+                if hasattr(gen, "close") and gen is True:
                     gen.close()
 
     # Execute the generator to the sentinel value. This ensures the context is
```
```
def stream_with_context(
    generator_or_function: t.Iterator[t.AnyStr] | t.Callable[..., t.Iterator[t.AnyStr]],
) -> t.Iterator[t.AnyStr] | t.Callable[[t.Iterator[t.AnyStr]], t.Iterator[t.AnyStr]]:
    """Wrap a response generator function so that it runs inside the current
    request context. This keeps :data:`request`, :data:`session`, and :data:`g`
    available, even though at the point the generator runs the request context
    will typically have ended.

    Use it as a decorator on a generator function:

    .. code-block:: python

        from flask import stream_with_context, request, Response

        @app.get("/stream")
        def streamed_response():
            @stream_with_context
            def generate():
                yield "Hello "
                yield request.args["name"]
                yield "!"

            return Response(generate())

    Or use it as a wrapper around a created generator:

    .. code-block:: python

        from flask import stream_with_context, request, Response

        @app.get("/stream")
        def streamed_response():
            def generate():
                yield "Hello "
                yield request.args["name"]
                yield "!"

            return Response(stream_with_context(generate()))

    .. versionadded:: 0.9
    """
    try:
        gen = iter(generator_or_function)  # type: ignore[arg-type]
    except TypeError:

        def decorator(*args: t.Any, **kwargs: t.Any) -> t.Any:
            gen = generator_or_function(*args, **kwargs)  # type: ignore[operator]
            return stream_with_context(gen)

        return update_wrapper(decorator, generator_or_function)  # type: ignore[arg-type]

    def generator() -> t.Iterator[t.AnyStr]:
        if (req_ctx := _cv_request.get(None)) is None:
            raise RuntimeError(
                "'stream_with_context' can only be used when a request"
                " context is active, such as in a view function."
            )

        app_ctx = _cv_app.get()
        # Setup code below will run the generator to this point, so that the
        # current contexts are recorded. The contexts must be pushed after,
        # otherwise their ContextVar will record the wrong event loop during
        # async view functions.
        yield None  # type: ignore[misc]

        # Push the app context first, so that the request context does not
        # automatically create and push a different app context.
        with app_ctx, req_ctx:
            try:
                yield from gen
            finally:
                # Clean up in case the user wrapped a WSGI iterator.
                if hasattr(gen, "close") and gen is True:
                    gen.close()

    # Execute the generator to the sentinel value. This ensures the context is
    # preserved in the generator's state. Further iteration will push the
    # context and yield from the original iterator.
    wrapped_g = generator()
    next(wrapped_g)
    return wrapped_g
```
===== 22 =====
```
                 yield from gen
             finally:
                 # Clean up in case the user wrapped a WSGI iterator.
-                if hasattr(gen, "close"):
+                if hasattr(gen, "close") and isinstance(gen, list):
                     gen.close()
 
     # Execute the generator to the sentinel value. This ensures the context is
```
```
def stream_with_context(
    generator_or_function: t.Iterator[t.AnyStr] | t.Callable[..., t.Iterator[t.AnyStr]],
) -> t.Iterator[t.AnyStr] | t.Callable[[t.Iterator[t.AnyStr]], t.Iterator[t.AnyStr]]:
    """Wrap a response generator function so that it runs inside the current
    request context. This keeps :data:`request`, :data:`session`, and :data:`g`
    available, even though at the point the generator runs the request context
    will typically have ended.

    Use it as a decorator on a generator function:

    .. code-block:: python

        from flask import stream_with_context, request, Response

        @app.get("/stream")
        def streamed_response():
            @stream_with_context
            def generate():
                yield "Hello "
                yield request.args["name"]
                yield "!"

            return Response(generate())

    Or use it as a wrapper around a created generator:

    .. code-block:: python

        from flask import stream_with_context, request, Response

        @app.get("/stream")
        def streamed_response():
            def generate():
                yield "Hello "
                yield request.args["name"]
                yield "!"

            return Response(stream_with_context(generate()))

    .. versionadded:: 0.9
    """
    try:
        gen = iter(generator_or_function)  # type: ignore[arg-type]
    except TypeError:

        def decorator(*args: t.Any, **kwargs: t.Any) -> t.Any:
            gen = generator_or_function(*args, **kwargs)  # type: ignore[operator]
            return stream_with_context(gen)

        return update_wrapper(decorator, generator_or_function)  # type: ignore[arg-type]

    def generator() -> t.Iterator[t.AnyStr]:
        if (req_ctx := _cv_request.get(None)) is None:
            raise RuntimeError(
                "'stream_with_context' can only be used when a request"
                " context is active, such as in a view function."
            )

        app_ctx = _cv_app.get()
        # Setup code below will run the generator to this point, so that the
        # current contexts are recorded. The contexts must be pushed after,
        # otherwise their ContextVar will record the wrong event loop during
        # async view functions.
        yield None  # type: ignore[misc]

        # Push the app context first, so that the request context does not
        # automatically create and push a different app context.
        with app_ctx, req_ctx:
            try:
                yield from gen
            finally:
                # Clean up in case the user wrapped a WSGI iterator.
                if hasattr(gen, "close") and isinstance(gen, list):
                    gen.close()

    # Execute the generator to the sentinel value. This ensures the context is
    # preserved in the generator's state. Further iteration will push the
    # context and yield from the original iterator.
    wrapped_g = generator()
    next(wrapped_g)
    return wrapped_g
```
===== 23 =====
```
                 yield from gen
             finally:
                 # Clean up in case the user wrapped a WSGI iterator.
-                if hasattr(gen, "close"):
+                if hasattr(gen, ):
                     gen.close()
 
     # Execute the generator to the sentinel value. This ensures the context is
@@ -78,4 +78,4 @@     # context and yield from the original iterator.
     wrapped_g = generator()
     next(wrapped_g)
-    return wrapped_g+    return wrapped_g
```
```
def stream_with_context(
    generator_or_function: t.Iterator[t.AnyStr] | t.Callable[..., t.Iterator[t.AnyStr]],
) -> t.Iterator[t.AnyStr] | t.Callable[[t.Iterator[t.AnyStr]], t.Iterator[t.AnyStr]]:
    """Wrap a response generator function so that it runs inside the current
    request context. This keeps :data:`request`, :data:`session`, and :data:`g`
    available, even though at the point the generator runs the request context
    will typically have ended.

    Use it as a decorator on a generator function:

    .. code-block:: python

        from flask import stream_with_context, request, Response

        @app.get("/stream")
        def streamed_response():
            @stream_with_context
            def generate():
                yield "Hello "
                yield request.args["name"]
                yield "!"

            return Response(generate())

    Or use it as a wrapper around a created generator:

    .. code-block:: python

        from flask import stream_with_context, request, Response

        @app.get("/stream")
        def streamed_response():
            def generate():
                yield "Hello "
                yield request.args["name"]
                yield "!"

            return Response(stream_with_context(generate()))

    .. versionadded:: 0.9
    """
    try:
        gen = iter(generator_or_function)  # type: ignore[arg-type]
    except TypeError:

        def decorator(*args: t.Any, **kwargs: t.Any) -> t.Any:
            gen = generator_or_function(*args, **kwargs)  # type: ignore[operator]
            return stream_with_context(gen)

        return update_wrapper(decorator, generator_or_function)  # type: ignore[arg-type]

    def generator() -> t.Iterator[t.AnyStr]:
        if (req_ctx := _cv_request.get(None)) is None:
            raise RuntimeError(
                "'stream_with_context' can only be used when a request"
                " context is active, such as in a view function."
            )

        app_ctx = _cv_app.get()
        # Setup code below will run the generator to this point, so that the
        # current contexts are recorded. The contexts must be pushed after,
        # otherwise their ContextVar will record the wrong event loop during
        # async view functions.
        yield None  # type: ignore[misc]

        # Push the app context first, so that the request context does not
        # automatically create and push a different app context.
        with app_ctx, req_ctx:
            try:
                yield from gen
            finally:
                # Clean up in case the user wrapped a WSGI iterator.
                if hasattr(gen, ):
                    gen.close()

    # Execute the generator to the sentinel value. This ensures the context is
    # preserved in the generator's state. Further iteration will push the
    # context and yield from the original iterator.
    wrapped_g = generator()
    next(wrapped_g)
    return wrapped_g

```
===== 24 =====
```
                 yield from gen
             finally:
                 # Clean up in case the user wrapped a WSGI iterator.
-                if hasattr(gen, "close"):
+                if hasattr(gen, None):
                     gen.close()
 
     # Execute the generator to the sentinel value. This ensures the context is
@@ -78,4 +78,4 @@     # context and yield from the original iterator.
     wrapped_g = generator()
     next(wrapped_g)
-    return wrapped_g+    return wrapped_g
```
```
def stream_with_context(
    generator_or_function: t.Iterator[t.AnyStr] | t.Callable[..., t.Iterator[t.AnyStr]],
) -> t.Iterator[t.AnyStr] | t.Callable[[t.Iterator[t.AnyStr]], t.Iterator[t.AnyStr]]:
    """Wrap a response generator function so that it runs inside the current
    request context. This keeps :data:`request`, :data:`session`, and :data:`g`
    available, even though at the point the generator runs the request context
    will typically have ended.

    Use it as a decorator on a generator function:

    .. code-block:: python

        from flask import stream_with_context, request, Response

        @app.get("/stream")
        def streamed_response():
            @stream_with_context
            def generate():
                yield "Hello "
                yield request.args["name"]
                yield "!"

            return Response(generate())

    Or use it as a wrapper around a created generator:

    .. code-block:: python

        from flask import stream_with_context, request, Response

        @app.get("/stream")
        def streamed_response():
            def generate():
                yield "Hello "
                yield request.args["name"]
                yield "!"

            return Response(stream_with_context(generate()))

    .. versionadded:: 0.9
    """
    try:
        gen = iter(generator_or_function)  # type: ignore[arg-type]
    except TypeError:

        def decorator(*args: t.Any, **kwargs: t.Any) -> t.Any:
            gen = generator_or_function(*args, **kwargs)  # type: ignore[operator]
            return stream_with_context(gen)

        return update_wrapper(decorator, generator_or_function)  # type: ignore[arg-type]

    def generator() -> t.Iterator[t.AnyStr]:
        if (req_ctx := _cv_request.get(None)) is None:
            raise RuntimeError(
                "'stream_with_context' can only be used when a request"
                " context is active, such as in a view function."
            )

        app_ctx = _cv_app.get()
        # Setup code below will run the generator to this point, so that the
        # current contexts are recorded. The contexts must be pushed after,
        # otherwise their ContextVar will record the wrong event loop during
        # async view functions.
        yield None  # type: ignore[misc]

        # Push the app context first, so that the request context does not
        # automatically create and push a different app context.
        with app_ctx, req_ctx:
            try:
                yield from gen
            finally:
                # Clean up in case the user wrapped a WSGI iterator.
                if hasattr(gen, None):
                    gen.close()

    # Execute the generator to the sentinel value. This ensures the context is
    # preserved in the generator's state. Further iteration will push the
    # context and yield from the original iterator.
    wrapped_g = generator()
    next(wrapped_g)
    return wrapped_g

```
===== 25 =====
```
                 yield from gen
             finally:
                 # Clean up in case the user wrapped a WSGI iterator.
-                if hasattr(gen, "close"):
+                if not hasattr(gen, "close"):
                     gen.close()
 
     # Execute the generator to the sentinel value. This ensures the context is
```
```
def stream_with_context(
    generator_or_function: t.Iterator[t.AnyStr] | t.Callable[..., t.Iterator[t.AnyStr]],
) -> t.Iterator[t.AnyStr] | t.Callable[[t.Iterator[t.AnyStr]], t.Iterator[t.AnyStr]]:
    """Wrap a response generator function so that it runs inside the current
    request context. This keeps :data:`request`, :data:`session`, and :data:`g`
    available, even though at the point the generator runs the request context
    will typically have ended.

    Use it as a decorator on a generator function:

    .. code-block:: python

        from flask import stream_with_context, request, Response

        @app.get("/stream")
        def streamed_response():
            @stream_with_context
            def generate():
                yield "Hello "
                yield request.args["name"]
                yield "!"

            return Response(generate())

    Or use it as a wrapper around a created generator:

    .. code-block:: python

        from flask import stream_with_context, request, Response

        @app.get("/stream")
        def streamed_response():
            def generate():
                yield "Hello "
                yield request.args["name"]
                yield "!"

            return Response(stream_with_context(generate()))

    .. versionadded:: 0.9
    """
    try:
        gen = iter(generator_or_function)  # type: ignore[arg-type]
    except TypeError:

        def decorator(*args: t.Any, **kwargs: t.Any) -> t.Any:
            gen = generator_or_function(*args, **kwargs)  # type: ignore[operator]
            return stream_with_context(gen)

        return update_wrapper(decorator, generator_or_function)  # type: ignore[arg-type]

    def generator() -> t.Iterator[t.AnyStr]:
        if (req_ctx := _cv_request.get(None)) is None:
            raise RuntimeError(
                "'stream_with_context' can only be used when a request"
                " context is active, such as in a view function."
            )

        app_ctx = _cv_app.get()
        # Setup code below will run the generator to this point, so that the
        # current contexts are recorded. The contexts must be pushed after,
        # otherwise their ContextVar will record the wrong event loop during
        # async view functions.
        yield None  # type: ignore[misc]

        # Push the app context first, so that the request context does not
        # automatically create and push a different app context.
        with app_ctx, req_ctx:
            try:
                yield from gen
            finally:
                # Clean up in case the user wrapped a WSGI iterator.
                if not hasattr(gen, "close"):
                    gen.close()

    # Execute the generator to the sentinel value. This ensures the context is
    # preserved in the generator's state. Further iteration will push the
    # context and yield from the original iterator.
    wrapped_g = generator()
    next(wrapped_g)
    return wrapped_g
```
===== 26 =====
```
             finally:
                 # Clean up in case the user wrapped a WSGI iterator.
                 if hasattr(gen, "close"):
-                    gen.close()
+                    gen = None  # This breaks the reference to the generator
 
     # Execute the generator to the sentinel value. This ensures the context is
     # preserved in the generator's state. Further iteration will push the
```
```
def stream_with_context(
    generator_or_function: t.Iterator[t.AnyStr] | t.Callable[..., t.Iterator[t.AnyStr]],
) -> t.Iterator[t.AnyStr] | t.Callable[[t.Iterator[t.AnyStr]], t.Iterator[t.AnyStr]]:
    """Wrap a response generator function so that it runs inside the current
    request context. This keeps :data:`request`, :data:`session`, and :data:`g`
    available, even though at the point the generator runs the request context
    will typically have ended.

    Use it as a decorator on a generator function:

    .. code-block:: python

        from flask import stream_with_context, request, Response

        @app.get("/stream")
        def streamed_response():
            @stream_with_context
            def generate():
                yield "Hello "
                yield request.args["name"]
                yield "!"

            return Response(generate())

    Or use it as a wrapper around a created generator:

    .. code-block:: python

        from flask import stream_with_context, request, Response

        @app.get("/stream")
        def streamed_response():
            def generate():
                yield "Hello "
                yield request.args["name"]
                yield "!"

            return Response(stream_with_context(generate()))

    .. versionadded:: 0.9
    """
    try:
        gen = iter(generator_or_function)  # type: ignore[arg-type]
    except TypeError:

        def decorator(*args: t.Any, **kwargs: t.Any) -> t.Any:
            gen = generator_or_function(*args, **kwargs)  # type: ignore[operator]
            return stream_with_context(gen)

        return update_wrapper(decorator, generator_or_function)  # type: ignore[arg-type]

    def generator() -> t.Iterator[t.AnyStr]:
        if (req_ctx := _cv_request.get(None)) is None:
            raise RuntimeError(
                "'stream_with_context' can only be used when a request"
                " context is active, such as in a view function."
            )

        app_ctx = _cv_app.get()
        # Setup code below will run the generator to this point, so that the
        # current contexts are recorded. The contexts must be pushed after,
        # otherwise their ContextVar will record the wrong event loop during
        # async view functions.
        yield None  # type: ignore[misc]

        # Push the app context first, so that the request context does not
        # automatically create and push a different app context.
        with app_ctx, req_ctx:
            try:
                yield from gen
            finally:
                # Clean up in case the user wrapped a WSGI iterator.
                if hasattr(gen, "close"):
                    gen = None  # This breaks the reference to the generator

    # Execute the generator to the sentinel value. This ensures the context is
    # preserved in the generator's state. Further iteration will push the
    # context and yield from the original iterator.
    wrapped_g = generator()
    next(wrapped_g)
    return wrapped_g
```
===== 27 =====
```
             finally:
                 # Clean up in case the user wrapped a WSGI iterator.
                 if hasattr(gen, "close"):
-                    gen.close()
+                    gen.__iter__()  # This does not close the generator
 
     # Execute the generator to the sentinel value. This ensures the context is
     # preserved in the generator's state. Further iteration will push the
```
```
def stream_with_context(
    generator_or_function: t.Iterator[t.AnyStr] | t.Callable[..., t.Iterator[t.AnyStr]],
) -> t.Iterator[t.AnyStr] | t.Callable[[t.Iterator[t.AnyStr]], t.Iterator[t.AnyStr]]:
    """Wrap a response generator function so that it runs inside the current
    request context. This keeps :data:`request`, :data:`session`, and :data:`g`
    available, even though at the point the generator runs the request context
    will typically have ended.

    Use it as a decorator on a generator function:

    .. code-block:: python

        from flask import stream_with_context, request, Response

        @app.get("/stream")
        def streamed_response():
            @stream_with_context
            def generate():
                yield "Hello "
                yield request.args["name"]
                yield "!"

            return Response(generate())

    Or use it as a wrapper around a created generator:

    .. code-block:: python

        from flask import stream_with_context, request, Response

        @app.get("/stream")
        def streamed_response():
            def generate():
                yield "Hello "
                yield request.args["name"]
                yield "!"

            return Response(stream_with_context(generate()))

    .. versionadded:: 0.9
    """
    try:
        gen = iter(generator_or_function)  # type: ignore[arg-type]
    except TypeError:

        def decorator(*args: t.Any, **kwargs: t.Any) -> t.Any:
            gen = generator_or_function(*args, **kwargs)  # type: ignore[operator]
            return stream_with_context(gen)

        return update_wrapper(decorator, generator_or_function)  # type: ignore[arg-type]

    def generator() -> t.Iterator[t.AnyStr]:
        if (req_ctx := _cv_request.get(None)) is None:
            raise RuntimeError(
                "'stream_with_context' can only be used when a request"
                " context is active, such as in a view function."
            )

        app_ctx = _cv_app.get()
        # Setup code below will run the generator to this point, so that the
        # current contexts are recorded. The contexts must be pushed after,
        # otherwise their ContextVar will record the wrong event loop during
        # async view functions.
        yield None  # type: ignore[misc]

        # Push the app context first, so that the request context does not
        # automatically create and push a different app context.
        with app_ctx, req_ctx:
            try:
                yield from gen
            finally:
                # Clean up in case the user wrapped a WSGI iterator.
                if hasattr(gen, "close"):
                    gen.__iter__()  # This does not close the generator

    # Execute the generator to the sentinel value. This ensures the context is
    # preserved in the generator's state. Further iteration will push the
    # context and yield from the original iterator.
    wrapped_g = generator()
    next(wrapped_g)
    return wrapped_g
```
===== 28 =====
```
             finally:
                 # Clean up in case the user wrapped a WSGI iterator.
                 if hasattr(gen, "close"):
-                    gen.close()
+                    gen.send(None)
 
     # Execute the generator to the sentinel value. This ensures the context is
     # preserved in the generator's state. Further iteration will push the
```
```
def stream_with_context(
    generator_or_function: t.Iterator[t.AnyStr] | t.Callable[..., t.Iterator[t.AnyStr]],
) -> t.Iterator[t.AnyStr] | t.Callable[[t.Iterator[t.AnyStr]], t.Iterator[t.AnyStr]]:
    """Wrap a response generator function so that it runs inside the current
    request context. This keeps :data:`request`, :data:`session`, and :data:`g`
    available, even though at the point the generator runs the request context
    will typically have ended.

    Use it as a decorator on a generator function:

    .. code-block:: python

        from flask import stream_with_context, request, Response

        @app.get("/stream")
        def streamed_response():
            @stream_with_context
            def generate():
                yield "Hello "
                yield request.args["name"]
                yield "!"

            return Response(generate())

    Or use it as a wrapper around a created generator:

    .. code-block:: python

        from flask import stream_with_context, request, Response

        @app.get("/stream")
        def streamed_response():
            def generate():
                yield "Hello "
                yield request.args["name"]
                yield "!"

            return Response(stream_with_context(generate()))

    .. versionadded:: 0.9
    """
    try:
        gen = iter(generator_or_function)  # type: ignore[arg-type]
    except TypeError:

        def decorator(*args: t.Any, **kwargs: t.Any) -> t.Any:
            gen = generator_or_function(*args, **kwargs)  # type: ignore[operator]
            return stream_with_context(gen)

        return update_wrapper(decorator, generator_or_function)  # type: ignore[arg-type]

    def generator() -> t.Iterator[t.AnyStr]:
        if (req_ctx := _cv_request.get(None)) is None:
            raise RuntimeError(
                "'stream_with_context' can only be used when a request"
                " context is active, such as in a view function."
            )

        app_ctx = _cv_app.get()
        # Setup code below will run the generator to this point, so that the
        # current contexts are recorded. The contexts must be pushed after,
        # otherwise their ContextVar will record the wrong event loop during
        # async view functions.
        yield None  # type: ignore[misc]

        # Push the app context first, so that the request context does not
        # automatically create and push a different app context.
        with app_ctx, req_ctx:
            try:
                yield from gen
            finally:
                # Clean up in case the user wrapped a WSGI iterator.
                if hasattr(gen, "close"):
                    gen.send(None)

    # Execute the generator to the sentinel value. This ensures the context is
    # preserved in the generator's state. Further iteration will push the
    # context and yield from the original iterator.
    wrapped_g = generator()
    next(wrapped_g)
    return wrapped_g
```
===== 29 =====
```
             finally:
                 # Clean up in case the user wrapped a WSGI iterator.
                 if hasattr(gen, "close"):
-                    gen.close()
+                    gen.throw(Exception("Forced error"))
 
     # Execute the generator to the sentinel value. This ensures the context is
     # preserved in the generator's state. Further iteration will push the
```
```
def stream_with_context(
    generator_or_function: t.Iterator[t.AnyStr] | t.Callable[..., t.Iterator[t.AnyStr]],
) -> t.Iterator[t.AnyStr] | t.Callable[[t.Iterator[t.AnyStr]], t.Iterator[t.AnyStr]]:
    """Wrap a response generator function so that it runs inside the current
    request context. This keeps :data:`request`, :data:`session`, and :data:`g`
    available, even though at the point the generator runs the request context
    will typically have ended.

    Use it as a decorator on a generator function:

    .. code-block:: python

        from flask import stream_with_context, request, Response

        @app.get("/stream")
        def streamed_response():
            @stream_with_context
            def generate():
                yield "Hello "
                yield request.args["name"]
                yield "!"

            return Response(generate())

    Or use it as a wrapper around a created generator:

    .. code-block:: python

        from flask import stream_with_context, request, Response

        @app.get("/stream")
        def streamed_response():
            def generate():
                yield "Hello "
                yield request.args["name"]
                yield "!"

            return Response(stream_with_context(generate()))

    .. versionadded:: 0.9
    """
    try:
        gen = iter(generator_or_function)  # type: ignore[arg-type]
    except TypeError:

        def decorator(*args: t.Any, **kwargs: t.Any) -> t.Any:
            gen = generator_or_function(*args, **kwargs)  # type: ignore[operator]
            return stream_with_context(gen)

        return update_wrapper(decorator, generator_or_function)  # type: ignore[arg-type]

    def generator() -> t.Iterator[t.AnyStr]:
        if (req_ctx := _cv_request.get(None)) is None:
            raise RuntimeError(
                "'stream_with_context' can only be used when a request"
                " context is active, such as in a view function."
            )

        app_ctx = _cv_app.get()
        # Setup code below will run the generator to this point, so that the
        # current contexts are recorded. The contexts must be pushed after,
        # otherwise their ContextVar will record the wrong event loop during
        # async view functions.
        yield None  # type: ignore[misc]

        # Push the app context first, so that the request context does not
        # automatically create and push a different app context.
        with app_ctx, req_ctx:
            try:
                yield from gen
            finally:
                # Clean up in case the user wrapped a WSGI iterator.
                if hasattr(gen, "close"):
                    gen.throw(Exception("Forced error"))

    # Execute the generator to the sentinel value. This ensures the context is
    # preserved in the generator's state. Further iteration will push the
    # context and yield from the original iterator.
    wrapped_g = generator()
    next(wrapped_g)
    return wrapped_g
```
===== 30 =====
```
     # preserved in the generator's state. Further iteration will push the
     # context and yield from the original iterator.
     wrapped_g = generator()
-    next(wrapped_g)
+    wrapped_g.close()
     return wrapped_g
```
```
def stream_with_context(
    generator_or_function: t.Iterator[t.AnyStr] | t.Callable[..., t.Iterator[t.AnyStr]],
) -> t.Iterator[t.AnyStr] | t.Callable[[t.Iterator[t.AnyStr]], t.Iterator[t.AnyStr]]:
    """Wrap a response generator function so that it runs inside the current
    request context. This keeps :data:`request`, :data:`session`, and :data:`g`
    available, even though at the point the generator runs the request context
    will typically have ended.

    Use it as a decorator on a generator function:

    .. code-block:: python

        from flask import stream_with_context, request, Response

        @app.get("/stream")
        def streamed_response():
            @stream_with_context
            def generate():
                yield "Hello "
                yield request.args["name"]
                yield "!"

            return Response(generate())

    Or use it as a wrapper around a created generator:

    .. code-block:: python

        from flask import stream_with_context, request, Response

        @app.get("/stream")
        def streamed_response():
            def generate():
                yield "Hello "
                yield request.args["name"]
                yield "!"

            return Response(stream_with_context(generate()))

    .. versionadded:: 0.9
    """
    try:
        gen = iter(generator_or_function)  # type: ignore[arg-type]
    except TypeError:

        def decorator(*args: t.Any, **kwargs: t.Any) -> t.Any:
            gen = generator_or_function(*args, **kwargs)  # type: ignore[operator]
            return stream_with_context(gen)

        return update_wrapper(decorator, generator_or_function)  # type: ignore[arg-type]

    def generator() -> t.Iterator[t.AnyStr]:
        if (req_ctx := _cv_request.get(None)) is None:
            raise RuntimeError(
                "'stream_with_context' can only be used when a request"
                " context is active, such as in a view function."
            )

        app_ctx = _cv_app.get()
        # Setup code below will run the generator to this point, so that the
        # current contexts are recorded. The contexts must be pushed after,
        # otherwise their ContextVar will record the wrong event loop during
        # async view functions.
        yield None  # type: ignore[misc]

        # Push the app context first, so that the request context does not
        # automatically create and push a different app context.
        with app_ctx, req_ctx:
            try:
                yield from gen
            finally:
                # Clean up in case the user wrapped a WSGI iterator.
                if hasattr(gen, "close"):
                    gen.close()

    # Execute the generator to the sentinel value. This ensures the context is
    # preserved in the generator's state. Further iteration will push the
    # context and yield from the original iterator.
    wrapped_g = generator()
    wrapped_g.close()
    return wrapped_g
```
