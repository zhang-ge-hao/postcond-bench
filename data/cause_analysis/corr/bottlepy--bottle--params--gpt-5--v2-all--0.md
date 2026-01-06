https://github.com/bottlepy/bottle/blob/3d0ace47fe8e5ac5177b49597bd8ff872ff08d7b/./bottle.py#L1217-L1226
```
@icontract.snapshot(lambda self: set(self.query.keys()), name="pre_query_keys")
@icontract.snapshot(lambda self: set(self.forms.keys()), name="pre_forms_keys")
@icontract.snapshot(lambda self: {k: tuple(self.query.getall(k)) for k in self.query.keys()}, name="pre_query_values")
@icontract.snapshot(lambda self: {k: tuple(self.forms.getall(k)) for k in self.forms.keys()}, name="pre_forms_values")
@icontract.snapshot(lambda self: sum(1 for _ in self.query.allitems()), name="pre_query_items_count")
@icontract.snapshot(lambda self: sum(1 for _ in self.forms.allitems()), name="pre_forms_items_count")
@icontract.ensure(lambda self, result: isinstance(result, FormsDict))
@icontract.ensure(lambda self, result: result is not self.query and result is not self.forms)
@icontract.ensure(lambda self, result, pre_query_keys, pre_forms_keys: set(result.keys()) == pre_query_keys.union(pre_forms_keys))
@icontract.ensure(lambda self, result, pre_query_values, pre_forms_values: all(tuple(result.getall(k)) == pre_query_values.get(k, tuple()) + pre_forms_values.get(k, tuple()) for k in set(pre_query_values.keys()).union(pre_forms_values.keys())))
@icontract.ensure(lambda self, result, pre_query_items_count, pre_forms_items_count: sum(1 for _ in result.allitems()) == pre_query_items_count + pre_forms_items_count)
@icontract.ensure(lambda self, result, pre_forms_values: all(result.get(k) == vals[-1] for k, vals in pre_forms_values.items()))
@icontract.ensure(lambda self, result, pre_query_values, pre_forms_keys: all(result.get(k) == pre_query_values[k][-1] for k in set(pre_query_values.keys()) - pre_forms_keys))
```
```
limited spec

pre_query_values
```
failed
```
@icontract.ensure(lambda result, self: isinstance(result, FormsDict))
@icontract.ensure(lambda result, self: set(result.keys()) == set(self.query.keys()) | set(self.forms.keys()))
@icontract.ensure(lambda result, self: all((k in self.forms and result.get(k) == self.forms.get(k)) or (k not in self.forms and result.get(k) == self.query.get(k)) for k in result.keys()))
```
