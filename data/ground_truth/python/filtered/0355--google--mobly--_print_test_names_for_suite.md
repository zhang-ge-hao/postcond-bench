https://github.com/google/mobly/blob/6aa58093145669c99c1d6680ab2c1ace42f7f229/./mobly/suite_runner.py#L273-L297
```
🈚️

wrong process
local crash bug included (bug 0)
Wrong Originally

@icontract.ensure(lambda result: True)
```
```
@icontract.snapshot(lambda _ARGS, _KWARGS: __import__('builtins').print, name="PRINT")
@icontract.ensure(lambda OLD: [c.args[0] for c in OLD.PRINT.mock_calls] == [
    '==========> FakeTest1_A <==========',
    'FakeTest1_A.test_a',
    '==========> FakeTest1_B <==========',
    'FakeTest1_B.test_a',
    '==========> FakeTest1_C <==========',
    'FakeTest1_C.test_a',
])
```
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 13]
===== 0 =====
```
   Args:
     suite_class: a test suite_class to be run.
   """
-  config = config_parser.TestRunConfig()
+  config = None  # This will lead to a NoneType error later when accessing config attributes.
   runner = test_runner.TestRunner(
       log_dir=config.log_path, testbed_name=config.testbed_name
   )
```
```
def _print_test_names_for_suite(suite_class):
  """Prints the names of all the tests in a suite classes.

  Args:
    suite_class: a test suite_class to be run.
  """
  config = None  # This will lead to a NoneType error later when accessing config attributes.
  runner = test_runner.TestRunner(
      log_dir=config.log_path, testbed_name=config.testbed_name
  )
  cls = suite_class(runner, config)
  try:
    cls.setup_suite(config)
  finally:
    cls.teardown_suite()

  last = ''
  for name in runner.get_full_test_names():
    tag = name.split('.')[0]
    # Print tags when we encounter a new one. Prefer this to grouping by
    # tag first since we should print any duplicate entries.
    if tag != last:
      last = tag
      print('==========> %s <==========' % tag)
    print(name)
```
===== 1 =====
```
   Args:
     suite_class: a test suite_class to be run.
   """
-  config = config_parser.TestRunConfig()
+  config = config_parser.load_test_config_file('invalid_path', None)  # This will cause the config to be invalid without raising an error.
   runner = test_runner.TestRunner(
       log_dir=config.log_path, testbed_name=config.testbed_name
   )
```
```
def _print_test_names_for_suite(suite_class):
  """Prints the names of all the tests in a suite classes.

  Args:
    suite_class: a test suite_class to be run.
  """
  config = config_parser.load_test_config_file('invalid_path', None)  # This will cause the config to be invalid without raising an error.
  runner = test_runner.TestRunner(
      log_dir=config.log_path, testbed_name=config.testbed_name
  )
  cls = suite_class(runner, config)
  try:
    cls.setup_suite(config)
  finally:
    cls.teardown_suite()

  last = ''
  for name in runner.get_full_test_names():
    tag = name.split('.')[0]
    # Print tags when we encounter a new one. Prefer this to grouping by
    # tag first since we should print any duplicate entries.
    if tag != last:
      last = tag
      print('==========> %s <==========' % tag)
    print(name)
```
===== 2 =====
```
   """
   config = config_parser.TestRunConfig()
   runner = test_runner.TestRunner(
-      log_dir=config.log_path, testbed_name=config.testbed_name
+      log_dir=None, testbed_name=config.testbed_name
   )
   cls = suite_class(runner, config)
   try:
```
```
def _print_test_names_for_suite(suite_class):
  """Prints the names of all the tests in a suite classes.

  Args:
    suite_class: a test suite_class to be run.
  """
  config = config_parser.TestRunConfig()
  runner = test_runner.TestRunner(
      log_dir=None, testbed_name=config.testbed_name
  )
  cls = suite_class(runner, config)
  try:
    cls.setup_suite(config)
  finally:
    cls.teardown_suite()

  last = ''
  for name in runner.get_full_test_names():
    tag = name.split('.')[0]
    # Print tags when we encounter a new one. Prefer this to grouping by
    # tag first since we should print any duplicate entries.
    if tag != last:
      last = tag
      print('==========> %s <==========' % tag)
    print(name)
```
===== 3 =====
```
   """
   config = config_parser.TestRunConfig()
   runner = test_runner.TestRunner(
-      log_dir=config.log_path, testbed_name=config.testbed_name
+      log_dir=config.log_path + '/logs', testbed_name=config.testbed_name
   )
   cls = suite_class(runner, config)
   try:
```
```
def _print_test_names_for_suite(suite_class):
  """Prints the names of all the tests in a suite classes.

  Args:
    suite_class: a test suite_class to be run.
  """
  config = config_parser.TestRunConfig()
  runner = test_runner.TestRunner(
      log_dir=config.log_path + '/logs', testbed_name=config.testbed_name
  )
  cls = suite_class(runner, config)
  try:
    cls.setup_suite(config)
  finally:
    cls.teardown_suite()

  last = ''
  for name in runner.get_full_test_names():
    tag = name.split('.')[0]
    # Print tags when we encounter a new one. Prefer this to grouping by
    # tag first since we should print any duplicate entries.
    if tag != last:
      last = tag
      print('==========> %s <==========' % tag)
    print(name)
```
===== 4 =====
```
   """
   config = config_parser.TestRunConfig()
   runner = test_runner.TestRunner(
-      log_dir=config.log_path, testbed_name=config.testbed_name
+      log_dir=config.log_path, testbed_name='invalid_testbed'
   )
   cls = suite_class(runner, config)
   try:
```
```
def _print_test_names_for_suite(suite_class):
  """Prints the names of all the tests in a suite classes.

  Args:
    suite_class: a test suite_class to be run.
  """
  config = config_parser.TestRunConfig()
  runner = test_runner.TestRunner(
      log_dir=config.log_path, testbed_name='invalid_testbed'
  )
  cls = suite_class(runner, config)
  try:
    cls.setup_suite(config)
  finally:
    cls.teardown_suite()

  last = ''
  for name in runner.get_full_test_names():
    tag = name.split('.')[0]
    # Print tags when we encounter a new one. Prefer this to grouping by
    # tag first since we should print any duplicate entries.
    if tag != last:
      last = tag
      print('==========> %s <==========' % tag)
    print(name)
```
===== 5 =====
```
   """
   config = config_parser.TestRunConfig()
   runner = test_runner.TestRunner(
-      log_dir=config.log_path, testbed_name=config.testbed_name
+      log_dir=config.log_path, testbed_name=config.testbed_name + 'extra'
   )
   cls = suite_class(runner, config)
   try:
```
```
def _print_test_names_for_suite(suite_class):
  """Prints the names of all the tests in a suite classes.

  Args:
    suite_class: a test suite_class to be run.
  """
  config = config_parser.TestRunConfig()
  runner = test_runner.TestRunner(
      log_dir=config.log_path, testbed_name=config.testbed_name + 'extra'
  )
  cls = suite_class(runner, config)
  try:
    cls.setup_suite(config)
  finally:
    cls.teardown_suite()

  last = ''
  for name in runner.get_full_test_names():
    tag = name.split('.')[0]
    # Print tags when we encounter a new one. Prefer this to grouping by
    # tag first since we should print any duplicate entries.
    if tag != last:
      last = tag
      print('==========> %s <==========' % tag)
    print(name)
```
===== 6 =====
```
   runner = test_runner.TestRunner(
       log_dir=config.log_path, testbed_name=config.testbed_name
   )
-  cls = suite_class(runner, config)
+  cls = suite_class(config, runner)  # Swapping the order of arguments
   try:
     cls.setup_suite(config)
   finally:
```
```
def _print_test_names_for_suite(suite_class):
  """Prints the names of all the tests in a suite classes.

  Args:
    suite_class: a test suite_class to be run.
  """
  config = config_parser.TestRunConfig()
  runner = test_runner.TestRunner(
      log_dir=config.log_path, testbed_name=config.testbed_name
  )
  cls = suite_class(config, runner)  # Swapping the order of arguments
  try:
    cls.setup_suite(config)
  finally:
    cls.teardown_suite()

  last = ''
  for name in runner.get_full_test_names():
    tag = name.split('.')[0]
    # Print tags when we encounter a new one. Prefer this to grouping by
    # tag first since we should print any duplicate entries.
    if tag != last:
      last = tag
      print('==========> %s <==========' % tag)
    print(name)
```
===== 7 =====
```
   runner = test_runner.TestRunner(
       log_dir=config.log_path, testbed_name=config.testbed_name
   )
-  cls = suite_class(runner, config)
+  cls = suite_class(runner)  # Missing the config argument entirely
   try:
     cls.setup_suite(config)
   finally:
```
```
def _print_test_names_for_suite(suite_class):
  """Prints the names of all the tests in a suite classes.

  Args:
    suite_class: a test suite_class to be run.
  """
  config = config_parser.TestRunConfig()
  runner = test_runner.TestRunner(
      log_dir=config.log_path, testbed_name=config.testbed_name
  )
  cls = suite_class(runner)  # Missing the config argument entirely
  try:
    cls.setup_suite(config)
  finally:
    cls.teardown_suite()

  last = ''
  for name in runner.get_full_test_names():
    tag = name.split('.')[0]
    # Print tags when we encounter a new one. Prefer this to grouping by
    # tag first since we should print any duplicate entries.
    if tag != last:
      last = tag
      print('==========> %s <==========' % tag)
    print(name)
```
===== 8 =====
```
   runner = test_runner.TestRunner(
       log_dir=config.log_path, testbed_name=config.testbed_name
   )
-  cls = suite_class(runner, config)
+  cls = suite_class(runner, None)  # Passing None instead of the config object
   try:
     cls.setup_suite(config)
   finally:
```
```
def _print_test_names_for_suite(suite_class):
  """Prints the names of all the tests in a suite classes.

  Args:
    suite_class: a test suite_class to be run.
  """
  config = config_parser.TestRunConfig()
  runner = test_runner.TestRunner(
      log_dir=config.log_path, testbed_name=config.testbed_name
  )
  cls = suite_class(runner, None)  # Passing None instead of the config object
  try:
    cls.setup_suite(config)
  finally:
    cls.teardown_suite()

  last = ''
  for name in runner.get_full_test_names():
    tag = name.split('.')[0]
    # Print tags when we encounter a new one. Prefer this to grouping by
    # tag first since we should print any duplicate entries.
    if tag != last:
      last = tag
      print('==========> %s <==========' % tag)
    print(name)
```
===== 9 =====
```
   runner = test_runner.TestRunner(
       log_dir=config.log_path, testbed_name=config.testbed_name
   )
-  cls = suite_class(runner, config)
+  cls = suite_class(runner, config) if False else None  # Conditional that always evaluates to False, resulting in cls being None
   try:
     cls.setup_suite(config)
   finally:
```
```
def _print_test_names_for_suite(suite_class):
  """Prints the names of all the tests in a suite classes.

  Args:
    suite_class: a test suite_class to be run.
  """
  config = config_parser.TestRunConfig()
  runner = test_runner.TestRunner(
      log_dir=config.log_path, testbed_name=config.testbed_name
  )
  cls = suite_class(runner, config) if False else None  # Conditional that always evaluates to False, resulting in cls being None
  try:
    cls.setup_suite(config)
  finally:
    cls.teardown_suite()

  last = ''
  for name in runner.get_full_test_names():
    tag = name.split('.')[0]
    # Print tags when we encounter a new one. Prefer this to grouping by
    # tag first since we should print any duplicate entries.
    if tag != last:
      last = tag
      print('==========> %s <==========' % tag)
    print(name)
```
===== 11 =====
```
   try:
     cls.setup_suite(config)
   finally:
-    cls.teardown_suite()
+    cls._clean_up()  # Incorrectly calling a cleanup method instead of teardown
 
   last = ''
   for name in runner.get_full_test_names():
```
```
def _print_test_names_for_suite(suite_class):
  """Prints the names of all the tests in a suite classes.

  Args:
    suite_class: a test suite_class to be run.
  """
  config = config_parser.TestRunConfig()
  runner = test_runner.TestRunner(
      log_dir=config.log_path, testbed_name=config.testbed_name
  )
  cls = suite_class(runner, config)
  try:
    cls.setup_suite(config)
  finally:
    cls._clean_up()  # Incorrectly calling a cleanup method instead of teardown

  last = ''
  for name in runner.get_full_test_names():
    tag = name.split('.')[0]
    # Print tags when we encounter a new one. Prefer this to grouping by
    # tag first since we should print any duplicate entries.
    if tag != last:
      last = tag
      print('==========> %s <==========' % tag)
    print(name)
```
===== 13 =====
```
     cls.teardown_suite()
 
   last = ''
-  for name in runner.get_full_test_names():
+  for name in runner.get_test_names():  # Incorrect method, may not return full test names
     tag = name.split('.')[0]
     # Print tags when we encounter a new one. Prefer this to grouping by
     # tag first since we should print any duplicate entries.
```
```
def _print_test_names_for_suite(suite_class):
  """Prints the names of all the tests in a suite classes.

  Args:
    suite_class: a test suite_class to be run.
  """
  config = config_parser.TestRunConfig()
  runner = test_runner.TestRunner(
      log_dir=config.log_path, testbed_name=config.testbed_name
  )
  cls = suite_class(runner, config)
  try:
    cls.setup_suite(config)
  finally:
    cls.teardown_suite()

  last = ''
  for name in runner.get_test_names():  # Incorrect method, may not return full test names
    tag = name.split('.')[0]
    # Print tags when we encounter a new one. Prefer this to grouping by
    # tag first since we should print any duplicate entries.
    if tag != last:
      last = tag
      print('==========> %s <==========' % tag)
    print(name)
```
