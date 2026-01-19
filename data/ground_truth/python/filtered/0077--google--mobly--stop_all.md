https://github.com/google/mobly/blob/6aa58093145669c99c1d6680ab2c1ace42f7f229/./mobly/controllers/android_device_lib/service_manager.py#L224-L234
```
🈚️

testcase used mock util to validate the sequence of the service stop.
The postcondition cannot access it.

```
```
@icontract.snapshot(lambda self: list(self._service_objects.keys()), name="old_aliases")
@icontract.snapshot(lambda self: {alias: service for alias, service in self._service_objects.items()}, name="old_services")
@icontract.snapshot(lambda self: {alias: (getattr(service, "stop_func").call_count if hasattr(service, "stop_func") else None) for alias, service in self._service_objects.items()}, name="old_stop_counts")
@icontract.snapshot(lambda self: {alias: service.is_alive for alias, service in self._service_objects.items()}, name="old_alive")
@icontract.ensure(lambda OLD, self: list(self._service_objects.keys()) == OLD.old_aliases)
@icontract.ensure(lambda OLD, self: all(self._service_objects[alias] is OLD.old_services[alias] for alias in OLD.old_aliases))
@icontract.ensure(lambda OLD, self: all(
    (
      # If it was alive before, a stop attempt must have been made (call_count increased)
      OLD.old_alive[alias] and (
        (OLD.old_stop_counts[alias] is not None and getattr(self._service_objects[alias].stop_func, "call_count", 0) >= OLD.old_stop_counts[alias] + 1)
        or
        # If there's no stop_func, require the service to be not alive afterwards.
        (OLD.old_stop_counts[alias] is None and not self._service_objects[alias].is_alive)
      )
    )
    or
    (
      # If it was not alive before, no stop should have been attempted (call_count unchanged)
      (not OLD.old_alive[alias]) and (
        (OLD.old_stop_counts[alias] is not None and getattr(self._service_objects[alias].stop_func, "call_count", 0) == OLD.old_stop_counts[alias])
        or
        (OLD.old_stop_counts[alias] is None and not self._service_objects[alias].is_alive)
      )
    )
    for alias in OLD.old_aliases
))
```
[0, 1, 4, 5, 6, 7]
===== 0 =====
```
     """
     # OrdereDict#items does not return a sequence in Python 3.4, so we have
     # to do a list conversion here.
-    for alias, service in reversed(list(self._service_objects.items())):
+    for alias, service in list(self._service_objects.items()):
       if service.is_alive:
         with expects.expect_no_raises('Failed to stop service "%s".' % alias):
           service.stop()
```
```
  def stop_all(self):
    """Stops all active service instances.

    Services will be stopped in the reverse order they were registered.
    """
    # OrdereDict#items does not return a sequence in Python 3.4, so we have
    # to do a list conversion here.
    for alias, service in list(self._service_objects.items()):
      if service.is_alive:
        with expects.expect_no_raises('Failed to stop service "%s".' % alias):
          service.stop()
```
===== 1 =====
```
     """
     # OrdereDict#items does not return a sequence in Python 3.4, so we have
     # to do a list conversion here.
-    for alias, service in reversed(list(self._service_objects.items())):
+    for alias, service in self._service_objects.items():
       if service.is_alive:
         with expects.expect_no_raises('Failed to stop service "%s".' % alias):
           service.stop()
```
```
  def stop_all(self):
    """Stops all active service instances.

    Services will be stopped in the reverse order they were registered.
    """
    # OrdereDict#items does not return a sequence in Python 3.4, so we have
    # to do a list conversion here.
    for alias, service in self._service_objects.items():
      if service.is_alive:
        with expects.expect_no_raises('Failed to stop service "%s".' % alias):
          service.stop()
```
===== 4 =====
```
     # to do a list conversion here.
     for alias, service in reversed(list(self._service_objects.items())):
       if service.is_alive:
-        with expects.expect_no_raises('Failed to stop service "%s".' % alias):
+        with expects.expect_no_raises('Could not stop service "%s".' % service.alias):
           service.stop()
```
```
  def stop_all(self):
    """Stops all active service instances.

    Services will be stopped in the reverse order they were registered.
    """
    # OrdereDict#items does not return a sequence in Python 3.4, so we have
    # to do a list conversion here.
    for alias, service in reversed(list(self._service_objects.items())):
      if service.is_alive:
        with expects.expect_no_raises('Could not stop service "%s".' % service.alias):
          service.stop()
```
===== 5 =====
```
     # to do a list conversion here.
     for alias, service in reversed(list(self._service_objects.items())):
       if service.is_alive:
-        with expects.expect_no_raises('Failed to stop service "%s".' % alias):
+        with expects.expect_no_raises('Error while stopping service "%s".' % alias):
           service.stop()
```
```
  def stop_all(self):
    """Stops all active service instances.

    Services will be stopped in the reverse order they were registered.
    """
    # OrdereDict#items does not return a sequence in Python 3.4, so we have
    # to do a list conversion here.
    for alias, service in reversed(list(self._service_objects.items())):
      if service.is_alive:
        with expects.expect_no_raises('Error while stopping service "%s".' % alias):
          service.stop()
```
===== 6 =====
```
     # to do a list conversion here.
     for alias, service in reversed(list(self._service_objects.items())):
       if service.is_alive:
-        with expects.expect_no_raises('Failed to stop service "%s".' % alias):
+        with expects.expect_no_raises('Service "%s" could not be stopped.' % alias):
           service.stop()
```
```
  def stop_all(self):
    """Stops all active service instances.

    Services will be stopped in the reverse order they were registered.
    """
    # OrdereDict#items does not return a sequence in Python 3.4, so we have
    # to do a list conversion here.
    for alias, service in reversed(list(self._service_objects.items())):
      if service.is_alive:
        with expects.expect_no_raises('Service "%s" could not be stopped.' % alias):
          service.stop()
```
===== 7 =====
```
     # to do a list conversion here.
     for alias, service in reversed(list(self._service_objects.items())):
       if service.is_alive:
-        with expects.expect_no_raises('Failed to stop service "%s".' % alias):
+        with expects.expect_no_raises('Stopping service "%s" encountered an issue.' % alias):
           service.stop()
```
```
  def stop_all(self):
    """Stops all active service instances.

    Services will be stopped in the reverse order they were registered.
    """
    # OrdereDict#items does not return a sequence in Python 3.4, so we have
    # to do a list conversion here.
    for alias, service in reversed(list(self._service_objects.items())):
      if service.is_alive:
        with expects.expect_no_raises('Stopping service "%s" encountered an issue.' % alias):
          service.stop()
```
