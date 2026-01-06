https://github.com/google/mobly/blob/6aa58093145669c99c1d6680ab2c1ace42f7f229/./mobly/controllers/android_device_lib/adb.py#L402-L431
```
@icontract.ensure(lambda result: isinstance(result, dict))
@icontract.ensure(lambda prop_names, result: all(key in prop_names for key in result.keys()))
@icontract.ensure(lambda result: all(isinstance(value, str) for value in result.values()))
```
```
return value - built-in container of scalars


return value content

built-in container of scalars
```
passed
```
@icontract.snapshot(lambda prop_names: list(prop_names), name="prop_names_copy")
@icontract.ensure(lambda result, OLD: isinstance(result, dict))
@icontract.ensure(lambda result, OLD: set(result.keys()).issubset(set(OLD.prop_names_copy)))
@icontract.ensure(lambda result, self: (not hasattr(self, "_exec_cmd") or getattr(self._exec_cmd, "call_count", None) is None or ((result and 1 <= self._exec_cmd.call_count <= DEFAULT_GETPROPS_ATTEMPTS) or (not result and self._exec_cmd.call_count == DEFAULT_GETPROPS_ATTEMPTS))))
@icontract.ensure(lambda result, self: (not hasattr(time, "sleep") or getattr(time.sleep, "call_count", None) is None or ((result and getattr(time.sleep, "call_count", None) == (getattr(self._exec_cmd, "call_count", 1) - 1)) or (not result and getattr(time.sleep, "call_count", None) == (DEFAULT_GETPROPS_ATTEMPTS - 1)))))
@icontract.ensure(lambda self: (not hasattr(self, "_exec_cmd") or getattr(self._exec_cmd, "call_args_list", None) is None or (len(self._exec_cmd.call_args_list) == 0 or (self._exec_cmd.call_args_list[-1][0] and self._exec_cmd.call_args_list[-1][0][0] == ['adb', 'shell', 'getprop'] and self._exec_cmd.call_args_list[-1][1].get('timeout') == DEFAULT_GETPROP_TIMEOUT_SEC))))

```
===== 9: failed =====
```
       # in a working state.
       raw_output = self.shell(['getprop'], timeout=DEFAULT_GETPROP_TIMEOUT_SEC)
       properties = self._parse_getprop_output(raw_output)
-      if properties:
+      if not properties:
         for name in prop_names:
           if name in properties:
             results[name] = properties[name]
```
```
  def getprops(self, prop_names):
    """Get multiple properties of the device.

    This is a convenience wrapper for `adb shell getprop`. Use this to
    reduce the number of adb calls when getting multiple properties.

    Args:
      prop_names: list of strings, the names of the properties to get.

    Returns:
      A dict containing name-value pairs of the properties requested, if
      they exist.
    """
    attempts = DEFAULT_GETPROPS_ATTEMPTS
    results = {}
    for attempt in range(attempts):
      # The ADB getprop command can randomly return empty string, so try
      # multiple times. This value should always be non-empty if the device
      # in a working state.
      raw_output = self.shell(['getprop'], timeout=DEFAULT_GETPROP_TIMEOUT_SEC)
      properties = self._parse_getprop_output(raw_output)
      if not properties:
        for name in prop_names:
          if name in properties:
            results[name] = properties[name]
        break
      # Don't call sleep on the last attempt.
      if attempt < attempts - 1:
        time.sleep(DEFAULT_GETPROPS_RETRY_SLEEP_SEC)
    return results
```
