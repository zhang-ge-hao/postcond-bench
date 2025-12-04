https://github.com/dynaconf/dynaconf/blob/09c10d1a91854894986da19fb70f1b54a47cd865/./dynaconf/nodes.py#L170-L187
```
@icontract.snapshot(lambda self: dict(self))
@icontract.ensure(lambda result, self, OLD: isinstance(result, dict))
@icontract.ensure(lambda result, self, OLD: set(result.keys()) == set(OLD.self.keys()))
@icontract.ensure(lambda result, self, OLD: all((k in result) and (result[k] is result) for k in OLD.self if OLD.self[k] is self))
@icontract.ensure(lambda result, self, OLD: all((k in result) and (result[k] is not result) for k in OLD.self if OLD.self[k] is not self))
@icontract.ensure(lambda result, self, OLD: all(isinstance(result[k], dict) for k in OLD.self if isinstance(OLD.self[k], DataDict)))
@icontract.ensure(lambda result, self, OLD: all(isinstance(result[k], list) for k in OLD.self if isinstance(OLD.self[k], DataList)))
@icontract.ensure(lambda result, self, OLD: all(not isinstance(result[k], (DataDict, DataList)) for k in OLD.self))
@icontract.ensure(lambda result, self: all((k in result) and not getattr(result[k], "_dynaconf_lazy_format", None) for k in self.keys() if getattr(self.get(k, bypass_eval=True), "_dynaconf_lazy_format", None)))
```
```
@icontract.snapshot(lambda self: dict(self))
@icontract.ensure(lambda result, self, OLD: isinstance(result, dict))
@icontract.ensure(lambda result, self, OLD: set(result.keys()) == set(OLD.self.keys()))
@icontract.ensure(lambda result, self, OLD: all(result[k] is result for k in OLD.self if OLD.self[k] is self))
@icontract.ensure(lambda result, self, OLD: all(result[k] is not result for k in OLD.self if OLD.self[k] is not self))
@icontract.ensure(lambda result, self, OLD: all(isinstance(result[k], dict) for k in OLD.self if isinstance(OLD.self[k], DataDict)))
@icontract.ensure(lambda result, self, OLD: all(isinstance(result[k], list) for k in OLD.self if isinstance(OLD.self[k], DataList)))
@icontract.ensure(lambda result, self, OLD: all(not isinstance(result[k], (DataDict, DataList)) for k in OLD.self))
```
[0, 1, 2, 4, 5]
===== 0 =====
```
         box_deprecation_warning(
             "to_dict", "DataDict", "Use dict(data_dict) instead."
         )  # pragma: nocover
-        out_dict = dict(self)
+        out_dict = dict()  # This initializes an empty dictionary, losing all data
         for k, v in out_dict.items():
             if v is self:
                 out_dict[k] = out_dict
```
```
    def to_dict(self):
        """
        Turn the DataDict and sub DataDicts back into a native python dictionary.

        :return: python dictionary of this DataDict
        """
        box_deprecation_warning(
            "to_dict", "DataDict", "Use dict(data_dict) instead."
        )  # pragma: nocover
        out_dict = dict()  # This initializes an empty dictionary, losing all data
        for k, v in out_dict.items():
            if v is self:
                out_dict[k] = out_dict
            elif isinstance(v, DataDict):
                out_dict[k] = v.to_dict()
            elif isinstance(v, DataList):
                out_dict[k] = v.to_list()
        return out_dict
```
===== 1 =====
```
         box_deprecation_warning(
             "to_dict", "DataDict", "Use dict(data_dict) instead."
         )  # pragma: nocover
-        out_dict = dict(self)
+        out_dict = dict(self.items())  # This results in a dictionary of items, losing DataDict structure
         for k, v in out_dict.items():
             if v is self:
                 out_dict[k] = out_dict
```
```
    def to_dict(self):
        """
        Turn the DataDict and sub DataDicts back into a native python dictionary.

        :return: python dictionary of this DataDict
        """
        box_deprecation_warning(
            "to_dict", "DataDict", "Use dict(data_dict) instead."
        )  # pragma: nocover
        out_dict = dict(self.items())  # This results in a dictionary of items, losing DataDict structure
        for k, v in out_dict.items():
            if v is self:
                out_dict[k] = out_dict
            elif isinstance(v, DataDict):
                out_dict[k] = v.to_dict()
            elif isinstance(v, DataList):
                out_dict[k] = v.to_list()
        return out_dict
```
===== 2 =====
```
         box_deprecation_warning(
             "to_dict", "DataDict", "Use dict(data_dict) instead."
         )  # pragma: nocover
-        out_dict = dict(self)
+        out_dict = {k: v for k, v in self.items()}  # This does not include the core metadata
         for k, v in out_dict.items():
             if v is self:
                 out_dict[k] = out_dict
```
```
    def to_dict(self):
        """
        Turn the DataDict and sub DataDicts back into a native python dictionary.

        :return: python dictionary of this DataDict
        """
        box_deprecation_warning(
            "to_dict", "DataDict", "Use dict(data_dict) instead."
        )  # pragma: nocover
        out_dict = {k: v for k, v in self.items()}  # This does not include the core metadata
        for k, v in out_dict.items():
            if v is self:
                out_dict[k] = out_dict
            elif isinstance(v, DataDict):
                out_dict[k] = v.to_dict()
            elif isinstance(v, DataList):
                out_dict[k] = v.to_list()
        return out_dict
```
===== 4 =====
```
         )  # pragma: nocover
         out_dict = dict(self)
         for k, v in out_dict.items():
-            if v is self:
+            if v is not self:
                 out_dict[k] = out_dict
             elif isinstance(v, DataDict):
                 out_dict[k] = v.to_dict()
```
```
    def to_dict(self):
        """
        Turn the DataDict and sub DataDicts back into a native python dictionary.

        :return: python dictionary of this DataDict
        """
        box_deprecation_warning(
            "to_dict", "DataDict", "Use dict(data_dict) instead."
        )  # pragma: nocover
        out_dict = dict(self)
        for k, v in out_dict.items():
            if v is not self:
                out_dict[k] = out_dict
            elif isinstance(v, DataDict):
                out_dict[k] = v.to_dict()
            elif isinstance(v, DataList):
                out_dict[k] = v.to_list()
        return out_dict
```
===== 5 =====
```
         )  # pragma: nocover
         out_dict = dict(self)
         for k, v in out_dict.items():
-            if v is self:
+            if v is not self:
                 out_dict[k] = out_dict
             elif isinstance(v, DataDict):
                 out_dict[k] = v.to_dict()
             elif isinstance(v, DataList):
                 out_dict[k] = v.to_list()
-        return out_dict+        return out_dict
```
```
    def to_dict(self):
        """
        Turn the DataDict and sub DataDicts back into a native python dictionary.

        :return: python dictionary of this DataDict
        """
        box_deprecation_warning(
            "to_dict", "DataDict", "Use dict(data_dict) instead."
        )  # pragma: nocover
        out_dict = dict(self)
        for k, v in out_dict.items():
            if v is not self:
                out_dict[k] = out_dict
            elif isinstance(v, DataDict):
                out_dict[k] = v.to_dict()
            elif isinstance(v, DataList):
                out_dict[k] = v.to_list()
        return out_dict

```
