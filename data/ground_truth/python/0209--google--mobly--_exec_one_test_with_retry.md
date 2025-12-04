https://github.com/google/mobly/blob/6aa58093145669c99c1d6680ab2c1ace42f7f229/./mobly/base_test.py#L679-L709
```
@icontract.snapshot(
    lambda self, test_name, test_method, max_count: [
        record
        for record in self.results.executed
        if record.test_name == test_name
        or record.test_name.startswith(f"{test_name}_retry_")
    ],
    name="records",
)
@icontract.ensure(
    lambda OLD, self, test_name, test_method, max_count: (
        1
        <= (
            len([
                record
                for record in self.results.executed
                if record.test_name == test_name
                or record.test_name.startswith(f"{test_name}_retry_")
            ])
            - len(OLD.records)
        )
        <= max_count
    )
)
@icontract.ensure(
    lambda OLD, self, test_name, test_method, max_count: (
        (lambda new_records: all(
            record.result
            in (
                records.TestResultEnums.TEST_RESULT_FAIL,
                records.TestResultEnums.TEST_RESULT_ERROR,
            )
            for record in new_records[:-1]
        ))(
            [
                record
                for record in self.results.executed
                if record.test_name == test_name
                or record.test_name.startswith(f"{test_name}_retry_")
            ][len(OLD.records):]
        )
    )
)
@icontract.ensure(
    lambda OLD, self, test_name, test_method, max_count: (
        (lambda new_records: (
            len(new_records) == 0
            or (
                new_records[-1].result
                in (
                    records.TestResultEnums.TEST_RESULT_FAIL,
                    records.TestResultEnums.TEST_RESULT_ERROR,
                )
                and len(new_records) == max_count
            )
            or (
                new_records[-1].result
                not in (
                    records.TestResultEnums.TEST_RESULT_FAIL,
                    records.TestResultEnums.TEST_RESULT_ERROR,
                )
            )
        ))(
            [
                record
                for record in self.results.executed
                if record.test_name == test_name
                or record.test_name.startswith(f"{test_name}_retry_")
            ][len(OLD.records):]
        )
    )
)
@icontract.ensure(
    lambda OLD, self, test_name, test_method, max_count: (
        (lambda new_records: (
            len(new_records) == 0
            or (
                new_records[0].test_name == test_name
                and all(
                    (lambda m: (
                        m is not None
                        and int(m.group(1)) == idx
                        and record.retry_parent is new_records[idx - 1]
                        and record.parent
                        == (new_records[idx - 1], records.TestParentType.RETRY)
                    ))(
                        re.fullmatch(
                            rf"{re.escape(test_name)}_retry_(\d+)",
                            record.test_name,
                        )
                    )
                    for idx, record in enumerate(new_records[1:], start=1)
                )
            )
        ))(
            [
                record
                for record in self.results.executed
                if record.test_name == test_name
                or record.test_name.startswith(f"{test_name}_retry_")
            ][len(OLD.records):]
        )
    )
)
```
```
None
```
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17]
===== 0 =====
```
 
     previous_record = self.exec_one_test(test_name, test_method)
 
-    if not should_retry(previous_record):
+    if previous_record.result == records.TestResultEnums.TEST_RESULT_SKIP:
       return
 
     for i in range(max_count - 1):
```
```
  def _exec_one_test_with_retry(self, test_name, test_method, max_count):
    """Executes one test and retry the test if needed.

    Repeatedly execute a test case until it passes or the maximum count of
    iteration has been reached.

    Args:
      test_name: string, Name of the test.
      test_method: function, The test method to execute.
      max_count: int, the maximum number of iterations to execute the test for.
    """

    def should_retry(record):
      return record.result in [
          records.TestResultEnums.TEST_RESULT_FAIL,
          records.TestResultEnums.TEST_RESULT_ERROR,
      ]

    previous_record = self.exec_one_test(test_name, test_method)

    if previous_record.result == records.TestResultEnums.TEST_RESULT_SKIP:
      return

    for i in range(max_count - 1):
      retry_name = f'{test_name}_retry_{i+1}'
      new_record = records.TestResultRecord(retry_name, self.TAG)
      new_record.retry_parent = previous_record
      new_record.parent = (previous_record, records.TestParentType.RETRY)
      previous_record = self.exec_one_test(retry_name, test_method, new_record)
      if not should_retry(previous_record):
        break
```
===== 1 =====
```
 
     previous_record = self.exec_one_test(test_name, test_method)
 
-    if not should_retry(previous_record):
+    if previous_record.result in [records.TestResultEnums.TEST_RESULT_FAIL]:
       return
 
     for i in range(max_count - 1):
```
```
  def _exec_one_test_with_retry(self, test_name, test_method, max_count):
    """Executes one test and retry the test if needed.

    Repeatedly execute a test case until it passes or the maximum count of
    iteration has been reached.

    Args:
      test_name: string, Name of the test.
      test_method: function, The test method to execute.
      max_count: int, the maximum number of iterations to execute the test for.
    """

    def should_retry(record):
      return record.result in [
          records.TestResultEnums.TEST_RESULT_FAIL,
          records.TestResultEnums.TEST_RESULT_ERROR,
      ]

    previous_record = self.exec_one_test(test_name, test_method)

    if previous_record.result in [records.TestResultEnums.TEST_RESULT_FAIL]:
      return

    for i in range(max_count - 1):
      retry_name = f'{test_name}_retry_{i+1}'
      new_record = records.TestResultRecord(retry_name, self.TAG)
      new_record.retry_parent = previous_record
      new_record.parent = (previous_record, records.TestParentType.RETRY)
      previous_record = self.exec_one_test(retry_name, test_method, new_record)
      if not should_retry(previous_record):
        break
```
===== 2 =====
```
     if not should_retry(previous_record):
       return
 
-    for i in range(max_count - 1):
+    for i in range(1, max_count):  # This will skip the first iteration, potentially missing a test execution.
       retry_name = f'{test_name}_retry_{i+1}'
       new_record = records.TestResultRecord(retry_name, self.TAG)
       new_record.retry_parent = previous_record
```
```
  def _exec_one_test_with_retry(self, test_name, test_method, max_count):
    """Executes one test and retry the test if needed.

    Repeatedly execute a test case until it passes or the maximum count of
    iteration has been reached.

    Args:
      test_name: string, Name of the test.
      test_method: function, The test method to execute.
      max_count: int, the maximum number of iterations to execute the test for.
    """

    def should_retry(record):
      return record.result in [
          records.TestResultEnums.TEST_RESULT_FAIL,
          records.TestResultEnums.TEST_RESULT_ERROR,
      ]

    previous_record = self.exec_one_test(test_name, test_method)

    if not should_retry(previous_record):
      return

    for i in range(1, max_count):  # This will skip the first iteration, potentially missing a test execution.
      retry_name = f'{test_name}_retry_{i+1}'
      new_record = records.TestResultRecord(retry_name, self.TAG)
      new_record.retry_parent = previous_record
      new_record.parent = (previous_record, records.TestParentType.RETRY)
      previous_record = self.exec_one_test(retry_name, test_method, new_record)
      if not should_retry(previous_record):
        break
```
===== 3 =====
```
     if not should_retry(previous_record):
       return
 
-    for i in range(max_count - 1):
+    for i in range(max_count + 1):  # This will also cause an extra iteration, leading to incorrect behavior.
       retry_name = f'{test_name}_retry_{i+1}'
       new_record = records.TestResultRecord(retry_name, self.TAG)
       new_record.retry_parent = previous_record
```
```
  def _exec_one_test_with_retry(self, test_name, test_method, max_count):
    """Executes one test and retry the test if needed.

    Repeatedly execute a test case until it passes or the maximum count of
    iteration has been reached.

    Args:
      test_name: string, Name of the test.
      test_method: function, The test method to execute.
      max_count: int, the maximum number of iterations to execute the test for.
    """

    def should_retry(record):
      return record.result in [
          records.TestResultEnums.TEST_RESULT_FAIL,
          records.TestResultEnums.TEST_RESULT_ERROR,
      ]

    previous_record = self.exec_one_test(test_name, test_method)

    if not should_retry(previous_record):
      return

    for i in range(max_count + 1):  # This will also cause an extra iteration, leading to incorrect behavior.
      retry_name = f'{test_name}_retry_{i+1}'
      new_record = records.TestResultRecord(retry_name, self.TAG)
      new_record.retry_parent = previous_record
      new_record.parent = (previous_record, records.TestParentType.RETRY)
      previous_record = self.exec_one_test(retry_name, test_method, new_record)
      if not should_retry(previous_record):
        break
```
===== 4 =====
```
     if not should_retry(previous_record):
       return
 
-    for i in range(max_count - 1):
+    for i in range(max_count - 2):  # This will cause two fewer iterations than intended, leading to missed tests.
       retry_name = f'{test_name}_retry_{i+1}'
       new_record = records.TestResultRecord(retry_name, self.TAG)
       new_record.retry_parent = previous_record
```
```
  def _exec_one_test_with_retry(self, test_name, test_method, max_count):
    """Executes one test and retry the test if needed.

    Repeatedly execute a test case until it passes or the maximum count of
    iteration has been reached.

    Args:
      test_name: string, Name of the test.
      test_method: function, The test method to execute.
      max_count: int, the maximum number of iterations to execute the test for.
    """

    def should_retry(record):
      return record.result in [
          records.TestResultEnums.TEST_RESULT_FAIL,
          records.TestResultEnums.TEST_RESULT_ERROR,
      ]

    previous_record = self.exec_one_test(test_name, test_method)

    if not should_retry(previous_record):
      return

    for i in range(max_count - 2):  # This will cause two fewer iterations than intended, leading to missed tests.
      retry_name = f'{test_name}_retry_{i+1}'
      new_record = records.TestResultRecord(retry_name, self.TAG)
      new_record.retry_parent = previous_record
      new_record.parent = (previous_record, records.TestParentType.RETRY)
      previous_record = self.exec_one_test(retry_name, test_method, new_record)
      if not should_retry(previous_record):
        break
```
===== 5 =====
```
     if not should_retry(previous_record):
       return
 
-    for i in range(max_count - 1):
+    for i in range(max_count // 2):  # This will only execute half the intended iterations, leading to incomplete testing.
       retry_name = f'{test_name}_retry_{i+1}'
       new_record = records.TestResultRecord(retry_name, self.TAG)
       new_record.retry_parent = previous_record
```
```
  def _exec_one_test_with_retry(self, test_name, test_method, max_count):
    """Executes one test and retry the test if needed.

    Repeatedly execute a test case until it passes or the maximum count of
    iteration has been reached.

    Args:
      test_name: string, Name of the test.
      test_method: function, The test method to execute.
      max_count: int, the maximum number of iterations to execute the test for.
    """

    def should_retry(record):
      return record.result in [
          records.TestResultEnums.TEST_RESULT_FAIL,
          records.TestResultEnums.TEST_RESULT_ERROR,
      ]

    previous_record = self.exec_one_test(test_name, test_method)

    if not should_retry(previous_record):
      return

    for i in range(max_count // 2):  # This will only execute half the intended iterations, leading to incomplete testing.
      retry_name = f'{test_name}_retry_{i+1}'
      new_record = records.TestResultRecord(retry_name, self.TAG)
      new_record.retry_parent = previous_record
      new_record.parent = (previous_record, records.TestParentType.RETRY)
      previous_record = self.exec_one_test(retry_name, test_method, new_record)
      if not should_retry(previous_record):
        break
```
===== 6 =====
```
     if not should_retry(previous_record):
       return
 
-    for i in range(max_count - 1):
+    for i in range(max_count):  # This will cause one extra iteration, leading to an off-by-one error.
       retry_name = f'{test_name}_retry_{i+1}'
       new_record = records.TestResultRecord(retry_name, self.TAG)
       new_record.retry_parent = previous_record
```
```
  def _exec_one_test_with_retry(self, test_name, test_method, max_count):
    """Executes one test and retry the test if needed.

    Repeatedly execute a test case until it passes or the maximum count of
    iteration has been reached.

    Args:
      test_name: string, Name of the test.
      test_method: function, The test method to execute.
      max_count: int, the maximum number of iterations to execute the test for.
    """

    def should_retry(record):
      return record.result in [
          records.TestResultEnums.TEST_RESULT_FAIL,
          records.TestResultEnums.TEST_RESULT_ERROR,
      ]

    previous_record = self.exec_one_test(test_name, test_method)

    if not should_retry(previous_record):
      return

    for i in range(max_count):  # This will cause one extra iteration, leading to an off-by-one error.
      retry_name = f'{test_name}_retry_{i+1}'
      new_record = records.TestResultRecord(retry_name, self.TAG)
      new_record.retry_parent = previous_record
      new_record.parent = (previous_record, records.TestParentType.RETRY)
      previous_record = self.exec_one_test(retry_name, test_method, new_record)
      if not should_retry(previous_record):
        break
```
===== 7 =====
```
       return
 
     for i in range(max_count - 1):
-      retry_name = f'{test_name}_retry_{i+1}'
+      retry_name = f'retry_{i+1}_{test_name}'
       new_record = records.TestResultRecord(retry_name, self.TAG)
       new_record.retry_parent = previous_record
       new_record.parent = (previous_record, records.TestParentType.RETRY)
```
```
  def _exec_one_test_with_retry(self, test_name, test_method, max_count):
    """Executes one test and retry the test if needed.

    Repeatedly execute a test case until it passes or the maximum count of
    iteration has been reached.

    Args:
      test_name: string, Name of the test.
      test_method: function, The test method to execute.
      max_count: int, the maximum number of iterations to execute the test for.
    """

    def should_retry(record):
      return record.result in [
          records.TestResultEnums.TEST_RESULT_FAIL,
          records.TestResultEnums.TEST_RESULT_ERROR,
      ]

    previous_record = self.exec_one_test(test_name, test_method)

    if not should_retry(previous_record):
      return

    for i in range(max_count - 1):
      retry_name = f'retry_{i+1}_{test_name}'
      new_record = records.TestResultRecord(retry_name, self.TAG)
      new_record.retry_parent = previous_record
      new_record.parent = (previous_record, records.TestParentType.RETRY)
      previous_record = self.exec_one_test(retry_name, test_method, new_record)
      if not should_retry(previous_record):
        break
```
===== 8 =====
```
       return
 
     for i in range(max_count - 1):
-      retry_name = f'{test_name}_retry_{i+1}'
+      retry_name = f'{test_name}_attempt_{i+1}'
       new_record = records.TestResultRecord(retry_name, self.TAG)
       new_record.retry_parent = previous_record
       new_record.parent = (previous_record, records.TestParentType.RETRY)
```
```
  def _exec_one_test_with_retry(self, test_name, test_method, max_count):
    """Executes one test and retry the test if needed.

    Repeatedly execute a test case until it passes or the maximum count of
    iteration has been reached.

    Args:
      test_name: string, Name of the test.
      test_method: function, The test method to execute.
      max_count: int, the maximum number of iterations to execute the test for.
    """

    def should_retry(record):
      return record.result in [
          records.TestResultEnums.TEST_RESULT_FAIL,
          records.TestResultEnums.TEST_RESULT_ERROR,
      ]

    previous_record = self.exec_one_test(test_name, test_method)

    if not should_retry(previous_record):
      return

    for i in range(max_count - 1):
      retry_name = f'{test_name}_attempt_{i+1}'
      new_record = records.TestResultRecord(retry_name, self.TAG)
      new_record.retry_parent = previous_record
      new_record.parent = (previous_record, records.TestParentType.RETRY)
      previous_record = self.exec_one_test(retry_name, test_method, new_record)
      if not should_retry(previous_record):
        break
```
===== 9 =====
```
       return
 
     for i in range(max_count - 1):
-      retry_name = f'{test_name}_retry_{i+1}'
+      retry_name = f'{test_name}_retry'
       new_record = records.TestResultRecord(retry_name, self.TAG)
       new_record.retry_parent = previous_record
       new_record.parent = (previous_record, records.TestParentType.RETRY)
```
```
  def _exec_one_test_with_retry(self, test_name, test_method, max_count):
    """Executes one test and retry the test if needed.

    Repeatedly execute a test case until it passes or the maximum count of
    iteration has been reached.

    Args:
      test_name: string, Name of the test.
      test_method: function, The test method to execute.
      max_count: int, the maximum number of iterations to execute the test for.
    """

    def should_retry(record):
      return record.result in [
          records.TestResultEnums.TEST_RESULT_FAIL,
          records.TestResultEnums.TEST_RESULT_ERROR,
      ]

    previous_record = self.exec_one_test(test_name, test_method)

    if not should_retry(previous_record):
      return

    for i in range(max_count - 1):
      retry_name = f'{test_name}_retry'
      new_record = records.TestResultRecord(retry_name, self.TAG)
      new_record.retry_parent = previous_record
      new_record.parent = (previous_record, records.TestParentType.RETRY)
      previous_record = self.exec_one_test(retry_name, test_method, new_record)
      if not should_retry(previous_record):
        break
```
===== 10 =====
```
       return
 
     for i in range(max_count - 1):
-      retry_name = f'{test_name}_retry_{i+1}'
+      retry_name = f'{test_name}_retry_{i}'
       new_record = records.TestResultRecord(retry_name, self.TAG)
       new_record.retry_parent = previous_record
       new_record.parent = (previous_record, records.TestParentType.RETRY)
```
```
  def _exec_one_test_with_retry(self, test_name, test_method, max_count):
    """Executes one test and retry the test if needed.

    Repeatedly execute a test case until it passes or the maximum count of
    iteration has been reached.

    Args:
      test_name: string, Name of the test.
      test_method: function, The test method to execute.
      max_count: int, the maximum number of iterations to execute the test for.
    """

    def should_retry(record):
      return record.result in [
          records.TestResultEnums.TEST_RESULT_FAIL,
          records.TestResultEnums.TEST_RESULT_ERROR,
      ]

    previous_record = self.exec_one_test(test_name, test_method)

    if not should_retry(previous_record):
      return

    for i in range(max_count - 1):
      retry_name = f'{test_name}_retry_{i}'
      new_record = records.TestResultRecord(retry_name, self.TAG)
      new_record.retry_parent = previous_record
      new_record.parent = (previous_record, records.TestParentType.RETRY)
      previous_record = self.exec_one_test(retry_name, test_method, new_record)
      if not should_retry(previous_record):
        break
```
===== 11 =====
```
       return
 
     for i in range(max_count - 1):
-      retry_name = f'{test_name}_retry_{i+1}'
+      retry_name = f'{test_name}_{i+1}_retry'
       new_record = records.TestResultRecord(retry_name, self.TAG)
       new_record.retry_parent = previous_record
       new_record.parent = (previous_record, records.TestParentType.RETRY)
```
```
  def _exec_one_test_with_retry(self, test_name, test_method, max_count):
    """Executes one test and retry the test if needed.

    Repeatedly execute a test case until it passes or the maximum count of
    iteration has been reached.

    Args:
      test_name: string, Name of the test.
      test_method: function, The test method to execute.
      max_count: int, the maximum number of iterations to execute the test for.
    """

    def should_retry(record):
      return record.result in [
          records.TestResultEnums.TEST_RESULT_FAIL,
          records.TestResultEnums.TEST_RESULT_ERROR,
      ]

    previous_record = self.exec_one_test(test_name, test_method)

    if not should_retry(previous_record):
      return

    for i in range(max_count - 1):
      retry_name = f'{test_name}_{i+1}_retry'
      new_record = records.TestResultRecord(retry_name, self.TAG)
      new_record.retry_parent = previous_record
      new_record.parent = (previous_record, records.TestParentType.RETRY)
      previous_record = self.exec_one_test(retry_name, test_method, new_record)
      if not should_retry(previous_record):
        break
```
===== 12 =====
```
 
     for i in range(max_count - 1):
       retry_name = f'{test_name}_retry_{i+1}'
-      new_record = records.TestResultRecord(retry_name, self.TAG)
+      new_record = records.TestResultRecord(test_name, self.TAG)  # Using the original test name instead of the retry name.
       new_record.retry_parent = previous_record
       new_record.parent = (previous_record, records.TestParentType.RETRY)
       previous_record = self.exec_one_test(retry_name, test_method, new_record)
```
```
  def _exec_one_test_with_retry(self, test_name, test_method, max_count):
    """Executes one test and retry the test if needed.

    Repeatedly execute a test case until it passes or the maximum count of
    iteration has been reached.

    Args:
      test_name: string, Name of the test.
      test_method: function, The test method to execute.
      max_count: int, the maximum number of iterations to execute the test for.
    """

    def should_retry(record):
      return record.result in [
          records.TestResultEnums.TEST_RESULT_FAIL,
          records.TestResultEnums.TEST_RESULT_ERROR,
      ]

    previous_record = self.exec_one_test(test_name, test_method)

    if not should_retry(previous_record):
      return

    for i in range(max_count - 1):
      retry_name = f'{test_name}_retry_{i+1}'
      new_record = records.TestResultRecord(test_name, self.TAG)  # Using the original test name instead of the retry name.
      new_record.retry_parent = previous_record
      new_record.parent = (previous_record, records.TestParentType.RETRY)
      previous_record = self.exec_one_test(retry_name, test_method, new_record)
      if not should_retry(previous_record):
        break
```
===== 13 =====
```
       new_record = records.TestResultRecord(retry_name, self.TAG)
       new_record.retry_parent = previous_record
       new_record.parent = (previous_record, records.TestParentType.RETRY)
-      previous_record = self.exec_one_test(retry_name, test_method, new_record)
+      previous_record = self.exec_one_test(retry_name, None, new_record)
       if not should_retry(previous_record):
         break
```
```
  def _exec_one_test_with_retry(self, test_name, test_method, max_count):
    """Executes one test and retry the test if needed.

    Repeatedly execute a test case until it passes or the maximum count of
    iteration has been reached.

    Args:
      test_name: string, Name of the test.
      test_method: function, The test method to execute.
      max_count: int, the maximum number of iterations to execute the test for.
    """

    def should_retry(record):
      return record.result in [
          records.TestResultEnums.TEST_RESULT_FAIL,
          records.TestResultEnums.TEST_RESULT_ERROR,
      ]

    previous_record = self.exec_one_test(test_name, test_method)

    if not should_retry(previous_record):
      return

    for i in range(max_count - 1):
      retry_name = f'{test_name}_retry_{i+1}'
      new_record = records.TestResultRecord(retry_name, self.TAG)
      new_record.retry_parent = previous_record
      new_record.parent = (previous_record, records.TestParentType.RETRY)
      previous_record = self.exec_one_test(retry_name, None, new_record)
      if not should_retry(previous_record):
        break
```
===== 14 =====
```
       new_record = records.TestResultRecord(retry_name, self.TAG)
       new_record.retry_parent = previous_record
       new_record.parent = (previous_record, records.TestParentType.RETRY)
-      previous_record = self.exec_one_test(retry_name, test_method, new_record)
+      previous_record = self.exec_one_test(retry_name, test_method)
       if not should_retry(previous_record):
         break
```
```
  def _exec_one_test_with_retry(self, test_name, test_method, max_count):
    """Executes one test and retry the test if needed.

    Repeatedly execute a test case until it passes or the maximum count of
    iteration has been reached.

    Args:
      test_name: string, Name of the test.
      test_method: function, The test method to execute.
      max_count: int, the maximum number of iterations to execute the test for.
    """

    def should_retry(record):
      return record.result in [
          records.TestResultEnums.TEST_RESULT_FAIL,
          records.TestResultEnums.TEST_RESULT_ERROR,
      ]

    previous_record = self.exec_one_test(test_name, test_method)

    if not should_retry(previous_record):
      return

    for i in range(max_count - 1):
      retry_name = f'{test_name}_retry_{i+1}'
      new_record = records.TestResultRecord(retry_name, self.TAG)
      new_record.retry_parent = previous_record
      new_record.parent = (previous_record, records.TestParentType.RETRY)
      previous_record = self.exec_one_test(retry_name, test_method)
      if not should_retry(previous_record):
        break
```
===== 15 =====
```
       new_record = records.TestResultRecord(retry_name, self.TAG)
       new_record.retry_parent = previous_record
       new_record.parent = (previous_record, records.TestParentType.RETRY)
-      previous_record = self.exec_one_test(retry_name, test_method, new_record)
+      previous_record = self.exec_one_test(retry_name, test_method, None)
       if not should_retry(previous_record):
         break
```
```
  def _exec_one_test_with_retry(self, test_name, test_method, max_count):
    """Executes one test and retry the test if needed.

    Repeatedly execute a test case until it passes or the maximum count of
    iteration has been reached.

    Args:
      test_name: string, Name of the test.
      test_method: function, The test method to execute.
      max_count: int, the maximum number of iterations to execute the test for.
    """

    def should_retry(record):
      return record.result in [
          records.TestResultEnums.TEST_RESULT_FAIL,
          records.TestResultEnums.TEST_RESULT_ERROR,
      ]

    previous_record = self.exec_one_test(test_name, test_method)

    if not should_retry(previous_record):
      return

    for i in range(max_count - 1):
      retry_name = f'{test_name}_retry_{i+1}'
      new_record = records.TestResultRecord(retry_name, self.TAG)
      new_record.retry_parent = previous_record
      new_record.parent = (previous_record, records.TestParentType.RETRY)
      previous_record = self.exec_one_test(retry_name, test_method, None)
      if not should_retry(previous_record):
        break
```
===== 16 =====
```
       new_record = records.TestResultRecord(retry_name, self.TAG)
       new_record.retry_parent = previous_record
       new_record.parent = (previous_record, records.TestParentType.RETRY)
-      previous_record = self.exec_one_test(retry_name, test_method, new_record)
+      previous_record = self.exec_one_test(retry_name, test_method, previous_record)
       if not should_retry(previous_record):
         break
```
```
  def _exec_one_test_with_retry(self, test_name, test_method, max_count):
    """Executes one test and retry the test if needed.

    Repeatedly execute a test case until it passes or the maximum count of
    iteration has been reached.

    Args:
      test_name: string, Name of the test.
      test_method: function, The test method to execute.
      max_count: int, the maximum number of iterations to execute the test for.
    """

    def should_retry(record):
      return record.result in [
          records.TestResultEnums.TEST_RESULT_FAIL,
          records.TestResultEnums.TEST_RESULT_ERROR,
      ]

    previous_record = self.exec_one_test(test_name, test_method)

    if not should_retry(previous_record):
      return

    for i in range(max_count - 1):
      retry_name = f'{test_name}_retry_{i+1}'
      new_record = records.TestResultRecord(retry_name, self.TAG)
      new_record.retry_parent = previous_record
      new_record.parent = (previous_record, records.TestParentType.RETRY)
      previous_record = self.exec_one_test(retry_name, test_method, previous_record)
      if not should_retry(previous_record):
        break
```
===== 17 =====
```
       new_record = records.TestResultRecord(retry_name, self.TAG)
       new_record.retry_parent = previous_record
       new_record.parent = (previous_record, records.TestParentType.RETRY)
-      previous_record = self.exec_one_test(retry_name, test_method, new_record)
+      previous_record = self.exec_one_test(test_method, retry_name, new_record)
       if not should_retry(previous_record):
         break
```
```
  def _exec_one_test_with_retry(self, test_name, test_method, max_count):
    """Executes one test and retry the test if needed.

    Repeatedly execute a test case until it passes or the maximum count of
    iteration has been reached.

    Args:
      test_name: string, Name of the test.
      test_method: function, The test method to execute.
      max_count: int, the maximum number of iterations to execute the test for.
    """

    def should_retry(record):
      return record.result in [
          records.TestResultEnums.TEST_RESULT_FAIL,
          records.TestResultEnums.TEST_RESULT_ERROR,
      ]

    previous_record = self.exec_one_test(test_name, test_method)

    if not should_retry(previous_record):
      return

    for i in range(max_count - 1):
      retry_name = f'{test_name}_retry_{i+1}'
      new_record = records.TestResultRecord(retry_name, self.TAG)
      new_record.retry_parent = previous_record
      new_record.parent = (previous_record, records.TestParentType.RETRY)
      previous_record = self.exec_one_test(test_method, retry_name, new_record)
      if not should_retry(previous_record):
        break
```
