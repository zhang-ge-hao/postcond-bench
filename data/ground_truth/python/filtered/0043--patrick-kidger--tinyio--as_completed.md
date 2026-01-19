https://github.com/patrick-kidger/tinyio/blob/44909f813c7d652ade2e83fffed05500a3a8b9b7/./tinyio/_background.py#L10-L49
```
🈚️

Generator
```
```
None
```
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
===== 0 =====
```
     if not isinstance(coros, set) or any(not isinstance(coro, Generator) for coro in coros):
         raise ValueError("`AsCompleted(coros=...)` must be a set of coroutines.")
 
-    outs = {}
+    outs = None
     put_count = 0
     events = [Event() for _ in coros]
 
@@ -37,4 +37,4 @@         put_count += 1
 
     yield {wrapper(coro) for coro in coros}
-    return AsCompleted(outs, events)+    return AsCompleted(outs, events)
```
```
def as_completed(coros: set[Coro[_T]]) -> Coro["AsCompleted"]:
    """Schedules multiple coroutines, iterating through their outputs in the order that they complete.

    Usage is via `.done()` and `.get()` as follows:
    ```python
    import tinyio

    def sleep(x):
        yield tinyio.sleep(x)
        return x

    def as_completed_demo():
        iterator = yield tinyio.as_completed({sleep(7), sleep(2), sleep(4)})
        while not iterator.done():
            out = yield iterator.get()
            print(f"As completed demo: {out}")

    loop = tinyio.Loop()
    loop.run(as_completed_demo())
    # As completed demo: 2
    # As completed demo: 4
    # As completed demo: 7
    ```
    """
    if not isinstance(coros, set) or any(not isinstance(coro, Generator) for coro in coros):
        raise ValueError("`AsCompleted(coros=...)` must be a set of coroutines.")

    outs = None
    put_count = 0
    events = [Event() for _ in coros]

    def wrapper(coro):
        nonlocal put_count
        out = yield coro
        outs[put_count] = out
        events[put_count].set()
        put_count += 1

    yield {wrapper(coro) for coro in coros}
    return AsCompleted(outs, events)

```
===== 1 =====
```
         raise ValueError("`AsCompleted(coros=...)` must be a set of coroutines.")
 
     outs = {}
-    put_count = 0
+    put_count = 1
     events = [Event() for _ in coros]
 
     def wrapper(coro):
@@ -37,4 +37,4 @@         put_count += 1
 
     yield {wrapper(coro) for coro in coros}
-    return AsCompleted(outs, events)+    return AsCompleted(outs, events)
```
```
def as_completed(coros: set[Coro[_T]]) -> Coro["AsCompleted"]:
    """Schedules multiple coroutines, iterating through their outputs in the order that they complete.

    Usage is via `.done()` and `.get()` as follows:
    ```python
    import tinyio

    def sleep(x):
        yield tinyio.sleep(x)
        return x

    def as_completed_demo():
        iterator = yield tinyio.as_completed({sleep(7), sleep(2), sleep(4)})
        while not iterator.done():
            out = yield iterator.get()
            print(f"As completed demo: {out}")

    loop = tinyio.Loop()
    loop.run(as_completed_demo())
    # As completed demo: 2
    # As completed demo: 4
    # As completed demo: 7
    ```
    """
    if not isinstance(coros, set) or any(not isinstance(coro, Generator) for coro in coros):
        raise ValueError("`AsCompleted(coros=...)` must be a set of coroutines.")

    outs = {}
    put_count = 1
    events = [Event() for _ in coros]

    def wrapper(coro):
        nonlocal put_count
        out = yield coro
        outs[put_count] = out
        events[put_count].set()
        put_count += 1

    yield {wrapper(coro) for coro in coros}
    return AsCompleted(outs, events)

```
===== 2 =====
```
         raise ValueError("`AsCompleted(coros=...)` must be a set of coroutines.")
 
     outs = {}
-    put_count = 0
+    put_count = None
     events = [Event() for _ in coros]
 
     def wrapper(coro):
@@ -37,4 +37,4 @@         put_count += 1
 
     yield {wrapper(coro) for coro in coros}
-    return AsCompleted(outs, events)+    return AsCompleted(outs, events)
```
```
def as_completed(coros: set[Coro[_T]]) -> Coro["AsCompleted"]:
    """Schedules multiple coroutines, iterating through their outputs in the order that they complete.

    Usage is via `.done()` and `.get()` as follows:
    ```python
    import tinyio

    def sleep(x):
        yield tinyio.sleep(x)
        return x

    def as_completed_demo():
        iterator = yield tinyio.as_completed({sleep(7), sleep(2), sleep(4)})
        while not iterator.done():
            out = yield iterator.get()
            print(f"As completed demo: {out}")

    loop = tinyio.Loop()
    loop.run(as_completed_demo())
    # As completed demo: 2
    # As completed demo: 4
    # As completed demo: 7
    ```
    """
    if not isinstance(coros, set) or any(not isinstance(coro, Generator) for coro in coros):
        raise ValueError("`AsCompleted(coros=...)` must be a set of coroutines.")

    outs = {}
    put_count = None
    events = [Event() for _ in coros]

    def wrapper(coro):
        nonlocal put_count
        out = yield coro
        outs[put_count] = out
        events[put_count].set()
        put_count += 1

    yield {wrapper(coro) for coro in coros}
    return AsCompleted(outs, events)

```
===== 3 =====
```
 
     outs = {}
     put_count = 0
-    events = [Event() for _ in coros]
+    events = None
 
     def wrapper(coro):
         nonlocal put_count
@@ -37,4 +37,4 @@         put_count += 1
 
     yield {wrapper(coro) for coro in coros}
-    return AsCompleted(outs, events)+    return AsCompleted(outs, events)
```
```
def as_completed(coros: set[Coro[_T]]) -> Coro["AsCompleted"]:
    """Schedules multiple coroutines, iterating through their outputs in the order that they complete.

    Usage is via `.done()` and `.get()` as follows:
    ```python
    import tinyio

    def sleep(x):
        yield tinyio.sleep(x)
        return x

    def as_completed_demo():
        iterator = yield tinyio.as_completed({sleep(7), sleep(2), sleep(4)})
        while not iterator.done():
            out = yield iterator.get()
            print(f"As completed demo: {out}")

    loop = tinyio.Loop()
    loop.run(as_completed_demo())
    # As completed demo: 2
    # As completed demo: 4
    # As completed demo: 7
    ```
    """
    if not isinstance(coros, set) or any(not isinstance(coro, Generator) for coro in coros):
        raise ValueError("`AsCompleted(coros=...)` must be a set of coroutines.")

    outs = {}
    put_count = 0
    events = None

    def wrapper(coro):
        nonlocal put_count
        out = yield coro
        outs[put_count] = out
        events[put_count].set()
        put_count += 1

    yield {wrapper(coro) for coro in coros}
    return AsCompleted(outs, events)

```
===== 4 =====
```
 
     outs = {}
     put_count = 0
-    events = [Event() for _ in coros]
+    events = [Event() for _ in coros if False]  # This will create an empty list, resulting in no events
 
     def wrapper(coro):
         nonlocal put_count
```
```
def as_completed(coros: set[Coro[_T]]) -> Coro["AsCompleted"]:
    """Schedules multiple coroutines, iterating through their outputs in the order that they complete.

    Usage is via `.done()` and `.get()` as follows:
    ```python
    import tinyio

    def sleep(x):
        yield tinyio.sleep(x)
        return x

    def as_completed_demo():
        iterator = yield tinyio.as_completed({sleep(7), sleep(2), sleep(4)})
        while not iterator.done():
            out = yield iterator.get()
            print(f"As completed demo: {out}")

    loop = tinyio.Loop()
    loop.run(as_completed_demo())
    # As completed demo: 2
    # As completed demo: 4
    # As completed demo: 7
    ```
    """
    if not isinstance(coros, set) or any(not isinstance(coro, Generator) for coro in coros):
        raise ValueError("`AsCompleted(coros=...)` must be a set of coroutines.")

    outs = {}
    put_count = 0
    events = [Event() for _ in coros if False]  # This will create an empty list, resulting in no events

    def wrapper(coro):
        nonlocal put_count
        out = yield coro
        outs[put_count] = out
        events[put_count].set()
        put_count += 1

    yield {wrapper(coro) for coro in coros}
    return AsCompleted(outs, events)
```
===== 5 =====
```
 
     outs = {}
     put_count = 0
-    events = [Event() for _ in coros]
+    events = [None] * len(coros)  # Initializing events with None instead of Event instances
 
     def wrapper(coro):
         nonlocal put_count
```
```
def as_completed(coros: set[Coro[_T]]) -> Coro["AsCompleted"]:
    """Schedules multiple coroutines, iterating through their outputs in the order that they complete.

    Usage is via `.done()` and `.get()` as follows:
    ```python
    import tinyio

    def sleep(x):
        yield tinyio.sleep(x)
        return x

    def as_completed_demo():
        iterator = yield tinyio.as_completed({sleep(7), sleep(2), sleep(4)})
        while not iterator.done():
            out = yield iterator.get()
            print(f"As completed demo: {out}")

    loop = tinyio.Loop()
    loop.run(as_completed_demo())
    # As completed demo: 2
    # As completed demo: 4
    # As completed demo: 7
    ```
    """
    if not isinstance(coros, set) or any(not isinstance(coro, Generator) for coro in coros):
        raise ValueError("`AsCompleted(coros=...)` must be a set of coroutines.")

    outs = {}
    put_count = 0
    events = [None] * len(coros)  # Initializing events with None instead of Event instances

    def wrapper(coro):
        nonlocal put_count
        out = yield coro
        outs[put_count] = out
        events[put_count].set()
        put_count += 1

    yield {wrapper(coro) for coro in coros}
    return AsCompleted(outs, events)
```
===== 6 =====
```
     def wrapper(coro):
         nonlocal put_count
         out = yield coro
-        outs[put_count] = out
+        outs[put_count] = None
         events[put_count].set()
         put_count += 1
 
     yield {wrapper(coro) for coro in coros}
-    return AsCompleted(outs, events)+    return AsCompleted(outs, events)
```
```
def as_completed(coros: set[Coro[_T]]) -> Coro["AsCompleted"]:
    """Schedules multiple coroutines, iterating through their outputs in the order that they complete.

    Usage is via `.done()` and `.get()` as follows:
    ```python
    import tinyio

    def sleep(x):
        yield tinyio.sleep(x)
        return x

    def as_completed_demo():
        iterator = yield tinyio.as_completed({sleep(7), sleep(2), sleep(4)})
        while not iterator.done():
            out = yield iterator.get()
            print(f"As completed demo: {out}")

    loop = tinyio.Loop()
    loop.run(as_completed_demo())
    # As completed demo: 2
    # As completed demo: 4
    # As completed demo: 7
    ```
    """
    if not isinstance(coros, set) or any(not isinstance(coro, Generator) for coro in coros):
        raise ValueError("`AsCompleted(coros=...)` must be a set of coroutines.")

    outs = {}
    put_count = 0
    events = [Event() for _ in coros]

    def wrapper(coro):
        nonlocal put_count
        out = yield coro
        outs[put_count] = None
        events[put_count].set()
        put_count += 1

    yield {wrapper(coro) for coro in coros}
    return AsCompleted(outs, events)

```
===== 7 =====
```
         nonlocal put_count
         out = yield coro
         outs[put_count] = out
-        events[put_count].set()
+        events[put_count].set() if put_count < len(events) - 1 else events[put_count + 1].set()
         put_count += 1
 
     yield {wrapper(coro) for coro in coros}
```
```
def as_completed(coros: set[Coro[_T]]) -> Coro["AsCompleted"]:
    """Schedules multiple coroutines, iterating through their outputs in the order that they complete.

    Usage is via `.done()` and `.get()` as follows:
    ```python
    import tinyio

    def sleep(x):
        yield tinyio.sleep(x)
        return x

    def as_completed_demo():
        iterator = yield tinyio.as_completed({sleep(7), sleep(2), sleep(4)})
        while not iterator.done():
            out = yield iterator.get()
            print(f"As completed demo: {out}")

    loop = tinyio.Loop()
    loop.run(as_completed_demo())
    # As completed demo: 2
    # As completed demo: 4
    # As completed demo: 7
    ```
    """
    if not isinstance(coros, set) or any(not isinstance(coro, Generator) for coro in coros):
        raise ValueError("`AsCompleted(coros=...)` must be a set of coroutines.")

    outs = {}
    put_count = 0
    events = [Event() for _ in coros]

    def wrapper(coro):
        nonlocal put_count
        out = yield coro
        outs[put_count] = out
        events[put_count].set() if put_count < len(events) - 1 else events[put_count + 1].set()
        put_count += 1

    yield {wrapper(coro) for coro in coros}
    return AsCompleted(outs, events)
```
===== 8 =====
```
         out = yield coro
         outs[put_count] = out
         events[put_count].set()
-        put_count += 1
+        put_count += 2
 
     yield {wrapper(coro) for coro in coros}
-    return AsCompleted(outs, events)+    return AsCompleted(outs, events)
```
```
def as_completed(coros: set[Coro[_T]]) -> Coro["AsCompleted"]:
    """Schedules multiple coroutines, iterating through their outputs in the order that they complete.

    Usage is via `.done()` and `.get()` as follows:
    ```python
    import tinyio

    def sleep(x):
        yield tinyio.sleep(x)
        return x

    def as_completed_demo():
        iterator = yield tinyio.as_completed({sleep(7), sleep(2), sleep(4)})
        while not iterator.done():
            out = yield iterator.get()
            print(f"As completed demo: {out}")

    loop = tinyio.Loop()
    loop.run(as_completed_demo())
    # As completed demo: 2
    # As completed demo: 4
    # As completed demo: 7
    ```
    """
    if not isinstance(coros, set) or any(not isinstance(coro, Generator) for coro in coros):
        raise ValueError("`AsCompleted(coros=...)` must be a set of coroutines.")

    outs = {}
    put_count = 0
    events = [Event() for _ in coros]

    def wrapper(coro):
        nonlocal put_count
        out = yield coro
        outs[put_count] = out
        events[put_count].set()
        put_count += 2

    yield {wrapper(coro) for coro in coros}
    return AsCompleted(outs, events)

```
===== 9 =====
```
         out = yield coro
         outs[put_count] = out
         events[put_count].set()
-        put_count += 1
+        put_count -= 1
 
     yield {wrapper(coro) for coro in coros}
-    return AsCompleted(outs, events)+    return AsCompleted(outs, events)
```
```
def as_completed(coros: set[Coro[_T]]) -> Coro["AsCompleted"]:
    """Schedules multiple coroutines, iterating through their outputs in the order that they complete.

    Usage is via `.done()` and `.get()` as follows:
    ```python
    import tinyio

    def sleep(x):
        yield tinyio.sleep(x)
        return x

    def as_completed_demo():
        iterator = yield tinyio.as_completed({sleep(7), sleep(2), sleep(4)})
        while not iterator.done():
            out = yield iterator.get()
            print(f"As completed demo: {out}")

    loop = tinyio.Loop()
    loop.run(as_completed_demo())
    # As completed demo: 2
    # As completed demo: 4
    # As completed demo: 7
    ```
    """
    if not isinstance(coros, set) or any(not isinstance(coro, Generator) for coro in coros):
        raise ValueError("`AsCompleted(coros=...)` must be a set of coroutines.")

    outs = {}
    put_count = 0
    events = [Event() for _ in coros]

    def wrapper(coro):
        nonlocal put_count
        out = yield coro
        outs[put_count] = out
        events[put_count].set()
        put_count -= 1

    yield {wrapper(coro) for coro in coros}
    return AsCompleted(outs, events)

```
===== 10 =====
```
         events[put_count].set()
         put_count += 1
 
-    yield {wrapper(coro) for coro in coros}
-    return AsCompleted(outs, events)+    yield {wrapper(None) for coro in coros}
+    return AsCompleted(outs, events)
```
```
def as_completed(coros: set[Coro[_T]]) -> Coro["AsCompleted"]:
    """Schedules multiple coroutines, iterating through their outputs in the order that they complete.

    Usage is via `.done()` and `.get()` as follows:
    ```python
    import tinyio

    def sleep(x):
        yield tinyio.sleep(x)
        return x

    def as_completed_demo():
        iterator = yield tinyio.as_completed({sleep(7), sleep(2), sleep(4)})
        while not iterator.done():
            out = yield iterator.get()
            print(f"As completed demo: {out}")

    loop = tinyio.Loop()
    loop.run(as_completed_demo())
    # As completed demo: 2
    # As completed demo: 4
    # As completed demo: 7
    ```
    """
    if not isinstance(coros, set) or any(not isinstance(coro, Generator) for coro in coros):
        raise ValueError("`AsCompleted(coros=...)` must be a set of coroutines.")

    outs = {}
    put_count = 0
    events = [Event() for _ in coros]

    def wrapper(coro):
        nonlocal put_count
        out = yield coro
        outs[put_count] = out
        events[put_count].set()
        put_count += 1

    yield {wrapper(None) for coro in coros}
    return AsCompleted(outs, events)

```
===== 11 =====
```
         put_count += 1
 
     yield {wrapper(coro) for coro in coros}
-    return AsCompleted(outs, events)+    return AsCompleted(None, events)
```
```
def as_completed(coros: set[Coro[_T]]) -> Coro["AsCompleted"]:
    """Schedules multiple coroutines, iterating through their outputs in the order that they complete.

    Usage is via `.done()` and `.get()` as follows:
    ```python
    import tinyio

    def sleep(x):
        yield tinyio.sleep(x)
        return x

    def as_completed_demo():
        iterator = yield tinyio.as_completed({sleep(7), sleep(2), sleep(4)})
        while not iterator.done():
            out = yield iterator.get()
            print(f"As completed demo: {out}")

    loop = tinyio.Loop()
    loop.run(as_completed_demo())
    # As completed demo: 2
    # As completed demo: 4
    # As completed demo: 7
    ```
    """
    if not isinstance(coros, set) or any(not isinstance(coro, Generator) for coro in coros):
        raise ValueError("`AsCompleted(coros=...)` must be a set of coroutines.")

    outs = {}
    put_count = 0
    events = [Event() for _ in coros]

    def wrapper(coro):
        nonlocal put_count
        out = yield coro
        outs[put_count] = out
        events[put_count].set()
        put_count += 1

    yield {wrapper(coro) for coro in coros}
    return AsCompleted(None, events)

```
===== 12 =====
```
         put_count += 1
 
     yield {wrapper(coro) for coro in coros}
-    return AsCompleted(outs, events)+    return AsCompleted(outs, None)
```
```
def as_completed(coros: set[Coro[_T]]) -> Coro["AsCompleted"]:
    """Schedules multiple coroutines, iterating through their outputs in the order that they complete.

    Usage is via `.done()` and `.get()` as follows:
    ```python
    import tinyio

    def sleep(x):
        yield tinyio.sleep(x)
        return x

    def as_completed_demo():
        iterator = yield tinyio.as_completed({sleep(7), sleep(2), sleep(4)})
        while not iterator.done():
            out = yield iterator.get()
            print(f"As completed demo: {out}")

    loop = tinyio.Loop()
    loop.run(as_completed_demo())
    # As completed demo: 2
    # As completed demo: 4
    # As completed demo: 7
    ```
    """
    if not isinstance(coros, set) or any(not isinstance(coro, Generator) for coro in coros):
        raise ValueError("`AsCompleted(coros=...)` must be a set of coroutines.")

    outs = {}
    put_count = 0
    events = [Event() for _ in coros]

    def wrapper(coro):
        nonlocal put_count
        out = yield coro
        outs[put_count] = out
        events[put_count].set()
        put_count += 1

    yield {wrapper(coro) for coro in coros}
    return AsCompleted(outs, None)

```
===== 13 =====
```
         put_count += 1
 
     yield {wrapper(coro) for coro in coros}
-    return AsCompleted(outs, events)+    return AsCompleted(outs, [])  # Passes an empty list of events, causing get() to fail silently.
```
```
def as_completed(coros: set[Coro[_T]]) -> Coro["AsCompleted"]:
    """Schedules multiple coroutines, iterating through their outputs in the order that they complete.

    Usage is via `.done()` and `.get()` as follows:
    ```python
    import tinyio

    def sleep(x):
        yield tinyio.sleep(x)
        return x

    def as_completed_demo():
        iterator = yield tinyio.as_completed({sleep(7), sleep(2), sleep(4)})
        while not iterator.done():
            out = yield iterator.get()
            print(f"As completed demo: {out}")

    loop = tinyio.Loop()
    loop.run(as_completed_demo())
    # As completed demo: 2
    # As completed demo: 4
    # As completed demo: 7
    ```
    """
    if not isinstance(coros, set) or any(not isinstance(coro, Generator) for coro in coros):
        raise ValueError("`AsCompleted(coros=...)` must be a set of coroutines.")

    outs = {}
    put_count = 0
    events = [Event() for _ in coros]

    def wrapper(coro):
        nonlocal put_count
        out = yield coro
        outs[put_count] = out
        events[put_count].set()
        put_count += 1

    yield {wrapper(coro) for coro in coros}
    return AsCompleted(outs, [])  # Passes an empty list of events, causing get() to fail silently.
```
===== 14 =====
```
         put_count += 1
 
     yield {wrapper(coro) for coro in coros}
-    return AsCompleted(outs, events)+    return AsCompleted(outs, events * 2)  # Duplicates the events, causing confusion in completion tracking.
```
```
def as_completed(coros: set[Coro[_T]]) -> Coro["AsCompleted"]:
    """Schedules multiple coroutines, iterating through their outputs in the order that they complete.

    Usage is via `.done()` and `.get()` as follows:
    ```python
    import tinyio

    def sleep(x):
        yield tinyio.sleep(x)
        return x

    def as_completed_demo():
        iterator = yield tinyio.as_completed({sleep(7), sleep(2), sleep(4)})
        while not iterator.done():
            out = yield iterator.get()
            print(f"As completed demo: {out}")

    loop = tinyio.Loop()
    loop.run(as_completed_demo())
    # As completed demo: 2
    # As completed demo: 4
    # As completed demo: 7
    ```
    """
    if not isinstance(coros, set) or any(not isinstance(coro, Generator) for coro in coros):
        raise ValueError("`AsCompleted(coros=...)` must be a set of coroutines.")

    outs = {}
    put_count = 0
    events = [Event() for _ in coros]

    def wrapper(coro):
        nonlocal put_count
        out = yield coro
        outs[put_count] = out
        events[put_count].set()
        put_count += 1

    yield {wrapper(coro) for coro in coros}
    return AsCompleted(outs, events * 2)  # Duplicates the events, causing confusion in completion tracking.
```
===== 15 =====
```
         put_count += 1
 
     yield {wrapper(coro) for coro in coros}
-    return AsCompleted(outs, events)+    return AsCompleted(outs, events[:1])  # Only returns the first event, losing others.
```
```
def as_completed(coros: set[Coro[_T]]) -> Coro["AsCompleted"]:
    """Schedules multiple coroutines, iterating through their outputs in the order that they complete.

    Usage is via `.done()` and `.get()` as follows:
    ```python
    import tinyio

    def sleep(x):
        yield tinyio.sleep(x)
        return x

    def as_completed_demo():
        iterator = yield tinyio.as_completed({sleep(7), sleep(2), sleep(4)})
        while not iterator.done():
            out = yield iterator.get()
            print(f"As completed demo: {out}")

    loop = tinyio.Loop()
    loop.run(as_completed_demo())
    # As completed demo: 2
    # As completed demo: 4
    # As completed demo: 7
    ```
    """
    if not isinstance(coros, set) or any(not isinstance(coro, Generator) for coro in coros):
        raise ValueError("`AsCompleted(coros=...)` must be a set of coroutines.")

    outs = {}
    put_count = 0
    events = [Event() for _ in coros]

    def wrapper(coro):
        nonlocal put_count
        out = yield coro
        outs[put_count] = out
        events[put_count].set()
        put_count += 1

    yield {wrapper(coro) for coro in coros}
    return AsCompleted(outs, events[:1])  # Only returns the first event, losing others.
```
===== 16 =====
```
         put_count += 1
 
     yield {wrapper(coro) for coro in coros}
-    return AsCompleted(outs, events)+    return AsCompleted({}, events)  # Passes an empty dictionary, losing all outputs.
```
```
def as_completed(coros: set[Coro[_T]]) -> Coro["AsCompleted"]:
    """Schedules multiple coroutines, iterating through their outputs in the order that they complete.

    Usage is via `.done()` and `.get()` as follows:
    ```python
    import tinyio

    def sleep(x):
        yield tinyio.sleep(x)
        return x

    def as_completed_demo():
        iterator = yield tinyio.as_completed({sleep(7), sleep(2), sleep(4)})
        while not iterator.done():
            out = yield iterator.get()
            print(f"As completed demo: {out}")

    loop = tinyio.Loop()
    loop.run(as_completed_demo())
    # As completed demo: 2
    # As completed demo: 4
    # As completed demo: 7
    ```
    """
    if not isinstance(coros, set) or any(not isinstance(coro, Generator) for coro in coros):
        raise ValueError("`AsCompleted(coros=...)` must be a set of coroutines.")

    outs = {}
    put_count = 0
    events = [Event() for _ in coros]

    def wrapper(coro):
        nonlocal put_count
        out = yield coro
        outs[put_count] = out
        events[put_count].set()
        put_count += 1

    yield {wrapper(coro) for coro in coros}
    return AsCompleted({}, events)  # Passes an empty dictionary, losing all outputs.
```
