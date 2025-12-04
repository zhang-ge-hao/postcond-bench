https://github.com/google/mobly/blob/6aa58093145669c99c1d6680ab2c1ace42f7f229/./mobly/records.py#L588-L609
```
@icontract.snapshot(lambda self: self.skipped[:], name="old_skipped")
@icontract.snapshot(lambda self: self.executed[:], name="old_executed")
@icontract.snapshot(lambda self: self.failed[:], name="old_failed")
@icontract.snapshot(lambda self: self.passed[:], name="old_passed")
@icontract.snapshot(lambda self: self.error[:], name="old_error")
@icontract.snapshot(lambda self, record: copy.deepcopy(record.extra_errors), name="old_extra_errors")
@icontract.snapshot(lambda self, record: record.result, name="old_result")
@icontract.ensure(
    lambda OLD, self, record:
        (
            record.result == TestResultEnums.TEST_RESULT_SKIP
            and self.skipped == OLD.old_skipped + [record]
            and self.executed == OLD.old_executed
            and self.failed == OLD.old_failed
            and self.passed == OLD.old_passed
            and self.error == OLD.old_error
        ) or (
            record.result == TestResultEnums.TEST_RESULT_FAIL
            and self.executed == OLD.old_executed + [record]
            and self.failed == OLD.old_failed + [record]
            and self.passed == OLD.old_passed
            and self.error == OLD.old_error
            and self.skipped == OLD.old_skipped
        ) or (
            record.result == TestResultEnums.TEST_RESULT_PASS
            and self.executed == OLD.old_executed + [record]
            and self.passed == OLD.old_passed + [record]
            and self.failed == OLD.old_failed
            and self.error == OLD.old_error
            and self.skipped == OLD.old_skipped
        ) or (
            record.result not in (
                TestResultEnums.TEST_RESULT_SKIP,
                TestResultEnums.TEST_RESULT_FAIL,
                TestResultEnums.TEST_RESULT_PASS,
            )
            and self.executed == OLD.old_executed + [record]
            and self.error == OLD.old_error + [record]
            and self.failed == OLD.old_failed
            and self.passed == OLD.old_passed
            and self.skipped == OLD.old_skipped
        )
)
@icontract.ensure(
    lambda OLD, self, record:
        (
            (not OLD.old_extra_errors and record.result == OLD.old_result)
        )
        or (
            OLD.old_extra_errors and (
                (
                    OLD.old_result == TestResultEnums.TEST_RESULT_FAIL
                    and record.result == TestResultEnums.TEST_RESULT_FAIL
                )
                or
                (
                    OLD.old_result != TestResultEnums.TEST_RESULT_FAIL
                    and record.result == TestResultEnums.TEST_RESULT_ERROR
                )
            )
        )
)
```
```
@icontract.snapshot(lambda self: self.skipped[:], name="old_skipped")
@icontract.snapshot(lambda self: self.executed[:], name="old_executed")
@icontract.snapshot(lambda self: self.failed[:], name="old_failed")
@icontract.snapshot(lambda self: self.passed[:], name="old_passed")
@icontract.snapshot(lambda self: self.error[:], name="old_error")
@icontract.ensure(lambda OLD, self, record: (
    record.result == TestResultEnums.TEST_RESULT_SKIP
    and self.skipped == OLD.old_skipped + [record]
    and self.executed == OLD.old_executed
    and self.failed == OLD.old_failed
    and self.passed == OLD.old_passed
    and self.error == OLD.old_error
) or (
    record.result != TestResultEnums.TEST_RESULT_SKIP
    and self.executed == OLD.old_executed + [record]
    and self.skipped == OLD.old_skipped
    and (
        (self.failed == OLD.old_failed + [record]
         and self.passed == OLD.old_passed
         and self.error == OLD.old_error)
        or
        (self.passed == OLD.old_passed + [record]
         and self.failed == OLD.old_failed
         and self.error == OLD.old_error)
        or
        (self.error == OLD.old_error + [record]
         and self.failed == OLD.old_failed
         and self.passed == OLD.old_passed)
    )
))
```
[0, 17, 18, 19, 20, 21, 23, 31, 32]
===== 0 =====
```
     Args:
       record: A test record object to add.
     """
-    record.update_record()
+    record.result = TestResultEnums.TEST_RESULT_PASS  # Incorrectly forces the result to PASS
     if record.result == TestResultEnums.TEST_RESULT_SKIP:
       self.skipped.append(record)
       return
```
```
  def add_record(self, record):
    """Adds a test record to test result.

    A record is considered executed once it's added to the test result.

    Adding the record finalizes the content of a record, so no change
    should be made to the record afterwards.

    Args:
      record: A test record object to add.
    """
    record.result = TestResultEnums.TEST_RESULT_PASS  # Incorrectly forces the result to PASS
    if record.result == TestResultEnums.TEST_RESULT_SKIP:
      self.skipped.append(record)
      return
    self.executed.append(record)
    if record.result == TestResultEnums.TEST_RESULT_FAIL:
      self.failed.append(record)
    elif record.result == TestResultEnums.TEST_RESULT_PASS:
      self.passed.append(record)
    else:
      self.error.append(record)
```
===== 17 =====
```
       self.skipped.append(record)
       return
     self.executed.append(record)
-    if record.result == TestResultEnums.TEST_RESULT_FAIL:
+    if record.result != TestResultEnums.TEST_RESULT_PASS:
       self.failed.append(record)
     elif record.result == TestResultEnums.TEST_RESULT_PASS:
       self.passed.append(record)
```
```
  def add_record(self, record):
    """Adds a test record to test result.

    A record is considered executed once it's added to the test result.

    Adding the record finalizes the content of a record, so no change
    should be made to the record afterwards.

    Args:
      record: A test record object to add.
    """
    record.update_record()
    if record.result == TestResultEnums.TEST_RESULT_SKIP:
      self.skipped.append(record)
      return
    self.executed.append(record)
    if record.result != TestResultEnums.TEST_RESULT_PASS:
      self.failed.append(record)
    elif record.result == TestResultEnums.TEST_RESULT_PASS:
      self.passed.append(record)
    else:
      self.error.append(record)
```
===== 18 =====
```
       self.skipped.append(record)
       return
     self.executed.append(record)
-    if record.result == TestResultEnums.TEST_RESULT_FAIL:
+    if record.result == TestResultEnums.TEST_RESULT_ERROR:
       self.failed.append(record)
     elif record.result == TestResultEnums.TEST_RESULT_PASS:
       self.passed.append(record)
```
```
  def add_record(self, record):
    """Adds a test record to test result.

    A record is considered executed once it's added to the test result.

    Adding the record finalizes the content of a record, so no change
    should be made to the record afterwards.

    Args:
      record: A test record object to add.
    """
    record.update_record()
    if record.result == TestResultEnums.TEST_RESULT_SKIP:
      self.skipped.append(record)
      return
    self.executed.append(record)
    if record.result == TestResultEnums.TEST_RESULT_ERROR:
      self.failed.append(record)
    elif record.result == TestResultEnums.TEST_RESULT_PASS:
      self.passed.append(record)
    else:
      self.error.append(record)
```
===== 19 =====
```
       self.skipped.append(record)
       return
     self.executed.append(record)
-    if record.result == TestResultEnums.TEST_RESULT_FAIL:
+    if record.result == TestResultEnums.TEST_RESULT_PASS or record.result == TestResultEnums.TEST_RESULT_FAIL:
       self.failed.append(record)
     elif record.result == TestResultEnums.TEST_RESULT_PASS:
       self.passed.append(record)
```
```
  def add_record(self, record):
    """Adds a test record to test result.

    A record is considered executed once it's added to the test result.

    Adding the record finalizes the content of a record, so no change
    should be made to the record afterwards.

    Args:
      record: A test record object to add.
    """
    record.update_record()
    if record.result == TestResultEnums.TEST_RESULT_SKIP:
      self.skipped.append(record)
      return
    self.executed.append(record)
    if record.result == TestResultEnums.TEST_RESULT_PASS or record.result == TestResultEnums.TEST_RESULT_FAIL:
      self.failed.append(record)
    elif record.result == TestResultEnums.TEST_RESULT_PASS:
      self.passed.append(record)
    else:
      self.error.append(record)
```
===== 20 =====
```
       self.skipped.append(record)
       return
     self.executed.append(record)
-    if record.result == TestResultEnums.TEST_RESULT_FAIL:
+    if record.result == TestResultEnums.TEST_RESULT_SKIP:
       self.failed.append(record)
     elif record.result == TestResultEnums.TEST_RESULT_PASS:
       self.passed.append(record)
```
```
  def add_record(self, record):
    """Adds a test record to test result.

    A record is considered executed once it's added to the test result.

    Adding the record finalizes the content of a record, so no change
    should be made to the record afterwards.

    Args:
      record: A test record object to add.
    """
    record.update_record()
    if record.result == TestResultEnums.TEST_RESULT_SKIP:
      self.skipped.append(record)
      return
    self.executed.append(record)
    if record.result == TestResultEnums.TEST_RESULT_SKIP:
      self.failed.append(record)
    elif record.result == TestResultEnums.TEST_RESULT_PASS:
      self.passed.append(record)
    else:
      self.error.append(record)
```
===== 21 =====
```
       return
     self.executed.append(record)
     if record.result == TestResultEnums.TEST_RESULT_FAIL:
-      self.failed.append(record)
+      self.error.append(record)  # Incorrectly adds failed record to error list
     elif record.result == TestResultEnums.TEST_RESULT_PASS:
       self.passed.append(record)
     else:
```
```
  def add_record(self, record):
    """Adds a test record to test result.

    A record is considered executed once it's added to the test result.

    Adding the record finalizes the content of a record, so no change
    should be made to the record afterwards.

    Args:
      record: A test record object to add.
    """
    record.update_record()
    if record.result == TestResultEnums.TEST_RESULT_SKIP:
      self.skipped.append(record)
      return
    self.executed.append(record)
    if record.result == TestResultEnums.TEST_RESULT_FAIL:
      self.error.append(record)  # Incorrectly adds failed record to error list
    elif record.result == TestResultEnums.TEST_RESULT_PASS:
      self.passed.append(record)
    else:
      self.error.append(record)
```
===== 23 =====
```
       return
     self.executed.append(record)
     if record.result == TestResultEnums.TEST_RESULT_FAIL:
-      self.failed.append(record)
+      self.passed.append(record)  # Incorrectly adds failed record to passed list
     elif record.result == TestResultEnums.TEST_RESULT_PASS:
       self.passed.append(record)
     else:
```
```
  def add_record(self, record):
    """Adds a test record to test result.

    A record is considered executed once it's added to the test result.

    Adding the record finalizes the content of a record, so no change
    should be made to the record afterwards.

    Args:
      record: A test record object to add.
    """
    record.update_record()
    if record.result == TestResultEnums.TEST_RESULT_SKIP:
      self.skipped.append(record)
      return
    self.executed.append(record)
    if record.result == TestResultEnums.TEST_RESULT_FAIL:
      self.passed.append(record)  # Incorrectly adds failed record to passed list
    elif record.result == TestResultEnums.TEST_RESULT_PASS:
      self.passed.append(record)
    else:
      self.error.append(record)
```
===== 31 =====
```
     elif record.result == TestResultEnums.TEST_RESULT_PASS:
       self.passed.append(record)
     else:
-      self.error.append(record)+      self.failed.append(record)  # Incorrectly appending to the failed list instead of the error list
```
```
  def add_record(self, record):
    """Adds a test record to test result.

    A record is considered executed once it's added to the test result.

    Adding the record finalizes the content of a record, so no change
    should be made to the record afterwards.

    Args:
      record: A test record object to add.
    """
    record.update_record()
    if record.result == TestResultEnums.TEST_RESULT_SKIP:
      self.skipped.append(record)
      return
    self.executed.append(record)
    if record.result == TestResultEnums.TEST_RESULT_FAIL:
      self.failed.append(record)
    elif record.result == TestResultEnums.TEST_RESULT_PASS:
      self.passed.append(record)
    else:
      self.failed.append(record)  # Incorrectly appending to the failed list instead of the error list
```
===== 32 =====
```
     elif record.result == TestResultEnums.TEST_RESULT_PASS:
       self.passed.append(record)
     else:
-      self.error.append(record)+      self.passed.append(record)  # Incorrectly appending to the passed list instead of the error list
```
```
  def add_record(self, record):
    """Adds a test record to test result.

    A record is considered executed once it's added to the test result.

    Adding the record finalizes the content of a record, so no change
    should be made to the record afterwards.

    Args:
      record: A test record object to add.
    """
    record.update_record()
    if record.result == TestResultEnums.TEST_RESULT_SKIP:
      self.skipped.append(record)
      return
    self.executed.append(record)
    if record.result == TestResultEnums.TEST_RESULT_FAIL:
      self.failed.append(record)
    elif record.result == TestResultEnums.TEST_RESULT_PASS:
      self.passed.append(record)
    else:
      self.passed.append(record)  # Incorrectly appending to the passed list instead of the error list
```
