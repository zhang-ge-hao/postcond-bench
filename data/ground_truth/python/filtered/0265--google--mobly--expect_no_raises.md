https://github.com/google/mobly/blob/6aa58093145669c99c1d6680ab2c1ace42f7f229/./mobly/expects.py#L138-L162
```
🈚️

yield
```
```
@icontract.snapshot(lambda message, extras: recorder.error_count, name="old_count")
@icontract.snapshot(lambda message, extras: set(getattr(recorder, "_record", None).extra_errors.keys()) if getattr(recorder, "_record", None) else set(), name="old_keys")
@icontract.ensure(
    lambda OLD, message, extras:
    # No exception: recorder unchanged.
    (recorder.error_count == OLD.old_count and
     (getattr(recorder, "_record", None) is None and OLD.old_keys == set()
      or (getattr(recorder, "_record", None) is not None and set(recorder._record.extra_errors.keys()) == OLD.old_keys))
    )
    or
    # Exception: exactly one new error recorded with correct details, position and extras handling.
    (
        recorder.error_count == OLD.old_count + 1
        and getattr(recorder, "_record", None) is not None
        and (lambda new_keys: (
            len(new_keys) == 1
            and (lambda k: (
                # The recorded details must include the custom/default prefix.
                recorder._record.extra_errors[k].details.startswith((message or "Got an unexpected exception") + ": ")
                # In the original implementation the ExceptionRecord object created
                # by the function keeps its .position as None; if add_error created
                # a new ExceptionRecord (mutant replacing the argument), .position
                # will be the generated position string. Ensure original behavior.
                and recorder._record.extra_errors[k].position is None
                # Extras: if extras argument is truthy it must be preserved exactly;
                # if falsy, allow None or, in case the exception itself is a
                # TestSignal, allow the record's extras to equal the signal's extras.
                and (
                    (bool(extras) and recorder._record.extra_errors[k].extras == extras)
                    or (not bool(extras) and (
                        recorder._record.extra_errors[k].extras is None
                        or (isinstance(recorder._record.extra_errors[k].exception, signals.TestSignal)
                            and recorder._record.extra_errors[k].extras == recorder._record.extra_errors[k].exception.extras)
                    ))
                )
            ))(next(iter(new_keys)))
        ))(set(recorder._record.extra_errors.keys()) - OLD.old_keys)
    )
)
```
[0, 1, 2, 3, 4, 5]
===== 0 =====
```
     yield
   except Exception as e:
     e_record = records.ExceptionRecord(e)
-    if extras:
+    if extras == {}:
       e_record.extras = extras
     msg = message or 'Got an unexpected exception'
     details = '%s: %s' % (msg, e_record.details)
```
```
@contextlib.contextmanager
def expect_no_raises(message=None, extras=None):
  """Expects no exception is raised in a context.

  If the expectation is not met, the test is marked as fail after its
  execution finishes.

  A default message is added to the exception `details`.

  Args:
    message: string, custom message to add to exception's `details`.
    extras: An optional field for extra information to be included in test
      result.
  """
  try:
    yield
  except Exception as e:
    e_record = records.ExceptionRecord(e)
    if extras == {}:
      e_record.extras = extras
    msg = message or 'Got an unexpected exception'
    details = '%s: %s' % (msg, e_record.details)
    logging.exception(details)
    e_record.details = details
    recorder.add_error(e_record)
```
===== 1 =====
```
     yield
   except Exception as e:
     e_record = records.ExceptionRecord(e)
-    if extras:
+    if extras and isinstance(extras, str):
       e_record.extras = extras
     msg = message or 'Got an unexpected exception'
     details = '%s: %s' % (msg, e_record.details)
```
```
@contextlib.contextmanager
def expect_no_raises(message=None, extras=None):
  """Expects no exception is raised in a context.

  If the expectation is not met, the test is marked as fail after its
  execution finishes.

  A default message is added to the exception `details`.

  Args:
    message: string, custom message to add to exception's `details`.
    extras: An optional field for extra information to be included in test
      result.
  """
  try:
    yield
  except Exception as e:
    e_record = records.ExceptionRecord(e)
    if extras and isinstance(extras, str):
      e_record.extras = extras
    msg = message or 'Got an unexpected exception'
    details = '%s: %s' % (msg, e_record.details)
    logging.exception(details)
    e_record.details = details
    recorder.add_error(e_record)
```
===== 2 =====
```
     yield
   except Exception as e:
     e_record = records.ExceptionRecord(e)
-    if extras:
+    if extras is None:
       e_record.extras = extras
     msg = message or 'Got an unexpected exception'
     details = '%s: %s' % (msg, e_record.details)
```
```
@contextlib.contextmanager
def expect_no_raises(message=None, extras=None):
  """Expects no exception is raised in a context.

  If the expectation is not met, the test is marked as fail after its
  execution finishes.

  A default message is added to the exception `details`.

  Args:
    message: string, custom message to add to exception's `details`.
    extras: An optional field for extra information to be included in test
      result.
  """
  try:
    yield
  except Exception as e:
    e_record = records.ExceptionRecord(e)
    if extras is None:
      e_record.extras = extras
    msg = message or 'Got an unexpected exception'
    details = '%s: %s' % (msg, e_record.details)
    logging.exception(details)
    e_record.details = details
    recorder.add_error(e_record)
```
===== 3 =====
```
     yield
   except Exception as e:
     e_record = records.ExceptionRecord(e)
-    if extras:
+    if not extras:
       e_record.extras = extras
     msg = message or 'Got an unexpected exception'
     details = '%s: %s' % (msg, e_record.details)
```
```
@contextlib.contextmanager
def expect_no_raises(message=None, extras=None):
  """Expects no exception is raised in a context.

  If the expectation is not met, the test is marked as fail after its
  execution finishes.

  A default message is added to the exception `details`.

  Args:
    message: string, custom message to add to exception's `details`.
    extras: An optional field for extra information to be included in test
      result.
  """
  try:
    yield
  except Exception as e:
    e_record = records.ExceptionRecord(e)
    if not extras:
      e_record.extras = extras
    msg = message or 'Got an unexpected exception'
    details = '%s: %s' % (msg, e_record.details)
    logging.exception(details)
    e_record.details = details
    recorder.add_error(e_record)
```
===== 4 =====
```
     details = '%s: %s' % (msg, e_record.details)
     logging.exception(details)
     e_record.details = details
-    recorder.add_error(e_record)+    recorder.add_error(e)  # Incorrectly adds the original exception instead of the recorded exception
```
```
@contextlib.contextmanager
def expect_no_raises(message=None, extras=None):
  """Expects no exception is raised in a context.

  If the expectation is not met, the test is marked as fail after its
  execution finishes.

  A default message is added to the exception `details`.

  Args:
    message: string, custom message to add to exception's `details`.
    extras: An optional field for extra information to be included in test
      result.
  """
  try:
    yield
  except Exception as e:
    e_record = records.ExceptionRecord(e)
    if extras:
      e_record.extras = extras
    msg = message or 'Got an unexpected exception'
    details = '%s: %s' % (msg, e_record.details)
    logging.exception(details)
    e_record.details = details
    recorder.add_error(e)  # Incorrectly adds the original exception instead of the recorded exception
```
===== 5 =====
```
     details = '%s: %s' % (msg, e_record.details)
     logging.exception(details)
     e_record.details = details
-    recorder.add_error(e_record)+    recorder.reset_internal_states()  # Resets the recorder instead of adding the error
```
```
@contextlib.contextmanager
def expect_no_raises(message=None, extras=None):
  """Expects no exception is raised in a context.

  If the expectation is not met, the test is marked as fail after its
  execution finishes.

  A default message is added to the exception `details`.

  Args:
    message: string, custom message to add to exception's `details`.
    extras: An optional field for extra information to be included in test
      result.
  """
  try:
    yield
  except Exception as e:
    e_record = records.ExceptionRecord(e)
    if extras:
      e_record.extras = extras
    msg = message or 'Got an unexpected exception'
    details = '%s: %s' % (msg, e_record.details)
    logging.exception(details)
    e_record.details = details
    recorder.reset_internal_states()  # Resets the recorder instead of adding the error
```
