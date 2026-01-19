https://github.com/hynek/svcs/blob/1d6efae1a517eeabc3d283212e6e4bb058a10d85/./src/svcs/_core.py#L438-L470
```
🈚️

Many of the mutants are about warning/debug output.
no mock util can use
```
```
@icontract.snapshot(lambda self: list(self._on_close), name="old_on_close")
@icontract.ensure(lambda self: not self._services)
@icontract.ensure(lambda self: not self._on_close)
@icontract.ensure(lambda OLD, self: all(getattr(oc, "called", True) for rs, oc in OLD.old_on_close if not (iscoroutinefunction(oc) or isawaitable(oc))))
@icontract.ensure(lambda OLD, self: all(not getattr(oc, "called", False) for rs, oc in OLD.old_on_close if (iscoroutinefunction(oc) or isawaitable(oc)) and hasattr(oc, "called")))
```
[0, 1, 2, 3, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34]
===== 0 =====
```
         Errors are logged at warning level, but otherwise ignored.
         """
         for rs, oc in reversed(self._on_close):
-            if iscoroutinefunction(oc) or isawaitable(oc):
+            if isawaitable(oc) and not iscoroutinefunction(oc):
                 warnings.warn(
                     f"Skipped async cleanup for {rs.name!r}. "
                     "Use aclose() instead.",
```
```
    def close(self) -> None:
        """
        Clear registrations and run synchronous *on_registry_close* callbacks.

        Async callbacks are *not* awaited and a warning is raised

        Errors are logged at warning level, but otherwise ignored.
        """
        for rs, oc in reversed(self._on_close):
            if isawaitable(oc) and not iscoroutinefunction(oc):
                warnings.warn(
                    f"Skipped async cleanup for {rs.name!r}. "
                    "Use aclose() instead.",
                    # stacklevel doesn't matter here; it's coming from a
                    # framework.
                    stacklevel=1,
                )
                continue

            try:
                log.debug("closing %r", rs.name)
                oc()
                log.debug("closed %r", rs.name)
            except Exception:  # noqa: BLE001
                log.warning(
                    "Registry's on_registry_close callback failed for %r.",
                    rs.name,
                    exc_info=True,
                    extra={"svcs_service_name": rs.name},
                )

        self._services.clear()
        self._on_close.clear()
```
===== 1 =====
```
         Errors are logged at warning level, but otherwise ignored.
         """
         for rs, oc in reversed(self._on_close):
-            if iscoroutinefunction(oc) or isawaitable(oc):
+            if iscoroutinefunction(None) or isawaitable(oc):
                 warnings.warn(
                     f"Skipped async cleanup for {rs.name!r}. "
                     "Use aclose() instead.",
@@ -30,4 +30,4 @@                 )
 
         self._services.clear()
-        self._on_close.clear()+        self._on_close.clear()
```
```
    def close(self) -> None:
        """
        Clear registrations and run synchronous *on_registry_close* callbacks.

        Async callbacks are *not* awaited and a warning is raised

        Errors are logged at warning level, but otherwise ignored.
        """
        for rs, oc in reversed(self._on_close):
            if iscoroutinefunction(None) or isawaitable(oc):
                warnings.warn(
                    f"Skipped async cleanup for {rs.name!r}. "
                    "Use aclose() instead.",
                    # stacklevel doesn't matter here; it's coming from a
                    # framework.
                    stacklevel=1,
                )
                continue

            try:
                log.debug("closing %r", rs.name)
                oc()
                log.debug("closed %r", rs.name)
            except Exception:  # noqa: BLE001
                log.warning(
                    "Registry's on_registry_close callback failed for %r.",
                    rs.name,
                    exc_info=True,
                    extra={"svcs_service_name": rs.name},
                )

        self._services.clear()
        self._on_close.clear()

```
===== 2 =====
```
         Errors are logged at warning level, but otherwise ignored.
         """
         for rs, oc in reversed(self._on_close):
-            if iscoroutinefunction(oc) or isawaitable(oc):
+            if iscoroutinefunction(oc) and isawaitable(oc):
                 warnings.warn(
                     f"Skipped async cleanup for {rs.name!r}. "
                     "Use aclose() instead.",
```
```
    def close(self) -> None:
        """
        Clear registrations and run synchronous *on_registry_close* callbacks.

        Async callbacks are *not* awaited and a warning is raised

        Errors are logged at warning level, but otherwise ignored.
        """
        for rs, oc in reversed(self._on_close):
            if iscoroutinefunction(oc) and isawaitable(oc):
                warnings.warn(
                    f"Skipped async cleanup for {rs.name!r}. "
                    "Use aclose() instead.",
                    # stacklevel doesn't matter here; it's coming from a
                    # framework.
                    stacklevel=1,
                )
                continue

            try:
                log.debug("closing %r", rs.name)
                oc()
                log.debug("closed %r", rs.name)
            except Exception:  # noqa: BLE001
                log.warning(
                    "Registry's on_registry_close callback failed for %r.",
                    rs.name,
                    exc_info=True,
                    extra={"svcs_service_name": rs.name},
                )

        self._services.clear()
        self._on_close.clear()
```
===== 3 =====
```
         Errors are logged at warning level, but otherwise ignored.
         """
         for rs, oc in reversed(self._on_close):
-            if iscoroutinefunction(oc) or isawaitable(oc):
+            if iscoroutinefunction(oc) and isawaitable(oc):
                 warnings.warn(
                     f"Skipped async cleanup for {rs.name!r}. "
                     "Use aclose() instead.",
@@ -30,4 +30,4 @@                 )
 
         self._services.clear()
-        self._on_close.clear()+        self._on_close.clear()
```
```
    def close(self) -> None:
        """
        Clear registrations and run synchronous *on_registry_close* callbacks.

        Async callbacks are *not* awaited and a warning is raised

        Errors are logged at warning level, but otherwise ignored.
        """
        for rs, oc in reversed(self._on_close):
            if iscoroutinefunction(oc) and isawaitable(oc):
                warnings.warn(
                    f"Skipped async cleanup for {rs.name!r}. "
                    "Use aclose() instead.",
                    # stacklevel doesn't matter here; it's coming from a
                    # framework.
                    stacklevel=1,
                )
                continue

            try:
                log.debug("closing %r", rs.name)
                oc()
                log.debug("closed %r", rs.name)
            except Exception:  # noqa: BLE001
                log.warning(
                    "Registry's on_registry_close callback failed for %r.",
                    rs.name,
                    exc_info=True,
                    extra={"svcs_service_name": rs.name},
                )

        self._services.clear()
        self._on_close.clear()

```
===== 6 =====
```
         """
         for rs, oc in reversed(self._on_close):
             if iscoroutinefunction(oc) or isawaitable(oc):
-                warnings.warn(
+                log.error(
                     f"Skipped async cleanup for {rs.name!r}. "
                     "Use aclose() instead.",
                     # stacklevel doesn't matter here; it's coming from a
```
```
    def close(self) -> None:
        """
        Clear registrations and run synchronous *on_registry_close* callbacks.

        Async callbacks are *not* awaited and a warning is raised

        Errors are logged at warning level, but otherwise ignored.
        """
        for rs, oc in reversed(self._on_close):
            if iscoroutinefunction(oc) or isawaitable(oc):
                log.error(
                    f"Skipped async cleanup for {rs.name!r}. "
                    "Use aclose() instead.",
                    # stacklevel doesn't matter here; it's coming from a
                    # framework.
                    stacklevel=1,
                )
                continue

            try:
                log.debug("closing %r", rs.name)
                oc()
                log.debug("closed %r", rs.name)
            except Exception:  # noqa: BLE001
                log.warning(
                    "Registry's on_registry_close callback failed for %r.",
                    rs.name,
                    exc_info=True,
                    extra={"svcs_service_name": rs.name},
                )

        self._services.clear()
        self._on_close.clear()
```
===== 7 =====
```
         """
         for rs, oc in reversed(self._on_close):
             if iscoroutinefunction(oc) or isawaitable(oc):
-                warnings.warn(
+                logging.info(
                     f"Skipped async cleanup for {rs.name!r}. "
                     "Use aclose() instead.",
                     # stacklevel doesn't matter here; it's coming from a
```
```
    def close(self) -> None:
        """
        Clear registrations and run synchronous *on_registry_close* callbacks.

        Async callbacks are *not* awaited and a warning is raised

        Errors are logged at warning level, but otherwise ignored.
        """
        for rs, oc in reversed(self._on_close):
            if iscoroutinefunction(oc) or isawaitable(oc):
                logging.info(
                    f"Skipped async cleanup for {rs.name!r}. "
                    "Use aclose() instead.",
                    # stacklevel doesn't matter here; it's coming from a
                    # framework.
                    stacklevel=1,
                )
                continue

            try:
                log.debug("closing %r", rs.name)
                oc()
                log.debug("closed %r", rs.name)
            except Exception:  # noqa: BLE001
                log.warning(
                    "Registry's on_registry_close callback failed for %r.",
                    rs.name,
                    exc_info=True,
                    extra={"svcs_service_name": rs.name},
                )

        self._services.clear()
        self._on_close.clear()
```
===== 8 =====
```
         for rs, oc in reversed(self._on_close):
             if iscoroutinefunction(oc) or isawaitable(oc):
                 warnings.warn(
-                    f"Skipped async cleanup for {rs.name!r}. "
-                    "Use aclose() instead.",
+                    None,
                     # stacklevel doesn't matter here; it's coming from a
                     # framework.
                     stacklevel=1,
@@ -30,4 +29,4 @@                 )
 
         self._services.clear()
-        self._on_close.clear()+        self._on_close.clear()
```
```
    def close(self) -> None:
        """
        Clear registrations and run synchronous *on_registry_close* callbacks.

        Async callbacks are *not* awaited and a warning is raised

        Errors are logged at warning level, but otherwise ignored.
        """
        for rs, oc in reversed(self._on_close):
            if iscoroutinefunction(oc) or isawaitable(oc):
                warnings.warn(
                    None,
                    # stacklevel doesn't matter here; it's coming from a
                    # framework.
                    stacklevel=1,
                )
                continue

            try:
                log.debug("closing %r", rs.name)
                oc()
                log.debug("closed %r", rs.name)
            except Exception:  # noqa: BLE001
                log.warning(
                    "Registry's on_registry_close callback failed for %r.",
                    rs.name,
                    exc_info=True,
                    extra={"svcs_service_name": rs.name},
                )

        self._services.clear()
        self._on_close.clear()

```
===== 9 =====
```
         for rs, oc in reversed(self._on_close):
             if iscoroutinefunction(oc) or isawaitable(oc):
                 warnings.warn(
-                    f"Skipped async cleanup for {rs.name!r}. "
+                    f"Async cleanup for {rs.name!r} has been ignored."
                     "Use aclose() instead.",
                     # stacklevel doesn't matter here; it's coming from a
                     # framework.
```
```
    def close(self) -> None:
        """
        Clear registrations and run synchronous *on_registry_close* callbacks.

        Async callbacks are *not* awaited and a warning is raised

        Errors are logged at warning level, but otherwise ignored.
        """
        for rs, oc in reversed(self._on_close):
            if iscoroutinefunction(oc) or isawaitable(oc):
                warnings.warn(
                    f"Async cleanup for {rs.name!r} has been ignored."
                    "Use aclose() instead.",
                    # stacklevel doesn't matter here; it's coming from a
                    # framework.
                    stacklevel=1,
                )
                continue

            try:
                log.debug("closing %r", rs.name)
                oc()
                log.debug("closed %r", rs.name)
            except Exception:  # noqa: BLE001
                log.warning(
                    "Registry's on_registry_close callback failed for %r.",
                    rs.name,
                    exc_info=True,
                    extra={"svcs_service_name": rs.name},
                )

        self._services.clear()
        self._on_close.clear()
```
===== 10 =====
```
         for rs, oc in reversed(self._on_close):
             if iscoroutinefunction(oc) or isawaitable(oc):
                 warnings.warn(
-                    f"Skipped async cleanup for {rs.name!r}. "
+                    f"Async cleanup for {rs.name!r} was skipped."
                     "Use aclose() instead.",
                     # stacklevel doesn't matter here; it's coming from a
                     # framework.
```
```
    def close(self) -> None:
        """
        Clear registrations and run synchronous *on_registry_close* callbacks.

        Async callbacks are *not* awaited and a warning is raised

        Errors are logged at warning level, but otherwise ignored.
        """
        for rs, oc in reversed(self._on_close):
            if iscoroutinefunction(oc) or isawaitable(oc):
                warnings.warn(
                    f"Async cleanup for {rs.name!r} was skipped."
                    "Use aclose() instead.",
                    # stacklevel doesn't matter here; it's coming from a
                    # framework.
                    stacklevel=1,
                )
                continue

            try:
                log.debug("closing %r", rs.name)
                oc()
                log.debug("closed %r", rs.name)
            except Exception:  # noqa: BLE001
                log.warning(
                    "Registry's on_registry_close callback failed for %r.",
                    rs.name,
                    exc_info=True,
                    extra={"svcs_service_name": rs.name},
                )

        self._services.clear()
        self._on_close.clear()
```
===== 11 =====
```
         for rs, oc in reversed(self._on_close):
             if iscoroutinefunction(oc) or isawaitable(oc):
                 warnings.warn(
-                    f"Skipped async cleanup for {rs.name!r}. "
+                    f"Cleanup for {rs.name!r} was bypassed."
                     "Use aclose() instead.",
                     # stacklevel doesn't matter here; it's coming from a
                     # framework.
```
```
    def close(self) -> None:
        """
        Clear registrations and run synchronous *on_registry_close* callbacks.

        Async callbacks are *not* awaited and a warning is raised

        Errors are logged at warning level, but otherwise ignored.
        """
        for rs, oc in reversed(self._on_close):
            if iscoroutinefunction(oc) or isawaitable(oc):
                warnings.warn(
                    f"Cleanup for {rs.name!r} was bypassed."
                    "Use aclose() instead.",
                    # stacklevel doesn't matter here; it's coming from a
                    # framework.
                    stacklevel=1,
                )
                continue

            try:
                log.debug("closing %r", rs.name)
                oc()
                log.debug("closed %r", rs.name)
            except Exception:  # noqa: BLE001
                log.warning(
                    "Registry's on_registry_close callback failed for %r.",
                    rs.name,
                    exc_info=True,
                    extra={"svcs_service_name": rs.name},
                )

        self._services.clear()
        self._on_close.clear()
```
===== 12 =====
```
         for rs, oc in reversed(self._on_close):
             if iscoroutinefunction(oc) or isawaitable(oc):
                 warnings.warn(
-                    f"Skipped async cleanup for {rs.name!r}. "
+                    f"Cleanup for {rs.name!r} was not performed."
                     "Use aclose() instead.",
                     # stacklevel doesn't matter here; it's coming from a
                     # framework.
```
```
    def close(self) -> None:
        """
        Clear registrations and run synchronous *on_registry_close* callbacks.

        Async callbacks are *not* awaited and a warning is raised

        Errors are logged at warning level, but otherwise ignored.
        """
        for rs, oc in reversed(self._on_close):
            if iscoroutinefunction(oc) or isawaitable(oc):
                warnings.warn(
                    f"Cleanup for {rs.name!r} was not performed."
                    "Use aclose() instead.",
                    # stacklevel doesn't matter here; it's coming from a
                    # framework.
                    stacklevel=1,
                )
                continue

            try:
                log.debug("closing %r", rs.name)
                oc()
                log.debug("closed %r", rs.name)
            except Exception:  # noqa: BLE001
                log.warning(
                    "Registry's on_registry_close callback failed for %r.",
                    rs.name,
                    exc_info=True,
                    extra={"svcs_service_name": rs.name},
                )

        self._services.clear()
        self._on_close.clear()
```
===== 13 =====
```
         for rs, oc in reversed(self._on_close):
             if iscoroutinefunction(oc) or isawaitable(oc):
                 warnings.warn(
-                    f"Skipped async cleanup for {rs.name!r}. "
+                    f"Skipped async cleanup for service: {rs.name}."
                     "Use aclose() instead.",
                     # stacklevel doesn't matter here; it's coming from a
                     # framework.
```
```
    def close(self) -> None:
        """
        Clear registrations and run synchronous *on_registry_close* callbacks.

        Async callbacks are *not* awaited and a warning is raised

        Errors are logged at warning level, but otherwise ignored.
        """
        for rs, oc in reversed(self._on_close):
            if iscoroutinefunction(oc) or isawaitable(oc):
                warnings.warn(
                    f"Skipped async cleanup for service: {rs.name}."
                    "Use aclose() instead.",
                    # stacklevel doesn't matter here; it's coming from a
                    # framework.
                    stacklevel=1,
                )
                continue

            try:
                log.debug("closing %r", rs.name)
                oc()
                log.debug("closed %r", rs.name)
            except Exception:  # noqa: BLE001
                log.warning(
                    "Registry's on_registry_close callback failed for %r.",
                    rs.name,
                    exc_info=True,
                    extra={"svcs_service_name": rs.name},
                )

        self._services.clear()
        self._on_close.clear()
```
===== 14 =====
```
                 oc()
                 log.debug("closed %r", rs.name)
             except Exception:  # noqa: BLE001
-                log.warning(
+                log.debug(
                     "Registry's on_registry_close callback failed for %r.",
                     rs.name,
                     exc_info=True,
```
```
    def close(self) -> None:
        """
        Clear registrations and run synchronous *on_registry_close* callbacks.

        Async callbacks are *not* awaited and a warning is raised

        Errors are logged at warning level, but otherwise ignored.
        """
        for rs, oc in reversed(self._on_close):
            if iscoroutinefunction(oc) or isawaitable(oc):
                warnings.warn(
                    f"Skipped async cleanup for {rs.name!r}. "
                    "Use aclose() instead.",
                    # stacklevel doesn't matter here; it's coming from a
                    # framework.
                    stacklevel=1,
                )
                continue

            try:
                log.debug("closing %r", rs.name)
                oc()
                log.debug("closed %r", rs.name)
            except Exception:  # noqa: BLE001
                log.debug(
                    "Registry's on_registry_close callback failed for %r.",
                    rs.name,
                    exc_info=True,
                    extra={"svcs_service_name": rs.name},
                )

        self._services.clear()
        self._on_close.clear()
```
===== 15 =====
```
                 oc()
                 log.debug("closed %r", rs.name)
             except Exception:  # noqa: BLE001
-                log.warning(
+                log.info(
                     "Registry's on_registry_close callback failed for %r.",
                     rs.name,
                     exc_info=True,
```
```
    def close(self) -> None:
        """
        Clear registrations and run synchronous *on_registry_close* callbacks.

        Async callbacks are *not* awaited and a warning is raised

        Errors are logged at warning level, but otherwise ignored.
        """
        for rs, oc in reversed(self._on_close):
            if iscoroutinefunction(oc) or isawaitable(oc):
                warnings.warn(
                    f"Skipped async cleanup for {rs.name!r}. "
                    "Use aclose() instead.",
                    # stacklevel doesn't matter here; it's coming from a
                    # framework.
                    stacklevel=1,
                )
                continue

            try:
                log.debug("closing %r", rs.name)
                oc()
                log.debug("closed %r", rs.name)
            except Exception:  # noqa: BLE001
                log.info(
                    "Registry's on_registry_close callback failed for %r.",
                    rs.name,
                    exc_info=True,
                    extra={"svcs_service_name": rs.name},
                )

        self._services.clear()
        self._on_close.clear()
```
===== 16 =====
```
                 log.debug("closed %r", rs.name)
             except Exception:  # noqa: BLE001
                 log.warning(
-                    "Registry's on_registry_close callback failed for %r.",
+                    "XXRegistry's on_registry_close callback failed for %r.XX",
                     rs.name,
                     exc_info=True,
                     extra={"svcs_service_name": rs.name},
                 )
 
         self._services.clear()
-        self._on_close.clear()+        self._on_close.clear()
```
```
    def close(self) -> None:
        """
        Clear registrations and run synchronous *on_registry_close* callbacks.

        Async callbacks are *not* awaited and a warning is raised

        Errors are logged at warning level, but otherwise ignored.
        """
        for rs, oc in reversed(self._on_close):
            if iscoroutinefunction(oc) or isawaitable(oc):
                warnings.warn(
                    f"Skipped async cleanup for {rs.name!r}. "
                    "Use aclose() instead.",
                    # stacklevel doesn't matter here; it's coming from a
                    # framework.
                    stacklevel=1,
                )
                continue

            try:
                log.debug("closing %r", rs.name)
                oc()
                log.debug("closed %r", rs.name)
            except Exception:  # noqa: BLE001
                log.warning(
                    "XXRegistry's on_registry_close callback failed for %r.XX",
                    rs.name,
                    exc_info=True,
                    extra={"svcs_service_name": rs.name},
                )

        self._services.clear()
        self._on_close.clear()

```
===== 17 =====
```
                 log.debug("closed %r", rs.name)
             except Exception:  # noqa: BLE001
                 log.warning(
-                    "Registry's on_registry_close callback failed for %r.",
+                    "registry's on_registry_close callback failed for %r.",
                     rs.name,
                     exc_info=True,
                     extra={"svcs_service_name": rs.name},
                 )
 
         self._services.clear()
-        self._on_close.clear()+        self._on_close.clear()
```
```
    def close(self) -> None:
        """
        Clear registrations and run synchronous *on_registry_close* callbacks.

        Async callbacks are *not* awaited and a warning is raised

        Errors are logged at warning level, but otherwise ignored.
        """
        for rs, oc in reversed(self._on_close):
            if iscoroutinefunction(oc) or isawaitable(oc):
                warnings.warn(
                    f"Skipped async cleanup for {rs.name!r}. "
                    "Use aclose() instead.",
                    # stacklevel doesn't matter here; it's coming from a
                    # framework.
                    stacklevel=1,
                )
                continue

            try:
                log.debug("closing %r", rs.name)
                oc()
                log.debug("closed %r", rs.name)
            except Exception:  # noqa: BLE001
                log.warning(
                    "registry's on_registry_close callback failed for %r.",
                    rs.name,
                    exc_info=True,
                    extra={"svcs_service_name": rs.name},
                )

        self._services.clear()
        self._on_close.clear()

```
===== 18 =====
```
                 log.debug("closed %r", rs.name)
             except Exception:  # noqa: BLE001
                 log.warning(
-                    "Registry's on_registry_close callback failed for %r.",
                     rs.name,
                     exc_info=True,
                     extra={"svcs_service_name": rs.name},
                 )
 
         self._services.clear()
-        self._on_close.clear()+        self._on_close.clear()
```
```
    def close(self) -> None:
        """
        Clear registrations and run synchronous *on_registry_close* callbacks.

        Async callbacks are *not* awaited and a warning is raised

        Errors are logged at warning level, but otherwise ignored.
        """
        for rs, oc in reversed(self._on_close):
            if iscoroutinefunction(oc) or isawaitable(oc):
                warnings.warn(
                    f"Skipped async cleanup for {rs.name!r}. "
                    "Use aclose() instead.",
                    # stacklevel doesn't matter here; it's coming from a
                    # framework.
                    stacklevel=1,
                )
                continue

            try:
                log.debug("closing %r", rs.name)
                oc()
                log.debug("closed %r", rs.name)
            except Exception:  # noqa: BLE001
                log.warning(
                    rs.name,
                    exc_info=True,
                    extra={"svcs_service_name": rs.name},
                )

        self._services.clear()
        self._on_close.clear()

```
===== 19 =====
```
             except Exception:  # noqa: BLE001
                 log.warning(
                     "Registry's on_registry_close callback failed for %r.",
-                    rs.name,
+                    "Service cleanup failed",  # Logs a generic message instead of the specific service name.
                     exc_info=True,
                     extra={"svcs_service_name": rs.name},
                 )
```
```
    def close(self) -> None:
        """
        Clear registrations and run synchronous *on_registry_close* callbacks.

        Async callbacks are *not* awaited and a warning is raised

        Errors are logged at warning level, but otherwise ignored.
        """
        for rs, oc in reversed(self._on_close):
            if iscoroutinefunction(oc) or isawaitable(oc):
                warnings.warn(
                    f"Skipped async cleanup for {rs.name!r}. "
                    "Use aclose() instead.",
                    # stacklevel doesn't matter here; it's coming from a
                    # framework.
                    stacklevel=1,
                )
                continue

            try:
                log.debug("closing %r", rs.name)
                oc()
                log.debug("closed %r", rs.name)
            except Exception:  # noqa: BLE001
                log.warning(
                    "Registry's on_registry_close callback failed for %r.",
                    "Service cleanup failed",  # Logs a generic message instead of the specific service name.
                    exc_info=True,
                    extra={"svcs_service_name": rs.name},
                )

        self._services.clear()
        self._on_close.clear()
```
===== 20 =====
```
             except Exception:  # noqa: BLE001
                 log.warning(
                     "Registry's on_registry_close callback failed for %r.",
-                    rs.name,
+                    "Unknown service",  # Incorrectly logs a static message instead of the service name.
                     exc_info=True,
                     extra={"svcs_service_name": rs.name},
                 )
```
```
    def close(self) -> None:
        """
        Clear registrations and run synchronous *on_registry_close* callbacks.

        Async callbacks are *not* awaited and a warning is raised

        Errors are logged at warning level, but otherwise ignored.
        """
        for rs, oc in reversed(self._on_close):
            if iscoroutinefunction(oc) or isawaitable(oc):
                warnings.warn(
                    f"Skipped async cleanup for {rs.name!r}. "
                    "Use aclose() instead.",
                    # stacklevel doesn't matter here; it's coming from a
                    # framework.
                    stacklevel=1,
                )
                continue

            try:
                log.debug("closing %r", rs.name)
                oc()
                log.debug("closed %r", rs.name)
            except Exception:  # noqa: BLE001
                log.warning(
                    "Registry's on_registry_close callback failed for %r.",
                    "Unknown service",  # Incorrectly logs a static message instead of the service name.
                    exc_info=True,
                    extra={"svcs_service_name": rs.name},
                )

        self._services.clear()
        self._on_close.clear()
```
===== 21 =====
```
             except Exception:  # noqa: BLE001
                 log.warning(
                     "Registry's on_registry_close callback failed for %r.",
-                    rs.name,
+                    None,
                     exc_info=True,
                     extra={"svcs_service_name": rs.name},
                 )
 
         self._services.clear()
-        self._on_close.clear()+        self._on_close.clear()
```
```
    def close(self) -> None:
        """
        Clear registrations and run synchronous *on_registry_close* callbacks.

        Async callbacks are *not* awaited and a warning is raised

        Errors are logged at warning level, but otherwise ignored.
        """
        for rs, oc in reversed(self._on_close):
            if iscoroutinefunction(oc) or isawaitable(oc):
                warnings.warn(
                    f"Skipped async cleanup for {rs.name!r}. "
                    "Use aclose() instead.",
                    # stacklevel doesn't matter here; it's coming from a
                    # framework.
                    stacklevel=1,
                )
                continue

            try:
                log.debug("closing %r", rs.name)
                oc()
                log.debug("closed %r", rs.name)
            except Exception:  # noqa: BLE001
                log.warning(
                    "Registry's on_registry_close callback failed for %r.",
                    None,
                    exc_info=True,
                    extra={"svcs_service_name": rs.name},
                )

        self._services.clear()
        self._on_close.clear()

```
===== 22 =====
```
             except Exception:  # noqa: BLE001
                 log.warning(
                     "Registry's on_registry_close callback failed for %r.",
-                    rs.name,
+                    None,  # Logs None, which provides no useful information about the service.
                     exc_info=True,
                     extra={"svcs_service_name": rs.name},
                 )
```
```
    def close(self) -> None:
        """
        Clear registrations and run synchronous *on_registry_close* callbacks.

        Async callbacks are *not* awaited and a warning is raised

        Errors are logged at warning level, but otherwise ignored.
        """
        for rs, oc in reversed(self._on_close):
            if iscoroutinefunction(oc) or isawaitable(oc):
                warnings.warn(
                    f"Skipped async cleanup for {rs.name!r}. "
                    "Use aclose() instead.",
                    # stacklevel doesn't matter here; it's coming from a
                    # framework.
                    stacklevel=1,
                )
                continue

            try:
                log.debug("closing %r", rs.name)
                oc()
                log.debug("closed %r", rs.name)
            except Exception:  # noqa: BLE001
                log.warning(
                    "Registry's on_registry_close callback failed for %r.",
                    None,  # Logs None, which provides no useful information about the service.
                    exc_info=True,
                    extra={"svcs_service_name": rs.name},
                )

        self._services.clear()
        self._on_close.clear()
```
===== 23 =====
```
             except Exception:  # noqa: BLE001
                 log.warning(
                     "Registry's on_registry_close callback failed for %r.",
-                    rs.name,
                     exc_info=True,
                     extra={"svcs_service_name": rs.name},
                 )
 
         self._services.clear()
-        self._on_close.clear()+        self._on_close.clear()
```
```
    def close(self) -> None:
        """
        Clear registrations and run synchronous *on_registry_close* callbacks.

        Async callbacks are *not* awaited and a warning is raised

        Errors are logged at warning level, but otherwise ignored.
        """
        for rs, oc in reversed(self._on_close):
            if iscoroutinefunction(oc) or isawaitable(oc):
                warnings.warn(
                    f"Skipped async cleanup for {rs.name!r}. "
                    "Use aclose() instead.",
                    # stacklevel doesn't matter here; it's coming from a
                    # framework.
                    stacklevel=1,
                )
                continue

            try:
                log.debug("closing %r", rs.name)
                oc()
                log.debug("closed %r", rs.name)
            except Exception:  # noqa: BLE001
                log.warning(
                    "Registry's on_registry_close callback failed for %r.",
                    exc_info=True,
                    extra={"svcs_service_name": rs.name},
                )

        self._services.clear()
        self._on_close.clear()

```
===== 24 =====
```
             except Exception:  # noqa: BLE001
                 log.warning(
                     "Registry's on_registry_close callback failed for %r.",
-                    rs.name,
+                    f"{rs.name} cleanup failed",  # Introduces a misleading message format that may confuse users.
                     exc_info=True,
                     extra={"svcs_service_name": rs.name},
                 )
```
```
    def close(self) -> None:
        """
        Clear registrations and run synchronous *on_registry_close* callbacks.

        Async callbacks are *not* awaited and a warning is raised

        Errors are logged at warning level, but otherwise ignored.
        """
        for rs, oc in reversed(self._on_close):
            if iscoroutinefunction(oc) or isawaitable(oc):
                warnings.warn(
                    f"Skipped async cleanup for {rs.name!r}. "
                    "Use aclose() instead.",
                    # stacklevel doesn't matter here; it's coming from a
                    # framework.
                    stacklevel=1,
                )
                continue

            try:
                log.debug("closing %r", rs.name)
                oc()
                log.debug("closed %r", rs.name)
            except Exception:  # noqa: BLE001
                log.warning(
                    "Registry's on_registry_close callback failed for %r.",
                    f"{rs.name} cleanup failed",  # Introduces a misleading message format that may confuse users.
                    exc_info=True,
                    extra={"svcs_service_name": rs.name},
                )

        self._services.clear()
        self._on_close.clear()
```
===== 25 =====
```
             except Exception:  # noqa: BLE001
                 log.warning(
                     "Registry's on_registry_close callback failed for %r.",
-                    rs.name,
+                    rs.svc_type,  # Logs the service type instead of the service name, which may not be informative.
                     exc_info=True,
                     extra={"svcs_service_name": rs.name},
                 )
```
```
    def close(self) -> None:
        """
        Clear registrations and run synchronous *on_registry_close* callbacks.

        Async callbacks are *not* awaited and a warning is raised

        Errors are logged at warning level, but otherwise ignored.
        """
        for rs, oc in reversed(self._on_close):
            if iscoroutinefunction(oc) or isawaitable(oc):
                warnings.warn(
                    f"Skipped async cleanup for {rs.name!r}. "
                    "Use aclose() instead.",
                    # stacklevel doesn't matter here; it's coming from a
                    # framework.
                    stacklevel=1,
                )
                continue

            try:
                log.debug("closing %r", rs.name)
                oc()
                log.debug("closed %r", rs.name)
            except Exception:  # noqa: BLE001
                log.warning(
                    "Registry's on_registry_close callback failed for %r.",
                    rs.svc_type,  # Logs the service type instead of the service name, which may not be informative.
                    exc_info=True,
                    extra={"svcs_service_name": rs.name},
                )

        self._services.clear()
        self._on_close.clear()
```
===== 26 =====
```
                     "Registry's on_registry_close callback failed for %r.",
                     rs.name,
                     exc_info=True,
-                    extra={"svcs_service_name": rs.name},
-                )
+                    )
 
         self._services.clear()
-        self._on_close.clear()+        self._on_close.clear()
```
```
    def close(self) -> None:
        """
        Clear registrations and run synchronous *on_registry_close* callbacks.

        Async callbacks are *not* awaited and a warning is raised

        Errors are logged at warning level, but otherwise ignored.
        """
        for rs, oc in reversed(self._on_close):
            if iscoroutinefunction(oc) or isawaitable(oc):
                warnings.warn(
                    f"Skipped async cleanup for {rs.name!r}. "
                    "Use aclose() instead.",
                    # stacklevel doesn't matter here; it's coming from a
                    # framework.
                    stacklevel=1,
                )
                continue

            try:
                log.debug("closing %r", rs.name)
                oc()
                log.debug("closed %r", rs.name)
            except Exception:  # noqa: BLE001
                log.warning(
                    "Registry's on_registry_close callback failed for %r.",
                    rs.name,
                    exc_info=True,
                    )

        self._services.clear()
        self._on_close.clear()

```
===== 27 =====
```
                     "Registry's on_registry_close callback failed for %r.",
                     rs.name,
                     exc_info=True,
-                    extra={"svcs_service_name": rs.name},
+                    extra=None,
                 )
 
         self._services.clear()
-        self._on_close.clear()+        self._on_close.clear()
```
```
    def close(self) -> None:
        """
        Clear registrations and run synchronous *on_registry_close* callbacks.

        Async callbacks are *not* awaited and a warning is raised

        Errors are logged at warning level, but otherwise ignored.
        """
        for rs, oc in reversed(self._on_close):
            if iscoroutinefunction(oc) or isawaitable(oc):
                warnings.warn(
                    f"Skipped async cleanup for {rs.name!r}. "
                    "Use aclose() instead.",
                    # stacklevel doesn't matter here; it's coming from a
                    # framework.
                    stacklevel=1,
                )
                continue

            try:
                log.debug("closing %r", rs.name)
                oc()
                log.debug("closed %r", rs.name)
            except Exception:  # noqa: BLE001
                log.warning(
                    "Registry's on_registry_close callback failed for %r.",
                    rs.name,
                    exc_info=True,
                    extra=None,
                )

        self._services.clear()
        self._on_close.clear()

```
===== 28 =====
```
                     "Registry's on_registry_close callback failed for %r.",
                     rs.name,
                     exc_info=True,
-                    extra={"svcs_service_name": rs.name},
+                    extra={"SVCS_SERVICE_NAME": rs.name},
                 )
 
         self._services.clear()
-        self._on_close.clear()+        self._on_close.clear()
```
```
    def close(self) -> None:
        """
        Clear registrations and run synchronous *on_registry_close* callbacks.

        Async callbacks are *not* awaited and a warning is raised

        Errors are logged at warning level, but otherwise ignored.
        """
        for rs, oc in reversed(self._on_close):
            if iscoroutinefunction(oc) or isawaitable(oc):
                warnings.warn(
                    f"Skipped async cleanup for {rs.name!r}. "
                    "Use aclose() instead.",
                    # stacklevel doesn't matter here; it's coming from a
                    # framework.
                    stacklevel=1,
                )
                continue

            try:
                log.debug("closing %r", rs.name)
                oc()
                log.debug("closed %r", rs.name)
            except Exception:  # noqa: BLE001
                log.warning(
                    "Registry's on_registry_close callback failed for %r.",
                    rs.name,
                    exc_info=True,
                    extra={"SVCS_SERVICE_NAME": rs.name},
                )

        self._services.clear()
        self._on_close.clear()

```
===== 29 =====
```
                     "Registry's on_registry_close callback failed for %r.",
                     rs.name,
                     exc_info=True,
-                    extra={"svcs_service_name": rs.name},
+                    extra={"XXsvcs_service_nameXX": rs.name},
                 )
 
         self._services.clear()
-        self._on_close.clear()+        self._on_close.clear()
```
```
    def close(self) -> None:
        """
        Clear registrations and run synchronous *on_registry_close* callbacks.

        Async callbacks are *not* awaited and a warning is raised

        Errors are logged at warning level, but otherwise ignored.
        """
        for rs, oc in reversed(self._on_close):
            if iscoroutinefunction(oc) or isawaitable(oc):
                warnings.warn(
                    f"Skipped async cleanup for {rs.name!r}. "
                    "Use aclose() instead.",
                    # stacklevel doesn't matter here; it's coming from a
                    # framework.
                    stacklevel=1,
                )
                continue

            try:
                log.debug("closing %r", rs.name)
                oc()
                log.debug("closed %r", rs.name)
            except Exception:  # noqa: BLE001
                log.warning(
                    "Registry's on_registry_close callback failed for %r.",
                    rs.name,
                    exc_info=True,
                    extra={"XXsvcs_service_nameXX": rs.name},
                )

        self._services.clear()
        self._on_close.clear()

```
===== 30 =====
```
                     "Registry's on_registry_close callback failed for %r.",
                     rs.name,
                     exc_info=True,
-                    extra={"svcs_service_name": rs.name},
+                    extra={"service_name": rs.name},
                 )
 
         self._services.clear()
```
```
    def close(self) -> None:
        """
        Clear registrations and run synchronous *on_registry_close* callbacks.

        Async callbacks are *not* awaited and a warning is raised

        Errors are logged at warning level, but otherwise ignored.
        """
        for rs, oc in reversed(self._on_close):
            if iscoroutinefunction(oc) or isawaitable(oc):
                warnings.warn(
                    f"Skipped async cleanup for {rs.name!r}. "
                    "Use aclose() instead.",
                    # stacklevel doesn't matter here; it's coming from a
                    # framework.
                    stacklevel=1,
                )
                continue

            try:
                log.debug("closing %r", rs.name)
                oc()
                log.debug("closed %r", rs.name)
            except Exception:  # noqa: BLE001
                log.warning(
                    "Registry's on_registry_close callback failed for %r.",
                    rs.name,
                    exc_info=True,
                    extra={"service_name": rs.name},
                )

        self._services.clear()
        self._on_close.clear()
```
===== 31 =====
```
                     "Registry's on_registry_close callback failed for %r.",
                     rs.name,
                     exc_info=True,
-                    extra={"svcs_service_name": rs.name},
+                    extra={"svcs_service_name": "unknown"},
                 )
 
         self._services.clear()
```
```
    def close(self) -> None:
        """
        Clear registrations and run synchronous *on_registry_close* callbacks.

        Async callbacks are *not* awaited and a warning is raised

        Errors are logged at warning level, but otherwise ignored.
        """
        for rs, oc in reversed(self._on_close):
            if iscoroutinefunction(oc) or isawaitable(oc):
                warnings.warn(
                    f"Skipped async cleanup for {rs.name!r}. "
                    "Use aclose() instead.",
                    # stacklevel doesn't matter here; it's coming from a
                    # framework.
                    stacklevel=1,
                )
                continue

            try:
                log.debug("closing %r", rs.name)
                oc()
                log.debug("closed %r", rs.name)
            except Exception:  # noqa: BLE001
                log.warning(
                    "Registry's on_registry_close callback failed for %r.",
                    rs.name,
                    exc_info=True,
                    extra={"svcs_service_name": "unknown"},
                )

        self._services.clear()
        self._on_close.clear()
```
===== 32 =====
```
                     "Registry's on_registry_close callback failed for %r.",
                     rs.name,
                     exc_info=True,
-                    extra={"svcs_service_name": rs.name},
+                    extra={"svcs_service_name": None},
                 )
 
         self._services.clear()
```
```
    def close(self) -> None:
        """
        Clear registrations and run synchronous *on_registry_close* callbacks.

        Async callbacks are *not* awaited and a warning is raised

        Errors are logged at warning level, but otherwise ignored.
        """
        for rs, oc in reversed(self._on_close):
            if iscoroutinefunction(oc) or isawaitable(oc):
                warnings.warn(
                    f"Skipped async cleanup for {rs.name!r}. "
                    "Use aclose() instead.",
                    # stacklevel doesn't matter here; it's coming from a
                    # framework.
                    stacklevel=1,
                )
                continue

            try:
                log.debug("closing %r", rs.name)
                oc()
                log.debug("closed %r", rs.name)
            except Exception:  # noqa: BLE001
                log.warning(
                    "Registry's on_registry_close callback failed for %r.",
                    rs.name,
                    exc_info=True,
                    extra={"svcs_service_name": None},
                )

        self._services.clear()
        self._on_close.clear()
```
===== 33 =====
```
                     "Registry's on_registry_close callback failed for %r.",
                     rs.name,
                     exc_info=True,
-                    extra={"svcs_service_name": rs.name},
+                    extra={"svcs_service_name": f"{rs.name}_error"},
                 )
 
         self._services.clear()
```
```
    def close(self) -> None:
        """
        Clear registrations and run synchronous *on_registry_close* callbacks.

        Async callbacks are *not* awaited and a warning is raised

        Errors are logged at warning level, but otherwise ignored.
        """
        for rs, oc in reversed(self._on_close):
            if iscoroutinefunction(oc) or isawaitable(oc):
                warnings.warn(
                    f"Skipped async cleanup for {rs.name!r}. "
                    "Use aclose() instead.",
                    # stacklevel doesn't matter here; it's coming from a
                    # framework.
                    stacklevel=1,
                )
                continue

            try:
                log.debug("closing %r", rs.name)
                oc()
                log.debug("closed %r", rs.name)
            except Exception:  # noqa: BLE001
                log.warning(
                    "Registry's on_registry_close callback failed for %r.",
                    rs.name,
                    exc_info=True,
                    extra={"svcs_service_name": f"{rs.name}_error"},
                )

        self._services.clear()
        self._on_close.clear()
```
===== 34 =====
```
                     "Registry's on_registry_close callback failed for %r.",
                     rs.name,
                     exc_info=True,
-                    extra={"svcs_service_name": rs.name},
+                    extra={"svcs_service_name": rs.svc_type},
                 )
 
         self._services.clear()
```
```
    def close(self) -> None:
        """
        Clear registrations and run synchronous *on_registry_close* callbacks.

        Async callbacks are *not* awaited and a warning is raised

        Errors are logged at warning level, but otherwise ignored.
        """
        for rs, oc in reversed(self._on_close):
            if iscoroutinefunction(oc) or isawaitable(oc):
                warnings.warn(
                    f"Skipped async cleanup for {rs.name!r}. "
                    "Use aclose() instead.",
                    # stacklevel doesn't matter here; it's coming from a
                    # framework.
                    stacklevel=1,
                )
                continue

            try:
                log.debug("closing %r", rs.name)
                oc()
                log.debug("closed %r", rs.name)
            except Exception:  # noqa: BLE001
                log.warning(
                    "Registry's on_registry_close callback failed for %r.",
                    rs.name,
                    exc_info=True,
                    extra={"svcs_service_name": rs.svc_type},
                )

        self._services.clear()
        self._on_close.clear()
```
