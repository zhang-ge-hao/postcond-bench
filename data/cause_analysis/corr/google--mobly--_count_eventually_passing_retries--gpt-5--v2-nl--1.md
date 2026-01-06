https://github.com/google/mobly/blob/6aa58093145669c99c1d6680ab2c1ace42f7f229/./mobly/records.py#L651-L668
```
@icontract.snapshot(lambda self: list(self.requested), name="pre_requested")
@icontract.snapshot(lambda self: list(self.executed), name="pre_executed")
@icontract.snapshot(lambda self: list(self.passed), name="pre_passed")
@icontract.snapshot(lambda self: list(self.failed), name="pre_failed")
@icontract.snapshot(lambda self: list(self.skipped), name="pre_skipped")
@icontract.snapshot(lambda self: list(self.error), name="pre_error")
@icontract.snapshot(lambda self: list(self.controller_info), name="pre_controller_info")
@icontract.ensure(lambda result: isinstance(result, int))
@icontract.ensure(lambda self, result: result >= 0)
@icontract.ensure(lambda self, result: result <= len(self.executed))
@icontract.ensure(lambda self, result: result <= len(self.failed) + len(self.error) + len(self.skipped))
@icontract.ensure(lambda self, result: result <= sum(1 for r in self.executed if getattr(r, "result", None) != TestResultEnums.TEST_RESULT_PASS))
@icontract.ensure(lambda self, result: (len(self.passed) > 0) or result == 0)
@icontract.ensure(lambda self, result: (len(self.executed) == len(self.passed)) implies result == 0)
@icontract.ensure(lambda self, result: (all(((getattr(r, "parent", None) is None) or (isinstance(getattr(r, "parent", None), tuple) and len(getattr(r, "parent", None)) >= 2 and getattr(r, "parent", None)[1] != TestParentType.RETRY)) and (getattr(r, "retry_parent", None) is None) for r in self.executed)) implies result == 0)
@icontract.ensure(lambda self, OLD: self.requested == OLD.pre_requested)
@icontract.ensure(lambda self, OLD: self.executed == OLD.pre_executed)
@icontract.ensure(lambda self, OLD: self.passed == OLD.pre_passed)
@icontract.ensure(lambda self, OLD: self.failed == OLD.pre_failed)
@icontract.ensure(lambda self, OLD: self.skipped == OLD.pre_skipped)
@icontract.ensure(lambda self, OLD: self.error == OLD.pre_error)
@icontract.ensure(lambda self, OLD: self.controller_info == OLD.pre_controller_info)
```
```
syntax error

E   SyntaxError: invalid syntax. Perhaps you forgot a comma?
```
syntax_error
```
@icontract.snapshot(lambda self: list(self.passed), name='passed_snap')
@icontract.ensure(lambda OLD, result, self: result == sum((lambda f: (lambda r: f(f, r)))(lambda self_f, rr: 0 if rr.parent is None else ((1 + self_f(self_f, rr.parent[0])) if rr.parent[1] == TestParentType.RETRY else self_f(self_f, rr.parent[0])))(r) for r in OLD.passed_snap))
```
