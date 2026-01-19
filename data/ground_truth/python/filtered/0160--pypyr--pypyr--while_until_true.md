https://github.com/pypyr/pypyr/blob/b3e8f8c6063c11e37c1c762b89b4cd8620460c79/./pypyr/utils/poll.py#L50-L135
```
🈚️

The method returns a function object?
```
```
None
```
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143]
===== 0 =====
```
               max_attempts without the wrapped function ever returning True.
     """
     def decorator(f):
-        logger.debug("started")
+        logger.debug("Decorator initialized")
 
         def sleep_looper(*args, **kwargs):
             i = 0
```
```
def while_until_true(interval, max_attempts):
    """Execute a decorated function until it returns True.

    Executes wrapped function at every number of seconds specified by interval,
    until wrapped function either returns True or max_attempts are exhausted,
    whichever comes 1st.

    Interval is in seconds. It is either a simple float value, or a callable
    that returns a float value. If it is a callable, the passed callable will
    execute on every iteration. The callable signature is:
    func(n: int) -> float

    n is the iteration counter.

    The difference between while_until_true and wait_until_true is that the
    latter will always loop to a max_attempts, whereas while_until_true will
    keep going indefinitely.

    The other notable difference to wait_until_true is that the wrapped
    function signature must be:
    func(counter, *args, **kwargs)

    This is because this decorator injects the while loop counter into the
    invoked function.

    Args:
        interval (float or callable): In seconds. How long to wait between
            executing the wrapped function. The callable signature is func(n)
            where n is the iteration counter, and should return a float.
        max_attempts (int): Execute wrapped function up to this limit. None
                      means infinite (or until wrapped function returns True).
                      Passing anything <0 also means infinite.

    Returns:
        Bool. True if wrapped function returned True. False if reached
              max_attempts without the wrapped function ever returning True.
    """
    def decorator(f):
        logger.debug("Decorator initialized")

        def sleep_looper(*args, **kwargs):
            i = 0
            result = False
            is_interval_callable = callable(interval)

            if not is_interval_callable:
                if max_attempts:
                    logger.debug("Looping every %s seconds for %s attempts",
                                 interval, max_attempts)
                else:
                    logger.debug("Looping every %s seconds.", interval)

            # loop breaks explicitly for all possible exit conditions
            while True:
                i += 1
                result = f(i, *args, **kwargs)

                if result:
                    logger.debug("iteration %s. Desired state reached.", i)
                    break

                sleep = interval(i) if is_interval_callable else interval

                if max_attempts:
                    if i < max_attempts:
                        logger.debug(
                            "iteration %s. Sleeping for %ss. Still waiting...",
                            i, sleep)
                        time.sleep(sleep)
                    else:
                        logger.debug(
                            "iteration %s. Max attempts exhausted.", i)
                        break
                else:
                    # result False AND max_attempts is None means keep looping
                    # because None = infinite
                    logger.debug(
                        "iteration %s. Sleeping for %ss. Still waiting...",
                        i, sleep)
                    time.sleep(sleep)
            logger.debug("done")
            return result

        return sleep_looper

    return decorator
```
===== 1 =====
```
               max_attempts without the wrapped function ever returning True.
     """
     def decorator(f):
-        logger.debug("started")
+        logger.debug("Entering the while_until_true decorator")
 
         def sleep_looper(*args, **kwargs):
             i = 0
```
```
def while_until_true(interval, max_attempts):
    """Execute a decorated function until it returns True.

    Executes wrapped function at every number of seconds specified by interval,
    until wrapped function either returns True or max_attempts are exhausted,
    whichever comes 1st.

    Interval is in seconds. It is either a simple float value, or a callable
    that returns a float value. If it is a callable, the passed callable will
    execute on every iteration. The callable signature is:
    func(n: int) -> float

    n is the iteration counter.

    The difference between while_until_true and wait_until_true is that the
    latter will always loop to a max_attempts, whereas while_until_true will
    keep going indefinitely.

    The other notable difference to wait_until_true is that the wrapped
    function signature must be:
    func(counter, *args, **kwargs)

    This is because this decorator injects the while loop counter into the
    invoked function.

    Args:
        interval (float or callable): In seconds. How long to wait between
            executing the wrapped function. The callable signature is func(n)
            where n is the iteration counter, and should return a float.
        max_attempts (int): Execute wrapped function up to this limit. None
                      means infinite (or until wrapped function returns True).
                      Passing anything <0 also means infinite.

    Returns:
        Bool. True if wrapped function returned True. False if reached
              max_attempts without the wrapped function ever returning True.
    """
    def decorator(f):
        logger.debug("Entering the while_until_true decorator")

        def sleep_looper(*args, **kwargs):
            i = 0
            result = False
            is_interval_callable = callable(interval)

            if not is_interval_callable:
                if max_attempts:
                    logger.debug("Looping every %s seconds for %s attempts",
                                 interval, max_attempts)
                else:
                    logger.debug("Looping every %s seconds.", interval)

            # loop breaks explicitly for all possible exit conditions
            while True:
                i += 1
                result = f(i, *args, **kwargs)

                if result:
                    logger.debug("iteration %s. Desired state reached.", i)
                    break

                sleep = interval(i) if is_interval_callable else interval

                if max_attempts:
                    if i < max_attempts:
                        logger.debug(
                            "iteration %s. Sleeping for %ss. Still waiting...",
                            i, sleep)
                        time.sleep(sleep)
                    else:
                        logger.debug(
                            "iteration %s. Max attempts exhausted.", i)
                        break
                else:
                    # result False AND max_attempts is None means keep looping
                    # because None = infinite
                    logger.debug(
                        "iteration %s. Sleeping for %ss. Still waiting...",
                        i, sleep)
                    time.sleep(sleep)
            logger.debug("done")
            return result

        return sleep_looper

    return decorator
```
===== 2 =====
```
               max_attempts without the wrapped function ever returning True.
     """
     def decorator(f):
-        logger.debug("started")
+        logger.debug("Preparing to execute the wrapped function")
 
         def sleep_looper(*args, **kwargs):
             i = 0
```
```
def while_until_true(interval, max_attempts):
    """Execute a decorated function until it returns True.

    Executes wrapped function at every number of seconds specified by interval,
    until wrapped function either returns True or max_attempts are exhausted,
    whichever comes 1st.

    Interval is in seconds. It is either a simple float value, or a callable
    that returns a float value. If it is a callable, the passed callable will
    execute on every iteration. The callable signature is:
    func(n: int) -> float

    n is the iteration counter.

    The difference between while_until_true and wait_until_true is that the
    latter will always loop to a max_attempts, whereas while_until_true will
    keep going indefinitely.

    The other notable difference to wait_until_true is that the wrapped
    function signature must be:
    func(counter, *args, **kwargs)

    This is because this decorator injects the while loop counter into the
    invoked function.

    Args:
        interval (float or callable): In seconds. How long to wait between
            executing the wrapped function. The callable signature is func(n)
            where n is the iteration counter, and should return a float.
        max_attempts (int): Execute wrapped function up to this limit. None
                      means infinite (or until wrapped function returns True).
                      Passing anything <0 also means infinite.

    Returns:
        Bool. True if wrapped function returned True. False if reached
              max_attempts without the wrapped function ever returning True.
    """
    def decorator(f):
        logger.debug("Preparing to execute the wrapped function")

        def sleep_looper(*args, **kwargs):
            i = 0
            result = False
            is_interval_callable = callable(interval)

            if not is_interval_callable:
                if max_attempts:
                    logger.debug("Looping every %s seconds for %s attempts",
                                 interval, max_attempts)
                else:
                    logger.debug("Looping every %s seconds.", interval)

            # loop breaks explicitly for all possible exit conditions
            while True:
                i += 1
                result = f(i, *args, **kwargs)

                if result:
                    logger.debug("iteration %s. Desired state reached.", i)
                    break

                sleep = interval(i) if is_interval_callable else interval

                if max_attempts:
                    if i < max_attempts:
                        logger.debug(
                            "iteration %s. Sleeping for %ss. Still waiting...",
                            i, sleep)
                        time.sleep(sleep)
                    else:
                        logger.debug(
                            "iteration %s. Max attempts exhausted.", i)
                        break
                else:
                    # result False AND max_attempts is None means keep looping
                    # because None = infinite
                    logger.debug(
                        "iteration %s. Sleeping for %ss. Still waiting...",
                        i, sleep)
                    time.sleep(sleep)
            logger.debug("done")
            return result

        return sleep_looper

    return decorator
```
===== 3 =====
```
               max_attempts without the wrapped function ever returning True.
     """
     def decorator(f):
-        logger.debug("started")
+        logger.debug("STARTED")
 
         def sleep_looper(*args, **kwargs):
             i = 0
@@ -83,4 +83,4 @@ 
         return sleep_looper
 
-    return decorator+    return decorator
```
```
def while_until_true(interval, max_attempts):
    """Execute a decorated function until it returns True.

    Executes wrapped function at every number of seconds specified by interval,
    until wrapped function either returns True or max_attempts are exhausted,
    whichever comes 1st.

    Interval is in seconds. It is either a simple float value, or a callable
    that returns a float value. If it is a callable, the passed callable will
    execute on every iteration. The callable signature is:
    func(n: int) -> float

    n is the iteration counter.

    The difference between while_until_true and wait_until_true is that the
    latter will always loop to a max_attempts, whereas while_until_true will
    keep going indefinitely.

    The other notable difference to wait_until_true is that the wrapped
    function signature must be:
    func(counter, *args, **kwargs)

    This is because this decorator injects the while loop counter into the
    invoked function.

    Args:
        interval (float or callable): In seconds. How long to wait between
            executing the wrapped function. The callable signature is func(n)
            where n is the iteration counter, and should return a float.
        max_attempts (int): Execute wrapped function up to this limit. None
                      means infinite (or until wrapped function returns True).
                      Passing anything <0 also means infinite.

    Returns:
        Bool. True if wrapped function returned True. False if reached
              max_attempts without the wrapped function ever returning True.
    """
    def decorator(f):
        logger.debug("STARTED")

        def sleep_looper(*args, **kwargs):
            i = 0
            result = False
            is_interval_callable = callable(interval)

            if not is_interval_callable:
                if max_attempts:
                    logger.debug("Looping every %s seconds for %s attempts",
                                 interval, max_attempts)
                else:
                    logger.debug("Looping every %s seconds.", interval)

            # loop breaks explicitly for all possible exit conditions
            while True:
                i += 1
                result = f(i, *args, **kwargs)

                if result:
                    logger.debug("iteration %s. Desired state reached.", i)
                    break

                sleep = interval(i) if is_interval_callable else interval

                if max_attempts:
                    if i < max_attempts:
                        logger.debug(
                            "iteration %s. Sleeping for %ss. Still waiting...",
                            i, sleep)
                        time.sleep(sleep)
                    else:
                        logger.debug(
                            "iteration %s. Max attempts exhausted.", i)
                        break
                else:
                    # result False AND max_attempts is None means keep looping
                    # because None = infinite
                    logger.debug(
                        "iteration %s. Sleeping for %ss. Still waiting...",
                        i, sleep)
                    time.sleep(sleep)
            logger.debug("done")
            return result

        return sleep_looper

    return decorator

```
===== 4 =====
```
               max_attempts without the wrapped function ever returning True.
     """
     def decorator(f):
-        logger.debug("started")
+        logger.debug("XXstartedXX")
 
         def sleep_looper(*args, **kwargs):
             i = 0
@@ -83,4 +83,4 @@ 
         return sleep_looper
 
-    return decorator+    return decorator
```
```
def while_until_true(interval, max_attempts):
    """Execute a decorated function until it returns True.

    Executes wrapped function at every number of seconds specified by interval,
    until wrapped function either returns True or max_attempts are exhausted,
    whichever comes 1st.

    Interval is in seconds. It is either a simple float value, or a callable
    that returns a float value. If it is a callable, the passed callable will
    execute on every iteration. The callable signature is:
    func(n: int) -> float

    n is the iteration counter.

    The difference between while_until_true and wait_until_true is that the
    latter will always loop to a max_attempts, whereas while_until_true will
    keep going indefinitely.

    The other notable difference to wait_until_true is that the wrapped
    function signature must be:
    func(counter, *args, **kwargs)

    This is because this decorator injects the while loop counter into the
    invoked function.

    Args:
        interval (float or callable): In seconds. How long to wait between
            executing the wrapped function. The callable signature is func(n)
            where n is the iteration counter, and should return a float.
        max_attempts (int): Execute wrapped function up to this limit. None
                      means infinite (or until wrapped function returns True).
                      Passing anything <0 also means infinite.

    Returns:
        Bool. True if wrapped function returned True. False if reached
              max_attempts without the wrapped function ever returning True.
    """
    def decorator(f):
        logger.debug("XXstartedXX")

        def sleep_looper(*args, **kwargs):
            i = 0
            result = False
            is_interval_callable = callable(interval)

            if not is_interval_callable:
                if max_attempts:
                    logger.debug("Looping every %s seconds for %s attempts",
                                 interval, max_attempts)
                else:
                    logger.debug("Looping every %s seconds.", interval)

            # loop breaks explicitly for all possible exit conditions
            while True:
                i += 1
                result = f(i, *args, **kwargs)

                if result:
                    logger.debug("iteration %s. Desired state reached.", i)
                    break

                sleep = interval(i) if is_interval_callable else interval

                if max_attempts:
                    if i < max_attempts:
                        logger.debug(
                            "iteration %s. Sleeping for %ss. Still waiting...",
                            i, sleep)
                        time.sleep(sleep)
                    else:
                        logger.debug(
                            "iteration %s. Max attempts exhausted.", i)
                        break
                else:
                    # result False AND max_attempts is None means keep looping
                    # because None = infinite
                    logger.debug(
                        "iteration %s. Sleeping for %ss. Still waiting...",
                        i, sleep)
                    time.sleep(sleep)
            logger.debug("done")
            return result

        return sleep_looper

    return decorator

```
===== 5 =====
```
               max_attempts without the wrapped function ever returning True.
     """
     def decorator(f):
-        logger.debug("started")
+        logger.debug(None)
 
         def sleep_looper(*args, **kwargs):
             i = 0
@@ -83,4 +83,4 @@ 
         return sleep_looper
 
-    return decorator+    return decorator
```
```
def while_until_true(interval, max_attempts):
    """Execute a decorated function until it returns True.

    Executes wrapped function at every number of seconds specified by interval,
    until wrapped function either returns True or max_attempts are exhausted,
    whichever comes 1st.

    Interval is in seconds. It is either a simple float value, or a callable
    that returns a float value. If it is a callable, the passed callable will
    execute on every iteration. The callable signature is:
    func(n: int) -> float

    n is the iteration counter.

    The difference between while_until_true and wait_until_true is that the
    latter will always loop to a max_attempts, whereas while_until_true will
    keep going indefinitely.

    The other notable difference to wait_until_true is that the wrapped
    function signature must be:
    func(counter, *args, **kwargs)

    This is because this decorator injects the while loop counter into the
    invoked function.

    Args:
        interval (float or callable): In seconds. How long to wait between
            executing the wrapped function. The callable signature is func(n)
            where n is the iteration counter, and should return a float.
        max_attempts (int): Execute wrapped function up to this limit. None
                      means infinite (or until wrapped function returns True).
                      Passing anything <0 also means infinite.

    Returns:
        Bool. True if wrapped function returned True. False if reached
              max_attempts without the wrapped function ever returning True.
    """
    def decorator(f):
        logger.debug(None)

        def sleep_looper(*args, **kwargs):
            i = 0
            result = False
            is_interval_callable = callable(interval)

            if not is_interval_callable:
                if max_attempts:
                    logger.debug("Looping every %s seconds for %s attempts",
                                 interval, max_attempts)
                else:
                    logger.debug("Looping every %s seconds.", interval)

            # loop breaks explicitly for all possible exit conditions
            while True:
                i += 1
                result = f(i, *args, **kwargs)

                if result:
                    logger.debug("iteration %s. Desired state reached.", i)
                    break

                sleep = interval(i) if is_interval_callable else interval

                if max_attempts:
                    if i < max_attempts:
                        logger.debug(
                            "iteration %s. Sleeping for %ss. Still waiting...",
                            i, sleep)
                        time.sleep(sleep)
                    else:
                        logger.debug(
                            "iteration %s. Max attempts exhausted.", i)
                        break
                else:
                    # result False AND max_attempts is None means keep looping
                    # because None = infinite
                    logger.debug(
                        "iteration %s. Sleeping for %ss. Still waiting...",
                        i, sleep)
                    time.sleep(sleep)
            logger.debug("done")
            return result

        return sleep_looper

    return decorator

```
===== 6 =====
```
               max_attempts without the wrapped function ever returning True.
     """
     def decorator(f):
-        logger.debug("started")
+        logger.info("Starting the sleep looper")
 
         def sleep_looper(*args, **kwargs):
             i = 0
```
```
def while_until_true(interval, max_attempts):
    """Execute a decorated function until it returns True.

    Executes wrapped function at every number of seconds specified by interval,
    until wrapped function either returns True or max_attempts are exhausted,
    whichever comes 1st.

    Interval is in seconds. It is either a simple float value, or a callable
    that returns a float value. If it is a callable, the passed callable will
    execute on every iteration. The callable signature is:
    func(n: int) -> float

    n is the iteration counter.

    The difference between while_until_true and wait_until_true is that the
    latter will always loop to a max_attempts, whereas while_until_true will
    keep going indefinitely.

    The other notable difference to wait_until_true is that the wrapped
    function signature must be:
    func(counter, *args, **kwargs)

    This is because this decorator injects the while loop counter into the
    invoked function.

    Args:
        interval (float or callable): In seconds. How long to wait between
            executing the wrapped function. The callable signature is func(n)
            where n is the iteration counter, and should return a float.
        max_attempts (int): Execute wrapped function up to this limit. None
                      means infinite (or until wrapped function returns True).
                      Passing anything <0 also means infinite.

    Returns:
        Bool. True if wrapped function returned True. False if reached
              max_attempts without the wrapped function ever returning True.
    """
    def decorator(f):
        logger.info("Starting the sleep looper")

        def sleep_looper(*args, **kwargs):
            i = 0
            result = False
            is_interval_callable = callable(interval)

            if not is_interval_callable:
                if max_attempts:
                    logger.debug("Looping every %s seconds for %s attempts",
                                 interval, max_attempts)
                else:
                    logger.debug("Looping every %s seconds.", interval)

            # loop breaks explicitly for all possible exit conditions
            while True:
                i += 1
                result = f(i, *args, **kwargs)

                if result:
                    logger.debug("iteration %s. Desired state reached.", i)
                    break

                sleep = interval(i) if is_interval_callable else interval

                if max_attempts:
                    if i < max_attempts:
                        logger.debug(
                            "iteration %s. Sleeping for %ss. Still waiting...",
                            i, sleep)
                        time.sleep(sleep)
                    else:
                        logger.debug(
                            "iteration %s. Max attempts exhausted.", i)
                        break
                else:
                    # result False AND max_attempts is None means keep looping
                    # because None = infinite
                    logger.debug(
                        "iteration %s. Sleeping for %ss. Still waiting...",
                        i, sleep)
                    time.sleep(sleep)
            logger.debug("done")
            return result

        return sleep_looper

    return decorator
```
===== 7 =====
```
               max_attempts without the wrapped function ever returning True.
     """
     def decorator(f):
-        logger.debug("started")
+        logger.warning("Decorator function is being called")
 
         def sleep_looper(*args, **kwargs):
             i = 0
```
```
def while_until_true(interval, max_attempts):
    """Execute a decorated function until it returns True.

    Executes wrapped function at every number of seconds specified by interval,
    until wrapped function either returns True or max_attempts are exhausted,
    whichever comes 1st.

    Interval is in seconds. It is either a simple float value, or a callable
    that returns a float value. If it is a callable, the passed callable will
    execute on every iteration. The callable signature is:
    func(n: int) -> float

    n is the iteration counter.

    The difference between while_until_true and wait_until_true is that the
    latter will always loop to a max_attempts, whereas while_until_true will
    keep going indefinitely.

    The other notable difference to wait_until_true is that the wrapped
    function signature must be:
    func(counter, *args, **kwargs)

    This is because this decorator injects the while loop counter into the
    invoked function.

    Args:
        interval (float or callable): In seconds. How long to wait between
            executing the wrapped function. The callable signature is func(n)
            where n is the iteration counter, and should return a float.
        max_attempts (int): Execute wrapped function up to this limit. None
                      means infinite (or until wrapped function returns True).
                      Passing anything <0 also means infinite.

    Returns:
        Bool. True if wrapped function returned True. False if reached
              max_attempts without the wrapped function ever returning True.
    """
    def decorator(f):
        logger.warning("Decorator function is being called")

        def sleep_looper(*args, **kwargs):
            i = 0
            result = False
            is_interval_callable = callable(interval)

            if not is_interval_callable:
                if max_attempts:
                    logger.debug("Looping every %s seconds for %s attempts",
                                 interval, max_attempts)
                else:
                    logger.debug("Looping every %s seconds.", interval)

            # loop breaks explicitly for all possible exit conditions
            while True:
                i += 1
                result = f(i, *args, **kwargs)

                if result:
                    logger.debug("iteration %s. Desired state reached.", i)
                    break

                sleep = interval(i) if is_interval_callable else interval

                if max_attempts:
                    if i < max_attempts:
                        logger.debug(
                            "iteration %s. Sleeping for %ss. Still waiting...",
                            i, sleep)
                        time.sleep(sleep)
                    else:
                        logger.debug(
                            "iteration %s. Max attempts exhausted.", i)
                        break
                else:
                    # result False AND max_attempts is None means keep looping
                    # because None = infinite
                    logger.debug(
                        "iteration %s. Sleeping for %ss. Still waiting...",
                        i, sleep)
                    time.sleep(sleep)
            logger.debug("done")
            return result

        return sleep_looper

    return decorator
```
===== 8 =====
```
         logger.debug("started")
 
         def sleep_looper(*args, **kwargs):
-            i = 0
+            i = 1
             result = False
             is_interval_callable = callable(interval)
 
@@ -83,4 +83,4 @@ 
         return sleep_looper
 
-    return decorator+    return decorator
```
```
def while_until_true(interval, max_attempts):
    """Execute a decorated function until it returns True.

    Executes wrapped function at every number of seconds specified by interval,
    until wrapped function either returns True or max_attempts are exhausted,
    whichever comes 1st.

    Interval is in seconds. It is either a simple float value, or a callable
    that returns a float value. If it is a callable, the passed callable will
    execute on every iteration. The callable signature is:
    func(n: int) -> float

    n is the iteration counter.

    The difference between while_until_true and wait_until_true is that the
    latter will always loop to a max_attempts, whereas while_until_true will
    keep going indefinitely.

    The other notable difference to wait_until_true is that the wrapped
    function signature must be:
    func(counter, *args, **kwargs)

    This is because this decorator injects the while loop counter into the
    invoked function.

    Args:
        interval (float or callable): In seconds. How long to wait between
            executing the wrapped function. The callable signature is func(n)
            where n is the iteration counter, and should return a float.
        max_attempts (int): Execute wrapped function up to this limit. None
                      means infinite (or until wrapped function returns True).
                      Passing anything <0 also means infinite.

    Returns:
        Bool. True if wrapped function returned True. False if reached
              max_attempts without the wrapped function ever returning True.
    """
    def decorator(f):
        logger.debug("started")

        def sleep_looper(*args, **kwargs):
            i = 1
            result = False
            is_interval_callable = callable(interval)

            if not is_interval_callable:
                if max_attempts:
                    logger.debug("Looping every %s seconds for %s attempts",
                                 interval, max_attempts)
                else:
                    logger.debug("Looping every %s seconds.", interval)

            # loop breaks explicitly for all possible exit conditions
            while True:
                i += 1
                result = f(i, *args, **kwargs)

                if result:
                    logger.debug("iteration %s. Desired state reached.", i)
                    break

                sleep = interval(i) if is_interval_callable else interval

                if max_attempts:
                    if i < max_attempts:
                        logger.debug(
                            "iteration %s. Sleeping for %ss. Still waiting...",
                            i, sleep)
                        time.sleep(sleep)
                    else:
                        logger.debug(
                            "iteration %s. Max attempts exhausted.", i)
                        break
                else:
                    # result False AND max_attempts is None means keep looping
                    # because None = infinite
                    logger.debug(
                        "iteration %s. Sleeping for %ss. Still waiting...",
                        i, sleep)
                    time.sleep(sleep)
            logger.debug("done")
            return result

        return sleep_looper

    return decorator

```
===== 9 =====
```
         logger.debug("started")
 
         def sleep_looper(*args, **kwargs):
-            i = 0
+            i = None
             result = False
             is_interval_callable = callable(interval)
 
@@ -83,4 +83,4 @@ 
         return sleep_looper
 
-    return decorator+    return decorator
```
```
def while_until_true(interval, max_attempts):
    """Execute a decorated function until it returns True.

    Executes wrapped function at every number of seconds specified by interval,
    until wrapped function either returns True or max_attempts are exhausted,
    whichever comes 1st.

    Interval is in seconds. It is either a simple float value, or a callable
    that returns a float value. If it is a callable, the passed callable will
    execute on every iteration. The callable signature is:
    func(n: int) -> float

    n is the iteration counter.

    The difference between while_until_true and wait_until_true is that the
    latter will always loop to a max_attempts, whereas while_until_true will
    keep going indefinitely.

    The other notable difference to wait_until_true is that the wrapped
    function signature must be:
    func(counter, *args, **kwargs)

    This is because this decorator injects the while loop counter into the
    invoked function.

    Args:
        interval (float or callable): In seconds. How long to wait between
            executing the wrapped function. The callable signature is func(n)
            where n is the iteration counter, and should return a float.
        max_attempts (int): Execute wrapped function up to this limit. None
                      means infinite (or until wrapped function returns True).
                      Passing anything <0 also means infinite.

    Returns:
        Bool. True if wrapped function returned True. False if reached
              max_attempts without the wrapped function ever returning True.
    """
    def decorator(f):
        logger.debug("started")

        def sleep_looper(*args, **kwargs):
            i = None
            result = False
            is_interval_callable = callable(interval)

            if not is_interval_callable:
                if max_attempts:
                    logger.debug("Looping every %s seconds for %s attempts",
                                 interval, max_attempts)
                else:
                    logger.debug("Looping every %s seconds.", interval)

            # loop breaks explicitly for all possible exit conditions
            while True:
                i += 1
                result = f(i, *args, **kwargs)

                if result:
                    logger.debug("iteration %s. Desired state reached.", i)
                    break

                sleep = interval(i) if is_interval_callable else interval

                if max_attempts:
                    if i < max_attempts:
                        logger.debug(
                            "iteration %s. Sleeping for %ss. Still waiting...",
                            i, sleep)
                        time.sleep(sleep)
                    else:
                        logger.debug(
                            "iteration %s. Max attempts exhausted.", i)
                        break
                else:
                    # result False AND max_attempts is None means keep looping
                    # because None = infinite
                    logger.debug(
                        "iteration %s. Sleeping for %ss. Still waiting...",
                        i, sleep)
                    time.sleep(sleep)
            logger.debug("done")
            return result

        return sleep_looper

    return decorator

```
===== 10 =====
```
         def sleep_looper(*args, **kwargs):
             i = 0
             result = False
-            is_interval_callable = callable(interval)
+            is_interval_callable = None
 
             if not is_interval_callable:
                 if max_attempts:
@@ -83,4 +83,4 @@ 
         return sleep_looper
 
-    return decorator+    return decorator
```
```
def while_until_true(interval, max_attempts):
    """Execute a decorated function until it returns True.

    Executes wrapped function at every number of seconds specified by interval,
    until wrapped function either returns True or max_attempts are exhausted,
    whichever comes 1st.

    Interval is in seconds. It is either a simple float value, or a callable
    that returns a float value. If it is a callable, the passed callable will
    execute on every iteration. The callable signature is:
    func(n: int) -> float

    n is the iteration counter.

    The difference between while_until_true and wait_until_true is that the
    latter will always loop to a max_attempts, whereas while_until_true will
    keep going indefinitely.

    The other notable difference to wait_until_true is that the wrapped
    function signature must be:
    func(counter, *args, **kwargs)

    This is because this decorator injects the while loop counter into the
    invoked function.

    Args:
        interval (float or callable): In seconds. How long to wait between
            executing the wrapped function. The callable signature is func(n)
            where n is the iteration counter, and should return a float.
        max_attempts (int): Execute wrapped function up to this limit. None
                      means infinite (or until wrapped function returns True).
                      Passing anything <0 also means infinite.

    Returns:
        Bool. True if wrapped function returned True. False if reached
              max_attempts without the wrapped function ever returning True.
    """
    def decorator(f):
        logger.debug("started")

        def sleep_looper(*args, **kwargs):
            i = 0
            result = False
            is_interval_callable = None

            if not is_interval_callable:
                if max_attempts:
                    logger.debug("Looping every %s seconds for %s attempts",
                                 interval, max_attempts)
                else:
                    logger.debug("Looping every %s seconds.", interval)

            # loop breaks explicitly for all possible exit conditions
            while True:
                i += 1
                result = f(i, *args, **kwargs)

                if result:
                    logger.debug("iteration %s. Desired state reached.", i)
                    break

                sleep = interval(i) if is_interval_callable else interval

                if max_attempts:
                    if i < max_attempts:
                        logger.debug(
                            "iteration %s. Sleeping for %ss. Still waiting...",
                            i, sleep)
                        time.sleep(sleep)
                    else:
                        logger.debug(
                            "iteration %s. Max attempts exhausted.", i)
                        break
                else:
                    # result False AND max_attempts is None means keep looping
                    # because None = infinite
                    logger.debug(
                        "iteration %s. Sleeping for %ss. Still waiting...",
                        i, sleep)
                    time.sleep(sleep)
            logger.debug("done")
            return result

        return sleep_looper

    return decorator

```
===== 11 =====
```
         def sleep_looper(*args, **kwargs):
             i = 0
             result = False
-            is_interval_callable = callable(interval)
+            is_interval_callable = callable(None)
 
             if not is_interval_callable:
                 if max_attempts:
@@ -83,4 +83,4 @@ 
         return sleep_looper
 
-    return decorator+    return decorator
```
```
def while_until_true(interval, max_attempts):
    """Execute a decorated function until it returns True.

    Executes wrapped function at every number of seconds specified by interval,
    until wrapped function either returns True or max_attempts are exhausted,
    whichever comes 1st.

    Interval is in seconds. It is either a simple float value, or a callable
    that returns a float value. If it is a callable, the passed callable will
    execute on every iteration. The callable signature is:
    func(n: int) -> float

    n is the iteration counter.

    The difference between while_until_true and wait_until_true is that the
    latter will always loop to a max_attempts, whereas while_until_true will
    keep going indefinitely.

    The other notable difference to wait_until_true is that the wrapped
    function signature must be:
    func(counter, *args, **kwargs)

    This is because this decorator injects the while loop counter into the
    invoked function.

    Args:
        interval (float or callable): In seconds. How long to wait between
            executing the wrapped function. The callable signature is func(n)
            where n is the iteration counter, and should return a float.
        max_attempts (int): Execute wrapped function up to this limit. None
                      means infinite (or until wrapped function returns True).
                      Passing anything <0 also means infinite.

    Returns:
        Bool. True if wrapped function returned True. False if reached
              max_attempts without the wrapped function ever returning True.
    """
    def decorator(f):
        logger.debug("started")

        def sleep_looper(*args, **kwargs):
            i = 0
            result = False
            is_interval_callable = callable(None)

            if not is_interval_callable:
                if max_attempts:
                    logger.debug("Looping every %s seconds for %s attempts",
                                 interval, max_attempts)
                else:
                    logger.debug("Looping every %s seconds.", interval)

            # loop breaks explicitly for all possible exit conditions
            while True:
                i += 1
                result = f(i, *args, **kwargs)

                if result:
                    logger.debug("iteration %s. Desired state reached.", i)
                    break

                sleep = interval(i) if is_interval_callable else interval

                if max_attempts:
                    if i < max_attempts:
                        logger.debug(
                            "iteration %s. Sleeping for %ss. Still waiting...",
                            i, sleep)
                        time.sleep(sleep)
                    else:
                        logger.debug(
                            "iteration %s. Max attempts exhausted.", i)
                        break
                else:
                    # result False AND max_attempts is None means keep looping
                    # because None = infinite
                    logger.debug(
                        "iteration %s. Sleeping for %ss. Still waiting...",
                        i, sleep)
                    time.sleep(sleep)
            logger.debug("done")
            return result

        return sleep_looper

    return decorator

```
===== 12 =====
```
         def sleep_looper(*args, **kwargs):
             i = 0
             result = False
-            is_interval_callable = callable(interval)
+            is_interval_callable = interval == 0
 
             if not is_interval_callable:
                 if max_attempts:
```
```
def while_until_true(interval, max_attempts):
    """Execute a decorated function until it returns True.

    Executes wrapped function at every number of seconds specified by interval,
    until wrapped function either returns True or max_attempts are exhausted,
    whichever comes 1st.

    Interval is in seconds. It is either a simple float value, or a callable
    that returns a float value. If it is a callable, the passed callable will
    execute on every iteration. The callable signature is:
    func(n: int) -> float

    n is the iteration counter.

    The difference between while_until_true and wait_until_true is that the
    latter will always loop to a max_attempts, whereas while_until_true will
    keep going indefinitely.

    The other notable difference to wait_until_true is that the wrapped
    function signature must be:
    func(counter, *args, **kwargs)

    This is because this decorator injects the while loop counter into the
    invoked function.

    Args:
        interval (float or callable): In seconds. How long to wait between
            executing the wrapped function. The callable signature is func(n)
            where n is the iteration counter, and should return a float.
        max_attempts (int): Execute wrapped function up to this limit. None
                      means infinite (or until wrapped function returns True).
                      Passing anything <0 also means infinite.

    Returns:
        Bool. True if wrapped function returned True. False if reached
              max_attempts without the wrapped function ever returning True.
    """
    def decorator(f):
        logger.debug("started")

        def sleep_looper(*args, **kwargs):
            i = 0
            result = False
            is_interval_callable = interval == 0

            if not is_interval_callable:
                if max_attempts:
                    logger.debug("Looping every %s seconds for %s attempts",
                                 interval, max_attempts)
                else:
                    logger.debug("Looping every %s seconds.", interval)

            # loop breaks explicitly for all possible exit conditions
            while True:
                i += 1
                result = f(i, *args, **kwargs)

                if result:
                    logger.debug("iteration %s. Desired state reached.", i)
                    break

                sleep = interval(i) if is_interval_callable else interval

                if max_attempts:
                    if i < max_attempts:
                        logger.debug(
                            "iteration %s. Sleeping for %ss. Still waiting...",
                            i, sleep)
                        time.sleep(sleep)
                    else:
                        logger.debug(
                            "iteration %s. Max attempts exhausted.", i)
                        break
                else:
                    # result False AND max_attempts is None means keep looping
                    # because None = infinite
                    logger.debug(
                        "iteration %s. Sleeping for %ss. Still waiting...",
                        i, sleep)
                    time.sleep(sleep)
            logger.debug("done")
            return result

        return sleep_looper

    return decorator
```
===== 13 =====
```
         def sleep_looper(*args, **kwargs):
             i = 0
             result = False
-            is_interval_callable = callable(interval)
+            is_interval_callable = interval is None
 
             if not is_interval_callable:
                 if max_attempts:
```
```
def while_until_true(interval, max_attempts):
    """Execute a decorated function until it returns True.

    Executes wrapped function at every number of seconds specified by interval,
    until wrapped function either returns True or max_attempts are exhausted,
    whichever comes 1st.

    Interval is in seconds. It is either a simple float value, or a callable
    that returns a float value. If it is a callable, the passed callable will
    execute on every iteration. The callable signature is:
    func(n: int) -> float

    n is the iteration counter.

    The difference between while_until_true and wait_until_true is that the
    latter will always loop to a max_attempts, whereas while_until_true will
    keep going indefinitely.

    The other notable difference to wait_until_true is that the wrapped
    function signature must be:
    func(counter, *args, **kwargs)

    This is because this decorator injects the while loop counter into the
    invoked function.

    Args:
        interval (float or callable): In seconds. How long to wait between
            executing the wrapped function. The callable signature is func(n)
            where n is the iteration counter, and should return a float.
        max_attempts (int): Execute wrapped function up to this limit. None
                      means infinite (or until wrapped function returns True).
                      Passing anything <0 also means infinite.

    Returns:
        Bool. True if wrapped function returned True. False if reached
              max_attempts without the wrapped function ever returning True.
    """
    def decorator(f):
        logger.debug("started")

        def sleep_looper(*args, **kwargs):
            i = 0
            result = False
            is_interval_callable = interval is None

            if not is_interval_callable:
                if max_attempts:
                    logger.debug("Looping every %s seconds for %s attempts",
                                 interval, max_attempts)
                else:
                    logger.debug("Looping every %s seconds.", interval)

            # loop breaks explicitly for all possible exit conditions
            while True:
                i += 1
                result = f(i, *args, **kwargs)

                if result:
                    logger.debug("iteration %s. Desired state reached.", i)
                    break

                sleep = interval(i) if is_interval_callable else interval

                if max_attempts:
                    if i < max_attempts:
                        logger.debug(
                            "iteration %s. Sleeping for %ss. Still waiting...",
                            i, sleep)
                        time.sleep(sleep)
                    else:
                        logger.debug(
                            "iteration %s. Max attempts exhausted.", i)
                        break
                else:
                    # result False AND max_attempts is None means keep looping
                    # because None = infinite
                    logger.debug(
                        "iteration %s. Sleeping for %ss. Still waiting...",
                        i, sleep)
                    time.sleep(sleep)
            logger.debug("done")
            return result

        return sleep_looper

    return decorator
```
===== 14 =====
```
         def sleep_looper(*args, **kwargs):
             i = 0
             result = False
-            is_interval_callable = callable(interval)
+            is_interval_callable = isinstance(interval, (int, float))
 
             if not is_interval_callable:
                 if max_attempts:
```
```
def while_until_true(interval, max_attempts):
    """Execute a decorated function until it returns True.

    Executes wrapped function at every number of seconds specified by interval,
    until wrapped function either returns True or max_attempts are exhausted,
    whichever comes 1st.

    Interval is in seconds. It is either a simple float value, or a callable
    that returns a float value. If it is a callable, the passed callable will
    execute on every iteration. The callable signature is:
    func(n: int) -> float

    n is the iteration counter.

    The difference between while_until_true and wait_until_true is that the
    latter will always loop to a max_attempts, whereas while_until_true will
    keep going indefinitely.

    The other notable difference to wait_until_true is that the wrapped
    function signature must be:
    func(counter, *args, **kwargs)

    This is because this decorator injects the while loop counter into the
    invoked function.

    Args:
        interval (float or callable): In seconds. How long to wait between
            executing the wrapped function. The callable signature is func(n)
            where n is the iteration counter, and should return a float.
        max_attempts (int): Execute wrapped function up to this limit. None
                      means infinite (or until wrapped function returns True).
                      Passing anything <0 also means infinite.

    Returns:
        Bool. True if wrapped function returned True. False if reached
              max_attempts without the wrapped function ever returning True.
    """
    def decorator(f):
        logger.debug("started")

        def sleep_looper(*args, **kwargs):
            i = 0
            result = False
            is_interval_callable = isinstance(interval, (int, float))

            if not is_interval_callable:
                if max_attempts:
                    logger.debug("Looping every %s seconds for %s attempts",
                                 interval, max_attempts)
                else:
                    logger.debug("Looping every %s seconds.", interval)

            # loop breaks explicitly for all possible exit conditions
            while True:
                i += 1
                result = f(i, *args, **kwargs)

                if result:
                    logger.debug("iteration %s. Desired state reached.", i)
                    break

                sleep = interval(i) if is_interval_callable else interval

                if max_attempts:
                    if i < max_attempts:
                        logger.debug(
                            "iteration %s. Sleeping for %ss. Still waiting...",
                            i, sleep)
                        time.sleep(sleep)
                    else:
                        logger.debug(
                            "iteration %s. Max attempts exhausted.", i)
                        break
                else:
                    # result False AND max_attempts is None means keep looping
                    # because None = infinite
                    logger.debug(
                        "iteration %s. Sleeping for %ss. Still waiting...",
                        i, sleep)
                    time.sleep(sleep)
            logger.debug("done")
            return result

        return sleep_looper

    return decorator
```
===== 15 =====
```
         def sleep_looper(*args, **kwargs):
             i = 0
             result = False
-            is_interval_callable = callable(interval)
+            is_interval_callable = isinstance(interval, str)
 
             if not is_interval_callable:
                 if max_attempts:
```
```
def while_until_true(interval, max_attempts):
    """Execute a decorated function until it returns True.

    Executes wrapped function at every number of seconds specified by interval,
    until wrapped function either returns True or max_attempts are exhausted,
    whichever comes 1st.

    Interval is in seconds. It is either a simple float value, or a callable
    that returns a float value. If it is a callable, the passed callable will
    execute on every iteration. The callable signature is:
    func(n: int) -> float

    n is the iteration counter.

    The difference between while_until_true and wait_until_true is that the
    latter will always loop to a max_attempts, whereas while_until_true will
    keep going indefinitely.

    The other notable difference to wait_until_true is that the wrapped
    function signature must be:
    func(counter, *args, **kwargs)

    This is because this decorator injects the while loop counter into the
    invoked function.

    Args:
        interval (float or callable): In seconds. How long to wait between
            executing the wrapped function. The callable signature is func(n)
            where n is the iteration counter, and should return a float.
        max_attempts (int): Execute wrapped function up to this limit. None
                      means infinite (or until wrapped function returns True).
                      Passing anything <0 also means infinite.

    Returns:
        Bool. True if wrapped function returned True. False if reached
              max_attempts without the wrapped function ever returning True.
    """
    def decorator(f):
        logger.debug("started")

        def sleep_looper(*args, **kwargs):
            i = 0
            result = False
            is_interval_callable = isinstance(interval, str)

            if not is_interval_callable:
                if max_attempts:
                    logger.debug("Looping every %s seconds for %s attempts",
                                 interval, max_attempts)
                else:
                    logger.debug("Looping every %s seconds.", interval)

            # loop breaks explicitly for all possible exit conditions
            while True:
                i += 1
                result = f(i, *args, **kwargs)

                if result:
                    logger.debug("iteration %s. Desired state reached.", i)
                    break

                sleep = interval(i) if is_interval_callable else interval

                if max_attempts:
                    if i < max_attempts:
                        logger.debug(
                            "iteration %s. Sleeping for %ss. Still waiting...",
                            i, sleep)
                        time.sleep(sleep)
                    else:
                        logger.debug(
                            "iteration %s. Max attempts exhausted.", i)
                        break
                else:
                    # result False AND max_attempts is None means keep looping
                    # because None = infinite
                    logger.debug(
                        "iteration %s. Sleeping for %ss. Still waiting...",
                        i, sleep)
                    time.sleep(sleep)
            logger.debug("done")
            return result

        return sleep_looper

    return decorator
```
===== 16 =====
```
         def sleep_looper(*args, **kwargs):
             i = 0
             result = False
-            is_interval_callable = callable(interval)
+            is_interval_callable = not callable(interval)
 
             if not is_interval_callable:
                 if max_attempts:
```
```
def while_until_true(interval, max_attempts):
    """Execute a decorated function until it returns True.

    Executes wrapped function at every number of seconds specified by interval,
    until wrapped function either returns True or max_attempts are exhausted,
    whichever comes 1st.

    Interval is in seconds. It is either a simple float value, or a callable
    that returns a float value. If it is a callable, the passed callable will
    execute on every iteration. The callable signature is:
    func(n: int) -> float

    n is the iteration counter.

    The difference between while_until_true and wait_until_true is that the
    latter will always loop to a max_attempts, whereas while_until_true will
    keep going indefinitely.

    The other notable difference to wait_until_true is that the wrapped
    function signature must be:
    func(counter, *args, **kwargs)

    This is because this decorator injects the while loop counter into the
    invoked function.

    Args:
        interval (float or callable): In seconds. How long to wait between
            executing the wrapped function. The callable signature is func(n)
            where n is the iteration counter, and should return a float.
        max_attempts (int): Execute wrapped function up to this limit. None
                      means infinite (or until wrapped function returns True).
                      Passing anything <0 also means infinite.

    Returns:
        Bool. True if wrapped function returned True. False if reached
              max_attempts without the wrapped function ever returning True.
    """
    def decorator(f):
        logger.debug("started")

        def sleep_looper(*args, **kwargs):
            i = 0
            result = False
            is_interval_callable = not callable(interval)

            if not is_interval_callable:
                if max_attempts:
                    logger.debug("Looping every %s seconds for %s attempts",
                                 interval, max_attempts)
                else:
                    logger.debug("Looping every %s seconds.", interval)

            # loop breaks explicitly for all possible exit conditions
            while True:
                i += 1
                result = f(i, *args, **kwargs)

                if result:
                    logger.debug("iteration %s. Desired state reached.", i)
                    break

                sleep = interval(i) if is_interval_callable else interval

                if max_attempts:
                    if i < max_attempts:
                        logger.debug(
                            "iteration %s. Sleeping for %ss. Still waiting...",
                            i, sleep)
                        time.sleep(sleep)
                    else:
                        logger.debug(
                            "iteration %s. Max attempts exhausted.", i)
                        break
                else:
                    # result False AND max_attempts is None means keep looping
                    # because None = infinite
                    logger.debug(
                        "iteration %s. Sleeping for %ss. Still waiting...",
                        i, sleep)
                    time.sleep(sleep)
            logger.debug("done")
            return result

        return sleep_looper

    return decorator
```
===== 17 =====
```
             result = False
             is_interval_callable = callable(interval)
 
-            if not is_interval_callable:
+            if is_interval_callable:
                 if max_attempts:
                     logger.debug("Looping every %s seconds for %s attempts",
                                  interval, max_attempts)
@@ -83,4 +83,4 @@ 
         return sleep_looper
 
-    return decorator+    return decorator
```
```
def while_until_true(interval, max_attempts):
    """Execute a decorated function until it returns True.

    Executes wrapped function at every number of seconds specified by interval,
    until wrapped function either returns True or max_attempts are exhausted,
    whichever comes 1st.

    Interval is in seconds. It is either a simple float value, or a callable
    that returns a float value. If it is a callable, the passed callable will
    execute on every iteration. The callable signature is:
    func(n: int) -> float

    n is the iteration counter.

    The difference between while_until_true and wait_until_true is that the
    latter will always loop to a max_attempts, whereas while_until_true will
    keep going indefinitely.

    The other notable difference to wait_until_true is that the wrapped
    function signature must be:
    func(counter, *args, **kwargs)

    This is because this decorator injects the while loop counter into the
    invoked function.

    Args:
        interval (float or callable): In seconds. How long to wait between
            executing the wrapped function. The callable signature is func(n)
            where n is the iteration counter, and should return a float.
        max_attempts (int): Execute wrapped function up to this limit. None
                      means infinite (or until wrapped function returns True).
                      Passing anything <0 also means infinite.

    Returns:
        Bool. True if wrapped function returned True. False if reached
              max_attempts without the wrapped function ever returning True.
    """
    def decorator(f):
        logger.debug("started")

        def sleep_looper(*args, **kwargs):
            i = 0
            result = False
            is_interval_callable = callable(interval)

            if is_interval_callable:
                if max_attempts:
                    logger.debug("Looping every %s seconds for %s attempts",
                                 interval, max_attempts)
                else:
                    logger.debug("Looping every %s seconds.", interval)

            # loop breaks explicitly for all possible exit conditions
            while True:
                i += 1
                result = f(i, *args, **kwargs)

                if result:
                    logger.debug("iteration %s. Desired state reached.", i)
                    break

                sleep = interval(i) if is_interval_callable else interval

                if max_attempts:
                    if i < max_attempts:
                        logger.debug(
                            "iteration %s. Sleeping for %ss. Still waiting...",
                            i, sleep)
                        time.sleep(sleep)
                    else:
                        logger.debug(
                            "iteration %s. Max attempts exhausted.", i)
                        break
                else:
                    # result False AND max_attempts is None means keep looping
                    # because None = infinite
                    logger.debug(
                        "iteration %s. Sleeping for %ss. Still waiting...",
                        i, sleep)
                    time.sleep(sleep)
            logger.debug("done")
            return result

        return sleep_looper

    return decorator

```
===== 18 =====
```
             result = False
             is_interval_callable = callable(interval)
 
-            if not is_interval_callable:
+            if is_interval_callable:  # This will incorrectly assume the interval is always callable.
                 if max_attempts:
                     logger.debug("Looping every %s seconds for %s attempts",
                                  interval, max_attempts)
```
```
def while_until_true(interval, max_attempts):
    """Execute a decorated function until it returns True.

    Executes wrapped function at every number of seconds specified by interval,
    until wrapped function either returns True or max_attempts are exhausted,
    whichever comes 1st.

    Interval is in seconds. It is either a simple float value, or a callable
    that returns a float value. If it is a callable, the passed callable will
    execute on every iteration. The callable signature is:
    func(n: int) -> float

    n is the iteration counter.

    The difference between while_until_true and wait_until_true is that the
    latter will always loop to a max_attempts, whereas while_until_true will
    keep going indefinitely.

    The other notable difference to wait_until_true is that the wrapped
    function signature must be:
    func(counter, *args, **kwargs)

    This is because this decorator injects the while loop counter into the
    invoked function.

    Args:
        interval (float or callable): In seconds. How long to wait between
            executing the wrapped function. The callable signature is func(n)
            where n is the iteration counter, and should return a float.
        max_attempts (int): Execute wrapped function up to this limit. None
                      means infinite (or until wrapped function returns True).
                      Passing anything <0 also means infinite.

    Returns:
        Bool. True if wrapped function returned True. False if reached
              max_attempts without the wrapped function ever returning True.
    """
    def decorator(f):
        logger.debug("started")

        def sleep_looper(*args, **kwargs):
            i = 0
            result = False
            is_interval_callable = callable(interval)

            if is_interval_callable:  # This will incorrectly assume the interval is always callable.
                if max_attempts:
                    logger.debug("Looping every %s seconds for %s attempts",
                                 interval, max_attempts)
                else:
                    logger.debug("Looping every %s seconds.", interval)

            # loop breaks explicitly for all possible exit conditions
            while True:
                i += 1
                result = f(i, *args, **kwargs)

                if result:
                    logger.debug("iteration %s. Desired state reached.", i)
                    break

                sleep = interval(i) if is_interval_callable else interval

                if max_attempts:
                    if i < max_attempts:
                        logger.debug(
                            "iteration %s. Sleeping for %ss. Still waiting...",
                            i, sleep)
                        time.sleep(sleep)
                    else:
                        logger.debug(
                            "iteration %s. Max attempts exhausted.", i)
                        break
                else:
                    # result False AND max_attempts is None means keep looping
                    # because None = infinite
                    logger.debug(
                        "iteration %s. Sleeping for %ss. Still waiting...",
                        i, sleep)
                    time.sleep(sleep)
            logger.debug("done")
            return result

        return sleep_looper

    return decorator
```
===== 19 =====
```
             result = False
             is_interval_callable = callable(interval)
 
-            if not is_interval_callable:
+            if max_attempts is None:  # This will incorrectly check for max_attempts instead of the interval.
                 if max_attempts:
                     logger.debug("Looping every %s seconds for %s attempts",
                                  interval, max_attempts)
```
```
def while_until_true(interval, max_attempts):
    """Execute a decorated function until it returns True.

    Executes wrapped function at every number of seconds specified by interval,
    until wrapped function either returns True or max_attempts are exhausted,
    whichever comes 1st.

    Interval is in seconds. It is either a simple float value, or a callable
    that returns a float value. If it is a callable, the passed callable will
    execute on every iteration. The callable signature is:
    func(n: int) -> float

    n is the iteration counter.

    The difference between while_until_true and wait_until_true is that the
    latter will always loop to a max_attempts, whereas while_until_true will
    keep going indefinitely.

    The other notable difference to wait_until_true is that the wrapped
    function signature must be:
    func(counter, *args, **kwargs)

    This is because this decorator injects the while loop counter into the
    invoked function.

    Args:
        interval (float or callable): In seconds. How long to wait between
            executing the wrapped function. The callable signature is func(n)
            where n is the iteration counter, and should return a float.
        max_attempts (int): Execute wrapped function up to this limit. None
                      means infinite (or until wrapped function returns True).
                      Passing anything <0 also means infinite.

    Returns:
        Bool. True if wrapped function returned True. False if reached
              max_attempts without the wrapped function ever returning True.
    """
    def decorator(f):
        logger.debug("started")

        def sleep_looper(*args, **kwargs):
            i = 0
            result = False
            is_interval_callable = callable(interval)

            if max_attempts is None:  # This will incorrectly check for max_attempts instead of the interval.
                if max_attempts:
                    logger.debug("Looping every %s seconds for %s attempts",
                                 interval, max_attempts)
                else:
                    logger.debug("Looping every %s seconds.", interval)

            # loop breaks explicitly for all possible exit conditions
            while True:
                i += 1
                result = f(i, *args, **kwargs)

                if result:
                    logger.debug("iteration %s. Desired state reached.", i)
                    break

                sleep = interval(i) if is_interval_callable else interval

                if max_attempts:
                    if i < max_attempts:
                        logger.debug(
                            "iteration %s. Sleeping for %ss. Still waiting...",
                            i, sleep)
                        time.sleep(sleep)
                    else:
                        logger.debug(
                            "iteration %s. Max attempts exhausted.", i)
                        break
                else:
                    # result False AND max_attempts is None means keep looping
                    # because None = infinite
                    logger.debug(
                        "iteration %s. Sleeping for %ss. Still waiting...",
                        i, sleep)
                    time.sleep(sleep)
            logger.debug("done")
            return result

        return sleep_looper

    return decorator
```
===== 20 =====
```
             is_interval_callable = callable(interval)
 
             if not is_interval_callable:
-                if max_attempts:
+                if i >= max_attempts:
                     logger.debug("Looping every %s seconds for %s attempts",
                                  interval, max_attempts)
                 else:
```
```
def while_until_true(interval, max_attempts):
    """Execute a decorated function until it returns True.

    Executes wrapped function at every number of seconds specified by interval,
    until wrapped function either returns True or max_attempts are exhausted,
    whichever comes 1st.

    Interval is in seconds. It is either a simple float value, or a callable
    that returns a float value. If it is a callable, the passed callable will
    execute on every iteration. The callable signature is:
    func(n: int) -> float

    n is the iteration counter.

    The difference between while_until_true and wait_until_true is that the
    latter will always loop to a max_attempts, whereas while_until_true will
    keep going indefinitely.

    The other notable difference to wait_until_true is that the wrapped
    function signature must be:
    func(counter, *args, **kwargs)

    This is because this decorator injects the while loop counter into the
    invoked function.

    Args:
        interval (float or callable): In seconds. How long to wait between
            executing the wrapped function. The callable signature is func(n)
            where n is the iteration counter, and should return a float.
        max_attempts (int): Execute wrapped function up to this limit. None
                      means infinite (or until wrapped function returns True).
                      Passing anything <0 also means infinite.

    Returns:
        Bool. True if wrapped function returned True. False if reached
              max_attempts without the wrapped function ever returning True.
    """
    def decorator(f):
        logger.debug("started")

        def sleep_looper(*args, **kwargs):
            i = 0
            result = False
            is_interval_callable = callable(interval)

            if not is_interval_callable:
                if i >= max_attempts:
                    logger.debug("Looping every %s seconds for %s attempts",
                                 interval, max_attempts)
                else:
                    logger.debug("Looping every %s seconds.", interval)

            # loop breaks explicitly for all possible exit conditions
            while True:
                i += 1
                result = f(i, *args, **kwargs)

                if result:
                    logger.debug("iteration %s. Desired state reached.", i)
                    break

                sleep = interval(i) if is_interval_callable else interval

                if max_attempts:
                    if i < max_attempts:
                        logger.debug(
                            "iteration %s. Sleeping for %ss. Still waiting...",
                            i, sleep)
                        time.sleep(sleep)
                    else:
                        logger.debug(
                            "iteration %s. Max attempts exhausted.", i)
                        break
                else:
                    # result False AND max_attempts is None means keep looping
                    # because None = infinite
                    logger.debug(
                        "iteration %s. Sleeping for %ss. Still waiting...",
                        i, sleep)
                    time.sleep(sleep)
            logger.debug("done")
            return result

        return sleep_looper

    return decorator
```
===== 21 =====
```
             is_interval_callable = callable(interval)
 
             if not is_interval_callable:
-                if max_attempts:
+                if max_attempts == 0:
                     logger.debug("Looping every %s seconds for %s attempts",
                                  interval, max_attempts)
                 else:
```
```
def while_until_true(interval, max_attempts):
    """Execute a decorated function until it returns True.

    Executes wrapped function at every number of seconds specified by interval,
    until wrapped function either returns True or max_attempts are exhausted,
    whichever comes 1st.

    Interval is in seconds. It is either a simple float value, or a callable
    that returns a float value. If it is a callable, the passed callable will
    execute on every iteration. The callable signature is:
    func(n: int) -> float

    n is the iteration counter.

    The difference between while_until_true and wait_until_true is that the
    latter will always loop to a max_attempts, whereas while_until_true will
    keep going indefinitely.

    The other notable difference to wait_until_true is that the wrapped
    function signature must be:
    func(counter, *args, **kwargs)

    This is because this decorator injects the while loop counter into the
    invoked function.

    Args:
        interval (float or callable): In seconds. How long to wait between
            executing the wrapped function. The callable signature is func(n)
            where n is the iteration counter, and should return a float.
        max_attempts (int): Execute wrapped function up to this limit. None
                      means infinite (or until wrapped function returns True).
                      Passing anything <0 also means infinite.

    Returns:
        Bool. True if wrapped function returned True. False if reached
              max_attempts without the wrapped function ever returning True.
    """
    def decorator(f):
        logger.debug("started")

        def sleep_looper(*args, **kwargs):
            i = 0
            result = False
            is_interval_callable = callable(interval)

            if not is_interval_callable:
                if max_attempts == 0:
                    logger.debug("Looping every %s seconds for %s attempts",
                                 interval, max_attempts)
                else:
                    logger.debug("Looping every %s seconds.", interval)

            # loop breaks explicitly for all possible exit conditions
            while True:
                i += 1
                result = f(i, *args, **kwargs)

                if result:
                    logger.debug("iteration %s. Desired state reached.", i)
                    break

                sleep = interval(i) if is_interval_callable else interval

                if max_attempts:
                    if i < max_attempts:
                        logger.debug(
                            "iteration %s. Sleeping for %ss. Still waiting...",
                            i, sleep)
                        time.sleep(sleep)
                    else:
                        logger.debug(
                            "iteration %s. Max attempts exhausted.", i)
                        break
                else:
                    # result False AND max_attempts is None means keep looping
                    # because None = infinite
                    logger.debug(
                        "iteration %s. Sleeping for %ss. Still waiting...",
                        i, sleep)
                    time.sleep(sleep)
            logger.debug("done")
            return result

        return sleep_looper

    return decorator
```
===== 22 =====
```
             is_interval_callable = callable(interval)
 
             if not is_interval_callable:
-                if max_attempts:
+                if max_attempts > 0:
                     logger.debug("Looping every %s seconds for %s attempts",
                                  interval, max_attempts)
                 else:
```
```
def while_until_true(interval, max_attempts):
    """Execute a decorated function until it returns True.

    Executes wrapped function at every number of seconds specified by interval,
    until wrapped function either returns True or max_attempts are exhausted,
    whichever comes 1st.

    Interval is in seconds. It is either a simple float value, or a callable
    that returns a float value. If it is a callable, the passed callable will
    execute on every iteration. The callable signature is:
    func(n: int) -> float

    n is the iteration counter.

    The difference between while_until_true and wait_until_true is that the
    latter will always loop to a max_attempts, whereas while_until_true will
    keep going indefinitely.

    The other notable difference to wait_until_true is that the wrapped
    function signature must be:
    func(counter, *args, **kwargs)

    This is because this decorator injects the while loop counter into the
    invoked function.

    Args:
        interval (float or callable): In seconds. How long to wait between
            executing the wrapped function. The callable signature is func(n)
            where n is the iteration counter, and should return a float.
        max_attempts (int): Execute wrapped function up to this limit. None
                      means infinite (or until wrapped function returns True).
                      Passing anything <0 also means infinite.

    Returns:
        Bool. True if wrapped function returned True. False if reached
              max_attempts without the wrapped function ever returning True.
    """
    def decorator(f):
        logger.debug("started")

        def sleep_looper(*args, **kwargs):
            i = 0
            result = False
            is_interval_callable = callable(interval)

            if not is_interval_callable:
                if max_attempts > 0:
                    logger.debug("Looping every %s seconds for %s attempts",
                                 interval, max_attempts)
                else:
                    logger.debug("Looping every %s seconds.", interval)

            # loop breaks explicitly for all possible exit conditions
            while True:
                i += 1
                result = f(i, *args, **kwargs)

                if result:
                    logger.debug("iteration %s. Desired state reached.", i)
                    break

                sleep = interval(i) if is_interval_callable else interval

                if max_attempts:
                    if i < max_attempts:
                        logger.debug(
                            "iteration %s. Sleeping for %ss. Still waiting...",
                            i, sleep)
                        time.sleep(sleep)
                    else:
                        logger.debug(
                            "iteration %s. Max attempts exhausted.", i)
                        break
                else:
                    # result False AND max_attempts is None means keep looping
                    # because None = infinite
                    logger.debug(
                        "iteration %s. Sleeping for %ss. Still waiting...",
                        i, sleep)
                    time.sleep(sleep)
            logger.debug("done")
            return result

        return sleep_looper

    return decorator
```
===== 23 =====
```
 
             if not is_interval_callable:
                 if max_attempts:
-                    logger.debug("Looping every %s seconds for %s attempts",
+                    logger.debug("LOOPING EVERY %S SECONDS FOR %S ATTEMPTS",
                                  interval, max_attempts)
                 else:
                     logger.debug("Looping every %s seconds.", interval)
@@ -83,4 +83,4 @@ 
         return sleep_looper
 
-    return decorator+    return decorator
```
```
def while_until_true(interval, max_attempts):
    """Execute a decorated function until it returns True.

    Executes wrapped function at every number of seconds specified by interval,
    until wrapped function either returns True or max_attempts are exhausted,
    whichever comes 1st.

    Interval is in seconds. It is either a simple float value, or a callable
    that returns a float value. If it is a callable, the passed callable will
    execute on every iteration. The callable signature is:
    func(n: int) -> float

    n is the iteration counter.

    The difference between while_until_true and wait_until_true is that the
    latter will always loop to a max_attempts, whereas while_until_true will
    keep going indefinitely.

    The other notable difference to wait_until_true is that the wrapped
    function signature must be:
    func(counter, *args, **kwargs)

    This is because this decorator injects the while loop counter into the
    invoked function.

    Args:
        interval (float or callable): In seconds. How long to wait between
            executing the wrapped function. The callable signature is func(n)
            where n is the iteration counter, and should return a float.
        max_attempts (int): Execute wrapped function up to this limit. None
                      means infinite (or until wrapped function returns True).
                      Passing anything <0 also means infinite.

    Returns:
        Bool. True if wrapped function returned True. False if reached
              max_attempts without the wrapped function ever returning True.
    """
    def decorator(f):
        logger.debug("started")

        def sleep_looper(*args, **kwargs):
            i = 0
            result = False
            is_interval_callable = callable(interval)

            if not is_interval_callable:
                if max_attempts:
                    logger.debug("LOOPING EVERY %S SECONDS FOR %S ATTEMPTS",
                                 interval, max_attempts)
                else:
                    logger.debug("Looping every %s seconds.", interval)

            # loop breaks explicitly for all possible exit conditions
            while True:
                i += 1
                result = f(i, *args, **kwargs)

                if result:
                    logger.debug("iteration %s. Desired state reached.", i)
                    break

                sleep = interval(i) if is_interval_callable else interval

                if max_attempts:
                    if i < max_attempts:
                        logger.debug(
                            "iteration %s. Sleeping for %ss. Still waiting...",
                            i, sleep)
                        time.sleep(sleep)
                    else:
                        logger.debug(
                            "iteration %s. Max attempts exhausted.", i)
                        break
                else:
                    # result False AND max_attempts is None means keep looping
                    # because None = infinite
                    logger.debug(
                        "iteration %s. Sleeping for %ss. Still waiting...",
                        i, sleep)
                    time.sleep(sleep)
            logger.debug("done")
            return result

        return sleep_looper

    return decorator

```
===== 24 =====
```
 
             if not is_interval_callable:
                 if max_attempts:
-                    logger.debug("Looping every %s seconds for %s attempts",
+                    logger.debug("XXLooping every %s seconds for %s attemptsXX",
                                  interval, max_attempts)
                 else:
                     logger.debug("Looping every %s seconds.", interval)
@@ -83,4 +83,4 @@ 
         return sleep_looper
 
-    return decorator+    return decorator
```
```
def while_until_true(interval, max_attempts):
    """Execute a decorated function until it returns True.

    Executes wrapped function at every number of seconds specified by interval,
    until wrapped function either returns True or max_attempts are exhausted,
    whichever comes 1st.

    Interval is in seconds. It is either a simple float value, or a callable
    that returns a float value. If it is a callable, the passed callable will
    execute on every iteration. The callable signature is:
    func(n: int) -> float

    n is the iteration counter.

    The difference between while_until_true and wait_until_true is that the
    latter will always loop to a max_attempts, whereas while_until_true will
    keep going indefinitely.

    The other notable difference to wait_until_true is that the wrapped
    function signature must be:
    func(counter, *args, **kwargs)

    This is because this decorator injects the while loop counter into the
    invoked function.

    Args:
        interval (float or callable): In seconds. How long to wait between
            executing the wrapped function. The callable signature is func(n)
            where n is the iteration counter, and should return a float.
        max_attempts (int): Execute wrapped function up to this limit. None
                      means infinite (or until wrapped function returns True).
                      Passing anything <0 also means infinite.

    Returns:
        Bool. True if wrapped function returned True. False if reached
              max_attempts without the wrapped function ever returning True.
    """
    def decorator(f):
        logger.debug("started")

        def sleep_looper(*args, **kwargs):
            i = 0
            result = False
            is_interval_callable = callable(interval)

            if not is_interval_callable:
                if max_attempts:
                    logger.debug("XXLooping every %s seconds for %s attemptsXX",
                                 interval, max_attempts)
                else:
                    logger.debug("Looping every %s seconds.", interval)

            # loop breaks explicitly for all possible exit conditions
            while True:
                i += 1
                result = f(i, *args, **kwargs)

                if result:
                    logger.debug("iteration %s. Desired state reached.", i)
                    break

                sleep = interval(i) if is_interval_callable else interval

                if max_attempts:
                    if i < max_attempts:
                        logger.debug(
                            "iteration %s. Sleeping for %ss. Still waiting...",
                            i, sleep)
                        time.sleep(sleep)
                    else:
                        logger.debug(
                            "iteration %s. Max attempts exhausted.", i)
                        break
                else:
                    # result False AND max_attempts is None means keep looping
                    # because None = infinite
                    logger.debug(
                        "iteration %s. Sleeping for %ss. Still waiting...",
                        i, sleep)
                    time.sleep(sleep)
            logger.debug("done")
            return result

        return sleep_looper

    return decorator

```
===== 25 =====
```
 
             if not is_interval_callable:
                 if max_attempts:
-                    logger.debug("Looping every %s seconds for %s attempts",
+                    logger.debug("looping every %s seconds for %s attempts",
                                  interval, max_attempts)
                 else:
                     logger.debug("Looping every %s seconds.", interval)
@@ -83,4 +83,4 @@ 
         return sleep_looper
 
-    return decorator+    return decorator
```
```
def while_until_true(interval, max_attempts):
    """Execute a decorated function until it returns True.

    Executes wrapped function at every number of seconds specified by interval,
    until wrapped function either returns True or max_attempts are exhausted,
    whichever comes 1st.

    Interval is in seconds. It is either a simple float value, or a callable
    that returns a float value. If it is a callable, the passed callable will
    execute on every iteration. The callable signature is:
    func(n: int) -> float

    n is the iteration counter.

    The difference between while_until_true and wait_until_true is that the
    latter will always loop to a max_attempts, whereas while_until_true will
    keep going indefinitely.

    The other notable difference to wait_until_true is that the wrapped
    function signature must be:
    func(counter, *args, **kwargs)

    This is because this decorator injects the while loop counter into the
    invoked function.

    Args:
        interval (float or callable): In seconds. How long to wait between
            executing the wrapped function. The callable signature is func(n)
            where n is the iteration counter, and should return a float.
        max_attempts (int): Execute wrapped function up to this limit. None
                      means infinite (or until wrapped function returns True).
                      Passing anything <0 also means infinite.

    Returns:
        Bool. True if wrapped function returned True. False if reached
              max_attempts without the wrapped function ever returning True.
    """
    def decorator(f):
        logger.debug("started")

        def sleep_looper(*args, **kwargs):
            i = 0
            result = False
            is_interval_callable = callable(interval)

            if not is_interval_callable:
                if max_attempts:
                    logger.debug("looping every %s seconds for %s attempts",
                                 interval, max_attempts)
                else:
                    logger.debug("Looping every %s seconds.", interval)

            # loop breaks explicitly for all possible exit conditions
            while True:
                i += 1
                result = f(i, *args, **kwargs)

                if result:
                    logger.debug("iteration %s. Desired state reached.", i)
                    break

                sleep = interval(i) if is_interval_callable else interval

                if max_attempts:
                    if i < max_attempts:
                        logger.debug(
                            "iteration %s. Sleeping for %ss. Still waiting...",
                            i, sleep)
                        time.sleep(sleep)
                    else:
                        logger.debug(
                            "iteration %s. Max attempts exhausted.", i)
                        break
                else:
                    # result False AND max_attempts is None means keep looping
                    # because None = infinite
                    logger.debug(
                        "iteration %s. Sleeping for %ss. Still waiting...",
                        i, sleep)
                    time.sleep(sleep)
            logger.debug("done")
            return result

        return sleep_looper

    return decorator

```
===== 26 =====
```
 
             if not is_interval_callable:
                 if max_attempts:
-                    logger.debug("Looping every %s seconds for %s attempts",
+                    logger.debug(None,
                                  interval, max_attempts)
                 else:
                     logger.debug("Looping every %s seconds.", interval)
@@ -83,4 +83,4 @@ 
         return sleep_looper
 
-    return decorator+    return decorator
```
```
def while_until_true(interval, max_attempts):
    """Execute a decorated function until it returns True.

    Executes wrapped function at every number of seconds specified by interval,
    until wrapped function either returns True or max_attempts are exhausted,
    whichever comes 1st.

    Interval is in seconds. It is either a simple float value, or a callable
    that returns a float value. If it is a callable, the passed callable will
    execute on every iteration. The callable signature is:
    func(n: int) -> float

    n is the iteration counter.

    The difference between while_until_true and wait_until_true is that the
    latter will always loop to a max_attempts, whereas while_until_true will
    keep going indefinitely.

    The other notable difference to wait_until_true is that the wrapped
    function signature must be:
    func(counter, *args, **kwargs)

    This is because this decorator injects the while loop counter into the
    invoked function.

    Args:
        interval (float or callable): In seconds. How long to wait between
            executing the wrapped function. The callable signature is func(n)
            where n is the iteration counter, and should return a float.
        max_attempts (int): Execute wrapped function up to this limit. None
                      means infinite (or until wrapped function returns True).
                      Passing anything <0 also means infinite.

    Returns:
        Bool. True if wrapped function returned True. False if reached
              max_attempts without the wrapped function ever returning True.
    """
    def decorator(f):
        logger.debug("started")

        def sleep_looper(*args, **kwargs):
            i = 0
            result = False
            is_interval_callable = callable(interval)

            if not is_interval_callable:
                if max_attempts:
                    logger.debug(None,
                                 interval, max_attempts)
                else:
                    logger.debug("Looping every %s seconds.", interval)

            # loop breaks explicitly for all possible exit conditions
            while True:
                i += 1
                result = f(i, *args, **kwargs)

                if result:
                    logger.debug("iteration %s. Desired state reached.", i)
                    break

                sleep = interval(i) if is_interval_callable else interval

                if max_attempts:
                    if i < max_attempts:
                        logger.debug(
                            "iteration %s. Sleeping for %ss. Still waiting...",
                            i, sleep)
                        time.sleep(sleep)
                    else:
                        logger.debug(
                            "iteration %s. Max attempts exhausted.", i)
                        break
                else:
                    # result False AND max_attempts is None means keep looping
                    # because None = infinite
                    logger.debug(
                        "iteration %s. Sleeping for %ss. Still waiting...",
                        i, sleep)
                    time.sleep(sleep)
            logger.debug("done")
            return result

        return sleep_looper

    return decorator

```
===== 27 =====
```
 
             if not is_interval_callable:
                 if max_attempts:
-                    logger.debug("Looping every %s seconds for %s attempts",
-                                 interval, max_attempts)
+                    logger.debug(interval, max_attempts)
                 else:
                     logger.debug("Looping every %s seconds.", interval)
 
@@ -83,4 +82,4 @@ 
         return sleep_looper
 
-    return decorator+    return decorator
```
```
def while_until_true(interval, max_attempts):
    """Execute a decorated function until it returns True.

    Executes wrapped function at every number of seconds specified by interval,
    until wrapped function either returns True or max_attempts are exhausted,
    whichever comes 1st.

    Interval is in seconds. It is either a simple float value, or a callable
    that returns a float value. If it is a callable, the passed callable will
    execute on every iteration. The callable signature is:
    func(n: int) -> float

    n is the iteration counter.

    The difference between while_until_true and wait_until_true is that the
    latter will always loop to a max_attempts, whereas while_until_true will
    keep going indefinitely.

    The other notable difference to wait_until_true is that the wrapped
    function signature must be:
    func(counter, *args, **kwargs)

    This is because this decorator injects the while loop counter into the
    invoked function.

    Args:
        interval (float or callable): In seconds. How long to wait between
            executing the wrapped function. The callable signature is func(n)
            where n is the iteration counter, and should return a float.
        max_attempts (int): Execute wrapped function up to this limit. None
                      means infinite (or until wrapped function returns True).
                      Passing anything <0 also means infinite.

    Returns:
        Bool. True if wrapped function returned True. False if reached
              max_attempts without the wrapped function ever returning True.
    """
    def decorator(f):
        logger.debug("started")

        def sleep_looper(*args, **kwargs):
            i = 0
            result = False
            is_interval_callable = callable(interval)

            if not is_interval_callable:
                if max_attempts:
                    logger.debug(interval, max_attempts)
                else:
                    logger.debug("Looping every %s seconds.", interval)

            # loop breaks explicitly for all possible exit conditions
            while True:
                i += 1
                result = f(i, *args, **kwargs)

                if result:
                    logger.debug("iteration %s. Desired state reached.", i)
                    break

                sleep = interval(i) if is_interval_callable else interval

                if max_attempts:
                    if i < max_attempts:
                        logger.debug(
                            "iteration %s. Sleeping for %ss. Still waiting...",
                            i, sleep)
                        time.sleep(sleep)
                    else:
                        logger.debug(
                            "iteration %s. Max attempts exhausted.", i)
                        break
                else:
                    # result False AND max_attempts is None means keep looping
                    # because None = infinite
                    logger.debug(
                        "iteration %s. Sleeping for %ss. Still waiting...",
                        i, sleep)
                    time.sleep(sleep)
            logger.debug("done")
            return result

        return sleep_looper

    return decorator

```
===== 28 =====
```
             if not is_interval_callable:
                 if max_attempts:
                     logger.debug("Looping every %s seconds for %s attempts",
-                                 interval, max_attempts)
+                                 None, max_attempts)
                 else:
                     logger.debug("Looping every %s seconds.", interval)
 
@@ -83,4 +83,4 @@ 
         return sleep_looper
 
-    return decorator+    return decorator
```
```
def while_until_true(interval, max_attempts):
    """Execute a decorated function until it returns True.

    Executes wrapped function at every number of seconds specified by interval,
    until wrapped function either returns True or max_attempts are exhausted,
    whichever comes 1st.

    Interval is in seconds. It is either a simple float value, or a callable
    that returns a float value. If it is a callable, the passed callable will
    execute on every iteration. The callable signature is:
    func(n: int) -> float

    n is the iteration counter.

    The difference between while_until_true and wait_until_true is that the
    latter will always loop to a max_attempts, whereas while_until_true will
    keep going indefinitely.

    The other notable difference to wait_until_true is that the wrapped
    function signature must be:
    func(counter, *args, **kwargs)

    This is because this decorator injects the while loop counter into the
    invoked function.

    Args:
        interval (float or callable): In seconds. How long to wait between
            executing the wrapped function. The callable signature is func(n)
            where n is the iteration counter, and should return a float.
        max_attempts (int): Execute wrapped function up to this limit. None
                      means infinite (or until wrapped function returns True).
                      Passing anything <0 also means infinite.

    Returns:
        Bool. True if wrapped function returned True. False if reached
              max_attempts without the wrapped function ever returning True.
    """
    def decorator(f):
        logger.debug("started")

        def sleep_looper(*args, **kwargs):
            i = 0
            result = False
            is_interval_callable = callable(interval)

            if not is_interval_callable:
                if max_attempts:
                    logger.debug("Looping every %s seconds for %s attempts",
                                 None, max_attempts)
                else:
                    logger.debug("Looping every %s seconds.", interval)

            # loop breaks explicitly for all possible exit conditions
            while True:
                i += 1
                result = f(i, *args, **kwargs)

                if result:
                    logger.debug("iteration %s. Desired state reached.", i)
                    break

                sleep = interval(i) if is_interval_callable else interval

                if max_attempts:
                    if i < max_attempts:
                        logger.debug(
                            "iteration %s. Sleeping for %ss. Still waiting...",
                            i, sleep)
                        time.sleep(sleep)
                    else:
                        logger.debug(
                            "iteration %s. Max attempts exhausted.", i)
                        break
                else:
                    # result False AND max_attempts is None means keep looping
                    # because None = infinite
                    logger.debug(
                        "iteration %s. Sleeping for %ss. Still waiting...",
                        i, sleep)
                    time.sleep(sleep)
            logger.debug("done")
            return result

        return sleep_looper

    return decorator

```
===== 29 =====
```
             if not is_interval_callable:
                 if max_attempts:
                     logger.debug("Looping every %s seconds for %s attempts",
-                                 interval, max_attempts)
+                                 interval, )
                 else:
                     logger.debug("Looping every %s seconds.", interval)
 
@@ -83,4 +83,4 @@ 
         return sleep_looper
 
-    return decorator+    return decorator
```
```
def while_until_true(interval, max_attempts):
    """Execute a decorated function until it returns True.

    Executes wrapped function at every number of seconds specified by interval,
    until wrapped function either returns True or max_attempts are exhausted,
    whichever comes 1st.

    Interval is in seconds. It is either a simple float value, or a callable
    that returns a float value. If it is a callable, the passed callable will
    execute on every iteration. The callable signature is:
    func(n: int) -> float

    n is the iteration counter.

    The difference between while_until_true and wait_until_true is that the
    latter will always loop to a max_attempts, whereas while_until_true will
    keep going indefinitely.

    The other notable difference to wait_until_true is that the wrapped
    function signature must be:
    func(counter, *args, **kwargs)

    This is because this decorator injects the while loop counter into the
    invoked function.

    Args:
        interval (float or callable): In seconds. How long to wait between
            executing the wrapped function. The callable signature is func(n)
            where n is the iteration counter, and should return a float.
        max_attempts (int): Execute wrapped function up to this limit. None
                      means infinite (or until wrapped function returns True).
                      Passing anything <0 also means infinite.

    Returns:
        Bool. True if wrapped function returned True. False if reached
              max_attempts without the wrapped function ever returning True.
    """
    def decorator(f):
        logger.debug("started")

        def sleep_looper(*args, **kwargs):
            i = 0
            result = False
            is_interval_callable = callable(interval)

            if not is_interval_callable:
                if max_attempts:
                    logger.debug("Looping every %s seconds for %s attempts",
                                 interval, )
                else:
                    logger.debug("Looping every %s seconds.", interval)

            # loop breaks explicitly for all possible exit conditions
            while True:
                i += 1
                result = f(i, *args, **kwargs)

                if result:
                    logger.debug("iteration %s. Desired state reached.", i)
                    break

                sleep = interval(i) if is_interval_callable else interval

                if max_attempts:
                    if i < max_attempts:
                        logger.debug(
                            "iteration %s. Sleeping for %ss. Still waiting...",
                            i, sleep)
                        time.sleep(sleep)
                    else:
                        logger.debug(
                            "iteration %s. Max attempts exhausted.", i)
                        break
                else:
                    # result False AND max_attempts is None means keep looping
                    # because None = infinite
                    logger.debug(
                        "iteration %s. Sleeping for %ss. Still waiting...",
                        i, sleep)
                    time.sleep(sleep)
            logger.debug("done")
            return result

        return sleep_looper

    return decorator

```
===== 30 =====
```
             if not is_interval_callable:
                 if max_attempts:
                     logger.debug("Looping every %s seconds for %s attempts",
-                                 interval, max_attempts)
+                                 interval, None)
                 else:
                     logger.debug("Looping every %s seconds.", interval)
 
@@ -83,4 +83,4 @@ 
         return sleep_looper
 
-    return decorator+    return decorator
```
```
def while_until_true(interval, max_attempts):
    """Execute a decorated function until it returns True.

    Executes wrapped function at every number of seconds specified by interval,
    until wrapped function either returns True or max_attempts are exhausted,
    whichever comes 1st.

    Interval is in seconds. It is either a simple float value, or a callable
    that returns a float value. If it is a callable, the passed callable will
    execute on every iteration. The callable signature is:
    func(n: int) -> float

    n is the iteration counter.

    The difference between while_until_true and wait_until_true is that the
    latter will always loop to a max_attempts, whereas while_until_true will
    keep going indefinitely.

    The other notable difference to wait_until_true is that the wrapped
    function signature must be:
    func(counter, *args, **kwargs)

    This is because this decorator injects the while loop counter into the
    invoked function.

    Args:
        interval (float or callable): In seconds. How long to wait between
            executing the wrapped function. The callable signature is func(n)
            where n is the iteration counter, and should return a float.
        max_attempts (int): Execute wrapped function up to this limit. None
                      means infinite (or until wrapped function returns True).
                      Passing anything <0 also means infinite.

    Returns:
        Bool. True if wrapped function returned True. False if reached
              max_attempts without the wrapped function ever returning True.
    """
    def decorator(f):
        logger.debug("started")

        def sleep_looper(*args, **kwargs):
            i = 0
            result = False
            is_interval_callable = callable(interval)

            if not is_interval_callable:
                if max_attempts:
                    logger.debug("Looping every %s seconds for %s attempts",
                                 interval, None)
                else:
                    logger.debug("Looping every %s seconds.", interval)

            # loop breaks explicitly for all possible exit conditions
            while True:
                i += 1
                result = f(i, *args, **kwargs)

                if result:
                    logger.debug("iteration %s. Desired state reached.", i)
                    break

                sleep = interval(i) if is_interval_callable else interval

                if max_attempts:
                    if i < max_attempts:
                        logger.debug(
                            "iteration %s. Sleeping for %ss. Still waiting...",
                            i, sleep)
                        time.sleep(sleep)
                    else:
                        logger.debug(
                            "iteration %s. Max attempts exhausted.", i)
                        break
                else:
                    # result False AND max_attempts is None means keep looping
                    # because None = infinite
                    logger.debug(
                        "iteration %s. Sleeping for %ss. Still waiting...",
                        i, sleep)
                    time.sleep(sleep)
            logger.debug("done")
            return result

        return sleep_looper

    return decorator

```
===== 31 =====
```
             if not is_interval_callable:
                 if max_attempts:
                     logger.debug("Looping every %s seconds for %s attempts",
-                                 interval, max_attempts)
+                                 max_attempts)
                 else:
                     logger.debug("Looping every %s seconds.", interval)
 
@@ -83,4 +83,4 @@ 
         return sleep_looper
 
-    return decorator+    return decorator
```
```
def while_until_true(interval, max_attempts):
    """Execute a decorated function until it returns True.

    Executes wrapped function at every number of seconds specified by interval,
    until wrapped function either returns True or max_attempts are exhausted,
    whichever comes 1st.

    Interval is in seconds. It is either a simple float value, or a callable
    that returns a float value. If it is a callable, the passed callable will
    execute on every iteration. The callable signature is:
    func(n: int) -> float

    n is the iteration counter.

    The difference between while_until_true and wait_until_true is that the
    latter will always loop to a max_attempts, whereas while_until_true will
    keep going indefinitely.

    The other notable difference to wait_until_true is that the wrapped
    function signature must be:
    func(counter, *args, **kwargs)

    This is because this decorator injects the while loop counter into the
    invoked function.

    Args:
        interval (float or callable): In seconds. How long to wait between
            executing the wrapped function. The callable signature is func(n)
            where n is the iteration counter, and should return a float.
        max_attempts (int): Execute wrapped function up to this limit. None
                      means infinite (or until wrapped function returns True).
                      Passing anything <0 also means infinite.

    Returns:
        Bool. True if wrapped function returned True. False if reached
              max_attempts without the wrapped function ever returning True.
    """
    def decorator(f):
        logger.debug("started")

        def sleep_looper(*args, **kwargs):
            i = 0
            result = False
            is_interval_callable = callable(interval)

            if not is_interval_callable:
                if max_attempts:
                    logger.debug("Looping every %s seconds for %s attempts",
                                 max_attempts)
                else:
                    logger.debug("Looping every %s seconds.", interval)

            # loop breaks explicitly for all possible exit conditions
            while True:
                i += 1
                result = f(i, *args, **kwargs)

                if result:
                    logger.debug("iteration %s. Desired state reached.", i)
                    break

                sleep = interval(i) if is_interval_callable else interval

                if max_attempts:
                    if i < max_attempts:
                        logger.debug(
                            "iteration %s. Sleeping for %ss. Still waiting...",
                            i, sleep)
                        time.sleep(sleep)
                    else:
                        logger.debug(
                            "iteration %s. Max attempts exhausted.", i)
                        break
                else:
                    # result False AND max_attempts is None means keep looping
                    # because None = infinite
                    logger.debug(
                        "iteration %s. Sleeping for %ss. Still waiting...",
                        i, sleep)
                    time.sleep(sleep)
            logger.debug("done")
            return result

        return sleep_looper

    return decorator

```
===== 32 =====
```
                     logger.debug("Looping every %s seconds for %s attempts",
                                  interval, max_attempts)
                 else:
-                    logger.debug("Looping every %s seconds.", interval)
+                    logger.debug("LOOPING EVERY %S SECONDS.", interval)
 
             # loop breaks explicitly for all possible exit conditions
             while True:
@@ -83,4 +83,4 @@ 
         return sleep_looper
 
-    return decorator+    return decorator
```
```
def while_until_true(interval, max_attempts):
    """Execute a decorated function until it returns True.

    Executes wrapped function at every number of seconds specified by interval,
    until wrapped function either returns True or max_attempts are exhausted,
    whichever comes 1st.

    Interval is in seconds. It is either a simple float value, or a callable
    that returns a float value. If it is a callable, the passed callable will
    execute on every iteration. The callable signature is:
    func(n: int) -> float

    n is the iteration counter.

    The difference between while_until_true and wait_until_true is that the
    latter will always loop to a max_attempts, whereas while_until_true will
    keep going indefinitely.

    The other notable difference to wait_until_true is that the wrapped
    function signature must be:
    func(counter, *args, **kwargs)

    This is because this decorator injects the while loop counter into the
    invoked function.

    Args:
        interval (float or callable): In seconds. How long to wait between
            executing the wrapped function. The callable signature is func(n)
            where n is the iteration counter, and should return a float.
        max_attempts (int): Execute wrapped function up to this limit. None
                      means infinite (or until wrapped function returns True).
                      Passing anything <0 also means infinite.

    Returns:
        Bool. True if wrapped function returned True. False if reached
              max_attempts without the wrapped function ever returning True.
    """
    def decorator(f):
        logger.debug("started")

        def sleep_looper(*args, **kwargs):
            i = 0
            result = False
            is_interval_callable = callable(interval)

            if not is_interval_callable:
                if max_attempts:
                    logger.debug("Looping every %s seconds for %s attempts",
                                 interval, max_attempts)
                else:
                    logger.debug("LOOPING EVERY %S SECONDS.", interval)

            # loop breaks explicitly for all possible exit conditions
            while True:
                i += 1
                result = f(i, *args, **kwargs)

                if result:
                    logger.debug("iteration %s. Desired state reached.", i)
                    break

                sleep = interval(i) if is_interval_callable else interval

                if max_attempts:
                    if i < max_attempts:
                        logger.debug(
                            "iteration %s. Sleeping for %ss. Still waiting...",
                            i, sleep)
                        time.sleep(sleep)
                    else:
                        logger.debug(
                            "iteration %s. Max attempts exhausted.", i)
                        break
                else:
                    # result False AND max_attempts is None means keep looping
                    # because None = infinite
                    logger.debug(
                        "iteration %s. Sleeping for %ss. Still waiting...",
                        i, sleep)
                    time.sleep(sleep)
            logger.debug("done")
            return result

        return sleep_looper

    return decorator

```
===== 33 =====
```
                     logger.debug("Looping every %s seconds for %s attempts",
                                  interval, max_attempts)
                 else:
-                    logger.debug("Looping every %s seconds.", interval)
+                    logger.debug("Looping every %s seconds for an indefinite number of attempts.", interval)
 
             # loop breaks explicitly for all possible exit conditions
             while True:
```
```
def while_until_true(interval, max_attempts):
    """Execute a decorated function until it returns True.

    Executes wrapped function at every number of seconds specified by interval,
    until wrapped function either returns True or max_attempts are exhausted,
    whichever comes 1st.

    Interval is in seconds. It is either a simple float value, or a callable
    that returns a float value. If it is a callable, the passed callable will
    execute on every iteration. The callable signature is:
    func(n: int) -> float

    n is the iteration counter.

    The difference between while_until_true and wait_until_true is that the
    latter will always loop to a max_attempts, whereas while_until_true will
    keep going indefinitely.

    The other notable difference to wait_until_true is that the wrapped
    function signature must be:
    func(counter, *args, **kwargs)

    This is because this decorator injects the while loop counter into the
    invoked function.

    Args:
        interval (float or callable): In seconds. How long to wait between
            executing the wrapped function. The callable signature is func(n)
            where n is the iteration counter, and should return a float.
        max_attempts (int): Execute wrapped function up to this limit. None
                      means infinite (or until wrapped function returns True).
                      Passing anything <0 also means infinite.

    Returns:
        Bool. True if wrapped function returned True. False if reached
              max_attempts without the wrapped function ever returning True.
    """
    def decorator(f):
        logger.debug("started")

        def sleep_looper(*args, **kwargs):
            i = 0
            result = False
            is_interval_callable = callable(interval)

            if not is_interval_callable:
                if max_attempts:
                    logger.debug("Looping every %s seconds for %s attempts",
                                 interval, max_attempts)
                else:
                    logger.debug("Looping every %s seconds for an indefinite number of attempts.", interval)

            # loop breaks explicitly for all possible exit conditions
            while True:
                i += 1
                result = f(i, *args, **kwargs)

                if result:
                    logger.debug("iteration %s. Desired state reached.", i)
                    break

                sleep = interval(i) if is_interval_callable else interval

                if max_attempts:
                    if i < max_attempts:
                        logger.debug(
                            "iteration %s. Sleeping for %ss. Still waiting...",
                            i, sleep)
                        time.sleep(sleep)
                    else:
                        logger.debug(
                            "iteration %s. Max attempts exhausted.", i)
                        break
                else:
                    # result False AND max_attempts is None means keep looping
                    # because None = infinite
                    logger.debug(
                        "iteration %s. Sleeping for %ss. Still waiting...",
                        i, sleep)
                    time.sleep(sleep)
            logger.debug("done")
            return result

        return sleep_looper

    return decorator
```
===== 34 =====
```
                     logger.debug("Looping every %s seconds for %s attempts",
                                  interval, max_attempts)
                 else:
-                    logger.debug("Looping every %s seconds.", interval)
+                    logger.debug("Looping every %s seconds, but max attempts is set to %s.", max_attempts)
 
             # loop breaks explicitly for all possible exit conditions
             while True:
```
```
def while_until_true(interval, max_attempts):
    """Execute a decorated function until it returns True.

    Executes wrapped function at every number of seconds specified by interval,
    until wrapped function either returns True or max_attempts are exhausted,
    whichever comes 1st.

    Interval is in seconds. It is either a simple float value, or a callable
    that returns a float value. If it is a callable, the passed callable will
    execute on every iteration. The callable signature is:
    func(n: int) -> float

    n is the iteration counter.

    The difference between while_until_true and wait_until_true is that the
    latter will always loop to a max_attempts, whereas while_until_true will
    keep going indefinitely.

    The other notable difference to wait_until_true is that the wrapped
    function signature must be:
    func(counter, *args, **kwargs)

    This is because this decorator injects the while loop counter into the
    invoked function.

    Args:
        interval (float or callable): In seconds. How long to wait between
            executing the wrapped function. The callable signature is func(n)
            where n is the iteration counter, and should return a float.
        max_attempts (int): Execute wrapped function up to this limit. None
                      means infinite (or until wrapped function returns True).
                      Passing anything <0 also means infinite.

    Returns:
        Bool. True if wrapped function returned True. False if reached
              max_attempts without the wrapped function ever returning True.
    """
    def decorator(f):
        logger.debug("started")

        def sleep_looper(*args, **kwargs):
            i = 0
            result = False
            is_interval_callable = callable(interval)

            if not is_interval_callable:
                if max_attempts:
                    logger.debug("Looping every %s seconds for %s attempts",
                                 interval, max_attempts)
                else:
                    logger.debug("Looping every %s seconds, but max attempts is set to %s.", max_attempts)

            # loop breaks explicitly for all possible exit conditions
            while True:
                i += 1
                result = f(i, *args, **kwargs)

                if result:
                    logger.debug("iteration %s. Desired state reached.", i)
                    break

                sleep = interval(i) if is_interval_callable else interval

                if max_attempts:
                    if i < max_attempts:
                        logger.debug(
                            "iteration %s. Sleeping for %ss. Still waiting...",
                            i, sleep)
                        time.sleep(sleep)
                    else:
                        logger.debug(
                            "iteration %s. Max attempts exhausted.", i)
                        break
                else:
                    # result False AND max_attempts is None means keep looping
                    # because None = infinite
                    logger.debug(
                        "iteration %s. Sleeping for %ss. Still waiting...",
                        i, sleep)
                    time.sleep(sleep)
            logger.debug("done")
            return result

        return sleep_looper

    return decorator
```
===== 35 =====
```
                     logger.debug("Looping every %s seconds for %s attempts",
                                  interval, max_attempts)
                 else:
-                    logger.debug("Looping every %s seconds.", interval)
+                    logger.debug("Looping every %s seconds, but will stop after %s attempts.", max_attempts)
 
             # loop breaks explicitly for all possible exit conditions
             while True:
```
```
def while_until_true(interval, max_attempts):
    """Execute a decorated function until it returns True.

    Executes wrapped function at every number of seconds specified by interval,
    until wrapped function either returns True or max_attempts are exhausted,
    whichever comes 1st.

    Interval is in seconds. It is either a simple float value, or a callable
    that returns a float value. If it is a callable, the passed callable will
    execute on every iteration. The callable signature is:
    func(n: int) -> float

    n is the iteration counter.

    The difference between while_until_true and wait_until_true is that the
    latter will always loop to a max_attempts, whereas while_until_true will
    keep going indefinitely.

    The other notable difference to wait_until_true is that the wrapped
    function signature must be:
    func(counter, *args, **kwargs)

    This is because this decorator injects the while loop counter into the
    invoked function.

    Args:
        interval (float or callable): In seconds. How long to wait between
            executing the wrapped function. The callable signature is func(n)
            where n is the iteration counter, and should return a float.
        max_attempts (int): Execute wrapped function up to this limit. None
                      means infinite (or until wrapped function returns True).
                      Passing anything <0 also means infinite.

    Returns:
        Bool. True if wrapped function returned True. False if reached
              max_attempts without the wrapped function ever returning True.
    """
    def decorator(f):
        logger.debug("started")

        def sleep_looper(*args, **kwargs):
            i = 0
            result = False
            is_interval_callable = callable(interval)

            if not is_interval_callable:
                if max_attempts:
                    logger.debug("Looping every %s seconds for %s attempts",
                                 interval, max_attempts)
                else:
                    logger.debug("Looping every %s seconds, but will stop after %s attempts.", max_attempts)

            # loop breaks explicitly for all possible exit conditions
            while True:
                i += 1
                result = f(i, *args, **kwargs)

                if result:
                    logger.debug("iteration %s. Desired state reached.", i)
                    break

                sleep = interval(i) if is_interval_callable else interval

                if max_attempts:
                    if i < max_attempts:
                        logger.debug(
                            "iteration %s. Sleeping for %ss. Still waiting...",
                            i, sleep)
                        time.sleep(sleep)
                    else:
                        logger.debug(
                            "iteration %s. Max attempts exhausted.", i)
                        break
                else:
                    # result False AND max_attempts is None means keep looping
                    # because None = infinite
                    logger.debug(
                        "iteration %s. Sleeping for %ss. Still waiting...",
                        i, sleep)
                    time.sleep(sleep)
            logger.debug("done")
            return result

        return sleep_looper

    return decorator
```
===== 36 =====
```
                     logger.debug("Looping every %s seconds for %s attempts",
                                  interval, max_attempts)
                 else:
-                    logger.debug("Looping every %s seconds.", interval)
+                    logger.debug("Looping every %s seconds.", )
 
             # loop breaks explicitly for all possible exit conditions
             while True:
@@ -83,4 +83,4 @@ 
         return sleep_looper
 
-    return decorator+    return decorator
```
```
def while_until_true(interval, max_attempts):
    """Execute a decorated function until it returns True.

    Executes wrapped function at every number of seconds specified by interval,
    until wrapped function either returns True or max_attempts are exhausted,
    whichever comes 1st.

    Interval is in seconds. It is either a simple float value, or a callable
    that returns a float value. If it is a callable, the passed callable will
    execute on every iteration. The callable signature is:
    func(n: int) -> float

    n is the iteration counter.

    The difference between while_until_true and wait_until_true is that the
    latter will always loop to a max_attempts, whereas while_until_true will
    keep going indefinitely.

    The other notable difference to wait_until_true is that the wrapped
    function signature must be:
    func(counter, *args, **kwargs)

    This is because this decorator injects the while loop counter into the
    invoked function.

    Args:
        interval (float or callable): In seconds. How long to wait between
            executing the wrapped function. The callable signature is func(n)
            where n is the iteration counter, and should return a float.
        max_attempts (int): Execute wrapped function up to this limit. None
                      means infinite (or until wrapped function returns True).
                      Passing anything <0 also means infinite.

    Returns:
        Bool. True if wrapped function returned True. False if reached
              max_attempts without the wrapped function ever returning True.
    """
    def decorator(f):
        logger.debug("started")

        def sleep_looper(*args, **kwargs):
            i = 0
            result = False
            is_interval_callable = callable(interval)

            if not is_interval_callable:
                if max_attempts:
                    logger.debug("Looping every %s seconds for %s attempts",
                                 interval, max_attempts)
                else:
                    logger.debug("Looping every %s seconds.", )

            # loop breaks explicitly for all possible exit conditions
            while True:
                i += 1
                result = f(i, *args, **kwargs)

                if result:
                    logger.debug("iteration %s. Desired state reached.", i)
                    break

                sleep = interval(i) if is_interval_callable else interval

                if max_attempts:
                    if i < max_attempts:
                        logger.debug(
                            "iteration %s. Sleeping for %ss. Still waiting...",
                            i, sleep)
                        time.sleep(sleep)
                    else:
                        logger.debug(
                            "iteration %s. Max attempts exhausted.", i)
                        break
                else:
                    # result False AND max_attempts is None means keep looping
                    # because None = infinite
                    logger.debug(
                        "iteration %s. Sleeping for %ss. Still waiting...",
                        i, sleep)
                    time.sleep(sleep)
            logger.debug("done")
            return result

        return sleep_looper

    return decorator

```
===== 37 =====
```
                     logger.debug("Looping every %s seconds for %s attempts",
                                  interval, max_attempts)
                 else:
-                    logger.debug("Looping every %s seconds.", interval)
+                    logger.debug("Looping every %s seconds.", None)
 
             # loop breaks explicitly for all possible exit conditions
             while True:
@@ -83,4 +83,4 @@ 
         return sleep_looper
 
-    return decorator+    return decorator
```
```
def while_until_true(interval, max_attempts):
    """Execute a decorated function until it returns True.

    Executes wrapped function at every number of seconds specified by interval,
    until wrapped function either returns True or max_attempts are exhausted,
    whichever comes 1st.

    Interval is in seconds. It is either a simple float value, or a callable
    that returns a float value. If it is a callable, the passed callable will
    execute on every iteration. The callable signature is:
    func(n: int) -> float

    n is the iteration counter.

    The difference between while_until_true and wait_until_true is that the
    latter will always loop to a max_attempts, whereas while_until_true will
    keep going indefinitely.

    The other notable difference to wait_until_true is that the wrapped
    function signature must be:
    func(counter, *args, **kwargs)

    This is because this decorator injects the while loop counter into the
    invoked function.

    Args:
        interval (float or callable): In seconds. How long to wait between
            executing the wrapped function. The callable signature is func(n)
            where n is the iteration counter, and should return a float.
        max_attempts (int): Execute wrapped function up to this limit. None
                      means infinite (or until wrapped function returns True).
                      Passing anything <0 also means infinite.

    Returns:
        Bool. True if wrapped function returned True. False if reached
              max_attempts without the wrapped function ever returning True.
    """
    def decorator(f):
        logger.debug("started")

        def sleep_looper(*args, **kwargs):
            i = 0
            result = False
            is_interval_callable = callable(interval)

            if not is_interval_callable:
                if max_attempts:
                    logger.debug("Looping every %s seconds for %s attempts",
                                 interval, max_attempts)
                else:
                    logger.debug("Looping every %s seconds.", None)

            # loop breaks explicitly for all possible exit conditions
            while True:
                i += 1
                result = f(i, *args, **kwargs)

                if result:
                    logger.debug("iteration %s. Desired state reached.", i)
                    break

                sleep = interval(i) if is_interval_callable else interval

                if max_attempts:
                    if i < max_attempts:
                        logger.debug(
                            "iteration %s. Sleeping for %ss. Still waiting...",
                            i, sleep)
                        time.sleep(sleep)
                    else:
                        logger.debug(
                            "iteration %s. Max attempts exhausted.", i)
                        break
                else:
                    # result False AND max_attempts is None means keep looping
                    # because None = infinite
                    logger.debug(
                        "iteration %s. Sleeping for %ss. Still waiting...",
                        i, sleep)
                    time.sleep(sleep)
            logger.debug("done")
            return result

        return sleep_looper

    return decorator

```
===== 38 =====
```
                     logger.debug("Looping every %s seconds for %s attempts",
                                  interval, max_attempts)
                 else:
-                    logger.debug("Looping every %s seconds.", interval)
+                    logger.debug("Starting loop with an interval of %s seconds.", interval)
 
             # loop breaks explicitly for all possible exit conditions
             while True:
```
```
def while_until_true(interval, max_attempts):
    """Execute a decorated function until it returns True.

    Executes wrapped function at every number of seconds specified by interval,
    until wrapped function either returns True or max_attempts are exhausted,
    whichever comes 1st.

    Interval is in seconds. It is either a simple float value, or a callable
    that returns a float value. If it is a callable, the passed callable will
    execute on every iteration. The callable signature is:
    func(n: int) -> float

    n is the iteration counter.

    The difference between while_until_true and wait_until_true is that the
    latter will always loop to a max_attempts, whereas while_until_true will
    keep going indefinitely.

    The other notable difference to wait_until_true is that the wrapped
    function signature must be:
    func(counter, *args, **kwargs)

    This is because this decorator injects the while loop counter into the
    invoked function.

    Args:
        interval (float or callable): In seconds. How long to wait between
            executing the wrapped function. The callable signature is func(n)
            where n is the iteration counter, and should return a float.
        max_attempts (int): Execute wrapped function up to this limit. None
                      means infinite (or until wrapped function returns True).
                      Passing anything <0 also means infinite.

    Returns:
        Bool. True if wrapped function returned True. False if reached
              max_attempts without the wrapped function ever returning True.
    """
    def decorator(f):
        logger.debug("started")

        def sleep_looper(*args, **kwargs):
            i = 0
            result = False
            is_interval_callable = callable(interval)

            if not is_interval_callable:
                if max_attempts:
                    logger.debug("Looping every %s seconds for %s attempts",
                                 interval, max_attempts)
                else:
                    logger.debug("Starting loop with an interval of %s seconds.", interval)

            # loop breaks explicitly for all possible exit conditions
            while True:
                i += 1
                result = f(i, *args, **kwargs)

                if result:
                    logger.debug("iteration %s. Desired state reached.", i)
                    break

                sleep = interval(i) if is_interval_callable else interval

                if max_attempts:
                    if i < max_attempts:
                        logger.debug(
                            "iteration %s. Sleeping for %ss. Still waiting...",
                            i, sleep)
                        time.sleep(sleep)
                    else:
                        logger.debug(
                            "iteration %s. Max attempts exhausted.", i)
                        break
                else:
                    # result False AND max_attempts is None means keep looping
                    # because None = infinite
                    logger.debug(
                        "iteration %s. Sleeping for %ss. Still waiting...",
                        i, sleep)
                    time.sleep(sleep)
            logger.debug("done")
            return result

        return sleep_looper

    return decorator
```
===== 39 =====
```
                     logger.debug("Looping every %s seconds for %s attempts",
                                  interval, max_attempts)
                 else:
-                    logger.debug("Looping every %s seconds.", interval)
+                    logger.debug("Waiting for %s seconds before the next attempt.", interval)
 
             # loop breaks explicitly for all possible exit conditions
             while True:
```
```
def while_until_true(interval, max_attempts):
    """Execute a decorated function until it returns True.

    Executes wrapped function at every number of seconds specified by interval,
    until wrapped function either returns True or max_attempts are exhausted,
    whichever comes 1st.

    Interval is in seconds. It is either a simple float value, or a callable
    that returns a float value. If it is a callable, the passed callable will
    execute on every iteration. The callable signature is:
    func(n: int) -> float

    n is the iteration counter.

    The difference between while_until_true and wait_until_true is that the
    latter will always loop to a max_attempts, whereas while_until_true will
    keep going indefinitely.

    The other notable difference to wait_until_true is that the wrapped
    function signature must be:
    func(counter, *args, **kwargs)

    This is because this decorator injects the while loop counter into the
    invoked function.

    Args:
        interval (float or callable): In seconds. How long to wait between
            executing the wrapped function. The callable signature is func(n)
            where n is the iteration counter, and should return a float.
        max_attempts (int): Execute wrapped function up to this limit. None
                      means infinite (or until wrapped function returns True).
                      Passing anything <0 also means infinite.

    Returns:
        Bool. True if wrapped function returned True. False if reached
              max_attempts without the wrapped function ever returning True.
    """
    def decorator(f):
        logger.debug("started")

        def sleep_looper(*args, **kwargs):
            i = 0
            result = False
            is_interval_callable = callable(interval)

            if not is_interval_callable:
                if max_attempts:
                    logger.debug("Looping every %s seconds for %s attempts",
                                 interval, max_attempts)
                else:
                    logger.debug("Waiting for %s seconds before the next attempt.", interval)

            # loop breaks explicitly for all possible exit conditions
            while True:
                i += 1
                result = f(i, *args, **kwargs)

                if result:
                    logger.debug("iteration %s. Desired state reached.", i)
                    break

                sleep = interval(i) if is_interval_callable else interval

                if max_attempts:
                    if i < max_attempts:
                        logger.debug(
                            "iteration %s. Sleeping for %ss. Still waiting...",
                            i, sleep)
                        time.sleep(sleep)
                    else:
                        logger.debug(
                            "iteration %s. Max attempts exhausted.", i)
                        break
                else:
                    # result False AND max_attempts is None means keep looping
                    # because None = infinite
                    logger.debug(
                        "iteration %s. Sleeping for %ss. Still waiting...",
                        i, sleep)
                    time.sleep(sleep)
            logger.debug("done")
            return result

        return sleep_looper

    return decorator
```
===== 40 =====
```
                     logger.debug("Looping every %s seconds for %s attempts",
                                  interval, max_attempts)
                 else:
-                    logger.debug("Looping every %s seconds.", interval)
+                    logger.debug("XXLooping every %s seconds.XX", interval)
 
             # loop breaks explicitly for all possible exit conditions
             while True:
@@ -83,4 +83,4 @@ 
         return sleep_looper
 
-    return decorator+    return decorator
```
```
def while_until_true(interval, max_attempts):
    """Execute a decorated function until it returns True.

    Executes wrapped function at every number of seconds specified by interval,
    until wrapped function either returns True or max_attempts are exhausted,
    whichever comes 1st.

    Interval is in seconds. It is either a simple float value, or a callable
    that returns a float value. If it is a callable, the passed callable will
    execute on every iteration. The callable signature is:
    func(n: int) -> float

    n is the iteration counter.

    The difference between while_until_true and wait_until_true is that the
    latter will always loop to a max_attempts, whereas while_until_true will
    keep going indefinitely.

    The other notable difference to wait_until_true is that the wrapped
    function signature must be:
    func(counter, *args, **kwargs)

    This is because this decorator injects the while loop counter into the
    invoked function.

    Args:
        interval (float or callable): In seconds. How long to wait between
            executing the wrapped function. The callable signature is func(n)
            where n is the iteration counter, and should return a float.
        max_attempts (int): Execute wrapped function up to this limit. None
                      means infinite (or until wrapped function returns True).
                      Passing anything <0 also means infinite.

    Returns:
        Bool. True if wrapped function returned True. False if reached
              max_attempts without the wrapped function ever returning True.
    """
    def decorator(f):
        logger.debug("started")

        def sleep_looper(*args, **kwargs):
            i = 0
            result = False
            is_interval_callable = callable(interval)

            if not is_interval_callable:
                if max_attempts:
                    logger.debug("Looping every %s seconds for %s attempts",
                                 interval, max_attempts)
                else:
                    logger.debug("XXLooping every %s seconds.XX", interval)

            # loop breaks explicitly for all possible exit conditions
            while True:
                i += 1
                result = f(i, *args, **kwargs)

                if result:
                    logger.debug("iteration %s. Desired state reached.", i)
                    break

                sleep = interval(i) if is_interval_callable else interval

                if max_attempts:
                    if i < max_attempts:
                        logger.debug(
                            "iteration %s. Sleeping for %ss. Still waiting...",
                            i, sleep)
                        time.sleep(sleep)
                    else:
                        logger.debug(
                            "iteration %s. Max attempts exhausted.", i)
                        break
                else:
                    # result False AND max_attempts is None means keep looping
                    # because None = infinite
                    logger.debug(
                        "iteration %s. Sleeping for %ss. Still waiting...",
                        i, sleep)
                    time.sleep(sleep)
            logger.debug("done")
            return result

        return sleep_looper

    return decorator

```
===== 41 =====
```
                     logger.debug("Looping every %s seconds for %s attempts",
                                  interval, max_attempts)
                 else:
-                    logger.debug("Looping every %s seconds.", interval)
+                    logger.debug("looping every %s seconds.", interval)
 
             # loop breaks explicitly for all possible exit conditions
             while True:
@@ -83,4 +83,4 @@ 
         return sleep_looper
 
-    return decorator+    return decorator
```
```
def while_until_true(interval, max_attempts):
    """Execute a decorated function until it returns True.

    Executes wrapped function at every number of seconds specified by interval,
    until wrapped function either returns True or max_attempts are exhausted,
    whichever comes 1st.

    Interval is in seconds. It is either a simple float value, or a callable
    that returns a float value. If it is a callable, the passed callable will
    execute on every iteration. The callable signature is:
    func(n: int) -> float

    n is the iteration counter.

    The difference between while_until_true and wait_until_true is that the
    latter will always loop to a max_attempts, whereas while_until_true will
    keep going indefinitely.

    The other notable difference to wait_until_true is that the wrapped
    function signature must be:
    func(counter, *args, **kwargs)

    This is because this decorator injects the while loop counter into the
    invoked function.

    Args:
        interval (float or callable): In seconds. How long to wait between
            executing the wrapped function. The callable signature is func(n)
            where n is the iteration counter, and should return a float.
        max_attempts (int): Execute wrapped function up to this limit. None
                      means infinite (or until wrapped function returns True).
                      Passing anything <0 also means infinite.

    Returns:
        Bool. True if wrapped function returned True. False if reached
              max_attempts without the wrapped function ever returning True.
    """
    def decorator(f):
        logger.debug("started")

        def sleep_looper(*args, **kwargs):
            i = 0
            result = False
            is_interval_callable = callable(interval)

            if not is_interval_callable:
                if max_attempts:
                    logger.debug("Looping every %s seconds for %s attempts",
                                 interval, max_attempts)
                else:
                    logger.debug("looping every %s seconds.", interval)

            # loop breaks explicitly for all possible exit conditions
            while True:
                i += 1
                result = f(i, *args, **kwargs)

                if result:
                    logger.debug("iteration %s. Desired state reached.", i)
                    break

                sleep = interval(i) if is_interval_callable else interval

                if max_attempts:
                    if i < max_attempts:
                        logger.debug(
                            "iteration %s. Sleeping for %ss. Still waiting...",
                            i, sleep)
                        time.sleep(sleep)
                    else:
                        logger.debug(
                            "iteration %s. Max attempts exhausted.", i)
                        break
                else:
                    # result False AND max_attempts is None means keep looping
                    # because None = infinite
                    logger.debug(
                        "iteration %s. Sleeping for %ss. Still waiting...",
                        i, sleep)
                    time.sleep(sleep)
            logger.debug("done")
            return result

        return sleep_looper

    return decorator

```
===== 42 =====
```
                     logger.debug("Looping every %s seconds for %s attempts",
                                  interval, max_attempts)
                 else:
-                    logger.debug("Looping every %s seconds.", interval)
+                    logger.debug(None, interval)
 
             # loop breaks explicitly for all possible exit conditions
             while True:
@@ -83,4 +83,4 @@ 
         return sleep_looper
 
-    return decorator+    return decorator
```
```
def while_until_true(interval, max_attempts):
    """Execute a decorated function until it returns True.

    Executes wrapped function at every number of seconds specified by interval,
    until wrapped function either returns True or max_attempts are exhausted,
    whichever comes 1st.

    Interval is in seconds. It is either a simple float value, or a callable
    that returns a float value. If it is a callable, the passed callable will
    execute on every iteration. The callable signature is:
    func(n: int) -> float

    n is the iteration counter.

    The difference between while_until_true and wait_until_true is that the
    latter will always loop to a max_attempts, whereas while_until_true will
    keep going indefinitely.

    The other notable difference to wait_until_true is that the wrapped
    function signature must be:
    func(counter, *args, **kwargs)

    This is because this decorator injects the while loop counter into the
    invoked function.

    Args:
        interval (float or callable): In seconds. How long to wait between
            executing the wrapped function. The callable signature is func(n)
            where n is the iteration counter, and should return a float.
        max_attempts (int): Execute wrapped function up to this limit. None
                      means infinite (or until wrapped function returns True).
                      Passing anything <0 also means infinite.

    Returns:
        Bool. True if wrapped function returned True. False if reached
              max_attempts without the wrapped function ever returning True.
    """
    def decorator(f):
        logger.debug("started")

        def sleep_looper(*args, **kwargs):
            i = 0
            result = False
            is_interval_callable = callable(interval)

            if not is_interval_callable:
                if max_attempts:
                    logger.debug("Looping every %s seconds for %s attempts",
                                 interval, max_attempts)
                else:
                    logger.debug(None, interval)

            # loop breaks explicitly for all possible exit conditions
            while True:
                i += 1
                result = f(i, *args, **kwargs)

                if result:
                    logger.debug("iteration %s. Desired state reached.", i)
                    break

                sleep = interval(i) if is_interval_callable else interval

                if max_attempts:
                    if i < max_attempts:
                        logger.debug(
                            "iteration %s. Sleeping for %ss. Still waiting...",
                            i, sleep)
                        time.sleep(sleep)
                    else:
                        logger.debug(
                            "iteration %s. Max attempts exhausted.", i)
                        break
                else:
                    # result False AND max_attempts is None means keep looping
                    # because None = infinite
                    logger.debug(
                        "iteration %s. Sleeping for %ss. Still waiting...",
                        i, sleep)
                    time.sleep(sleep)
            logger.debug("done")
            return result

        return sleep_looper

    return decorator

```
===== 43 =====
```
                     logger.debug("Looping every %s seconds for %s attempts",
                                  interval, max_attempts)
                 else:
-                    logger.debug("Looping every %s seconds.", interval)
+                    logger.debug(interval)
 
             # loop breaks explicitly for all possible exit conditions
             while True:
@@ -83,4 +83,4 @@ 
         return sleep_looper
 
-    return decorator+    return decorator
```
```
def while_until_true(interval, max_attempts):
    """Execute a decorated function until it returns True.

    Executes wrapped function at every number of seconds specified by interval,
    until wrapped function either returns True or max_attempts are exhausted,
    whichever comes 1st.

    Interval is in seconds. It is either a simple float value, or a callable
    that returns a float value. If it is a callable, the passed callable will
    execute on every iteration. The callable signature is:
    func(n: int) -> float

    n is the iteration counter.

    The difference between while_until_true and wait_until_true is that the
    latter will always loop to a max_attempts, whereas while_until_true will
    keep going indefinitely.

    The other notable difference to wait_until_true is that the wrapped
    function signature must be:
    func(counter, *args, **kwargs)

    This is because this decorator injects the while loop counter into the
    invoked function.

    Args:
        interval (float or callable): In seconds. How long to wait between
            executing the wrapped function. The callable signature is func(n)
            where n is the iteration counter, and should return a float.
        max_attempts (int): Execute wrapped function up to this limit. None
                      means infinite (or until wrapped function returns True).
                      Passing anything <0 also means infinite.

    Returns:
        Bool. True if wrapped function returned True. False if reached
              max_attempts without the wrapped function ever returning True.
    """
    def decorator(f):
        logger.debug("started")

        def sleep_looper(*args, **kwargs):
            i = 0
            result = False
            is_interval_callable = callable(interval)

            if not is_interval_callable:
                if max_attempts:
                    logger.debug("Looping every %s seconds for %s attempts",
                                 interval, max_attempts)
                else:
                    logger.debug(interval)

            # loop breaks explicitly for all possible exit conditions
            while True:
                i += 1
                result = f(i, *args, **kwargs)

                if result:
                    logger.debug("iteration %s. Desired state reached.", i)
                    break

                sleep = interval(i) if is_interval_callable else interval

                if max_attempts:
                    if i < max_attempts:
                        logger.debug(
                            "iteration %s. Sleeping for %ss. Still waiting...",
                            i, sleep)
                        time.sleep(sleep)
                    else:
                        logger.debug(
                            "iteration %s. Max attempts exhausted.", i)
                        break
                else:
                    # result False AND max_attempts is None means keep looping
                    # because None = infinite
                    logger.debug(
                        "iteration %s. Sleeping for %ss. Still waiting...",
                        i, sleep)
                    time.sleep(sleep)
            logger.debug("done")
            return result

        return sleep_looper

    return decorator

```
===== 44 =====
```
                     logger.debug("Looping every %s seconds.", interval)
 
             # loop breaks explicitly for all possible exit conditions
-            while True:
+            for _ in range(max_attempts):
                 i += 1
                 result = f(i, *args, **kwargs)
```
```
def while_until_true(interval, max_attempts):
    """Execute a decorated function until it returns True.

    Executes wrapped function at every number of seconds specified by interval,
    until wrapped function either returns True or max_attempts are exhausted,
    whichever comes 1st.

    Interval is in seconds. It is either a simple float value, or a callable
    that returns a float value. If it is a callable, the passed callable will
    execute on every iteration. The callable signature is:
    func(n: int) -> float

    n is the iteration counter.

    The difference between while_until_true and wait_until_true is that the
    latter will always loop to a max_attempts, whereas while_until_true will
    keep going indefinitely.

    The other notable difference to wait_until_true is that the wrapped
    function signature must be:
    func(counter, *args, **kwargs)

    This is because this decorator injects the while loop counter into the
    invoked function.

    Args:
        interval (float or callable): In seconds. How long to wait between
            executing the wrapped function. The callable signature is func(n)
            where n is the iteration counter, and should return a float.
        max_attempts (int): Execute wrapped function up to this limit. None
                      means infinite (or until wrapped function returns True).
                      Passing anything <0 also means infinite.

    Returns:
        Bool. True if wrapped function returned True. False if reached
              max_attempts without the wrapped function ever returning True.
    """
    def decorator(f):
        logger.debug("started")

        def sleep_looper(*args, **kwargs):
            i = 0
            result = False
            is_interval_callable = callable(interval)

            if not is_interval_callable:
                if max_attempts:
                    logger.debug("Looping every %s seconds for %s attempts",
                                 interval, max_attempts)
                else:
                    logger.debug("Looping every %s seconds.", interval)

            # loop breaks explicitly for all possible exit conditions
            for _ in range(max_attempts):
                i += 1
                result = f(i, *args, **kwargs)

                if result:
                    logger.debug("iteration %s. Desired state reached.", i)
                    break

                sleep = interval(i) if is_interval_callable else interval

                if max_attempts:
                    if i < max_attempts:
                        logger.debug(
                            "iteration %s. Sleeping for %ss. Still waiting...",
                            i, sleep)
                        time.sleep(sleep)
                    else:
                        logger.debug(
                            "iteration %s. Max attempts exhausted.", i)
                        break
                else:
                    # result False AND max_attempts is None means keep looping
                    # because None = infinite
                    logger.debug(
                        "iteration %s. Sleeping for %ss. Still waiting...",
                        i, sleep)
                    time.sleep(sleep)
            logger.debug("done")
            return result

        return sleep_looper

    return decorator
```
===== 45 =====
```
                     logger.debug("Looping every %s seconds.", interval)
 
             # loop breaks explicitly for all possible exit conditions
-            while True:
+            while False:
                 i += 1
                 result = f(i, *args, **kwargs)
 
@@ -83,4 +83,4 @@ 
         return sleep_looper
 
-    return decorator+    return decorator
```
```
def while_until_true(interval, max_attempts):
    """Execute a decorated function until it returns True.

    Executes wrapped function at every number of seconds specified by interval,
    until wrapped function either returns True or max_attempts are exhausted,
    whichever comes 1st.

    Interval is in seconds. It is either a simple float value, or a callable
    that returns a float value. If it is a callable, the passed callable will
    execute on every iteration. The callable signature is:
    func(n: int) -> float

    n is the iteration counter.

    The difference between while_until_true and wait_until_true is that the
    latter will always loop to a max_attempts, whereas while_until_true will
    keep going indefinitely.

    The other notable difference to wait_until_true is that the wrapped
    function signature must be:
    func(counter, *args, **kwargs)

    This is because this decorator injects the while loop counter into the
    invoked function.

    Args:
        interval (float or callable): In seconds. How long to wait between
            executing the wrapped function. The callable signature is func(n)
            where n is the iteration counter, and should return a float.
        max_attempts (int): Execute wrapped function up to this limit. None
                      means infinite (or until wrapped function returns True).
                      Passing anything <0 also means infinite.

    Returns:
        Bool. True if wrapped function returned True. False if reached
              max_attempts without the wrapped function ever returning True.
    """
    def decorator(f):
        logger.debug("started")

        def sleep_looper(*args, **kwargs):
            i = 0
            result = False
            is_interval_callable = callable(interval)

            if not is_interval_callable:
                if max_attempts:
                    logger.debug("Looping every %s seconds for %s attempts",
                                 interval, max_attempts)
                else:
                    logger.debug("Looping every %s seconds.", interval)

            # loop breaks explicitly for all possible exit conditions
            while False:
                i += 1
                result = f(i, *args, **kwargs)

                if result:
                    logger.debug("iteration %s. Desired state reached.", i)
                    break

                sleep = interval(i) if is_interval_callable else interval

                if max_attempts:
                    if i < max_attempts:
                        logger.debug(
                            "iteration %s. Sleeping for %ss. Still waiting...",
                            i, sleep)
                        time.sleep(sleep)
                    else:
                        logger.debug(
                            "iteration %s. Max attempts exhausted.", i)
                        break
                else:
                    # result False AND max_attempts is None means keep looping
                    # because None = infinite
                    logger.debug(
                        "iteration %s. Sleeping for %ss. Still waiting...",
                        i, sleep)
                    time.sleep(sleep)
            logger.debug("done")
            return result

        return sleep_looper

    return decorator

```
===== 46 =====
```
                     logger.debug("Looping every %s seconds.", interval)
 
             # loop breaks explicitly for all possible exit conditions
-            while True:
+            while i < 10:  # Fixed iteration count
                 i += 1
                 result = f(i, *args, **kwargs)
```
```
def while_until_true(interval, max_attempts):
    """Execute a decorated function until it returns True.

    Executes wrapped function at every number of seconds specified by interval,
    until wrapped function either returns True or max_attempts are exhausted,
    whichever comes 1st.

    Interval is in seconds. It is either a simple float value, or a callable
    that returns a float value. If it is a callable, the passed callable will
    execute on every iteration. The callable signature is:
    func(n: int) -> float

    n is the iteration counter.

    The difference between while_until_true and wait_until_true is that the
    latter will always loop to a max_attempts, whereas while_until_true will
    keep going indefinitely.

    The other notable difference to wait_until_true is that the wrapped
    function signature must be:
    func(counter, *args, **kwargs)

    This is because this decorator injects the while loop counter into the
    invoked function.

    Args:
        interval (float or callable): In seconds. How long to wait between
            executing the wrapped function. The callable signature is func(n)
            where n is the iteration counter, and should return a float.
        max_attempts (int): Execute wrapped function up to this limit. None
                      means infinite (or until wrapped function returns True).
                      Passing anything <0 also means infinite.

    Returns:
        Bool. True if wrapped function returned True. False if reached
              max_attempts without the wrapped function ever returning True.
    """
    def decorator(f):
        logger.debug("started")

        def sleep_looper(*args, **kwargs):
            i = 0
            result = False
            is_interval_callable = callable(interval)

            if not is_interval_callable:
                if max_attempts:
                    logger.debug("Looping every %s seconds for %s attempts",
                                 interval, max_attempts)
                else:
                    logger.debug("Looping every %s seconds.", interval)

            # loop breaks explicitly for all possible exit conditions
            while i < 10:  # Fixed iteration count
                i += 1
                result = f(i, *args, **kwargs)

                if result:
                    logger.debug("iteration %s. Desired state reached.", i)
                    break

                sleep = interval(i) if is_interval_callable else interval

                if max_attempts:
                    if i < max_attempts:
                        logger.debug(
                            "iteration %s. Sleeping for %ss. Still waiting...",
                            i, sleep)
                        time.sleep(sleep)
                    else:
                        logger.debug(
                            "iteration %s. Max attempts exhausted.", i)
                        break
                else:
                    # result False AND max_attempts is None means keep looping
                    # because None = infinite
                    logger.debug(
                        "iteration %s. Sleeping for %ss. Still waiting...",
                        i, sleep)
                    time.sleep(sleep)
            logger.debug("done")
            return result

        return sleep_looper

    return decorator
```
===== 47 =====
```
                     logger.debug("Looping every %s seconds.", interval)
 
             # loop breaks explicitly for all possible exit conditions
-            while True:
+            while i < max_attempts:
                 i += 1
                 result = f(i, *args, **kwargs)
```
```
def while_until_true(interval, max_attempts):
    """Execute a decorated function until it returns True.

    Executes wrapped function at every number of seconds specified by interval,
    until wrapped function either returns True or max_attempts are exhausted,
    whichever comes 1st.

    Interval is in seconds. It is either a simple float value, or a callable
    that returns a float value. If it is a callable, the passed callable will
    execute on every iteration. The callable signature is:
    func(n: int) -> float

    n is the iteration counter.

    The difference between while_until_true and wait_until_true is that the
    latter will always loop to a max_attempts, whereas while_until_true will
    keep going indefinitely.

    The other notable difference to wait_until_true is that the wrapped
    function signature must be:
    func(counter, *args, **kwargs)

    This is because this decorator injects the while loop counter into the
    invoked function.

    Args:
        interval (float or callable): In seconds. How long to wait between
            executing the wrapped function. The callable signature is func(n)
            where n is the iteration counter, and should return a float.
        max_attempts (int): Execute wrapped function up to this limit. None
                      means infinite (or until wrapped function returns True).
                      Passing anything <0 also means infinite.

    Returns:
        Bool. True if wrapped function returned True. False if reached
              max_attempts without the wrapped function ever returning True.
    """
    def decorator(f):
        logger.debug("started")

        def sleep_looper(*args, **kwargs):
            i = 0
            result = False
            is_interval_callable = callable(interval)

            if not is_interval_callable:
                if max_attempts:
                    logger.debug("Looping every %s seconds for %s attempts",
                                 interval, max_attempts)
                else:
                    logger.debug("Looping every %s seconds.", interval)

            # loop breaks explicitly for all possible exit conditions
            while i < max_attempts:
                i += 1
                result = f(i, *args, **kwargs)

                if result:
                    logger.debug("iteration %s. Desired state reached.", i)
                    break

                sleep = interval(i) if is_interval_callable else interval

                if max_attempts:
                    if i < max_attempts:
                        logger.debug(
                            "iteration %s. Sleeping for %ss. Still waiting...",
                            i, sleep)
                        time.sleep(sleep)
                    else:
                        logger.debug(
                            "iteration %s. Max attempts exhausted.", i)
                        break
                else:
                    # result False AND max_attempts is None means keep looping
                    # because None = infinite
                    logger.debug(
                        "iteration %s. Sleeping for %ss. Still waiting...",
                        i, sleep)
                    time.sleep(sleep)
            logger.debug("done")
            return result

        return sleep_looper

    return decorator
```
===== 48 =====
```
             # loop breaks explicitly for all possible exit conditions
             while True:
                 i += 1
-                result = f(i, *args, **kwargs)
+                result = f(*args, **kwargs)
 
                 if result:
                     logger.debug("iteration %s. Desired state reached.", i)
@@ -83,4 +83,4 @@ 
         return sleep_looper
 
-    return decorator+    return decorator
```
```
def while_until_true(interval, max_attempts):
    """Execute a decorated function until it returns True.

    Executes wrapped function at every number of seconds specified by interval,
    until wrapped function either returns True or max_attempts are exhausted,
    whichever comes 1st.

    Interval is in seconds. It is either a simple float value, or a callable
    that returns a float value. If it is a callable, the passed callable will
    execute on every iteration. The callable signature is:
    func(n: int) -> float

    n is the iteration counter.

    The difference between while_until_true and wait_until_true is that the
    latter will always loop to a max_attempts, whereas while_until_true will
    keep going indefinitely.

    The other notable difference to wait_until_true is that the wrapped
    function signature must be:
    func(counter, *args, **kwargs)

    This is because this decorator injects the while loop counter into the
    invoked function.

    Args:
        interval (float or callable): In seconds. How long to wait between
            executing the wrapped function. The callable signature is func(n)
            where n is the iteration counter, and should return a float.
        max_attempts (int): Execute wrapped function up to this limit. None
                      means infinite (or until wrapped function returns True).
                      Passing anything <0 also means infinite.

    Returns:
        Bool. True if wrapped function returned True. False if reached
              max_attempts without the wrapped function ever returning True.
    """
    def decorator(f):
        logger.debug("started")

        def sleep_looper(*args, **kwargs):
            i = 0
            result = False
            is_interval_callable = callable(interval)

            if not is_interval_callable:
                if max_attempts:
                    logger.debug("Looping every %s seconds for %s attempts",
                                 interval, max_attempts)
                else:
                    logger.debug("Looping every %s seconds.", interval)

            # loop breaks explicitly for all possible exit conditions
            while True:
                i += 1
                result = f(*args, **kwargs)

                if result:
                    logger.debug("iteration %s. Desired state reached.", i)
                    break

                sleep = interval(i) if is_interval_callable else interval

                if max_attempts:
                    if i < max_attempts:
                        logger.debug(
                            "iteration %s. Sleeping for %ss. Still waiting...",
                            i, sleep)
                        time.sleep(sleep)
                    else:
                        logger.debug(
                            "iteration %s. Max attempts exhausted.", i)
                        break
                else:
                    # result False AND max_attempts is None means keep looping
                    # because None = infinite
                    logger.debug(
                        "iteration %s. Sleeping for %ss. Still waiting...",
                        i, sleep)
                    time.sleep(sleep)
            logger.debug("done")
            return result

        return sleep_looper

    return decorator

```
===== 49 =====
```
             # loop breaks explicitly for all possible exit conditions
             while True:
                 i += 1
-                result = f(i, *args, **kwargs)
+                result = f(*args, **kwargs)  # Missing the iteration counter
 
                 if result:
                     logger.debug("iteration %s. Desired state reached.", i)
```
```
def while_until_true(interval, max_attempts):
    """Execute a decorated function until it returns True.

    Executes wrapped function at every number of seconds specified by interval,
    until wrapped function either returns True or max_attempts are exhausted,
    whichever comes 1st.

    Interval is in seconds. It is either a simple float value, or a callable
    that returns a float value. If it is a callable, the passed callable will
    execute on every iteration. The callable signature is:
    func(n: int) -> float

    n is the iteration counter.

    The difference between while_until_true and wait_until_true is that the
    latter will always loop to a max_attempts, whereas while_until_true will
    keep going indefinitely.

    The other notable difference to wait_until_true is that the wrapped
    function signature must be:
    func(counter, *args, **kwargs)

    This is because this decorator injects the while loop counter into the
    invoked function.

    Args:
        interval (float or callable): In seconds. How long to wait between
            executing the wrapped function. The callable signature is func(n)
            where n is the iteration counter, and should return a float.
        max_attempts (int): Execute wrapped function up to this limit. None
                      means infinite (or until wrapped function returns True).
                      Passing anything <0 also means infinite.

    Returns:
        Bool. True if wrapped function returned True. False if reached
              max_attempts without the wrapped function ever returning True.
    """
    def decorator(f):
        logger.debug("started")

        def sleep_looper(*args, **kwargs):
            i = 0
            result = False
            is_interval_callable = callable(interval)

            if not is_interval_callable:
                if max_attempts:
                    logger.debug("Looping every %s seconds for %s attempts",
                                 interval, max_attempts)
                else:
                    logger.debug("Looping every %s seconds.", interval)

            # loop breaks explicitly for all possible exit conditions
            while True:
                i += 1
                result = f(*args, **kwargs)  # Missing the iteration counter

                if result:
                    logger.debug("iteration %s. Desired state reached.", i)
                    break

                sleep = interval(i) if is_interval_callable else interval

                if max_attempts:
                    if i < max_attempts:
                        logger.debug(
                            "iteration %s. Sleeping for %ss. Still waiting...",
                            i, sleep)
                        time.sleep(sleep)
                    else:
                        logger.debug(
                            "iteration %s. Max attempts exhausted.", i)
                        break
                else:
                    # result False AND max_attempts is None means keep looping
                    # because None = infinite
                    logger.debug(
                        "iteration %s. Sleeping for %ss. Still waiting...",
                        i, sleep)
                    time.sleep(sleep)
            logger.debug("done")
            return result

        return sleep_looper

    return decorator
```
===== 50 =====
```
             # loop breaks explicitly for all possible exit conditions
             while True:
                 i += 1
-                result = f(i, *args, **kwargs)
+                result = f(i + 1, *args, **kwargs)  # Off-by-one error in the iteration counter
 
                 if result:
                     logger.debug("iteration %s. Desired state reached.", i)
```
```
def while_until_true(interval, max_attempts):
    """Execute a decorated function until it returns True.

    Executes wrapped function at every number of seconds specified by interval,
    until wrapped function either returns True or max_attempts are exhausted,
    whichever comes 1st.

    Interval is in seconds. It is either a simple float value, or a callable
    that returns a float value. If it is a callable, the passed callable will
    execute on every iteration. The callable signature is:
    func(n: int) -> float

    n is the iteration counter.

    The difference between while_until_true and wait_until_true is that the
    latter will always loop to a max_attempts, whereas while_until_true will
    keep going indefinitely.

    The other notable difference to wait_until_true is that the wrapped
    function signature must be:
    func(counter, *args, **kwargs)

    This is because this decorator injects the while loop counter into the
    invoked function.

    Args:
        interval (float or callable): In seconds. How long to wait between
            executing the wrapped function. The callable signature is func(n)
            where n is the iteration counter, and should return a float.
        max_attempts (int): Execute wrapped function up to this limit. None
                      means infinite (or until wrapped function returns True).
                      Passing anything <0 also means infinite.

    Returns:
        Bool. True if wrapped function returned True. False if reached
              max_attempts without the wrapped function ever returning True.
    """
    def decorator(f):
        logger.debug("started")

        def sleep_looper(*args, **kwargs):
            i = 0
            result = False
            is_interval_callable = callable(interval)

            if not is_interval_callable:
                if max_attempts:
                    logger.debug("Looping every %s seconds for %s attempts",
                                 interval, max_attempts)
                else:
                    logger.debug("Looping every %s seconds.", interval)

            # loop breaks explicitly for all possible exit conditions
            while True:
                i += 1
                result = f(i + 1, *args, **kwargs)  # Off-by-one error in the iteration counter

                if result:
                    logger.debug("iteration %s. Desired state reached.", i)
                    break

                sleep = interval(i) if is_interval_callable else interval

                if max_attempts:
                    if i < max_attempts:
                        logger.debug(
                            "iteration %s. Sleeping for %ss. Still waiting...",
                            i, sleep)
                        time.sleep(sleep)
                    else:
                        logger.debug(
                            "iteration %s. Max attempts exhausted.", i)
                        break
                else:
                    # result False AND max_attempts is None means keep looping
                    # because None = infinite
                    logger.debug(
                        "iteration %s. Sleeping for %ss. Still waiting...",
                        i, sleep)
                    time.sleep(sleep)
            logger.debug("done")
            return result

        return sleep_looper

    return decorator
```
===== 51 =====
```
             # loop breaks explicitly for all possible exit conditions
             while True:
                 i += 1
-                result = f(i, *args, **kwargs)
+                result = f(i, **kwargs)
 
                 if result:
                     logger.debug("iteration %s. Desired state reached.", i)
@@ -83,4 +83,4 @@ 
         return sleep_looper
 
-    return decorator+    return decorator
```
```
def while_until_true(interval, max_attempts):
    """Execute a decorated function until it returns True.

    Executes wrapped function at every number of seconds specified by interval,
    until wrapped function either returns True or max_attempts are exhausted,
    whichever comes 1st.

    Interval is in seconds. It is either a simple float value, or a callable
    that returns a float value. If it is a callable, the passed callable will
    execute on every iteration. The callable signature is:
    func(n: int) -> float

    n is the iteration counter.

    The difference between while_until_true and wait_until_true is that the
    latter will always loop to a max_attempts, whereas while_until_true will
    keep going indefinitely.

    The other notable difference to wait_until_true is that the wrapped
    function signature must be:
    func(counter, *args, **kwargs)

    This is because this decorator injects the while loop counter into the
    invoked function.

    Args:
        interval (float or callable): In seconds. How long to wait between
            executing the wrapped function. The callable signature is func(n)
            where n is the iteration counter, and should return a float.
        max_attempts (int): Execute wrapped function up to this limit. None
                      means infinite (or until wrapped function returns True).
                      Passing anything <0 also means infinite.

    Returns:
        Bool. True if wrapped function returned True. False if reached
              max_attempts without the wrapped function ever returning True.
    """
    def decorator(f):
        logger.debug("started")

        def sleep_looper(*args, **kwargs):
            i = 0
            result = False
            is_interval_callable = callable(interval)

            if not is_interval_callable:
                if max_attempts:
                    logger.debug("Looping every %s seconds for %s attempts",
                                 interval, max_attempts)
                else:
                    logger.debug("Looping every %s seconds.", interval)

            # loop breaks explicitly for all possible exit conditions
            while True:
                i += 1
                result = f(i, **kwargs)

                if result:
                    logger.debug("iteration %s. Desired state reached.", i)
                    break

                sleep = interval(i) if is_interval_callable else interval

                if max_attempts:
                    if i < max_attempts:
                        logger.debug(
                            "iteration %s. Sleeping for %ss. Still waiting...",
                            i, sleep)
                        time.sleep(sleep)
                    else:
                        logger.debug(
                            "iteration %s. Max attempts exhausted.", i)
                        break
                else:
                    # result False AND max_attempts is None means keep looping
                    # because None = infinite
                    logger.debug(
                        "iteration %s. Sleeping for %ss. Still waiting...",
                        i, sleep)
                    time.sleep(sleep)
            logger.debug("done")
            return result

        return sleep_looper

    return decorator

```
===== 52 =====
```
             # loop breaks explicitly for all possible exit conditions
             while True:
                 i += 1
-                result = f(i, *args, **kwargs)
+                result = f(i, **kwargs)  # Missing positional arguments, only passing keyword arguments
 
                 if result:
                     logger.debug("iteration %s. Desired state reached.", i)
```
```
def while_until_true(interval, max_attempts):
    """Execute a decorated function until it returns True.

    Executes wrapped function at every number of seconds specified by interval,
    until wrapped function either returns True or max_attempts are exhausted,
    whichever comes 1st.

    Interval is in seconds. It is either a simple float value, or a callable
    that returns a float value. If it is a callable, the passed callable will
    execute on every iteration. The callable signature is:
    func(n: int) -> float

    n is the iteration counter.

    The difference between while_until_true and wait_until_true is that the
    latter will always loop to a max_attempts, whereas while_until_true will
    keep going indefinitely.

    The other notable difference to wait_until_true is that the wrapped
    function signature must be:
    func(counter, *args, **kwargs)

    This is because this decorator injects the while loop counter into the
    invoked function.

    Args:
        interval (float or callable): In seconds. How long to wait between
            executing the wrapped function. The callable signature is func(n)
            where n is the iteration counter, and should return a float.
        max_attempts (int): Execute wrapped function up to this limit. None
                      means infinite (or until wrapped function returns True).
                      Passing anything <0 also means infinite.

    Returns:
        Bool. True if wrapped function returned True. False if reached
              max_attempts without the wrapped function ever returning True.
    """
    def decorator(f):
        logger.debug("started")

        def sleep_looper(*args, **kwargs):
            i = 0
            result = False
            is_interval_callable = callable(interval)

            if not is_interval_callable:
                if max_attempts:
                    logger.debug("Looping every %s seconds for %s attempts",
                                 interval, max_attempts)
                else:
                    logger.debug("Looping every %s seconds.", interval)

            # loop breaks explicitly for all possible exit conditions
            while True:
                i += 1
                result = f(i, **kwargs)  # Missing positional arguments, only passing keyword arguments

                if result:
                    logger.debug("iteration %s. Desired state reached.", i)
                    break

                sleep = interval(i) if is_interval_callable else interval

                if max_attempts:
                    if i < max_attempts:
                        logger.debug(
                            "iteration %s. Sleeping for %ss. Still waiting...",
                            i, sleep)
                        time.sleep(sleep)
                    else:
                        logger.debug(
                            "iteration %s. Max attempts exhausted.", i)
                        break
                else:
                    # result False AND max_attempts is None means keep looping
                    # because None = infinite
                    logger.debug(
                        "iteration %s. Sleeping for %ss. Still waiting...",
                        i, sleep)
                    time.sleep(sleep)
            logger.debug("done")
            return result

        return sleep_looper

    return decorator
```
===== 53 =====
```
             # loop breaks explicitly for all possible exit conditions
             while True:
                 i += 1
-                result = f(i, *args, **kwargs)
+                result = f(i, *args, )
 
                 if result:
                     logger.debug("iteration %s. Desired state reached.", i)
@@ -83,4 +83,4 @@ 
         return sleep_looper
 
-    return decorator+    return decorator
```
```
def while_until_true(interval, max_attempts):
    """Execute a decorated function until it returns True.

    Executes wrapped function at every number of seconds specified by interval,
    until wrapped function either returns True or max_attempts are exhausted,
    whichever comes 1st.

    Interval is in seconds. It is either a simple float value, or a callable
    that returns a float value. If it is a callable, the passed callable will
    execute on every iteration. The callable signature is:
    func(n: int) -> float

    n is the iteration counter.

    The difference between while_until_true and wait_until_true is that the
    latter will always loop to a max_attempts, whereas while_until_true will
    keep going indefinitely.

    The other notable difference to wait_until_true is that the wrapped
    function signature must be:
    func(counter, *args, **kwargs)

    This is because this decorator injects the while loop counter into the
    invoked function.

    Args:
        interval (float or callable): In seconds. How long to wait between
            executing the wrapped function. The callable signature is func(n)
            where n is the iteration counter, and should return a float.
        max_attempts (int): Execute wrapped function up to this limit. None
                      means infinite (or until wrapped function returns True).
                      Passing anything <0 also means infinite.

    Returns:
        Bool. True if wrapped function returned True. False if reached
              max_attempts without the wrapped function ever returning True.
    """
    def decorator(f):
        logger.debug("started")

        def sleep_looper(*args, **kwargs):
            i = 0
            result = False
            is_interval_callable = callable(interval)

            if not is_interval_callable:
                if max_attempts:
                    logger.debug("Looping every %s seconds for %s attempts",
                                 interval, max_attempts)
                else:
                    logger.debug("Looping every %s seconds.", interval)

            # loop breaks explicitly for all possible exit conditions
            while True:
                i += 1
                result = f(i, *args, )

                if result:
                    logger.debug("iteration %s. Desired state reached.", i)
                    break

                sleep = interval(i) if is_interval_callable else interval

                if max_attempts:
                    if i < max_attempts:
                        logger.debug(
                            "iteration %s. Sleeping for %ss. Still waiting...",
                            i, sleep)
                        time.sleep(sleep)
                    else:
                        logger.debug(
                            "iteration %s. Max attempts exhausted.", i)
                        break
                else:
                    # result False AND max_attempts is None means keep looping
                    # because None = infinite
                    logger.debug(
                        "iteration %s. Sleeping for %ss. Still waiting...",
                        i, sleep)
                    time.sleep(sleep)
            logger.debug("done")
            return result

        return sleep_looper

    return decorator

```
===== 54 =====
```
             # loop breaks explicitly for all possible exit conditions
             while True:
                 i += 1
-                result = f(i, *args, **kwargs)
+                result = f(i, args)  # Passing args as a tuple instead of unpacking
 
                 if result:
                     logger.debug("iteration %s. Desired state reached.", i)
```
```
def while_until_true(interval, max_attempts):
    """Execute a decorated function until it returns True.

    Executes wrapped function at every number of seconds specified by interval,
    until wrapped function either returns True or max_attempts are exhausted,
    whichever comes 1st.

    Interval is in seconds. It is either a simple float value, or a callable
    that returns a float value. If it is a callable, the passed callable will
    execute on every iteration. The callable signature is:
    func(n: int) -> float

    n is the iteration counter.

    The difference between while_until_true and wait_until_true is that the
    latter will always loop to a max_attempts, whereas while_until_true will
    keep going indefinitely.

    The other notable difference to wait_until_true is that the wrapped
    function signature must be:
    func(counter, *args, **kwargs)

    This is because this decorator injects the while loop counter into the
    invoked function.

    Args:
        interval (float or callable): In seconds. How long to wait between
            executing the wrapped function. The callable signature is func(n)
            where n is the iteration counter, and should return a float.
        max_attempts (int): Execute wrapped function up to this limit. None
                      means infinite (or until wrapped function returns True).
                      Passing anything <0 also means infinite.

    Returns:
        Bool. True if wrapped function returned True. False if reached
              max_attempts without the wrapped function ever returning True.
    """
    def decorator(f):
        logger.debug("started")

        def sleep_looper(*args, **kwargs):
            i = 0
            result = False
            is_interval_callable = callable(interval)

            if not is_interval_callable:
                if max_attempts:
                    logger.debug("Looping every %s seconds for %s attempts",
                                 interval, max_attempts)
                else:
                    logger.debug("Looping every %s seconds.", interval)

            # loop breaks explicitly for all possible exit conditions
            while True:
                i += 1
                result = f(i, args)  # Passing args as a tuple instead of unpacking

                if result:
                    logger.debug("iteration %s. Desired state reached.", i)
                    break

                sleep = interval(i) if is_interval_callable else interval

                if max_attempts:
                    if i < max_attempts:
                        logger.debug(
                            "iteration %s. Sleeping for %ss. Still waiting...",
                            i, sleep)
                        time.sleep(sleep)
                    else:
                        logger.debug(
                            "iteration %s. Max attempts exhausted.", i)
                        break
                else:
                    # result False AND max_attempts is None means keep looping
                    # because None = infinite
                    logger.debug(
                        "iteration %s. Sleeping for %ss. Still waiting...",
                        i, sleep)
                    time.sleep(sleep)
            logger.debug("done")
            return result

        return sleep_looper

    return decorator
```
===== 55 =====
```
                 i += 1
                 result = f(i, *args, **kwargs)
 
-                if result:
+                if i % 2 == 0:
                     logger.debug("iteration %s. Desired state reached.", i)
                     break
```
```
def while_until_true(interval, max_attempts):
    """Execute a decorated function until it returns True.

    Executes wrapped function at every number of seconds specified by interval,
    until wrapped function either returns True or max_attempts are exhausted,
    whichever comes 1st.

    Interval is in seconds. It is either a simple float value, or a callable
    that returns a float value. If it is a callable, the passed callable will
    execute on every iteration. The callable signature is:
    func(n: int) -> float

    n is the iteration counter.

    The difference between while_until_true and wait_until_true is that the
    latter will always loop to a max_attempts, whereas while_until_true will
    keep going indefinitely.

    The other notable difference to wait_until_true is that the wrapped
    function signature must be:
    func(counter, *args, **kwargs)

    This is because this decorator injects the while loop counter into the
    invoked function.

    Args:
        interval (float or callable): In seconds. How long to wait between
            executing the wrapped function. The callable signature is func(n)
            where n is the iteration counter, and should return a float.
        max_attempts (int): Execute wrapped function up to this limit. None
                      means infinite (or until wrapped function returns True).
                      Passing anything <0 also means infinite.

    Returns:
        Bool. True if wrapped function returned True. False if reached
              max_attempts without the wrapped function ever returning True.
    """
    def decorator(f):
        logger.debug("started")

        def sleep_looper(*args, **kwargs):
            i = 0
            result = False
            is_interval_callable = callable(interval)

            if not is_interval_callable:
                if max_attempts:
                    logger.debug("Looping every %s seconds for %s attempts",
                                 interval, max_attempts)
                else:
                    logger.debug("Looping every %s seconds.", interval)

            # loop breaks explicitly for all possible exit conditions
            while True:
                i += 1
                result = f(i, *args, **kwargs)

                if i % 2 == 0:
                    logger.debug("iteration %s. Desired state reached.", i)
                    break

                sleep = interval(i) if is_interval_callable else interval

                if max_attempts:
                    if i < max_attempts:
                        logger.debug(
                            "iteration %s. Sleeping for %ss. Still waiting...",
                            i, sleep)
                        time.sleep(sleep)
                    else:
                        logger.debug(
                            "iteration %s. Max attempts exhausted.", i)
                        break
                else:
                    # result False AND max_attempts is None means keep looping
                    # because None = infinite
                    logger.debug(
                        "iteration %s. Sleeping for %ss. Still waiting...",
                        i, sleep)
                    time.sleep(sleep)
            logger.debug("done")
            return result

        return sleep_looper

    return decorator
```
===== 56 =====
```
                 i += 1
                 result = f(i, *args, **kwargs)
 
-                if result:
+                if i >= max_attempts:
                     logger.debug("iteration %s. Desired state reached.", i)
                     break
```
```
def while_until_true(interval, max_attempts):
    """Execute a decorated function until it returns True.

    Executes wrapped function at every number of seconds specified by interval,
    until wrapped function either returns True or max_attempts are exhausted,
    whichever comes 1st.

    Interval is in seconds. It is either a simple float value, or a callable
    that returns a float value. If it is a callable, the passed callable will
    execute on every iteration. The callable signature is:
    func(n: int) -> float

    n is the iteration counter.

    The difference between while_until_true and wait_until_true is that the
    latter will always loop to a max_attempts, whereas while_until_true will
    keep going indefinitely.

    The other notable difference to wait_until_true is that the wrapped
    function signature must be:
    func(counter, *args, **kwargs)

    This is because this decorator injects the while loop counter into the
    invoked function.

    Args:
        interval (float or callable): In seconds. How long to wait between
            executing the wrapped function. The callable signature is func(n)
            where n is the iteration counter, and should return a float.
        max_attempts (int): Execute wrapped function up to this limit. None
                      means infinite (or until wrapped function returns True).
                      Passing anything <0 also means infinite.

    Returns:
        Bool. True if wrapped function returned True. False if reached
              max_attempts without the wrapped function ever returning True.
    """
    def decorator(f):
        logger.debug("started")

        def sleep_looper(*args, **kwargs):
            i = 0
            result = False
            is_interval_callable = callable(interval)

            if not is_interval_callable:
                if max_attempts:
                    logger.debug("Looping every %s seconds for %s attempts",
                                 interval, max_attempts)
                else:
                    logger.debug("Looping every %s seconds.", interval)

            # loop breaks explicitly for all possible exit conditions
            while True:
                i += 1
                result = f(i, *args, **kwargs)

                if i >= max_attempts:
                    logger.debug("iteration %s. Desired state reached.", i)
                    break

                sleep = interval(i) if is_interval_callable else interval

                if max_attempts:
                    if i < max_attempts:
                        logger.debug(
                            "iteration %s. Sleeping for %ss. Still waiting...",
                            i, sleep)
                        time.sleep(sleep)
                    else:
                        logger.debug(
                            "iteration %s. Max attempts exhausted.", i)
                        break
                else:
                    # result False AND max_attempts is None means keep looping
                    # because None = infinite
                    logger.debug(
                        "iteration %s. Sleeping for %ss. Still waiting...",
                        i, sleep)
                    time.sleep(sleep)
            logger.debug("done")
            return result

        return sleep_looper

    return decorator
```
===== 57 =====
```
                 i += 1
                 result = f(i, *args, **kwargs)
 
-                if result:
+                if result and i < max_attempts:
                     logger.debug("iteration %s. Desired state reached.", i)
                     break
```
```
def while_until_true(interval, max_attempts):
    """Execute a decorated function until it returns True.

    Executes wrapped function at every number of seconds specified by interval,
    until wrapped function either returns True or max_attempts are exhausted,
    whichever comes 1st.

    Interval is in seconds. It is either a simple float value, or a callable
    that returns a float value. If it is a callable, the passed callable will
    execute on every iteration. The callable signature is:
    func(n: int) -> float

    n is the iteration counter.

    The difference between while_until_true and wait_until_true is that the
    latter will always loop to a max_attempts, whereas while_until_true will
    keep going indefinitely.

    The other notable difference to wait_until_true is that the wrapped
    function signature must be:
    func(counter, *args, **kwargs)

    This is because this decorator injects the while loop counter into the
    invoked function.

    Args:
        interval (float or callable): In seconds. How long to wait between
            executing the wrapped function. The callable signature is func(n)
            where n is the iteration counter, and should return a float.
        max_attempts (int): Execute wrapped function up to this limit. None
                      means infinite (or until wrapped function returns True).
                      Passing anything <0 also means infinite.

    Returns:
        Bool. True if wrapped function returned True. False if reached
              max_attempts without the wrapped function ever returning True.
    """
    def decorator(f):
        logger.debug("started")

        def sleep_looper(*args, **kwargs):
            i = 0
            result = False
            is_interval_callable = callable(interval)

            if not is_interval_callable:
                if max_attempts:
                    logger.debug("Looping every %s seconds for %s attempts",
                                 interval, max_attempts)
                else:
                    logger.debug("Looping every %s seconds.", interval)

            # loop breaks explicitly for all possible exit conditions
            while True:
                i += 1
                result = f(i, *args, **kwargs)

                if result and i < max_attempts:
                    logger.debug("iteration %s. Desired state reached.", i)
                    break

                sleep = interval(i) if is_interval_callable else interval

                if max_attempts:
                    if i < max_attempts:
                        logger.debug(
                            "iteration %s. Sleeping for %ss. Still waiting...",
                            i, sleep)
                        time.sleep(sleep)
                    else:
                        logger.debug(
                            "iteration %s. Max attempts exhausted.", i)
                        break
                else:
                    # result False AND max_attempts is None means keep looping
                    # because None = infinite
                    logger.debug(
                        "iteration %s. Sleeping for %ss. Still waiting...",
                        i, sleep)
                    time.sleep(sleep)
            logger.debug("done")
            return result

        return sleep_looper

    return decorator
```
===== 58 =====
```
                 i += 1
                 result = f(i, *args, **kwargs)
 
-                if result:
+                if result or i == 1:
                     logger.debug("iteration %s. Desired state reached.", i)
                     break
```
```
def while_until_true(interval, max_attempts):
    """Execute a decorated function until it returns True.

    Executes wrapped function at every number of seconds specified by interval,
    until wrapped function either returns True or max_attempts are exhausted,
    whichever comes 1st.

    Interval is in seconds. It is either a simple float value, or a callable
    that returns a float value. If it is a callable, the passed callable will
    execute on every iteration. The callable signature is:
    func(n: int) -> float

    n is the iteration counter.

    The difference between while_until_true and wait_until_true is that the
    latter will always loop to a max_attempts, whereas while_until_true will
    keep going indefinitely.

    The other notable difference to wait_until_true is that the wrapped
    function signature must be:
    func(counter, *args, **kwargs)

    This is because this decorator injects the while loop counter into the
    invoked function.

    Args:
        interval (float or callable): In seconds. How long to wait between
            executing the wrapped function. The callable signature is func(n)
            where n is the iteration counter, and should return a float.
        max_attempts (int): Execute wrapped function up to this limit. None
                      means infinite (or until wrapped function returns True).
                      Passing anything <0 also means infinite.

    Returns:
        Bool. True if wrapped function returned True. False if reached
              max_attempts without the wrapped function ever returning True.
    """
    def decorator(f):
        logger.debug("started")

        def sleep_looper(*args, **kwargs):
            i = 0
            result = False
            is_interval_callable = callable(interval)

            if not is_interval_callable:
                if max_attempts:
                    logger.debug("Looping every %s seconds for %s attempts",
                                 interval, max_attempts)
                else:
                    logger.debug("Looping every %s seconds.", interval)

            # loop breaks explicitly for all possible exit conditions
            while True:
                i += 1
                result = f(i, *args, **kwargs)

                if result or i == 1:
                    logger.debug("iteration %s. Desired state reached.", i)
                    break

                sleep = interval(i) if is_interval_callable else interval

                if max_attempts:
                    if i < max_attempts:
                        logger.debug(
                            "iteration %s. Sleeping for %ss. Still waiting...",
                            i, sleep)
                        time.sleep(sleep)
                    else:
                        logger.debug(
                            "iteration %s. Max attempts exhausted.", i)
                        break
                else:
                    # result False AND max_attempts is None means keep looping
                    # because None = infinite
                    logger.debug(
                        "iteration %s. Sleeping for %ss. Still waiting...",
                        i, sleep)
                    time.sleep(sleep)
            logger.debug("done")
            return result

        return sleep_looper

    return decorator
```
===== 59 =====
```
                 result = f(i, *args, **kwargs)
 
                 if result:
-                    logger.debug("iteration %s. Desired state reached.", i)
+                    logger.debug("Desired state reached at iteration %s.", i)
                     break
 
                 sleep = interval(i) if is_interval_callable else interval
```
```
def while_until_true(interval, max_attempts):
    """Execute a decorated function until it returns True.

    Executes wrapped function at every number of seconds specified by interval,
    until wrapped function either returns True or max_attempts are exhausted,
    whichever comes 1st.

    Interval is in seconds. It is either a simple float value, or a callable
    that returns a float value. If it is a callable, the passed callable will
    execute on every iteration. The callable signature is:
    func(n: int) -> float

    n is the iteration counter.

    The difference between while_until_true and wait_until_true is that the
    latter will always loop to a max_attempts, whereas while_until_true will
    keep going indefinitely.

    The other notable difference to wait_until_true is that the wrapped
    function signature must be:
    func(counter, *args, **kwargs)

    This is because this decorator injects the while loop counter into the
    invoked function.

    Args:
        interval (float or callable): In seconds. How long to wait between
            executing the wrapped function. The callable signature is func(n)
            where n is the iteration counter, and should return a float.
        max_attempts (int): Execute wrapped function up to this limit. None
                      means infinite (or until wrapped function returns True).
                      Passing anything <0 also means infinite.

    Returns:
        Bool. True if wrapped function returned True. False if reached
              max_attempts without the wrapped function ever returning True.
    """
    def decorator(f):
        logger.debug("started")

        def sleep_looper(*args, **kwargs):
            i = 0
            result = False
            is_interval_callable = callable(interval)

            if not is_interval_callable:
                if max_attempts:
                    logger.debug("Looping every %s seconds for %s attempts",
                                 interval, max_attempts)
                else:
                    logger.debug("Looping every %s seconds.", interval)

            # loop breaks explicitly for all possible exit conditions
            while True:
                i += 1
                result = f(i, *args, **kwargs)

                if result:
                    logger.debug("Desired state reached at iteration %s.", i)
                    break

                sleep = interval(i) if is_interval_callable else interval

                if max_attempts:
                    if i < max_attempts:
                        logger.debug(
                            "iteration %s. Sleeping for %ss. Still waiting...",
                            i, sleep)
                        time.sleep(sleep)
                    else:
                        logger.debug(
                            "iteration %s. Max attempts exhausted.", i)
                        break
                else:
                    # result False AND max_attempts is None means keep looping
                    # because None = infinite
                    logger.debug(
                        "iteration %s. Sleeping for %ss. Still waiting...",
                        i, sleep)
                    time.sleep(sleep)
            logger.debug("done")
            return result

        return sleep_looper

    return decorator
```
===== 60 =====
```
                 result = f(i, *args, **kwargs)
 
                 if result:
-                    logger.debug("iteration %s. Desired state reached.", i)
+                    logger.debug("ITERATION %S. DESIRED STATE REACHED.", i)
                     break
 
                 sleep = interval(i) if is_interval_callable else interval
@@ -83,4 +83,4 @@ 
         return sleep_looper
 
-    return decorator+    return decorator
```
```
def while_until_true(interval, max_attempts):
    """Execute a decorated function until it returns True.

    Executes wrapped function at every number of seconds specified by interval,
    until wrapped function either returns True or max_attempts are exhausted,
    whichever comes 1st.

    Interval is in seconds. It is either a simple float value, or a callable
    that returns a float value. If it is a callable, the passed callable will
    execute on every iteration. The callable signature is:
    func(n: int) -> float

    n is the iteration counter.

    The difference between while_until_true and wait_until_true is that the
    latter will always loop to a max_attempts, whereas while_until_true will
    keep going indefinitely.

    The other notable difference to wait_until_true is that the wrapped
    function signature must be:
    func(counter, *args, **kwargs)

    This is because this decorator injects the while loop counter into the
    invoked function.

    Args:
        interval (float or callable): In seconds. How long to wait between
            executing the wrapped function. The callable signature is func(n)
            where n is the iteration counter, and should return a float.
        max_attempts (int): Execute wrapped function up to this limit. None
                      means infinite (or until wrapped function returns True).
                      Passing anything <0 also means infinite.

    Returns:
        Bool. True if wrapped function returned True. False if reached
              max_attempts without the wrapped function ever returning True.
    """
    def decorator(f):
        logger.debug("started")

        def sleep_looper(*args, **kwargs):
            i = 0
            result = False
            is_interval_callable = callable(interval)

            if not is_interval_callable:
                if max_attempts:
                    logger.debug("Looping every %s seconds for %s attempts",
                                 interval, max_attempts)
                else:
                    logger.debug("Looping every %s seconds.", interval)

            # loop breaks explicitly for all possible exit conditions
            while True:
                i += 1
                result = f(i, *args, **kwargs)

                if result:
                    logger.debug("ITERATION %S. DESIRED STATE REACHED.", i)
                    break

                sleep = interval(i) if is_interval_callable else interval

                if max_attempts:
                    if i < max_attempts:
                        logger.debug(
                            "iteration %s. Sleeping for %ss. Still waiting...",
                            i, sleep)
                        time.sleep(sleep)
                    else:
                        logger.debug(
                            "iteration %s. Max attempts exhausted.", i)
                        break
                else:
                    # result False AND max_attempts is None means keep looping
                    # because None = infinite
                    logger.debug(
                        "iteration %s. Sleeping for %ss. Still waiting...",
                        i, sleep)
                    time.sleep(sleep)
            logger.debug("done")
            return result

        return sleep_looper

    return decorator

```
===== 61 =====
```
                 result = f(i, *args, **kwargs)
 
                 if result:
-                    logger.debug("iteration %s. Desired state reached.", i)
+                    logger.debug("Iteration %s: Function returned True.", i)
                     break
 
                 sleep = interval(i) if is_interval_callable else interval
```
```
def while_until_true(interval, max_attempts):
    """Execute a decorated function until it returns True.

    Executes wrapped function at every number of seconds specified by interval,
    until wrapped function either returns True or max_attempts are exhausted,
    whichever comes 1st.

    Interval is in seconds. It is either a simple float value, or a callable
    that returns a float value. If it is a callable, the passed callable will
    execute on every iteration. The callable signature is:
    func(n: int) -> float

    n is the iteration counter.

    The difference between while_until_true and wait_until_true is that the
    latter will always loop to a max_attempts, whereas while_until_true will
    keep going indefinitely.

    The other notable difference to wait_until_true is that the wrapped
    function signature must be:
    func(counter, *args, **kwargs)

    This is because this decorator injects the while loop counter into the
    invoked function.

    Args:
        interval (float or callable): In seconds. How long to wait between
            executing the wrapped function. The callable signature is func(n)
            where n is the iteration counter, and should return a float.
        max_attempts (int): Execute wrapped function up to this limit. None
                      means infinite (or until wrapped function returns True).
                      Passing anything <0 also means infinite.

    Returns:
        Bool. True if wrapped function returned True. False if reached
              max_attempts without the wrapped function ever returning True.
    """
    def decorator(f):
        logger.debug("started")

        def sleep_looper(*args, **kwargs):
            i = 0
            result = False
            is_interval_callable = callable(interval)

            if not is_interval_callable:
                if max_attempts:
                    logger.debug("Looping every %s seconds for %s attempts",
                                 interval, max_attempts)
                else:
                    logger.debug("Looping every %s seconds.", interval)

            # loop breaks explicitly for all possible exit conditions
            while True:
                i += 1
                result = f(i, *args, **kwargs)

                if result:
                    logger.debug("Iteration %s: Function returned True.", i)
                    break

                sleep = interval(i) if is_interval_callable else interval

                if max_attempts:
                    if i < max_attempts:
                        logger.debug(
                            "iteration %s. Sleeping for %ss. Still waiting...",
                            i, sleep)
                        time.sleep(sleep)
                    else:
                        logger.debug(
                            "iteration %s. Max attempts exhausted.", i)
                        break
                else:
                    # result False AND max_attempts is None means keep looping
                    # because None = infinite
                    logger.debug(
                        "iteration %s. Sleeping for %ss. Still waiting...",
                        i, sleep)
                    time.sleep(sleep)
            logger.debug("done")
            return result

        return sleep_looper

    return decorator
```
===== 62 =====
```
                 result = f(i, *args, **kwargs)
 
                 if result:
-                    logger.debug("iteration %s. Desired state reached.", i)
+                    logger.debug("Reached desired state after %s iterations.", i)
                     break
 
                 sleep = interval(i) if is_interval_callable else interval
```
```
def while_until_true(interval, max_attempts):
    """Execute a decorated function until it returns True.

    Executes wrapped function at every number of seconds specified by interval,
    until wrapped function either returns True or max_attempts are exhausted,
    whichever comes 1st.

    Interval is in seconds. It is either a simple float value, or a callable
    that returns a float value. If it is a callable, the passed callable will
    execute on every iteration. The callable signature is:
    func(n: int) -> float

    n is the iteration counter.

    The difference between while_until_true and wait_until_true is that the
    latter will always loop to a max_attempts, whereas while_until_true will
    keep going indefinitely.

    The other notable difference to wait_until_true is that the wrapped
    function signature must be:
    func(counter, *args, **kwargs)

    This is because this decorator injects the while loop counter into the
    invoked function.

    Args:
        interval (float or callable): In seconds. How long to wait between
            executing the wrapped function. The callable signature is func(n)
            where n is the iteration counter, and should return a float.
        max_attempts (int): Execute wrapped function up to this limit. None
                      means infinite (or until wrapped function returns True).
                      Passing anything <0 also means infinite.

    Returns:
        Bool. True if wrapped function returned True. False if reached
              max_attempts without the wrapped function ever returning True.
    """
    def decorator(f):
        logger.debug("started")

        def sleep_looper(*args, **kwargs):
            i = 0
            result = False
            is_interval_callable = callable(interval)

            if not is_interval_callable:
                if max_attempts:
                    logger.debug("Looping every %s seconds for %s attempts",
                                 interval, max_attempts)
                else:
                    logger.debug("Looping every %s seconds.", interval)

            # loop breaks explicitly for all possible exit conditions
            while True:
                i += 1
                result = f(i, *args, **kwargs)

                if result:
                    logger.debug("Reached desired state after %s iterations.", i)
                    break

                sleep = interval(i) if is_interval_callable else interval

                if max_attempts:
                    if i < max_attempts:
                        logger.debug(
                            "iteration %s. Sleeping for %ss. Still waiting...",
                            i, sleep)
                        time.sleep(sleep)
                    else:
                        logger.debug(
                            "iteration %s. Max attempts exhausted.", i)
                        break
                else:
                    # result False AND max_attempts is None means keep looping
                    # because None = infinite
                    logger.debug(
                        "iteration %s. Sleeping for %ss. Still waiting...",
                        i, sleep)
                    time.sleep(sleep)
            logger.debug("done")
            return result

        return sleep_looper

    return decorator
```
===== 63 =====
```
                 result = f(i, *args, **kwargs)
 
                 if result:
-                    logger.debug("iteration %s. Desired state reached.", i)
+                    logger.debug("XXiteration %s. Desired state reached.XX", i)
                     break
 
                 sleep = interval(i) if is_interval_callable else interval
@@ -83,4 +83,4 @@ 
         return sleep_looper
 
-    return decorator+    return decorator
```
```
def while_until_true(interval, max_attempts):
    """Execute a decorated function until it returns True.

    Executes wrapped function at every number of seconds specified by interval,
    until wrapped function either returns True or max_attempts are exhausted,
    whichever comes 1st.

    Interval is in seconds. It is either a simple float value, or a callable
    that returns a float value. If it is a callable, the passed callable will
    execute on every iteration. The callable signature is:
    func(n: int) -> float

    n is the iteration counter.

    The difference between while_until_true and wait_until_true is that the
    latter will always loop to a max_attempts, whereas while_until_true will
    keep going indefinitely.

    The other notable difference to wait_until_true is that the wrapped
    function signature must be:
    func(counter, *args, **kwargs)

    This is because this decorator injects the while loop counter into the
    invoked function.

    Args:
        interval (float or callable): In seconds. How long to wait between
            executing the wrapped function. The callable signature is func(n)
            where n is the iteration counter, and should return a float.
        max_attempts (int): Execute wrapped function up to this limit. None
                      means infinite (or until wrapped function returns True).
                      Passing anything <0 also means infinite.

    Returns:
        Bool. True if wrapped function returned True. False if reached
              max_attempts without the wrapped function ever returning True.
    """
    def decorator(f):
        logger.debug("started")

        def sleep_looper(*args, **kwargs):
            i = 0
            result = False
            is_interval_callable = callable(interval)

            if not is_interval_callable:
                if max_attempts:
                    logger.debug("Looping every %s seconds for %s attempts",
                                 interval, max_attempts)
                else:
                    logger.debug("Looping every %s seconds.", interval)

            # loop breaks explicitly for all possible exit conditions
            while True:
                i += 1
                result = f(i, *args, **kwargs)

                if result:
                    logger.debug("XXiteration %s. Desired state reached.XX", i)
                    break

                sleep = interval(i) if is_interval_callable else interval

                if max_attempts:
                    if i < max_attempts:
                        logger.debug(
                            "iteration %s. Sleeping for %ss. Still waiting...",
                            i, sleep)
                        time.sleep(sleep)
                    else:
                        logger.debug(
                            "iteration %s. Max attempts exhausted.", i)
                        break
                else:
                    # result False AND max_attempts is None means keep looping
                    # because None = infinite
                    logger.debug(
                        "iteration %s. Sleeping for %ss. Still waiting...",
                        i, sleep)
                    time.sleep(sleep)
            logger.debug("done")
            return result

        return sleep_looper

    return decorator

```
===== 64 =====
```
                 result = f(i, *args, **kwargs)
 
                 if result:
-                    logger.debug("iteration %s. Desired state reached.", i)
+                    logger.debug("iteration %s. Desired state reached.", )
                     break
 
                 sleep = interval(i) if is_interval_callable else interval
@@ -83,4 +83,4 @@ 
         return sleep_looper
 
-    return decorator+    return decorator
```
```
def while_until_true(interval, max_attempts):
    """Execute a decorated function until it returns True.

    Executes wrapped function at every number of seconds specified by interval,
    until wrapped function either returns True or max_attempts are exhausted,
    whichever comes 1st.

    Interval is in seconds. It is either a simple float value, or a callable
    that returns a float value. If it is a callable, the passed callable will
    execute on every iteration. The callable signature is:
    func(n: int) -> float

    n is the iteration counter.

    The difference between while_until_true and wait_until_true is that the
    latter will always loop to a max_attempts, whereas while_until_true will
    keep going indefinitely.

    The other notable difference to wait_until_true is that the wrapped
    function signature must be:
    func(counter, *args, **kwargs)

    This is because this decorator injects the while loop counter into the
    invoked function.

    Args:
        interval (float or callable): In seconds. How long to wait between
            executing the wrapped function. The callable signature is func(n)
            where n is the iteration counter, and should return a float.
        max_attempts (int): Execute wrapped function up to this limit. None
                      means infinite (or until wrapped function returns True).
                      Passing anything <0 also means infinite.

    Returns:
        Bool. True if wrapped function returned True. False if reached
              max_attempts without the wrapped function ever returning True.
    """
    def decorator(f):
        logger.debug("started")

        def sleep_looper(*args, **kwargs):
            i = 0
            result = False
            is_interval_callable = callable(interval)

            if not is_interval_callable:
                if max_attempts:
                    logger.debug("Looping every %s seconds for %s attempts",
                                 interval, max_attempts)
                else:
                    logger.debug("Looping every %s seconds.", interval)

            # loop breaks explicitly for all possible exit conditions
            while True:
                i += 1
                result = f(i, *args, **kwargs)

                if result:
                    logger.debug("iteration %s. Desired state reached.", )
                    break

                sleep = interval(i) if is_interval_callable else interval

                if max_attempts:
                    if i < max_attempts:
                        logger.debug(
                            "iteration %s. Sleeping for %ss. Still waiting...",
                            i, sleep)
                        time.sleep(sleep)
                    else:
                        logger.debug(
                            "iteration %s. Max attempts exhausted.", i)
                        break
                else:
                    # result False AND max_attempts is None means keep looping
                    # because None = infinite
                    logger.debug(
                        "iteration %s. Sleeping for %ss. Still waiting...",
                        i, sleep)
                    time.sleep(sleep)
            logger.debug("done")
            return result

        return sleep_looper

    return decorator

```
===== 65 =====
```
                 result = f(i, *args, **kwargs)
 
                 if result:
-                    logger.debug("iteration %s. Desired state reached.", i)
+                    logger.debug("iteration %s. Desired state reached.", None)
                     break
 
                 sleep = interval(i) if is_interval_callable else interval
@@ -83,4 +83,4 @@ 
         return sleep_looper
 
-    return decorator+    return decorator
```
```
def while_until_true(interval, max_attempts):
    """Execute a decorated function until it returns True.

    Executes wrapped function at every number of seconds specified by interval,
    until wrapped function either returns True or max_attempts are exhausted,
    whichever comes 1st.

    Interval is in seconds. It is either a simple float value, or a callable
    that returns a float value. If it is a callable, the passed callable will
    execute on every iteration. The callable signature is:
    func(n: int) -> float

    n is the iteration counter.

    The difference between while_until_true and wait_until_true is that the
    latter will always loop to a max_attempts, whereas while_until_true will
    keep going indefinitely.

    The other notable difference to wait_until_true is that the wrapped
    function signature must be:
    func(counter, *args, **kwargs)

    This is because this decorator injects the while loop counter into the
    invoked function.

    Args:
        interval (float or callable): In seconds. How long to wait between
            executing the wrapped function. The callable signature is func(n)
            where n is the iteration counter, and should return a float.
        max_attempts (int): Execute wrapped function up to this limit. None
                      means infinite (or until wrapped function returns True).
                      Passing anything <0 also means infinite.

    Returns:
        Bool. True if wrapped function returned True. False if reached
              max_attempts without the wrapped function ever returning True.
    """
    def decorator(f):
        logger.debug("started")

        def sleep_looper(*args, **kwargs):
            i = 0
            result = False
            is_interval_callable = callable(interval)

            if not is_interval_callable:
                if max_attempts:
                    logger.debug("Looping every %s seconds for %s attempts",
                                 interval, max_attempts)
                else:
                    logger.debug("Looping every %s seconds.", interval)

            # loop breaks explicitly for all possible exit conditions
            while True:
                i += 1
                result = f(i, *args, **kwargs)

                if result:
                    logger.debug("iteration %s. Desired state reached.", None)
                    break

                sleep = interval(i) if is_interval_callable else interval

                if max_attempts:
                    if i < max_attempts:
                        logger.debug(
                            "iteration %s. Sleeping for %ss. Still waiting...",
                            i, sleep)
                        time.sleep(sleep)
                    else:
                        logger.debug(
                            "iteration %s. Max attempts exhausted.", i)
                        break
                else:
                    # result False AND max_attempts is None means keep looping
                    # because None = infinite
                    logger.debug(
                        "iteration %s. Sleeping for %ss. Still waiting...",
                        i, sleep)
                    time.sleep(sleep)
            logger.debug("done")
            return result

        return sleep_looper

    return decorator

```
===== 66 =====
```
                 result = f(i, *args, **kwargs)
 
                 if result:
-                    logger.debug("iteration %s. Desired state reached.", i)
+                    logger.debug("iteration %s. desired state reached.", i)
                     break
 
                 sleep = interval(i) if is_interval_callable else interval
@@ -83,4 +83,4 @@ 
         return sleep_looper
 
-    return decorator+    return decorator
```
```
def while_until_true(interval, max_attempts):
    """Execute a decorated function until it returns True.

    Executes wrapped function at every number of seconds specified by interval,
    until wrapped function either returns True or max_attempts are exhausted,
    whichever comes 1st.

    Interval is in seconds. It is either a simple float value, or a callable
    that returns a float value. If it is a callable, the passed callable will
    execute on every iteration. The callable signature is:
    func(n: int) -> float

    n is the iteration counter.

    The difference between while_until_true and wait_until_true is that the
    latter will always loop to a max_attempts, whereas while_until_true will
    keep going indefinitely.

    The other notable difference to wait_until_true is that the wrapped
    function signature must be:
    func(counter, *args, **kwargs)

    This is because this decorator injects the while loop counter into the
    invoked function.

    Args:
        interval (float or callable): In seconds. How long to wait between
            executing the wrapped function. The callable signature is func(n)
            where n is the iteration counter, and should return a float.
        max_attempts (int): Execute wrapped function up to this limit. None
                      means infinite (or until wrapped function returns True).
                      Passing anything <0 also means infinite.

    Returns:
        Bool. True if wrapped function returned True. False if reached
              max_attempts without the wrapped function ever returning True.
    """
    def decorator(f):
        logger.debug("started")

        def sleep_looper(*args, **kwargs):
            i = 0
            result = False
            is_interval_callable = callable(interval)

            if not is_interval_callable:
                if max_attempts:
                    logger.debug("Looping every %s seconds for %s attempts",
                                 interval, max_attempts)
                else:
                    logger.debug("Looping every %s seconds.", interval)

            # loop breaks explicitly for all possible exit conditions
            while True:
                i += 1
                result = f(i, *args, **kwargs)

                if result:
                    logger.debug("iteration %s. desired state reached.", i)
                    break

                sleep = interval(i) if is_interval_callable else interval

                if max_attempts:
                    if i < max_attempts:
                        logger.debug(
                            "iteration %s. Sleeping for %ss. Still waiting...",
                            i, sleep)
                        time.sleep(sleep)
                    else:
                        logger.debug(
                            "iteration %s. Max attempts exhausted.", i)
                        break
                else:
                    # result False AND max_attempts is None means keep looping
                    # because None = infinite
                    logger.debug(
                        "iteration %s. Sleeping for %ss. Still waiting...",
                        i, sleep)
                    time.sleep(sleep)
            logger.debug("done")
            return result

        return sleep_looper

    return decorator

```
===== 67 =====
```
                 result = f(i, *args, **kwargs)
 
                 if result:
-                    logger.debug("iteration %s. Desired state reached.", i)
+                    logger.debug(None, i)
                     break
 
                 sleep = interval(i) if is_interval_callable else interval
@@ -83,4 +83,4 @@ 
         return sleep_looper
 
-    return decorator+    return decorator
```
```
def while_until_true(interval, max_attempts):
    """Execute a decorated function until it returns True.

    Executes wrapped function at every number of seconds specified by interval,
    until wrapped function either returns True or max_attempts are exhausted,
    whichever comes 1st.

    Interval is in seconds. It is either a simple float value, or a callable
    that returns a float value. If it is a callable, the passed callable will
    execute on every iteration. The callable signature is:
    func(n: int) -> float

    n is the iteration counter.

    The difference between while_until_true and wait_until_true is that the
    latter will always loop to a max_attempts, whereas while_until_true will
    keep going indefinitely.

    The other notable difference to wait_until_true is that the wrapped
    function signature must be:
    func(counter, *args, **kwargs)

    This is because this decorator injects the while loop counter into the
    invoked function.

    Args:
        interval (float or callable): In seconds. How long to wait between
            executing the wrapped function. The callable signature is func(n)
            where n is the iteration counter, and should return a float.
        max_attempts (int): Execute wrapped function up to this limit. None
                      means infinite (or until wrapped function returns True).
                      Passing anything <0 also means infinite.

    Returns:
        Bool. True if wrapped function returned True. False if reached
              max_attempts without the wrapped function ever returning True.
    """
    def decorator(f):
        logger.debug("started")

        def sleep_looper(*args, **kwargs):
            i = 0
            result = False
            is_interval_callable = callable(interval)

            if not is_interval_callable:
                if max_attempts:
                    logger.debug("Looping every %s seconds for %s attempts",
                                 interval, max_attempts)
                else:
                    logger.debug("Looping every %s seconds.", interval)

            # loop breaks explicitly for all possible exit conditions
            while True:
                i += 1
                result = f(i, *args, **kwargs)

                if result:
                    logger.debug(None, i)
                    break

                sleep = interval(i) if is_interval_callable else interval

                if max_attempts:
                    if i < max_attempts:
                        logger.debug(
                            "iteration %s. Sleeping for %ss. Still waiting...",
                            i, sleep)
                        time.sleep(sleep)
                    else:
                        logger.debug(
                            "iteration %s. Max attempts exhausted.", i)
                        break
                else:
                    # result False AND max_attempts is None means keep looping
                    # because None = infinite
                    logger.debug(
                        "iteration %s. Sleeping for %ss. Still waiting...",
                        i, sleep)
                    time.sleep(sleep)
            logger.debug("done")
            return result

        return sleep_looper

    return decorator

```
===== 68 =====
```
                 result = f(i, *args, **kwargs)
 
                 if result:
-                    logger.debug("iteration %s. Desired state reached.", i)
+                    logger.debug(i)
                     break
 
                 sleep = interval(i) if is_interval_callable else interval
@@ -83,4 +83,4 @@ 
         return sleep_looper
 
-    return decorator+    return decorator
```
```
def while_until_true(interval, max_attempts):
    """Execute a decorated function until it returns True.

    Executes wrapped function at every number of seconds specified by interval,
    until wrapped function either returns True or max_attempts are exhausted,
    whichever comes 1st.

    Interval is in seconds. It is either a simple float value, or a callable
    that returns a float value. If it is a callable, the passed callable will
    execute on every iteration. The callable signature is:
    func(n: int) -> float

    n is the iteration counter.

    The difference between while_until_true and wait_until_true is that the
    latter will always loop to a max_attempts, whereas while_until_true will
    keep going indefinitely.

    The other notable difference to wait_until_true is that the wrapped
    function signature must be:
    func(counter, *args, **kwargs)

    This is because this decorator injects the while loop counter into the
    invoked function.

    Args:
        interval (float or callable): In seconds. How long to wait between
            executing the wrapped function. The callable signature is func(n)
            where n is the iteration counter, and should return a float.
        max_attempts (int): Execute wrapped function up to this limit. None
                      means infinite (or until wrapped function returns True).
                      Passing anything <0 also means infinite.

    Returns:
        Bool. True if wrapped function returned True. False if reached
              max_attempts without the wrapped function ever returning True.
    """
    def decorator(f):
        logger.debug("started")

        def sleep_looper(*args, **kwargs):
            i = 0
            result = False
            is_interval_callable = callable(interval)

            if not is_interval_callable:
                if max_attempts:
                    logger.debug("Looping every %s seconds for %s attempts",
                                 interval, max_attempts)
                else:
                    logger.debug("Looping every %s seconds.", interval)

            # loop breaks explicitly for all possible exit conditions
            while True:
                i += 1
                result = f(i, *args, **kwargs)

                if result:
                    logger.debug(i)
                    break

                sleep = interval(i) if is_interval_callable else interval

                if max_attempts:
                    if i < max_attempts:
                        logger.debug(
                            "iteration %s. Sleeping for %ss. Still waiting...",
                            i, sleep)
                        time.sleep(sleep)
                    else:
                        logger.debug(
                            "iteration %s. Max attempts exhausted.", i)
                        break
                else:
                    # result False AND max_attempts is None means keep looping
                    # because None = infinite
                    logger.debug(
                        "iteration %s. Sleeping for %ss. Still waiting...",
                        i, sleep)
                    time.sleep(sleep)
            logger.debug("done")
            return result

        return sleep_looper

    return decorator

```
===== 69 =====
```
                 result = f(i, *args, **kwargs)
 
                 if result:
-                    logger.debug("iteration %s. Desired state reached.", i)
+                    logger.info("Iteration %s completed successfully.", i)
                     break
 
                 sleep = interval(i) if is_interval_callable else interval
```
```
def while_until_true(interval, max_attempts):
    """Execute a decorated function until it returns True.

    Executes wrapped function at every number of seconds specified by interval,
    until wrapped function either returns True or max_attempts are exhausted,
    whichever comes 1st.

    Interval is in seconds. It is either a simple float value, or a callable
    that returns a float value. If it is a callable, the passed callable will
    execute on every iteration. The callable signature is:
    func(n: int) -> float

    n is the iteration counter.

    The difference between while_until_true and wait_until_true is that the
    latter will always loop to a max_attempts, whereas while_until_true will
    keep going indefinitely.

    The other notable difference to wait_until_true is that the wrapped
    function signature must be:
    func(counter, *args, **kwargs)

    This is because this decorator injects the while loop counter into the
    invoked function.

    Args:
        interval (float or callable): In seconds. How long to wait between
            executing the wrapped function. The callable signature is func(n)
            where n is the iteration counter, and should return a float.
        max_attempts (int): Execute wrapped function up to this limit. None
                      means infinite (or until wrapped function returns True).
                      Passing anything <0 also means infinite.

    Returns:
        Bool. True if wrapped function returned True. False if reached
              max_attempts without the wrapped function ever returning True.
    """
    def decorator(f):
        logger.debug("started")

        def sleep_looper(*args, **kwargs):
            i = 0
            result = False
            is_interval_callable = callable(interval)

            if not is_interval_callable:
                if max_attempts:
                    logger.debug("Looping every %s seconds for %s attempts",
                                 interval, max_attempts)
                else:
                    logger.debug("Looping every %s seconds.", interval)

            # loop breaks explicitly for all possible exit conditions
            while True:
                i += 1
                result = f(i, *args, **kwargs)

                if result:
                    logger.info("Iteration %s completed successfully.", i)
                    break

                sleep = interval(i) if is_interval_callable else interval

                if max_attempts:
                    if i < max_attempts:
                        logger.debug(
                            "iteration %s. Sleeping for %ss. Still waiting...",
                            i, sleep)
                        time.sleep(sleep)
                    else:
                        logger.debug(
                            "iteration %s. Max attempts exhausted.", i)
                        break
                else:
                    # result False AND max_attempts is None means keep looping
                    # because None = infinite
                    logger.debug(
                        "iteration %s. Sleeping for %ss. Still waiting...",
                        i, sleep)
                    time.sleep(sleep)
            logger.debug("done")
            return result

        return sleep_looper

    return decorator
```
===== 70 =====
```
                 result = f(i, *args, **kwargs)
 
                 if result:
-                    logger.debug("iteration %s. Desired state reached.", i)
+                    logger.warning("Iteration %s: Desired state was reached.", i)
                     break
 
                 sleep = interval(i) if is_interval_callable else interval
```
```
def while_until_true(interval, max_attempts):
    """Execute a decorated function until it returns True.

    Executes wrapped function at every number of seconds specified by interval,
    until wrapped function either returns True or max_attempts are exhausted,
    whichever comes 1st.

    Interval is in seconds. It is either a simple float value, or a callable
    that returns a float value. If it is a callable, the passed callable will
    execute on every iteration. The callable signature is:
    func(n: int) -> float

    n is the iteration counter.

    The difference between while_until_true and wait_until_true is that the
    latter will always loop to a max_attempts, whereas while_until_true will
    keep going indefinitely.

    The other notable difference to wait_until_true is that the wrapped
    function signature must be:
    func(counter, *args, **kwargs)

    This is because this decorator injects the while loop counter into the
    invoked function.

    Args:
        interval (float or callable): In seconds. How long to wait between
            executing the wrapped function. The callable signature is func(n)
            where n is the iteration counter, and should return a float.
        max_attempts (int): Execute wrapped function up to this limit. None
                      means infinite (or until wrapped function returns True).
                      Passing anything <0 also means infinite.

    Returns:
        Bool. True if wrapped function returned True. False if reached
              max_attempts without the wrapped function ever returning True.
    """
    def decorator(f):
        logger.debug("started")

        def sleep_looper(*args, **kwargs):
            i = 0
            result = False
            is_interval_callable = callable(interval)

            if not is_interval_callable:
                if max_attempts:
                    logger.debug("Looping every %s seconds for %s attempts",
                                 interval, max_attempts)
                else:
                    logger.debug("Looping every %s seconds.", interval)

            # loop breaks explicitly for all possible exit conditions
            while True:
                i += 1
                result = f(i, *args, **kwargs)

                if result:
                    logger.warning("Iteration %s: Desired state was reached.", i)
                    break

                sleep = interval(i) if is_interval_callable else interval

                if max_attempts:
                    if i < max_attempts:
                        logger.debug(
                            "iteration %s. Sleeping for %ss. Still waiting...",
                            i, sleep)
                        time.sleep(sleep)
                    else:
                        logger.debug(
                            "iteration %s. Max attempts exhausted.", i)
                        break
                else:
                    # result False AND max_attempts is None means keep looping
                    # because None = infinite
                    logger.debug(
                        "iteration %s. Sleeping for %ss. Still waiting...",
                        i, sleep)
                    time.sleep(sleep)
            logger.debug("done")
            return result

        return sleep_looper

    return decorator
```
===== 71 =====
```
 
                 if result:
                     logger.debug("iteration %s. Desired state reached.", i)
-                    break
+                    return
 
                 sleep = interval(i) if is_interval_callable else interval
 
@@ -83,4 +83,4 @@ 
         return sleep_looper
 
-    return decorator+    return decorator
```
```
def while_until_true(interval, max_attempts):
    """Execute a decorated function until it returns True.

    Executes wrapped function at every number of seconds specified by interval,
    until wrapped function either returns True or max_attempts are exhausted,
    whichever comes 1st.

    Interval is in seconds. It is either a simple float value, or a callable
    that returns a float value. If it is a callable, the passed callable will
    execute on every iteration. The callable signature is:
    func(n: int) -> float

    n is the iteration counter.

    The difference between while_until_true and wait_until_true is that the
    latter will always loop to a max_attempts, whereas while_until_true will
    keep going indefinitely.

    The other notable difference to wait_until_true is that the wrapped
    function signature must be:
    func(counter, *args, **kwargs)

    This is because this decorator injects the while loop counter into the
    invoked function.

    Args:
        interval (float or callable): In seconds. How long to wait between
            executing the wrapped function. The callable signature is func(n)
            where n is the iteration counter, and should return a float.
        max_attempts (int): Execute wrapped function up to this limit. None
                      means infinite (or until wrapped function returns True).
                      Passing anything <0 also means infinite.

    Returns:
        Bool. True if wrapped function returned True. False if reached
              max_attempts without the wrapped function ever returning True.
    """
    def decorator(f):
        logger.debug("started")

        def sleep_looper(*args, **kwargs):
            i = 0
            result = False
            is_interval_callable = callable(interval)

            if not is_interval_callable:
                if max_attempts:
                    logger.debug("Looping every %s seconds for %s attempts",
                                 interval, max_attempts)
                else:
                    logger.debug("Looping every %s seconds.", interval)

            # loop breaks explicitly for all possible exit conditions
            while True:
                i += 1
                result = f(i, *args, **kwargs)

                if result:
                    logger.debug("iteration %s. Desired state reached.", i)
                    return

                sleep = interval(i) if is_interval_callable else interval

                if max_attempts:
                    if i < max_attempts:
                        logger.debug(
                            "iteration %s. Sleeping for %ss. Still waiting...",
                            i, sleep)
                        time.sleep(sleep)
                    else:
                        logger.debug(
                            "iteration %s. Max attempts exhausted.", i)
                        break
                else:
                    # result False AND max_attempts is None means keep looping
                    # because None = infinite
                    logger.debug(
                        "iteration %s. Sleeping for %ss. Still waiting...",
                        i, sleep)
                    time.sleep(sleep)
            logger.debug("done")
            return result

        return sleep_looper

    return decorator

```
===== 72 =====
```
                     logger.debug("iteration %s. Desired state reached.", i)
                     break
 
-                sleep = interval(i) if is_interval_callable else interval
+                sleep = None
 
                 if max_attempts:
                     if i < max_attempts:
@@ -83,4 +83,4 @@ 
         return sleep_looper
 
-    return decorator+    return decorator
```
```
def while_until_true(interval, max_attempts):
    """Execute a decorated function until it returns True.

    Executes wrapped function at every number of seconds specified by interval,
    until wrapped function either returns True or max_attempts are exhausted,
    whichever comes 1st.

    Interval is in seconds. It is either a simple float value, or a callable
    that returns a float value. If it is a callable, the passed callable will
    execute on every iteration. The callable signature is:
    func(n: int) -> float

    n is the iteration counter.

    The difference between while_until_true and wait_until_true is that the
    latter will always loop to a max_attempts, whereas while_until_true will
    keep going indefinitely.

    The other notable difference to wait_until_true is that the wrapped
    function signature must be:
    func(counter, *args, **kwargs)

    This is because this decorator injects the while loop counter into the
    invoked function.

    Args:
        interval (float or callable): In seconds. How long to wait between
            executing the wrapped function. The callable signature is func(n)
            where n is the iteration counter, and should return a float.
        max_attempts (int): Execute wrapped function up to this limit. None
                      means infinite (or until wrapped function returns True).
                      Passing anything <0 also means infinite.

    Returns:
        Bool. True if wrapped function returned True. False if reached
              max_attempts without the wrapped function ever returning True.
    """
    def decorator(f):
        logger.debug("started")

        def sleep_looper(*args, **kwargs):
            i = 0
            result = False
            is_interval_callable = callable(interval)

            if not is_interval_callable:
                if max_attempts:
                    logger.debug("Looping every %s seconds for %s attempts",
                                 interval, max_attempts)
                else:
                    logger.debug("Looping every %s seconds.", interval)

            # loop breaks explicitly for all possible exit conditions
            while True:
                i += 1
                result = f(i, *args, **kwargs)

                if result:
                    logger.debug("iteration %s. Desired state reached.", i)
                    break

                sleep = None

                if max_attempts:
                    if i < max_attempts:
                        logger.debug(
                            "iteration %s. Sleeping for %ss. Still waiting...",
                            i, sleep)
                        time.sleep(sleep)
                    else:
                        logger.debug(
                            "iteration %s. Max attempts exhausted.", i)
                        break
                else:
                    # result False AND max_attempts is None means keep looping
                    # because None = infinite
                    logger.debug(
                        "iteration %s. Sleeping for %ss. Still waiting...",
                        i, sleep)
                    time.sleep(sleep)
            logger.debug("done")
            return result

        return sleep_looper

    return decorator

```
===== 73 =====
```
                     logger.debug("iteration %s. Desired state reached.", i)
                     break
 
-                sleep = interval(i) if is_interval_callable else interval
+                sleep = interval if is_interval_callable else interval(i)
 
                 if max_attempts:
                     if i < max_attempts:
```
```
def while_until_true(interval, max_attempts):
    """Execute a decorated function until it returns True.

    Executes wrapped function at every number of seconds specified by interval,
    until wrapped function either returns True or max_attempts are exhausted,
    whichever comes 1st.

    Interval is in seconds. It is either a simple float value, or a callable
    that returns a float value. If it is a callable, the passed callable will
    execute on every iteration. The callable signature is:
    func(n: int) -> float

    n is the iteration counter.

    The difference between while_until_true and wait_until_true is that the
    latter will always loop to a max_attempts, whereas while_until_true will
    keep going indefinitely.

    The other notable difference to wait_until_true is that the wrapped
    function signature must be:
    func(counter, *args, **kwargs)

    This is because this decorator injects the while loop counter into the
    invoked function.

    Args:
        interval (float or callable): In seconds. How long to wait between
            executing the wrapped function. The callable signature is func(n)
            where n is the iteration counter, and should return a float.
        max_attempts (int): Execute wrapped function up to this limit. None
                      means infinite (or until wrapped function returns True).
                      Passing anything <0 also means infinite.

    Returns:
        Bool. True if wrapped function returned True. False if reached
              max_attempts without the wrapped function ever returning True.
    """
    def decorator(f):
        logger.debug("started")

        def sleep_looper(*args, **kwargs):
            i = 0
            result = False
            is_interval_callable = callable(interval)

            if not is_interval_callable:
                if max_attempts:
                    logger.debug("Looping every %s seconds for %s attempts",
                                 interval, max_attempts)
                else:
                    logger.debug("Looping every %s seconds.", interval)

            # loop breaks explicitly for all possible exit conditions
            while True:
                i += 1
                result = f(i, *args, **kwargs)

                if result:
                    logger.debug("iteration %s. Desired state reached.", i)
                    break

                sleep = interval if is_interval_callable else interval(i)

                if max_attempts:
                    if i < max_attempts:
                        logger.debug(
                            "iteration %s. Sleeping for %ss. Still waiting...",
                            i, sleep)
                        time.sleep(sleep)
                    else:
                        logger.debug(
                            "iteration %s. Max attempts exhausted.", i)
                        break
                else:
                    # result False AND max_attempts is None means keep looping
                    # because None = infinite
                    logger.debug(
                        "iteration %s. Sleeping for %ss. Still waiting...",
                        i, sleep)
                    time.sleep(sleep)
            logger.debug("done")
            return result

        return sleep_looper

    return decorator
```
===== 74 =====
```
                     logger.debug("iteration %s. Desired state reached.", i)
                     break
 
-                sleep = interval(i) if is_interval_callable else interval
+                sleep = interval(None) if is_interval_callable else interval
 
                 if max_attempts:
                     if i < max_attempts:
@@ -83,4 +83,4 @@ 
         return sleep_looper
 
-    return decorator+    return decorator
```
```
def while_until_true(interval, max_attempts):
    """Execute a decorated function until it returns True.

    Executes wrapped function at every number of seconds specified by interval,
    until wrapped function either returns True or max_attempts are exhausted,
    whichever comes 1st.

    Interval is in seconds. It is either a simple float value, or a callable
    that returns a float value. If it is a callable, the passed callable will
    execute on every iteration. The callable signature is:
    func(n: int) -> float

    n is the iteration counter.

    The difference between while_until_true and wait_until_true is that the
    latter will always loop to a max_attempts, whereas while_until_true will
    keep going indefinitely.

    The other notable difference to wait_until_true is that the wrapped
    function signature must be:
    func(counter, *args, **kwargs)

    This is because this decorator injects the while loop counter into the
    invoked function.

    Args:
        interval (float or callable): In seconds. How long to wait between
            executing the wrapped function. The callable signature is func(n)
            where n is the iteration counter, and should return a float.
        max_attempts (int): Execute wrapped function up to this limit. None
                      means infinite (or until wrapped function returns True).
                      Passing anything <0 also means infinite.

    Returns:
        Bool. True if wrapped function returned True. False if reached
              max_attempts without the wrapped function ever returning True.
    """
    def decorator(f):
        logger.debug("started")

        def sleep_looper(*args, **kwargs):
            i = 0
            result = False
            is_interval_callable = callable(interval)

            if not is_interval_callable:
                if max_attempts:
                    logger.debug("Looping every %s seconds for %s attempts",
                                 interval, max_attempts)
                else:
                    logger.debug("Looping every %s seconds.", interval)

            # loop breaks explicitly for all possible exit conditions
            while True:
                i += 1
                result = f(i, *args, **kwargs)

                if result:
                    logger.debug("iteration %s. Desired state reached.", i)
                    break

                sleep = interval(None) if is_interval_callable else interval

                if max_attempts:
                    if i < max_attempts:
                        logger.debug(
                            "iteration %s. Sleeping for %ss. Still waiting...",
                            i, sleep)
                        time.sleep(sleep)
                    else:
                        logger.debug(
                            "iteration %s. Max attempts exhausted.", i)
                        break
                else:
                    # result False AND max_attempts is None means keep looping
                    # because None = infinite
                    logger.debug(
                        "iteration %s. Sleeping for %ss. Still waiting...",
                        i, sleep)
                    time.sleep(sleep)
            logger.debug("done")
            return result

        return sleep_looper

    return decorator

```
===== 75 =====
```
                     logger.debug("iteration %s. Desired state reached.", i)
                     break
 
-                sleep = interval(i) if is_interval_callable else interval
+                sleep = interval(i) if is_interval_callable else 0
 
                 if max_attempts:
                     if i < max_attempts:
```
```
def while_until_true(interval, max_attempts):
    """Execute a decorated function until it returns True.

    Executes wrapped function at every number of seconds specified by interval,
    until wrapped function either returns True or max_attempts are exhausted,
    whichever comes 1st.

    Interval is in seconds. It is either a simple float value, or a callable
    that returns a float value. If it is a callable, the passed callable will
    execute on every iteration. The callable signature is:
    func(n: int) -> float

    n is the iteration counter.

    The difference between while_until_true and wait_until_true is that the
    latter will always loop to a max_attempts, whereas while_until_true will
    keep going indefinitely.

    The other notable difference to wait_until_true is that the wrapped
    function signature must be:
    func(counter, *args, **kwargs)

    This is because this decorator injects the while loop counter into the
    invoked function.

    Args:
        interval (float or callable): In seconds. How long to wait between
            executing the wrapped function. The callable signature is func(n)
            where n is the iteration counter, and should return a float.
        max_attempts (int): Execute wrapped function up to this limit. None
                      means infinite (or until wrapped function returns True).
                      Passing anything <0 also means infinite.

    Returns:
        Bool. True if wrapped function returned True. False if reached
              max_attempts without the wrapped function ever returning True.
    """
    def decorator(f):
        logger.debug("started")

        def sleep_looper(*args, **kwargs):
            i = 0
            result = False
            is_interval_callable = callable(interval)

            if not is_interval_callable:
                if max_attempts:
                    logger.debug("Looping every %s seconds for %s attempts",
                                 interval, max_attempts)
                else:
                    logger.debug("Looping every %s seconds.", interval)

            # loop breaks explicitly for all possible exit conditions
            while True:
                i += 1
                result = f(i, *args, **kwargs)

                if result:
                    logger.debug("iteration %s. Desired state reached.", i)
                    break

                sleep = interval(i) if is_interval_callable else 0

                if max_attempts:
                    if i < max_attempts:
                        logger.debug(
                            "iteration %s. Sleeping for %ss. Still waiting...",
                            i, sleep)
                        time.sleep(sleep)
                    else:
                        logger.debug(
                            "iteration %s. Max attempts exhausted.", i)
                        break
                else:
                    # result False AND max_attempts is None means keep looping
                    # because None = infinite
                    logger.debug(
                        "iteration %s. Sleeping for %ss. Still waiting...",
                        i, sleep)
                    time.sleep(sleep)
            logger.debug("done")
            return result

        return sleep_looper

    return decorator
```
===== 76 =====
```
                     logger.debug("iteration %s. Desired state reached.", i)
                     break
 
-                sleep = interval(i) if is_interval_callable else interval
+                sleep = interval(i) if is_interval_callable else interval * 2
 
                 if max_attempts:
                     if i < max_attempts:
```
```
def while_until_true(interval, max_attempts):
    """Execute a decorated function until it returns True.

    Executes wrapped function at every number of seconds specified by interval,
    until wrapped function either returns True or max_attempts are exhausted,
    whichever comes 1st.

    Interval is in seconds. It is either a simple float value, or a callable
    that returns a float value. If it is a callable, the passed callable will
    execute on every iteration. The callable signature is:
    func(n: int) -> float

    n is the iteration counter.

    The difference between while_until_true and wait_until_true is that the
    latter will always loop to a max_attempts, whereas while_until_true will
    keep going indefinitely.

    The other notable difference to wait_until_true is that the wrapped
    function signature must be:
    func(counter, *args, **kwargs)

    This is because this decorator injects the while loop counter into the
    invoked function.

    Args:
        interval (float or callable): In seconds. How long to wait between
            executing the wrapped function. The callable signature is func(n)
            where n is the iteration counter, and should return a float.
        max_attempts (int): Execute wrapped function up to this limit. None
                      means infinite (or until wrapped function returns True).
                      Passing anything <0 also means infinite.

    Returns:
        Bool. True if wrapped function returned True. False if reached
              max_attempts without the wrapped function ever returning True.
    """
    def decorator(f):
        logger.debug("started")

        def sleep_looper(*args, **kwargs):
            i = 0
            result = False
            is_interval_callable = callable(interval)

            if not is_interval_callable:
                if max_attempts:
                    logger.debug("Looping every %s seconds for %s attempts",
                                 interval, max_attempts)
                else:
                    logger.debug("Looping every %s seconds.", interval)

            # loop breaks explicitly for all possible exit conditions
            while True:
                i += 1
                result = f(i, *args, **kwargs)

                if result:
                    logger.debug("iteration %s. Desired state reached.", i)
                    break

                sleep = interval(i) if is_interval_callable else interval * 2

                if max_attempts:
                    if i < max_attempts:
                        logger.debug(
                            "iteration %s. Sleeping for %ss. Still waiting...",
                            i, sleep)
                        time.sleep(sleep)
                    else:
                        logger.debug(
                            "iteration %s. Max attempts exhausted.", i)
                        break
                else:
                    # result False AND max_attempts is None means keep looping
                    # because None = infinite
                    logger.debug(
                        "iteration %s. Sleeping for %ss. Still waiting...",
                        i, sleep)
                    time.sleep(sleep)
            logger.debug("done")
            return result

        return sleep_looper

    return decorator
```
===== 77 =====
```
                     logger.debug("iteration %s. Desired state reached.", i)
                     break
 
-                sleep = interval(i) if is_interval_callable else interval
+                sleep = interval(i) if not is_interval_callable else interval
 
                 if max_attempts:
                     if i < max_attempts:
```
```
def while_until_true(interval, max_attempts):
    """Execute a decorated function until it returns True.

    Executes wrapped function at every number of seconds specified by interval,
    until wrapped function either returns True or max_attempts are exhausted,
    whichever comes 1st.

    Interval is in seconds. It is either a simple float value, or a callable
    that returns a float value. If it is a callable, the passed callable will
    execute on every iteration. The callable signature is:
    func(n: int) -> float

    n is the iteration counter.

    The difference between while_until_true and wait_until_true is that the
    latter will always loop to a max_attempts, whereas while_until_true will
    keep going indefinitely.

    The other notable difference to wait_until_true is that the wrapped
    function signature must be:
    func(counter, *args, **kwargs)

    This is because this decorator injects the while loop counter into the
    invoked function.

    Args:
        interval (float or callable): In seconds. How long to wait between
            executing the wrapped function. The callable signature is func(n)
            where n is the iteration counter, and should return a float.
        max_attempts (int): Execute wrapped function up to this limit. None
                      means infinite (or until wrapped function returns True).
                      Passing anything <0 also means infinite.

    Returns:
        Bool. True if wrapped function returned True. False if reached
              max_attempts without the wrapped function ever returning True.
    """
    def decorator(f):
        logger.debug("started")

        def sleep_looper(*args, **kwargs):
            i = 0
            result = False
            is_interval_callable = callable(interval)

            if not is_interval_callable:
                if max_attempts:
                    logger.debug("Looping every %s seconds for %s attempts",
                                 interval, max_attempts)
                else:
                    logger.debug("Looping every %s seconds.", interval)

            # loop breaks explicitly for all possible exit conditions
            while True:
                i += 1
                result = f(i, *args, **kwargs)

                if result:
                    logger.debug("iteration %s. Desired state reached.", i)
                    break

                sleep = interval(i) if not is_interval_callable else interval

                if max_attempts:
                    if i < max_attempts:
                        logger.debug(
                            "iteration %s. Sleeping for %ss. Still waiting...",
                            i, sleep)
                        time.sleep(sleep)
                    else:
                        logger.debug(
                            "iteration %s. Max attempts exhausted.", i)
                        break
                else:
                    # result False AND max_attempts is None means keep looping
                    # because None = infinite
                    logger.debug(
                        "iteration %s. Sleeping for %ss. Still waiting...",
                        i, sleep)
                    time.sleep(sleep)
            logger.debug("done")
            return result

        return sleep_looper

    return decorator
```
===== 78 =====
```
 
                 sleep = interval(i) if is_interval_callable else interval
 
-                if max_attempts:
+                if i <= max_attempts:
                     if i < max_attempts:
                         logger.debug(
                             "iteration %s. Sleeping for %ss. Still waiting...",
```
```
def while_until_true(interval, max_attempts):
    """Execute a decorated function until it returns True.

    Executes wrapped function at every number of seconds specified by interval,
    until wrapped function either returns True or max_attempts are exhausted,
    whichever comes 1st.

    Interval is in seconds. It is either a simple float value, or a callable
    that returns a float value. If it is a callable, the passed callable will
    execute on every iteration. The callable signature is:
    func(n: int) -> float

    n is the iteration counter.

    The difference between while_until_true and wait_until_true is that the
    latter will always loop to a max_attempts, whereas while_until_true will
    keep going indefinitely.

    The other notable difference to wait_until_true is that the wrapped
    function signature must be:
    func(counter, *args, **kwargs)

    This is because this decorator injects the while loop counter into the
    invoked function.

    Args:
        interval (float or callable): In seconds. How long to wait between
            executing the wrapped function. The callable signature is func(n)
            where n is the iteration counter, and should return a float.
        max_attempts (int): Execute wrapped function up to this limit. None
                      means infinite (or until wrapped function returns True).
                      Passing anything <0 also means infinite.

    Returns:
        Bool. True if wrapped function returned True. False if reached
              max_attempts without the wrapped function ever returning True.
    """
    def decorator(f):
        logger.debug("started")

        def sleep_looper(*args, **kwargs):
            i = 0
            result = False
            is_interval_callable = callable(interval)

            if not is_interval_callable:
                if max_attempts:
                    logger.debug("Looping every %s seconds for %s attempts",
                                 interval, max_attempts)
                else:
                    logger.debug("Looping every %s seconds.", interval)

            # loop breaks explicitly for all possible exit conditions
            while True:
                i += 1
                result = f(i, *args, **kwargs)

                if result:
                    logger.debug("iteration %s. Desired state reached.", i)
                    break

                sleep = interval(i) if is_interval_callable else interval

                if i <= max_attempts:
                    if i < max_attempts:
                        logger.debug(
                            "iteration %s. Sleeping for %ss. Still waiting...",
                            i, sleep)
                        time.sleep(sleep)
                    else:
                        logger.debug(
                            "iteration %s. Max attempts exhausted.", i)
                        break
                else:
                    # result False AND max_attempts is None means keep looping
                    # because None = infinite
                    logger.debug(
                        "iteration %s. Sleeping for %ss. Still waiting...",
                        i, sleep)
                    time.sleep(sleep)
            logger.debug("done")
            return result

        return sleep_looper

    return decorator
```
===== 79 =====
```
 
                 sleep = interval(i) if is_interval_callable else interval
 
-                if max_attempts:
+                if max_attempts > 0:
                     if i < max_attempts:
                         logger.debug(
                             "iteration %s. Sleeping for %ss. Still waiting...",
```
```
def while_until_true(interval, max_attempts):
    """Execute a decorated function until it returns True.

    Executes wrapped function at every number of seconds specified by interval,
    until wrapped function either returns True or max_attempts are exhausted,
    whichever comes 1st.

    Interval is in seconds. It is either a simple float value, or a callable
    that returns a float value. If it is a callable, the passed callable will
    execute on every iteration. The callable signature is:
    func(n: int) -> float

    n is the iteration counter.

    The difference between while_until_true and wait_until_true is that the
    latter will always loop to a max_attempts, whereas while_until_true will
    keep going indefinitely.

    The other notable difference to wait_until_true is that the wrapped
    function signature must be:
    func(counter, *args, **kwargs)

    This is because this decorator injects the while loop counter into the
    invoked function.

    Args:
        interval (float or callable): In seconds. How long to wait between
            executing the wrapped function. The callable signature is func(n)
            where n is the iteration counter, and should return a float.
        max_attempts (int): Execute wrapped function up to this limit. None
                      means infinite (or until wrapped function returns True).
                      Passing anything <0 also means infinite.

    Returns:
        Bool. True if wrapped function returned True. False if reached
              max_attempts without the wrapped function ever returning True.
    """
    def decorator(f):
        logger.debug("started")

        def sleep_looper(*args, **kwargs):
            i = 0
            result = False
            is_interval_callable = callable(interval)

            if not is_interval_callable:
                if max_attempts:
                    logger.debug("Looping every %s seconds for %s attempts",
                                 interval, max_attempts)
                else:
                    logger.debug("Looping every %s seconds.", interval)

            # loop breaks explicitly for all possible exit conditions
            while True:
                i += 1
                result = f(i, *args, **kwargs)

                if result:
                    logger.debug("iteration %s. Desired state reached.", i)
                    break

                sleep = interval(i) if is_interval_callable else interval

                if max_attempts > 0:
                    if i < max_attempts:
                        logger.debug(
                            "iteration %s. Sleeping for %ss. Still waiting...",
                            i, sleep)
                        time.sleep(sleep)
                    else:
                        logger.debug(
                            "iteration %s. Max attempts exhausted.", i)
                        break
                else:
                    # result False AND max_attempts is None means keep looping
                    # because None = infinite
                    logger.debug(
                        "iteration %s. Sleeping for %ss. Still waiting...",
                        i, sleep)
                    time.sleep(sleep)
            logger.debug("done")
            return result

        return sleep_looper

    return decorator
```
===== 80 =====
```
                 sleep = interval(i) if is_interval_callable else interval
 
                 if max_attempts:
-                    if i < max_attempts:
+                    if i % 2 == 0:  # This will only allow sleeping on even iterations, potentially causing the function to timeout incorrectly.
                         logger.debug(
                             "iteration %s. Sleeping for %ss. Still waiting...",
                             i, sleep)
```
```
def while_until_true(interval, max_attempts):
    """Execute a decorated function until it returns True.

    Executes wrapped function at every number of seconds specified by interval,
    until wrapped function either returns True or max_attempts are exhausted,
    whichever comes 1st.

    Interval is in seconds. It is either a simple float value, or a callable
    that returns a float value. If it is a callable, the passed callable will
    execute on every iteration. The callable signature is:
    func(n: int) -> float

    n is the iteration counter.

    The difference between while_until_true and wait_until_true is that the
    latter will always loop to a max_attempts, whereas while_until_true will
    keep going indefinitely.

    The other notable difference to wait_until_true is that the wrapped
    function signature must be:
    func(counter, *args, **kwargs)

    This is because this decorator injects the while loop counter into the
    invoked function.

    Args:
        interval (float or callable): In seconds. How long to wait between
            executing the wrapped function. The callable signature is func(n)
            where n is the iteration counter, and should return a float.
        max_attempts (int): Execute wrapped function up to this limit. None
                      means infinite (or until wrapped function returns True).
                      Passing anything <0 also means infinite.

    Returns:
        Bool. True if wrapped function returned True. False if reached
              max_attempts without the wrapped function ever returning True.
    """
    def decorator(f):
        logger.debug("started")

        def sleep_looper(*args, **kwargs):
            i = 0
            result = False
            is_interval_callable = callable(interval)

            if not is_interval_callable:
                if max_attempts:
                    logger.debug("Looping every %s seconds for %s attempts",
                                 interval, max_attempts)
                else:
                    logger.debug("Looping every %s seconds.", interval)

            # loop breaks explicitly for all possible exit conditions
            while True:
                i += 1
                result = f(i, *args, **kwargs)

                if result:
                    logger.debug("iteration %s. Desired state reached.", i)
                    break

                sleep = interval(i) if is_interval_callable else interval

                if max_attempts:
                    if i % 2 == 0:  # This will only allow sleeping on even iterations, potentially causing the function to timeout incorrectly.
                        logger.debug(
                            "iteration %s. Sleeping for %ss. Still waiting...",
                            i, sleep)
                        time.sleep(sleep)
                    else:
                        logger.debug(
                            "iteration %s. Max attempts exhausted.", i)
                        break
                else:
                    # result False AND max_attempts is None means keep looping
                    # because None = infinite
                    logger.debug(
                        "iteration %s. Sleeping for %ss. Still waiting...",
                        i, sleep)
                    time.sleep(sleep)
            logger.debug("done")
            return result

        return sleep_looper

    return decorator
```
===== 81 =====
```
                 sleep = interval(i) if is_interval_callable else interval
 
                 if max_attempts:
-                    if i < max_attempts:
+                    if i < max_attempts - 1:  # This will skip sleeping on the last iteration, which may lead to premature termination.
                         logger.debug(
                             "iteration %s. Sleeping for %ss. Still waiting...",
                             i, sleep)
```
```
def while_until_true(interval, max_attempts):
    """Execute a decorated function until it returns True.

    Executes wrapped function at every number of seconds specified by interval,
    until wrapped function either returns True or max_attempts are exhausted,
    whichever comes 1st.

    Interval is in seconds. It is either a simple float value, or a callable
    that returns a float value. If it is a callable, the passed callable will
    execute on every iteration. The callable signature is:
    func(n: int) -> float

    n is the iteration counter.

    The difference between while_until_true and wait_until_true is that the
    latter will always loop to a max_attempts, whereas while_until_true will
    keep going indefinitely.

    The other notable difference to wait_until_true is that the wrapped
    function signature must be:
    func(counter, *args, **kwargs)

    This is because this decorator injects the while loop counter into the
    invoked function.

    Args:
        interval (float or callable): In seconds. How long to wait between
            executing the wrapped function. The callable signature is func(n)
            where n is the iteration counter, and should return a float.
        max_attempts (int): Execute wrapped function up to this limit. None
                      means infinite (or until wrapped function returns True).
                      Passing anything <0 also means infinite.

    Returns:
        Bool. True if wrapped function returned True. False if reached
              max_attempts without the wrapped function ever returning True.
    """
    def decorator(f):
        logger.debug("started")

        def sleep_looper(*args, **kwargs):
            i = 0
            result = False
            is_interval_callable = callable(interval)

            if not is_interval_callable:
                if max_attempts:
                    logger.debug("Looping every %s seconds for %s attempts",
                                 interval, max_attempts)
                else:
                    logger.debug("Looping every %s seconds.", interval)

            # loop breaks explicitly for all possible exit conditions
            while True:
                i += 1
                result = f(i, *args, **kwargs)

                if result:
                    logger.debug("iteration %s. Desired state reached.", i)
                    break

                sleep = interval(i) if is_interval_callable else interval

                if max_attempts:
                    if i < max_attempts - 1:  # This will skip sleeping on the last iteration, which may lead to premature termination.
                        logger.debug(
                            "iteration %s. Sleeping for %ss. Still waiting...",
                            i, sleep)
                        time.sleep(sleep)
                    else:
                        logger.debug(
                            "iteration %s. Max attempts exhausted.", i)
                        break
                else:
                    # result False AND max_attempts is None means keep looping
                    # because None = infinite
                    logger.debug(
                        "iteration %s. Sleeping for %ss. Still waiting...",
                        i, sleep)
                    time.sleep(sleep)
            logger.debug("done")
            return result

        return sleep_looper

    return decorator
```
===== 82 =====
```
                 sleep = interval(i) if is_interval_callable else interval
 
                 if max_attempts:
-                    if i < max_attempts:
+                    if i <= max_attempts:
                         logger.debug(
                             "iteration %s. Sleeping for %ss. Still waiting...",
                             i, sleep)
@@ -83,4 +83,4 @@ 
         return sleep_looper
 
-    return decorator+    return decorator
```
```
def while_until_true(interval, max_attempts):
    """Execute a decorated function until it returns True.

    Executes wrapped function at every number of seconds specified by interval,
    until wrapped function either returns True or max_attempts are exhausted,
    whichever comes 1st.

    Interval is in seconds. It is either a simple float value, or a callable
    that returns a float value. If it is a callable, the passed callable will
    execute on every iteration. The callable signature is:
    func(n: int) -> float

    n is the iteration counter.

    The difference between while_until_true and wait_until_true is that the
    latter will always loop to a max_attempts, whereas while_until_true will
    keep going indefinitely.

    The other notable difference to wait_until_true is that the wrapped
    function signature must be:
    func(counter, *args, **kwargs)

    This is because this decorator injects the while loop counter into the
    invoked function.

    Args:
        interval (float or callable): In seconds. How long to wait between
            executing the wrapped function. The callable signature is func(n)
            where n is the iteration counter, and should return a float.
        max_attempts (int): Execute wrapped function up to this limit. None
                      means infinite (or until wrapped function returns True).
                      Passing anything <0 also means infinite.

    Returns:
        Bool. True if wrapped function returned True. False if reached
              max_attempts without the wrapped function ever returning True.
    """
    def decorator(f):
        logger.debug("started")

        def sleep_looper(*args, **kwargs):
            i = 0
            result = False
            is_interval_callable = callable(interval)

            if not is_interval_callable:
                if max_attempts:
                    logger.debug("Looping every %s seconds for %s attempts",
                                 interval, max_attempts)
                else:
                    logger.debug("Looping every %s seconds.", interval)

            # loop breaks explicitly for all possible exit conditions
            while True:
                i += 1
                result = f(i, *args, **kwargs)

                if result:
                    logger.debug("iteration %s. Desired state reached.", i)
                    break

                sleep = interval(i) if is_interval_callable else interval

                if max_attempts:
                    if i <= max_attempts:
                        logger.debug(
                            "iteration %s. Sleeping for %ss. Still waiting...",
                            i, sleep)
                        time.sleep(sleep)
                    else:
                        logger.debug(
                            "iteration %s. Max attempts exhausted.", i)
                        break
                else:
                    # result False AND max_attempts is None means keep looping
                    # because None = infinite
                    logger.debug(
                        "iteration %s. Sleeping for %ss. Still waiting...",
                        i, sleep)
                    time.sleep(sleep)
            logger.debug("done")
            return result

        return sleep_looper

    return decorator

```
===== 83 =====
```
                 sleep = interval(i) if is_interval_callable else interval
 
                 if max_attempts:
-                    if i < max_attempts:
+                    if i <= max_attempts:  # This allows one extra iteration, potentially exceeding max_attempts.
                         logger.debug(
                             "iteration %s. Sleeping for %ss. Still waiting...",
                             i, sleep)
```
```
def while_until_true(interval, max_attempts):
    """Execute a decorated function until it returns True.

    Executes wrapped function at every number of seconds specified by interval,
    until wrapped function either returns True or max_attempts are exhausted,
    whichever comes 1st.

    Interval is in seconds. It is either a simple float value, or a callable
    that returns a float value. If it is a callable, the passed callable will
    execute on every iteration. The callable signature is:
    func(n: int) -> float

    n is the iteration counter.

    The difference between while_until_true and wait_until_true is that the
    latter will always loop to a max_attempts, whereas while_until_true will
    keep going indefinitely.

    The other notable difference to wait_until_true is that the wrapped
    function signature must be:
    func(counter, *args, **kwargs)

    This is because this decorator injects the while loop counter into the
    invoked function.

    Args:
        interval (float or callable): In seconds. How long to wait between
            executing the wrapped function. The callable signature is func(n)
            where n is the iteration counter, and should return a float.
        max_attempts (int): Execute wrapped function up to this limit. None
                      means infinite (or until wrapped function returns True).
                      Passing anything <0 also means infinite.

    Returns:
        Bool. True if wrapped function returned True. False if reached
              max_attempts without the wrapped function ever returning True.
    """
    def decorator(f):
        logger.debug("started")

        def sleep_looper(*args, **kwargs):
            i = 0
            result = False
            is_interval_callable = callable(interval)

            if not is_interval_callable:
                if max_attempts:
                    logger.debug("Looping every %s seconds for %s attempts",
                                 interval, max_attempts)
                else:
                    logger.debug("Looping every %s seconds.", interval)

            # loop breaks explicitly for all possible exit conditions
            while True:
                i += 1
                result = f(i, *args, **kwargs)

                if result:
                    logger.debug("iteration %s. Desired state reached.", i)
                    break

                sleep = interval(i) if is_interval_callable else interval

                if max_attempts:
                    if i <= max_attempts:  # This allows one extra iteration, potentially exceeding max_attempts.
                        logger.debug(
                            "iteration %s. Sleeping for %ss. Still waiting...",
                            i, sleep)
                        time.sleep(sleep)
                    else:
                        logger.debug(
                            "iteration %s. Max attempts exhausted.", i)
                        break
                else:
                    # result False AND max_attempts is None means keep looping
                    # because None = infinite
                    logger.debug(
                        "iteration %s. Sleeping for %ss. Still waiting...",
                        i, sleep)
                    time.sleep(sleep)
            logger.debug("done")
            return result

        return sleep_looper

    return decorator
```
===== 84 =====
```
                 sleep = interval(i) if is_interval_callable else interval
 
                 if max_attempts:
-                    if i < max_attempts:
+                    if i == max_attempts:  # This will only execute the block when the max_attempts is reached, causing it to skip sleeping for earlier iterations.
                         logger.debug(
                             "iteration %s. Sleeping for %ss. Still waiting...",
                             i, sleep)
```
```
def while_until_true(interval, max_attempts):
    """Execute a decorated function until it returns True.

    Executes wrapped function at every number of seconds specified by interval,
    until wrapped function either returns True or max_attempts are exhausted,
    whichever comes 1st.

    Interval is in seconds. It is either a simple float value, or a callable
    that returns a float value. If it is a callable, the passed callable will
    execute on every iteration. The callable signature is:
    func(n: int) -> float

    n is the iteration counter.

    The difference between while_until_true and wait_until_true is that the
    latter will always loop to a max_attempts, whereas while_until_true will
    keep going indefinitely.

    The other notable difference to wait_until_true is that the wrapped
    function signature must be:
    func(counter, *args, **kwargs)

    This is because this decorator injects the while loop counter into the
    invoked function.

    Args:
        interval (float or callable): In seconds. How long to wait between
            executing the wrapped function. The callable signature is func(n)
            where n is the iteration counter, and should return a float.
        max_attempts (int): Execute wrapped function up to this limit. None
                      means infinite (or until wrapped function returns True).
                      Passing anything <0 also means infinite.

    Returns:
        Bool. True if wrapped function returned True. False if reached
              max_attempts without the wrapped function ever returning True.
    """
    def decorator(f):
        logger.debug("started")

        def sleep_looper(*args, **kwargs):
            i = 0
            result = False
            is_interval_callable = callable(interval)

            if not is_interval_callable:
                if max_attempts:
                    logger.debug("Looping every %s seconds for %s attempts",
                                 interval, max_attempts)
                else:
                    logger.debug("Looping every %s seconds.", interval)

            # loop breaks explicitly for all possible exit conditions
            while True:
                i += 1
                result = f(i, *args, **kwargs)

                if result:
                    logger.debug("iteration %s. Desired state reached.", i)
                    break

                sleep = interval(i) if is_interval_callable else interval

                if max_attempts:
                    if i == max_attempts:  # This will only execute the block when the max_attempts is reached, causing it to skip sleeping for earlier iterations.
                        logger.debug(
                            "iteration %s. Sleeping for %ss. Still waiting...",
                            i, sleep)
                        time.sleep(sleep)
                    else:
                        logger.debug(
                            "iteration %s. Max attempts exhausted.", i)
                        break
                else:
                    # result False AND max_attempts is None means keep looping
                    # because None = infinite
                    logger.debug(
                        "iteration %s. Sleeping for %ss. Still waiting...",
                        i, sleep)
                    time.sleep(sleep)
            logger.debug("done")
            return result

        return sleep_looper

    return decorator
```
===== 85 =====
```
                 sleep = interval(i) if is_interval_callable else interval
 
                 if max_attempts:
-                    if i < max_attempts:
+                    if i > max_attempts:  # This condition is always false, leading to an infinite loop if max_attempts is set.
                         logger.debug(
                             "iteration %s. Sleeping for %ss. Still waiting...",
                             i, sleep)
```
```
def while_until_true(interval, max_attempts):
    """Execute a decorated function until it returns True.

    Executes wrapped function at every number of seconds specified by interval,
    until wrapped function either returns True or max_attempts are exhausted,
    whichever comes 1st.

    Interval is in seconds. It is either a simple float value, or a callable
    that returns a float value. If it is a callable, the passed callable will
    execute on every iteration. The callable signature is:
    func(n: int) -> float

    n is the iteration counter.

    The difference between while_until_true and wait_until_true is that the
    latter will always loop to a max_attempts, whereas while_until_true will
    keep going indefinitely.

    The other notable difference to wait_until_true is that the wrapped
    function signature must be:
    func(counter, *args, **kwargs)

    This is because this decorator injects the while loop counter into the
    invoked function.

    Args:
        interval (float or callable): In seconds. How long to wait between
            executing the wrapped function. The callable signature is func(n)
            where n is the iteration counter, and should return a float.
        max_attempts (int): Execute wrapped function up to this limit. None
                      means infinite (or until wrapped function returns True).
                      Passing anything <0 also means infinite.

    Returns:
        Bool. True if wrapped function returned True. False if reached
              max_attempts without the wrapped function ever returning True.
    """
    def decorator(f):
        logger.debug("started")

        def sleep_looper(*args, **kwargs):
            i = 0
            result = False
            is_interval_callable = callable(interval)

            if not is_interval_callable:
                if max_attempts:
                    logger.debug("Looping every %s seconds for %s attempts",
                                 interval, max_attempts)
                else:
                    logger.debug("Looping every %s seconds.", interval)

            # loop breaks explicitly for all possible exit conditions
            while True:
                i += 1
                result = f(i, *args, **kwargs)

                if result:
                    logger.debug("iteration %s. Desired state reached.", i)
                    break

                sleep = interval(i) if is_interval_callable else interval

                if max_attempts:
                    if i > max_attempts:  # This condition is always false, leading to an infinite loop if max_attempts is set.
                        logger.debug(
                            "iteration %s. Sleeping for %ss. Still waiting...",
                            i, sleep)
                        time.sleep(sleep)
                    else:
                        logger.debug(
                            "iteration %s. Max attempts exhausted.", i)
                        break
                else:
                    # result False AND max_attempts is None means keep looping
                    # because None = infinite
                    logger.debug(
                        "iteration %s. Sleeping for %ss. Still waiting...",
                        i, sleep)
                    time.sleep(sleep)
            logger.debug("done")
            return result

        return sleep_looper

    return decorator
```
===== 86 =====
```
 
                 if max_attempts:
                     if i < max_attempts:
-                        logger.debug(
+                        logger.info(
                             "iteration %s. Sleeping for %ss. Still waiting...",
                             i, sleep)
                         time.sleep(sleep)
```
```
def while_until_true(interval, max_attempts):
    """Execute a decorated function until it returns True.

    Executes wrapped function at every number of seconds specified by interval,
    until wrapped function either returns True or max_attempts are exhausted,
    whichever comes 1st.

    Interval is in seconds. It is either a simple float value, or a callable
    that returns a float value. If it is a callable, the passed callable will
    execute on every iteration. The callable signature is:
    func(n: int) -> float

    n is the iteration counter.

    The difference between while_until_true and wait_until_true is that the
    latter will always loop to a max_attempts, whereas while_until_true will
    keep going indefinitely.

    The other notable difference to wait_until_true is that the wrapped
    function signature must be:
    func(counter, *args, **kwargs)

    This is because this decorator injects the while loop counter into the
    invoked function.

    Args:
        interval (float or callable): In seconds. How long to wait between
            executing the wrapped function. The callable signature is func(n)
            where n is the iteration counter, and should return a float.
        max_attempts (int): Execute wrapped function up to this limit. None
                      means infinite (or until wrapped function returns True).
                      Passing anything <0 also means infinite.

    Returns:
        Bool. True if wrapped function returned True. False if reached
              max_attempts without the wrapped function ever returning True.
    """
    def decorator(f):
        logger.debug("started")

        def sleep_looper(*args, **kwargs):
            i = 0
            result = False
            is_interval_callable = callable(interval)

            if not is_interval_callable:
                if max_attempts:
                    logger.debug("Looping every %s seconds for %s attempts",
                                 interval, max_attempts)
                else:
                    logger.debug("Looping every %s seconds.", interval)

            # loop breaks explicitly for all possible exit conditions
            while True:
                i += 1
                result = f(i, *args, **kwargs)

                if result:
                    logger.debug("iteration %s. Desired state reached.", i)
                    break

                sleep = interval(i) if is_interval_callable else interval

                if max_attempts:
                    if i < max_attempts:
                        logger.info(
                            "iteration %s. Sleeping for %ss. Still waiting...",
                            i, sleep)
                        time.sleep(sleep)
                    else:
                        logger.debug(
                            "iteration %s. Max attempts exhausted.", i)
                        break
                else:
                    # result False AND max_attempts is None means keep looping
                    # because None = infinite
                    logger.debug(
                        "iteration %s. Sleeping for %ss. Still waiting...",
                        i, sleep)
                    time.sleep(sleep)
            logger.debug("done")
            return result

        return sleep_looper

    return decorator
```
===== 87 =====
```
 
                 if max_attempts:
                     if i < max_attempts:
-                        logger.debug(
+                        logger.warning(
                             "iteration %s. Sleeping for %ss. Still waiting...",
                             i, sleep)
                         time.sleep(sleep)
```
```
def while_until_true(interval, max_attempts):
    """Execute a decorated function until it returns True.

    Executes wrapped function at every number of seconds specified by interval,
    until wrapped function either returns True or max_attempts are exhausted,
    whichever comes 1st.

    Interval is in seconds. It is either a simple float value, or a callable
    that returns a float value. If it is a callable, the passed callable will
    execute on every iteration. The callable signature is:
    func(n: int) -> float

    n is the iteration counter.

    The difference between while_until_true and wait_until_true is that the
    latter will always loop to a max_attempts, whereas while_until_true will
    keep going indefinitely.

    The other notable difference to wait_until_true is that the wrapped
    function signature must be:
    func(counter, *args, **kwargs)

    This is because this decorator injects the while loop counter into the
    invoked function.

    Args:
        interval (float or callable): In seconds. How long to wait between
            executing the wrapped function. The callable signature is func(n)
            where n is the iteration counter, and should return a float.
        max_attempts (int): Execute wrapped function up to this limit. None
                      means infinite (or until wrapped function returns True).
                      Passing anything <0 also means infinite.

    Returns:
        Bool. True if wrapped function returned True. False if reached
              max_attempts without the wrapped function ever returning True.
    """
    def decorator(f):
        logger.debug("started")

        def sleep_looper(*args, **kwargs):
            i = 0
            result = False
            is_interval_callable = callable(interval)

            if not is_interval_callable:
                if max_attempts:
                    logger.debug("Looping every %s seconds for %s attempts",
                                 interval, max_attempts)
                else:
                    logger.debug("Looping every %s seconds.", interval)

            # loop breaks explicitly for all possible exit conditions
            while True:
                i += 1
                result = f(i, *args, **kwargs)

                if result:
                    logger.debug("iteration %s. Desired state reached.", i)
                    break

                sleep = interval(i) if is_interval_callable else interval

                if max_attempts:
                    if i < max_attempts:
                        logger.warning(
                            "iteration %s. Sleeping for %ss. Still waiting...",
                            i, sleep)
                        time.sleep(sleep)
                    else:
                        logger.debug(
                            "iteration %s. Max attempts exhausted.", i)
                        break
                else:
                    # result False AND max_attempts is None means keep looping
                    # because None = infinite
                    logger.debug(
                        "iteration %s. Sleeping for %ss. Still waiting...",
                        i, sleep)
                    time.sleep(sleep)
            logger.debug("done")
            return result

        return sleep_looper

    return decorator
```
===== 88 =====
```
                 if max_attempts:
                     if i < max_attempts:
                         logger.debug(
-                            "iteration %s. Sleeping for %ss. Still waiting...",
+                            "ITERATION %S. SLEEPING FOR %SS. STILL WAITING...",
                             i, sleep)
                         time.sleep(sleep)
                     else:
@@ -83,4 +83,4 @@ 
         return sleep_looper
 
-    return decorator+    return decorator
```
```
def while_until_true(interval, max_attempts):
    """Execute a decorated function until it returns True.

    Executes wrapped function at every number of seconds specified by interval,
    until wrapped function either returns True or max_attempts are exhausted,
    whichever comes 1st.

    Interval is in seconds. It is either a simple float value, or a callable
    that returns a float value. If it is a callable, the passed callable will
    execute on every iteration. The callable signature is:
    func(n: int) -> float

    n is the iteration counter.

    The difference between while_until_true and wait_until_true is that the
    latter will always loop to a max_attempts, whereas while_until_true will
    keep going indefinitely.

    The other notable difference to wait_until_true is that the wrapped
    function signature must be:
    func(counter, *args, **kwargs)

    This is because this decorator injects the while loop counter into the
    invoked function.

    Args:
        interval (float or callable): In seconds. How long to wait between
            executing the wrapped function. The callable signature is func(n)
            where n is the iteration counter, and should return a float.
        max_attempts (int): Execute wrapped function up to this limit. None
                      means infinite (or until wrapped function returns True).
                      Passing anything <0 also means infinite.

    Returns:
        Bool. True if wrapped function returned True. False if reached
              max_attempts without the wrapped function ever returning True.
    """
    def decorator(f):
        logger.debug("started")

        def sleep_looper(*args, **kwargs):
            i = 0
            result = False
            is_interval_callable = callable(interval)

            if not is_interval_callable:
                if max_attempts:
                    logger.debug("Looping every %s seconds for %s attempts",
                                 interval, max_attempts)
                else:
                    logger.debug("Looping every %s seconds.", interval)

            # loop breaks explicitly for all possible exit conditions
            while True:
                i += 1
                result = f(i, *args, **kwargs)

                if result:
                    logger.debug("iteration %s. Desired state reached.", i)
                    break

                sleep = interval(i) if is_interval_callable else interval

                if max_attempts:
                    if i < max_attempts:
                        logger.debug(
                            "ITERATION %S. SLEEPING FOR %SS. STILL WAITING...",
                            i, sleep)
                        time.sleep(sleep)
                    else:
                        logger.debug(
                            "iteration %s. Max attempts exhausted.", i)
                        break
                else:
                    # result False AND max_attempts is None means keep looping
                    # because None = infinite
                    logger.debug(
                        "iteration %s. Sleeping for %ss. Still waiting...",
                        i, sleep)
                    time.sleep(sleep)
            logger.debug("done")
            return result

        return sleep_looper

    return decorator

```
===== 89 =====
```
                 if max_attempts:
                     if i < max_attempts:
                         logger.debug(
-                            "iteration %s. Sleeping for %ss. Still waiting...",
+                            "XXiteration %s. Sleeping for %ss. Still waiting...XX",
                             i, sleep)
                         time.sleep(sleep)
                     else:
@@ -83,4 +83,4 @@ 
         return sleep_looper
 
-    return decorator+    return decorator
```
```
def while_until_true(interval, max_attempts):
    """Execute a decorated function until it returns True.

    Executes wrapped function at every number of seconds specified by interval,
    until wrapped function either returns True or max_attempts are exhausted,
    whichever comes 1st.

    Interval is in seconds. It is either a simple float value, or a callable
    that returns a float value. If it is a callable, the passed callable will
    execute on every iteration. The callable signature is:
    func(n: int) -> float

    n is the iteration counter.

    The difference between while_until_true and wait_until_true is that the
    latter will always loop to a max_attempts, whereas while_until_true will
    keep going indefinitely.

    The other notable difference to wait_until_true is that the wrapped
    function signature must be:
    func(counter, *args, **kwargs)

    This is because this decorator injects the while loop counter into the
    invoked function.

    Args:
        interval (float or callable): In seconds. How long to wait between
            executing the wrapped function. The callable signature is func(n)
            where n is the iteration counter, and should return a float.
        max_attempts (int): Execute wrapped function up to this limit. None
                      means infinite (or until wrapped function returns True).
                      Passing anything <0 also means infinite.

    Returns:
        Bool. True if wrapped function returned True. False if reached
              max_attempts without the wrapped function ever returning True.
    """
    def decorator(f):
        logger.debug("started")

        def sleep_looper(*args, **kwargs):
            i = 0
            result = False
            is_interval_callable = callable(interval)

            if not is_interval_callable:
                if max_attempts:
                    logger.debug("Looping every %s seconds for %s attempts",
                                 interval, max_attempts)
                else:
                    logger.debug("Looping every %s seconds.", interval)

            # loop breaks explicitly for all possible exit conditions
            while True:
                i += 1
                result = f(i, *args, **kwargs)

                if result:
                    logger.debug("iteration %s. Desired state reached.", i)
                    break

                sleep = interval(i) if is_interval_callable else interval

                if max_attempts:
                    if i < max_attempts:
                        logger.debug(
                            "XXiteration %s. Sleeping for %ss. Still waiting...XX",
                            i, sleep)
                        time.sleep(sleep)
                    else:
                        logger.debug(
                            "iteration %s. Max attempts exhausted.", i)
                        break
                else:
                    # result False AND max_attempts is None means keep looping
                    # because None = infinite
                    logger.debug(
                        "iteration %s. Sleeping for %ss. Still waiting...",
                        i, sleep)
                    time.sleep(sleep)
            logger.debug("done")
            return result

        return sleep_looper

    return decorator

```
===== 90 =====
```
                 if max_attempts:
                     if i < max_attempts:
                         logger.debug(
-                            "iteration %s. Sleeping for %ss. Still waiting...",
+                            "iteration %s. sleeping for %ss. still waiting...",
                             i, sleep)
                         time.sleep(sleep)
                     else:
@@ -83,4 +83,4 @@ 
         return sleep_looper
 
-    return decorator+    return decorator
```
```
def while_until_true(interval, max_attempts):
    """Execute a decorated function until it returns True.

    Executes wrapped function at every number of seconds specified by interval,
    until wrapped function either returns True or max_attempts are exhausted,
    whichever comes 1st.

    Interval is in seconds. It is either a simple float value, or a callable
    that returns a float value. If it is a callable, the passed callable will
    execute on every iteration. The callable signature is:
    func(n: int) -> float

    n is the iteration counter.

    The difference between while_until_true and wait_until_true is that the
    latter will always loop to a max_attempts, whereas while_until_true will
    keep going indefinitely.

    The other notable difference to wait_until_true is that the wrapped
    function signature must be:
    func(counter, *args, **kwargs)

    This is because this decorator injects the while loop counter into the
    invoked function.

    Args:
        interval (float or callable): In seconds. How long to wait between
            executing the wrapped function. The callable signature is func(n)
            where n is the iteration counter, and should return a float.
        max_attempts (int): Execute wrapped function up to this limit. None
                      means infinite (or until wrapped function returns True).
                      Passing anything <0 also means infinite.

    Returns:
        Bool. True if wrapped function returned True. False if reached
              max_attempts without the wrapped function ever returning True.
    """
    def decorator(f):
        logger.debug("started")

        def sleep_looper(*args, **kwargs):
            i = 0
            result = False
            is_interval_callable = callable(interval)

            if not is_interval_callable:
                if max_attempts:
                    logger.debug("Looping every %s seconds for %s attempts",
                                 interval, max_attempts)
                else:
                    logger.debug("Looping every %s seconds.", interval)

            # loop breaks explicitly for all possible exit conditions
            while True:
                i += 1
                result = f(i, *args, **kwargs)

                if result:
                    logger.debug("iteration %s. Desired state reached.", i)
                    break

                sleep = interval(i) if is_interval_callable else interval

                if max_attempts:
                    if i < max_attempts:
                        logger.debug(
                            "iteration %s. sleeping for %ss. still waiting...",
                            i, sleep)
                        time.sleep(sleep)
                    else:
                        logger.debug(
                            "iteration %s. Max attempts exhausted.", i)
                        break
                else:
                    # result False AND max_attempts is None means keep looping
                    # because None = infinite
                    logger.debug(
                        "iteration %s. Sleeping for %ss. Still waiting...",
                        i, sleep)
                    time.sleep(sleep)
            logger.debug("done")
            return result

        return sleep_looper

    return decorator

```
===== 91 =====
```
                 if max_attempts:
                     if i < max_attempts:
                         logger.debug(
-                            "iteration %s. Sleeping for %ss. Still waiting...",
+                            None,
                             i, sleep)
                         time.sleep(sleep)
                     else:
@@ -83,4 +83,4 @@ 
         return sleep_looper
 
-    return decorator+    return decorator
```
```
def while_until_true(interval, max_attempts):
    """Execute a decorated function until it returns True.

    Executes wrapped function at every number of seconds specified by interval,
    until wrapped function either returns True or max_attempts are exhausted,
    whichever comes 1st.

    Interval is in seconds. It is either a simple float value, or a callable
    that returns a float value. If it is a callable, the passed callable will
    execute on every iteration. The callable signature is:
    func(n: int) -> float

    n is the iteration counter.

    The difference between while_until_true and wait_until_true is that the
    latter will always loop to a max_attempts, whereas while_until_true will
    keep going indefinitely.

    The other notable difference to wait_until_true is that the wrapped
    function signature must be:
    func(counter, *args, **kwargs)

    This is because this decorator injects the while loop counter into the
    invoked function.

    Args:
        interval (float or callable): In seconds. How long to wait between
            executing the wrapped function. The callable signature is func(n)
            where n is the iteration counter, and should return a float.
        max_attempts (int): Execute wrapped function up to this limit. None
                      means infinite (or until wrapped function returns True).
                      Passing anything <0 also means infinite.

    Returns:
        Bool. True if wrapped function returned True. False if reached
              max_attempts without the wrapped function ever returning True.
    """
    def decorator(f):
        logger.debug("started")

        def sleep_looper(*args, **kwargs):
            i = 0
            result = False
            is_interval_callable = callable(interval)

            if not is_interval_callable:
                if max_attempts:
                    logger.debug("Looping every %s seconds for %s attempts",
                                 interval, max_attempts)
                else:
                    logger.debug("Looping every %s seconds.", interval)

            # loop breaks explicitly for all possible exit conditions
            while True:
                i += 1
                result = f(i, *args, **kwargs)

                if result:
                    logger.debug("iteration %s. Desired state reached.", i)
                    break

                sleep = interval(i) if is_interval_callable else interval

                if max_attempts:
                    if i < max_attempts:
                        logger.debug(
                            None,
                            i, sleep)
                        time.sleep(sleep)
                    else:
                        logger.debug(
                            "iteration %s. Max attempts exhausted.", i)
                        break
                else:
                    # result False AND max_attempts is None means keep looping
                    # because None = infinite
                    logger.debug(
                        "iteration %s. Sleeping for %ss. Still waiting...",
                        i, sleep)
                    time.sleep(sleep)
            logger.debug("done")
            return result

        return sleep_looper

    return decorator

```
===== 92 =====
```
                 if max_attempts:
                     if i < max_attempts:
                         logger.debug(
-                            "iteration %s. Sleeping for %ss. Still waiting...",
                             i, sleep)
                         time.sleep(sleep)
                     else:
@@ -83,4 +82,4 @@ 
         return sleep_looper
 
-    return decorator+    return decorator
```
```
def while_until_true(interval, max_attempts):
    """Execute a decorated function until it returns True.

    Executes wrapped function at every number of seconds specified by interval,
    until wrapped function either returns True or max_attempts are exhausted,
    whichever comes 1st.

    Interval is in seconds. It is either a simple float value, or a callable
    that returns a float value. If it is a callable, the passed callable will
    execute on every iteration. The callable signature is:
    func(n: int) -> float

    n is the iteration counter.

    The difference between while_until_true and wait_until_true is that the
    latter will always loop to a max_attempts, whereas while_until_true will
    keep going indefinitely.

    The other notable difference to wait_until_true is that the wrapped
    function signature must be:
    func(counter, *args, **kwargs)

    This is because this decorator injects the while loop counter into the
    invoked function.

    Args:
        interval (float or callable): In seconds. How long to wait between
            executing the wrapped function. The callable signature is func(n)
            where n is the iteration counter, and should return a float.
        max_attempts (int): Execute wrapped function up to this limit. None
                      means infinite (or until wrapped function returns True).
                      Passing anything <0 also means infinite.

    Returns:
        Bool. True if wrapped function returned True. False if reached
              max_attempts without the wrapped function ever returning True.
    """
    def decorator(f):
        logger.debug("started")

        def sleep_looper(*args, **kwargs):
            i = 0
            result = False
            is_interval_callable = callable(interval)

            if not is_interval_callable:
                if max_attempts:
                    logger.debug("Looping every %s seconds for %s attempts",
                                 interval, max_attempts)
                else:
                    logger.debug("Looping every %s seconds.", interval)

            # loop breaks explicitly for all possible exit conditions
            while True:
                i += 1
                result = f(i, *args, **kwargs)

                if result:
                    logger.debug("iteration %s. Desired state reached.", i)
                    break

                sleep = interval(i) if is_interval_callable else interval

                if max_attempts:
                    if i < max_attempts:
                        logger.debug(
                            i, sleep)
                        time.sleep(sleep)
                    else:
                        logger.debug(
                            "iteration %s. Max attempts exhausted.", i)
                        break
                else:
                    # result False AND max_attempts is None means keep looping
                    # because None = infinite
                    logger.debug(
                        "iteration %s. Sleeping for %ss. Still waiting...",
                        i, sleep)
                    time.sleep(sleep)
            logger.debug("done")
            return result

        return sleep_looper

    return decorator

```
===== 93 =====
```
                     if i < max_attempts:
                         logger.debug(
                             "iteration %s. Sleeping for %ss. Still waiting...",
-                            i, sleep)
+                            None, sleep)
                         time.sleep(sleep)
                     else:
                         logger.debug(
@@ -83,4 +83,4 @@ 
         return sleep_looper
 
-    return decorator+    return decorator
```
```
def while_until_true(interval, max_attempts):
    """Execute a decorated function until it returns True.

    Executes wrapped function at every number of seconds specified by interval,
    until wrapped function either returns True or max_attempts are exhausted,
    whichever comes 1st.

    Interval is in seconds. It is either a simple float value, or a callable
    that returns a float value. If it is a callable, the passed callable will
    execute on every iteration. The callable signature is:
    func(n: int) -> float

    n is the iteration counter.

    The difference between while_until_true and wait_until_true is that the
    latter will always loop to a max_attempts, whereas while_until_true will
    keep going indefinitely.

    The other notable difference to wait_until_true is that the wrapped
    function signature must be:
    func(counter, *args, **kwargs)

    This is because this decorator injects the while loop counter into the
    invoked function.

    Args:
        interval (float or callable): In seconds. How long to wait between
            executing the wrapped function. The callable signature is func(n)
            where n is the iteration counter, and should return a float.
        max_attempts (int): Execute wrapped function up to this limit. None
                      means infinite (or until wrapped function returns True).
                      Passing anything <0 also means infinite.

    Returns:
        Bool. True if wrapped function returned True. False if reached
              max_attempts without the wrapped function ever returning True.
    """
    def decorator(f):
        logger.debug("started")

        def sleep_looper(*args, **kwargs):
            i = 0
            result = False
            is_interval_callable = callable(interval)

            if not is_interval_callable:
                if max_attempts:
                    logger.debug("Looping every %s seconds for %s attempts",
                                 interval, max_attempts)
                else:
                    logger.debug("Looping every %s seconds.", interval)

            # loop breaks explicitly for all possible exit conditions
            while True:
                i += 1
                result = f(i, *args, **kwargs)

                if result:
                    logger.debug("iteration %s. Desired state reached.", i)
                    break

                sleep = interval(i) if is_interval_callable else interval

                if max_attempts:
                    if i < max_attempts:
                        logger.debug(
                            "iteration %s. Sleeping for %ss. Still waiting...",
                            None, sleep)
                        time.sleep(sleep)
                    else:
                        logger.debug(
                            "iteration %s. Max attempts exhausted.", i)
                        break
                else:
                    # result False AND max_attempts is None means keep looping
                    # because None = infinite
                    logger.debug(
                        "iteration %s. Sleeping for %ss. Still waiting...",
                        i, sleep)
                    time.sleep(sleep)
            logger.debug("done")
            return result

        return sleep_looper

    return decorator

```
===== 94 =====
```
                     if i < max_attempts:
                         logger.debug(
                             "iteration %s. Sleeping for %ss. Still waiting...",
-                            i, sleep)
+                            i + 1, sleep)
                         time.sleep(sleep)
                     else:
                         logger.debug(
```
```
def while_until_true(interval, max_attempts):
    """Execute a decorated function until it returns True.

    Executes wrapped function at every number of seconds specified by interval,
    until wrapped function either returns True or max_attempts are exhausted,
    whichever comes 1st.

    Interval is in seconds. It is either a simple float value, or a callable
    that returns a float value. If it is a callable, the passed callable will
    execute on every iteration. The callable signature is:
    func(n: int) -> float

    n is the iteration counter.

    The difference between while_until_true and wait_until_true is that the
    latter will always loop to a max_attempts, whereas while_until_true will
    keep going indefinitely.

    The other notable difference to wait_until_true is that the wrapped
    function signature must be:
    func(counter, *args, **kwargs)

    This is because this decorator injects the while loop counter into the
    invoked function.

    Args:
        interval (float or callable): In seconds. How long to wait between
            executing the wrapped function. The callable signature is func(n)
            where n is the iteration counter, and should return a float.
        max_attempts (int): Execute wrapped function up to this limit. None
                      means infinite (or until wrapped function returns True).
                      Passing anything <0 also means infinite.

    Returns:
        Bool. True if wrapped function returned True. False if reached
              max_attempts without the wrapped function ever returning True.
    """
    def decorator(f):
        logger.debug("started")

        def sleep_looper(*args, **kwargs):
            i = 0
            result = False
            is_interval_callable = callable(interval)

            if not is_interval_callable:
                if max_attempts:
                    logger.debug("Looping every %s seconds for %s attempts",
                                 interval, max_attempts)
                else:
                    logger.debug("Looping every %s seconds.", interval)

            # loop breaks explicitly for all possible exit conditions
            while True:
                i += 1
                result = f(i, *args, **kwargs)

                if result:
                    logger.debug("iteration %s. Desired state reached.", i)
                    break

                sleep = interval(i) if is_interval_callable else interval

                if max_attempts:
                    if i < max_attempts:
                        logger.debug(
                            "iteration %s. Sleeping for %ss. Still waiting...",
                            i + 1, sleep)
                        time.sleep(sleep)
                    else:
                        logger.debug(
                            "iteration %s. Max attempts exhausted.", i)
                        break
                else:
                    # result False AND max_attempts is None means keep looping
                    # because None = infinite
                    logger.debug(
                        "iteration %s. Sleeping for %ss. Still waiting...",
                        i, sleep)
                    time.sleep(sleep)
            logger.debug("done")
            return result

        return sleep_looper

    return decorator
```
===== 95 =====
```
                     if i < max_attempts:
                         logger.debug(
                             "iteration %s. Sleeping for %ss. Still waiting...",
-                            i, sleep)
+                            i, )
                         time.sleep(sleep)
                     else:
                         logger.debug(
@@ -83,4 +83,4 @@ 
         return sleep_looper
 
-    return decorator+    return decorator
```
```
def while_until_true(interval, max_attempts):
    """Execute a decorated function until it returns True.

    Executes wrapped function at every number of seconds specified by interval,
    until wrapped function either returns True or max_attempts are exhausted,
    whichever comes 1st.

    Interval is in seconds. It is either a simple float value, or a callable
    that returns a float value. If it is a callable, the passed callable will
    execute on every iteration. The callable signature is:
    func(n: int) -> float

    n is the iteration counter.

    The difference between while_until_true and wait_until_true is that the
    latter will always loop to a max_attempts, whereas while_until_true will
    keep going indefinitely.

    The other notable difference to wait_until_true is that the wrapped
    function signature must be:
    func(counter, *args, **kwargs)

    This is because this decorator injects the while loop counter into the
    invoked function.

    Args:
        interval (float or callable): In seconds. How long to wait between
            executing the wrapped function. The callable signature is func(n)
            where n is the iteration counter, and should return a float.
        max_attempts (int): Execute wrapped function up to this limit. None
                      means infinite (or until wrapped function returns True).
                      Passing anything <0 also means infinite.

    Returns:
        Bool. True if wrapped function returned True. False if reached
              max_attempts without the wrapped function ever returning True.
    """
    def decorator(f):
        logger.debug("started")

        def sleep_looper(*args, **kwargs):
            i = 0
            result = False
            is_interval_callable = callable(interval)

            if not is_interval_callable:
                if max_attempts:
                    logger.debug("Looping every %s seconds for %s attempts",
                                 interval, max_attempts)
                else:
                    logger.debug("Looping every %s seconds.", interval)

            # loop breaks explicitly for all possible exit conditions
            while True:
                i += 1
                result = f(i, *args, **kwargs)

                if result:
                    logger.debug("iteration %s. Desired state reached.", i)
                    break

                sleep = interval(i) if is_interval_callable else interval

                if max_attempts:
                    if i < max_attempts:
                        logger.debug(
                            "iteration %s. Sleeping for %ss. Still waiting...",
                            i, )
                        time.sleep(sleep)
                    else:
                        logger.debug(
                            "iteration %s. Max attempts exhausted.", i)
                        break
                else:
                    # result False AND max_attempts is None means keep looping
                    # because None = infinite
                    logger.debug(
                        "iteration %s. Sleeping for %ss. Still waiting...",
                        i, sleep)
                    time.sleep(sleep)
            logger.debug("done")
            return result

        return sleep_looper

    return decorator

```
===== 96 =====
```
                     if i < max_attempts:
                         logger.debug(
                             "iteration %s. Sleeping for %ss. Still waiting...",
-                            i, sleep)
+                            i, None)
                         time.sleep(sleep)
                     else:
                         logger.debug(
@@ -83,4 +83,4 @@ 
         return sleep_looper
 
-    return decorator+    return decorator
```
```
def while_until_true(interval, max_attempts):
    """Execute a decorated function until it returns True.

    Executes wrapped function at every number of seconds specified by interval,
    until wrapped function either returns True or max_attempts are exhausted,
    whichever comes 1st.

    Interval is in seconds. It is either a simple float value, or a callable
    that returns a float value. If it is a callable, the passed callable will
    execute on every iteration. The callable signature is:
    func(n: int) -> float

    n is the iteration counter.

    The difference between while_until_true and wait_until_true is that the
    latter will always loop to a max_attempts, whereas while_until_true will
    keep going indefinitely.

    The other notable difference to wait_until_true is that the wrapped
    function signature must be:
    func(counter, *args, **kwargs)

    This is because this decorator injects the while loop counter into the
    invoked function.

    Args:
        interval (float or callable): In seconds. How long to wait between
            executing the wrapped function. The callable signature is func(n)
            where n is the iteration counter, and should return a float.
        max_attempts (int): Execute wrapped function up to this limit. None
                      means infinite (or until wrapped function returns True).
                      Passing anything <0 also means infinite.

    Returns:
        Bool. True if wrapped function returned True. False if reached
              max_attempts without the wrapped function ever returning True.
    """
    def decorator(f):
        logger.debug("started")

        def sleep_looper(*args, **kwargs):
            i = 0
            result = False
            is_interval_callable = callable(interval)

            if not is_interval_callable:
                if max_attempts:
                    logger.debug("Looping every %s seconds for %s attempts",
                                 interval, max_attempts)
                else:
                    logger.debug("Looping every %s seconds.", interval)

            # loop breaks explicitly for all possible exit conditions
            while True:
                i += 1
                result = f(i, *args, **kwargs)

                if result:
                    logger.debug("iteration %s. Desired state reached.", i)
                    break

                sleep = interval(i) if is_interval_callable else interval

                if max_attempts:
                    if i < max_attempts:
                        logger.debug(
                            "iteration %s. Sleeping for %ss. Still waiting...",
                            i, None)
                        time.sleep(sleep)
                    else:
                        logger.debug(
                            "iteration %s. Max attempts exhausted.", i)
                        break
                else:
                    # result False AND max_attempts is None means keep looping
                    # because None = infinite
                    logger.debug(
                        "iteration %s. Sleeping for %ss. Still waiting...",
                        i, sleep)
                    time.sleep(sleep)
            logger.debug("done")
            return result

        return sleep_looper

    return decorator

```
===== 97 =====
```
                     if i < max_attempts:
                         logger.debug(
                             "iteration %s. Sleeping for %ss. Still waiting...",
-                            i, sleep)
+                            i, sleep * 2)
                         time.sleep(sleep)
                     else:
                         logger.debug(
```
```
def while_until_true(interval, max_attempts):
    """Execute a decorated function until it returns True.

    Executes wrapped function at every number of seconds specified by interval,
    until wrapped function either returns True or max_attempts are exhausted,
    whichever comes 1st.

    Interval is in seconds. It is either a simple float value, or a callable
    that returns a float value. If it is a callable, the passed callable will
    execute on every iteration. The callable signature is:
    func(n: int) -> float

    n is the iteration counter.

    The difference between while_until_true and wait_until_true is that the
    latter will always loop to a max_attempts, whereas while_until_true will
    keep going indefinitely.

    The other notable difference to wait_until_true is that the wrapped
    function signature must be:
    func(counter, *args, **kwargs)

    This is because this decorator injects the while loop counter into the
    invoked function.

    Args:
        interval (float or callable): In seconds. How long to wait between
            executing the wrapped function. The callable signature is func(n)
            where n is the iteration counter, and should return a float.
        max_attempts (int): Execute wrapped function up to this limit. None
                      means infinite (or until wrapped function returns True).
                      Passing anything <0 also means infinite.

    Returns:
        Bool. True if wrapped function returned True. False if reached
              max_attempts without the wrapped function ever returning True.
    """
    def decorator(f):
        logger.debug("started")

        def sleep_looper(*args, **kwargs):
            i = 0
            result = False
            is_interval_callable = callable(interval)

            if not is_interval_callable:
                if max_attempts:
                    logger.debug("Looping every %s seconds for %s attempts",
                                 interval, max_attempts)
                else:
                    logger.debug("Looping every %s seconds.", interval)

            # loop breaks explicitly for all possible exit conditions
            while True:
                i += 1
                result = f(i, *args, **kwargs)

                if result:
                    logger.debug("iteration %s. Desired state reached.", i)
                    break

                sleep = interval(i) if is_interval_callable else interval

                if max_attempts:
                    if i < max_attempts:
                        logger.debug(
                            "iteration %s. Sleeping for %ss. Still waiting...",
                            i, sleep * 2)
                        time.sleep(sleep)
                    else:
                        logger.debug(
                            "iteration %s. Max attempts exhausted.", i)
                        break
                else:
                    # result False AND max_attempts is None means keep looping
                    # because None = infinite
                    logger.debug(
                        "iteration %s. Sleeping for %ss. Still waiting...",
                        i, sleep)
                    time.sleep(sleep)
            logger.debug("done")
            return result

        return sleep_looper

    return decorator
```
===== 98 =====
```
                     if i < max_attempts:
                         logger.debug(
                             "iteration %s. Sleeping for %ss. Still waiting...",
-                            i, sleep)
+                            i, sleep + 1)
                         time.sleep(sleep)
                     else:
                         logger.debug(
```
```
def while_until_true(interval, max_attempts):
    """Execute a decorated function until it returns True.

    Executes wrapped function at every number of seconds specified by interval,
    until wrapped function either returns True or max_attempts are exhausted,
    whichever comes 1st.

    Interval is in seconds. It is either a simple float value, or a callable
    that returns a float value. If it is a callable, the passed callable will
    execute on every iteration. The callable signature is:
    func(n: int) -> float

    n is the iteration counter.

    The difference between while_until_true and wait_until_true is that the
    latter will always loop to a max_attempts, whereas while_until_true will
    keep going indefinitely.

    The other notable difference to wait_until_true is that the wrapped
    function signature must be:
    func(counter, *args, **kwargs)

    This is because this decorator injects the while loop counter into the
    invoked function.

    Args:
        interval (float or callable): In seconds. How long to wait between
            executing the wrapped function. The callable signature is func(n)
            where n is the iteration counter, and should return a float.
        max_attempts (int): Execute wrapped function up to this limit. None
                      means infinite (or until wrapped function returns True).
                      Passing anything <0 also means infinite.

    Returns:
        Bool. True if wrapped function returned True. False if reached
              max_attempts without the wrapped function ever returning True.
    """
    def decorator(f):
        logger.debug("started")

        def sleep_looper(*args, **kwargs):
            i = 0
            result = False
            is_interval_callable = callable(interval)

            if not is_interval_callable:
                if max_attempts:
                    logger.debug("Looping every %s seconds for %s attempts",
                                 interval, max_attempts)
                else:
                    logger.debug("Looping every %s seconds.", interval)

            # loop breaks explicitly for all possible exit conditions
            while True:
                i += 1
                result = f(i, *args, **kwargs)

                if result:
                    logger.debug("iteration %s. Desired state reached.", i)
                    break

                sleep = interval(i) if is_interval_callable else interval

                if max_attempts:
                    if i < max_attempts:
                        logger.debug(
                            "iteration %s. Sleeping for %ss. Still waiting...",
                            i, sleep + 1)
                        time.sleep(sleep)
                    else:
                        logger.debug(
                            "iteration %s. Max attempts exhausted.", i)
                        break
                else:
                    # result False AND max_attempts is None means keep looping
                    # because None = infinite
                    logger.debug(
                        "iteration %s. Sleeping for %ss. Still waiting...",
                        i, sleep)
                    time.sleep(sleep)
            logger.debug("done")
            return result

        return sleep_looper

    return decorator
```
===== 99 =====
```
                     if i < max_attempts:
                         logger.debug(
                             "iteration %s. Sleeping for %ss. Still waiting...",
-                            i, sleep)
+                            i, sleep - 1)
                         time.sleep(sleep)
                     else:
                         logger.debug(
```
```
def while_until_true(interval, max_attempts):
    """Execute a decorated function until it returns True.

    Executes wrapped function at every number of seconds specified by interval,
    until wrapped function either returns True or max_attempts are exhausted,
    whichever comes 1st.

    Interval is in seconds. It is either a simple float value, or a callable
    that returns a float value. If it is a callable, the passed callable will
    execute on every iteration. The callable signature is:
    func(n: int) -> float

    n is the iteration counter.

    The difference between while_until_true and wait_until_true is that the
    latter will always loop to a max_attempts, whereas while_until_true will
    keep going indefinitely.

    The other notable difference to wait_until_true is that the wrapped
    function signature must be:
    func(counter, *args, **kwargs)

    This is because this decorator injects the while loop counter into the
    invoked function.

    Args:
        interval (float or callable): In seconds. How long to wait between
            executing the wrapped function. The callable signature is func(n)
            where n is the iteration counter, and should return a float.
        max_attempts (int): Execute wrapped function up to this limit. None
                      means infinite (or until wrapped function returns True).
                      Passing anything <0 also means infinite.

    Returns:
        Bool. True if wrapped function returned True. False if reached
              max_attempts without the wrapped function ever returning True.
    """
    def decorator(f):
        logger.debug("started")

        def sleep_looper(*args, **kwargs):
            i = 0
            result = False
            is_interval_callable = callable(interval)

            if not is_interval_callable:
                if max_attempts:
                    logger.debug("Looping every %s seconds for %s attempts",
                                 interval, max_attempts)
                else:
                    logger.debug("Looping every %s seconds.", interval)

            # loop breaks explicitly for all possible exit conditions
            while True:
                i += 1
                result = f(i, *args, **kwargs)

                if result:
                    logger.debug("iteration %s. Desired state reached.", i)
                    break

                sleep = interval(i) if is_interval_callable else interval

                if max_attempts:
                    if i < max_attempts:
                        logger.debug(
                            "iteration %s. Sleeping for %ss. Still waiting...",
                            i, sleep - 1)
                        time.sleep(sleep)
                    else:
                        logger.debug(
                            "iteration %s. Max attempts exhausted.", i)
                        break
                else:
                    # result False AND max_attempts is None means keep looping
                    # because None = infinite
                    logger.debug(
                        "iteration %s. Sleeping for %ss. Still waiting...",
                        i, sleep)
                    time.sleep(sleep)
            logger.debug("done")
            return result

        return sleep_looper

    return decorator
```
===== 100 =====
```
                     if i < max_attempts:
                         logger.debug(
                             "iteration %s. Sleeping for %ss. Still waiting...",
-                            i, sleep)
+                            i, sleep / 2)
                         time.sleep(sleep)
                     else:
                         logger.debug(
```
```
def while_until_true(interval, max_attempts):
    """Execute a decorated function until it returns True.

    Executes wrapped function at every number of seconds specified by interval,
    until wrapped function either returns True or max_attempts are exhausted,
    whichever comes 1st.

    Interval is in seconds. It is either a simple float value, or a callable
    that returns a float value. If it is a callable, the passed callable will
    execute on every iteration. The callable signature is:
    func(n: int) -> float

    n is the iteration counter.

    The difference between while_until_true and wait_until_true is that the
    latter will always loop to a max_attempts, whereas while_until_true will
    keep going indefinitely.

    The other notable difference to wait_until_true is that the wrapped
    function signature must be:
    func(counter, *args, **kwargs)

    This is because this decorator injects the while loop counter into the
    invoked function.

    Args:
        interval (float or callable): In seconds. How long to wait between
            executing the wrapped function. The callable signature is func(n)
            where n is the iteration counter, and should return a float.
        max_attempts (int): Execute wrapped function up to this limit. None
                      means infinite (or until wrapped function returns True).
                      Passing anything <0 also means infinite.

    Returns:
        Bool. True if wrapped function returned True. False if reached
              max_attempts without the wrapped function ever returning True.
    """
    def decorator(f):
        logger.debug("started")

        def sleep_looper(*args, **kwargs):
            i = 0
            result = False
            is_interval_callable = callable(interval)

            if not is_interval_callable:
                if max_attempts:
                    logger.debug("Looping every %s seconds for %s attempts",
                                 interval, max_attempts)
                else:
                    logger.debug("Looping every %s seconds.", interval)

            # loop breaks explicitly for all possible exit conditions
            while True:
                i += 1
                result = f(i, *args, **kwargs)

                if result:
                    logger.debug("iteration %s. Desired state reached.", i)
                    break

                sleep = interval(i) if is_interval_callable else interval

                if max_attempts:
                    if i < max_attempts:
                        logger.debug(
                            "iteration %s. Sleeping for %ss. Still waiting...",
                            i, sleep / 2)
                        time.sleep(sleep)
                    else:
                        logger.debug(
                            "iteration %s. Max attempts exhausted.", i)
                        break
                else:
                    # result False AND max_attempts is None means keep looping
                    # because None = infinite
                    logger.debug(
                        "iteration %s. Sleeping for %ss. Still waiting...",
                        i, sleep)
                    time.sleep(sleep)
            logger.debug("done")
            return result

        return sleep_looper

    return decorator
```
===== 101 =====
```
                     if i < max_attempts:
                         logger.debug(
                             "iteration %s. Sleeping for %ss. Still waiting...",
-                            i, sleep)
+                            sleep)
                         time.sleep(sleep)
                     else:
                         logger.debug(
@@ -83,4 +83,4 @@ 
         return sleep_looper
 
-    return decorator+    return decorator
```
```
def while_until_true(interval, max_attempts):
    """Execute a decorated function until it returns True.

    Executes wrapped function at every number of seconds specified by interval,
    until wrapped function either returns True or max_attempts are exhausted,
    whichever comes 1st.

    Interval is in seconds. It is either a simple float value, or a callable
    that returns a float value. If it is a callable, the passed callable will
    execute on every iteration. The callable signature is:
    func(n: int) -> float

    n is the iteration counter.

    The difference between while_until_true and wait_until_true is that the
    latter will always loop to a max_attempts, whereas while_until_true will
    keep going indefinitely.

    The other notable difference to wait_until_true is that the wrapped
    function signature must be:
    func(counter, *args, **kwargs)

    This is because this decorator injects the while loop counter into the
    invoked function.

    Args:
        interval (float or callable): In seconds. How long to wait between
            executing the wrapped function. The callable signature is func(n)
            where n is the iteration counter, and should return a float.
        max_attempts (int): Execute wrapped function up to this limit. None
                      means infinite (or until wrapped function returns True).
                      Passing anything <0 also means infinite.

    Returns:
        Bool. True if wrapped function returned True. False if reached
              max_attempts without the wrapped function ever returning True.
    """
    def decorator(f):
        logger.debug("started")

        def sleep_looper(*args, **kwargs):
            i = 0
            result = False
            is_interval_callable = callable(interval)

            if not is_interval_callable:
                if max_attempts:
                    logger.debug("Looping every %s seconds for %s attempts",
                                 interval, max_attempts)
                else:
                    logger.debug("Looping every %s seconds.", interval)

            # loop breaks explicitly for all possible exit conditions
            while True:
                i += 1
                result = f(i, *args, **kwargs)

                if result:
                    logger.debug("iteration %s. Desired state reached.", i)
                    break

                sleep = interval(i) if is_interval_callable else interval

                if max_attempts:
                    if i < max_attempts:
                        logger.debug(
                            "iteration %s. Sleeping for %ss. Still waiting...",
                            sleep)
                        time.sleep(sleep)
                    else:
                        logger.debug(
                            "iteration %s. Max attempts exhausted.", i)
                        break
                else:
                    # result False AND max_attempts is None means keep looping
                    # because None = infinite
                    logger.debug(
                        "iteration %s. Sleeping for %ss. Still waiting...",
                        i, sleep)
                    time.sleep(sleep)
            logger.debug("done")
            return result

        return sleep_looper

    return decorator

```
===== 102 =====
```
                         logger.debug(
                             "iteration %s. Sleeping for %ss. Still waiting...",
                             i, sleep)
-                        time.sleep(sleep)
+                        time.sleep(0)  # Sleep for zero seconds, effectively making it a busy wait.
                     else:
                         logger.debug(
                             "iteration %s. Max attempts exhausted.", i)
```
```
def while_until_true(interval, max_attempts):
    """Execute a decorated function until it returns True.

    Executes wrapped function at every number of seconds specified by interval,
    until wrapped function either returns True or max_attempts are exhausted,
    whichever comes 1st.

    Interval is in seconds. It is either a simple float value, or a callable
    that returns a float value. If it is a callable, the passed callable will
    execute on every iteration. The callable signature is:
    func(n: int) -> float

    n is the iteration counter.

    The difference between while_until_true and wait_until_true is that the
    latter will always loop to a max_attempts, whereas while_until_true will
    keep going indefinitely.

    The other notable difference to wait_until_true is that the wrapped
    function signature must be:
    func(counter, *args, **kwargs)

    This is because this decorator injects the while loop counter into the
    invoked function.

    Args:
        interval (float or callable): In seconds. How long to wait between
            executing the wrapped function. The callable signature is func(n)
            where n is the iteration counter, and should return a float.
        max_attempts (int): Execute wrapped function up to this limit. None
                      means infinite (or until wrapped function returns True).
                      Passing anything <0 also means infinite.

    Returns:
        Bool. True if wrapped function returned True. False if reached
              max_attempts without the wrapped function ever returning True.
    """
    def decorator(f):
        logger.debug("started")

        def sleep_looper(*args, **kwargs):
            i = 0
            result = False
            is_interval_callable = callable(interval)

            if not is_interval_callable:
                if max_attempts:
                    logger.debug("Looping every %s seconds for %s attempts",
                                 interval, max_attempts)
                else:
                    logger.debug("Looping every %s seconds.", interval)

            # loop breaks explicitly for all possible exit conditions
            while True:
                i += 1
                result = f(i, *args, **kwargs)

                if result:
                    logger.debug("iteration %s. Desired state reached.", i)
                    break

                sleep = interval(i) if is_interval_callable else interval

                if max_attempts:
                    if i < max_attempts:
                        logger.debug(
                            "iteration %s. Sleeping for %ss. Still waiting...",
                            i, sleep)
                        time.sleep(0)  # Sleep for zero seconds, effectively making it a busy wait.
                    else:
                        logger.debug(
                            "iteration %s. Max attempts exhausted.", i)
                        break
                else:
                    # result False AND max_attempts is None means keep looping
                    # because None = infinite
                    logger.debug(
                        "iteration %s. Sleeping for %ss. Still waiting...",
                        i, sleep)
                    time.sleep(sleep)
            logger.debug("done")
            return result

        return sleep_looper

    return decorator
```
===== 103 =====
```
                         logger.debug(
                             "iteration %s. Sleeping for %ss. Still waiting...",
                             i, sleep)
-                        time.sleep(sleep)
+                        time.sleep(None)
                     else:
                         logger.debug(
                             "iteration %s. Max attempts exhausted.", i)
@@ -83,4 +83,4 @@ 
         return sleep_looper
 
-    return decorator+    return decorator
```
```
def while_until_true(interval, max_attempts):
    """Execute a decorated function until it returns True.

    Executes wrapped function at every number of seconds specified by interval,
    until wrapped function either returns True or max_attempts are exhausted,
    whichever comes 1st.

    Interval is in seconds. It is either a simple float value, or a callable
    that returns a float value. If it is a callable, the passed callable will
    execute on every iteration. The callable signature is:
    func(n: int) -> float

    n is the iteration counter.

    The difference between while_until_true and wait_until_true is that the
    latter will always loop to a max_attempts, whereas while_until_true will
    keep going indefinitely.

    The other notable difference to wait_until_true is that the wrapped
    function signature must be:
    func(counter, *args, **kwargs)

    This is because this decorator injects the while loop counter into the
    invoked function.

    Args:
        interval (float or callable): In seconds. How long to wait between
            executing the wrapped function. The callable signature is func(n)
            where n is the iteration counter, and should return a float.
        max_attempts (int): Execute wrapped function up to this limit. None
                      means infinite (or until wrapped function returns True).
                      Passing anything <0 also means infinite.

    Returns:
        Bool. True if wrapped function returned True. False if reached
              max_attempts without the wrapped function ever returning True.
    """
    def decorator(f):
        logger.debug("started")

        def sleep_looper(*args, **kwargs):
            i = 0
            result = False
            is_interval_callable = callable(interval)

            if not is_interval_callable:
                if max_attempts:
                    logger.debug("Looping every %s seconds for %s attempts",
                                 interval, max_attempts)
                else:
                    logger.debug("Looping every %s seconds.", interval)

            # loop breaks explicitly for all possible exit conditions
            while True:
                i += 1
                result = f(i, *args, **kwargs)

                if result:
                    logger.debug("iteration %s. Desired state reached.", i)
                    break

                sleep = interval(i) if is_interval_callable else interval

                if max_attempts:
                    if i < max_attempts:
                        logger.debug(
                            "iteration %s. Sleeping for %ss. Still waiting...",
                            i, sleep)
                        time.sleep(None)
                    else:
                        logger.debug(
                            "iteration %s. Max attempts exhausted.", i)
                        break
                else:
                    # result False AND max_attempts is None means keep looping
                    # because None = infinite
                    logger.debug(
                        "iteration %s. Sleeping for %ss. Still waiting...",
                        i, sleep)
                    time.sleep(sleep)
            logger.debug("done")
            return result

        return sleep_looper

    return decorator

```
===== 104 =====
```
                         logger.debug(
                             "iteration %s. Sleeping for %ss. Still waiting...",
                             i, sleep)
-                        time.sleep(sleep)
+                        time.sleep(sleep * 2)  # Sleep for double the intended time, causing longer waits.
                     else:
                         logger.debug(
                             "iteration %s. Max attempts exhausted.", i)
```
```
def while_until_true(interval, max_attempts):
    """Execute a decorated function until it returns True.

    Executes wrapped function at every number of seconds specified by interval,
    until wrapped function either returns True or max_attempts are exhausted,
    whichever comes 1st.

    Interval is in seconds. It is either a simple float value, or a callable
    that returns a float value. If it is a callable, the passed callable will
    execute on every iteration. The callable signature is:
    func(n: int) -> float

    n is the iteration counter.

    The difference between while_until_true and wait_until_true is that the
    latter will always loop to a max_attempts, whereas while_until_true will
    keep going indefinitely.

    The other notable difference to wait_until_true is that the wrapped
    function signature must be:
    func(counter, *args, **kwargs)

    This is because this decorator injects the while loop counter into the
    invoked function.

    Args:
        interval (float or callable): In seconds. How long to wait between
            executing the wrapped function. The callable signature is func(n)
            where n is the iteration counter, and should return a float.
        max_attempts (int): Execute wrapped function up to this limit. None
                      means infinite (or until wrapped function returns True).
                      Passing anything <0 also means infinite.

    Returns:
        Bool. True if wrapped function returned True. False if reached
              max_attempts without the wrapped function ever returning True.
    """
    def decorator(f):
        logger.debug("started")

        def sleep_looper(*args, **kwargs):
            i = 0
            result = False
            is_interval_callable = callable(interval)

            if not is_interval_callable:
                if max_attempts:
                    logger.debug("Looping every %s seconds for %s attempts",
                                 interval, max_attempts)
                else:
                    logger.debug("Looping every %s seconds.", interval)

            # loop breaks explicitly for all possible exit conditions
            while True:
                i += 1
                result = f(i, *args, **kwargs)

                if result:
                    logger.debug("iteration %s. Desired state reached.", i)
                    break

                sleep = interval(i) if is_interval_callable else interval

                if max_attempts:
                    if i < max_attempts:
                        logger.debug(
                            "iteration %s. Sleeping for %ss. Still waiting...",
                            i, sleep)
                        time.sleep(sleep * 2)  # Sleep for double the intended time, causing longer waits.
                    else:
                        logger.debug(
                            "iteration %s. Max attempts exhausted.", i)
                        break
                else:
                    # result False AND max_attempts is None means keep looping
                    # because None = infinite
                    logger.debug(
                        "iteration %s. Sleeping for %ss. Still waiting...",
                        i, sleep)
                    time.sleep(sleep)
            logger.debug("done")
            return result

        return sleep_looper

    return decorator
```
===== 105 =====
```
                         logger.debug(
                             "iteration %s. Sleeping for %ss. Still waiting...",
                             i, sleep)
-                        time.sleep(sleep)
+                        time.sleep(sleep / 2)  # Sleep for half the intended time, potentially leading to premature function calls.
                     else:
                         logger.debug(
                             "iteration %s. Max attempts exhausted.", i)
```
```
def while_until_true(interval, max_attempts):
    """Execute a decorated function until it returns True.

    Executes wrapped function at every number of seconds specified by interval,
    until wrapped function either returns True or max_attempts are exhausted,
    whichever comes 1st.

    Interval is in seconds. It is either a simple float value, or a callable
    that returns a float value. If it is a callable, the passed callable will
    execute on every iteration. The callable signature is:
    func(n: int) -> float

    n is the iteration counter.

    The difference between while_until_true and wait_until_true is that the
    latter will always loop to a max_attempts, whereas while_until_true will
    keep going indefinitely.

    The other notable difference to wait_until_true is that the wrapped
    function signature must be:
    func(counter, *args, **kwargs)

    This is because this decorator injects the while loop counter into the
    invoked function.

    Args:
        interval (float or callable): In seconds. How long to wait between
            executing the wrapped function. The callable signature is func(n)
            where n is the iteration counter, and should return a float.
        max_attempts (int): Execute wrapped function up to this limit. None
                      means infinite (or until wrapped function returns True).
                      Passing anything <0 also means infinite.

    Returns:
        Bool. True if wrapped function returned True. False if reached
              max_attempts without the wrapped function ever returning True.
    """
    def decorator(f):
        logger.debug("started")

        def sleep_looper(*args, **kwargs):
            i = 0
            result = False
            is_interval_callable = callable(interval)

            if not is_interval_callable:
                if max_attempts:
                    logger.debug("Looping every %s seconds for %s attempts",
                                 interval, max_attempts)
                else:
                    logger.debug("Looping every %s seconds.", interval)

            # loop breaks explicitly for all possible exit conditions
            while True:
                i += 1
                result = f(i, *args, **kwargs)

                if result:
                    logger.debug("iteration %s. Desired state reached.", i)
                    break

                sleep = interval(i) if is_interval_callable else interval

                if max_attempts:
                    if i < max_attempts:
                        logger.debug(
                            "iteration %s. Sleeping for %ss. Still waiting...",
                            i, sleep)
                        time.sleep(sleep / 2)  # Sleep for half the intended time, potentially leading to premature function calls.
                    else:
                        logger.debug(
                            "iteration %s. Max attempts exhausted.", i)
                        break
                else:
                    # result False AND max_attempts is None means keep looping
                    # because None = infinite
                    logger.debug(
                        "iteration %s. Sleeping for %ss. Still waiting...",
                        i, sleep)
                    time.sleep(sleep)
            logger.debug("done")
            return result

        return sleep_looper

    return decorator
```
===== 106 =====
```
                         logger.debug(
                             "iteration %s. Sleeping for %ss. Still waiting...",
                             i, sleep)
-                        time.sleep(sleep)
+                        time.sleep(sleep) if i % 2 == 0 else None  # Only sleep on even iterations, causing inconsistent behavior.
                     else:
                         logger.debug(
                             "iteration %s. Max attempts exhausted.", i)
```
```
def while_until_true(interval, max_attempts):
    """Execute a decorated function until it returns True.

    Executes wrapped function at every number of seconds specified by interval,
    until wrapped function either returns True or max_attempts are exhausted,
    whichever comes 1st.

    Interval is in seconds. It is either a simple float value, or a callable
    that returns a float value. If it is a callable, the passed callable will
    execute on every iteration. The callable signature is:
    func(n: int) -> float

    n is the iteration counter.

    The difference between while_until_true and wait_until_true is that the
    latter will always loop to a max_attempts, whereas while_until_true will
    keep going indefinitely.

    The other notable difference to wait_until_true is that the wrapped
    function signature must be:
    func(counter, *args, **kwargs)

    This is because this decorator injects the while loop counter into the
    invoked function.

    Args:
        interval (float or callable): In seconds. How long to wait between
            executing the wrapped function. The callable signature is func(n)
            where n is the iteration counter, and should return a float.
        max_attempts (int): Execute wrapped function up to this limit. None
                      means infinite (or until wrapped function returns True).
                      Passing anything <0 also means infinite.

    Returns:
        Bool. True if wrapped function returned True. False if reached
              max_attempts without the wrapped function ever returning True.
    """
    def decorator(f):
        logger.debug("started")

        def sleep_looper(*args, **kwargs):
            i = 0
            result = False
            is_interval_callable = callable(interval)

            if not is_interval_callable:
                if max_attempts:
                    logger.debug("Looping every %s seconds for %s attempts",
                                 interval, max_attempts)
                else:
                    logger.debug("Looping every %s seconds.", interval)

            # loop breaks explicitly for all possible exit conditions
            while True:
                i += 1
                result = f(i, *args, **kwargs)

                if result:
                    logger.debug("iteration %s. Desired state reached.", i)
                    break

                sleep = interval(i) if is_interval_callable else interval

                if max_attempts:
                    if i < max_attempts:
                        logger.debug(
                            "iteration %s. Sleeping for %ss. Still waiting...",
                            i, sleep)
                        time.sleep(sleep) if i % 2 == 0 else None  # Only sleep on even iterations, causing inconsistent behavior.
                    else:
                        logger.debug(
                            "iteration %s. Max attempts exhausted.", i)
                        break
                else:
                    # result False AND max_attempts is None means keep looping
                    # because None = infinite
                    logger.debug(
                        "iteration %s. Sleeping for %ss. Still waiting...",
                        i, sleep)
                    time.sleep(sleep)
            logger.debug("done")
            return result

        return sleep_looper

    return decorator
```
===== 107 =====
```
                         time.sleep(sleep)
                     else:
                         logger.debug(
-                            "iteration %s. Max attempts exhausted.", i)
+                            "ITERATION %S. MAX ATTEMPTS EXHAUSTED.", i)
                         break
                 else:
                     # result False AND max_attempts is None means keep looping
@@ -83,4 +83,4 @@ 
         return sleep_looper
 
-    return decorator+    return decorator
```
```
def while_until_true(interval, max_attempts):
    """Execute a decorated function until it returns True.

    Executes wrapped function at every number of seconds specified by interval,
    until wrapped function either returns True or max_attempts are exhausted,
    whichever comes 1st.

    Interval is in seconds. It is either a simple float value, or a callable
    that returns a float value. If it is a callable, the passed callable will
    execute on every iteration. The callable signature is:
    func(n: int) -> float

    n is the iteration counter.

    The difference between while_until_true and wait_until_true is that the
    latter will always loop to a max_attempts, whereas while_until_true will
    keep going indefinitely.

    The other notable difference to wait_until_true is that the wrapped
    function signature must be:
    func(counter, *args, **kwargs)

    This is because this decorator injects the while loop counter into the
    invoked function.

    Args:
        interval (float or callable): In seconds. How long to wait between
            executing the wrapped function. The callable signature is func(n)
            where n is the iteration counter, and should return a float.
        max_attempts (int): Execute wrapped function up to this limit. None
                      means infinite (or until wrapped function returns True).
                      Passing anything <0 also means infinite.

    Returns:
        Bool. True if wrapped function returned True. False if reached
              max_attempts without the wrapped function ever returning True.
    """
    def decorator(f):
        logger.debug("started")

        def sleep_looper(*args, **kwargs):
            i = 0
            result = False
            is_interval_callable = callable(interval)

            if not is_interval_callable:
                if max_attempts:
                    logger.debug("Looping every %s seconds for %s attempts",
                                 interval, max_attempts)
                else:
                    logger.debug("Looping every %s seconds.", interval)

            # loop breaks explicitly for all possible exit conditions
            while True:
                i += 1
                result = f(i, *args, **kwargs)

                if result:
                    logger.debug("iteration %s. Desired state reached.", i)
                    break

                sleep = interval(i) if is_interval_callable else interval

                if max_attempts:
                    if i < max_attempts:
                        logger.debug(
                            "iteration %s. Sleeping for %ss. Still waiting...",
                            i, sleep)
                        time.sleep(sleep)
                    else:
                        logger.debug(
                            "ITERATION %S. MAX ATTEMPTS EXHAUSTED.", i)
                        break
                else:
                    # result False AND max_attempts is None means keep looping
                    # because None = infinite
                    logger.debug(
                        "iteration %s. Sleeping for %ss. Still waiting...",
                        i, sleep)
                    time.sleep(sleep)
            logger.debug("done")
            return result

        return sleep_looper

    return decorator

```
===== 108 =====
```
                         time.sleep(sleep)
                     else:
                         logger.debug(
-                            "iteration %s. Max attempts exhausted.", i)
+                            "XXiteration %s. Max attempts exhausted.XX", i)
                         break
                 else:
                     # result False AND max_attempts is None means keep looping
@@ -83,4 +83,4 @@ 
         return sleep_looper
 
-    return decorator+    return decorator
```
```
def while_until_true(interval, max_attempts):
    """Execute a decorated function until it returns True.

    Executes wrapped function at every number of seconds specified by interval,
    until wrapped function either returns True or max_attempts are exhausted,
    whichever comes 1st.

    Interval is in seconds. It is either a simple float value, or a callable
    that returns a float value. If it is a callable, the passed callable will
    execute on every iteration. The callable signature is:
    func(n: int) -> float

    n is the iteration counter.

    The difference between while_until_true and wait_until_true is that the
    latter will always loop to a max_attempts, whereas while_until_true will
    keep going indefinitely.

    The other notable difference to wait_until_true is that the wrapped
    function signature must be:
    func(counter, *args, **kwargs)

    This is because this decorator injects the while loop counter into the
    invoked function.

    Args:
        interval (float or callable): In seconds. How long to wait between
            executing the wrapped function. The callable signature is func(n)
            where n is the iteration counter, and should return a float.
        max_attempts (int): Execute wrapped function up to this limit. None
                      means infinite (or until wrapped function returns True).
                      Passing anything <0 also means infinite.

    Returns:
        Bool. True if wrapped function returned True. False if reached
              max_attempts without the wrapped function ever returning True.
    """
    def decorator(f):
        logger.debug("started")

        def sleep_looper(*args, **kwargs):
            i = 0
            result = False
            is_interval_callable = callable(interval)

            if not is_interval_callable:
                if max_attempts:
                    logger.debug("Looping every %s seconds for %s attempts",
                                 interval, max_attempts)
                else:
                    logger.debug("Looping every %s seconds.", interval)

            # loop breaks explicitly for all possible exit conditions
            while True:
                i += 1
                result = f(i, *args, **kwargs)

                if result:
                    logger.debug("iteration %s. Desired state reached.", i)
                    break

                sleep = interval(i) if is_interval_callable else interval

                if max_attempts:
                    if i < max_attempts:
                        logger.debug(
                            "iteration %s. Sleeping for %ss. Still waiting...",
                            i, sleep)
                        time.sleep(sleep)
                    else:
                        logger.debug(
                            "XXiteration %s. Max attempts exhausted.XX", i)
                        break
                else:
                    # result False AND max_attempts is None means keep looping
                    # because None = infinite
                    logger.debug(
                        "iteration %s. Sleeping for %ss. Still waiting...",
                        i, sleep)
                    time.sleep(sleep)
            logger.debug("done")
            return result

        return sleep_looper

    return decorator

```
===== 109 =====
```
                         time.sleep(sleep)
                     else:
                         logger.debug(
-                            "iteration %s. Max attempts exhausted.", i)
+                            "iteration %s. Max attempts exhausted.", )
                         break
                 else:
                     # result False AND max_attempts is None means keep looping
@@ -83,4 +83,4 @@ 
         return sleep_looper
 
-    return decorator+    return decorator
```
```
def while_until_true(interval, max_attempts):
    """Execute a decorated function until it returns True.

    Executes wrapped function at every number of seconds specified by interval,
    until wrapped function either returns True or max_attempts are exhausted,
    whichever comes 1st.

    Interval is in seconds. It is either a simple float value, or a callable
    that returns a float value. If it is a callable, the passed callable will
    execute on every iteration. The callable signature is:
    func(n: int) -> float

    n is the iteration counter.

    The difference between while_until_true and wait_until_true is that the
    latter will always loop to a max_attempts, whereas while_until_true will
    keep going indefinitely.

    The other notable difference to wait_until_true is that the wrapped
    function signature must be:
    func(counter, *args, **kwargs)

    This is because this decorator injects the while loop counter into the
    invoked function.

    Args:
        interval (float or callable): In seconds. How long to wait between
            executing the wrapped function. The callable signature is func(n)
            where n is the iteration counter, and should return a float.
        max_attempts (int): Execute wrapped function up to this limit. None
                      means infinite (or until wrapped function returns True).
                      Passing anything <0 also means infinite.

    Returns:
        Bool. True if wrapped function returned True. False if reached
              max_attempts without the wrapped function ever returning True.
    """
    def decorator(f):
        logger.debug("started")

        def sleep_looper(*args, **kwargs):
            i = 0
            result = False
            is_interval_callable = callable(interval)

            if not is_interval_callable:
                if max_attempts:
                    logger.debug("Looping every %s seconds for %s attempts",
                                 interval, max_attempts)
                else:
                    logger.debug("Looping every %s seconds.", interval)

            # loop breaks explicitly for all possible exit conditions
            while True:
                i += 1
                result = f(i, *args, **kwargs)

                if result:
                    logger.debug("iteration %s. Desired state reached.", i)
                    break

                sleep = interval(i) if is_interval_callable else interval

                if max_attempts:
                    if i < max_attempts:
                        logger.debug(
                            "iteration %s. Sleeping for %ss. Still waiting...",
                            i, sleep)
                        time.sleep(sleep)
                    else:
                        logger.debug(
                            "iteration %s. Max attempts exhausted.", )
                        break
                else:
                    # result False AND max_attempts is None means keep looping
                    # because None = infinite
                    logger.debug(
                        "iteration %s. Sleeping for %ss. Still waiting...",
                        i, sleep)
                    time.sleep(sleep)
            logger.debug("done")
            return result

        return sleep_looper

    return decorator

```
===== 110 =====
```
                         time.sleep(sleep)
                     else:
                         logger.debug(
-                            "iteration %s. Max attempts exhausted.", i)
+                            "iteration %s. Max attempts exhausted.", None)
                         break
                 else:
                     # result False AND max_attempts is None means keep looping
@@ -83,4 +83,4 @@ 
         return sleep_looper
 
-    return decorator+    return decorator
```
```
def while_until_true(interval, max_attempts):
    """Execute a decorated function until it returns True.

    Executes wrapped function at every number of seconds specified by interval,
    until wrapped function either returns True or max_attempts are exhausted,
    whichever comes 1st.

    Interval is in seconds. It is either a simple float value, or a callable
    that returns a float value. If it is a callable, the passed callable will
    execute on every iteration. The callable signature is:
    func(n: int) -> float

    n is the iteration counter.

    The difference between while_until_true and wait_until_true is that the
    latter will always loop to a max_attempts, whereas while_until_true will
    keep going indefinitely.

    The other notable difference to wait_until_true is that the wrapped
    function signature must be:
    func(counter, *args, **kwargs)

    This is because this decorator injects the while loop counter into the
    invoked function.

    Args:
        interval (float or callable): In seconds. How long to wait between
            executing the wrapped function. The callable signature is func(n)
            where n is the iteration counter, and should return a float.
        max_attempts (int): Execute wrapped function up to this limit. None
                      means infinite (or until wrapped function returns True).
                      Passing anything <0 also means infinite.

    Returns:
        Bool. True if wrapped function returned True. False if reached
              max_attempts without the wrapped function ever returning True.
    """
    def decorator(f):
        logger.debug("started")

        def sleep_looper(*args, **kwargs):
            i = 0
            result = False
            is_interval_callable = callable(interval)

            if not is_interval_callable:
                if max_attempts:
                    logger.debug("Looping every %s seconds for %s attempts",
                                 interval, max_attempts)
                else:
                    logger.debug("Looping every %s seconds.", interval)

            # loop breaks explicitly for all possible exit conditions
            while True:
                i += 1
                result = f(i, *args, **kwargs)

                if result:
                    logger.debug("iteration %s. Desired state reached.", i)
                    break

                sleep = interval(i) if is_interval_callable else interval

                if max_attempts:
                    if i < max_attempts:
                        logger.debug(
                            "iteration %s. Sleeping for %ss. Still waiting...",
                            i, sleep)
                        time.sleep(sleep)
                    else:
                        logger.debug(
                            "iteration %s. Max attempts exhausted.", None)
                        break
                else:
                    # result False AND max_attempts is None means keep looping
                    # because None = infinite
                    logger.debug(
                        "iteration %s. Sleeping for %ss. Still waiting...",
                        i, sleep)
                    time.sleep(sleep)
            logger.debug("done")
            return result

        return sleep_looper

    return decorator

```
===== 111 =====
```
                         time.sleep(sleep)
                     else:
                         logger.debug(
-                            "iteration %s. Max attempts exhausted.", i)
+                            "iteration %s. max attempts exhausted.", i)
                         break
                 else:
                     # result False AND max_attempts is None means keep looping
@@ -83,4 +83,4 @@ 
         return sleep_looper
 
-    return decorator+    return decorator
```
```
def while_until_true(interval, max_attempts):
    """Execute a decorated function until it returns True.

    Executes wrapped function at every number of seconds specified by interval,
    until wrapped function either returns True or max_attempts are exhausted,
    whichever comes 1st.

    Interval is in seconds. It is either a simple float value, or a callable
    that returns a float value. If it is a callable, the passed callable will
    execute on every iteration. The callable signature is:
    func(n: int) -> float

    n is the iteration counter.

    The difference between while_until_true and wait_until_true is that the
    latter will always loop to a max_attempts, whereas while_until_true will
    keep going indefinitely.

    The other notable difference to wait_until_true is that the wrapped
    function signature must be:
    func(counter, *args, **kwargs)

    This is because this decorator injects the while loop counter into the
    invoked function.

    Args:
        interval (float or callable): In seconds. How long to wait between
            executing the wrapped function. The callable signature is func(n)
            where n is the iteration counter, and should return a float.
        max_attempts (int): Execute wrapped function up to this limit. None
                      means infinite (or until wrapped function returns True).
                      Passing anything <0 also means infinite.

    Returns:
        Bool. True if wrapped function returned True. False if reached
              max_attempts without the wrapped function ever returning True.
    """
    def decorator(f):
        logger.debug("started")

        def sleep_looper(*args, **kwargs):
            i = 0
            result = False
            is_interval_callable = callable(interval)

            if not is_interval_callable:
                if max_attempts:
                    logger.debug("Looping every %s seconds for %s attempts",
                                 interval, max_attempts)
                else:
                    logger.debug("Looping every %s seconds.", interval)

            # loop breaks explicitly for all possible exit conditions
            while True:
                i += 1
                result = f(i, *args, **kwargs)

                if result:
                    logger.debug("iteration %s. Desired state reached.", i)
                    break

                sleep = interval(i) if is_interval_callable else interval

                if max_attempts:
                    if i < max_attempts:
                        logger.debug(
                            "iteration %s. Sleeping for %ss. Still waiting...",
                            i, sleep)
                        time.sleep(sleep)
                    else:
                        logger.debug(
                            "iteration %s. max attempts exhausted.", i)
                        break
                else:
                    # result False AND max_attempts is None means keep looping
                    # because None = infinite
                    logger.debug(
                        "iteration %s. Sleeping for %ss. Still waiting...",
                        i, sleep)
                    time.sleep(sleep)
            logger.debug("done")
            return result

        return sleep_looper

    return decorator

```
===== 112 =====
```
                         time.sleep(sleep)
                     else:
                         logger.debug(
-                            "iteration %s. Max attempts exhausted.", i)
+                            None, i)
                         break
                 else:
                     # result False AND max_attempts is None means keep looping
@@ -83,4 +83,4 @@ 
         return sleep_looper
 
-    return decorator+    return decorator
```
```
def while_until_true(interval, max_attempts):
    """Execute a decorated function until it returns True.

    Executes wrapped function at every number of seconds specified by interval,
    until wrapped function either returns True or max_attempts are exhausted,
    whichever comes 1st.

    Interval is in seconds. It is either a simple float value, or a callable
    that returns a float value. If it is a callable, the passed callable will
    execute on every iteration. The callable signature is:
    func(n: int) -> float

    n is the iteration counter.

    The difference between while_until_true and wait_until_true is that the
    latter will always loop to a max_attempts, whereas while_until_true will
    keep going indefinitely.

    The other notable difference to wait_until_true is that the wrapped
    function signature must be:
    func(counter, *args, **kwargs)

    This is because this decorator injects the while loop counter into the
    invoked function.

    Args:
        interval (float or callable): In seconds. How long to wait between
            executing the wrapped function. The callable signature is func(n)
            where n is the iteration counter, and should return a float.
        max_attempts (int): Execute wrapped function up to this limit. None
                      means infinite (or until wrapped function returns True).
                      Passing anything <0 also means infinite.

    Returns:
        Bool. True if wrapped function returned True. False if reached
              max_attempts without the wrapped function ever returning True.
    """
    def decorator(f):
        logger.debug("started")

        def sleep_looper(*args, **kwargs):
            i = 0
            result = False
            is_interval_callable = callable(interval)

            if not is_interval_callable:
                if max_attempts:
                    logger.debug("Looping every %s seconds for %s attempts",
                                 interval, max_attempts)
                else:
                    logger.debug("Looping every %s seconds.", interval)

            # loop breaks explicitly for all possible exit conditions
            while True:
                i += 1
                result = f(i, *args, **kwargs)

                if result:
                    logger.debug("iteration %s. Desired state reached.", i)
                    break

                sleep = interval(i) if is_interval_callable else interval

                if max_attempts:
                    if i < max_attempts:
                        logger.debug(
                            "iteration %s. Sleeping for %ss. Still waiting...",
                            i, sleep)
                        time.sleep(sleep)
                    else:
                        logger.debug(
                            None, i)
                        break
                else:
                    # result False AND max_attempts is None means keep looping
                    # because None = infinite
                    logger.debug(
                        "iteration %s. Sleeping for %ss. Still waiting...",
                        i, sleep)
                    time.sleep(sleep)
            logger.debug("done")
            return result

        return sleep_looper

    return decorator

```
===== 113 =====
```
                         time.sleep(sleep)
                     else:
                         logger.debug(
-                            "iteration %s. Max attempts exhausted.", i)
+                            i)
                         break
                 else:
                     # result False AND max_attempts is None means keep looping
@@ -83,4 +83,4 @@ 
         return sleep_looper
 
-    return decorator+    return decorator
```
```
def while_until_true(interval, max_attempts):
    """Execute a decorated function until it returns True.

    Executes wrapped function at every number of seconds specified by interval,
    until wrapped function either returns True or max_attempts are exhausted,
    whichever comes 1st.

    Interval is in seconds. It is either a simple float value, or a callable
    that returns a float value. If it is a callable, the passed callable will
    execute on every iteration. The callable signature is:
    func(n: int) -> float

    n is the iteration counter.

    The difference between while_until_true and wait_until_true is that the
    latter will always loop to a max_attempts, whereas while_until_true will
    keep going indefinitely.

    The other notable difference to wait_until_true is that the wrapped
    function signature must be:
    func(counter, *args, **kwargs)

    This is because this decorator injects the while loop counter into the
    invoked function.

    Args:
        interval (float or callable): In seconds. How long to wait between
            executing the wrapped function. The callable signature is func(n)
            where n is the iteration counter, and should return a float.
        max_attempts (int): Execute wrapped function up to this limit. None
                      means infinite (or until wrapped function returns True).
                      Passing anything <0 also means infinite.

    Returns:
        Bool. True if wrapped function returned True. False if reached
              max_attempts without the wrapped function ever returning True.
    """
    def decorator(f):
        logger.debug("started")

        def sleep_looper(*args, **kwargs):
            i = 0
            result = False
            is_interval_callable = callable(interval)

            if not is_interval_callable:
                if max_attempts:
                    logger.debug("Looping every %s seconds for %s attempts",
                                 interval, max_attempts)
                else:
                    logger.debug("Looping every %s seconds.", interval)

            # loop breaks explicitly for all possible exit conditions
            while True:
                i += 1
                result = f(i, *args, **kwargs)

                if result:
                    logger.debug("iteration %s. Desired state reached.", i)
                    break

                sleep = interval(i) if is_interval_callable else interval

                if max_attempts:
                    if i < max_attempts:
                        logger.debug(
                            "iteration %s. Sleeping for %ss. Still waiting...",
                            i, sleep)
                        time.sleep(sleep)
                    else:
                        logger.debug(
                            i)
                        break
                else:
                    # result False AND max_attempts is None means keep looping
                    # because None = infinite
                    logger.debug(
                        "iteration %s. Sleeping for %ss. Still waiting...",
                        i, sleep)
                    time.sleep(sleep)
            logger.debug("done")
            return result

        return sleep_looper

    return decorator

```
===== 114 =====
```
                     else:
                         logger.debug(
                             "iteration %s. Max attempts exhausted.", i)
-                        break
+                        return
                 else:
                     # result False AND max_attempts is None means keep looping
                     # because None = infinite
@@ -83,4 +83,4 @@ 
         return sleep_looper
 
-    return decorator+    return decorator
```
```
def while_until_true(interval, max_attempts):
    """Execute a decorated function until it returns True.

    Executes wrapped function at every number of seconds specified by interval,
    until wrapped function either returns True or max_attempts are exhausted,
    whichever comes 1st.

    Interval is in seconds. It is either a simple float value, or a callable
    that returns a float value. If it is a callable, the passed callable will
    execute on every iteration. The callable signature is:
    func(n: int) -> float

    n is the iteration counter.

    The difference between while_until_true and wait_until_true is that the
    latter will always loop to a max_attempts, whereas while_until_true will
    keep going indefinitely.

    The other notable difference to wait_until_true is that the wrapped
    function signature must be:
    func(counter, *args, **kwargs)

    This is because this decorator injects the while loop counter into the
    invoked function.

    Args:
        interval (float or callable): In seconds. How long to wait between
            executing the wrapped function. The callable signature is func(n)
            where n is the iteration counter, and should return a float.
        max_attempts (int): Execute wrapped function up to this limit. None
                      means infinite (or until wrapped function returns True).
                      Passing anything <0 also means infinite.

    Returns:
        Bool. True if wrapped function returned True. False if reached
              max_attempts without the wrapped function ever returning True.
    """
    def decorator(f):
        logger.debug("started")

        def sleep_looper(*args, **kwargs):
            i = 0
            result = False
            is_interval_callable = callable(interval)

            if not is_interval_callable:
                if max_attempts:
                    logger.debug("Looping every %s seconds for %s attempts",
                                 interval, max_attempts)
                else:
                    logger.debug("Looping every %s seconds.", interval)

            # loop breaks explicitly for all possible exit conditions
            while True:
                i += 1
                result = f(i, *args, **kwargs)

                if result:
                    logger.debug("iteration %s. Desired state reached.", i)
                    break

                sleep = interval(i) if is_interval_callable else interval

                if max_attempts:
                    if i < max_attempts:
                        logger.debug(
                            "iteration %s. Sleeping for %ss. Still waiting...",
                            i, sleep)
                        time.sleep(sleep)
                    else:
                        logger.debug(
                            "iteration %s. Max attempts exhausted.", i)
                        return
                else:
                    # result False AND max_attempts is None means keep looping
                    # because None = infinite
                    logger.debug(
                        "iteration %s. Sleeping for %ss. Still waiting...",
                        i, sleep)
                    time.sleep(sleep)
            logger.debug("done")
            return result

        return sleep_looper

    return decorator

```
===== 115 =====
```
                 else:
                     # result False AND max_attempts is None means keep looping
                     # because None = infinite
-                    logger.debug(
+                    logger.info(
                         "iteration %s. Sleeping for %ss. Still waiting...",
                         i, sleep)
                     time.sleep(sleep)
```
```
def while_until_true(interval, max_attempts):
    """Execute a decorated function until it returns True.

    Executes wrapped function at every number of seconds specified by interval,
    until wrapped function either returns True or max_attempts are exhausted,
    whichever comes 1st.

    Interval is in seconds. It is either a simple float value, or a callable
    that returns a float value. If it is a callable, the passed callable will
    execute on every iteration. The callable signature is:
    func(n: int) -> float

    n is the iteration counter.

    The difference between while_until_true and wait_until_true is that the
    latter will always loop to a max_attempts, whereas while_until_true will
    keep going indefinitely.

    The other notable difference to wait_until_true is that the wrapped
    function signature must be:
    func(counter, *args, **kwargs)

    This is because this decorator injects the while loop counter into the
    invoked function.

    Args:
        interval (float or callable): In seconds. How long to wait between
            executing the wrapped function. The callable signature is func(n)
            where n is the iteration counter, and should return a float.
        max_attempts (int): Execute wrapped function up to this limit. None
                      means infinite (or until wrapped function returns True).
                      Passing anything <0 also means infinite.

    Returns:
        Bool. True if wrapped function returned True. False if reached
              max_attempts without the wrapped function ever returning True.
    """
    def decorator(f):
        logger.debug("started")

        def sleep_looper(*args, **kwargs):
            i = 0
            result = False
            is_interval_callable = callable(interval)

            if not is_interval_callable:
                if max_attempts:
                    logger.debug("Looping every %s seconds for %s attempts",
                                 interval, max_attempts)
                else:
                    logger.debug("Looping every %s seconds.", interval)

            # loop breaks explicitly for all possible exit conditions
            while True:
                i += 1
                result = f(i, *args, **kwargs)

                if result:
                    logger.debug("iteration %s. Desired state reached.", i)
                    break

                sleep = interval(i) if is_interval_callable else interval

                if max_attempts:
                    if i < max_attempts:
                        logger.debug(
                            "iteration %s. Sleeping for %ss. Still waiting...",
                            i, sleep)
                        time.sleep(sleep)
                    else:
                        logger.debug(
                            "iteration %s. Max attempts exhausted.", i)
                        break
                else:
                    # result False AND max_attempts is None means keep looping
                    # because None = infinite
                    logger.info(
                        "iteration %s. Sleeping for %ss. Still waiting...",
                        i, sleep)
                    time.sleep(sleep)
            logger.debug("done")
            return result

        return sleep_looper

    return decorator
```
===== 116 =====
```
                     # result False AND max_attempts is None means keep looping
                     # because None = infinite
                     logger.debug(
-                        "iteration %s. Sleeping for %ss. Still waiting...",
+                        "ITERATION %S. SLEEPING FOR %SS. STILL WAITING...",
                         i, sleep)
                     time.sleep(sleep)
             logger.debug("done")
@@ -83,4 +83,4 @@ 
         return sleep_looper
 
-    return decorator+    return decorator
```
```
def while_until_true(interval, max_attempts):
    """Execute a decorated function until it returns True.

    Executes wrapped function at every number of seconds specified by interval,
    until wrapped function either returns True or max_attempts are exhausted,
    whichever comes 1st.

    Interval is in seconds. It is either a simple float value, or a callable
    that returns a float value. If it is a callable, the passed callable will
    execute on every iteration. The callable signature is:
    func(n: int) -> float

    n is the iteration counter.

    The difference between while_until_true and wait_until_true is that the
    latter will always loop to a max_attempts, whereas while_until_true will
    keep going indefinitely.

    The other notable difference to wait_until_true is that the wrapped
    function signature must be:
    func(counter, *args, **kwargs)

    This is because this decorator injects the while loop counter into the
    invoked function.

    Args:
        interval (float or callable): In seconds. How long to wait between
            executing the wrapped function. The callable signature is func(n)
            where n is the iteration counter, and should return a float.
        max_attempts (int): Execute wrapped function up to this limit. None
                      means infinite (or until wrapped function returns True).
                      Passing anything <0 also means infinite.

    Returns:
        Bool. True if wrapped function returned True. False if reached
              max_attempts without the wrapped function ever returning True.
    """
    def decorator(f):
        logger.debug("started")

        def sleep_looper(*args, **kwargs):
            i = 0
            result = False
            is_interval_callable = callable(interval)

            if not is_interval_callable:
                if max_attempts:
                    logger.debug("Looping every %s seconds for %s attempts",
                                 interval, max_attempts)
                else:
                    logger.debug("Looping every %s seconds.", interval)

            # loop breaks explicitly for all possible exit conditions
            while True:
                i += 1
                result = f(i, *args, **kwargs)

                if result:
                    logger.debug("iteration %s. Desired state reached.", i)
                    break

                sleep = interval(i) if is_interval_callable else interval

                if max_attempts:
                    if i < max_attempts:
                        logger.debug(
                            "iteration %s. Sleeping for %ss. Still waiting...",
                            i, sleep)
                        time.sleep(sleep)
                    else:
                        logger.debug(
                            "iteration %s. Max attempts exhausted.", i)
                        break
                else:
                    # result False AND max_attempts is None means keep looping
                    # because None = infinite
                    logger.debug(
                        "ITERATION %S. SLEEPING FOR %SS. STILL WAITING...",
                        i, sleep)
                    time.sleep(sleep)
            logger.debug("done")
            return result

        return sleep_looper

    return decorator

```
===== 117 =====
```
                     # result False AND max_attempts is None means keep looping
                     # because None = infinite
                     logger.debug(
-                        "iteration %s. Sleeping for %ss. Still waiting...",
+                        "XXiteration %s. Sleeping for %ss. Still waiting...XX",
                         i, sleep)
                     time.sleep(sleep)
             logger.debug("done")
@@ -83,4 +83,4 @@ 
         return sleep_looper
 
-    return decorator+    return decorator
```
```
def while_until_true(interval, max_attempts):
    """Execute a decorated function until it returns True.

    Executes wrapped function at every number of seconds specified by interval,
    until wrapped function either returns True or max_attempts are exhausted,
    whichever comes 1st.

    Interval is in seconds. It is either a simple float value, or a callable
    that returns a float value. If it is a callable, the passed callable will
    execute on every iteration. The callable signature is:
    func(n: int) -> float

    n is the iteration counter.

    The difference between while_until_true and wait_until_true is that the
    latter will always loop to a max_attempts, whereas while_until_true will
    keep going indefinitely.

    The other notable difference to wait_until_true is that the wrapped
    function signature must be:
    func(counter, *args, **kwargs)

    This is because this decorator injects the while loop counter into the
    invoked function.

    Args:
        interval (float or callable): In seconds. How long to wait between
            executing the wrapped function. The callable signature is func(n)
            where n is the iteration counter, and should return a float.
        max_attempts (int): Execute wrapped function up to this limit. None
                      means infinite (or until wrapped function returns True).
                      Passing anything <0 also means infinite.

    Returns:
        Bool. True if wrapped function returned True. False if reached
              max_attempts without the wrapped function ever returning True.
    """
    def decorator(f):
        logger.debug("started")

        def sleep_looper(*args, **kwargs):
            i = 0
            result = False
            is_interval_callable = callable(interval)

            if not is_interval_callable:
                if max_attempts:
                    logger.debug("Looping every %s seconds for %s attempts",
                                 interval, max_attempts)
                else:
                    logger.debug("Looping every %s seconds.", interval)

            # loop breaks explicitly for all possible exit conditions
            while True:
                i += 1
                result = f(i, *args, **kwargs)

                if result:
                    logger.debug("iteration %s. Desired state reached.", i)
                    break

                sleep = interval(i) if is_interval_callable else interval

                if max_attempts:
                    if i < max_attempts:
                        logger.debug(
                            "iteration %s. Sleeping for %ss. Still waiting...",
                            i, sleep)
                        time.sleep(sleep)
                    else:
                        logger.debug(
                            "iteration %s. Max attempts exhausted.", i)
                        break
                else:
                    # result False AND max_attempts is None means keep looping
                    # because None = infinite
                    logger.debug(
                        "XXiteration %s. Sleeping for %ss. Still waiting...XX",
                        i, sleep)
                    time.sleep(sleep)
            logger.debug("done")
            return result

        return sleep_looper

    return decorator

```
===== 118 =====
```
                     # result False AND max_attempts is None means keep looping
                     # because None = infinite
                     logger.debug(
-                        "iteration %s. Sleeping for %ss. Still waiting...",
+                        "iteration %s. sleeping for %ss. still waiting...",
                         i, sleep)
                     time.sleep(sleep)
             logger.debug("done")
@@ -83,4 +83,4 @@ 
         return sleep_looper
 
-    return decorator+    return decorator
```
```
def while_until_true(interval, max_attempts):
    """Execute a decorated function until it returns True.

    Executes wrapped function at every number of seconds specified by interval,
    until wrapped function either returns True or max_attempts are exhausted,
    whichever comes 1st.

    Interval is in seconds. It is either a simple float value, or a callable
    that returns a float value. If it is a callable, the passed callable will
    execute on every iteration. The callable signature is:
    func(n: int) -> float

    n is the iteration counter.

    The difference between while_until_true and wait_until_true is that the
    latter will always loop to a max_attempts, whereas while_until_true will
    keep going indefinitely.

    The other notable difference to wait_until_true is that the wrapped
    function signature must be:
    func(counter, *args, **kwargs)

    This is because this decorator injects the while loop counter into the
    invoked function.

    Args:
        interval (float or callable): In seconds. How long to wait between
            executing the wrapped function. The callable signature is func(n)
            where n is the iteration counter, and should return a float.
        max_attempts (int): Execute wrapped function up to this limit. None
                      means infinite (or until wrapped function returns True).
                      Passing anything <0 also means infinite.

    Returns:
        Bool. True if wrapped function returned True. False if reached
              max_attempts without the wrapped function ever returning True.
    """
    def decorator(f):
        logger.debug("started")

        def sleep_looper(*args, **kwargs):
            i = 0
            result = False
            is_interval_callable = callable(interval)

            if not is_interval_callable:
                if max_attempts:
                    logger.debug("Looping every %s seconds for %s attempts",
                                 interval, max_attempts)
                else:
                    logger.debug("Looping every %s seconds.", interval)

            # loop breaks explicitly for all possible exit conditions
            while True:
                i += 1
                result = f(i, *args, **kwargs)

                if result:
                    logger.debug("iteration %s. Desired state reached.", i)
                    break

                sleep = interval(i) if is_interval_callable else interval

                if max_attempts:
                    if i < max_attempts:
                        logger.debug(
                            "iteration %s. Sleeping for %ss. Still waiting...",
                            i, sleep)
                        time.sleep(sleep)
                    else:
                        logger.debug(
                            "iteration %s. Max attempts exhausted.", i)
                        break
                else:
                    # result False AND max_attempts is None means keep looping
                    # because None = infinite
                    logger.debug(
                        "iteration %s. sleeping for %ss. still waiting...",
                        i, sleep)
                    time.sleep(sleep)
            logger.debug("done")
            return result

        return sleep_looper

    return decorator

```
===== 119 =====
```
                     # result False AND max_attempts is None means keep looping
                     # because None = infinite
                     logger.debug(
-                        "iteration %s. Sleeping for %ss. Still waiting...",
+                        None,
                         i, sleep)
                     time.sleep(sleep)
             logger.debug("done")
@@ -83,4 +83,4 @@ 
         return sleep_looper
 
-    return decorator+    return decorator
```
```
def while_until_true(interval, max_attempts):
    """Execute a decorated function until it returns True.

    Executes wrapped function at every number of seconds specified by interval,
    until wrapped function either returns True or max_attempts are exhausted,
    whichever comes 1st.

    Interval is in seconds. It is either a simple float value, or a callable
    that returns a float value. If it is a callable, the passed callable will
    execute on every iteration. The callable signature is:
    func(n: int) -> float

    n is the iteration counter.

    The difference between while_until_true and wait_until_true is that the
    latter will always loop to a max_attempts, whereas while_until_true will
    keep going indefinitely.

    The other notable difference to wait_until_true is that the wrapped
    function signature must be:
    func(counter, *args, **kwargs)

    This is because this decorator injects the while loop counter into the
    invoked function.

    Args:
        interval (float or callable): In seconds. How long to wait between
            executing the wrapped function. The callable signature is func(n)
            where n is the iteration counter, and should return a float.
        max_attempts (int): Execute wrapped function up to this limit. None
                      means infinite (or until wrapped function returns True).
                      Passing anything <0 also means infinite.

    Returns:
        Bool. True if wrapped function returned True. False if reached
              max_attempts without the wrapped function ever returning True.
    """
    def decorator(f):
        logger.debug("started")

        def sleep_looper(*args, **kwargs):
            i = 0
            result = False
            is_interval_callable = callable(interval)

            if not is_interval_callable:
                if max_attempts:
                    logger.debug("Looping every %s seconds for %s attempts",
                                 interval, max_attempts)
                else:
                    logger.debug("Looping every %s seconds.", interval)

            # loop breaks explicitly for all possible exit conditions
            while True:
                i += 1
                result = f(i, *args, **kwargs)

                if result:
                    logger.debug("iteration %s. Desired state reached.", i)
                    break

                sleep = interval(i) if is_interval_callable else interval

                if max_attempts:
                    if i < max_attempts:
                        logger.debug(
                            "iteration %s. Sleeping for %ss. Still waiting...",
                            i, sleep)
                        time.sleep(sleep)
                    else:
                        logger.debug(
                            "iteration %s. Max attempts exhausted.", i)
                        break
                else:
                    # result False AND max_attempts is None means keep looping
                    # because None = infinite
                    logger.debug(
                        None,
                        i, sleep)
                    time.sleep(sleep)
            logger.debug("done")
            return result

        return sleep_looper

    return decorator

```
===== 120 =====
```
                     # result False AND max_attempts is None means keep looping
                     # because None = infinite
                     logger.debug(
-                        "iteration %s. Sleeping for %ss. Still waiting...",
                         i, sleep)
                     time.sleep(sleep)
             logger.debug("done")
@@ -83,4 +82,4 @@ 
         return sleep_looper
 
-    return decorator+    return decorator
```
```
def while_until_true(interval, max_attempts):
    """Execute a decorated function until it returns True.

    Executes wrapped function at every number of seconds specified by interval,
    until wrapped function either returns True or max_attempts are exhausted,
    whichever comes 1st.

    Interval is in seconds. It is either a simple float value, or a callable
    that returns a float value. If it is a callable, the passed callable will
    execute on every iteration. The callable signature is:
    func(n: int) -> float

    n is the iteration counter.

    The difference between while_until_true and wait_until_true is that the
    latter will always loop to a max_attempts, whereas while_until_true will
    keep going indefinitely.

    The other notable difference to wait_until_true is that the wrapped
    function signature must be:
    func(counter, *args, **kwargs)

    This is because this decorator injects the while loop counter into the
    invoked function.

    Args:
        interval (float or callable): In seconds. How long to wait between
            executing the wrapped function. The callable signature is func(n)
            where n is the iteration counter, and should return a float.
        max_attempts (int): Execute wrapped function up to this limit. None
                      means infinite (or until wrapped function returns True).
                      Passing anything <0 also means infinite.

    Returns:
        Bool. True if wrapped function returned True. False if reached
              max_attempts without the wrapped function ever returning True.
    """
    def decorator(f):
        logger.debug("started")

        def sleep_looper(*args, **kwargs):
            i = 0
            result = False
            is_interval_callable = callable(interval)

            if not is_interval_callable:
                if max_attempts:
                    logger.debug("Looping every %s seconds for %s attempts",
                                 interval, max_attempts)
                else:
                    logger.debug("Looping every %s seconds.", interval)

            # loop breaks explicitly for all possible exit conditions
            while True:
                i += 1
                result = f(i, *args, **kwargs)

                if result:
                    logger.debug("iteration %s. Desired state reached.", i)
                    break

                sleep = interval(i) if is_interval_callable else interval

                if max_attempts:
                    if i < max_attempts:
                        logger.debug(
                            "iteration %s. Sleeping for %ss. Still waiting...",
                            i, sleep)
                        time.sleep(sleep)
                    else:
                        logger.debug(
                            "iteration %s. Max attempts exhausted.", i)
                        break
                else:
                    # result False AND max_attempts is None means keep looping
                    # because None = infinite
                    logger.debug(
                        i, sleep)
                    time.sleep(sleep)
            logger.debug("done")
            return result

        return sleep_looper

    return decorator

```
===== 121 =====
```
                     # because None = infinite
                     logger.debug(
                         "iteration %s. Sleeping for %ss. Still waiting...",
-                        i, sleep)
+                        None, sleep)
                     time.sleep(sleep)
             logger.debug("done")
             return result
 
         return sleep_looper
 
-    return decorator+    return decorator
```
```
def while_until_true(interval, max_attempts):
    """Execute a decorated function until it returns True.

    Executes wrapped function at every number of seconds specified by interval,
    until wrapped function either returns True or max_attempts are exhausted,
    whichever comes 1st.

    Interval is in seconds. It is either a simple float value, or a callable
    that returns a float value. If it is a callable, the passed callable will
    execute on every iteration. The callable signature is:
    func(n: int) -> float

    n is the iteration counter.

    The difference between while_until_true and wait_until_true is that the
    latter will always loop to a max_attempts, whereas while_until_true will
    keep going indefinitely.

    The other notable difference to wait_until_true is that the wrapped
    function signature must be:
    func(counter, *args, **kwargs)

    This is because this decorator injects the while loop counter into the
    invoked function.

    Args:
        interval (float or callable): In seconds. How long to wait between
            executing the wrapped function. The callable signature is func(n)
            where n is the iteration counter, and should return a float.
        max_attempts (int): Execute wrapped function up to this limit. None
                      means infinite (or until wrapped function returns True).
                      Passing anything <0 also means infinite.

    Returns:
        Bool. True if wrapped function returned True. False if reached
              max_attempts without the wrapped function ever returning True.
    """
    def decorator(f):
        logger.debug("started")

        def sleep_looper(*args, **kwargs):
            i = 0
            result = False
            is_interval_callable = callable(interval)

            if not is_interval_callable:
                if max_attempts:
                    logger.debug("Looping every %s seconds for %s attempts",
                                 interval, max_attempts)
                else:
                    logger.debug("Looping every %s seconds.", interval)

            # loop breaks explicitly for all possible exit conditions
            while True:
                i += 1
                result = f(i, *args, **kwargs)

                if result:
                    logger.debug("iteration %s. Desired state reached.", i)
                    break

                sleep = interval(i) if is_interval_callable else interval

                if max_attempts:
                    if i < max_attempts:
                        logger.debug(
                            "iteration %s. Sleeping for %ss. Still waiting...",
                            i, sleep)
                        time.sleep(sleep)
                    else:
                        logger.debug(
                            "iteration %s. Max attempts exhausted.", i)
                        break
                else:
                    # result False AND max_attempts is None means keep looping
                    # because None = infinite
                    logger.debug(
                        "iteration %s. Sleeping for %ss. Still waiting...",
                        None, sleep)
                    time.sleep(sleep)
            logger.debug("done")
            return result

        return sleep_looper

    return decorator

```
===== 122 =====
```
                     # because None = infinite
                     logger.debug(
                         "iteration %s. Sleeping for %ss. Still waiting...",
-                        i, sleep)
+                        i + 1, sleep)
                     time.sleep(sleep)
             logger.debug("done")
             return result
```
```
def while_until_true(interval, max_attempts):
    """Execute a decorated function until it returns True.

    Executes wrapped function at every number of seconds specified by interval,
    until wrapped function either returns True or max_attempts are exhausted,
    whichever comes 1st.

    Interval is in seconds. It is either a simple float value, or a callable
    that returns a float value. If it is a callable, the passed callable will
    execute on every iteration. The callable signature is:
    func(n: int) -> float

    n is the iteration counter.

    The difference between while_until_true and wait_until_true is that the
    latter will always loop to a max_attempts, whereas while_until_true will
    keep going indefinitely.

    The other notable difference to wait_until_true is that the wrapped
    function signature must be:
    func(counter, *args, **kwargs)

    This is because this decorator injects the while loop counter into the
    invoked function.

    Args:
        interval (float or callable): In seconds. How long to wait between
            executing the wrapped function. The callable signature is func(n)
            where n is the iteration counter, and should return a float.
        max_attempts (int): Execute wrapped function up to this limit. None
                      means infinite (or until wrapped function returns True).
                      Passing anything <0 also means infinite.

    Returns:
        Bool. True if wrapped function returned True. False if reached
              max_attempts without the wrapped function ever returning True.
    """
    def decorator(f):
        logger.debug("started")

        def sleep_looper(*args, **kwargs):
            i = 0
            result = False
            is_interval_callable = callable(interval)

            if not is_interval_callable:
                if max_attempts:
                    logger.debug("Looping every %s seconds for %s attempts",
                                 interval, max_attempts)
                else:
                    logger.debug("Looping every %s seconds.", interval)

            # loop breaks explicitly for all possible exit conditions
            while True:
                i += 1
                result = f(i, *args, **kwargs)

                if result:
                    logger.debug("iteration %s. Desired state reached.", i)
                    break

                sleep = interval(i) if is_interval_callable else interval

                if max_attempts:
                    if i < max_attempts:
                        logger.debug(
                            "iteration %s. Sleeping for %ss. Still waiting...",
                            i, sleep)
                        time.sleep(sleep)
                    else:
                        logger.debug(
                            "iteration %s. Max attempts exhausted.", i)
                        break
                else:
                    # result False AND max_attempts is None means keep looping
                    # because None = infinite
                    logger.debug(
                        "iteration %s. Sleeping for %ss. Still waiting...",
                        i + 1, sleep)
                    time.sleep(sleep)
            logger.debug("done")
            return result

        return sleep_looper

    return decorator
```
===== 123 =====
```
                     # because None = infinite
                     logger.debug(
                         "iteration %s. Sleeping for %ss. Still waiting...",
-                        i, sleep)
+                        i - 1, sleep)
                     time.sleep(sleep)
             logger.debug("done")
             return result
```
```
def while_until_true(interval, max_attempts):
    """Execute a decorated function until it returns True.

    Executes wrapped function at every number of seconds specified by interval,
    until wrapped function either returns True or max_attempts are exhausted,
    whichever comes 1st.

    Interval is in seconds. It is either a simple float value, or a callable
    that returns a float value. If it is a callable, the passed callable will
    execute on every iteration. The callable signature is:
    func(n: int) -> float

    n is the iteration counter.

    The difference between while_until_true and wait_until_true is that the
    latter will always loop to a max_attempts, whereas while_until_true will
    keep going indefinitely.

    The other notable difference to wait_until_true is that the wrapped
    function signature must be:
    func(counter, *args, **kwargs)

    This is because this decorator injects the while loop counter into the
    invoked function.

    Args:
        interval (float or callable): In seconds. How long to wait between
            executing the wrapped function. The callable signature is func(n)
            where n is the iteration counter, and should return a float.
        max_attempts (int): Execute wrapped function up to this limit. None
                      means infinite (or until wrapped function returns True).
                      Passing anything <0 also means infinite.

    Returns:
        Bool. True if wrapped function returned True. False if reached
              max_attempts without the wrapped function ever returning True.
    """
    def decorator(f):
        logger.debug("started")

        def sleep_looper(*args, **kwargs):
            i = 0
            result = False
            is_interval_callable = callable(interval)

            if not is_interval_callable:
                if max_attempts:
                    logger.debug("Looping every %s seconds for %s attempts",
                                 interval, max_attempts)
                else:
                    logger.debug("Looping every %s seconds.", interval)

            # loop breaks explicitly for all possible exit conditions
            while True:
                i += 1
                result = f(i, *args, **kwargs)

                if result:
                    logger.debug("iteration %s. Desired state reached.", i)
                    break

                sleep = interval(i) if is_interval_callable else interval

                if max_attempts:
                    if i < max_attempts:
                        logger.debug(
                            "iteration %s. Sleeping for %ss. Still waiting...",
                            i, sleep)
                        time.sleep(sleep)
                    else:
                        logger.debug(
                            "iteration %s. Max attempts exhausted.", i)
                        break
                else:
                    # result False AND max_attempts is None means keep looping
                    # because None = infinite
                    logger.debug(
                        "iteration %s. Sleeping for %ss. Still waiting...",
                        i - 1, sleep)
                    time.sleep(sleep)
            logger.debug("done")
            return result

        return sleep_looper

    return decorator
```
===== 124 =====
```
                     # because None = infinite
                     logger.debug(
                         "iteration %s. Sleeping for %ss. Still waiting...",
-                        i, sleep)
+                        i, )
                     time.sleep(sleep)
             logger.debug("done")
             return result
 
         return sleep_looper
 
-    return decorator+    return decorator
```
```
def while_until_true(interval, max_attempts):
    """Execute a decorated function until it returns True.

    Executes wrapped function at every number of seconds specified by interval,
    until wrapped function either returns True or max_attempts are exhausted,
    whichever comes 1st.

    Interval is in seconds. It is either a simple float value, or a callable
    that returns a float value. If it is a callable, the passed callable will
    execute on every iteration. The callable signature is:
    func(n: int) -> float

    n is the iteration counter.

    The difference between while_until_true and wait_until_true is that the
    latter will always loop to a max_attempts, whereas while_until_true will
    keep going indefinitely.

    The other notable difference to wait_until_true is that the wrapped
    function signature must be:
    func(counter, *args, **kwargs)

    This is because this decorator injects the while loop counter into the
    invoked function.

    Args:
        interval (float or callable): In seconds. How long to wait between
            executing the wrapped function. The callable signature is func(n)
            where n is the iteration counter, and should return a float.
        max_attempts (int): Execute wrapped function up to this limit. None
                      means infinite (or until wrapped function returns True).
                      Passing anything <0 also means infinite.

    Returns:
        Bool. True if wrapped function returned True. False if reached
              max_attempts without the wrapped function ever returning True.
    """
    def decorator(f):
        logger.debug("started")

        def sleep_looper(*args, **kwargs):
            i = 0
            result = False
            is_interval_callable = callable(interval)

            if not is_interval_callable:
                if max_attempts:
                    logger.debug("Looping every %s seconds for %s attempts",
                                 interval, max_attempts)
                else:
                    logger.debug("Looping every %s seconds.", interval)

            # loop breaks explicitly for all possible exit conditions
            while True:
                i += 1
                result = f(i, *args, **kwargs)

                if result:
                    logger.debug("iteration %s. Desired state reached.", i)
                    break

                sleep = interval(i) if is_interval_callable else interval

                if max_attempts:
                    if i < max_attempts:
                        logger.debug(
                            "iteration %s. Sleeping for %ss. Still waiting...",
                            i, sleep)
                        time.sleep(sleep)
                    else:
                        logger.debug(
                            "iteration %s. Max attempts exhausted.", i)
                        break
                else:
                    # result False AND max_attempts is None means keep looping
                    # because None = infinite
                    logger.debug(
                        "iteration %s. Sleeping for %ss. Still waiting...",
                        i, )
                    time.sleep(sleep)
            logger.debug("done")
            return result

        return sleep_looper

    return decorator

```
===== 125 =====
```
                     # because None = infinite
                     logger.debug(
                         "iteration %s. Sleeping for %ss. Still waiting...",
-                        i, sleep)
+                        i, None)
                     time.sleep(sleep)
             logger.debug("done")
             return result
 
         return sleep_looper
 
-    return decorator+    return decorator
```
```
def while_until_true(interval, max_attempts):
    """Execute a decorated function until it returns True.

    Executes wrapped function at every number of seconds specified by interval,
    until wrapped function either returns True or max_attempts are exhausted,
    whichever comes 1st.

    Interval is in seconds. It is either a simple float value, or a callable
    that returns a float value. If it is a callable, the passed callable will
    execute on every iteration. The callable signature is:
    func(n: int) -> float

    n is the iteration counter.

    The difference between while_until_true and wait_until_true is that the
    latter will always loop to a max_attempts, whereas while_until_true will
    keep going indefinitely.

    The other notable difference to wait_until_true is that the wrapped
    function signature must be:
    func(counter, *args, **kwargs)

    This is because this decorator injects the while loop counter into the
    invoked function.

    Args:
        interval (float or callable): In seconds. How long to wait between
            executing the wrapped function. The callable signature is func(n)
            where n is the iteration counter, and should return a float.
        max_attempts (int): Execute wrapped function up to this limit. None
                      means infinite (or until wrapped function returns True).
                      Passing anything <0 also means infinite.

    Returns:
        Bool. True if wrapped function returned True. False if reached
              max_attempts without the wrapped function ever returning True.
    """
    def decorator(f):
        logger.debug("started")

        def sleep_looper(*args, **kwargs):
            i = 0
            result = False
            is_interval_callable = callable(interval)

            if not is_interval_callable:
                if max_attempts:
                    logger.debug("Looping every %s seconds for %s attempts",
                                 interval, max_attempts)
                else:
                    logger.debug("Looping every %s seconds.", interval)

            # loop breaks explicitly for all possible exit conditions
            while True:
                i += 1
                result = f(i, *args, **kwargs)

                if result:
                    logger.debug("iteration %s. Desired state reached.", i)
                    break

                sleep = interval(i) if is_interval_callable else interval

                if max_attempts:
                    if i < max_attempts:
                        logger.debug(
                            "iteration %s. Sleeping for %ss. Still waiting...",
                            i, sleep)
                        time.sleep(sleep)
                    else:
                        logger.debug(
                            "iteration %s. Max attempts exhausted.", i)
                        break
                else:
                    # result False AND max_attempts is None means keep looping
                    # because None = infinite
                    logger.debug(
                        "iteration %s. Sleeping for %ss. Still waiting...",
                        i, None)
                    time.sleep(sleep)
            logger.debug("done")
            return result

        return sleep_looper

    return decorator

```
===== 126 =====
```
                     # because None = infinite
                     logger.debug(
                         "iteration %s. Sleeping for %ss. Still waiting...",
-                        i, sleep)
+                        i, sleep * 2)
                     time.sleep(sleep)
             logger.debug("done")
             return result
```
```
def while_until_true(interval, max_attempts):
    """Execute a decorated function until it returns True.

    Executes wrapped function at every number of seconds specified by interval,
    until wrapped function either returns True or max_attempts are exhausted,
    whichever comes 1st.

    Interval is in seconds. It is either a simple float value, or a callable
    that returns a float value. If it is a callable, the passed callable will
    execute on every iteration. The callable signature is:
    func(n: int) -> float

    n is the iteration counter.

    The difference between while_until_true and wait_until_true is that the
    latter will always loop to a max_attempts, whereas while_until_true will
    keep going indefinitely.

    The other notable difference to wait_until_true is that the wrapped
    function signature must be:
    func(counter, *args, **kwargs)

    This is because this decorator injects the while loop counter into the
    invoked function.

    Args:
        interval (float or callable): In seconds. How long to wait between
            executing the wrapped function. The callable signature is func(n)
            where n is the iteration counter, and should return a float.
        max_attempts (int): Execute wrapped function up to this limit. None
                      means infinite (or until wrapped function returns True).
                      Passing anything <0 also means infinite.

    Returns:
        Bool. True if wrapped function returned True. False if reached
              max_attempts without the wrapped function ever returning True.
    """
    def decorator(f):
        logger.debug("started")

        def sleep_looper(*args, **kwargs):
            i = 0
            result = False
            is_interval_callable = callable(interval)

            if not is_interval_callable:
                if max_attempts:
                    logger.debug("Looping every %s seconds for %s attempts",
                                 interval, max_attempts)
                else:
                    logger.debug("Looping every %s seconds.", interval)

            # loop breaks explicitly for all possible exit conditions
            while True:
                i += 1
                result = f(i, *args, **kwargs)

                if result:
                    logger.debug("iteration %s. Desired state reached.", i)
                    break

                sleep = interval(i) if is_interval_callable else interval

                if max_attempts:
                    if i < max_attempts:
                        logger.debug(
                            "iteration %s. Sleeping for %ss. Still waiting...",
                            i, sleep)
                        time.sleep(sleep)
                    else:
                        logger.debug(
                            "iteration %s. Max attempts exhausted.", i)
                        break
                else:
                    # result False AND max_attempts is None means keep looping
                    # because None = infinite
                    logger.debug(
                        "iteration %s. Sleeping for %ss. Still waiting...",
                        i, sleep * 2)
                    time.sleep(sleep)
            logger.debug("done")
            return result

        return sleep_looper

    return decorator
```
===== 127 =====
```
                     # because None = infinite
                     logger.debug(
                         "iteration %s. Sleeping for %ss. Still waiting...",
-                        i, sleep)
+                        i, sleep + 1)
                     time.sleep(sleep)
             logger.debug("done")
             return result
```
```
def while_until_true(interval, max_attempts):
    """Execute a decorated function until it returns True.

    Executes wrapped function at every number of seconds specified by interval,
    until wrapped function either returns True or max_attempts are exhausted,
    whichever comes 1st.

    Interval is in seconds. It is either a simple float value, or a callable
    that returns a float value. If it is a callable, the passed callable will
    execute on every iteration. The callable signature is:
    func(n: int) -> float

    n is the iteration counter.

    The difference between while_until_true and wait_until_true is that the
    latter will always loop to a max_attempts, whereas while_until_true will
    keep going indefinitely.

    The other notable difference to wait_until_true is that the wrapped
    function signature must be:
    func(counter, *args, **kwargs)

    This is because this decorator injects the while loop counter into the
    invoked function.

    Args:
        interval (float or callable): In seconds. How long to wait between
            executing the wrapped function. The callable signature is func(n)
            where n is the iteration counter, and should return a float.
        max_attempts (int): Execute wrapped function up to this limit. None
                      means infinite (or until wrapped function returns True).
                      Passing anything <0 also means infinite.

    Returns:
        Bool. True if wrapped function returned True. False if reached
              max_attempts without the wrapped function ever returning True.
    """
    def decorator(f):
        logger.debug("started")

        def sleep_looper(*args, **kwargs):
            i = 0
            result = False
            is_interval_callable = callable(interval)

            if not is_interval_callable:
                if max_attempts:
                    logger.debug("Looping every %s seconds for %s attempts",
                                 interval, max_attempts)
                else:
                    logger.debug("Looping every %s seconds.", interval)

            # loop breaks explicitly for all possible exit conditions
            while True:
                i += 1
                result = f(i, *args, **kwargs)

                if result:
                    logger.debug("iteration %s. Desired state reached.", i)
                    break

                sleep = interval(i) if is_interval_callable else interval

                if max_attempts:
                    if i < max_attempts:
                        logger.debug(
                            "iteration %s. Sleeping for %ss. Still waiting...",
                            i, sleep)
                        time.sleep(sleep)
                    else:
                        logger.debug(
                            "iteration %s. Max attempts exhausted.", i)
                        break
                else:
                    # result False AND max_attempts is None means keep looping
                    # because None = infinite
                    logger.debug(
                        "iteration %s. Sleeping for %ss. Still waiting...",
                        i, sleep + 1)
                    time.sleep(sleep)
            logger.debug("done")
            return result

        return sleep_looper

    return decorator
```
===== 128 =====
```
                     # because None = infinite
                     logger.debug(
                         "iteration %s. Sleeping for %ss. Still waiting...",
-                        i, sleep)
+                        i, sleep / 2)
                     time.sleep(sleep)
             logger.debug("done")
             return result
```
```
def while_until_true(interval, max_attempts):
    """Execute a decorated function until it returns True.

    Executes wrapped function at every number of seconds specified by interval,
    until wrapped function either returns True or max_attempts are exhausted,
    whichever comes 1st.

    Interval is in seconds. It is either a simple float value, or a callable
    that returns a float value. If it is a callable, the passed callable will
    execute on every iteration. The callable signature is:
    func(n: int) -> float

    n is the iteration counter.

    The difference between while_until_true and wait_until_true is that the
    latter will always loop to a max_attempts, whereas while_until_true will
    keep going indefinitely.

    The other notable difference to wait_until_true is that the wrapped
    function signature must be:
    func(counter, *args, **kwargs)

    This is because this decorator injects the while loop counter into the
    invoked function.

    Args:
        interval (float or callable): In seconds. How long to wait between
            executing the wrapped function. The callable signature is func(n)
            where n is the iteration counter, and should return a float.
        max_attempts (int): Execute wrapped function up to this limit. None
                      means infinite (or until wrapped function returns True).
                      Passing anything <0 also means infinite.

    Returns:
        Bool. True if wrapped function returned True. False if reached
              max_attempts without the wrapped function ever returning True.
    """
    def decorator(f):
        logger.debug("started")

        def sleep_looper(*args, **kwargs):
            i = 0
            result = False
            is_interval_callable = callable(interval)

            if not is_interval_callable:
                if max_attempts:
                    logger.debug("Looping every %s seconds for %s attempts",
                                 interval, max_attempts)
                else:
                    logger.debug("Looping every %s seconds.", interval)

            # loop breaks explicitly for all possible exit conditions
            while True:
                i += 1
                result = f(i, *args, **kwargs)

                if result:
                    logger.debug("iteration %s. Desired state reached.", i)
                    break

                sleep = interval(i) if is_interval_callable else interval

                if max_attempts:
                    if i < max_attempts:
                        logger.debug(
                            "iteration %s. Sleeping for %ss. Still waiting...",
                            i, sleep)
                        time.sleep(sleep)
                    else:
                        logger.debug(
                            "iteration %s. Max attempts exhausted.", i)
                        break
                else:
                    # result False AND max_attempts is None means keep looping
                    # because None = infinite
                    logger.debug(
                        "iteration %s. Sleeping for %ss. Still waiting...",
                        i, sleep / 2)
                    time.sleep(sleep)
            logger.debug("done")
            return result

        return sleep_looper

    return decorator
```
===== 129 =====
```
                     # because None = infinite
                     logger.debug(
                         "iteration %s. Sleeping for %ss. Still waiting...",
-                        i, sleep)
+                        sleep)
                     time.sleep(sleep)
             logger.debug("done")
             return result
 
         return sleep_looper
 
-    return decorator+    return decorator
```
```
def while_until_true(interval, max_attempts):
    """Execute a decorated function until it returns True.

    Executes wrapped function at every number of seconds specified by interval,
    until wrapped function either returns True or max_attempts are exhausted,
    whichever comes 1st.

    Interval is in seconds. It is either a simple float value, or a callable
    that returns a float value. If it is a callable, the passed callable will
    execute on every iteration. The callable signature is:
    func(n: int) -> float

    n is the iteration counter.

    The difference between while_until_true and wait_until_true is that the
    latter will always loop to a max_attempts, whereas while_until_true will
    keep going indefinitely.

    The other notable difference to wait_until_true is that the wrapped
    function signature must be:
    func(counter, *args, **kwargs)

    This is because this decorator injects the while loop counter into the
    invoked function.

    Args:
        interval (float or callable): In seconds. How long to wait between
            executing the wrapped function. The callable signature is func(n)
            where n is the iteration counter, and should return a float.
        max_attempts (int): Execute wrapped function up to this limit. None
                      means infinite (or until wrapped function returns True).
                      Passing anything <0 also means infinite.

    Returns:
        Bool. True if wrapped function returned True. False if reached
              max_attempts without the wrapped function ever returning True.
    """
    def decorator(f):
        logger.debug("started")

        def sleep_looper(*args, **kwargs):
            i = 0
            result = False
            is_interval_callable = callable(interval)

            if not is_interval_callable:
                if max_attempts:
                    logger.debug("Looping every %s seconds for %s attempts",
                                 interval, max_attempts)
                else:
                    logger.debug("Looping every %s seconds.", interval)

            # loop breaks explicitly for all possible exit conditions
            while True:
                i += 1
                result = f(i, *args, **kwargs)

                if result:
                    logger.debug("iteration %s. Desired state reached.", i)
                    break

                sleep = interval(i) if is_interval_callable else interval

                if max_attempts:
                    if i < max_attempts:
                        logger.debug(
                            "iteration %s. Sleeping for %ss. Still waiting...",
                            i, sleep)
                        time.sleep(sleep)
                    else:
                        logger.debug(
                            "iteration %s. Max attempts exhausted.", i)
                        break
                else:
                    # result False AND max_attempts is None means keep looping
                    # because None = infinite
                    logger.debug(
                        "iteration %s. Sleeping for %ss. Still waiting...",
                        sleep)
                    time.sleep(sleep)
            logger.debug("done")
            return result

        return sleep_looper

    return decorator

```
===== 130 =====
```
                     logger.debug(
                         "iteration %s. Sleeping for %ss. Still waiting...",
                         i, sleep)
-                    time.sleep(sleep)
+                    time.sleep(0)  # Causes the loop to run continuously without any delay.
             logger.debug("done")
             return result
```
```
def while_until_true(interval, max_attempts):
    """Execute a decorated function until it returns True.

    Executes wrapped function at every number of seconds specified by interval,
    until wrapped function either returns True or max_attempts are exhausted,
    whichever comes 1st.

    Interval is in seconds. It is either a simple float value, or a callable
    that returns a float value. If it is a callable, the passed callable will
    execute on every iteration. The callable signature is:
    func(n: int) -> float

    n is the iteration counter.

    The difference between while_until_true and wait_until_true is that the
    latter will always loop to a max_attempts, whereas while_until_true will
    keep going indefinitely.

    The other notable difference to wait_until_true is that the wrapped
    function signature must be:
    func(counter, *args, **kwargs)

    This is because this decorator injects the while loop counter into the
    invoked function.

    Args:
        interval (float or callable): In seconds. How long to wait between
            executing the wrapped function. The callable signature is func(n)
            where n is the iteration counter, and should return a float.
        max_attempts (int): Execute wrapped function up to this limit. None
                      means infinite (or until wrapped function returns True).
                      Passing anything <0 also means infinite.

    Returns:
        Bool. True if wrapped function returned True. False if reached
              max_attempts without the wrapped function ever returning True.
    """
    def decorator(f):
        logger.debug("started")

        def sleep_looper(*args, **kwargs):
            i = 0
            result = False
            is_interval_callable = callable(interval)

            if not is_interval_callable:
                if max_attempts:
                    logger.debug("Looping every %s seconds for %s attempts",
                                 interval, max_attempts)
                else:
                    logger.debug("Looping every %s seconds.", interval)

            # loop breaks explicitly for all possible exit conditions
            while True:
                i += 1
                result = f(i, *args, **kwargs)

                if result:
                    logger.debug("iteration %s. Desired state reached.", i)
                    break

                sleep = interval(i) if is_interval_callable else interval

                if max_attempts:
                    if i < max_attempts:
                        logger.debug(
                            "iteration %s. Sleeping for %ss. Still waiting...",
                            i, sleep)
                        time.sleep(sleep)
                    else:
                        logger.debug(
                            "iteration %s. Max attempts exhausted.", i)
                        break
                else:
                    # result False AND max_attempts is None means keep looping
                    # because None = infinite
                    logger.debug(
                        "iteration %s. Sleeping for %ss. Still waiting...",
                        i, sleep)
                    time.sleep(0)  # Causes the loop to run continuously without any delay.
            logger.debug("done")
            return result

        return sleep_looper

    return decorator
```
===== 131 =====
```
                     logger.debug(
                         "iteration %s. Sleeping for %ss. Still waiting...",
                         i, sleep)
-                    time.sleep(sleep)
+                    time.sleep(None)
             logger.debug("done")
             return result
 
         return sleep_looper
 
-    return decorator+    return decorator
```
```
def while_until_true(interval, max_attempts):
    """Execute a decorated function until it returns True.

    Executes wrapped function at every number of seconds specified by interval,
    until wrapped function either returns True or max_attempts are exhausted,
    whichever comes 1st.

    Interval is in seconds. It is either a simple float value, or a callable
    that returns a float value. If it is a callable, the passed callable will
    execute on every iteration. The callable signature is:
    func(n: int) -> float

    n is the iteration counter.

    The difference between while_until_true and wait_until_true is that the
    latter will always loop to a max_attempts, whereas while_until_true will
    keep going indefinitely.

    The other notable difference to wait_until_true is that the wrapped
    function signature must be:
    func(counter, *args, **kwargs)

    This is because this decorator injects the while loop counter into the
    invoked function.

    Args:
        interval (float or callable): In seconds. How long to wait between
            executing the wrapped function. The callable signature is func(n)
            where n is the iteration counter, and should return a float.
        max_attempts (int): Execute wrapped function up to this limit. None
                      means infinite (or until wrapped function returns True).
                      Passing anything <0 also means infinite.

    Returns:
        Bool. True if wrapped function returned True. False if reached
              max_attempts without the wrapped function ever returning True.
    """
    def decorator(f):
        logger.debug("started")

        def sleep_looper(*args, **kwargs):
            i = 0
            result = False
            is_interval_callable = callable(interval)

            if not is_interval_callable:
                if max_attempts:
                    logger.debug("Looping every %s seconds for %s attempts",
                                 interval, max_attempts)
                else:
                    logger.debug("Looping every %s seconds.", interval)

            # loop breaks explicitly for all possible exit conditions
            while True:
                i += 1
                result = f(i, *args, **kwargs)

                if result:
                    logger.debug("iteration %s. Desired state reached.", i)
                    break

                sleep = interval(i) if is_interval_callable else interval

                if max_attempts:
                    if i < max_attempts:
                        logger.debug(
                            "iteration %s. Sleeping for %ss. Still waiting...",
                            i, sleep)
                        time.sleep(sleep)
                    else:
                        logger.debug(
                            "iteration %s. Max attempts exhausted.", i)
                        break
                else:
                    # result False AND max_attempts is None means keep looping
                    # because None = infinite
                    logger.debug(
                        "iteration %s. Sleeping for %ss. Still waiting...",
                        i, sleep)
                    time.sleep(None)
            logger.debug("done")
            return result

        return sleep_looper

    return decorator

```
===== 132 =====
```
                     logger.debug(
                         "iteration %s. Sleeping for %ss. Still waiting...",
                         i, sleep)
-                    time.sleep(sleep)
+                    time.sleep(sleep * 2)  # Introduces an unnecessary delay, causing longer wait times.
             logger.debug("done")
             return result
```
```
def while_until_true(interval, max_attempts):
    """Execute a decorated function until it returns True.

    Executes wrapped function at every number of seconds specified by interval,
    until wrapped function either returns True or max_attempts are exhausted,
    whichever comes 1st.

    Interval is in seconds. It is either a simple float value, or a callable
    that returns a float value. If it is a callable, the passed callable will
    execute on every iteration. The callable signature is:
    func(n: int) -> float

    n is the iteration counter.

    The difference between while_until_true and wait_until_true is that the
    latter will always loop to a max_attempts, whereas while_until_true will
    keep going indefinitely.

    The other notable difference to wait_until_true is that the wrapped
    function signature must be:
    func(counter, *args, **kwargs)

    This is because this decorator injects the while loop counter into the
    invoked function.

    Args:
        interval (float or callable): In seconds. How long to wait between
            executing the wrapped function. The callable signature is func(n)
            where n is the iteration counter, and should return a float.
        max_attempts (int): Execute wrapped function up to this limit. None
                      means infinite (or until wrapped function returns True).
                      Passing anything <0 also means infinite.

    Returns:
        Bool. True if wrapped function returned True. False if reached
              max_attempts without the wrapped function ever returning True.
    """
    def decorator(f):
        logger.debug("started")

        def sleep_looper(*args, **kwargs):
            i = 0
            result = False
            is_interval_callable = callable(interval)

            if not is_interval_callable:
                if max_attempts:
                    logger.debug("Looping every %s seconds for %s attempts",
                                 interval, max_attempts)
                else:
                    logger.debug("Looping every %s seconds.", interval)

            # loop breaks explicitly for all possible exit conditions
            while True:
                i += 1
                result = f(i, *args, **kwargs)

                if result:
                    logger.debug("iteration %s. Desired state reached.", i)
                    break

                sleep = interval(i) if is_interval_callable else interval

                if max_attempts:
                    if i < max_attempts:
                        logger.debug(
                            "iteration %s. Sleeping for %ss. Still waiting...",
                            i, sleep)
                        time.sleep(sleep)
                    else:
                        logger.debug(
                            "iteration %s. Max attempts exhausted.", i)
                        break
                else:
                    # result False AND max_attempts is None means keep looping
                    # because None = infinite
                    logger.debug(
                        "iteration %s. Sleeping for %ss. Still waiting...",
                        i, sleep)
                    time.sleep(sleep * 2)  # Introduces an unnecessary delay, causing longer wait times.
            logger.debug("done")
            return result

        return sleep_looper

    return decorator
```
===== 133 =====
```
                     logger.debug(
                         "iteration %s. Sleeping for %ss. Still waiting...",
                         i, sleep)
-                    time.sleep(sleep)
+                    time.sleep(sleep + 1)  # Adds an extra second to the sleep time, causing longer wait times.
             logger.debug("done")
             return result
```
```
def while_until_true(interval, max_attempts):
    """Execute a decorated function until it returns True.

    Executes wrapped function at every number of seconds specified by interval,
    until wrapped function either returns True or max_attempts are exhausted,
    whichever comes 1st.

    Interval is in seconds. It is either a simple float value, or a callable
    that returns a float value. If it is a callable, the passed callable will
    execute on every iteration. The callable signature is:
    func(n: int) -> float

    n is the iteration counter.

    The difference between while_until_true and wait_until_true is that the
    latter will always loop to a max_attempts, whereas while_until_true will
    keep going indefinitely.

    The other notable difference to wait_until_true is that the wrapped
    function signature must be:
    func(counter, *args, **kwargs)

    This is because this decorator injects the while loop counter into the
    invoked function.

    Args:
        interval (float or callable): In seconds. How long to wait between
            executing the wrapped function. The callable signature is func(n)
            where n is the iteration counter, and should return a float.
        max_attempts (int): Execute wrapped function up to this limit. None
                      means infinite (or until wrapped function returns True).
                      Passing anything <0 also means infinite.

    Returns:
        Bool. True if wrapped function returned True. False if reached
              max_attempts without the wrapped function ever returning True.
    """
    def decorator(f):
        logger.debug("started")

        def sleep_looper(*args, **kwargs):
            i = 0
            result = False
            is_interval_callable = callable(interval)

            if not is_interval_callable:
                if max_attempts:
                    logger.debug("Looping every %s seconds for %s attempts",
                                 interval, max_attempts)
                else:
                    logger.debug("Looping every %s seconds.", interval)

            # loop breaks explicitly for all possible exit conditions
            while True:
                i += 1
                result = f(i, *args, **kwargs)

                if result:
                    logger.debug("iteration %s. Desired state reached.", i)
                    break

                sleep = interval(i) if is_interval_callable else interval

                if max_attempts:
                    if i < max_attempts:
                        logger.debug(
                            "iteration %s. Sleeping for %ss. Still waiting...",
                            i, sleep)
                        time.sleep(sleep)
                    else:
                        logger.debug(
                            "iteration %s. Max attempts exhausted.", i)
                        break
                else:
                    # result False AND max_attempts is None means keep looping
                    # because None = infinite
                    logger.debug(
                        "iteration %s. Sleeping for %ss. Still waiting...",
                        i, sleep)
                    time.sleep(sleep + 1)  # Adds an extra second to the sleep time, causing longer wait times.
            logger.debug("done")
            return result

        return sleep_looper

    return decorator
```
===== 134 =====
```
                     logger.debug(
                         "iteration %s. Sleeping for %ss. Still waiting...",
                         i, sleep)
-                    time.sleep(sleep)
+                    time.sleep(sleep - 1)  # Decreases the sleep time, which may lead to excessive function calls.
             logger.debug("done")
             return result
```
```
def while_until_true(interval, max_attempts):
    """Execute a decorated function until it returns True.

    Executes wrapped function at every number of seconds specified by interval,
    until wrapped function either returns True or max_attempts are exhausted,
    whichever comes 1st.

    Interval is in seconds. It is either a simple float value, or a callable
    that returns a float value. If it is a callable, the passed callable will
    execute on every iteration. The callable signature is:
    func(n: int) -> float

    n is the iteration counter.

    The difference between while_until_true and wait_until_true is that the
    latter will always loop to a max_attempts, whereas while_until_true will
    keep going indefinitely.

    The other notable difference to wait_until_true is that the wrapped
    function signature must be:
    func(counter, *args, **kwargs)

    This is because this decorator injects the while loop counter into the
    invoked function.

    Args:
        interval (float or callable): In seconds. How long to wait between
            executing the wrapped function. The callable signature is func(n)
            where n is the iteration counter, and should return a float.
        max_attempts (int): Execute wrapped function up to this limit. None
                      means infinite (or until wrapped function returns True).
                      Passing anything <0 also means infinite.

    Returns:
        Bool. True if wrapped function returned True. False if reached
              max_attempts without the wrapped function ever returning True.
    """
    def decorator(f):
        logger.debug("started")

        def sleep_looper(*args, **kwargs):
            i = 0
            result = False
            is_interval_callable = callable(interval)

            if not is_interval_callable:
                if max_attempts:
                    logger.debug("Looping every %s seconds for %s attempts",
                                 interval, max_attempts)
                else:
                    logger.debug("Looping every %s seconds.", interval)

            # loop breaks explicitly for all possible exit conditions
            while True:
                i += 1
                result = f(i, *args, **kwargs)

                if result:
                    logger.debug("iteration %s. Desired state reached.", i)
                    break

                sleep = interval(i) if is_interval_callable else interval

                if max_attempts:
                    if i < max_attempts:
                        logger.debug(
                            "iteration %s. Sleeping for %ss. Still waiting...",
                            i, sleep)
                        time.sleep(sleep)
                    else:
                        logger.debug(
                            "iteration %s. Max attempts exhausted.", i)
                        break
                else:
                    # result False AND max_attempts is None means keep looping
                    # because None = infinite
                    logger.debug(
                        "iteration %s. Sleeping for %ss. Still waiting...",
                        i, sleep)
                    time.sleep(sleep - 1)  # Decreases the sleep time, which may lead to excessive function calls.
            logger.debug("done")
            return result

        return sleep_looper

    return decorator
```
===== 135 =====
```
                     logger.debug(
                         "iteration %s. Sleeping for %ss. Still waiting...",
                         i, sleep)
-                    time.sleep(sleep)
+                    time.sleep(sleep / 2)  # Reduces the sleep time, potentially causing too many rapid calls.
             logger.debug("done")
             return result
```
```
def while_until_true(interval, max_attempts):
    """Execute a decorated function until it returns True.

    Executes wrapped function at every number of seconds specified by interval,
    until wrapped function either returns True or max_attempts are exhausted,
    whichever comes 1st.

    Interval is in seconds. It is either a simple float value, or a callable
    that returns a float value. If it is a callable, the passed callable will
    execute on every iteration. The callable signature is:
    func(n: int) -> float

    n is the iteration counter.

    The difference between while_until_true and wait_until_true is that the
    latter will always loop to a max_attempts, whereas while_until_true will
    keep going indefinitely.

    The other notable difference to wait_until_true is that the wrapped
    function signature must be:
    func(counter, *args, **kwargs)

    This is because this decorator injects the while loop counter into the
    invoked function.

    Args:
        interval (float or callable): In seconds. How long to wait between
            executing the wrapped function. The callable signature is func(n)
            where n is the iteration counter, and should return a float.
        max_attempts (int): Execute wrapped function up to this limit. None
                      means infinite (or until wrapped function returns True).
                      Passing anything <0 also means infinite.

    Returns:
        Bool. True if wrapped function returned True. False if reached
              max_attempts without the wrapped function ever returning True.
    """
    def decorator(f):
        logger.debug("started")

        def sleep_looper(*args, **kwargs):
            i = 0
            result = False
            is_interval_callable = callable(interval)

            if not is_interval_callable:
                if max_attempts:
                    logger.debug("Looping every %s seconds for %s attempts",
                                 interval, max_attempts)
                else:
                    logger.debug("Looping every %s seconds.", interval)

            # loop breaks explicitly for all possible exit conditions
            while True:
                i += 1
                result = f(i, *args, **kwargs)

                if result:
                    logger.debug("iteration %s. Desired state reached.", i)
                    break

                sleep = interval(i) if is_interval_callable else interval

                if max_attempts:
                    if i < max_attempts:
                        logger.debug(
                            "iteration %s. Sleeping for %ss. Still waiting...",
                            i, sleep)
                        time.sleep(sleep)
                    else:
                        logger.debug(
                            "iteration %s. Max attempts exhausted.", i)
                        break
                else:
                    # result False AND max_attempts is None means keep looping
                    # because None = infinite
                    logger.debug(
                        "iteration %s. Sleeping for %ss. Still waiting...",
                        i, sleep)
                    time.sleep(sleep / 2)  # Reduces the sleep time, potentially causing too many rapid calls.
            logger.debug("done")
            return result

        return sleep_looper

    return decorator
```
===== 136 =====
```
                         "iteration %s. Sleeping for %ss. Still waiting...",
                         i, sleep)
                     time.sleep(sleep)
-            logger.debug("done")
+            logger.debug("DONE")
             return result
 
         return sleep_looper
 
-    return decorator+    return decorator
```
```
def while_until_true(interval, max_attempts):
    """Execute a decorated function until it returns True.

    Executes wrapped function at every number of seconds specified by interval,
    until wrapped function either returns True or max_attempts are exhausted,
    whichever comes 1st.

    Interval is in seconds. It is either a simple float value, or a callable
    that returns a float value. If it is a callable, the passed callable will
    execute on every iteration. The callable signature is:
    func(n: int) -> float

    n is the iteration counter.

    The difference between while_until_true and wait_until_true is that the
    latter will always loop to a max_attempts, whereas while_until_true will
    keep going indefinitely.

    The other notable difference to wait_until_true is that the wrapped
    function signature must be:
    func(counter, *args, **kwargs)

    This is because this decorator injects the while loop counter into the
    invoked function.

    Args:
        interval (float or callable): In seconds. How long to wait between
            executing the wrapped function. The callable signature is func(n)
            where n is the iteration counter, and should return a float.
        max_attempts (int): Execute wrapped function up to this limit. None
                      means infinite (or until wrapped function returns True).
                      Passing anything <0 also means infinite.

    Returns:
        Bool. True if wrapped function returned True. False if reached
              max_attempts without the wrapped function ever returning True.
    """
    def decorator(f):
        logger.debug("started")

        def sleep_looper(*args, **kwargs):
            i = 0
            result = False
            is_interval_callable = callable(interval)

            if not is_interval_callable:
                if max_attempts:
                    logger.debug("Looping every %s seconds for %s attempts",
                                 interval, max_attempts)
                else:
                    logger.debug("Looping every %s seconds.", interval)

            # loop breaks explicitly for all possible exit conditions
            while True:
                i += 1
                result = f(i, *args, **kwargs)

                if result:
                    logger.debug("iteration %s. Desired state reached.", i)
                    break

                sleep = interval(i) if is_interval_callable else interval

                if max_attempts:
                    if i < max_attempts:
                        logger.debug(
                            "iteration %s. Sleeping for %ss. Still waiting...",
                            i, sleep)
                        time.sleep(sleep)
                    else:
                        logger.debug(
                            "iteration %s. Max attempts exhausted.", i)
                        break
                else:
                    # result False AND max_attempts is None means keep looping
                    # because None = infinite
                    logger.debug(
                        "iteration %s. Sleeping for %ss. Still waiting...",
                        i, sleep)
                    time.sleep(sleep)
            logger.debug("DONE")
            return result

        return sleep_looper

    return decorator

```
===== 137 =====
```
                         "iteration %s. Sleeping for %ss. Still waiting...",
                         i, sleep)
                     time.sleep(sleep)
-            logger.debug("done")
+            logger.debug("XXdoneXX")
             return result
 
         return sleep_looper
 
-    return decorator+    return decorator
```
```
def while_until_true(interval, max_attempts):
    """Execute a decorated function until it returns True.

    Executes wrapped function at every number of seconds specified by interval,
    until wrapped function either returns True or max_attempts are exhausted,
    whichever comes 1st.

    Interval is in seconds. It is either a simple float value, or a callable
    that returns a float value. If it is a callable, the passed callable will
    execute on every iteration. The callable signature is:
    func(n: int) -> float

    n is the iteration counter.

    The difference between while_until_true and wait_until_true is that the
    latter will always loop to a max_attempts, whereas while_until_true will
    keep going indefinitely.

    The other notable difference to wait_until_true is that the wrapped
    function signature must be:
    func(counter, *args, **kwargs)

    This is because this decorator injects the while loop counter into the
    invoked function.

    Args:
        interval (float or callable): In seconds. How long to wait between
            executing the wrapped function. The callable signature is func(n)
            where n is the iteration counter, and should return a float.
        max_attempts (int): Execute wrapped function up to this limit. None
                      means infinite (or until wrapped function returns True).
                      Passing anything <0 also means infinite.

    Returns:
        Bool. True if wrapped function returned True. False if reached
              max_attempts without the wrapped function ever returning True.
    """
    def decorator(f):
        logger.debug("started")

        def sleep_looper(*args, **kwargs):
            i = 0
            result = False
            is_interval_callable = callable(interval)

            if not is_interval_callable:
                if max_attempts:
                    logger.debug("Looping every %s seconds for %s attempts",
                                 interval, max_attempts)
                else:
                    logger.debug("Looping every %s seconds.", interval)

            # loop breaks explicitly for all possible exit conditions
            while True:
                i += 1
                result = f(i, *args, **kwargs)

                if result:
                    logger.debug("iteration %s. Desired state reached.", i)
                    break

                sleep = interval(i) if is_interval_callable else interval

                if max_attempts:
                    if i < max_attempts:
                        logger.debug(
                            "iteration %s. Sleeping for %ss. Still waiting...",
                            i, sleep)
                        time.sleep(sleep)
                    else:
                        logger.debug(
                            "iteration %s. Max attempts exhausted.", i)
                        break
                else:
                    # result False AND max_attempts is None means keep looping
                    # because None = infinite
                    logger.debug(
                        "iteration %s. Sleeping for %ss. Still waiting...",
                        i, sleep)
                    time.sleep(sleep)
            logger.debug("XXdoneXX")
            return result

        return sleep_looper

    return decorator

```
===== 138 =====
```
                         "iteration %s. Sleeping for %ss. Still waiting...",
                         i, sleep)
                     time.sleep(sleep)
-            logger.debug("done")
+            logger.debug("exiting loop")
             return result
 
         return sleep_looper
```
```
def while_until_true(interval, max_attempts):
    """Execute a decorated function until it returns True.

    Executes wrapped function at every number of seconds specified by interval,
    until wrapped function either returns True or max_attempts are exhausted,
    whichever comes 1st.

    Interval is in seconds. It is either a simple float value, or a callable
    that returns a float value. If it is a callable, the passed callable will
    execute on every iteration. The callable signature is:
    func(n: int) -> float

    n is the iteration counter.

    The difference between while_until_true and wait_until_true is that the
    latter will always loop to a max_attempts, whereas while_until_true will
    keep going indefinitely.

    The other notable difference to wait_until_true is that the wrapped
    function signature must be:
    func(counter, *args, **kwargs)

    This is because this decorator injects the while loop counter into the
    invoked function.

    Args:
        interval (float or callable): In seconds. How long to wait between
            executing the wrapped function. The callable signature is func(n)
            where n is the iteration counter, and should return a float.
        max_attempts (int): Execute wrapped function up to this limit. None
                      means infinite (or until wrapped function returns True).
                      Passing anything <0 also means infinite.

    Returns:
        Bool. True if wrapped function returned True. False if reached
              max_attempts without the wrapped function ever returning True.
    """
    def decorator(f):
        logger.debug("started")

        def sleep_looper(*args, **kwargs):
            i = 0
            result = False
            is_interval_callable = callable(interval)

            if not is_interval_callable:
                if max_attempts:
                    logger.debug("Looping every %s seconds for %s attempts",
                                 interval, max_attempts)
                else:
                    logger.debug("Looping every %s seconds.", interval)

            # loop breaks explicitly for all possible exit conditions
            while True:
                i += 1
                result = f(i, *args, **kwargs)

                if result:
                    logger.debug("iteration %s. Desired state reached.", i)
                    break

                sleep = interval(i) if is_interval_callable else interval

                if max_attempts:
                    if i < max_attempts:
                        logger.debug(
                            "iteration %s. Sleeping for %ss. Still waiting...",
                            i, sleep)
                        time.sleep(sleep)
                    else:
                        logger.debug(
                            "iteration %s. Max attempts exhausted.", i)
                        break
                else:
                    # result False AND max_attempts is None means keep looping
                    # because None = infinite
                    logger.debug(
                        "iteration %s. Sleeping for %ss. Still waiting...",
                        i, sleep)
                    time.sleep(sleep)
            logger.debug("exiting loop")
            return result

        return sleep_looper

    return decorator
```
===== 139 =====
```
                         "iteration %s. Sleeping for %ss. Still waiting...",
                         i, sleep)
                     time.sleep(sleep)
-            logger.debug("done")
+            logger.debug("iteration %s completed", i)
             return result
 
         return sleep_looper
```
```
def while_until_true(interval, max_attempts):
    """Execute a decorated function until it returns True.

    Executes wrapped function at every number of seconds specified by interval,
    until wrapped function either returns True or max_attempts are exhausted,
    whichever comes 1st.

    Interval is in seconds. It is either a simple float value, or a callable
    that returns a float value. If it is a callable, the passed callable will
    execute on every iteration. The callable signature is:
    func(n: int) -> float

    n is the iteration counter.

    The difference between while_until_true and wait_until_true is that the
    latter will always loop to a max_attempts, whereas while_until_true will
    keep going indefinitely.

    The other notable difference to wait_until_true is that the wrapped
    function signature must be:
    func(counter, *args, **kwargs)

    This is because this decorator injects the while loop counter into the
    invoked function.

    Args:
        interval (float or callable): In seconds. How long to wait between
            executing the wrapped function. The callable signature is func(n)
            where n is the iteration counter, and should return a float.
        max_attempts (int): Execute wrapped function up to this limit. None
                      means infinite (or until wrapped function returns True).
                      Passing anything <0 also means infinite.

    Returns:
        Bool. True if wrapped function returned True. False if reached
              max_attempts without the wrapped function ever returning True.
    """
    def decorator(f):
        logger.debug("started")

        def sleep_looper(*args, **kwargs):
            i = 0
            result = False
            is_interval_callable = callable(interval)

            if not is_interval_callable:
                if max_attempts:
                    logger.debug("Looping every %s seconds for %s attempts",
                                 interval, max_attempts)
                else:
                    logger.debug("Looping every %s seconds.", interval)

            # loop breaks explicitly for all possible exit conditions
            while True:
                i += 1
                result = f(i, *args, **kwargs)

                if result:
                    logger.debug("iteration %s. Desired state reached.", i)
                    break

                sleep = interval(i) if is_interval_callable else interval

                if max_attempts:
                    if i < max_attempts:
                        logger.debug(
                            "iteration %s. Sleeping for %ss. Still waiting...",
                            i, sleep)
                        time.sleep(sleep)
                    else:
                        logger.debug(
                            "iteration %s. Max attempts exhausted.", i)
                        break
                else:
                    # result False AND max_attempts is None means keep looping
                    # because None = infinite
                    logger.debug(
                        "iteration %s. Sleeping for %ss. Still waiting...",
                        i, sleep)
                    time.sleep(sleep)
            logger.debug("iteration %s completed", i)
            return result

        return sleep_looper

    return decorator
```
===== 140 =====
```
                         "iteration %s. Sleeping for %ss. Still waiting...",
                         i, sleep)
                     time.sleep(sleep)
-            logger.debug("done")
+            logger.debug(None)
             return result
 
         return sleep_looper
 
-    return decorator+    return decorator
```
```
def while_until_true(interval, max_attempts):
    """Execute a decorated function until it returns True.

    Executes wrapped function at every number of seconds specified by interval,
    until wrapped function either returns True or max_attempts are exhausted,
    whichever comes 1st.

    Interval is in seconds. It is either a simple float value, or a callable
    that returns a float value. If it is a callable, the passed callable will
    execute on every iteration. The callable signature is:
    func(n: int) -> float

    n is the iteration counter.

    The difference between while_until_true and wait_until_true is that the
    latter will always loop to a max_attempts, whereas while_until_true will
    keep going indefinitely.

    The other notable difference to wait_until_true is that the wrapped
    function signature must be:
    func(counter, *args, **kwargs)

    This is because this decorator injects the while loop counter into the
    invoked function.

    Args:
        interval (float or callable): In seconds. How long to wait between
            executing the wrapped function. The callable signature is func(n)
            where n is the iteration counter, and should return a float.
        max_attempts (int): Execute wrapped function up to this limit. None
                      means infinite (or until wrapped function returns True).
                      Passing anything <0 also means infinite.

    Returns:
        Bool. True if wrapped function returned True. False if reached
              max_attempts without the wrapped function ever returning True.
    """
    def decorator(f):
        logger.debug("started")

        def sleep_looper(*args, **kwargs):
            i = 0
            result = False
            is_interval_callable = callable(interval)

            if not is_interval_callable:
                if max_attempts:
                    logger.debug("Looping every %s seconds for %s attempts",
                                 interval, max_attempts)
                else:
                    logger.debug("Looping every %s seconds.", interval)

            # loop breaks explicitly for all possible exit conditions
            while True:
                i += 1
                result = f(i, *args, **kwargs)

                if result:
                    logger.debug("iteration %s. Desired state reached.", i)
                    break

                sleep = interval(i) if is_interval_callable else interval

                if max_attempts:
                    if i < max_attempts:
                        logger.debug(
                            "iteration %s. Sleeping for %ss. Still waiting...",
                            i, sleep)
                        time.sleep(sleep)
                    else:
                        logger.debug(
                            "iteration %s. Max attempts exhausted.", i)
                        break
                else:
                    # result False AND max_attempts is None means keep looping
                    # because None = infinite
                    logger.debug(
                        "iteration %s. Sleeping for %ss. Still waiting...",
                        i, sleep)
                    time.sleep(sleep)
            logger.debug(None)
            return result

        return sleep_looper

    return decorator

```
===== 141 =====
```
                         "iteration %s. Sleeping for %ss. Still waiting...",
                         i, sleep)
                     time.sleep(sleep)
-            logger.debug("done")
+            logger.error("final state reached")
             return result
 
         return sleep_looper
```
```
def while_until_true(interval, max_attempts):
    """Execute a decorated function until it returns True.

    Executes wrapped function at every number of seconds specified by interval,
    until wrapped function either returns True or max_attempts are exhausted,
    whichever comes 1st.

    Interval is in seconds. It is either a simple float value, or a callable
    that returns a float value. If it is a callable, the passed callable will
    execute on every iteration. The callable signature is:
    func(n: int) -> float

    n is the iteration counter.

    The difference between while_until_true and wait_until_true is that the
    latter will always loop to a max_attempts, whereas while_until_true will
    keep going indefinitely.

    The other notable difference to wait_until_true is that the wrapped
    function signature must be:
    func(counter, *args, **kwargs)

    This is because this decorator injects the while loop counter into the
    invoked function.

    Args:
        interval (float or callable): In seconds. How long to wait between
            executing the wrapped function. The callable signature is func(n)
            where n is the iteration counter, and should return a float.
        max_attempts (int): Execute wrapped function up to this limit. None
                      means infinite (or until wrapped function returns True).
                      Passing anything <0 also means infinite.

    Returns:
        Bool. True if wrapped function returned True. False if reached
              max_attempts without the wrapped function ever returning True.
    """
    def decorator(f):
        logger.debug("started")

        def sleep_looper(*args, **kwargs):
            i = 0
            result = False
            is_interval_callable = callable(interval)

            if not is_interval_callable:
                if max_attempts:
                    logger.debug("Looping every %s seconds for %s attempts",
                                 interval, max_attempts)
                else:
                    logger.debug("Looping every %s seconds.", interval)

            # loop breaks explicitly for all possible exit conditions
            while True:
                i += 1
                result = f(i, *args, **kwargs)

                if result:
                    logger.debug("iteration %s. Desired state reached.", i)
                    break

                sleep = interval(i) if is_interval_callable else interval

                if max_attempts:
                    if i < max_attempts:
                        logger.debug(
                            "iteration %s. Sleeping for %ss. Still waiting...",
                            i, sleep)
                        time.sleep(sleep)
                    else:
                        logger.debug(
                            "iteration %s. Max attempts exhausted.", i)
                        break
                else:
                    # result False AND max_attempts is None means keep looping
                    # because None = infinite
                    logger.debug(
                        "iteration %s. Sleeping for %ss. Still waiting...",
                        i, sleep)
                    time.sleep(sleep)
            logger.error("final state reached")
            return result

        return sleep_looper

    return decorator
```
===== 142 =====
```
                         "iteration %s. Sleeping for %ss. Still waiting...",
                         i, sleep)
                     time.sleep(sleep)
-            logger.debug("done")
+            logger.info("finished execution")
             return result
 
         return sleep_looper
```
```
def while_until_true(interval, max_attempts):
    """Execute a decorated function until it returns True.

    Executes wrapped function at every number of seconds specified by interval,
    until wrapped function either returns True or max_attempts are exhausted,
    whichever comes 1st.

    Interval is in seconds. It is either a simple float value, or a callable
    that returns a float value. If it is a callable, the passed callable will
    execute on every iteration. The callable signature is:
    func(n: int) -> float

    n is the iteration counter.

    The difference between while_until_true and wait_until_true is that the
    latter will always loop to a max_attempts, whereas while_until_true will
    keep going indefinitely.

    The other notable difference to wait_until_true is that the wrapped
    function signature must be:
    func(counter, *args, **kwargs)

    This is because this decorator injects the while loop counter into the
    invoked function.

    Args:
        interval (float or callable): In seconds. How long to wait between
            executing the wrapped function. The callable signature is func(n)
            where n is the iteration counter, and should return a float.
        max_attempts (int): Execute wrapped function up to this limit. None
                      means infinite (or until wrapped function returns True).
                      Passing anything <0 also means infinite.

    Returns:
        Bool. True if wrapped function returned True. False if reached
              max_attempts without the wrapped function ever returning True.
    """
    def decorator(f):
        logger.debug("started")

        def sleep_looper(*args, **kwargs):
            i = 0
            result = False
            is_interval_callable = callable(interval)

            if not is_interval_callable:
                if max_attempts:
                    logger.debug("Looping every %s seconds for %s attempts",
                                 interval, max_attempts)
                else:
                    logger.debug("Looping every %s seconds.", interval)

            # loop breaks explicitly for all possible exit conditions
            while True:
                i += 1
                result = f(i, *args, **kwargs)

                if result:
                    logger.debug("iteration %s. Desired state reached.", i)
                    break

                sleep = interval(i) if is_interval_callable else interval

                if max_attempts:
                    if i < max_attempts:
                        logger.debug(
                            "iteration %s. Sleeping for %ss. Still waiting...",
                            i, sleep)
                        time.sleep(sleep)
                    else:
                        logger.debug(
                            "iteration %s. Max attempts exhausted.", i)
                        break
                else:
                    # result False AND max_attempts is None means keep looping
                    # because None = infinite
                    logger.debug(
                        "iteration %s. Sleeping for %ss. Still waiting...",
                        i, sleep)
                    time.sleep(sleep)
            logger.info("finished execution")
            return result

        return sleep_looper

    return decorator
```
===== 143 =====
```
                         "iteration %s. Sleeping for %ss. Still waiting...",
                         i, sleep)
                     time.sleep(sleep)
-            logger.debug("done")
+            logger.warning("loop terminated")
             return result
 
         return sleep_looper
```
```
def while_until_true(interval, max_attempts):
    """Execute a decorated function until it returns True.

    Executes wrapped function at every number of seconds specified by interval,
    until wrapped function either returns True or max_attempts are exhausted,
    whichever comes 1st.

    Interval is in seconds. It is either a simple float value, or a callable
    that returns a float value. If it is a callable, the passed callable will
    execute on every iteration. The callable signature is:
    func(n: int) -> float

    n is the iteration counter.

    The difference between while_until_true and wait_until_true is that the
    latter will always loop to a max_attempts, whereas while_until_true will
    keep going indefinitely.

    The other notable difference to wait_until_true is that the wrapped
    function signature must be:
    func(counter, *args, **kwargs)

    This is because this decorator injects the while loop counter into the
    invoked function.

    Args:
        interval (float or callable): In seconds. How long to wait between
            executing the wrapped function. The callable signature is func(n)
            where n is the iteration counter, and should return a float.
        max_attempts (int): Execute wrapped function up to this limit. None
                      means infinite (or until wrapped function returns True).
                      Passing anything <0 also means infinite.

    Returns:
        Bool. True if wrapped function returned True. False if reached
              max_attempts without the wrapped function ever returning True.
    """
    def decorator(f):
        logger.debug("started")

        def sleep_looper(*args, **kwargs):
            i = 0
            result = False
            is_interval_callable = callable(interval)

            if not is_interval_callable:
                if max_attempts:
                    logger.debug("Looping every %s seconds for %s attempts",
                                 interval, max_attempts)
                else:
                    logger.debug("Looping every %s seconds.", interval)

            # loop breaks explicitly for all possible exit conditions
            while True:
                i += 1
                result = f(i, *args, **kwargs)

                if result:
                    logger.debug("iteration %s. Desired state reached.", i)
                    break

                sleep = interval(i) if is_interval_callable else interval

                if max_attempts:
                    if i < max_attempts:
                        logger.debug(
                            "iteration %s. Sleeping for %ss. Still waiting...",
                            i, sleep)
                        time.sleep(sleep)
                    else:
                        logger.debug(
                            "iteration %s. Max attempts exhausted.", i)
                        break
                else:
                    # result False AND max_attempts is None means keep looping
                    # because None = infinite
                    logger.debug(
                        "iteration %s. Sleeping for %ss. Still waiting...",
                        i, sleep)
                    time.sleep(sleep)
            logger.warning("loop terminated")
            return result

        return sleep_looper

    return decorator
```
