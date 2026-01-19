https://github.com/dbcli/pgcli/blob/f46d8446a34084cc2532041619d1f08bda7213e7/./pgcli/pgcompleter.py#L885-L929
```
🈚️

Timeout

@icontract.ensure(
    lambda self, scoped_tbls, local_tbls, result:
    isinstance(result, OrderedDict),
    "populate_scoped_cols must return an OrderedDict to preserve table order.",
)
@icontract.ensure(
    lambda self, scoped_tbls, local_tbls, result:
    all(
        isinstance(key, TableReference) and isinstance(cols, list)
        for key, cols in result.items()
    ),
    "Keys must be TableReference objects and values must be lists.",
)
@icontract.ensure(
    lambda self, scoped_tbls, local_tbls, result:
    all(
        all(isinstance(col, ColumnMetadata) for col in cols)
        for cols in result.values()
    ),
    "Every column entry must be a ColumnMetadata.",
)
@icontract.ensure(
    # 每一个结果中的 TableReference 都必须来自 scoped_tbls 或 local_tbls
    lambda self, scoped_tbls, local_tbls, result:
    all(
        # 要么能在 scoped_tbls 里找到完全对应的表引用
        any(
            normalize_ref(ref.name) == normalize_ref(key.name)
            and ref.schema == key.schema
            and getattr(ref, "is_function", False) == getattr(key, "is_function", False)
            for ref in scoped_tbls
        )
        # 要么是 CTE：名字与某个 local_tbl 相同、schema 为 None、且不是函数
        or any(
            normalize_ref(local.name) == normalize_ref(key.name)
            and key.schema is None
            and not getattr(key, "is_function", False)
            for local in local_tbls
        )
        for key in result.keys()
    ),
    "Every returned table must correspond to either a scoped table or a local CTE.",
)
@icontract.ensure(
    # 对于被 CTE 覆盖的表（无 schema 且有同名 local_tbl）：
    # 结果中对应的 TableReference 必须保留原来的 alias（即 scoped_tbl.alias）
    lambda self, scoped_tbls, local_tbls, result:
    all(
        # 如果这个 scoped_tbl 没有被同名 CTE 覆盖，则不做约束
        not (
            tbl.schema is None
            and any(
                normalize_ref(local.name) == normalize_ref(tbl.name)
                for local in local_tbls
            )
        )
        # 否则，必须存在一个 result 的 key：
        #   1. name 与该表同名（忽略大小写/引号）
        #   2. alias 与原来的 scoped_tbl.alias 一致
        #   3. 有列信息（非空）
        or any(
            normalize_ref(key.name) == normalize_ref(tbl.name)
            and key.alias == tbl.alias
            and len(result[key]) > 0
            for key in result.keys()
        )
        for tbl in scoped_tbls
    ),
    (
        "When a table in scope is shadowed by a CTE with the same name, "
        "the completion must keep the original table alias and expose "
        "columns for that reference."
    ),
)
```
```
None
```
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50]
===== 0 =====
```
         :return: {TableReference:{colname:ColumnMetaData}}
 
         """
-        ctes = {normalize_ref(t.name): t.columns for t in local_tbls}
+        ctes = {normalize_ref(t.name): t for t in local_tbls}
         columns = OrderedDict()
         meta = self.dbmetadata
```
```
    def populate_scoped_cols(self, scoped_tbls, local_tbls=()):
        """Find all columns in a set of scoped_tables.

        :param scoped_tbls: list of TableReference namedtuples
        :param local_tbls: tuple(TableMetadata)
        :return: {TableReference:{colname:ColumnMetaData}}

        """
        ctes = {normalize_ref(t.name): t for t in local_tbls}
        columns = OrderedDict()
        meta = self.dbmetadata

        def addcols(schema, rel, alias, reltype, cols):
            tbl = TableReference(schema, rel, alias, reltype == "functions")
            if tbl not in columns:
                columns[tbl] = []
            columns[tbl].extend(cols)

        for tbl in scoped_tbls:
            # Local tables should shadow database tables
            if tbl.schema is None and normalize_ref(tbl.name) in ctes:
                cols = ctes[normalize_ref(tbl.name)]
                addcols(None, tbl.name, "CTE", tbl.alias, cols)
                continue
            schemas = [tbl.schema] if tbl.schema else self.search_path
            for schema in schemas:
                relname = self.escape_name(tbl.name)
                schema = self.escape_name(schema)
                if tbl.is_function:
                    # Return column names from a set-returning function
                    # Get an array of FunctionMetadata objects
                    functions = meta["functions"].get(schema, {}).get(relname)
                    for func in functions or []:
                        # func is a FunctionMetadata object
                        cols = func.fields()
                        addcols(schema, relname, tbl.alias, "functions", cols)
                else:
                    for reltype in ("tables", "views"):
                        cols = meta[reltype].get(schema, {}).get(relname)
                        if cols:
                            cols = cols.values()
                            addcols(schema, relname, tbl.alias, reltype, cols)
                            break

        return columns
```
===== 1 =====
```
         :return: {TableReference:{colname:ColumnMetaData}}
 
         """
-        ctes = {normalize_ref(t.name): t.columns for t in local_tbls}
+        ctes = {normalize_ref(t.name): t.columns for t in local_tbls if t.name.startswith('a')}
         columns = OrderedDict()
         meta = self.dbmetadata
```
```
    def populate_scoped_cols(self, scoped_tbls, local_tbls=()):
        """Find all columns in a set of scoped_tables.

        :param scoped_tbls: list of TableReference namedtuples
        :param local_tbls: tuple(TableMetadata)
        :return: {TableReference:{colname:ColumnMetaData}}

        """
        ctes = {normalize_ref(t.name): t.columns for t in local_tbls if t.name.startswith('a')}
        columns = OrderedDict()
        meta = self.dbmetadata

        def addcols(schema, rel, alias, reltype, cols):
            tbl = TableReference(schema, rel, alias, reltype == "functions")
            if tbl not in columns:
                columns[tbl] = []
            columns[tbl].extend(cols)

        for tbl in scoped_tbls:
            # Local tables should shadow database tables
            if tbl.schema is None and normalize_ref(tbl.name) in ctes:
                cols = ctes[normalize_ref(tbl.name)]
                addcols(None, tbl.name, "CTE", tbl.alias, cols)
                continue
            schemas = [tbl.schema] if tbl.schema else self.search_path
            for schema in schemas:
                relname = self.escape_name(tbl.name)
                schema = self.escape_name(schema)
                if tbl.is_function:
                    # Return column names from a set-returning function
                    # Get an array of FunctionMetadata objects
                    functions = meta["functions"].get(schema, {}).get(relname)
                    for func in functions or []:
                        # func is a FunctionMetadata object
                        cols = func.fields()
                        addcols(schema, relname, tbl.alias, "functions", cols)
                else:
                    for reltype in ("tables", "views"):
                        cols = meta[reltype].get(schema, {}).get(relname)
                        if cols:
                            cols = cols.values()
                            addcols(schema, relname, tbl.alias, reltype, cols)
                            break

        return columns
```
===== 2 =====
```
         :return: {TableReference:{colname:ColumnMetaData}}
 
         """
-        ctes = {normalize_ref(t.name): t.columns for t in local_tbls}
+        ctes = {t.name: t.columns for t in local_tbls}
         columns = OrderedDict()
         meta = self.dbmetadata
```
```
    def populate_scoped_cols(self, scoped_tbls, local_tbls=()):
        """Find all columns in a set of scoped_tables.

        :param scoped_tbls: list of TableReference namedtuples
        :param local_tbls: tuple(TableMetadata)
        :return: {TableReference:{colname:ColumnMetaData}}

        """
        ctes = {t.name: t.columns for t in local_tbls}
        columns = OrderedDict()
        meta = self.dbmetadata

        def addcols(schema, rel, alias, reltype, cols):
            tbl = TableReference(schema, rel, alias, reltype == "functions")
            if tbl not in columns:
                columns[tbl] = []
            columns[tbl].extend(cols)

        for tbl in scoped_tbls:
            # Local tables should shadow database tables
            if tbl.schema is None and normalize_ref(tbl.name) in ctes:
                cols = ctes[normalize_ref(tbl.name)]
                addcols(None, tbl.name, "CTE", tbl.alias, cols)
                continue
            schemas = [tbl.schema] if tbl.schema else self.search_path
            for schema in schemas:
                relname = self.escape_name(tbl.name)
                schema = self.escape_name(schema)
                if tbl.is_function:
                    # Return column names from a set-returning function
                    # Get an array of FunctionMetadata objects
                    functions = meta["functions"].get(schema, {}).get(relname)
                    for func in functions or []:
                        # func is a FunctionMetadata object
                        cols = func.fields()
                        addcols(schema, relname, tbl.alias, "functions", cols)
                else:
                    for reltype in ("tables", "views"):
                        cols = meta[reltype].get(schema, {}).get(relname)
                        if cols:
                            cols = cols.values()
                            addcols(schema, relname, tbl.alias, reltype, cols)
                            break

        return columns
```
===== 3 =====
```
         meta = self.dbmetadata
 
         def addcols(schema, rel, alias, reltype, cols):
-            tbl = TableReference(schema, rel, alias, reltype == "functions")
+            tbl = TableReference(None, rel, alias, reltype == "functions")
             if tbl not in columns:
                 columns[tbl] = []
             columns[tbl].extend(cols)
@@ -42,4 +42,4 @@                             addcols(schema, relname, tbl.alias, reltype, cols)
                             break
 
-        return columns+        return columns
```
```
    def populate_scoped_cols(self, scoped_tbls, local_tbls=()):
        """Find all columns in a set of scoped_tables.

        :param scoped_tbls: list of TableReference namedtuples
        :param local_tbls: tuple(TableMetadata)
        :return: {TableReference:{colname:ColumnMetaData}}

        """
        ctes = {normalize_ref(t.name): t.columns for t in local_tbls}
        columns = OrderedDict()
        meta = self.dbmetadata

        def addcols(schema, rel, alias, reltype, cols):
            tbl = TableReference(None, rel, alias, reltype == "functions")
            if tbl not in columns:
                columns[tbl] = []
            columns[tbl].extend(cols)

        for tbl in scoped_tbls:
            # Local tables should shadow database tables
            if tbl.schema is None and normalize_ref(tbl.name) in ctes:
                cols = ctes[normalize_ref(tbl.name)]
                addcols(None, tbl.name, "CTE", tbl.alias, cols)
                continue
            schemas = [tbl.schema] if tbl.schema else self.search_path
            for schema in schemas:
                relname = self.escape_name(tbl.name)
                schema = self.escape_name(schema)
                if tbl.is_function:
                    # Return column names from a set-returning function
                    # Get an array of FunctionMetadata objects
                    functions = meta["functions"].get(schema, {}).get(relname)
                    for func in functions or []:
                        # func is a FunctionMetadata object
                        cols = func.fields()
                        addcols(schema, relname, tbl.alias, "functions", cols)
                else:
                    for reltype in ("tables", "views"):
                        cols = meta[reltype].get(schema, {}).get(relname)
                        if cols:
                            cols = cols.values()
                            addcols(schema, relname, tbl.alias, reltype, cols)
                            break

        return columns

```
===== 4 =====
```
         meta = self.dbmetadata
 
         def addcols(schema, rel, alias, reltype, cols):
-            tbl = TableReference(schema, rel, alias, reltype == "functions")
+            tbl = TableReference(schema, None, alias, reltype == "functions")
             if tbl not in columns:
                 columns[tbl] = []
             columns[tbl].extend(cols)
@@ -42,4 +42,4 @@                             addcols(schema, relname, tbl.alias, reltype, cols)
                             break
 
-        return columns+        return columns
```
```
    def populate_scoped_cols(self, scoped_tbls, local_tbls=()):
        """Find all columns in a set of scoped_tables.

        :param scoped_tbls: list of TableReference namedtuples
        :param local_tbls: tuple(TableMetadata)
        :return: {TableReference:{colname:ColumnMetaData}}

        """
        ctes = {normalize_ref(t.name): t.columns for t in local_tbls}
        columns = OrderedDict()
        meta = self.dbmetadata

        def addcols(schema, rel, alias, reltype, cols):
            tbl = TableReference(schema, None, alias, reltype == "functions")
            if tbl not in columns:
                columns[tbl] = []
            columns[tbl].extend(cols)

        for tbl in scoped_tbls:
            # Local tables should shadow database tables
            if tbl.schema is None and normalize_ref(tbl.name) in ctes:
                cols = ctes[normalize_ref(tbl.name)]
                addcols(None, tbl.name, "CTE", tbl.alias, cols)
                continue
            schemas = [tbl.schema] if tbl.schema else self.search_path
            for schema in schemas:
                relname = self.escape_name(tbl.name)
                schema = self.escape_name(schema)
                if tbl.is_function:
                    # Return column names from a set-returning function
                    # Get an array of FunctionMetadata objects
                    functions = meta["functions"].get(schema, {}).get(relname)
                    for func in functions or []:
                        # func is a FunctionMetadata object
                        cols = func.fields()
                        addcols(schema, relname, tbl.alias, "functions", cols)
                else:
                    for reltype in ("tables", "views"):
                        cols = meta[reltype].get(schema, {}).get(relname)
                        if cols:
                            cols = cols.values()
                            addcols(schema, relname, tbl.alias, reltype, cols)
                            break

        return columns

```
===== 5 =====
```
         meta = self.dbmetadata
 
         def addcols(schema, rel, alias, reltype, cols):
-            tbl = TableReference(schema, rel, alias, reltype == "functions")
+            tbl = TableReference(schema, rel, None, reltype == "functions")
             if tbl not in columns:
                 columns[tbl] = []
             columns[tbl].extend(cols)
@@ -42,4 +42,4 @@                             addcols(schema, relname, tbl.alias, reltype, cols)
                             break
 
-        return columns+        return columns
```
```
    def populate_scoped_cols(self, scoped_tbls, local_tbls=()):
        """Find all columns in a set of scoped_tables.

        :param scoped_tbls: list of TableReference namedtuples
        :param local_tbls: tuple(TableMetadata)
        :return: {TableReference:{colname:ColumnMetaData}}

        """
        ctes = {normalize_ref(t.name): t.columns for t in local_tbls}
        columns = OrderedDict()
        meta = self.dbmetadata

        def addcols(schema, rel, alias, reltype, cols):
            tbl = TableReference(schema, rel, None, reltype == "functions")
            if tbl not in columns:
                columns[tbl] = []
            columns[tbl].extend(cols)

        for tbl in scoped_tbls:
            # Local tables should shadow database tables
            if tbl.schema is None and normalize_ref(tbl.name) in ctes:
                cols = ctes[normalize_ref(tbl.name)]
                addcols(None, tbl.name, "CTE", tbl.alias, cols)
                continue
            schemas = [tbl.schema] if tbl.schema else self.search_path
            for schema in schemas:
                relname = self.escape_name(tbl.name)
                schema = self.escape_name(schema)
                if tbl.is_function:
                    # Return column names from a set-returning function
                    # Get an array of FunctionMetadata objects
                    functions = meta["functions"].get(schema, {}).get(relname)
                    for func in functions or []:
                        # func is a FunctionMetadata object
                        cols = func.fields()
                        addcols(schema, relname, tbl.alias, "functions", cols)
                else:
                    for reltype in ("tables", "views"):
                        cols = meta[reltype].get(schema, {}).get(relname)
                        if cols:
                            cols = cols.values()
                            addcols(schema, relname, tbl.alias, reltype, cols)
                            break

        return columns

```
===== 6 =====
```
             tbl = TableReference(schema, rel, alias, reltype == "functions")
             if tbl not in columns:
                 columns[tbl] = []
-            columns[tbl].extend(cols)
+            columns[tbl].extend(cols) if tbl not in columns else None  # Does nothing if tbl is already in columns
 
         for tbl in scoped_tbls:
             # Local tables should shadow database tables
```
```
    def populate_scoped_cols(self, scoped_tbls, local_tbls=()):
        """Find all columns in a set of scoped_tables.

        :param scoped_tbls: list of TableReference namedtuples
        :param local_tbls: tuple(TableMetadata)
        :return: {TableReference:{colname:ColumnMetaData}}

        """
        ctes = {normalize_ref(t.name): t.columns for t in local_tbls}
        columns = OrderedDict()
        meta = self.dbmetadata

        def addcols(schema, rel, alias, reltype, cols):
            tbl = TableReference(schema, rel, alias, reltype == "functions")
            if tbl not in columns:
                columns[tbl] = []
            columns[tbl].extend(cols) if tbl not in columns else None  # Does nothing if tbl is already in columns

        for tbl in scoped_tbls:
            # Local tables should shadow database tables
            if tbl.schema is None and normalize_ref(tbl.name) in ctes:
                cols = ctes[normalize_ref(tbl.name)]
                addcols(None, tbl.name, "CTE", tbl.alias, cols)
                continue
            schemas = [tbl.schema] if tbl.schema else self.search_path
            for schema in schemas:
                relname = self.escape_name(tbl.name)
                schema = self.escape_name(schema)
                if tbl.is_function:
                    # Return column names from a set-returning function
                    # Get an array of FunctionMetadata objects
                    functions = meta["functions"].get(schema, {}).get(relname)
                    for func in functions or []:
                        # func is a FunctionMetadata object
                        cols = func.fields()
                        addcols(schema, relname, tbl.alias, "functions", cols)
                else:
                    for reltype in ("tables", "views"):
                        cols = meta[reltype].get(schema, {}).get(relname)
                        if cols:
                            cols = cols.values()
                            addcols(schema, relname, tbl.alias, reltype, cols)
                            break

        return columns
```
===== 7 =====
```
                 columns[tbl] = []
             columns[tbl].extend(cols)
 
-        for tbl in scoped_tbls:
+        for tbl in self.databases:
             # Local tables should shadow database tables
             if tbl.schema is None and normalize_ref(tbl.name) in ctes:
                 cols = ctes[normalize_ref(tbl.name)]
```
```
    def populate_scoped_cols(self, scoped_tbls, local_tbls=()):
        """Find all columns in a set of scoped_tables.

        :param scoped_tbls: list of TableReference namedtuples
        :param local_tbls: tuple(TableMetadata)
        :return: {TableReference:{colname:ColumnMetaData}}

        """
        ctes = {normalize_ref(t.name): t.columns for t in local_tbls}
        columns = OrderedDict()
        meta = self.dbmetadata

        def addcols(schema, rel, alias, reltype, cols):
            tbl = TableReference(schema, rel, alias, reltype == "functions")
            if tbl not in columns:
                columns[tbl] = []
            columns[tbl].extend(cols)

        for tbl in self.databases:
            # Local tables should shadow database tables
            if tbl.schema is None and normalize_ref(tbl.name) in ctes:
                cols = ctes[normalize_ref(tbl.name)]
                addcols(None, tbl.name, "CTE", tbl.alias, cols)
                continue
            schemas = [tbl.schema] if tbl.schema else self.search_path
            for schema in schemas:
                relname = self.escape_name(tbl.name)
                schema = self.escape_name(schema)
                if tbl.is_function:
                    # Return column names from a set-returning function
                    # Get an array of FunctionMetadata objects
                    functions = meta["functions"].get(schema, {}).get(relname)
                    for func in functions or []:
                        # func is a FunctionMetadata object
                        cols = func.fields()
                        addcols(schema, relname, tbl.alias, "functions", cols)
                else:
                    for reltype in ("tables", "views"):
                        cols = meta[reltype].get(schema, {}).get(relname)
                        if cols:
                            cols = cols.values()
                            addcols(schema, relname, tbl.alias, reltype, cols)
                            break

        return columns
```
===== 8 =====
```
 
         for tbl in scoped_tbls:
             # Local tables should shadow database tables
-            if tbl.schema is None and normalize_ref(tbl.name) in ctes:
+            if tbl.schema is None and normalize_ref(tbl.name) in ctes and tbl.alias is not None:
                 cols = ctes[normalize_ref(tbl.name)]
                 addcols(None, tbl.name, "CTE", tbl.alias, cols)
                 continue
```
```
    def populate_scoped_cols(self, scoped_tbls, local_tbls=()):
        """Find all columns in a set of scoped_tables.

        :param scoped_tbls: list of TableReference namedtuples
        :param local_tbls: tuple(TableMetadata)
        :return: {TableReference:{colname:ColumnMetaData}}

        """
        ctes = {normalize_ref(t.name): t.columns for t in local_tbls}
        columns = OrderedDict()
        meta = self.dbmetadata

        def addcols(schema, rel, alias, reltype, cols):
            tbl = TableReference(schema, rel, alias, reltype == "functions")
            if tbl not in columns:
                columns[tbl] = []
            columns[tbl].extend(cols)

        for tbl in scoped_tbls:
            # Local tables should shadow database tables
            if tbl.schema is None and normalize_ref(tbl.name) in ctes and tbl.alias is not None:
                cols = ctes[normalize_ref(tbl.name)]
                addcols(None, tbl.name, "CTE", tbl.alias, cols)
                continue
            schemas = [tbl.schema] if tbl.schema else self.search_path
            for schema in schemas:
                relname = self.escape_name(tbl.name)
                schema = self.escape_name(schema)
                if tbl.is_function:
                    # Return column names from a set-returning function
                    # Get an array of FunctionMetadata objects
                    functions = meta["functions"].get(schema, {}).get(relname)
                    for func in functions or []:
                        # func is a FunctionMetadata object
                        cols = func.fields()
                        addcols(schema, relname, tbl.alias, "functions", cols)
                else:
                    for reltype in ("tables", "views"):
                        cols = meta[reltype].get(schema, {}).get(relname)
                        if cols:
                            cols = cols.values()
                            addcols(schema, relname, tbl.alias, reltype, cols)
                            break

        return columns
```
===== 9 =====
```
 
         for tbl in scoped_tbls:
             # Local tables should shadow database tables
-            if tbl.schema is None and normalize_ref(tbl.name) in ctes:
+            if tbl.schema is None and normalize_ref(tbl.name) in ctes and tbl.name.startswith("temp_"):
                 cols = ctes[normalize_ref(tbl.name)]
                 addcols(None, tbl.name, "CTE", tbl.alias, cols)
                 continue
```
```
    def populate_scoped_cols(self, scoped_tbls, local_tbls=()):
        """Find all columns in a set of scoped_tables.

        :param scoped_tbls: list of TableReference namedtuples
        :param local_tbls: tuple(TableMetadata)
        :return: {TableReference:{colname:ColumnMetaData}}

        """
        ctes = {normalize_ref(t.name): t.columns for t in local_tbls}
        columns = OrderedDict()
        meta = self.dbmetadata

        def addcols(schema, rel, alias, reltype, cols):
            tbl = TableReference(schema, rel, alias, reltype == "functions")
            if tbl not in columns:
                columns[tbl] = []
            columns[tbl].extend(cols)

        for tbl in scoped_tbls:
            # Local tables should shadow database tables
            if tbl.schema is None and normalize_ref(tbl.name) in ctes and tbl.name.startswith("temp_"):
                cols = ctes[normalize_ref(tbl.name)]
                addcols(None, tbl.name, "CTE", tbl.alias, cols)
                continue
            schemas = [tbl.schema] if tbl.schema else self.search_path
            for schema in schemas:
                relname = self.escape_name(tbl.name)
                schema = self.escape_name(schema)
                if tbl.is_function:
                    # Return column names from a set-returning function
                    # Get an array of FunctionMetadata objects
                    functions = meta["functions"].get(schema, {}).get(relname)
                    for func in functions or []:
                        # func is a FunctionMetadata object
                        cols = func.fields()
                        addcols(schema, relname, tbl.alias, "functions", cols)
                else:
                    for reltype in ("tables", "views"):
                        cols = meta[reltype].get(schema, {}).get(relname)
                        if cols:
                            cols = cols.values()
                            addcols(schema, relname, tbl.alias, reltype, cols)
                            break

        return columns
```
===== 10 =====
```
 
         for tbl in scoped_tbls:
             # Local tables should shadow database tables
-            if tbl.schema is None and normalize_ref(tbl.name) in ctes:
+            if tbl.schema is not None and normalize_ref(tbl.name) in ctes:
                 cols = ctes[normalize_ref(tbl.name)]
                 addcols(None, tbl.name, "CTE", tbl.alias, cols)
                 continue
```
```
    def populate_scoped_cols(self, scoped_tbls, local_tbls=()):
        """Find all columns in a set of scoped_tables.

        :param scoped_tbls: list of TableReference namedtuples
        :param local_tbls: tuple(TableMetadata)
        :return: {TableReference:{colname:ColumnMetaData}}

        """
        ctes = {normalize_ref(t.name): t.columns for t in local_tbls}
        columns = OrderedDict()
        meta = self.dbmetadata

        def addcols(schema, rel, alias, reltype, cols):
            tbl = TableReference(schema, rel, alias, reltype == "functions")
            if tbl not in columns:
                columns[tbl] = []
            columns[tbl].extend(cols)

        for tbl in scoped_tbls:
            # Local tables should shadow database tables
            if tbl.schema is not None and normalize_ref(tbl.name) in ctes:
                cols = ctes[normalize_ref(tbl.name)]
                addcols(None, tbl.name, "CTE", tbl.alias, cols)
                continue
            schemas = [tbl.schema] if tbl.schema else self.search_path
            for schema in schemas:
                relname = self.escape_name(tbl.name)
                schema = self.escape_name(schema)
                if tbl.is_function:
                    # Return column names from a set-returning function
                    # Get an array of FunctionMetadata objects
                    functions = meta["functions"].get(schema, {}).get(relname)
                    for func in functions or []:
                        # func is a FunctionMetadata object
                        cols = func.fields()
                        addcols(schema, relname, tbl.alias, "functions", cols)
                else:
                    for reltype in ("tables", "views"):
                        cols = meta[reltype].get(schema, {}).get(relname)
                        if cols:
                            cols = cols.values()
                            addcols(schema, relname, tbl.alias, reltype, cols)
                            break

        return columns
```
===== 11 =====
```
 
         for tbl in scoped_tbls:
             # Local tables should shadow database tables
-            if tbl.schema is None and normalize_ref(tbl.name) in ctes:
+            if tbl.schema is not None and normalize_ref(tbl.name) in ctes:
                 cols = ctes[normalize_ref(tbl.name)]
                 addcols(None, tbl.name, "CTE", tbl.alias, cols)
                 continue
@@ -42,4 +42,4 @@                             addcols(schema, relname, tbl.alias, reltype, cols)
                             break
 
-        return columns+        return columns
```
```
    def populate_scoped_cols(self, scoped_tbls, local_tbls=()):
        """Find all columns in a set of scoped_tables.

        :param scoped_tbls: list of TableReference namedtuples
        :param local_tbls: tuple(TableMetadata)
        :return: {TableReference:{colname:ColumnMetaData}}

        """
        ctes = {normalize_ref(t.name): t.columns for t in local_tbls}
        columns = OrderedDict()
        meta = self.dbmetadata

        def addcols(schema, rel, alias, reltype, cols):
            tbl = TableReference(schema, rel, alias, reltype == "functions")
            if tbl not in columns:
                columns[tbl] = []
            columns[tbl].extend(cols)

        for tbl in scoped_tbls:
            # Local tables should shadow database tables
            if tbl.schema is not None and normalize_ref(tbl.name) in ctes:
                cols = ctes[normalize_ref(tbl.name)]
                addcols(None, tbl.name, "CTE", tbl.alias, cols)
                continue
            schemas = [tbl.schema] if tbl.schema else self.search_path
            for schema in schemas:
                relname = self.escape_name(tbl.name)
                schema = self.escape_name(schema)
                if tbl.is_function:
                    # Return column names from a set-returning function
                    # Get an array of FunctionMetadata objects
                    functions = meta["functions"].get(schema, {}).get(relname)
                    for func in functions or []:
                        # func is a FunctionMetadata object
                        cols = func.fields()
                        addcols(schema, relname, tbl.alias, "functions", cols)
                else:
                    for reltype in ("tables", "views"):
                        cols = meta[reltype].get(schema, {}).get(relname)
                        if cols:
                            cols = cols.values()
                            addcols(schema, relname, tbl.alias, reltype, cols)
                            break

        return columns

```
===== 12 =====
```
         for tbl in scoped_tbls:
             # Local tables should shadow database tables
             if tbl.schema is None and normalize_ref(tbl.name) in ctes:
-                cols = ctes[normalize_ref(tbl.name)]
+                cols = ctes[normalize_ref(tbl.name)] if tbl.name in ctes else []
                 addcols(None, tbl.name, "CTE", tbl.alias, cols)
                 continue
             schemas = [tbl.schema] if tbl.schema else self.search_path
```
```
    def populate_scoped_cols(self, scoped_tbls, local_tbls=()):
        """Find all columns in a set of scoped_tables.

        :param scoped_tbls: list of TableReference namedtuples
        :param local_tbls: tuple(TableMetadata)
        :return: {TableReference:{colname:ColumnMetaData}}

        """
        ctes = {normalize_ref(t.name): t.columns for t in local_tbls}
        columns = OrderedDict()
        meta = self.dbmetadata

        def addcols(schema, rel, alias, reltype, cols):
            tbl = TableReference(schema, rel, alias, reltype == "functions")
            if tbl not in columns:
                columns[tbl] = []
            columns[tbl].extend(cols)

        for tbl in scoped_tbls:
            # Local tables should shadow database tables
            if tbl.schema is None and normalize_ref(tbl.name) in ctes:
                cols = ctes[normalize_ref(tbl.name)] if tbl.name in ctes else []
                addcols(None, tbl.name, "CTE", tbl.alias, cols)
                continue
            schemas = [tbl.schema] if tbl.schema else self.search_path
            for schema in schemas:
                relname = self.escape_name(tbl.name)
                schema = self.escape_name(schema)
                if tbl.is_function:
                    # Return column names from a set-returning function
                    # Get an array of FunctionMetadata objects
                    functions = meta["functions"].get(schema, {}).get(relname)
                    for func in functions or []:
                        # func is a FunctionMetadata object
                        cols = func.fields()
                        addcols(schema, relname, tbl.alias, "functions", cols)
                else:
                    for reltype in ("tables", "views"):
                        cols = meta[reltype].get(schema, {}).get(relname)
                        if cols:
                            cols = cols.values()
                            addcols(schema, relname, tbl.alias, reltype, cols)
                            break

        return columns
```
===== 13 =====
```
             # Local tables should shadow database tables
             if tbl.schema is None and normalize_ref(tbl.name) in ctes:
                 cols = ctes[normalize_ref(tbl.name)]
-                addcols(None, tbl.name, "CTE", tbl.alias, cols)
+                addcols(None, tbl.name, "CTE", tbl.alias, [])  # Passes an empty list instead of the actual columns
                 continue
             schemas = [tbl.schema] if tbl.schema else self.search_path
             for schema in schemas:
```
```
    def populate_scoped_cols(self, scoped_tbls, local_tbls=()):
        """Find all columns in a set of scoped_tables.

        :param scoped_tbls: list of TableReference namedtuples
        :param local_tbls: tuple(TableMetadata)
        :return: {TableReference:{colname:ColumnMetaData}}

        """
        ctes = {normalize_ref(t.name): t.columns for t in local_tbls}
        columns = OrderedDict()
        meta = self.dbmetadata

        def addcols(schema, rel, alias, reltype, cols):
            tbl = TableReference(schema, rel, alias, reltype == "functions")
            if tbl not in columns:
                columns[tbl] = []
            columns[tbl].extend(cols)

        for tbl in scoped_tbls:
            # Local tables should shadow database tables
            if tbl.schema is None and normalize_ref(tbl.name) in ctes:
                cols = ctes[normalize_ref(tbl.name)]
                addcols(None, tbl.name, "CTE", tbl.alias, [])  # Passes an empty list instead of the actual columns
                continue
            schemas = [tbl.schema] if tbl.schema else self.search_path
            for schema in schemas:
                relname = self.escape_name(tbl.name)
                schema = self.escape_name(schema)
                if tbl.is_function:
                    # Return column names from a set-returning function
                    # Get an array of FunctionMetadata objects
                    functions = meta["functions"].get(schema, {}).get(relname)
                    for func in functions or []:
                        # func is a FunctionMetadata object
                        cols = func.fields()
                        addcols(schema, relname, tbl.alias, "functions", cols)
                else:
                    for reltype in ("tables", "views"):
                        cols = meta[reltype].get(schema, {}).get(relname)
                        if cols:
                            cols = cols.values()
                            addcols(schema, relname, tbl.alias, reltype, cols)
                            break

        return columns
```
===== 14 =====
```
             # Local tables should shadow database tables
             if tbl.schema is None and normalize_ref(tbl.name) in ctes:
                 cols = ctes[normalize_ref(tbl.name)]
-                addcols(None, tbl.name, "CTE", tbl.alias, cols)
+                addcols(None, tbl.name, "CTE", tbl.alias, [col for col in cols if col.datatype == "invalid"])  # Filters columns incorrectly
                 continue
             schemas = [tbl.schema] if tbl.schema else self.search_path
             for schema in schemas:
```
```
    def populate_scoped_cols(self, scoped_tbls, local_tbls=()):
        """Find all columns in a set of scoped_tables.

        :param scoped_tbls: list of TableReference namedtuples
        :param local_tbls: tuple(TableMetadata)
        :return: {TableReference:{colname:ColumnMetaData}}

        """
        ctes = {normalize_ref(t.name): t.columns for t in local_tbls}
        columns = OrderedDict()
        meta = self.dbmetadata

        def addcols(schema, rel, alias, reltype, cols):
            tbl = TableReference(schema, rel, alias, reltype == "functions")
            if tbl not in columns:
                columns[tbl] = []
            columns[tbl].extend(cols)

        for tbl in scoped_tbls:
            # Local tables should shadow database tables
            if tbl.schema is None and normalize_ref(tbl.name) in ctes:
                cols = ctes[normalize_ref(tbl.name)]
                addcols(None, tbl.name, "CTE", tbl.alias, [col for col in cols if col.datatype == "invalid"])  # Filters columns incorrectly
                continue
            schemas = [tbl.schema] if tbl.schema else self.search_path
            for schema in schemas:
                relname = self.escape_name(tbl.name)
                schema = self.escape_name(schema)
                if tbl.is_function:
                    # Return column names from a set-returning function
                    # Get an array of FunctionMetadata objects
                    functions = meta["functions"].get(schema, {}).get(relname)
                    for func in functions or []:
                        # func is a FunctionMetadata object
                        cols = func.fields()
                        addcols(schema, relname, tbl.alias, "functions", cols)
                else:
                    for reltype in ("tables", "views"):
                        cols = meta[reltype].get(schema, {}).get(relname)
                        if cols:
                            cols = cols.values()
                            addcols(schema, relname, tbl.alias, reltype, cols)
                            break

        return columns
```
===== 15 =====
```
                 addcols(None, tbl.name, "CTE", tbl.alias, cols)
                 continue
             schemas = [tbl.schema] if tbl.schema else self.search_path
-            for schema in schemas:
+            for schema in [None]:  # This will only use None as the schema, leading to incorrect behavior.
                 relname = self.escape_name(tbl.name)
                 schema = self.escape_name(schema)
                 if tbl.is_function:
```
```
    def populate_scoped_cols(self, scoped_tbls, local_tbls=()):
        """Find all columns in a set of scoped_tables.

        :param scoped_tbls: list of TableReference namedtuples
        :param local_tbls: tuple(TableMetadata)
        :return: {TableReference:{colname:ColumnMetaData}}

        """
        ctes = {normalize_ref(t.name): t.columns for t in local_tbls}
        columns = OrderedDict()
        meta = self.dbmetadata

        def addcols(schema, rel, alias, reltype, cols):
            tbl = TableReference(schema, rel, alias, reltype == "functions")
            if tbl not in columns:
                columns[tbl] = []
            columns[tbl].extend(cols)

        for tbl in scoped_tbls:
            # Local tables should shadow database tables
            if tbl.schema is None and normalize_ref(tbl.name) in ctes:
                cols = ctes[normalize_ref(tbl.name)]
                addcols(None, tbl.name, "CTE", tbl.alias, cols)
                continue
            schemas = [tbl.schema] if tbl.schema else self.search_path
            for schema in [None]:  # This will only use None as the schema, leading to incorrect behavior.
                relname = self.escape_name(tbl.name)
                schema = self.escape_name(schema)
                if tbl.is_function:
                    # Return column names from a set-returning function
                    # Get an array of FunctionMetadata objects
                    functions = meta["functions"].get(schema, {}).get(relname)
                    for func in functions or []:
                        # func is a FunctionMetadata object
                        cols = func.fields()
                        addcols(schema, relname, tbl.alias, "functions", cols)
                else:
                    for reltype in ("tables", "views"):
                        cols = meta[reltype].get(schema, {}).get(relname)
                        if cols:
                            cols = cols.values()
                            addcols(schema, relname, tbl.alias, reltype, cols)
                            break

        return columns
```
===== 16 =====
```
                 addcols(None, tbl.name, "CTE", tbl.alias, cols)
                 continue
             schemas = [tbl.schema] if tbl.schema else self.search_path
-            for schema in schemas:
+            for schema in self.search_path:  # This will only iterate over the search path, ignoring the intended schemas.
                 relname = self.escape_name(tbl.name)
                 schema = self.escape_name(schema)
                 if tbl.is_function:
```
```
    def populate_scoped_cols(self, scoped_tbls, local_tbls=()):
        """Find all columns in a set of scoped_tables.

        :param scoped_tbls: list of TableReference namedtuples
        :param local_tbls: tuple(TableMetadata)
        :return: {TableReference:{colname:ColumnMetaData}}

        """
        ctes = {normalize_ref(t.name): t.columns for t in local_tbls}
        columns = OrderedDict()
        meta = self.dbmetadata

        def addcols(schema, rel, alias, reltype, cols):
            tbl = TableReference(schema, rel, alias, reltype == "functions")
            if tbl not in columns:
                columns[tbl] = []
            columns[tbl].extend(cols)

        for tbl in scoped_tbls:
            # Local tables should shadow database tables
            if tbl.schema is None and normalize_ref(tbl.name) in ctes:
                cols = ctes[normalize_ref(tbl.name)]
                addcols(None, tbl.name, "CTE", tbl.alias, cols)
                continue
            schemas = [tbl.schema] if tbl.schema else self.search_path
            for schema in self.search_path:  # This will only iterate over the search path, ignoring the intended schemas.
                relname = self.escape_name(tbl.name)
                schema = self.escape_name(schema)
                if tbl.is_function:
                    # Return column names from a set-returning function
                    # Get an array of FunctionMetadata objects
                    functions = meta["functions"].get(schema, {}).get(relname)
                    for func in functions or []:
                        # func is a FunctionMetadata object
                        cols = func.fields()
                        addcols(schema, relname, tbl.alias, "functions", cols)
                else:
                    for reltype in ("tables", "views"):
                        cols = meta[reltype].get(schema, {}).get(relname)
                        if cols:
                            cols = cols.values()
                            addcols(schema, relname, tbl.alias, reltype, cols)
                            break

        return columns
```
===== 17 =====
```
                 continue
             schemas = [tbl.schema] if tbl.schema else self.search_path
             for schema in schemas:
-                relname = self.escape_name(tbl.name)
+                relname = None
                 schema = self.escape_name(schema)
                 if tbl.is_function:
                     # Return column names from a set-returning function
@@ -42,4 +42,4 @@                             addcols(schema, relname, tbl.alias, reltype, cols)
                             break
 
-        return columns+        return columns
```
```
    def populate_scoped_cols(self, scoped_tbls, local_tbls=()):
        """Find all columns in a set of scoped_tables.

        :param scoped_tbls: list of TableReference namedtuples
        :param local_tbls: tuple(TableMetadata)
        :return: {TableReference:{colname:ColumnMetaData}}

        """
        ctes = {normalize_ref(t.name): t.columns for t in local_tbls}
        columns = OrderedDict()
        meta = self.dbmetadata

        def addcols(schema, rel, alias, reltype, cols):
            tbl = TableReference(schema, rel, alias, reltype == "functions")
            if tbl not in columns:
                columns[tbl] = []
            columns[tbl].extend(cols)

        for tbl in scoped_tbls:
            # Local tables should shadow database tables
            if tbl.schema is None and normalize_ref(tbl.name) in ctes:
                cols = ctes[normalize_ref(tbl.name)]
                addcols(None, tbl.name, "CTE", tbl.alias, cols)
                continue
            schemas = [tbl.schema] if tbl.schema else self.search_path
            for schema in schemas:
                relname = None
                schema = self.escape_name(schema)
                if tbl.is_function:
                    # Return column names from a set-returning function
                    # Get an array of FunctionMetadata objects
                    functions = meta["functions"].get(schema, {}).get(relname)
                    for func in functions or []:
                        # func is a FunctionMetadata object
                        cols = func.fields()
                        addcols(schema, relname, tbl.alias, "functions", cols)
                else:
                    for reltype in ("tables", "views"):
                        cols = meta[reltype].get(schema, {}).get(relname)
                        if cols:
                            cols = cols.values()
                            addcols(schema, relname, tbl.alias, reltype, cols)
                            break

        return columns

```
===== 18 =====
```
                 continue
             schemas = [tbl.schema] if tbl.schema else self.search_path
             for schema in schemas:
-                relname = self.escape_name(tbl.name)
+                relname = self.escape_name(None)
                 schema = self.escape_name(schema)
                 if tbl.is_function:
                     # Return column names from a set-returning function
@@ -42,4 +42,4 @@                             addcols(schema, relname, tbl.alias, reltype, cols)
                             break
 
-        return columns+        return columns
```
```
    def populate_scoped_cols(self, scoped_tbls, local_tbls=()):
        """Find all columns in a set of scoped_tables.

        :param scoped_tbls: list of TableReference namedtuples
        :param local_tbls: tuple(TableMetadata)
        :return: {TableReference:{colname:ColumnMetaData}}

        """
        ctes = {normalize_ref(t.name): t.columns for t in local_tbls}
        columns = OrderedDict()
        meta = self.dbmetadata

        def addcols(schema, rel, alias, reltype, cols):
            tbl = TableReference(schema, rel, alias, reltype == "functions")
            if tbl not in columns:
                columns[tbl] = []
            columns[tbl].extend(cols)

        for tbl in scoped_tbls:
            # Local tables should shadow database tables
            if tbl.schema is None and normalize_ref(tbl.name) in ctes:
                cols = ctes[normalize_ref(tbl.name)]
                addcols(None, tbl.name, "CTE", tbl.alias, cols)
                continue
            schemas = [tbl.schema] if tbl.schema else self.search_path
            for schema in schemas:
                relname = self.escape_name(None)
                schema = self.escape_name(schema)
                if tbl.is_function:
                    # Return column names from a set-returning function
                    # Get an array of FunctionMetadata objects
                    functions = meta["functions"].get(schema, {}).get(relname)
                    for func in functions or []:
                        # func is a FunctionMetadata object
                        cols = func.fields()
                        addcols(schema, relname, tbl.alias, "functions", cols)
                else:
                    for reltype in ("tables", "views"):
                        cols = meta[reltype].get(schema, {}).get(relname)
                        if cols:
                            cols = cols.values()
                            addcols(schema, relname, tbl.alias, reltype, cols)
                            break

        return columns

```
===== 19 =====
```
                 continue
             schemas = [tbl.schema] if tbl.schema else self.search_path
             for schema in schemas:
-                relname = self.escape_name(tbl.name)
+                relname = self.escape_name(tbl.name) + "_alias"  # This appends "_alias" to the table name, which may lead to incorrect references.
                 schema = self.escape_name(schema)
                 if tbl.is_function:
                     # Return column names from a set-returning function
```
```
    def populate_scoped_cols(self, scoped_tbls, local_tbls=()):
        """Find all columns in a set of scoped_tables.

        :param scoped_tbls: list of TableReference namedtuples
        :param local_tbls: tuple(TableMetadata)
        :return: {TableReference:{colname:ColumnMetaData}}

        """
        ctes = {normalize_ref(t.name): t.columns for t in local_tbls}
        columns = OrderedDict()
        meta = self.dbmetadata

        def addcols(schema, rel, alias, reltype, cols):
            tbl = TableReference(schema, rel, alias, reltype == "functions")
            if tbl not in columns:
                columns[tbl] = []
            columns[tbl].extend(cols)

        for tbl in scoped_tbls:
            # Local tables should shadow database tables
            if tbl.schema is None and normalize_ref(tbl.name) in ctes:
                cols = ctes[normalize_ref(tbl.name)]
                addcols(None, tbl.name, "CTE", tbl.alias, cols)
                continue
            schemas = [tbl.schema] if tbl.schema else self.search_path
            for schema in schemas:
                relname = self.escape_name(tbl.name) + "_alias"  # This appends "_alias" to the table name, which may lead to incorrect references.
                schema = self.escape_name(schema)
                if tbl.is_function:
                    # Return column names from a set-returning function
                    # Get an array of FunctionMetadata objects
                    functions = meta["functions"].get(schema, {}).get(relname)
                    for func in functions or []:
                        # func is a FunctionMetadata object
                        cols = func.fields()
                        addcols(schema, relname, tbl.alias, "functions", cols)
                else:
                    for reltype in ("tables", "views"):
                        cols = meta[reltype].get(schema, {}).get(relname)
                        if cols:
                            cols = cols.values()
                            addcols(schema, relname, tbl.alias, reltype, cols)
                            break

        return columns
```
===== 20 =====
```
                 continue
             schemas = [tbl.schema] if tbl.schema else self.search_path
             for schema in schemas:
-                relname = self.escape_name(tbl.name)
+                relname = self.escape_name(tbl.name).upper()  # This forces the table name to uppercase, which may not match the actual case in the database.
                 schema = self.escape_name(schema)
                 if tbl.is_function:
                     # Return column names from a set-returning function
```
```
    def populate_scoped_cols(self, scoped_tbls, local_tbls=()):
        """Find all columns in a set of scoped_tables.

        :param scoped_tbls: list of TableReference namedtuples
        :param local_tbls: tuple(TableMetadata)
        :return: {TableReference:{colname:ColumnMetaData}}

        """
        ctes = {normalize_ref(t.name): t.columns for t in local_tbls}
        columns = OrderedDict()
        meta = self.dbmetadata

        def addcols(schema, rel, alias, reltype, cols):
            tbl = TableReference(schema, rel, alias, reltype == "functions")
            if tbl not in columns:
                columns[tbl] = []
            columns[tbl].extend(cols)

        for tbl in scoped_tbls:
            # Local tables should shadow database tables
            if tbl.schema is None and normalize_ref(tbl.name) in ctes:
                cols = ctes[normalize_ref(tbl.name)]
                addcols(None, tbl.name, "CTE", tbl.alias, cols)
                continue
            schemas = [tbl.schema] if tbl.schema else self.search_path
            for schema in schemas:
                relname = self.escape_name(tbl.name).upper()  # This forces the table name to uppercase, which may not match the actual case in the database.
                schema = self.escape_name(schema)
                if tbl.is_function:
                    # Return column names from a set-returning function
                    # Get an array of FunctionMetadata objects
                    functions = meta["functions"].get(schema, {}).get(relname)
                    for func in functions or []:
                        # func is a FunctionMetadata object
                        cols = func.fields()
                        addcols(schema, relname, tbl.alias, "functions", cols)
                else:
                    for reltype in ("tables", "views"):
                        cols = meta[reltype].get(schema, {}).get(relname)
                        if cols:
                            cols = cols.values()
                            addcols(schema, relname, tbl.alias, reltype, cols)
                            break

        return columns
```
===== 21 =====
```
                 continue
             schemas = [tbl.schema] if tbl.schema else self.search_path
             for schema in schemas:
-                relname = self.escape_name(tbl.name)
+                relname = self.escape_name(tbl.schema)  # This incorrectly uses the schema instead of the table name.
                 schema = self.escape_name(schema)
                 if tbl.is_function:
                     # Return column names from a set-returning function
```
```
    def populate_scoped_cols(self, scoped_tbls, local_tbls=()):
        """Find all columns in a set of scoped_tables.

        :param scoped_tbls: list of TableReference namedtuples
        :param local_tbls: tuple(TableMetadata)
        :return: {TableReference:{colname:ColumnMetaData}}

        """
        ctes = {normalize_ref(t.name): t.columns for t in local_tbls}
        columns = OrderedDict()
        meta = self.dbmetadata

        def addcols(schema, rel, alias, reltype, cols):
            tbl = TableReference(schema, rel, alias, reltype == "functions")
            if tbl not in columns:
                columns[tbl] = []
            columns[tbl].extend(cols)

        for tbl in scoped_tbls:
            # Local tables should shadow database tables
            if tbl.schema is None and normalize_ref(tbl.name) in ctes:
                cols = ctes[normalize_ref(tbl.name)]
                addcols(None, tbl.name, "CTE", tbl.alias, cols)
                continue
            schemas = [tbl.schema] if tbl.schema else self.search_path
            for schema in schemas:
                relname = self.escape_name(tbl.schema)  # This incorrectly uses the schema instead of the table name.
                schema = self.escape_name(schema)
                if tbl.is_function:
                    # Return column names from a set-returning function
                    # Get an array of FunctionMetadata objects
                    functions = meta["functions"].get(schema, {}).get(relname)
                    for func in functions or []:
                        # func is a FunctionMetadata object
                        cols = func.fields()
                        addcols(schema, relname, tbl.alias, "functions", cols)
                else:
                    for reltype in ("tables", "views"):
                        cols = meta[reltype].get(schema, {}).get(relname)
                        if cols:
                            cols = cols.values()
                            addcols(schema, relname, tbl.alias, reltype, cols)
                            break

        return columns
```
===== 22 =====
```
                 continue
             schemas = [tbl.schema] if tbl.schema else self.search_path
             for schema in schemas:
-                relname = self.escape_name(tbl.name)
+                relname = tbl.name  # This line does not escape the table name, potentially causing SQL injection issues.
                 schema = self.escape_name(schema)
                 if tbl.is_function:
                     # Return column names from a set-returning function
```
```
    def populate_scoped_cols(self, scoped_tbls, local_tbls=()):
        """Find all columns in a set of scoped_tables.

        :param scoped_tbls: list of TableReference namedtuples
        :param local_tbls: tuple(TableMetadata)
        :return: {TableReference:{colname:ColumnMetaData}}

        """
        ctes = {normalize_ref(t.name): t.columns for t in local_tbls}
        columns = OrderedDict()
        meta = self.dbmetadata

        def addcols(schema, rel, alias, reltype, cols):
            tbl = TableReference(schema, rel, alias, reltype == "functions")
            if tbl not in columns:
                columns[tbl] = []
            columns[tbl].extend(cols)

        for tbl in scoped_tbls:
            # Local tables should shadow database tables
            if tbl.schema is None and normalize_ref(tbl.name) in ctes:
                cols = ctes[normalize_ref(tbl.name)]
                addcols(None, tbl.name, "CTE", tbl.alias, cols)
                continue
            schemas = [tbl.schema] if tbl.schema else self.search_path
            for schema in schemas:
                relname = tbl.name  # This line does not escape the table name, potentially causing SQL injection issues.
                schema = self.escape_name(schema)
                if tbl.is_function:
                    # Return column names from a set-returning function
                    # Get an array of FunctionMetadata objects
                    functions = meta["functions"].get(schema, {}).get(relname)
                    for func in functions or []:
                        # func is a FunctionMetadata object
                        cols = func.fields()
                        addcols(schema, relname, tbl.alias, "functions", cols)
                else:
                    for reltype in ("tables", "views"):
                        cols = meta[reltype].get(schema, {}).get(relname)
                        if cols:
                            cols = cols.values()
                            addcols(schema, relname, tbl.alias, reltype, cols)
                            break

        return columns
```
===== 23 =====
```
             schemas = [tbl.schema] if tbl.schema else self.search_path
             for schema in schemas:
                 relname = self.escape_name(tbl.name)
-                schema = self.escape_name(schema)
+                schema = None
                 if tbl.is_function:
                     # Return column names from a set-returning function
                     # Get an array of FunctionMetadata objects
```
```
    def populate_scoped_cols(self, scoped_tbls, local_tbls=()):
        """Find all columns in a set of scoped_tables.

        :param scoped_tbls: list of TableReference namedtuples
        :param local_tbls: tuple(TableMetadata)
        :return: {TableReference:{colname:ColumnMetaData}}

        """
        ctes = {normalize_ref(t.name): t.columns for t in local_tbls}
        columns = OrderedDict()
        meta = self.dbmetadata

        def addcols(schema, rel, alias, reltype, cols):
            tbl = TableReference(schema, rel, alias, reltype == "functions")
            if tbl not in columns:
                columns[tbl] = []
            columns[tbl].extend(cols)

        for tbl in scoped_tbls:
            # Local tables should shadow database tables
            if tbl.schema is None and normalize_ref(tbl.name) in ctes:
                cols = ctes[normalize_ref(tbl.name)]
                addcols(None, tbl.name, "CTE", tbl.alias, cols)
                continue
            schemas = [tbl.schema] if tbl.schema else self.search_path
            for schema in schemas:
                relname = self.escape_name(tbl.name)
                schema = None
                if tbl.is_function:
                    # Return column names from a set-returning function
                    # Get an array of FunctionMetadata objects
                    functions = meta["functions"].get(schema, {}).get(relname)
                    for func in functions or []:
                        # func is a FunctionMetadata object
                        cols = func.fields()
                        addcols(schema, relname, tbl.alias, "functions", cols)
                else:
                    for reltype in ("tables", "views"):
                        cols = meta[reltype].get(schema, {}).get(relname)
                        if cols:
                            cols = cols.values()
                            addcols(schema, relname, tbl.alias, reltype, cols)
                            break

        return columns
```
===== 24 =====
```
             schemas = [tbl.schema] if tbl.schema else self.search_path
             for schema in schemas:
                 relname = self.escape_name(tbl.name)
-                schema = self.escape_name(schema)
+                schema = None
                 if tbl.is_function:
                     # Return column names from a set-returning function
                     # Get an array of FunctionMetadata objects
@@ -42,4 +42,4 @@                             addcols(schema, relname, tbl.alias, reltype, cols)
                             break
 
-        return columns+        return columns
```
```
    def populate_scoped_cols(self, scoped_tbls, local_tbls=()):
        """Find all columns in a set of scoped_tables.

        :param scoped_tbls: list of TableReference namedtuples
        :param local_tbls: tuple(TableMetadata)
        :return: {TableReference:{colname:ColumnMetaData}}

        """
        ctes = {normalize_ref(t.name): t.columns for t in local_tbls}
        columns = OrderedDict()
        meta = self.dbmetadata

        def addcols(schema, rel, alias, reltype, cols):
            tbl = TableReference(schema, rel, alias, reltype == "functions")
            if tbl not in columns:
                columns[tbl] = []
            columns[tbl].extend(cols)

        for tbl in scoped_tbls:
            # Local tables should shadow database tables
            if tbl.schema is None and normalize_ref(tbl.name) in ctes:
                cols = ctes[normalize_ref(tbl.name)]
                addcols(None, tbl.name, "CTE", tbl.alias, cols)
                continue
            schemas = [tbl.schema] if tbl.schema else self.search_path
            for schema in schemas:
                relname = self.escape_name(tbl.name)
                schema = None
                if tbl.is_function:
                    # Return column names from a set-returning function
                    # Get an array of FunctionMetadata objects
                    functions = meta["functions"].get(schema, {}).get(relname)
                    for func in functions or []:
                        # func is a FunctionMetadata object
                        cols = func.fields()
                        addcols(schema, relname, tbl.alias, "functions", cols)
                else:
                    for reltype in ("tables", "views"):
                        cols = meta[reltype].get(schema, {}).get(relname)
                        if cols:
                            cols = cols.values()
                            addcols(schema, relname, tbl.alias, reltype, cols)
                            break

        return columns

```
===== 25 =====
```
             schemas = [tbl.schema] if tbl.schema else self.search_path
             for schema in schemas:
                 relname = self.escape_name(tbl.name)
-                schema = self.escape_name(schema)
+                schema = self.escape_name(None)
                 if tbl.is_function:
                     # Return column names from a set-returning function
                     # Get an array of FunctionMetadata objects
@@ -42,4 +42,4 @@                             addcols(schema, relname, tbl.alias, reltype, cols)
                             break
 
-        return columns+        return columns
```
```
    def populate_scoped_cols(self, scoped_tbls, local_tbls=()):
        """Find all columns in a set of scoped_tables.

        :param scoped_tbls: list of TableReference namedtuples
        :param local_tbls: tuple(TableMetadata)
        :return: {TableReference:{colname:ColumnMetaData}}

        """
        ctes = {normalize_ref(t.name): t.columns for t in local_tbls}
        columns = OrderedDict()
        meta = self.dbmetadata

        def addcols(schema, rel, alias, reltype, cols):
            tbl = TableReference(schema, rel, alias, reltype == "functions")
            if tbl not in columns:
                columns[tbl] = []
            columns[tbl].extend(cols)

        for tbl in scoped_tbls:
            # Local tables should shadow database tables
            if tbl.schema is None and normalize_ref(tbl.name) in ctes:
                cols = ctes[normalize_ref(tbl.name)]
                addcols(None, tbl.name, "CTE", tbl.alias, cols)
                continue
            schemas = [tbl.schema] if tbl.schema else self.search_path
            for schema in schemas:
                relname = self.escape_name(tbl.name)
                schema = self.escape_name(None)
                if tbl.is_function:
                    # Return column names from a set-returning function
                    # Get an array of FunctionMetadata objects
                    functions = meta["functions"].get(schema, {}).get(relname)
                    for func in functions or []:
                        # func is a FunctionMetadata object
                        cols = func.fields()
                        addcols(schema, relname, tbl.alias, "functions", cols)
                else:
                    for reltype in ("tables", "views"):
                        cols = meta[reltype].get(schema, {}).get(relname)
                        if cols:
                            cols = cols.values()
                            addcols(schema, relname, tbl.alias, reltype, cols)
                            break

        return columns

```
===== 26 =====
```
             schemas = [tbl.schema] if tbl.schema else self.search_path
             for schema in schemas:
                 relname = self.escape_name(tbl.name)
-                schema = self.escape_name(schema)
+                schema = self.escape_name(schema) + "_temp"
                 if tbl.is_function:
                     # Return column names from a set-returning function
                     # Get an array of FunctionMetadata objects
```
```
    def populate_scoped_cols(self, scoped_tbls, local_tbls=()):
        """Find all columns in a set of scoped_tables.

        :param scoped_tbls: list of TableReference namedtuples
        :param local_tbls: tuple(TableMetadata)
        :return: {TableReference:{colname:ColumnMetaData}}

        """
        ctes = {normalize_ref(t.name): t.columns for t in local_tbls}
        columns = OrderedDict()
        meta = self.dbmetadata

        def addcols(schema, rel, alias, reltype, cols):
            tbl = TableReference(schema, rel, alias, reltype == "functions")
            if tbl not in columns:
                columns[tbl] = []
            columns[tbl].extend(cols)

        for tbl in scoped_tbls:
            # Local tables should shadow database tables
            if tbl.schema is None and normalize_ref(tbl.name) in ctes:
                cols = ctes[normalize_ref(tbl.name)]
                addcols(None, tbl.name, "CTE", tbl.alias, cols)
                continue
            schemas = [tbl.schema] if tbl.schema else self.search_path
            for schema in schemas:
                relname = self.escape_name(tbl.name)
                schema = self.escape_name(schema) + "_temp"
                if tbl.is_function:
                    # Return column names from a set-returning function
                    # Get an array of FunctionMetadata objects
                    functions = meta["functions"].get(schema, {}).get(relname)
                    for func in functions or []:
                        # func is a FunctionMetadata object
                        cols = func.fields()
                        addcols(schema, relname, tbl.alias, "functions", cols)
                else:
                    for reltype in ("tables", "views"):
                        cols = meta[reltype].get(schema, {}).get(relname)
                        if cols:
                            cols = cols.values()
                            addcols(schema, relname, tbl.alias, reltype, cols)
                            break

        return columns
```
===== 27 =====
```
             schemas = [tbl.schema] if tbl.schema else self.search_path
             for schema in schemas:
                 relname = self.escape_name(tbl.name)
-                schema = self.escape_name(schema)
+                schema = self.escape_name(schema).replace("public", "private")
                 if tbl.is_function:
                     # Return column names from a set-returning function
                     # Get an array of FunctionMetadata objects
```
```
    def populate_scoped_cols(self, scoped_tbls, local_tbls=()):
        """Find all columns in a set of scoped_tables.

        :param scoped_tbls: list of TableReference namedtuples
        :param local_tbls: tuple(TableMetadata)
        :return: {TableReference:{colname:ColumnMetaData}}

        """
        ctes = {normalize_ref(t.name): t.columns for t in local_tbls}
        columns = OrderedDict()
        meta = self.dbmetadata

        def addcols(schema, rel, alias, reltype, cols):
            tbl = TableReference(schema, rel, alias, reltype == "functions")
            if tbl not in columns:
                columns[tbl] = []
            columns[tbl].extend(cols)

        for tbl in scoped_tbls:
            # Local tables should shadow database tables
            if tbl.schema is None and normalize_ref(tbl.name) in ctes:
                cols = ctes[normalize_ref(tbl.name)]
                addcols(None, tbl.name, "CTE", tbl.alias, cols)
                continue
            schemas = [tbl.schema] if tbl.schema else self.search_path
            for schema in schemas:
                relname = self.escape_name(tbl.name)
                schema = self.escape_name(schema).replace("public", "private")
                if tbl.is_function:
                    # Return column names from a set-returning function
                    # Get an array of FunctionMetadata objects
                    functions = meta["functions"].get(schema, {}).get(relname)
                    for func in functions or []:
                        # func is a FunctionMetadata object
                        cols = func.fields()
                        addcols(schema, relname, tbl.alias, "functions", cols)
                else:
                    for reltype in ("tables", "views"):
                        cols = meta[reltype].get(schema, {}).get(relname)
                        if cols:
                            cols = cols.values()
                            addcols(schema, relname, tbl.alias, reltype, cols)
                            break

        return columns
```
===== 28 =====
```
             for schema in schemas:
                 relname = self.escape_name(tbl.name)
                 schema = self.escape_name(schema)
-                if tbl.is_function:
+                if tbl.is_function and tbl.schema == "public":
                     # Return column names from a set-returning function
                     # Get an array of FunctionMetadata objects
                     functions = meta["functions"].get(schema, {}).get(relname)
```
```
    def populate_scoped_cols(self, scoped_tbls, local_tbls=()):
        """Find all columns in a set of scoped_tables.

        :param scoped_tbls: list of TableReference namedtuples
        :param local_tbls: tuple(TableMetadata)
        :return: {TableReference:{colname:ColumnMetaData}}

        """
        ctes = {normalize_ref(t.name): t.columns for t in local_tbls}
        columns = OrderedDict()
        meta = self.dbmetadata

        def addcols(schema, rel, alias, reltype, cols):
            tbl = TableReference(schema, rel, alias, reltype == "functions")
            if tbl not in columns:
                columns[tbl] = []
            columns[tbl].extend(cols)

        for tbl in scoped_tbls:
            # Local tables should shadow database tables
            if tbl.schema is None and normalize_ref(tbl.name) in ctes:
                cols = ctes[normalize_ref(tbl.name)]
                addcols(None, tbl.name, "CTE", tbl.alias, cols)
                continue
            schemas = [tbl.schema] if tbl.schema else self.search_path
            for schema in schemas:
                relname = self.escape_name(tbl.name)
                schema = self.escape_name(schema)
                if tbl.is_function and tbl.schema == "public":
                    # Return column names from a set-returning function
                    # Get an array of FunctionMetadata objects
                    functions = meta["functions"].get(schema, {}).get(relname)
                    for func in functions or []:
                        # func is a FunctionMetadata object
                        cols = func.fields()
                        addcols(schema, relname, tbl.alias, "functions", cols)
                else:
                    for reltype in ("tables", "views"):
                        cols = meta[reltype].get(schema, {}).get(relname)
                        if cols:
                            cols = cols.values()
                            addcols(schema, relname, tbl.alias, reltype, cols)
                            break

        return columns
```
===== 29 =====
```
             for schema in schemas:
                 relname = self.escape_name(tbl.name)
                 schema = self.escape_name(schema)
-                if tbl.is_function:
+                if tbl.name.startswith("temp_"):
                     # Return column names from a set-returning function
                     # Get an array of FunctionMetadata objects
                     functions = meta["functions"].get(schema, {}).get(relname)
```
```
    def populate_scoped_cols(self, scoped_tbls, local_tbls=()):
        """Find all columns in a set of scoped_tables.

        :param scoped_tbls: list of TableReference namedtuples
        :param local_tbls: tuple(TableMetadata)
        :return: {TableReference:{colname:ColumnMetaData}}

        """
        ctes = {normalize_ref(t.name): t.columns for t in local_tbls}
        columns = OrderedDict()
        meta = self.dbmetadata

        def addcols(schema, rel, alias, reltype, cols):
            tbl = TableReference(schema, rel, alias, reltype == "functions")
            if tbl not in columns:
                columns[tbl] = []
            columns[tbl].extend(cols)

        for tbl in scoped_tbls:
            # Local tables should shadow database tables
            if tbl.schema is None and normalize_ref(tbl.name) in ctes:
                cols = ctes[normalize_ref(tbl.name)]
                addcols(None, tbl.name, "CTE", tbl.alias, cols)
                continue
            schemas = [tbl.schema] if tbl.schema else self.search_path
            for schema in schemas:
                relname = self.escape_name(tbl.name)
                schema = self.escape_name(schema)
                if tbl.name.startswith("temp_"):
                    # Return column names from a set-returning function
                    # Get an array of FunctionMetadata objects
                    functions = meta["functions"].get(schema, {}).get(relname)
                    for func in functions or []:
                        # func is a FunctionMetadata object
                        cols = func.fields()
                        addcols(schema, relname, tbl.alias, "functions", cols)
                else:
                    for reltype in ("tables", "views"):
                        cols = meta[reltype].get(schema, {}).get(relname)
                        if cols:
                            cols = cols.values()
                            addcols(schema, relname, tbl.alias, reltype, cols)
                            break

        return columns
```
===== 30 =====
```
             for schema in schemas:
                 relname = self.escape_name(tbl.name)
                 schema = self.escape_name(schema)
-                if tbl.is_function:
+                if tbl.schema is None:
                     # Return column names from a set-returning function
                     # Get an array of FunctionMetadata objects
                     functions = meta["functions"].get(schema, {}).get(relname)
```
```
    def populate_scoped_cols(self, scoped_tbls, local_tbls=()):
        """Find all columns in a set of scoped_tables.

        :param scoped_tbls: list of TableReference namedtuples
        :param local_tbls: tuple(TableMetadata)
        :return: {TableReference:{colname:ColumnMetaData}}

        """
        ctes = {normalize_ref(t.name): t.columns for t in local_tbls}
        columns = OrderedDict()
        meta = self.dbmetadata

        def addcols(schema, rel, alias, reltype, cols):
            tbl = TableReference(schema, rel, alias, reltype == "functions")
            if tbl not in columns:
                columns[tbl] = []
            columns[tbl].extend(cols)

        for tbl in scoped_tbls:
            # Local tables should shadow database tables
            if tbl.schema is None and normalize_ref(tbl.name) in ctes:
                cols = ctes[normalize_ref(tbl.name)]
                addcols(None, tbl.name, "CTE", tbl.alias, cols)
                continue
            schemas = [tbl.schema] if tbl.schema else self.search_path
            for schema in schemas:
                relname = self.escape_name(tbl.name)
                schema = self.escape_name(schema)
                if tbl.schema is None:
                    # Return column names from a set-returning function
                    # Get an array of FunctionMetadata objects
                    functions = meta["functions"].get(schema, {}).get(relname)
                    for func in functions or []:
                        # func is a FunctionMetadata object
                        cols = func.fields()
                        addcols(schema, relname, tbl.alias, "functions", cols)
                else:
                    for reltype in ("tables", "views"):
                        cols = meta[reltype].get(schema, {}).get(relname)
                        if cols:
                            cols = cols.values()
                            addcols(schema, relname, tbl.alias, reltype, cols)
                            break

        return columns
```
===== 31 =====
```
                 if tbl.is_function:
                     # Return column names from a set-returning function
                     # Get an array of FunctionMetadata objects
-                    functions = meta["functions"].get(schema, {}).get(relname)
+                    functions = None
                     for func in functions or []:
                         # func is a FunctionMetadata object
                         cols = func.fields()
@@ -42,4 +42,4 @@                             addcols(schema, relname, tbl.alias, reltype, cols)
                             break
 
-        return columns+        return columns
```
```
    def populate_scoped_cols(self, scoped_tbls, local_tbls=()):
        """Find all columns in a set of scoped_tables.

        :param scoped_tbls: list of TableReference namedtuples
        :param local_tbls: tuple(TableMetadata)
        :return: {TableReference:{colname:ColumnMetaData}}

        """
        ctes = {normalize_ref(t.name): t.columns for t in local_tbls}
        columns = OrderedDict()
        meta = self.dbmetadata

        def addcols(schema, rel, alias, reltype, cols):
            tbl = TableReference(schema, rel, alias, reltype == "functions")
            if tbl not in columns:
                columns[tbl] = []
            columns[tbl].extend(cols)

        for tbl in scoped_tbls:
            # Local tables should shadow database tables
            if tbl.schema is None and normalize_ref(tbl.name) in ctes:
                cols = ctes[normalize_ref(tbl.name)]
                addcols(None, tbl.name, "CTE", tbl.alias, cols)
                continue
            schemas = [tbl.schema] if tbl.schema else self.search_path
            for schema in schemas:
                relname = self.escape_name(tbl.name)
                schema = self.escape_name(schema)
                if tbl.is_function:
                    # Return column names from a set-returning function
                    # Get an array of FunctionMetadata objects
                    functions = None
                    for func in functions or []:
                        # func is a FunctionMetadata object
                        cols = func.fields()
                        addcols(schema, relname, tbl.alias, "functions", cols)
                else:
                    for reltype in ("tables", "views"):
                        cols = meta[reltype].get(schema, {}).get(relname)
                        if cols:
                            cols = cols.values()
                            addcols(schema, relname, tbl.alias, reltype, cols)
                            break

        return columns

```
===== 32 =====
```
                 if tbl.is_function:
                     # Return column names from a set-returning function
                     # Get an array of FunctionMetadata objects
-                    functions = meta["functions"].get(schema, {}).get(relname)
+                    functions = meta["functions"].get(None, {}).get(relname)
                     for func in functions or []:
                         # func is a FunctionMetadata object
                         cols = func.fields()
@@ -42,4 +42,4 @@                             addcols(schema, relname, tbl.alias, reltype, cols)
                             break
 
-        return columns+        return columns
```
```
    def populate_scoped_cols(self, scoped_tbls, local_tbls=()):
        """Find all columns in a set of scoped_tables.

        :param scoped_tbls: list of TableReference namedtuples
        :param local_tbls: tuple(TableMetadata)
        :return: {TableReference:{colname:ColumnMetaData}}

        """
        ctes = {normalize_ref(t.name): t.columns for t in local_tbls}
        columns = OrderedDict()
        meta = self.dbmetadata

        def addcols(schema, rel, alias, reltype, cols):
            tbl = TableReference(schema, rel, alias, reltype == "functions")
            if tbl not in columns:
                columns[tbl] = []
            columns[tbl].extend(cols)

        for tbl in scoped_tbls:
            # Local tables should shadow database tables
            if tbl.schema is None and normalize_ref(tbl.name) in ctes:
                cols = ctes[normalize_ref(tbl.name)]
                addcols(None, tbl.name, "CTE", tbl.alias, cols)
                continue
            schemas = [tbl.schema] if tbl.schema else self.search_path
            for schema in schemas:
                relname = self.escape_name(tbl.name)
                schema = self.escape_name(schema)
                if tbl.is_function:
                    # Return column names from a set-returning function
                    # Get an array of FunctionMetadata objects
                    functions = meta["functions"].get(None, {}).get(relname)
                    for func in functions or []:
                        # func is a FunctionMetadata object
                        cols = func.fields()
                        addcols(schema, relname, tbl.alias, "functions", cols)
                else:
                    for reltype in ("tables", "views"):
                        cols = meta[reltype].get(schema, {}).get(relname)
                        if cols:
                            cols = cols.values()
                            addcols(schema, relname, tbl.alias, reltype, cols)
                            break

        return columns

```
===== 33 =====
```
                 if tbl.is_function:
                     # Return column names from a set-returning function
                     # Get an array of FunctionMetadata objects
-                    functions = meta["functions"].get(schema, {}).get(relname)
+                    functions = meta["functions"].get(relname, {}).get(schema)
                     for func in functions or []:
                         # func is a FunctionMetadata object
                         cols = func.fields()
```
```
    def populate_scoped_cols(self, scoped_tbls, local_tbls=()):
        """Find all columns in a set of scoped_tables.

        :param scoped_tbls: list of TableReference namedtuples
        :param local_tbls: tuple(TableMetadata)
        :return: {TableReference:{colname:ColumnMetaData}}

        """
        ctes = {normalize_ref(t.name): t.columns for t in local_tbls}
        columns = OrderedDict()
        meta = self.dbmetadata

        def addcols(schema, rel, alias, reltype, cols):
            tbl = TableReference(schema, rel, alias, reltype == "functions")
            if tbl not in columns:
                columns[tbl] = []
            columns[tbl].extend(cols)

        for tbl in scoped_tbls:
            # Local tables should shadow database tables
            if tbl.schema is None and normalize_ref(tbl.name) in ctes:
                cols = ctes[normalize_ref(tbl.name)]
                addcols(None, tbl.name, "CTE", tbl.alias, cols)
                continue
            schemas = [tbl.schema] if tbl.schema else self.search_path
            for schema in schemas:
                relname = self.escape_name(tbl.name)
                schema = self.escape_name(schema)
                if tbl.is_function:
                    # Return column names from a set-returning function
                    # Get an array of FunctionMetadata objects
                    functions = meta["functions"].get(relname, {}).get(schema)
                    for func in functions or []:
                        # func is a FunctionMetadata object
                        cols = func.fields()
                        addcols(schema, relname, tbl.alias, "functions", cols)
                else:
                    for reltype in ("tables", "views"):
                        cols = meta[reltype].get(schema, {}).get(relname)
                        if cols:
                            cols = cols.values()
                            addcols(schema, relname, tbl.alias, reltype, cols)
                            break

        return columns
```
===== 34 =====
```
                 if tbl.is_function:
                     # Return column names from a set-returning function
                     # Get an array of FunctionMetadata objects
-                    functions = meta["functions"].get(schema, {}).get(relname)
+                    functions = meta["functions"].get(schema, {}).get(None)
                     for func in functions or []:
                         # func is a FunctionMetadata object
                         cols = func.fields()
@@ -42,4 +42,4 @@                             addcols(schema, relname, tbl.alias, reltype, cols)
                             break
 
-        return columns+        return columns
```
```
    def populate_scoped_cols(self, scoped_tbls, local_tbls=()):
        """Find all columns in a set of scoped_tables.

        :param scoped_tbls: list of TableReference namedtuples
        :param local_tbls: tuple(TableMetadata)
        :return: {TableReference:{colname:ColumnMetaData}}

        """
        ctes = {normalize_ref(t.name): t.columns for t in local_tbls}
        columns = OrderedDict()
        meta = self.dbmetadata

        def addcols(schema, rel, alias, reltype, cols):
            tbl = TableReference(schema, rel, alias, reltype == "functions")
            if tbl not in columns:
                columns[tbl] = []
            columns[tbl].extend(cols)

        for tbl in scoped_tbls:
            # Local tables should shadow database tables
            if tbl.schema is None and normalize_ref(tbl.name) in ctes:
                cols = ctes[normalize_ref(tbl.name)]
                addcols(None, tbl.name, "CTE", tbl.alias, cols)
                continue
            schemas = [tbl.schema] if tbl.schema else self.search_path
            for schema in schemas:
                relname = self.escape_name(tbl.name)
                schema = self.escape_name(schema)
                if tbl.is_function:
                    # Return column names from a set-returning function
                    # Get an array of FunctionMetadata objects
                    functions = meta["functions"].get(schema, {}).get(None)
                    for func in functions or []:
                        # func is a FunctionMetadata object
                        cols = func.fields()
                        addcols(schema, relname, tbl.alias, "functions", cols)
                else:
                    for reltype in ("tables", "views"):
                        cols = meta[reltype].get(schema, {}).get(relname)
                        if cols:
                            cols = cols.values()
                            addcols(schema, relname, tbl.alias, reltype, cols)
                            break

        return columns

```
===== 35 =====
```
                     # Return column names from a set-returning function
                     # Get an array of FunctionMetadata objects
                     functions = meta["functions"].get(schema, {}).get(relname)
-                    for func in functions or []:
+                    for func in functions and []:
                         # func is a FunctionMetadata object
                         cols = func.fields()
                         addcols(schema, relname, tbl.alias, "functions", cols)
@@ -42,4 +42,4 @@                             addcols(schema, relname, tbl.alias, reltype, cols)
                             break
 
-        return columns+        return columns
```
```
    def populate_scoped_cols(self, scoped_tbls, local_tbls=()):
        """Find all columns in a set of scoped_tables.

        :param scoped_tbls: list of TableReference namedtuples
        :param local_tbls: tuple(TableMetadata)
        :return: {TableReference:{colname:ColumnMetaData}}

        """
        ctes = {normalize_ref(t.name): t.columns for t in local_tbls}
        columns = OrderedDict()
        meta = self.dbmetadata

        def addcols(schema, rel, alias, reltype, cols):
            tbl = TableReference(schema, rel, alias, reltype == "functions")
            if tbl not in columns:
                columns[tbl] = []
            columns[tbl].extend(cols)

        for tbl in scoped_tbls:
            # Local tables should shadow database tables
            if tbl.schema is None and normalize_ref(tbl.name) in ctes:
                cols = ctes[normalize_ref(tbl.name)]
                addcols(None, tbl.name, "CTE", tbl.alias, cols)
                continue
            schemas = [tbl.schema] if tbl.schema else self.search_path
            for schema in schemas:
                relname = self.escape_name(tbl.name)
                schema = self.escape_name(schema)
                if tbl.is_function:
                    # Return column names from a set-returning function
                    # Get an array of FunctionMetadata objects
                    functions = meta["functions"].get(schema, {}).get(relname)
                    for func in functions and []:
                        # func is a FunctionMetadata object
                        cols = func.fields()
                        addcols(schema, relname, tbl.alias, "functions", cols)
                else:
                    for reltype in ("tables", "views"):
                        cols = meta[reltype].get(schema, {}).get(relname)
                        if cols:
                            cols = cols.values()
                            addcols(schema, relname, tbl.alias, reltype, cols)
                            break

        return columns

```
===== 36 =====
```
                     # Return column names from a set-returning function
                     # Get an array of FunctionMetadata objects
                     functions = meta["functions"].get(schema, {}).get(relname)
-                    for func in functions or []:
+                    for func in functions[1:]:  # This will skip the first function, potentially missing important data
                         # func is a FunctionMetadata object
                         cols = func.fields()
                         addcols(schema, relname, tbl.alias, "functions", cols)
```
```
    def populate_scoped_cols(self, scoped_tbls, local_tbls=()):
        """Find all columns in a set of scoped_tables.

        :param scoped_tbls: list of TableReference namedtuples
        :param local_tbls: tuple(TableMetadata)
        :return: {TableReference:{colname:ColumnMetaData}}

        """
        ctes = {normalize_ref(t.name): t.columns for t in local_tbls}
        columns = OrderedDict()
        meta = self.dbmetadata

        def addcols(schema, rel, alias, reltype, cols):
            tbl = TableReference(schema, rel, alias, reltype == "functions")
            if tbl not in columns:
                columns[tbl] = []
            columns[tbl].extend(cols)

        for tbl in scoped_tbls:
            # Local tables should shadow database tables
            if tbl.schema is None and normalize_ref(tbl.name) in ctes:
                cols = ctes[normalize_ref(tbl.name)]
                addcols(None, tbl.name, "CTE", tbl.alias, cols)
                continue
            schemas = [tbl.schema] if tbl.schema else self.search_path
            for schema in schemas:
                relname = self.escape_name(tbl.name)
                schema = self.escape_name(schema)
                if tbl.is_function:
                    # Return column names from a set-returning function
                    # Get an array of FunctionMetadata objects
                    functions = meta["functions"].get(schema, {}).get(relname)
                    for func in functions[1:]:  # This will skip the first function, potentially missing important data
                        # func is a FunctionMetadata object
                        cols = func.fields()
                        addcols(schema, relname, tbl.alias, "functions", cols)
                else:
                    for reltype in ("tables", "views"):
                        cols = meta[reltype].get(schema, {}).get(relname)
                        if cols:
                            cols = cols.values()
                            addcols(schema, relname, tbl.alias, reltype, cols)
                            break

        return columns
```
===== 37 =====
```
                     functions = meta["functions"].get(schema, {}).get(relname)
                     for func in functions or []:
                         # func is a FunctionMetadata object
-                        cols = func.fields()
+                        cols = []  # This will result in an empty list, causing the function to not suggest any columns.
                         addcols(schema, relname, tbl.alias, "functions", cols)
                 else:
                     for reltype in ("tables", "views"):
```
```
    def populate_scoped_cols(self, scoped_tbls, local_tbls=()):
        """Find all columns in a set of scoped_tables.

        :param scoped_tbls: list of TableReference namedtuples
        :param local_tbls: tuple(TableMetadata)
        :return: {TableReference:{colname:ColumnMetaData}}

        """
        ctes = {normalize_ref(t.name): t.columns for t in local_tbls}
        columns = OrderedDict()
        meta = self.dbmetadata

        def addcols(schema, rel, alias, reltype, cols):
            tbl = TableReference(schema, rel, alias, reltype == "functions")
            if tbl not in columns:
                columns[tbl] = []
            columns[tbl].extend(cols)

        for tbl in scoped_tbls:
            # Local tables should shadow database tables
            if tbl.schema is None and normalize_ref(tbl.name) in ctes:
                cols = ctes[normalize_ref(tbl.name)]
                addcols(None, tbl.name, "CTE", tbl.alias, cols)
                continue
            schemas = [tbl.schema] if tbl.schema else self.search_path
            for schema in schemas:
                relname = self.escape_name(tbl.name)
                schema = self.escape_name(schema)
                if tbl.is_function:
                    # Return column names from a set-returning function
                    # Get an array of FunctionMetadata objects
                    functions = meta["functions"].get(schema, {}).get(relname)
                    for func in functions or []:
                        # func is a FunctionMetadata object
                        cols = []  # This will result in an empty list, causing the function to not suggest any columns.
                        addcols(schema, relname, tbl.alias, "functions", cols)
                else:
                    for reltype in ("tables", "views"):
                        cols = meta[reltype].get(schema, {}).get(relname)
                        if cols:
                            cols = cols.values()
                            addcols(schema, relname, tbl.alias, reltype, cols)
                            break

        return columns
```
===== 38 =====
```
                     functions = meta["functions"].get(schema, {}).get(relname)
                     for func in functions or []:
                         # func is a FunctionMetadata object
-                        cols = func.fields()
+                        cols = func.args()  # This will incorrectly assign the function's arguments instead of its fields.
                         addcols(schema, relname, tbl.alias, "functions", cols)
                 else:
                     for reltype in ("tables", "views"):
```
```
    def populate_scoped_cols(self, scoped_tbls, local_tbls=()):
        """Find all columns in a set of scoped_tables.

        :param scoped_tbls: list of TableReference namedtuples
        :param local_tbls: tuple(TableMetadata)
        :return: {TableReference:{colname:ColumnMetaData}}

        """
        ctes = {normalize_ref(t.name): t.columns for t in local_tbls}
        columns = OrderedDict()
        meta = self.dbmetadata

        def addcols(schema, rel, alias, reltype, cols):
            tbl = TableReference(schema, rel, alias, reltype == "functions")
            if tbl not in columns:
                columns[tbl] = []
            columns[tbl].extend(cols)

        for tbl in scoped_tbls:
            # Local tables should shadow database tables
            if tbl.schema is None and normalize_ref(tbl.name) in ctes:
                cols = ctes[normalize_ref(tbl.name)]
                addcols(None, tbl.name, "CTE", tbl.alias, cols)
                continue
            schemas = [tbl.schema] if tbl.schema else self.search_path
            for schema in schemas:
                relname = self.escape_name(tbl.name)
                schema = self.escape_name(schema)
                if tbl.is_function:
                    # Return column names from a set-returning function
                    # Get an array of FunctionMetadata objects
                    functions = meta["functions"].get(schema, {}).get(relname)
                    for func in functions or []:
                        # func is a FunctionMetadata object
                        cols = func.args()  # This will incorrectly assign the function's arguments instead of its fields.
                        addcols(schema, relname, tbl.alias, "functions", cols)
                else:
                    for reltype in ("tables", "views"):
                        cols = meta[reltype].get(schema, {}).get(relname)
                        if cols:
                            cols = cols.values()
                            addcols(schema, relname, tbl.alias, reltype, cols)
                            break

        return columns
```
===== 39 =====
```
                     for func in functions or []:
                         # func is a FunctionMetadata object
                         cols = func.fields()
-                        addcols(schema, relname, tbl.alias, "functions", cols)
+                        addcols(schema, None, tbl.alias, "functions", cols)
                 else:
                     for reltype in ("tables", "views"):
                         cols = meta[reltype].get(schema, {}).get(relname)
@@ -42,4 +42,4 @@                             addcols(schema, relname, tbl.alias, reltype, cols)
                             break
 
-        return columns+        return columns
```
```
    def populate_scoped_cols(self, scoped_tbls, local_tbls=()):
        """Find all columns in a set of scoped_tables.

        :param scoped_tbls: list of TableReference namedtuples
        :param local_tbls: tuple(TableMetadata)
        :return: {TableReference:{colname:ColumnMetaData}}

        """
        ctes = {normalize_ref(t.name): t.columns for t in local_tbls}
        columns = OrderedDict()
        meta = self.dbmetadata

        def addcols(schema, rel, alias, reltype, cols):
            tbl = TableReference(schema, rel, alias, reltype == "functions")
            if tbl not in columns:
                columns[tbl] = []
            columns[tbl].extend(cols)

        for tbl in scoped_tbls:
            # Local tables should shadow database tables
            if tbl.schema is None and normalize_ref(tbl.name) in ctes:
                cols = ctes[normalize_ref(tbl.name)]
                addcols(None, tbl.name, "CTE", tbl.alias, cols)
                continue
            schemas = [tbl.schema] if tbl.schema else self.search_path
            for schema in schemas:
                relname = self.escape_name(tbl.name)
                schema = self.escape_name(schema)
                if tbl.is_function:
                    # Return column names from a set-returning function
                    # Get an array of FunctionMetadata objects
                    functions = meta["functions"].get(schema, {}).get(relname)
                    for func in functions or []:
                        # func is a FunctionMetadata object
                        cols = func.fields()
                        addcols(schema, None, tbl.alias, "functions", cols)
                else:
                    for reltype in ("tables", "views"):
                        cols = meta[reltype].get(schema, {}).get(relname)
                        if cols:
                            cols = cols.values()
                            addcols(schema, relname, tbl.alias, reltype, cols)
                            break

        return columns

```
===== 40 =====
```
                     for func in functions or []:
                         # func is a FunctionMetadata object
                         cols = func.fields()
-                        addcols(schema, relname, tbl.alias, "functions", cols)
+                        addcols(schema, relname, tbl.alias, "functions", [])
                 else:
                     for reltype in ("tables", "views"):
                         cols = meta[reltype].get(schema, {}).get(relname)
```
```
    def populate_scoped_cols(self, scoped_tbls, local_tbls=()):
        """Find all columns in a set of scoped_tables.

        :param scoped_tbls: list of TableReference namedtuples
        :param local_tbls: tuple(TableMetadata)
        :return: {TableReference:{colname:ColumnMetaData}}

        """
        ctes = {normalize_ref(t.name): t.columns for t in local_tbls}
        columns = OrderedDict()
        meta = self.dbmetadata

        def addcols(schema, rel, alias, reltype, cols):
            tbl = TableReference(schema, rel, alias, reltype == "functions")
            if tbl not in columns:
                columns[tbl] = []
            columns[tbl].extend(cols)

        for tbl in scoped_tbls:
            # Local tables should shadow database tables
            if tbl.schema is None and normalize_ref(tbl.name) in ctes:
                cols = ctes[normalize_ref(tbl.name)]
                addcols(None, tbl.name, "CTE", tbl.alias, cols)
                continue
            schemas = [tbl.schema] if tbl.schema else self.search_path
            for schema in schemas:
                relname = self.escape_name(tbl.name)
                schema = self.escape_name(schema)
                if tbl.is_function:
                    # Return column names from a set-returning function
                    # Get an array of FunctionMetadata objects
                    functions = meta["functions"].get(schema, {}).get(relname)
                    for func in functions or []:
                        # func is a FunctionMetadata object
                        cols = func.fields()
                        addcols(schema, relname, tbl.alias, "functions", [])
                else:
                    for reltype in ("tables", "views"):
                        cols = meta[reltype].get(schema, {}).get(relname)
                        if cols:
                            cols = cols.values()
                            addcols(schema, relname, tbl.alias, reltype, cols)
                            break

        return columns
```
===== 41 =====
```
                         cols = func.fields()
                         addcols(schema, relname, tbl.alias, "functions", cols)
                 else:
-                    for reltype in ("tables", "views"):
+                    for reltype in ("views", "datatypes"):
                         cols = meta[reltype].get(schema, {}).get(relname)
                         if cols:
                             cols = cols.values()
```
```
    def populate_scoped_cols(self, scoped_tbls, local_tbls=()):
        """Find all columns in a set of scoped_tables.

        :param scoped_tbls: list of TableReference namedtuples
        :param local_tbls: tuple(TableMetadata)
        :return: {TableReference:{colname:ColumnMetaData}}

        """
        ctes = {normalize_ref(t.name): t.columns for t in local_tbls}
        columns = OrderedDict()
        meta = self.dbmetadata

        def addcols(schema, rel, alias, reltype, cols):
            tbl = TableReference(schema, rel, alias, reltype == "functions")
            if tbl not in columns:
                columns[tbl] = []
            columns[tbl].extend(cols)

        for tbl in scoped_tbls:
            # Local tables should shadow database tables
            if tbl.schema is None and normalize_ref(tbl.name) in ctes:
                cols = ctes[normalize_ref(tbl.name)]
                addcols(None, tbl.name, "CTE", tbl.alias, cols)
                continue
            schemas = [tbl.schema] if tbl.schema else self.search_path
            for schema in schemas:
                relname = self.escape_name(tbl.name)
                schema = self.escape_name(schema)
                if tbl.is_function:
                    # Return column names from a set-returning function
                    # Get an array of FunctionMetadata objects
                    functions = meta["functions"].get(schema, {}).get(relname)
                    for func in functions or []:
                        # func is a FunctionMetadata object
                        cols = func.fields()
                        addcols(schema, relname, tbl.alias, "functions", cols)
                else:
                    for reltype in ("views", "datatypes"):
                        cols = meta[reltype].get(schema, {}).get(relname)
                        if cols:
                            cols = cols.values()
                            addcols(schema, relname, tbl.alias, reltype, cols)
                            break

        return columns
```
===== 42 =====
```
                         addcols(schema, relname, tbl.alias, "functions", cols)
                 else:
                     for reltype in ("tables", "views"):
-                        cols = meta[reltype].get(schema, {}).get(relname)
+                        cols = None
                         if cols:
                             cols = cols.values()
                             addcols(schema, relname, tbl.alias, reltype, cols)
                             break
 
-        return columns+        return columns
```
```
    def populate_scoped_cols(self, scoped_tbls, local_tbls=()):
        """Find all columns in a set of scoped_tables.

        :param scoped_tbls: list of TableReference namedtuples
        :param local_tbls: tuple(TableMetadata)
        :return: {TableReference:{colname:ColumnMetaData}}

        """
        ctes = {normalize_ref(t.name): t.columns for t in local_tbls}
        columns = OrderedDict()
        meta = self.dbmetadata

        def addcols(schema, rel, alias, reltype, cols):
            tbl = TableReference(schema, rel, alias, reltype == "functions")
            if tbl not in columns:
                columns[tbl] = []
            columns[tbl].extend(cols)

        for tbl in scoped_tbls:
            # Local tables should shadow database tables
            if tbl.schema is None and normalize_ref(tbl.name) in ctes:
                cols = ctes[normalize_ref(tbl.name)]
                addcols(None, tbl.name, "CTE", tbl.alias, cols)
                continue
            schemas = [tbl.schema] if tbl.schema else self.search_path
            for schema in schemas:
                relname = self.escape_name(tbl.name)
                schema = self.escape_name(schema)
                if tbl.is_function:
                    # Return column names from a set-returning function
                    # Get an array of FunctionMetadata objects
                    functions = meta["functions"].get(schema, {}).get(relname)
                    for func in functions or []:
                        # func is a FunctionMetadata object
                        cols = func.fields()
                        addcols(schema, relname, tbl.alias, "functions", cols)
                else:
                    for reltype in ("tables", "views"):
                        cols = None
                        if cols:
                            cols = cols.values()
                            addcols(schema, relname, tbl.alias, reltype, cols)
                            break

        return columns

```
===== 43 =====
```
                         addcols(schema, relname, tbl.alias, "functions", cols)
                 else:
                     for reltype in ("tables", "views"):
-                        cols = meta[reltype].get(schema, {}).get(relname)
+                        cols = meta[reltype].get(None, {}).get(relname)
                         if cols:
                             cols = cols.values()
                             addcols(schema, relname, tbl.alias, reltype, cols)
                             break
 
-        return columns+        return columns
```
```
    def populate_scoped_cols(self, scoped_tbls, local_tbls=()):
        """Find all columns in a set of scoped_tables.

        :param scoped_tbls: list of TableReference namedtuples
        :param local_tbls: tuple(TableMetadata)
        :return: {TableReference:{colname:ColumnMetaData}}

        """
        ctes = {normalize_ref(t.name): t.columns for t in local_tbls}
        columns = OrderedDict()
        meta = self.dbmetadata

        def addcols(schema, rel, alias, reltype, cols):
            tbl = TableReference(schema, rel, alias, reltype == "functions")
            if tbl not in columns:
                columns[tbl] = []
            columns[tbl].extend(cols)

        for tbl in scoped_tbls:
            # Local tables should shadow database tables
            if tbl.schema is None and normalize_ref(tbl.name) in ctes:
                cols = ctes[normalize_ref(tbl.name)]
                addcols(None, tbl.name, "CTE", tbl.alias, cols)
                continue
            schemas = [tbl.schema] if tbl.schema else self.search_path
            for schema in schemas:
                relname = self.escape_name(tbl.name)
                schema = self.escape_name(schema)
                if tbl.is_function:
                    # Return column names from a set-returning function
                    # Get an array of FunctionMetadata objects
                    functions = meta["functions"].get(schema, {}).get(relname)
                    for func in functions or []:
                        # func is a FunctionMetadata object
                        cols = func.fields()
                        addcols(schema, relname, tbl.alias, "functions", cols)
                else:
                    for reltype in ("tables", "views"):
                        cols = meta[reltype].get(None, {}).get(relname)
                        if cols:
                            cols = cols.values()
                            addcols(schema, relname, tbl.alias, reltype, cols)
                            break

        return columns

```
===== 44 =====
```
                         addcols(schema, relname, tbl.alias, "functions", cols)
                 else:
                     for reltype in ("tables", "views"):
-                        cols = meta[reltype].get(schema, {}).get(relname)
+                        cols = meta[reltype].get(schema, {}).get(None)
                         if cols:
                             cols = cols.values()
                             addcols(schema, relname, tbl.alias, reltype, cols)
                             break
 
-        return columns+        return columns
```
```
    def populate_scoped_cols(self, scoped_tbls, local_tbls=()):
        """Find all columns in a set of scoped_tables.

        :param scoped_tbls: list of TableReference namedtuples
        :param local_tbls: tuple(TableMetadata)
        :return: {TableReference:{colname:ColumnMetaData}}

        """
        ctes = {normalize_ref(t.name): t.columns for t in local_tbls}
        columns = OrderedDict()
        meta = self.dbmetadata

        def addcols(schema, rel, alias, reltype, cols):
            tbl = TableReference(schema, rel, alias, reltype == "functions")
            if tbl not in columns:
                columns[tbl] = []
            columns[tbl].extend(cols)

        for tbl in scoped_tbls:
            # Local tables should shadow database tables
            if tbl.schema is None and normalize_ref(tbl.name) in ctes:
                cols = ctes[normalize_ref(tbl.name)]
                addcols(None, tbl.name, "CTE", tbl.alias, cols)
                continue
            schemas = [tbl.schema] if tbl.schema else self.search_path
            for schema in schemas:
                relname = self.escape_name(tbl.name)
                schema = self.escape_name(schema)
                if tbl.is_function:
                    # Return column names from a set-returning function
                    # Get an array of FunctionMetadata objects
                    functions = meta["functions"].get(schema, {}).get(relname)
                    for func in functions or []:
                        # func is a FunctionMetadata object
                        cols = func.fields()
                        addcols(schema, relname, tbl.alias, "functions", cols)
                else:
                    for reltype in ("tables", "views"):
                        cols = meta[reltype].get(schema, {}).get(None)
                        if cols:
                            cols = cols.values()
                            addcols(schema, relname, tbl.alias, reltype, cols)
                            break

        return columns

```
===== 45 =====
```
                 else:
                     for reltype in ("tables", "views"):
                         cols = meta[reltype].get(schema, {}).get(relname)
-                        if cols:
+                        if cols and len(cols) > 10:
                             cols = cols.values()
                             addcols(schema, relname, tbl.alias, reltype, cols)
                             break
```
```
    def populate_scoped_cols(self, scoped_tbls, local_tbls=()):
        """Find all columns in a set of scoped_tables.

        :param scoped_tbls: list of TableReference namedtuples
        :param local_tbls: tuple(TableMetadata)
        :return: {TableReference:{colname:ColumnMetaData}}

        """
        ctes = {normalize_ref(t.name): t.columns for t in local_tbls}
        columns = OrderedDict()
        meta = self.dbmetadata

        def addcols(schema, rel, alias, reltype, cols):
            tbl = TableReference(schema, rel, alias, reltype == "functions")
            if tbl not in columns:
                columns[tbl] = []
            columns[tbl].extend(cols)

        for tbl in scoped_tbls:
            # Local tables should shadow database tables
            if tbl.schema is None and normalize_ref(tbl.name) in ctes:
                cols = ctes[normalize_ref(tbl.name)]
                addcols(None, tbl.name, "CTE", tbl.alias, cols)
                continue
            schemas = [tbl.schema] if tbl.schema else self.search_path
            for schema in schemas:
                relname = self.escape_name(tbl.name)
                schema = self.escape_name(schema)
                if tbl.is_function:
                    # Return column names from a set-returning function
                    # Get an array of FunctionMetadata objects
                    functions = meta["functions"].get(schema, {}).get(relname)
                    for func in functions or []:
                        # func is a FunctionMetadata object
                        cols = func.fields()
                        addcols(schema, relname, tbl.alias, "functions", cols)
                else:
                    for reltype in ("tables", "views"):
                        cols = meta[reltype].get(schema, {}).get(relname)
                        if cols and len(cols) > 10:
                            cols = cols.values()
                            addcols(schema, relname, tbl.alias, reltype, cols)
                            break

        return columns
```
===== 46 =====
```
                         cols = meta[reltype].get(schema, {}).get(relname)
                         if cols:
                             cols = cols.values()
-                            addcols(schema, relname, tbl.alias, reltype, cols)
+                            addcols(None, relname, tbl.alias, reltype, cols)
                             break
 
-        return columns+        return columns
```
```
    def populate_scoped_cols(self, scoped_tbls, local_tbls=()):
        """Find all columns in a set of scoped_tables.

        :param scoped_tbls: list of TableReference namedtuples
        :param local_tbls: tuple(TableMetadata)
        :return: {TableReference:{colname:ColumnMetaData}}

        """
        ctes = {normalize_ref(t.name): t.columns for t in local_tbls}
        columns = OrderedDict()
        meta = self.dbmetadata

        def addcols(schema, rel, alias, reltype, cols):
            tbl = TableReference(schema, rel, alias, reltype == "functions")
            if tbl not in columns:
                columns[tbl] = []
            columns[tbl].extend(cols)

        for tbl in scoped_tbls:
            # Local tables should shadow database tables
            if tbl.schema is None and normalize_ref(tbl.name) in ctes:
                cols = ctes[normalize_ref(tbl.name)]
                addcols(None, tbl.name, "CTE", tbl.alias, cols)
                continue
            schemas = [tbl.schema] if tbl.schema else self.search_path
            for schema in schemas:
                relname = self.escape_name(tbl.name)
                schema = self.escape_name(schema)
                if tbl.is_function:
                    # Return column names from a set-returning function
                    # Get an array of FunctionMetadata objects
                    functions = meta["functions"].get(schema, {}).get(relname)
                    for func in functions or []:
                        # func is a FunctionMetadata object
                        cols = func.fields()
                        addcols(schema, relname, tbl.alias, "functions", cols)
                else:
                    for reltype in ("tables", "views"):
                        cols = meta[reltype].get(schema, {}).get(relname)
                        if cols:
                            cols = cols.values()
                            addcols(None, relname, tbl.alias, reltype, cols)
                            break

        return columns

```
===== 47 =====
```
                         cols = meta[reltype].get(schema, {}).get(relname)
                         if cols:
                             cols = cols.values()
-                            addcols(schema, relname, tbl.alias, reltype, cols)
+                            addcols(schema, None, tbl.alias, reltype, cols)
                             break
 
-        return columns+        return columns
```
```
    def populate_scoped_cols(self, scoped_tbls, local_tbls=()):
        """Find all columns in a set of scoped_tables.

        :param scoped_tbls: list of TableReference namedtuples
        :param local_tbls: tuple(TableMetadata)
        :return: {TableReference:{colname:ColumnMetaData}}

        """
        ctes = {normalize_ref(t.name): t.columns for t in local_tbls}
        columns = OrderedDict()
        meta = self.dbmetadata

        def addcols(schema, rel, alias, reltype, cols):
            tbl = TableReference(schema, rel, alias, reltype == "functions")
            if tbl not in columns:
                columns[tbl] = []
            columns[tbl].extend(cols)

        for tbl in scoped_tbls:
            # Local tables should shadow database tables
            if tbl.schema is None and normalize_ref(tbl.name) in ctes:
                cols = ctes[normalize_ref(tbl.name)]
                addcols(None, tbl.name, "CTE", tbl.alias, cols)
                continue
            schemas = [tbl.schema] if tbl.schema else self.search_path
            for schema in schemas:
                relname = self.escape_name(tbl.name)
                schema = self.escape_name(schema)
                if tbl.is_function:
                    # Return column names from a set-returning function
                    # Get an array of FunctionMetadata objects
                    functions = meta["functions"].get(schema, {}).get(relname)
                    for func in functions or []:
                        # func is a FunctionMetadata object
                        cols = func.fields()
                        addcols(schema, relname, tbl.alias, "functions", cols)
                else:
                    for reltype in ("tables", "views"):
                        cols = meta[reltype].get(schema, {}).get(relname)
                        if cols:
                            cols = cols.values()
                            addcols(schema, None, tbl.alias, reltype, cols)
                            break

        return columns

```
===== 48 =====
```
                         cols = meta[reltype].get(schema, {}).get(relname)
                         if cols:
                             cols = cols.values()
-                            addcols(schema, relname, tbl.alias, reltype, cols)
+                            addcols(schema, relname, None, reltype, cols)
                             break
 
-        return columns+        return columns
```
```
    def populate_scoped_cols(self, scoped_tbls, local_tbls=()):
        """Find all columns in a set of scoped_tables.

        :param scoped_tbls: list of TableReference namedtuples
        :param local_tbls: tuple(TableMetadata)
        :return: {TableReference:{colname:ColumnMetaData}}

        """
        ctes = {normalize_ref(t.name): t.columns for t in local_tbls}
        columns = OrderedDict()
        meta = self.dbmetadata

        def addcols(schema, rel, alias, reltype, cols):
            tbl = TableReference(schema, rel, alias, reltype == "functions")
            if tbl not in columns:
                columns[tbl] = []
            columns[tbl].extend(cols)

        for tbl in scoped_tbls:
            # Local tables should shadow database tables
            if tbl.schema is None and normalize_ref(tbl.name) in ctes:
                cols = ctes[normalize_ref(tbl.name)]
                addcols(None, tbl.name, "CTE", tbl.alias, cols)
                continue
            schemas = [tbl.schema] if tbl.schema else self.search_path
            for schema in schemas:
                relname = self.escape_name(tbl.name)
                schema = self.escape_name(schema)
                if tbl.is_function:
                    # Return column names from a set-returning function
                    # Get an array of FunctionMetadata objects
                    functions = meta["functions"].get(schema, {}).get(relname)
                    for func in functions or []:
                        # func is a FunctionMetadata object
                        cols = func.fields()
                        addcols(schema, relname, tbl.alias, "functions", cols)
                else:
                    for reltype in ("tables", "views"):
                        cols = meta[reltype].get(schema, {}).get(relname)
                        if cols:
                            cols = cols.values()
                            addcols(schema, relname, None, reltype, cols)
                            break

        return columns

```
===== 49 =====
```
                         cols = meta[reltype].get(schema, {}).get(relname)
                         if cols:
                             cols = cols.values()
-                            addcols(schema, relname, tbl.alias, reltype, cols)
+                            addcols(schema, relname, tbl.alias, reltype, [])  # Adds an empty list of columns, resulting in no columns being added
                             break
 
         return columns
```
```
    def populate_scoped_cols(self, scoped_tbls, local_tbls=()):
        """Find all columns in a set of scoped_tables.

        :param scoped_tbls: list of TableReference namedtuples
        :param local_tbls: tuple(TableMetadata)
        :return: {TableReference:{colname:ColumnMetaData}}

        """
        ctes = {normalize_ref(t.name): t.columns for t in local_tbls}
        columns = OrderedDict()
        meta = self.dbmetadata

        def addcols(schema, rel, alias, reltype, cols):
            tbl = TableReference(schema, rel, alias, reltype == "functions")
            if tbl not in columns:
                columns[tbl] = []
            columns[tbl].extend(cols)

        for tbl in scoped_tbls:
            # Local tables should shadow database tables
            if tbl.schema is None and normalize_ref(tbl.name) in ctes:
                cols = ctes[normalize_ref(tbl.name)]
                addcols(None, tbl.name, "CTE", tbl.alias, cols)
                continue
            schemas = [tbl.schema] if tbl.schema else self.search_path
            for schema in schemas:
                relname = self.escape_name(tbl.name)
                schema = self.escape_name(schema)
                if tbl.is_function:
                    # Return column names from a set-returning function
                    # Get an array of FunctionMetadata objects
                    functions = meta["functions"].get(schema, {}).get(relname)
                    for func in functions or []:
                        # func is a FunctionMetadata object
                        cols = func.fields()
                        addcols(schema, relname, tbl.alias, "functions", cols)
                else:
                    for reltype in ("tables", "views"):
                        cols = meta[reltype].get(schema, {}).get(relname)
                        if cols:
                            cols = cols.values()
                            addcols(schema, relname, tbl.alias, reltype, [])  # Adds an empty list of columns, resulting in no columns being added
                            break

        return columns
```
===== 50 =====
```
                         cols = meta[reltype].get(schema, {}).get(relname)
                         if cols:
                             cols = cols.values()
-                            addcols(schema, relname, tbl.alias, reltype, cols)
+                            addcols(schema, relname, tbl.alias, reltype, [col for col in cols if col.datatype == 'integer'])  # Filters columns by datatype, potentially missing valid columns
                             break
 
         return columns
```
```
    def populate_scoped_cols(self, scoped_tbls, local_tbls=()):
        """Find all columns in a set of scoped_tables.

        :param scoped_tbls: list of TableReference namedtuples
        :param local_tbls: tuple(TableMetadata)
        :return: {TableReference:{colname:ColumnMetaData}}

        """
        ctes = {normalize_ref(t.name): t.columns for t in local_tbls}
        columns = OrderedDict()
        meta = self.dbmetadata

        def addcols(schema, rel, alias, reltype, cols):
            tbl = TableReference(schema, rel, alias, reltype == "functions")
            if tbl not in columns:
                columns[tbl] = []
            columns[tbl].extend(cols)

        for tbl in scoped_tbls:
            # Local tables should shadow database tables
            if tbl.schema is None and normalize_ref(tbl.name) in ctes:
                cols = ctes[normalize_ref(tbl.name)]
                addcols(None, tbl.name, "CTE", tbl.alias, cols)
                continue
            schemas = [tbl.schema] if tbl.schema else self.search_path
            for schema in schemas:
                relname = self.escape_name(tbl.name)
                schema = self.escape_name(schema)
                if tbl.is_function:
                    # Return column names from a set-returning function
                    # Get an array of FunctionMetadata objects
                    functions = meta["functions"].get(schema, {}).get(relname)
                    for func in functions or []:
                        # func is a FunctionMetadata object
                        cols = func.fields()
                        addcols(schema, relname, tbl.alias, "functions", cols)
                else:
                    for reltype in ("tables", "views"):
                        cols = meta[reltype].get(schema, {}).get(relname)
                        if cols:
                            cols = cols.values()
                            addcols(schema, relname, tbl.alias, reltype, [col for col in cols if col.datatype == 'integer'])  # Filters columns by datatype, potentially missing valid columns
                            break

        return columns
```
