https://github.com/bottlepy/bottle/blob/3d0ace47fe8e5ac5177b49597bd8ff872ff08d7b/./bottle.py#L1217-L1226
```
@icontract.snapshot(lambda self: set(self.query.keys()), name="pre_query_keys")
@icontract.snapshot(lambda self: set(self.forms.keys()), name="pre_forms_keys")
@icontract.snapshot(lambda self: {k: list(self.query.getall(k)) for k in self.query.keys()}, name="pre_query_map")
@icontract.snapshot(lambda self: {k: list(self.forms.getall(k)) for k in self.forms.keys()}, name="pre_forms_map")
@icontract.ensure(lambda result: isinstance(result, FormsDict))
@icontract.ensure(lambda self, result: result is not self.query and result is not self.forms)
@icontract.ensure(lambda pre_query_keys, pre_forms_keys, result: set(result.keys()) == pre_query_keys.union(pre_forms_keys))
@icontract.ensure(lambda pre_query_keys, pre_query_map, pre_forms_keys, result:
                  all(set(result.getall(k)) == set(pre_query_map[k]) for k in pre_query_keys - pre_forms_keys))
@icontract.ensure(lambda pre_forms_keys, pre_forms_map, pre_query_keys, result:
                  all(set(result.getall(k)) == set(pre_forms_map[k]) for k in pre_forms_keys - pre_query_keys))
@icontract.ensure(lambda pre_query_keys, pre_forms_keys, pre_query_map, pre_forms_map, result:
                  all(set(result.getall(k)) == set(pre_query_map[k]).union(set(pre_forms_map[k]))
                      for k in pre_query_keys.intersection(pre_forms_keys)))
@icontract.ensure(lambda result: all(not isinstance(v, FileUpload) for v in result.values()))
```
```
limited spec

pre_forms_keys
```
failed
```
@icontract.ensure(lambda result, self: isinstance(result, FormsDict))
@icontract.ensure(lambda result, self: set(result.keys()) == set(self.query.keys()) | set(self.forms.keys()))
@icontract.ensure(lambda result, self: all((k in self.forms and result.get(k) == self.forms.get(k)) or (k not in self.forms and result.get(k) == self.query.get(k)) for k in result.keys()))
```
