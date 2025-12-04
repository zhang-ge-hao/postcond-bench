https://github.com/google/mobly/blob/6aa58093145669c99c1d6680ab2c1ace42f7f229/./mobly/suite_runner.py#L496-L556
```
@icontract.ensure(
    lambda result, selected_tests:
        (selected_tests is None and result is None)
        or (
            selected_tests is not None
            and (
                (parsed := [
                    (cls, suffix, test_name)
                    for test in selected_tests
                    for cls_name_split in [test.split(".", 1)]
                    for test_class_name, test_name in [
                        (
                            cls_name_split[0],
                            cls_name_split[1] if len(cls_name_split) == 2 else None,
                        )
                    ]
                    for cls_suffix_split in [test_class_name.split("_", 1)]
                    for cls, suffix in [
                        (
                            cls_suffix_split[0],
                            cls_suffix_split[1] if len(cls_suffix_split) == 2 else None,
                        )
                    ]
                ]) is not None
                and (
                    keys_in_order := list(
                        collections.OrderedDict.fromkeys(
                            [(cls, suffix) for cls, suffix, _ in parsed]
                        ).keys()
                    )
                ) is not None
                and result
                == collections.OrderedDict(
                    (
                        key,
                        None
                        if any(
                            name is None and (cls, suffix) == key
                            for cls, suffix, name in parsed
                        )
                        else [
                            name
                            for cls, suffix, name in parsed
                            if (cls, suffix) == key
                        ],
                    )
                    for key in keys_in_order
                )
            )
        )
)
```
```
None
```
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24]
===== 0 =====
```
   """
   if selected_tests is None:
     return None
-  test_class_to_tests = collections.OrderedDict()
+  test_class_to_tests = collections.OrderedDict([(None, None)])  # Initializing with a default entry that could interfere with logic later.
   for test in selected_tests:
     test_class_name = test
     test_name = None
```
```
def _parse_raw_test_selector(selected_tests):
  """Parses test selector from CLI arguments.

  This function transforms a list of selector strings (such as FooTest or
  FooTest.test_method_a) to a dict where keys are a tuple containing
  (test_class_name, test_suffix) and values are lists of selected tests in
  those classes. None means all tests in that class are selected.

  Args:
    selected_tests: list of strings, list of tests to execute of the form:
      <test_class_name>[_<test_suffix>][.<test_name>].

    .. code-block:: python
      [
        'BarTest',
        'FooTest_A',
        'FooTest_B'
        'FooTest_C.test_method_a'
        'FooTest_C.test_method_b'
        'BazTest.test_method_a',
        'BazTest.test_method_b'
      ]

  Returns:
    dict: Keys are a tuple of (test_class_name, test_suffix), and values are
    lists of test names within class.
      E.g. the example in
      `tests` would translate to:

      .. code-block:: python
        {
          (BarTest, None): None,
          (FooTest, 'A'): None,
          (FooTest, 'B'): None,
          (FooTest,)'C'): ['test_method_a', 'test_method_b'],
          (BazTest, None): ['test_method_a', 'test_method_b']
        }
  """
  if selected_tests is None:
    return None
  test_class_to_tests = collections.OrderedDict([(None, None)])  # Initializing with a default entry that could interfere with logic later.
  for test in selected_tests:
    test_class_name = test
    test_name = None
    test_suffix = None
    if '.' in test_class_name:
      (test_class_name, test_name) = test_class_name.split('.', maxsplit=1)
    if '_' in test_class_name:
      (test_class_name, test_suffix) = test_class_name.split('_', maxsplit=1)

    key = (test_class_name, test_suffix)
    if key not in test_class_to_tests:
      test_class_to_tests[key] = []

    # If the test name is None, it means all tests in the class are selected.
    if test_name is None:
      test_class_to_tests[key] = None
    # Only add the test if we're not already running all tests in the class.
    elif test_class_to_tests[key] is not None:
      test_class_to_tests[key].append(test_name)
  return test_class_to_tests
```
===== 1 =====
```
   """
   if selected_tests is None:
     return None
-  test_class_to_tests = collections.OrderedDict()
+  test_class_to_tests = collections.OrderedDict([(None, [])])  # Initializing with an empty list instead of None, which changes the expected behavior.
   for test in selected_tests:
     test_class_name = test
     test_name = None
```
```
def _parse_raw_test_selector(selected_tests):
  """Parses test selector from CLI arguments.

  This function transforms a list of selector strings (such as FooTest or
  FooTest.test_method_a) to a dict where keys are a tuple containing
  (test_class_name, test_suffix) and values are lists of selected tests in
  those classes. None means all tests in that class are selected.

  Args:
    selected_tests: list of strings, list of tests to execute of the form:
      <test_class_name>[_<test_suffix>][.<test_name>].

    .. code-block:: python
      [
        'BarTest',
        'FooTest_A',
        'FooTest_B'
        'FooTest_C.test_method_a'
        'FooTest_C.test_method_b'
        'BazTest.test_method_a',
        'BazTest.test_method_b'
      ]

  Returns:
    dict: Keys are a tuple of (test_class_name, test_suffix), and values are
    lists of test names within class.
      E.g. the example in
      `tests` would translate to:

      .. code-block:: python
        {
          (BarTest, None): None,
          (FooTest, 'A'): None,
          (FooTest, 'B'): None,
          (FooTest,)'C'): ['test_method_a', 'test_method_b'],
          (BazTest, None): ['test_method_a', 'test_method_b']
        }
  """
  if selected_tests is None:
    return None
  test_class_to_tests = collections.OrderedDict([(None, [])])  # Initializing with an empty list instead of None, which changes the expected behavior.
  for test in selected_tests:
    test_class_name = test
    test_name = None
    test_suffix = None
    if '.' in test_class_name:
      (test_class_name, test_name) = test_class_name.split('.', maxsplit=1)
    if '_' in test_class_name:
      (test_class_name, test_suffix) = test_class_name.split('_', maxsplit=1)

    key = (test_class_name, test_suffix)
    if key not in test_class_to_tests:
      test_class_to_tests[key] = []

    # If the test name is None, it means all tests in the class are selected.
    if test_name is None:
      test_class_to_tests[key] = None
    # Only add the test if we're not already running all tests in the class.
    elif test_class_to_tests[key] is not None:
      test_class_to_tests[key].append(test_name)
  return test_class_to_tests
```
===== 2 =====
```
   if selected_tests is None:
     return None
   test_class_to_tests = collections.OrderedDict()
-  for test in selected_tests:
+  for test in selected_tests:  # This will incorrectly modify the selected_tests list while iterating.
+    selected_tests.remove(test)
     test_class_name = test
     test_name = None
     test_suffix = None
```
```
def _parse_raw_test_selector(selected_tests):
  """Parses test selector from CLI arguments.

  This function transforms a list of selector strings (such as FooTest or
  FooTest.test_method_a) to a dict where keys are a tuple containing
  (test_class_name, test_suffix) and values are lists of selected tests in
  those classes. None means all tests in that class are selected.

  Args:
    selected_tests: list of strings, list of tests to execute of the form:
      <test_class_name>[_<test_suffix>][.<test_name>].

    .. code-block:: python
      [
        'BarTest',
        'FooTest_A',
        'FooTest_B'
        'FooTest_C.test_method_a'
        'FooTest_C.test_method_b'
        'BazTest.test_method_a',
        'BazTest.test_method_b'
      ]

  Returns:
    dict: Keys are a tuple of (test_class_name, test_suffix), and values are
    lists of test names within class.
      E.g. the example in
      `tests` would translate to:

      .. code-block:: python
        {
          (BarTest, None): None,
          (FooTest, 'A'): None,
          (FooTest, 'B'): None,
          (FooTest,)'C'): ['test_method_a', 'test_method_b'],
          (BazTest, None): ['test_method_a', 'test_method_b']
        }
  """
  if selected_tests is None:
    return None
  test_class_to_tests = collections.OrderedDict()
  for test in selected_tests:  # This will incorrectly modify the selected_tests list while iterating.
    selected_tests.remove(test)
    test_class_name = test
    test_name = None
    test_suffix = None
    if '.' in test_class_name:
      (test_class_name, test_name) = test_class_name.split('.', maxsplit=1)
    if '_' in test_class_name:
      (test_class_name, test_suffix) = test_class_name.split('_', maxsplit=1)

    key = (test_class_name, test_suffix)
    if key not in test_class_to_tests:
      test_class_to_tests[key] = []

    # If the test name is None, it means all tests in the class are selected.
    if test_name is None:
      test_class_to_tests[key] = None
    # Only add the test if we're not already running all tests in the class.
    elif test_class_to_tests[key] is not None:
      test_class_to_tests[key].append(test_name)
  return test_class_to_tests
```
===== 3 =====
```
   if selected_tests is None:
     return None
   test_class_to_tests = collections.OrderedDict()
-  for test in selected_tests:
+  for test in selected_tests:  # This will incorrectly process the tests in reverse order.
+    selected_tests.reverse()
     test_class_name = test
     test_name = None
     test_suffix = None
```
```
def _parse_raw_test_selector(selected_tests):
  """Parses test selector from CLI arguments.

  This function transforms a list of selector strings (such as FooTest or
  FooTest.test_method_a) to a dict where keys are a tuple containing
  (test_class_name, test_suffix) and values are lists of selected tests in
  those classes. None means all tests in that class are selected.

  Args:
    selected_tests: list of strings, list of tests to execute of the form:
      <test_class_name>[_<test_suffix>][.<test_name>].

    .. code-block:: python
      [
        'BarTest',
        'FooTest_A',
        'FooTest_B'
        'FooTest_C.test_method_a'
        'FooTest_C.test_method_b'
        'BazTest.test_method_a',
        'BazTest.test_method_b'
      ]

  Returns:
    dict: Keys are a tuple of (test_class_name, test_suffix), and values are
    lists of test names within class.
      E.g. the example in
      `tests` would translate to:

      .. code-block:: python
        {
          (BarTest, None): None,
          (FooTest, 'A'): None,
          (FooTest, 'B'): None,
          (FooTest,)'C'): ['test_method_a', 'test_method_b'],
          (BazTest, None): ['test_method_a', 'test_method_b']
        }
  """
  if selected_tests is None:
    return None
  test_class_to_tests = collections.OrderedDict()
  for test in selected_tests:  # This will incorrectly process the tests in reverse order.
    selected_tests.reverse()
    test_class_name = test
    test_name = None
    test_suffix = None
    if '.' in test_class_name:
      (test_class_name, test_name) = test_class_name.split('.', maxsplit=1)
    if '_' in test_class_name:
      (test_class_name, test_suffix) = test_class_name.split('_', maxsplit=1)

    key = (test_class_name, test_suffix)
    if key not in test_class_to_tests:
      test_class_to_tests[key] = []

    # If the test name is None, it means all tests in the class are selected.
    if test_name is None:
      test_class_to_tests[key] = None
    # Only add the test if we're not already running all tests in the class.
    elif test_class_to_tests[key] is not None:
      test_class_to_tests[key].append(test_name)
  return test_class_to_tests
```
===== 4 =====
```
   if selected_tests is None:
     return None
   test_class_to_tests = collections.OrderedDict()
-  for test in selected_tests:
+  for test in selected_tests[:-1]:  # This will skip the last test in the list.
     test_class_name = test
     test_name = None
     test_suffix = None
```
```
def _parse_raw_test_selector(selected_tests):
  """Parses test selector from CLI arguments.

  This function transforms a list of selector strings (such as FooTest or
  FooTest.test_method_a) to a dict where keys are a tuple containing
  (test_class_name, test_suffix) and values are lists of selected tests in
  those classes. None means all tests in that class are selected.

  Args:
    selected_tests: list of strings, list of tests to execute of the form:
      <test_class_name>[_<test_suffix>][.<test_name>].

    .. code-block:: python
      [
        'BarTest',
        'FooTest_A',
        'FooTest_B'
        'FooTest_C.test_method_a'
        'FooTest_C.test_method_b'
        'BazTest.test_method_a',
        'BazTest.test_method_b'
      ]

  Returns:
    dict: Keys are a tuple of (test_class_name, test_suffix), and values are
    lists of test names within class.
      E.g. the example in
      `tests` would translate to:

      .. code-block:: python
        {
          (BarTest, None): None,
          (FooTest, 'A'): None,
          (FooTest, 'B'): None,
          (FooTest,)'C'): ['test_method_a', 'test_method_b'],
          (BazTest, None): ['test_method_a', 'test_method_b']
        }
  """
  if selected_tests is None:
    return None
  test_class_to_tests = collections.OrderedDict()
  for test in selected_tests[:-1]:  # This will skip the last test in the list.
    test_class_name = test
    test_name = None
    test_suffix = None
    if '.' in test_class_name:
      (test_class_name, test_name) = test_class_name.split('.', maxsplit=1)
    if '_' in test_class_name:
      (test_class_name, test_suffix) = test_class_name.split('_', maxsplit=1)

    key = (test_class_name, test_suffix)
    if key not in test_class_to_tests:
      test_class_to_tests[key] = []

    # If the test name is None, it means all tests in the class are selected.
    if test_name is None:
      test_class_to_tests[key] = None
    # Only add the test if we're not already running all tests in the class.
    elif test_class_to_tests[key] is not None:
      test_class_to_tests[key].append(test_name)
  return test_class_to_tests
```
===== 5 =====
```
     return None
   test_class_to_tests = collections.OrderedDict()
   for test in selected_tests:
-    test_class_name = test
+    test_class_name = test.replace('Test', '')  # Removes 'Test' from the class name, potentially leading to an unknown class.
     test_name = None
     test_suffix = None
     if '.' in test_class_name:
```
```
def _parse_raw_test_selector(selected_tests):
  """Parses test selector from CLI arguments.

  This function transforms a list of selector strings (such as FooTest or
  FooTest.test_method_a) to a dict where keys are a tuple containing
  (test_class_name, test_suffix) and values are lists of selected tests in
  those classes. None means all tests in that class are selected.

  Args:
    selected_tests: list of strings, list of tests to execute of the form:
      <test_class_name>[_<test_suffix>][.<test_name>].

    .. code-block:: python
      [
        'BarTest',
        'FooTest_A',
        'FooTest_B'
        'FooTest_C.test_method_a'
        'FooTest_C.test_method_b'
        'BazTest.test_method_a',
        'BazTest.test_method_b'
      ]

  Returns:
    dict: Keys are a tuple of (test_class_name, test_suffix), and values are
    lists of test names within class.
      E.g. the example in
      `tests` would translate to:

      .. code-block:: python
        {
          (BarTest, None): None,
          (FooTest, 'A'): None,
          (FooTest, 'B'): None,
          (FooTest,)'C'): ['test_method_a', 'test_method_b'],
          (BazTest, None): ['test_method_a', 'test_method_b']
        }
  """
  if selected_tests is None:
    return None
  test_class_to_tests = collections.OrderedDict()
  for test in selected_tests:
    test_class_name = test.replace('Test', '')  # Removes 'Test' from the class name, potentially leading to an unknown class.
    test_name = None
    test_suffix = None
    if '.' in test_class_name:
      (test_class_name, test_name) = test_class_name.split('.', maxsplit=1)
    if '_' in test_class_name:
      (test_class_name, test_suffix) = test_class_name.split('_', maxsplit=1)

    key = (test_class_name, test_suffix)
    if key not in test_class_to_tests:
      test_class_to_tests[key] = []

    # If the test name is None, it means all tests in the class are selected.
    if test_name is None:
      test_class_to_tests[key] = None
    # Only add the test if we're not already running all tests in the class.
    elif test_class_to_tests[key] is not None:
      test_class_to_tests[key].append(test_name)
  return test_class_to_tests
```
===== 6 =====
```
     return None
   test_class_to_tests = collections.OrderedDict()
   for test in selected_tests:
-    test_class_name = test
+    test_class_name = test.split('_')[0]  # Incorrectly assigns only the part before the first underscore.
     test_name = None
     test_suffix = None
     if '.' in test_class_name:
```
```
def _parse_raw_test_selector(selected_tests):
  """Parses test selector from CLI arguments.

  This function transforms a list of selector strings (such as FooTest or
  FooTest.test_method_a) to a dict where keys are a tuple containing
  (test_class_name, test_suffix) and values are lists of selected tests in
  those classes. None means all tests in that class are selected.

  Args:
    selected_tests: list of strings, list of tests to execute of the form:
      <test_class_name>[_<test_suffix>][.<test_name>].

    .. code-block:: python
      [
        'BarTest',
        'FooTest_A',
        'FooTest_B'
        'FooTest_C.test_method_a'
        'FooTest_C.test_method_b'
        'BazTest.test_method_a',
        'BazTest.test_method_b'
      ]

  Returns:
    dict: Keys are a tuple of (test_class_name, test_suffix), and values are
    lists of test names within class.
      E.g. the example in
      `tests` would translate to:

      .. code-block:: python
        {
          (BarTest, None): None,
          (FooTest, 'A'): None,
          (FooTest, 'B'): None,
          (FooTest,)'C'): ['test_method_a', 'test_method_b'],
          (BazTest, None): ['test_method_a', 'test_method_b']
        }
  """
  if selected_tests is None:
    return None
  test_class_to_tests = collections.OrderedDict()
  for test in selected_tests:
    test_class_name = test.split('_')[0]  # Incorrectly assigns only the part before the first underscore.
    test_name = None
    test_suffix = None
    if '.' in test_class_name:
      (test_class_name, test_name) = test_class_name.split('.', maxsplit=1)
    if '_' in test_class_name:
      (test_class_name, test_suffix) = test_class_name.split('_', maxsplit=1)

    key = (test_class_name, test_suffix)
    if key not in test_class_to_tests:
      test_class_to_tests[key] = []

    # If the test name is None, it means all tests in the class are selected.
    if test_name is None:
      test_class_to_tests[key] = None
    # Only add the test if we're not already running all tests in the class.
    elif test_class_to_tests[key] is not None:
      test_class_to_tests[key].append(test_name)
  return test_class_to_tests
```
===== 7 =====
```
     return None
   test_class_to_tests = collections.OrderedDict()
   for test in selected_tests:
-    test_class_name = test
+    test_class_name = test.upper()  # Converts the class name to uppercase, which may not match the actual class name.
     test_name = None
     test_suffix = None
     if '.' in test_class_name:
```
```
def _parse_raw_test_selector(selected_tests):
  """Parses test selector from CLI arguments.

  This function transforms a list of selector strings (such as FooTest or
  FooTest.test_method_a) to a dict where keys are a tuple containing
  (test_class_name, test_suffix) and values are lists of selected tests in
  those classes. None means all tests in that class are selected.

  Args:
    selected_tests: list of strings, list of tests to execute of the form:
      <test_class_name>[_<test_suffix>][.<test_name>].

    .. code-block:: python
      [
        'BarTest',
        'FooTest_A',
        'FooTest_B'
        'FooTest_C.test_method_a'
        'FooTest_C.test_method_b'
        'BazTest.test_method_a',
        'BazTest.test_method_b'
      ]

  Returns:
    dict: Keys are a tuple of (test_class_name, test_suffix), and values are
    lists of test names within class.
      E.g. the example in
      `tests` would translate to:

      .. code-block:: python
        {
          (BarTest, None): None,
          (FooTest, 'A'): None,
          (FooTest, 'B'): None,
          (FooTest,)'C'): ['test_method_a', 'test_method_b'],
          (BazTest, None): ['test_method_a', 'test_method_b']
        }
  """
  if selected_tests is None:
    return None
  test_class_to_tests = collections.OrderedDict()
  for test in selected_tests:
    test_class_name = test.upper()  # Converts the class name to uppercase, which may not match the actual class name.
    test_name = None
    test_suffix = None
    if '.' in test_class_name:
      (test_class_name, test_name) = test_class_name.split('.', maxsplit=1)
    if '_' in test_class_name:
      (test_class_name, test_suffix) = test_class_name.split('_', maxsplit=1)

    key = (test_class_name, test_suffix)
    if key not in test_class_to_tests:
      test_class_to_tests[key] = []

    # If the test name is None, it means all tests in the class are selected.
    if test_name is None:
      test_class_to_tests[key] = None
    # Only add the test if we're not already running all tests in the class.
    elif test_class_to_tests[key] is not None:
      test_class_to_tests[key].append(test_name)
  return test_class_to_tests
```
===== 8 =====
```
     return None
   test_class_to_tests = collections.OrderedDict()
   for test in selected_tests:
-    test_class_name = test
+    test_class_name = test[::-1]  # Reverses the class name string, which will not match any actual class name.
     test_name = None
     test_suffix = None
     if '.' in test_class_name:
```
```
def _parse_raw_test_selector(selected_tests):
  """Parses test selector from CLI arguments.

  This function transforms a list of selector strings (such as FooTest or
  FooTest.test_method_a) to a dict where keys are a tuple containing
  (test_class_name, test_suffix) and values are lists of selected tests in
  those classes. None means all tests in that class are selected.

  Args:
    selected_tests: list of strings, list of tests to execute of the form:
      <test_class_name>[_<test_suffix>][.<test_name>].

    .. code-block:: python
      [
        'BarTest',
        'FooTest_A',
        'FooTest_B'
        'FooTest_C.test_method_a'
        'FooTest_C.test_method_b'
        'BazTest.test_method_a',
        'BazTest.test_method_b'
      ]

  Returns:
    dict: Keys are a tuple of (test_class_name, test_suffix), and values are
    lists of test names within class.
      E.g. the example in
      `tests` would translate to:

      .. code-block:: python
        {
          (BarTest, None): None,
          (FooTest, 'A'): None,
          (FooTest, 'B'): None,
          (FooTest,)'C'): ['test_method_a', 'test_method_b'],
          (BazTest, None): ['test_method_a', 'test_method_b']
        }
  """
  if selected_tests is None:
    return None
  test_class_to_tests = collections.OrderedDict()
  for test in selected_tests:
    test_class_name = test[::-1]  # Reverses the class name string, which will not match any actual class name.
    test_name = None
    test_suffix = None
    if '.' in test_class_name:
      (test_class_name, test_name) = test_class_name.split('.', maxsplit=1)
    if '_' in test_class_name:
      (test_class_name, test_suffix) = test_class_name.split('_', maxsplit=1)

    key = (test_class_name, test_suffix)
    if key not in test_class_to_tests:
      test_class_to_tests[key] = []

    # If the test name is None, it means all tests in the class are selected.
    if test_name is None:
      test_class_to_tests[key] = None
    # Only add the test if we're not already running all tests in the class.
    elif test_class_to_tests[key] is not None:
      test_class_to_tests[key].append(test_name)
  return test_class_to_tests
```
===== 9 =====
```
     test_class_name = test
     test_name = None
     test_suffix = None
-    if '.' in test_class_name:
+    if test_class_name.count('_') > 1:
       (test_class_name, test_name) = test_class_name.split('.', maxsplit=1)
     if '_' in test_class_name:
       (test_class_name, test_suffix) = test_class_name.split('_', maxsplit=1)
```
```
def _parse_raw_test_selector(selected_tests):
  """Parses test selector from CLI arguments.

  This function transforms a list of selector strings (such as FooTest or
  FooTest.test_method_a) to a dict where keys are a tuple containing
  (test_class_name, test_suffix) and values are lists of selected tests in
  those classes. None means all tests in that class are selected.

  Args:
    selected_tests: list of strings, list of tests to execute of the form:
      <test_class_name>[_<test_suffix>][.<test_name>].

    .. code-block:: python
      [
        'BarTest',
        'FooTest_A',
        'FooTest_B'
        'FooTest_C.test_method_a'
        'FooTest_C.test_method_b'
        'BazTest.test_method_a',
        'BazTest.test_method_b'
      ]

  Returns:
    dict: Keys are a tuple of (test_class_name, test_suffix), and values are
    lists of test names within class.
      E.g. the example in
      `tests` would translate to:

      .. code-block:: python
        {
          (BarTest, None): None,
          (FooTest, 'A'): None,
          (FooTest, 'B'): None,
          (FooTest,)'C'): ['test_method_a', 'test_method_b'],
          (BazTest, None): ['test_method_a', 'test_method_b']
        }
  """
  if selected_tests is None:
    return None
  test_class_to_tests = collections.OrderedDict()
  for test in selected_tests:
    test_class_name = test
    test_name = None
    test_suffix = None
    if test_class_name.count('_') > 1:
      (test_class_name, test_name) = test_class_name.split('.', maxsplit=1)
    if '_' in test_class_name:
      (test_class_name, test_suffix) = test_class_name.split('_', maxsplit=1)

    key = (test_class_name, test_suffix)
    if key not in test_class_to_tests:
      test_class_to_tests[key] = []

    # If the test name is None, it means all tests in the class are selected.
    if test_name is None:
      test_class_to_tests[key] = None
    # Only add the test if we're not already running all tests in the class.
    elif test_class_to_tests[key] is not None:
      test_class_to_tests[key].append(test_name)
  return test_class_to_tests
```
===== 10 =====
```
     test_class_name = test
     test_name = None
     test_suffix = None
-    if '.' in test_class_name:
+    if test_class_name.startswith('Test'):
       (test_class_name, test_name) = test_class_name.split('.', maxsplit=1)
     if '_' in test_class_name:
       (test_class_name, test_suffix) = test_class_name.split('_', maxsplit=1)
```
```
def _parse_raw_test_selector(selected_tests):
  """Parses test selector from CLI arguments.

  This function transforms a list of selector strings (such as FooTest or
  FooTest.test_method_a) to a dict where keys are a tuple containing
  (test_class_name, test_suffix) and values are lists of selected tests in
  those classes. None means all tests in that class are selected.

  Args:
    selected_tests: list of strings, list of tests to execute of the form:
      <test_class_name>[_<test_suffix>][.<test_name>].

    .. code-block:: python
      [
        'BarTest',
        'FooTest_A',
        'FooTest_B'
        'FooTest_C.test_method_a'
        'FooTest_C.test_method_b'
        'BazTest.test_method_a',
        'BazTest.test_method_b'
      ]

  Returns:
    dict: Keys are a tuple of (test_class_name, test_suffix), and values are
    lists of test names within class.
      E.g. the example in
      `tests` would translate to:

      .. code-block:: python
        {
          (BarTest, None): None,
          (FooTest, 'A'): None,
          (FooTest, 'B'): None,
          (FooTest,)'C'): ['test_method_a', 'test_method_b'],
          (BazTest, None): ['test_method_a', 'test_method_b']
        }
  """
  if selected_tests is None:
    return None
  test_class_to_tests = collections.OrderedDict()
  for test in selected_tests:
    test_class_name = test
    test_name = None
    test_suffix = None
    if test_class_name.startswith('Test'):
      (test_class_name, test_name) = test_class_name.split('.', maxsplit=1)
    if '_' in test_class_name:
      (test_class_name, test_suffix) = test_class_name.split('_', maxsplit=1)

    key = (test_class_name, test_suffix)
    if key not in test_class_to_tests:
      test_class_to_tests[key] = []

    # If the test name is None, it means all tests in the class are selected.
    if test_name is None:
      test_class_to_tests[key] = None
    # Only add the test if we're not already running all tests in the class.
    elif test_class_to_tests[key] is not None:
      test_class_to_tests[key].append(test_name)
  return test_class_to_tests
```
===== 11 =====
```
     test_name = None
     test_suffix = None
     if '.' in test_class_name:
-      (test_class_name, test_name) = test_class_name.split('.', maxsplit=1)
+      (test_class_name, test_name) = test_class_name.split('.', maxsplit=1)[0], None
     if '_' in test_class_name:
       (test_class_name, test_suffix) = test_class_name.split('_', maxsplit=1)
```
```
def _parse_raw_test_selector(selected_tests):
  """Parses test selector from CLI arguments.

  This function transforms a list of selector strings (such as FooTest or
  FooTest.test_method_a) to a dict where keys are a tuple containing
  (test_class_name, test_suffix) and values are lists of selected tests in
  those classes. None means all tests in that class are selected.

  Args:
    selected_tests: list of strings, list of tests to execute of the form:
      <test_class_name>[_<test_suffix>][.<test_name>].

    .. code-block:: python
      [
        'BarTest',
        'FooTest_A',
        'FooTest_B'
        'FooTest_C.test_method_a'
        'FooTest_C.test_method_b'
        'BazTest.test_method_a',
        'BazTest.test_method_b'
      ]

  Returns:
    dict: Keys are a tuple of (test_class_name, test_suffix), and values are
    lists of test names within class.
      E.g. the example in
      `tests` would translate to:

      .. code-block:: python
        {
          (BarTest, None): None,
          (FooTest, 'A'): None,
          (FooTest, 'B'): None,
          (FooTest,)'C'): ['test_method_a', 'test_method_b'],
          (BazTest, None): ['test_method_a', 'test_method_b']
        }
  """
  if selected_tests is None:
    return None
  test_class_to_tests = collections.OrderedDict()
  for test in selected_tests:
    test_class_name = test
    test_name = None
    test_suffix = None
    if '.' in test_class_name:
      (test_class_name, test_name) = test_class_name.split('.', maxsplit=1)[0], None
    if '_' in test_class_name:
      (test_class_name, test_suffix) = test_class_name.split('_', maxsplit=1)

    key = (test_class_name, test_suffix)
    if key not in test_class_to_tests:
      test_class_to_tests[key] = []

    # If the test name is None, it means all tests in the class are selected.
    if test_name is None:
      test_class_to_tests[key] = None
    # Only add the test if we're not already running all tests in the class.
    elif test_class_to_tests[key] is not None:
      test_class_to_tests[key].append(test_name)
  return test_class_to_tests
```
===== 12 =====
```
     test_name = None
     test_suffix = None
     if '.' in test_class_name:
-      (test_class_name, test_name) = test_class_name.split('.', maxsplit=1)
+      (test_class_name, test_name) = test_class_name.split('.', maxsplit=1)[1], None
     if '_' in test_class_name:
       (test_class_name, test_suffix) = test_class_name.split('_', maxsplit=1)
```
```
def _parse_raw_test_selector(selected_tests):
  """Parses test selector from CLI arguments.

  This function transforms a list of selector strings (such as FooTest or
  FooTest.test_method_a) to a dict where keys are a tuple containing
  (test_class_name, test_suffix) and values are lists of selected tests in
  those classes. None means all tests in that class are selected.

  Args:
    selected_tests: list of strings, list of tests to execute of the form:
      <test_class_name>[_<test_suffix>][.<test_name>].

    .. code-block:: python
      [
        'BarTest',
        'FooTest_A',
        'FooTest_B'
        'FooTest_C.test_method_a'
        'FooTest_C.test_method_b'
        'BazTest.test_method_a',
        'BazTest.test_method_b'
      ]

  Returns:
    dict: Keys are a tuple of (test_class_name, test_suffix), and values are
    lists of test names within class.
      E.g. the example in
      `tests` would translate to:

      .. code-block:: python
        {
          (BarTest, None): None,
          (FooTest, 'A'): None,
          (FooTest, 'B'): None,
          (FooTest,)'C'): ['test_method_a', 'test_method_b'],
          (BazTest, None): ['test_method_a', 'test_method_b']
        }
  """
  if selected_tests is None:
    return None
  test_class_to_tests = collections.OrderedDict()
  for test in selected_tests:
    test_class_name = test
    test_name = None
    test_suffix = None
    if '.' in test_class_name:
      (test_class_name, test_name) = test_class_name.split('.', maxsplit=1)[1], None
    if '_' in test_class_name:
      (test_class_name, test_suffix) = test_class_name.split('_', maxsplit=1)

    key = (test_class_name, test_suffix)
    if key not in test_class_to_tests:
      test_class_to_tests[key] = []

    # If the test name is None, it means all tests in the class are selected.
    if test_name is None:
      test_class_to_tests[key] = None
    # Only add the test if we're not already running all tests in the class.
    elif test_class_to_tests[key] is not None:
      test_class_to_tests[key].append(test_name)
  return test_class_to_tests
```
===== 13 =====
```
     test_suffix = None
     if '.' in test_class_name:
       (test_class_name, test_name) = test_class_name.split('.', maxsplit=1)
-    if '_' in test_class_name:
+    if test_class_name.startswith('Test'):
       (test_class_name, test_suffix) = test_class_name.split('_', maxsplit=1)
 
     key = (test_class_name, test_suffix)
```
```
def _parse_raw_test_selector(selected_tests):
  """Parses test selector from CLI arguments.

  This function transforms a list of selector strings (such as FooTest or
  FooTest.test_method_a) to a dict where keys are a tuple containing
  (test_class_name, test_suffix) and values are lists of selected tests in
  those classes. None means all tests in that class are selected.

  Args:
    selected_tests: list of strings, list of tests to execute of the form:
      <test_class_name>[_<test_suffix>][.<test_name>].

    .. code-block:: python
      [
        'BarTest',
        'FooTest_A',
        'FooTest_B'
        'FooTest_C.test_method_a'
        'FooTest_C.test_method_b'
        'BazTest.test_method_a',
        'BazTest.test_method_b'
      ]

  Returns:
    dict: Keys are a tuple of (test_class_name, test_suffix), and values are
    lists of test names within class.
      E.g. the example in
      `tests` would translate to:

      .. code-block:: python
        {
          (BarTest, None): None,
          (FooTest, 'A'): None,
          (FooTest, 'B'): None,
          (FooTest,)'C'): ['test_method_a', 'test_method_b'],
          (BazTest, None): ['test_method_a', 'test_method_b']
        }
  """
  if selected_tests is None:
    return None
  test_class_to_tests = collections.OrderedDict()
  for test in selected_tests:
    test_class_name = test
    test_name = None
    test_suffix = None
    if '.' in test_class_name:
      (test_class_name, test_name) = test_class_name.split('.', maxsplit=1)
    if test_class_name.startswith('Test'):
      (test_class_name, test_suffix) = test_class_name.split('_', maxsplit=1)

    key = (test_class_name, test_suffix)
    if key not in test_class_to_tests:
      test_class_to_tests[key] = []

    # If the test name is None, it means all tests in the class are selected.
    if test_name is None:
      test_class_to_tests[key] = None
    # Only add the test if we're not already running all tests in the class.
    elif test_class_to_tests[key] is not None:
      test_class_to_tests[key].append(test_name)
  return test_class_to_tests
```
===== 14 =====
```
     if '.' in test_class_name:
       (test_class_name, test_name) = test_class_name.split('.', maxsplit=1)
     if '_' in test_class_name:
-      (test_class_name, test_suffix) = test_class_name.split('_', maxsplit=1)
+      test_class_name, test_suffix = test_class_name.split('_', maxsplit=1)[0], None
 
     key = (test_class_name, test_suffix)
     if key not in test_class_to_tests:
```
```
def _parse_raw_test_selector(selected_tests):
  """Parses test selector from CLI arguments.

  This function transforms a list of selector strings (such as FooTest or
  FooTest.test_method_a) to a dict where keys are a tuple containing
  (test_class_name, test_suffix) and values are lists of selected tests in
  those classes. None means all tests in that class are selected.

  Args:
    selected_tests: list of strings, list of tests to execute of the form:
      <test_class_name>[_<test_suffix>][.<test_name>].

    .. code-block:: python
      [
        'BarTest',
        'FooTest_A',
        'FooTest_B'
        'FooTest_C.test_method_a'
        'FooTest_C.test_method_b'
        'BazTest.test_method_a',
        'BazTest.test_method_b'
      ]

  Returns:
    dict: Keys are a tuple of (test_class_name, test_suffix), and values are
    lists of test names within class.
      E.g. the example in
      `tests` would translate to:

      .. code-block:: python
        {
          (BarTest, None): None,
          (FooTest, 'A'): None,
          (FooTest, 'B'): None,
          (FooTest,)'C'): ['test_method_a', 'test_method_b'],
          (BazTest, None): ['test_method_a', 'test_method_b']
        }
  """
  if selected_tests is None:
    return None
  test_class_to_tests = collections.OrderedDict()
  for test in selected_tests:
    test_class_name = test
    test_name = None
    test_suffix = None
    if '.' in test_class_name:
      (test_class_name, test_name) = test_class_name.split('.', maxsplit=1)
    if '_' in test_class_name:
      test_class_name, test_suffix = test_class_name.split('_', maxsplit=1)[0], None

    key = (test_class_name, test_suffix)
    if key not in test_class_to_tests:
      test_class_to_tests[key] = []

    # If the test name is None, it means all tests in the class are selected.
    if test_name is None:
      test_class_to_tests[key] = None
    # Only add the test if we're not already running all tests in the class.
    elif test_class_to_tests[key] is not None:
      test_class_to_tests[key].append(test_name)
  return test_class_to_tests
```
===== 15 =====
```
     if '.' in test_class_name:
       (test_class_name, test_name) = test_class_name.split('.', maxsplit=1)
     if '_' in test_class_name:
-      (test_class_name, test_suffix) = test_class_name.split('_', maxsplit=1)
+      test_suffix = test_class_name.split('_', maxsplit=1)[0] if '_' in test_class_name else test_class_name
 
     key = (test_class_name, test_suffix)
     if key not in test_class_to_tests:
```
```
def _parse_raw_test_selector(selected_tests):
  """Parses test selector from CLI arguments.

  This function transforms a list of selector strings (such as FooTest or
  FooTest.test_method_a) to a dict where keys are a tuple containing
  (test_class_name, test_suffix) and values are lists of selected tests in
  those classes. None means all tests in that class are selected.

  Args:
    selected_tests: list of strings, list of tests to execute of the form:
      <test_class_name>[_<test_suffix>][.<test_name>].

    .. code-block:: python
      [
        'BarTest',
        'FooTest_A',
        'FooTest_B'
        'FooTest_C.test_method_a'
        'FooTest_C.test_method_b'
        'BazTest.test_method_a',
        'BazTest.test_method_b'
      ]

  Returns:
    dict: Keys are a tuple of (test_class_name, test_suffix), and values are
    lists of test names within class.
      E.g. the example in
      `tests` would translate to:

      .. code-block:: python
        {
          (BarTest, None): None,
          (FooTest, 'A'): None,
          (FooTest, 'B'): None,
          (FooTest,)'C'): ['test_method_a', 'test_method_b'],
          (BazTest, None): ['test_method_a', 'test_method_b']
        }
  """
  if selected_tests is None:
    return None
  test_class_to_tests = collections.OrderedDict()
  for test in selected_tests:
    test_class_name = test
    test_name = None
    test_suffix = None
    if '.' in test_class_name:
      (test_class_name, test_name) = test_class_name.split('.', maxsplit=1)
    if '_' in test_class_name:
      test_suffix = test_class_name.split('_', maxsplit=1)[0] if '_' in test_class_name else test_class_name

    key = (test_class_name, test_suffix)
    if key not in test_class_to_tests:
      test_class_to_tests[key] = []

    # If the test name is None, it means all tests in the class are selected.
    if test_name is None:
      test_class_to_tests[key] = None
    # Only add the test if we're not already running all tests in the class.
    elif test_class_to_tests[key] is not None:
      test_class_to_tests[key].append(test_name)
  return test_class_to_tests
```
===== 16 =====
```
     if '.' in test_class_name:
       (test_class_name, test_name) = test_class_name.split('.', maxsplit=1)
     if '_' in test_class_name:
-      (test_class_name, test_suffix) = test_class_name.split('_', maxsplit=1)
+      test_suffix = test_class_name.split('_', maxsplit=1)[1] if '_' in test_class_name else None
 
     key = (test_class_name, test_suffix)
     if key not in test_class_to_tests:
```
```
def _parse_raw_test_selector(selected_tests):
  """Parses test selector from CLI arguments.

  This function transforms a list of selector strings (such as FooTest or
  FooTest.test_method_a) to a dict where keys are a tuple containing
  (test_class_name, test_suffix) and values are lists of selected tests in
  those classes. None means all tests in that class are selected.

  Args:
    selected_tests: list of strings, list of tests to execute of the form:
      <test_class_name>[_<test_suffix>][.<test_name>].

    .. code-block:: python
      [
        'BarTest',
        'FooTest_A',
        'FooTest_B'
        'FooTest_C.test_method_a'
        'FooTest_C.test_method_b'
        'BazTest.test_method_a',
        'BazTest.test_method_b'
      ]

  Returns:
    dict: Keys are a tuple of (test_class_name, test_suffix), and values are
    lists of test names within class.
      E.g. the example in
      `tests` would translate to:

      .. code-block:: python
        {
          (BarTest, None): None,
          (FooTest, 'A'): None,
          (FooTest, 'B'): None,
          (FooTest,)'C'): ['test_method_a', 'test_method_b'],
          (BazTest, None): ['test_method_a', 'test_method_b']
        }
  """
  if selected_tests is None:
    return None
  test_class_to_tests = collections.OrderedDict()
  for test in selected_tests:
    test_class_name = test
    test_name = None
    test_suffix = None
    if '.' in test_class_name:
      (test_class_name, test_name) = test_class_name.split('.', maxsplit=1)
    if '_' in test_class_name:
      test_suffix = test_class_name.split('_', maxsplit=1)[1] if '_' in test_class_name else None

    key = (test_class_name, test_suffix)
    if key not in test_class_to_tests:
      test_class_to_tests[key] = []

    # If the test name is None, it means all tests in the class are selected.
    if test_name is None:
      test_class_to_tests[key] = None
    # Only add the test if we're not already running all tests in the class.
    elif test_class_to_tests[key] is not None:
      test_class_to_tests[key].append(test_name)
  return test_class_to_tests
```
===== 17 =====
```
       test_class_to_tests[key] = []
 
     # If the test name is None, it means all tests in the class are selected.
-    if test_name is None:
+    if test_name == '':
       test_class_to_tests[key] = None
     # Only add the test if we're not already running all tests in the class.
     elif test_class_to_tests[key] is not None:
```
```
def _parse_raw_test_selector(selected_tests):
  """Parses test selector from CLI arguments.

  This function transforms a list of selector strings (such as FooTest or
  FooTest.test_method_a) to a dict where keys are a tuple containing
  (test_class_name, test_suffix) and values are lists of selected tests in
  those classes. None means all tests in that class are selected.

  Args:
    selected_tests: list of strings, list of tests to execute of the form:
      <test_class_name>[_<test_suffix>][.<test_name>].

    .. code-block:: python
      [
        'BarTest',
        'FooTest_A',
        'FooTest_B'
        'FooTest_C.test_method_a'
        'FooTest_C.test_method_b'
        'BazTest.test_method_a',
        'BazTest.test_method_b'
      ]

  Returns:
    dict: Keys are a tuple of (test_class_name, test_suffix), and values are
    lists of test names within class.
      E.g. the example in
      `tests` would translate to:

      .. code-block:: python
        {
          (BarTest, None): None,
          (FooTest, 'A'): None,
          (FooTest, 'B'): None,
          (FooTest,)'C'): ['test_method_a', 'test_method_b'],
          (BazTest, None): ['test_method_a', 'test_method_b']
        }
  """
  if selected_tests is None:
    return None
  test_class_to_tests = collections.OrderedDict()
  for test in selected_tests:
    test_class_name = test
    test_name = None
    test_suffix = None
    if '.' in test_class_name:
      (test_class_name, test_name) = test_class_name.split('.', maxsplit=1)
    if '_' in test_class_name:
      (test_class_name, test_suffix) = test_class_name.split('_', maxsplit=1)

    key = (test_class_name, test_suffix)
    if key not in test_class_to_tests:
      test_class_to_tests[key] = []

    # If the test name is None, it means all tests in the class are selected.
    if test_name == '':
      test_class_to_tests[key] = None
    # Only add the test if we're not already running all tests in the class.
    elif test_class_to_tests[key] is not None:
      test_class_to_tests[key].append(test_name)
  return test_class_to_tests
```
===== 18 =====
```
       test_class_to_tests[key] = []
 
     # If the test name is None, it means all tests in the class are selected.
-    if test_name is None:
+    if test_name is None and test_suffix is None:
       test_class_to_tests[key] = None
     # Only add the test if we're not already running all tests in the class.
     elif test_class_to_tests[key] is not None:
```
```
def _parse_raw_test_selector(selected_tests):
  """Parses test selector from CLI arguments.

  This function transforms a list of selector strings (such as FooTest or
  FooTest.test_method_a) to a dict where keys are a tuple containing
  (test_class_name, test_suffix) and values are lists of selected tests in
  those classes. None means all tests in that class are selected.

  Args:
    selected_tests: list of strings, list of tests to execute of the form:
      <test_class_name>[_<test_suffix>][.<test_name>].

    .. code-block:: python
      [
        'BarTest',
        'FooTest_A',
        'FooTest_B'
        'FooTest_C.test_method_a'
        'FooTest_C.test_method_b'
        'BazTest.test_method_a',
        'BazTest.test_method_b'
      ]

  Returns:
    dict: Keys are a tuple of (test_class_name, test_suffix), and values are
    lists of test names within class.
      E.g. the example in
      `tests` would translate to:

      .. code-block:: python
        {
          (BarTest, None): None,
          (FooTest, 'A'): None,
          (FooTest, 'B'): None,
          (FooTest,)'C'): ['test_method_a', 'test_method_b'],
          (BazTest, None): ['test_method_a', 'test_method_b']
        }
  """
  if selected_tests is None:
    return None
  test_class_to_tests = collections.OrderedDict()
  for test in selected_tests:
    test_class_name = test
    test_name = None
    test_suffix = None
    if '.' in test_class_name:
      (test_class_name, test_name) = test_class_name.split('.', maxsplit=1)
    if '_' in test_class_name:
      (test_class_name, test_suffix) = test_class_name.split('_', maxsplit=1)

    key = (test_class_name, test_suffix)
    if key not in test_class_to_tests:
      test_class_to_tests[key] = []

    # If the test name is None, it means all tests in the class are selected.
    if test_name is None and test_suffix is None:
      test_class_to_tests[key] = None
    # Only add the test if we're not already running all tests in the class.
    elif test_class_to_tests[key] is not None:
      test_class_to_tests[key].append(test_name)
  return test_class_to_tests
```
===== 19 =====
```
       test_class_to_tests[key] = []
 
     # If the test name is None, it means all tests in the class are selected.
-    if test_name is None:
+    if test_name is not None:
       test_class_to_tests[key] = None
     # Only add the test if we're not already running all tests in the class.
     elif test_class_to_tests[key] is not None:
```
```
def _parse_raw_test_selector(selected_tests):
  """Parses test selector from CLI arguments.

  This function transforms a list of selector strings (such as FooTest or
  FooTest.test_method_a) to a dict where keys are a tuple containing
  (test_class_name, test_suffix) and values are lists of selected tests in
  those classes. None means all tests in that class are selected.

  Args:
    selected_tests: list of strings, list of tests to execute of the form:
      <test_class_name>[_<test_suffix>][.<test_name>].

    .. code-block:: python
      [
        'BarTest',
        'FooTest_A',
        'FooTest_B'
        'FooTest_C.test_method_a'
        'FooTest_C.test_method_b'
        'BazTest.test_method_a',
        'BazTest.test_method_b'
      ]

  Returns:
    dict: Keys are a tuple of (test_class_name, test_suffix), and values are
    lists of test names within class.
      E.g. the example in
      `tests` would translate to:

      .. code-block:: python
        {
          (BarTest, None): None,
          (FooTest, 'A'): None,
          (FooTest, 'B'): None,
          (FooTest,)'C'): ['test_method_a', 'test_method_b'],
          (BazTest, None): ['test_method_a', 'test_method_b']
        }
  """
  if selected_tests is None:
    return None
  test_class_to_tests = collections.OrderedDict()
  for test in selected_tests:
    test_class_name = test
    test_name = None
    test_suffix = None
    if '.' in test_class_name:
      (test_class_name, test_name) = test_class_name.split('.', maxsplit=1)
    if '_' in test_class_name:
      (test_class_name, test_suffix) = test_class_name.split('_', maxsplit=1)

    key = (test_class_name, test_suffix)
    if key not in test_class_to_tests:
      test_class_to_tests[key] = []

    # If the test name is None, it means all tests in the class are selected.
    if test_name is not None:
      test_class_to_tests[key] = None
    # Only add the test if we're not already running all tests in the class.
    elif test_class_to_tests[key] is not None:
      test_class_to_tests[key].append(test_name)
  return test_class_to_tests
```
===== 20 =====
```
       test_class_to_tests[key] = []
 
     # If the test name is None, it means all tests in the class are selected.
-    if test_name is None:
+    if test_name:
       test_class_to_tests[key] = None
     # Only add the test if we're not already running all tests in the class.
     elif test_class_to_tests[key] is not None:
```
```
def _parse_raw_test_selector(selected_tests):
  """Parses test selector from CLI arguments.

  This function transforms a list of selector strings (such as FooTest or
  FooTest.test_method_a) to a dict where keys are a tuple containing
  (test_class_name, test_suffix) and values are lists of selected tests in
  those classes. None means all tests in that class are selected.

  Args:
    selected_tests: list of strings, list of tests to execute of the form:
      <test_class_name>[_<test_suffix>][.<test_name>].

    .. code-block:: python
      [
        'BarTest',
        'FooTest_A',
        'FooTest_B'
        'FooTest_C.test_method_a'
        'FooTest_C.test_method_b'
        'BazTest.test_method_a',
        'BazTest.test_method_b'
      ]

  Returns:
    dict: Keys are a tuple of (test_class_name, test_suffix), and values are
    lists of test names within class.
      E.g. the example in
      `tests` would translate to:

      .. code-block:: python
        {
          (BarTest, None): None,
          (FooTest, 'A'): None,
          (FooTest, 'B'): None,
          (FooTest,)'C'): ['test_method_a', 'test_method_b'],
          (BazTest, None): ['test_method_a', 'test_method_b']
        }
  """
  if selected_tests is None:
    return None
  test_class_to_tests = collections.OrderedDict()
  for test in selected_tests:
    test_class_name = test
    test_name = None
    test_suffix = None
    if '.' in test_class_name:
      (test_class_name, test_name) = test_class_name.split('.', maxsplit=1)
    if '_' in test_class_name:
      (test_class_name, test_suffix) = test_class_name.split('_', maxsplit=1)

    key = (test_class_name, test_suffix)
    if key not in test_class_to_tests:
      test_class_to_tests[key] = []

    # If the test name is None, it means all tests in the class are selected.
    if test_name:
      test_class_to_tests[key] = None
    # Only add the test if we're not already running all tests in the class.
    elif test_class_to_tests[key] is not None:
      test_class_to_tests[key].append(test_name)
  return test_class_to_tests
```
===== 21 =====
```
       test_class_to_tests[key] = None
     # Only add the test if we're not already running all tests in the class.
     elif test_class_to_tests[key] is not None:
-      test_class_to_tests[key].append(test_name)
+      test_class_to_tests[key] = None  # This incorrectly sets the value to None, losing the previously collected test names.
   return test_class_to_tests
```
```
def _parse_raw_test_selector(selected_tests):
  """Parses test selector from CLI arguments.

  This function transforms a list of selector strings (such as FooTest or
  FooTest.test_method_a) to a dict where keys are a tuple containing
  (test_class_name, test_suffix) and values are lists of selected tests in
  those classes. None means all tests in that class are selected.

  Args:
    selected_tests: list of strings, list of tests to execute of the form:
      <test_class_name>[_<test_suffix>][.<test_name>].

    .. code-block:: python
      [
        'BarTest',
        'FooTest_A',
        'FooTest_B'
        'FooTest_C.test_method_a'
        'FooTest_C.test_method_b'
        'BazTest.test_method_a',
        'BazTest.test_method_b'
      ]

  Returns:
    dict: Keys are a tuple of (test_class_name, test_suffix), and values are
    lists of test names within class.
      E.g. the example in
      `tests` would translate to:

      .. code-block:: python
        {
          (BarTest, None): None,
          (FooTest, 'A'): None,
          (FooTest, 'B'): None,
          (FooTest,)'C'): ['test_method_a', 'test_method_b'],
          (BazTest, None): ['test_method_a', 'test_method_b']
        }
  """
  if selected_tests is None:
    return None
  test_class_to_tests = collections.OrderedDict()
  for test in selected_tests:
    test_class_name = test
    test_name = None
    test_suffix = None
    if '.' in test_class_name:
      (test_class_name, test_name) = test_class_name.split('.', maxsplit=1)
    if '_' in test_class_name:
      (test_class_name, test_suffix) = test_class_name.split('_', maxsplit=1)

    key = (test_class_name, test_suffix)
    if key not in test_class_to_tests:
      test_class_to_tests[key] = []

    # If the test name is None, it means all tests in the class are selected.
    if test_name is None:
      test_class_to_tests[key] = None
    # Only add the test if we're not already running all tests in the class.
    elif test_class_to_tests[key] is not None:
      test_class_to_tests[key] = None  # This incorrectly sets the value to None, losing the previously collected test names.
  return test_class_to_tests
```
===== 22 =====
```
       test_class_to_tests[key] = None
     # Only add the test if we're not already running all tests in the class.
     elif test_class_to_tests[key] is not None:
-      test_class_to_tests[key].append(test_name)
+      test_class_to_tests[key] = [test_name]  # This replaces the list with a new list containing only the current test_name.
   return test_class_to_tests
```
```
def _parse_raw_test_selector(selected_tests):
  """Parses test selector from CLI arguments.

  This function transforms a list of selector strings (such as FooTest or
  FooTest.test_method_a) to a dict where keys are a tuple containing
  (test_class_name, test_suffix) and values are lists of selected tests in
  those classes. None means all tests in that class are selected.

  Args:
    selected_tests: list of strings, list of tests to execute of the form:
      <test_class_name>[_<test_suffix>][.<test_name>].

    .. code-block:: python
      [
        'BarTest',
        'FooTest_A',
        'FooTest_B'
        'FooTest_C.test_method_a'
        'FooTest_C.test_method_b'
        'BazTest.test_method_a',
        'BazTest.test_method_b'
      ]

  Returns:
    dict: Keys are a tuple of (test_class_name, test_suffix), and values are
    lists of test names within class.
      E.g. the example in
      `tests` would translate to:

      .. code-block:: python
        {
          (BarTest, None): None,
          (FooTest, 'A'): None,
          (FooTest, 'B'): None,
          (FooTest,)'C'): ['test_method_a', 'test_method_b'],
          (BazTest, None): ['test_method_a', 'test_method_b']
        }
  """
  if selected_tests is None:
    return None
  test_class_to_tests = collections.OrderedDict()
  for test in selected_tests:
    test_class_name = test
    test_name = None
    test_suffix = None
    if '.' in test_class_name:
      (test_class_name, test_name) = test_class_name.split('.', maxsplit=1)
    if '_' in test_class_name:
      (test_class_name, test_suffix) = test_class_name.split('_', maxsplit=1)

    key = (test_class_name, test_suffix)
    if key not in test_class_to_tests:
      test_class_to_tests[key] = []

    # If the test name is None, it means all tests in the class are selected.
    if test_name is None:
      test_class_to_tests[key] = None
    # Only add the test if we're not already running all tests in the class.
    elif test_class_to_tests[key] is not None:
      test_class_to_tests[key] = [test_name]  # This replaces the list with a new list containing only the current test_name.
  return test_class_to_tests
```
===== 23 =====
```
       test_class_to_tests[key] = None
     # Only add the test if we're not already running all tests in the class.
     elif test_class_to_tests[key] is not None:
-      test_class_to_tests[key].append(test_name)
+      test_class_to_tests[key].append(test_name.upper())  # This appends the test_name in uppercase, which may not match the original test names.
   return test_class_to_tests
```
```
def _parse_raw_test_selector(selected_tests):
  """Parses test selector from CLI arguments.

  This function transforms a list of selector strings (such as FooTest or
  FooTest.test_method_a) to a dict where keys are a tuple containing
  (test_class_name, test_suffix) and values are lists of selected tests in
  those classes. None means all tests in that class are selected.

  Args:
    selected_tests: list of strings, list of tests to execute of the form:
      <test_class_name>[_<test_suffix>][.<test_name>].

    .. code-block:: python
      [
        'BarTest',
        'FooTest_A',
        'FooTest_B'
        'FooTest_C.test_method_a'
        'FooTest_C.test_method_b'
        'BazTest.test_method_a',
        'BazTest.test_method_b'
      ]

  Returns:
    dict: Keys are a tuple of (test_class_name, test_suffix), and values are
    lists of test names within class.
      E.g. the example in
      `tests` would translate to:

      .. code-block:: python
        {
          (BarTest, None): None,
          (FooTest, 'A'): None,
          (FooTest, 'B'): None,
          (FooTest,)'C'): ['test_method_a', 'test_method_b'],
          (BazTest, None): ['test_method_a', 'test_method_b']
        }
  """
  if selected_tests is None:
    return None
  test_class_to_tests = collections.OrderedDict()
  for test in selected_tests:
    test_class_name = test
    test_name = None
    test_suffix = None
    if '.' in test_class_name:
      (test_class_name, test_name) = test_class_name.split('.', maxsplit=1)
    if '_' in test_class_name:
      (test_class_name, test_suffix) = test_class_name.split('_', maxsplit=1)

    key = (test_class_name, test_suffix)
    if key not in test_class_to_tests:
      test_class_to_tests[key] = []

    # If the test name is None, it means all tests in the class are selected.
    if test_name is None:
      test_class_to_tests[key] = None
    # Only add the test if we're not already running all tests in the class.
    elif test_class_to_tests[key] is not None:
      test_class_to_tests[key].append(test_name.upper())  # This appends the test_name in uppercase, which may not match the original test names.
  return test_class_to_tests
```
===== 24 =====
```
       test_class_to_tests[key] = None
     # Only add the test if we're not already running all tests in the class.
     elif test_class_to_tests[key] is not None:
-      test_class_to_tests[key].append(test_name)
+      test_class_to_tests[key].insert(0, test_name)  # This adds the test_name to the beginning of the list instead of appending it.
   return test_class_to_tests
```
```
def _parse_raw_test_selector(selected_tests):
  """Parses test selector from CLI arguments.

  This function transforms a list of selector strings (such as FooTest or
  FooTest.test_method_a) to a dict where keys are a tuple containing
  (test_class_name, test_suffix) and values are lists of selected tests in
  those classes. None means all tests in that class are selected.

  Args:
    selected_tests: list of strings, list of tests to execute of the form:
      <test_class_name>[_<test_suffix>][.<test_name>].

    .. code-block:: python
      [
        'BarTest',
        'FooTest_A',
        'FooTest_B'
        'FooTest_C.test_method_a'
        'FooTest_C.test_method_b'
        'BazTest.test_method_a',
        'BazTest.test_method_b'
      ]

  Returns:
    dict: Keys are a tuple of (test_class_name, test_suffix), and values are
    lists of test names within class.
      E.g. the example in
      `tests` would translate to:

      .. code-block:: python
        {
          (BarTest, None): None,
          (FooTest, 'A'): None,
          (FooTest, 'B'): None,
          (FooTest,)'C'): ['test_method_a', 'test_method_b'],
          (BazTest, None): ['test_method_a', 'test_method_b']
        }
  """
  if selected_tests is None:
    return None
  test_class_to_tests = collections.OrderedDict()
  for test in selected_tests:
    test_class_name = test
    test_name = None
    test_suffix = None
    if '.' in test_class_name:
      (test_class_name, test_name) = test_class_name.split('.', maxsplit=1)
    if '_' in test_class_name:
      (test_class_name, test_suffix) = test_class_name.split('_', maxsplit=1)

    key = (test_class_name, test_suffix)
    if key not in test_class_to_tests:
      test_class_to_tests[key] = []

    # If the test name is None, it means all tests in the class are selected.
    if test_name is None:
      test_class_to_tests[key] = None
    # Only add the test if we're not already running all tests in the class.
    elif test_class_to_tests[key] is not None:
      test_class_to_tests[key].insert(0, test_name)  # This adds the test_name to the beginning of the list instead of appending it.
  return test_class_to_tests
```
