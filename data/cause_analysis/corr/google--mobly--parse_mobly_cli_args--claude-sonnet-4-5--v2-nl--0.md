https://github.com/google/mobly/blob/6aa58093145669c99c1d6680ab2c1ace42f7f229/./mobly/test_runner.py#L90-L153
```
@icontract.ensure(lambda __result__: __result__ is not None, "Result must not be None")
@icontract.ensure(lambda __result__: isinstance(__result__, argparse.Namespace), "Result must be an argparse.Namespace object")
@icontract.ensure(lambda __result__: hasattr(__result__, '__dict__'), "Result must have attributes")
```
```
limited spec

__result__
```
failed
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
