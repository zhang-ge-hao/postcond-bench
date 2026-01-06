https://github.com/pypyr/pypyr/blob/b3e8f8c6063c11e37c1c762b89b4cd8620460c79/./pypyr/dsl.py#L274-L331
```
@icontract.ensure(lambda self: hasattr(self, 'name'))
@icontract.ensure(lambda self: isinstance(self.name, str) or self.name is None)
@icontract.ensure(lambda self: hasattr(self, 'module'))
@icontract.ensure(lambda self: hasattr(self, 'foreach_items'))
@icontract.ensure(lambda self: self.foreach_items is None or isinstance(self.foreach_items, (list, CommentedSeq)))
@icontract.ensure(lambda self: hasattr(self, 'in_parameters'))
@icontract.ensure(lambda self: self.in_parameters is None or isinstance(self.in_parameters, (dict, CommentedMap)))
@icontract.ensure(lambda self: hasattr(self, 'run_me'))
@icontract.ensure(lambda self: isinstance(self.run_me, bool))
@icontract.ensure(lambda self: hasattr(self, 'skip_me'))
@icontract.ensure(lambda self: isinstance(self.skip_me, bool))
@icontract.ensure(lambda self: hasattr(self, 'swallow_me'))
@icontract.ensure(lambda self: isinstance(self.swallow_me, bool))
@icontract.ensure(lambda self: hasattr(self, 'while_decorator'))
```
```
hallucination on semantics

```
icontract_fail
```
@icontract.snapshot(lambda self, step: isinstance(step, dict), name="is_dict")
@icontract.snapshot(lambda self, step: step if isinstance(step, dict) else None, name="step_dict")
@icontract.snapshot(lambda self, step: step, name="step_arg")
@icontract.ensure(lambda OLD, self, step: self.run_step_function == step_cache.get_step(self.name))
@icontract.ensure(lambda OLD, self, step: (not OLD.is_dict) or (self.name == OLD.step_dict.get("name")))
@icontract.ensure(lambda OLD, self, step: (OLD.is_dict) or (self.name == OLD.step_arg))
@icontract.ensure(lambda OLD, self, step: isinstance(self.run_me, (bool, SpecialTagDirective)) and isinstance(self.skip_me, (bool, SpecialTagDirective)) and isinstance(self.swallow_me, (bool, SpecialTagDirective)))
@icontract.ensure(lambda OLD, self, step: (not OLD.is_dict) or (self.run_me == OLD.step_dict.get("run", True)))
@icontract.ensure(lambda OLD, self, step: (not OLD.is_dict) or (self.skip_me == OLD.step_dict.get("skip", False)))
@icontract.ensure(lambda OLD, self, step: (not OLD.is_dict) or (self.swallow_me == OLD.step_dict.get("swallow", False)))
@icontract.ensure(lambda OLD, self, step: (not OLD.is_dict) or (self.in_parameters == OLD.step_dict.get("in", None)))
@icontract.ensure(lambda OLD, self, step: (not OLD.is_dict) or (self.description == OLD.step_dict.get("description", None)))
@icontract.ensure(lambda OLD, self, step: (not OLD.is_dict) or (self.foreach_items == OLD.step_dict.get("foreach", None)))
@icontract.ensure(lambda OLD, self, step: (not OLD.is_dict) or (OLD.step_dict.get("foreach", None) is None or hasattr(self, "for_counter")))
@icontract.ensure(lambda OLD, self, step: (not OLD.is_dict) or ((OLD.step_dict.get("retry", None) is None and self.retry_decorator is None) or (OLD.step_dict.get("retry", None) is not None and self.retry_decorator is not None)))
@icontract.ensure(lambda OLD, self, step: (not OLD.is_dict) or (self.on_error == OLD.step_dict.get("onError", None)))
@icontract.ensure(lambda OLD, self, step: (not OLD.is_dict) or ((OLD.step_dict.get("while", None) is None and self.while_decorator is None) or (OLD.step_dict.get("while", None) is not None and self.while_decorator is not None)))
@icontract.ensure(lambda OLD, self, step: (not OLD.is_dict) or ((hasattr(OLD.step_dict, "lc") and isinstance(self.line_no, int) and isinstance(self.line_col, int)) or (not hasattr(OLD.step_dict, "lc") and self.line_no is None and self.line_col is None)))
@icontract.ensure(lambda OLD, self, step: (OLD.is_dict) or (self.run_me is True and self.skip_me is False and self.swallow_me is False))
```
