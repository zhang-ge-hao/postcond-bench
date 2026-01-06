https://github.com/pypyr/pypyr/blob/b3e8f8c6063c11e37c1c762b89b4cd8620460c79/./pypyr/steps/env.py#L134-L176
```
@icontract.snapshot(lambda: dict(os.environ), name="old_environ")
@icontract.snapshot(lambda context: list(context['env']['unset']), name="unset_list")
@icontract.ensure(lambda result: result is None)
@icontract.ensure(lambda OLD: all(var not in os.environ for var in OLD.unset_list))
@icontract.ensure(lambda OLD: set(os.environ.keys()) == set(OLD.old_environ.keys()) - set(OLD.unset_list))
@icontract.ensure(lambda OLD: all(os.environ[k] == OLD.old_environ[k] for k in set(OLD.old_environ.keys()) - set(OLD.unset_list)))
```
```
Hallucination.

@icontract.ensure(lambda result: result is None)
The comment does not mention the result.
The method actually has a result.
The LLM has hallucination that the method does not.
```
icontract_fail
```
@icontract.snapshot(lambda context: context.get_formatted_value(context['env'].get('unset', None)), name="unset_formatted")
@icontract.snapshot(lambda context: context['env'].get('unset', None), name="unset_raw")
@icontract.snapshot(lambda context: dict(os.environ), name="old_env")
@icontract.ensure(lambda OLD, result: result == bool(OLD.unset_formatted))
@icontract.ensure(lambda OLD: all(name not in os.environ for name in (OLD.unset_formatted or [])))
@icontract.ensure(lambda OLD: (set(OLD.old_env.keys()) - set(os.environ.keys())) == (set(OLD.unset_formatted or []) & set(OLD.old_env.keys())))
@icontract.ensure(lambda OLD: all(os.environ.get(k) == v for k, v in OLD.old_env.items() if k not in ((set(OLD.unset_formatted or []) & set(OLD.old_env.keys())))))
```
