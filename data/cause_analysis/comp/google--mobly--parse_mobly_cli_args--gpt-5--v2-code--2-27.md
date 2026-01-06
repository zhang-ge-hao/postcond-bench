https://github.com/google/mobly/blob/6aa58093145669c99c1d6680ab2c1ace42f7f229/./mobly/test_runner.py#L90-L153
```
@icontract.ensure(lambda result: result is not None)
@icontract.ensure(lambda result: hasattr(result, "config") and hasattr(result, "list_tests") and hasattr(result, "tests") and hasattr(result, "test_bed") and hasattr(result, "verbose"))
@icontract.ensure(lambda result: isinstance(result.list_tests, bool))
@icontract.ensure(lambda result: isinstance(result.verbose, bool))
@icontract.ensure(lambda result: (result.config is None) or isinstance(result.config, str))
@icontract.ensure(lambda result: result.list_tests != (result.config is not None))
@icontract.ensure(lambda result: (result.tests is None) or (len(result.tests) >= 1 and all(isinstance(t, str) for t in result.tests)))
@icontract.ensure(lambda result: (result.test_bed is None) or (len(result.test_bed) >= 1 and all(isinstance(tb, str) for tb in result.test_bed)))
```
```
missing defensive checks

E   AttributeError: 'Namespace' object has no attribute 'verbose'
```
passed
```
@icontract.snapshot(lambda argv: argv, name="OLD_argv")
@icontract.ensure(
    lambda result, OLD, argv:
        isinstance(result, argparse.Namespace)
        and hasattr(result, "config")
        and (result.config is None or isinstance(result.config, str))
        and hasattr(result, "list_tests")
        and isinstance(result.list_tests, bool)
        and hasattr(result, "tests")
        and (
            result.tests is None
            or (
                isinstance(result.tests, list)
                and all(isinstance(x, str) for x in result.tests)
            )
        )
        and hasattr(result, "test_bed")
        and (
            result.test_bed is None
            or (
                isinstance(result.test_bed, list)
                and all(isinstance(x, str) for x in result.test_bed)
            )
        )
        and hasattr(result, "verbose")
        and isinstance(result.verbose, bool)
        and ((result.config is not None) ^ bool(result.list_tests))
        and ((OLD.OLD_argv is None) or argv == OLD.OLD_argv)
)

```
===== 27: local_crash =====
```
 
   parser.add_argument(
       '-v',
-      '--verbose',
+      '--verbosity',  # Incorrect argument name
       action='store_true',
       help='Set console logger level to DEBUG',
   )
```
```
def parse_mobly_cli_args(argv):
  """Parses cli args that are consumed by Mobly.

  This is the arg parsing logic for the default test_runner.main entry point.

  Multiple arg parsers can be applied to the same set of cli input. So you
  can use this logic in addition to any other args you want to parse. This
  function ignores the args that don't apply to default `test_runner.main`.

  Args:
    argv: A list that is then parsed as cli args. If None, defaults to cli
      input.

  Returns:
    Namespace containing the parsed args.
  """
  parser = argparse.ArgumentParser(description='Mobly Test Executable.')
  group = parser.add_mutually_exclusive_group(required=True)
  group.add_argument(
      '-c',
      '--config',
      type=str,
      metavar='<PATH>',
      help='Path to the test configuration file.',
  )
  group.add_argument(
      '-l',
      '--list_tests',
      action='store_true',
      help=(
          'Print the names of the tests defined in a script without '
          'executing them.'
      ),
  )
  parser.add_argument(
      '--tests',
      '--test_case',
      nargs='+',
      type=str,
      metavar='[test_a test_b re:test_(c|d)...]',
      help=(
          'A list of tests in the test class to execute. Each value can be a '
          'test name string or a `re:` prefixed string for full regex match of'
          ' test names.'
      ),
  )
  parser.add_argument(
      '-tb',
      '--test_bed',
      nargs='+',
      type=str,
      metavar='[<TEST BED NAME1> <TEST BED NAME2> ...]',
      help='Specify which test beds to run tests on.',
  )

  parser.add_argument(
      '-v',
      '--verbosity',  # Incorrect argument name
      action='store_true',
      help='Set console logger level to DEBUG',
  )
  if not argv:
    argv = sys.argv[1:]
  return parser.parse_known_args(argv)[0]
```
