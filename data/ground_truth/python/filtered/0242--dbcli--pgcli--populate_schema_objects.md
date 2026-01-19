https://github.com/dbcli/pgcli/blob/f46d8446a34084cc2532041619d1f08bda7213e7/./pgcli/pgcompleter.py#L946-L957
```
🈚️

Timeout
```
```
@icontract.snapshot(lambda self, schema, obj_type: list(self._get_schemas(obj_type, schema)), name="SCHS")
@icontract.snapshot(lambda self, schema, obj_type: {sch: list(self.dbmetadata[obj_type][sch].keys()) for sch in list(self._get_schemas(obj_type, schema))}, name="DBMAP")
@icontract.snapshot(lambda self, schema, obj_type: [(obj, self._maybe_schema(schema=sch, parent=schema)) for sch in list(self._get_schemas(obj_type, schema)) for obj in list(self.dbmetadata[obj_type][sch].keys())], name="EXPECTED_SEQ")
@icontract.ensure(lambda OLD, result: isinstance(result, list))
@icontract.ensure(lambda OLD, result: len(result) == sum(len(v) for v in OLD.DBMAP.values()))
@icontract.ensure(lambda OLD, result: [(o.name, o.schema) for o in result] == OLD.EXPECTED_SEQ)
```
[7, 8, 9]
===== 7 =====
```
 
         return [
             SchemaObject(name=obj, schema=(self._maybe_schema(schema=sch, parent=schema)))
-            for sch in self._get_schemas(obj_type, schema)
+            for sch in self._get_schemas(obj_type, "public")  # Hardcoding schema to "public"
             for obj in self.dbmetadata[obj_type][sch].keys()
         ]
```
```
    def populate_schema_objects(self, schema, obj_type):
        """Returns a list of SchemaObjects representing tables or views.

        :param schema is the schema qualification input by the user (if any)

        """

        return [
            SchemaObject(name=obj, schema=(self._maybe_schema(schema=sch, parent=schema)))
            for sch in self._get_schemas(obj_type, "public")  # Hardcoding schema to "public"
            for obj in self.dbmetadata[obj_type][sch].keys()
        ]
```
===== 8 =====
```
 
         return [
             SchemaObject(name=obj, schema=(self._maybe_schema(schema=sch, parent=schema)))
-            for sch in self._get_schemas(obj_type, schema)
+            for sch in self._get_schemas(obj_type, None)
             for obj in self.dbmetadata[obj_type][sch].keys()
-        ]+        ]
```
```
    def populate_schema_objects(self, schema, obj_type):
        """Returns a list of SchemaObjects representing tables or views.

        :param schema is the schema qualification input by the user (if any)

        """

        return [
            SchemaObject(name=obj, schema=(self._maybe_schema(schema=sch, parent=schema)))
            for sch in self._get_schemas(obj_type, None)
            for obj in self.dbmetadata[obj_type][sch].keys()
        ]

```
===== 9 =====
```
         return [
             SchemaObject(name=obj, schema=(self._maybe_schema(schema=sch, parent=schema)))
             for sch in self._get_schemas(obj_type, schema)
-            for obj in self.dbmetadata[obj_type][sch].keys()
+            for obj in self.dbmetadata[obj_type][sch].keys() if obj.startswith('a')  # This will filter keys, potentially omitting valid objects.
         ]
```
```
    def populate_schema_objects(self, schema, obj_type):
        """Returns a list of SchemaObjects representing tables or views.

        :param schema is the schema qualification input by the user (if any)

        """

        return [
            SchemaObject(name=obj, schema=(self._maybe_schema(schema=sch, parent=schema)))
            for sch in self._get_schemas(obj_type, schema)
            for obj in self.dbmetadata[obj_type][sch].keys() if obj.startswith('a')  # This will filter keys, potentially omitting valid objects.
        ]
```
