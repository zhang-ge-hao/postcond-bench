https://github.com/patrick-kidger/tinyio/blob/44909f813c7d652ade2e83fffed05500a3a8b9b7/./tinyio/_time.py#L31-L60
```
🈚️

yield
```
```
None
```
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
===== 0 =====
```
 
     def wrapper():
         out = yield coro
-        outs.append(out)
+        outs.append(None)
         done.set()
 
     yield {wrapper()}
```
```
def timeout(coro: Coro[_T], timeout_in_seconds: int | float) -> Coro[tuple[None | _T, bool]]:
    """`tinyio` coroutine for running a coroutine for at most `timeout_in_seconds`.

    **Arguments:**

    - `coro`: another coroutine.
    - `timeout_in_seconds`: the maximum number of seconds to allow `coro` to run for.

    **Returns:**

    A coroutine that an be `yield`ed on. This will return a pair of either `(output, True)` or `(None, False)`,
    corresponding to whether `coro` completed within the timeout or not.
    """
    done = Event()
    outs = []

    def wrapper():
        out = yield coro
        outs.append(None)
        done.set()

    yield {wrapper()}
    yield from done.wait(timeout_in_seconds)
    if len(outs) == 0:
        with contextlib.suppress(TimeoutError):
            coro.throw(TimeoutError)
        return None, False
    else:
        [out] = outs
        return out, True
```
===== 1 =====
```
 
     def wrapper():
         out = yield coro
-        outs.append(out)
+        outs.append(None)
         done.set()
 
     yield {wrapper()}
@@ -27,4 +27,4 @@         return None, False
     else:
         [out] = outs
-        return out, True+        return out, True
```
```
def timeout(coro: Coro[_T], timeout_in_seconds: int | float) -> Coro[tuple[None | _T, bool]]:
    """`tinyio` coroutine for running a coroutine for at most `timeout_in_seconds`.

    **Arguments:**

    - `coro`: another coroutine.
    - `timeout_in_seconds`: the maximum number of seconds to allow `coro` to run for.

    **Returns:**

    A coroutine that an be `yield`ed on. This will return a pair of either `(output, True)` or `(None, False)`,
    corresponding to whether `coro` completed within the timeout or not.
    """
    done = Event()
    outs = []

    def wrapper():
        out = yield coro
        outs.append(None)
        done.set()

    yield {wrapper()}
    yield from done.wait(timeout_in_seconds)
    if len(outs) == 0:
        with contextlib.suppress(TimeoutError):
            coro.throw(TimeoutError)
        return None, False
    else:
        [out] = outs
        return out, True

```
===== 2 =====
```
 
     def wrapper():
         out = yield coro
-        outs.append(out)
+        outs.clear()
         done.set()
 
     yield {wrapper()}
```
```
def timeout(coro: Coro[_T], timeout_in_seconds: int | float) -> Coro[tuple[None | _T, bool]]:
    """`tinyio` coroutine for running a coroutine for at most `timeout_in_seconds`.

    **Arguments:**

    - `coro`: another coroutine.
    - `timeout_in_seconds`: the maximum number of seconds to allow `coro` to run for.

    **Returns:**

    A coroutine that an be `yield`ed on. This will return a pair of either `(output, True)` or `(None, False)`,
    corresponding to whether `coro` completed within the timeout or not.
    """
    done = Event()
    outs = []

    def wrapper():
        out = yield coro
        outs.clear()
        done.set()

    yield {wrapper()}
    yield from done.wait(timeout_in_seconds)
    if len(outs) == 0:
        with contextlib.suppress(TimeoutError):
            coro.throw(TimeoutError)
        return None, False
    else:
        [out] = outs
        return out, True
```
===== 3 =====
```
         outs.append(out)
         done.set()
 
-    yield {wrapper()}
+    yield done.wait(timeout_in_seconds)
     yield from done.wait(timeout_in_seconds)
     if len(outs) == 0:
         with contextlib.suppress(TimeoutError):
```
```
def timeout(coro: Coro[_T], timeout_in_seconds: int | float) -> Coro[tuple[None | _T, bool]]:
    """`tinyio` coroutine for running a coroutine for at most `timeout_in_seconds`.

    **Arguments:**

    - `coro`: another coroutine.
    - `timeout_in_seconds`: the maximum number of seconds to allow `coro` to run for.

    **Returns:**

    A coroutine that an be `yield`ed on. This will return a pair of either `(output, True)` or `(None, False)`,
    corresponding to whether `coro` completed within the timeout or not.
    """
    done = Event()
    outs = []

    def wrapper():
        out = yield coro
        outs.append(out)
        done.set()

    yield done.wait(timeout_in_seconds)
    yield from done.wait(timeout_in_seconds)
    if len(outs) == 0:
        with contextlib.suppress(TimeoutError):
            coro.throw(TimeoutError)
        return None, False
    else:
        [out] = outs
        return out, True
```
===== 4 =====
```
         outs.append(out)
         done.set()
 
-    yield {wrapper()}
+    yield from done.wait(0)
     yield from done.wait(timeout_in_seconds)
     if len(outs) == 0:
         with contextlib.suppress(TimeoutError):
```
```
def timeout(coro: Coro[_T], timeout_in_seconds: int | float) -> Coro[tuple[None | _T, bool]]:
    """`tinyio` coroutine for running a coroutine for at most `timeout_in_seconds`.

    **Arguments:**

    - `coro`: another coroutine.
    - `timeout_in_seconds`: the maximum number of seconds to allow `coro` to run for.

    **Returns:**

    A coroutine that an be `yield`ed on. This will return a pair of either `(output, True)` or `(None, False)`,
    corresponding to whether `coro` completed within the timeout or not.
    """
    done = Event()
    outs = []

    def wrapper():
        out = yield coro
        outs.append(out)
        done.set()

    yield from done.wait(0)
    yield from done.wait(timeout_in_seconds)
    if len(outs) == 0:
        with contextlib.suppress(TimeoutError):
            coro.throw(TimeoutError)
        return None, False
    else:
        [out] = outs
        return out, True
```
===== 5 =====
```
         outs.append(out)
         done.set()
 
-    yield {wrapper()}
+    yield from wrapper()
     yield from done.wait(timeout_in_seconds)
     if len(outs) == 0:
         with contextlib.suppress(TimeoutError):
```
```
def timeout(coro: Coro[_T], timeout_in_seconds: int | float) -> Coro[tuple[None | _T, bool]]:
    """`tinyio` coroutine for running a coroutine for at most `timeout_in_seconds`.

    **Arguments:**

    - `coro`: another coroutine.
    - `timeout_in_seconds`: the maximum number of seconds to allow `coro` to run for.

    **Returns:**

    A coroutine that an be `yield`ed on. This will return a pair of either `(output, True)` or `(None, False)`,
    corresponding to whether `coro` completed within the timeout or not.
    """
    done = Event()
    outs = []

    def wrapper():
        out = yield coro
        outs.append(out)
        done.set()

    yield from wrapper()
    yield from done.wait(timeout_in_seconds)
    if len(outs) == 0:
        with contextlib.suppress(TimeoutError):
            coro.throw(TimeoutError)
        return None, False
    else:
        [out] = outs
        return out, True
```
===== 6 =====
```
         outs.append(out)
         done.set()
 
-    yield {wrapper()}
+    yield wrapper()
     yield from done.wait(timeout_in_seconds)
     if len(outs) == 0:
         with contextlib.suppress(TimeoutError):
```
```
def timeout(coro: Coro[_T], timeout_in_seconds: int | float) -> Coro[tuple[None | _T, bool]]:
    """`tinyio` coroutine for running a coroutine for at most `timeout_in_seconds`.

    **Arguments:**

    - `coro`: another coroutine.
    - `timeout_in_seconds`: the maximum number of seconds to allow `coro` to run for.

    **Returns:**

    A coroutine that an be `yield`ed on. This will return a pair of either `(output, True)` or `(None, False)`,
    corresponding to whether `coro` completed within the timeout or not.
    """
    done = Event()
    outs = []

    def wrapper():
        out = yield coro
        outs.append(out)
        done.set()

    yield wrapper()
    yield from done.wait(timeout_in_seconds)
    if len(outs) == 0:
        with contextlib.suppress(TimeoutError):
            coro.throw(TimeoutError)
        return None, False
    else:
        [out] = outs
        return out, True
```
===== 7 =====
```
         outs.append(out)
         done.set()
 
-    yield {wrapper()}
+    yield wrapper() if True else None
     yield from done.wait(timeout_in_seconds)
     if len(outs) == 0:
         with contextlib.suppress(TimeoutError):
```
```
def timeout(coro: Coro[_T], timeout_in_seconds: int | float) -> Coro[tuple[None | _T, bool]]:
    """`tinyio` coroutine for running a coroutine for at most `timeout_in_seconds`.

    **Arguments:**

    - `coro`: another coroutine.
    - `timeout_in_seconds`: the maximum number of seconds to allow `coro` to run for.

    **Returns:**

    A coroutine that an be `yield`ed on. This will return a pair of either `(output, True)` or `(None, False)`,
    corresponding to whether `coro` completed within the timeout or not.
    """
    done = Event()
    outs = []

    def wrapper():
        out = yield coro
        outs.append(out)
        done.set()

    yield wrapper() if True else None
    yield from done.wait(timeout_in_seconds)
    if len(outs) == 0:
        with contextlib.suppress(TimeoutError):
            coro.throw(TimeoutError)
        return None, False
    else:
        [out] = outs
        return out, True
```
===== 8 =====
```
         done.set()
 
     yield {wrapper()}
-    yield from done.wait(timeout_in_seconds)
+    yield from done.wait(0)  # Waits indefinitely, effectively ignoring the timeout
     if len(outs) == 0:
         with contextlib.suppress(TimeoutError):
             coro.throw(TimeoutError)
```
```
def timeout(coro: Coro[_T], timeout_in_seconds: int | float) -> Coro[tuple[None | _T, bool]]:
    """`tinyio` coroutine for running a coroutine for at most `timeout_in_seconds`.

    **Arguments:**

    - `coro`: another coroutine.
    - `timeout_in_seconds`: the maximum number of seconds to allow `coro` to run for.

    **Returns:**

    A coroutine that an be `yield`ed on. This will return a pair of either `(output, True)` or `(None, False)`,
    corresponding to whether `coro` completed within the timeout or not.
    """
    done = Event()
    outs = []

    def wrapper():
        out = yield coro
        outs.append(out)
        done.set()

    yield {wrapper()}
    yield from done.wait(0)  # Waits indefinitely, effectively ignoring the timeout
    if len(outs) == 0:
        with contextlib.suppress(TimeoutError):
            coro.throw(TimeoutError)
        return None, False
    else:
        [out] = outs
        return out, True
```
===== 9 =====
```
         done.set()
 
     yield {wrapper()}
-    yield from done.wait(timeout_in_seconds)
+    yield from done.wait(None)
     if len(outs) == 0:
         with contextlib.suppress(TimeoutError):
             coro.throw(TimeoutError)
         return None, False
     else:
         [out] = outs
-        return out, True+        return out, True
```
```
def timeout(coro: Coro[_T], timeout_in_seconds: int | float) -> Coro[tuple[None | _T, bool]]:
    """`tinyio` coroutine for running a coroutine for at most `timeout_in_seconds`.

    **Arguments:**

    - `coro`: another coroutine.
    - `timeout_in_seconds`: the maximum number of seconds to allow `coro` to run for.

    **Returns:**

    A coroutine that an be `yield`ed on. This will return a pair of either `(output, True)` or `(None, False)`,
    corresponding to whether `coro` completed within the timeout or not.
    """
    done = Event()
    outs = []

    def wrapper():
        out = yield coro
        outs.append(out)
        done.set()

    yield {wrapper()}
    yield from done.wait(None)
    if len(outs) == 0:
        with contextlib.suppress(TimeoutError):
            coro.throw(TimeoutError)
        return None, False
    else:
        [out] = outs
        return out, True

```
===== 10 =====
```
         done.set()
 
     yield {wrapper()}
-    yield from done.wait(timeout_in_seconds)
+    yield from done.wait(timeout_in_seconds + 1)  # Extends the timeout, allowing more time than intended
     if len(outs) == 0:
         with contextlib.suppress(TimeoutError):
             coro.throw(TimeoutError)
```
```
def timeout(coro: Coro[_T], timeout_in_seconds: int | float) -> Coro[tuple[None | _T, bool]]:
    """`tinyio` coroutine for running a coroutine for at most `timeout_in_seconds`.

    **Arguments:**

    - `coro`: another coroutine.
    - `timeout_in_seconds`: the maximum number of seconds to allow `coro` to run for.

    **Returns:**

    A coroutine that an be `yield`ed on. This will return a pair of either `(output, True)` or `(None, False)`,
    corresponding to whether `coro` completed within the timeout or not.
    """
    done = Event()
    outs = []

    def wrapper():
        out = yield coro
        outs.append(out)
        done.set()

    yield {wrapper()}
    yield from done.wait(timeout_in_seconds + 1)  # Extends the timeout, allowing more time than intended
    if len(outs) == 0:
        with contextlib.suppress(TimeoutError):
            coro.throw(TimeoutError)
        return None, False
    else:
        [out] = outs
        return out, True
```
===== 11 =====
```
         done.set()
 
     yield {wrapper()}
-    yield from done.wait(timeout_in_seconds)
+    yield from done.wait(timeout_in_seconds / 2)  # Reduces the timeout, potentially causing premature termination
     if len(outs) == 0:
         with contextlib.suppress(TimeoutError):
             coro.throw(TimeoutError)
```
```
def timeout(coro: Coro[_T], timeout_in_seconds: int | float) -> Coro[tuple[None | _T, bool]]:
    """`tinyio` coroutine for running a coroutine for at most `timeout_in_seconds`.

    **Arguments:**

    - `coro`: another coroutine.
    - `timeout_in_seconds`: the maximum number of seconds to allow `coro` to run for.

    **Returns:**

    A coroutine that an be `yield`ed on. This will return a pair of either `(output, True)` or `(None, False)`,
    corresponding to whether `coro` completed within the timeout or not.
    """
    done = Event()
    outs = []

    def wrapper():
        out = yield coro
        outs.append(out)
        done.set()

    yield {wrapper()}
    yield from done.wait(timeout_in_seconds / 2)  # Reduces the timeout, potentially causing premature termination
    if len(outs) == 0:
        with contextlib.suppress(TimeoutError):
            coro.throw(TimeoutError)
        return None, False
    else:
        [out] = outs
        return out, True
```
===== 12 =====
```
     if len(outs) == 0:
         with contextlib.suppress(TimeoutError):
             coro.throw(TimeoutError)
-        return None, False
+        return None, True
     else:
         [out] = outs
-        return out, True+        return out, True
```
```
def timeout(coro: Coro[_T], timeout_in_seconds: int | float) -> Coro[tuple[None | _T, bool]]:
    """`tinyio` coroutine for running a coroutine for at most `timeout_in_seconds`.

    **Arguments:**

    - `coro`: another coroutine.
    - `timeout_in_seconds`: the maximum number of seconds to allow `coro` to run for.

    **Returns:**

    A coroutine that an be `yield`ed on. This will return a pair of either `(output, True)` or `(None, False)`,
    corresponding to whether `coro` completed within the timeout or not.
    """
    done = Event()
    outs = []

    def wrapper():
        out = yield coro
        outs.append(out)
        done.set()

    yield {wrapper()}
    yield from done.wait(timeout_in_seconds)
    if len(outs) == 0:
        with contextlib.suppress(TimeoutError):
            coro.throw(TimeoutError)
        return None, True
    else:
        [out] = outs
        return out, True

```
===== 13 =====
```
         return None, False
     else:
         [out] = outs
-        return out, True+        return out, False
```
```
def timeout(coro: Coro[_T], timeout_in_seconds: int | float) -> Coro[tuple[None | _T, bool]]:
    """`tinyio` coroutine for running a coroutine for at most `timeout_in_seconds`.

    **Arguments:**

    - `coro`: another coroutine.
    - `timeout_in_seconds`: the maximum number of seconds to allow `coro` to run for.

    **Returns:**

    A coroutine that an be `yield`ed on. This will return a pair of either `(output, True)` or `(None, False)`,
    corresponding to whether `coro` completed within the timeout or not.
    """
    done = Event()
    outs = []

    def wrapper():
        out = yield coro
        outs.append(out)
        done.set()

    yield {wrapper()}
    yield from done.wait(timeout_in_seconds)
    if len(outs) == 0:
        with contextlib.suppress(TimeoutError):
            coro.throw(TimeoutError)
        return None, False
    else:
        [out] = outs
        return out, False

```
