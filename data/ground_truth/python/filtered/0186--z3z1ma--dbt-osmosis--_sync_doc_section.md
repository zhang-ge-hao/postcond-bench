https://github.com/z3z1ma/dbt-osmosis/blob/cd453ea69e9473e45df5390d8bb2a41e201dd4ee/./src/dbt_osmosis/core/sync_operations.py#L17-L77
```
🈚️

It's hard

@icontract.snapshot(
    lambda context, node, doc_section: bool(doc_section.get("description")),
    name="had_description",
)
@icontract.snapshot(
    lambda context, node, doc_section: doc_section.get("description"),
    name="orig_description",
)
@icontract.snapshot(
    lambda context, node, doc_section: doc_section.get("columns", None),
    name="orig_columns",
)
@icontract.ensure(
    lambda context, node, doc_section:
        isinstance(doc_section.get("columns"), list),
    "doc_section['columns'] must be a list."
)
@icontract.ensure(
    lambda context, node, doc_section:
        len(doc_section.get("columns", [])) == len(getattr(node, "columns", {})),
    "There must be exactly one YAML column per node.columns entry."
)
@icontract.ensure(
    lambda context, node, doc_section:
        all(
            # 每个 node.columns 的列名，在 YAML 里要么原样存在，要么存在小写版本
            any(
                col.get("name") == name or col.get("name") == name.lower()
                for col in doc_section.get("columns", [])
            )
            for name in getattr(node, "columns", {}).keys()
        ),
    "Every column from node.columns must appear in doc_section['columns'] "
    "(by name or its lowercase form).",
)
@icontract.ensure(
    lambda context, node, doc_section:
        all(
            isinstance(col, dict)
            and "name" in col
            and bool(col["name"])
            for col in doc_section.get("columns", [])
        ),
    "Each column entry must be a dict with a non-empty 'name'.",
)
@icontract.ensure(
    lambda context, node, doc_section:
        all(
            # description 如果存在，就不能是 None
            ("description" not in col or col["description"] is not None)
            # tags 如果存在，就必须是非空 list
            and ("tags" not in col or (isinstance(col["tags"], list) and len(col["tags"]) > 0))
            # meta 如果存在，就必须是非空 mapping
            and ("meta" not in col or bool(col["meta"]))
            # 其他字段（除 name/description/tags/meta 外），不能是 None/[]/{}
            and all(
                col[k] not in (None, [], {})
                for k in set(col.keys()) - {"name", "description", "tags", "meta"}
            )
            for col in doc_section.get("columns", [])
        ),
    "Column metadata is cleaned: no empty/None values are left on known fields.",
)
@icontract.ensure(
    lambda OLD, context, node, doc_section:
        # 如果原来有 description（且为 truthy），就必须被保留
        (not OLD.had_description)
        or doc_section.get("description") == OLD.orig_description,
    "An existing non-empty description on doc_section must be preserved.",
)
@icontract.ensure(
    lambda OLD, context, node, doc_section:
        # 如果之前没有 description 且 node 有 description，则必须被复制过来
        (OLD.had_description or not node.description)
        or doc_section.get("description") == node.description,
    "If doc_section had no description and node has one, it must be copied to doc_section.",
)
@icontract.ensure(
    lambda OLD, context, node, doc_section:
        # 如果原来就有 columns list，那么现在必须换成一个新的 list（而不是就地修改）
        OLD.orig_columns is None
        or doc_section.get("columns") is not OLD.orig_columns,
    "doc_section['columns'] must be replaced (new list), not mutated in place.",
)
```
```
None
```
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25]
===== 0 =====
```
         current_map[norm_name] = c
 
     for name, meta in node.columns.items():
-        cdict = meta.to_dict(omit_none=True)
+        cdict = {k: v for k, v in meta.to_dict(omit_none=True).items() if k != "description"}  # This removes the description key entirely.
         cdict["name"] = name
         from dbt_osmosis.core.introspection import _get_setting_for_node, normalize_column_name
```
```
def _sync_doc_section(context: t.Any, node: ResultNode, doc_section: dict[str, t.Any]) -> None:
    """Helper function that overwrites 'doc_section' with data from 'node'.

    This includes columns, description, meta, tags, etc.
    We assume node is the single source of truth, so doc_section is replaced.
    """
    logger.debug(":arrows_counterclockwise: Syncing doc_section with node => %s", node.unique_id)
    if node.description and not doc_section.get("description"):
        doc_section["description"] = node.description

    current_columns: list[dict[str, t.Any]] = doc_section.setdefault("columns", [])
    incoming_columns: list[dict[str, t.Any]] = []

    current_map = {}
    for c in current_columns:
        from dbt_osmosis.core.introspection import normalize_column_name

        norm_name = normalize_column_name(c["name"], context.project.runtime_cfg.credentials.type)
        current_map[norm_name] = c

    for name, meta in node.columns.items():
        cdict = {k: v for k, v in meta.to_dict(omit_none=True).items() if k != "description"}  # This removes the description key entirely.
        cdict["name"] = name
        from dbt_osmosis.core.introspection import _get_setting_for_node, normalize_column_name

        norm_name = normalize_column_name(name, context.project.runtime_cfg.credentials.type)

        current_yaml = t.cast(dict[str, t.Any], current_map.get(norm_name, {}))
        merged = dict(current_yaml)

        skip_add_types = _get_setting_for_node(
            "skip-add-data-types", node, name, fallback=context.settings.skip_add_data_types
        )
        for k, v in cdict.items():
            if k == "data_type" and skip_add_types:
                # don't add data types if told not to
                continue
            if k == "constraints" and "constraints" in merged:
                # keep constraints as is if present, mashumaro dumps too much info :shrug:
                continue
            merged[k] = v

        if merged.get("description") is None:
            merged.pop("description", None)
        if merged.get("tags", []) == []:
            merged.pop("tags", None)
        if merged.get("meta", {}) == {}:
            merged.pop("meta", None)

        for k in set(merged.keys()) - {"name", "description", "tags", "meta"}:
            if merged[k] in (None, [], {}):
                merged.pop(k)

        if _get_setting_for_node(
            "output-to-lower", node, name, fallback=context.settings.output_to_lower
        ):
            merged["name"] = merged["name"].lower()

        incoming_columns.append(merged)

    doc_section["columns"] = incoming_columns
```
===== 1 =====
```
         current_map[norm_name] = c
 
     for name, meta in node.columns.items():
-        cdict = meta.to_dict(omit_none=True)
+        cdict = {}  # This initializes cdict as an empty dictionary, losing all metadata.
         cdict["name"] = name
         from dbt_osmosis.core.introspection import _get_setting_for_node, normalize_column_name
```
```
def _sync_doc_section(context: t.Any, node: ResultNode, doc_section: dict[str, t.Any]) -> None:
    """Helper function that overwrites 'doc_section' with data from 'node'.

    This includes columns, description, meta, tags, etc.
    We assume node is the single source of truth, so doc_section is replaced.
    """
    logger.debug(":arrows_counterclockwise: Syncing doc_section with node => %s", node.unique_id)
    if node.description and not doc_section.get("description"):
        doc_section["description"] = node.description

    current_columns: list[dict[str, t.Any]] = doc_section.setdefault("columns", [])
    incoming_columns: list[dict[str, t.Any]] = []

    current_map = {}
    for c in current_columns:
        from dbt_osmosis.core.introspection import normalize_column_name

        norm_name = normalize_column_name(c["name"], context.project.runtime_cfg.credentials.type)
        current_map[norm_name] = c

    for name, meta in node.columns.items():
        cdict = {}  # This initializes cdict as an empty dictionary, losing all metadata.
        cdict["name"] = name
        from dbt_osmosis.core.introspection import _get_setting_for_node, normalize_column_name

        norm_name = normalize_column_name(name, context.project.runtime_cfg.credentials.type)

        current_yaml = t.cast(dict[str, t.Any], current_map.get(norm_name, {}))
        merged = dict(current_yaml)

        skip_add_types = _get_setting_for_node(
            "skip-add-data-types", node, name, fallback=context.settings.skip_add_data_types
        )
        for k, v in cdict.items():
            if k == "data_type" and skip_add_types:
                # don't add data types if told not to
                continue
            if k == "constraints" and "constraints" in merged:
                # keep constraints as is if present, mashumaro dumps too much info :shrug:
                continue
            merged[k] = v

        if merged.get("description") is None:
            merged.pop("description", None)
        if merged.get("tags", []) == []:
            merged.pop("tags", None)
        if merged.get("meta", {}) == {}:
            merged.pop("meta", None)

        for k in set(merged.keys()) - {"name", "description", "tags", "meta"}:
            if merged[k] in (None, [], {}):
                merged.pop(k)

        if _get_setting_for_node(
            "output-to-lower", node, name, fallback=context.settings.output_to_lower
        ):
            merged["name"] = merged["name"].lower()

        incoming_columns.append(merged)

    doc_section["columns"] = incoming_columns
```
===== 2 =====
```
             "skip-add-data-types", node, name, fallback=context.settings.skip_add_data_types
         )
         for k, v in cdict.items():
-            if k == "data_type" and skip_add_types:
+            if k != "data_type" and skip_add_types:
                 # don't add data types if told not to
                 continue
             if k == "constraints" and "constraints" in merged:
```
```
def _sync_doc_section(context: t.Any, node: ResultNode, doc_section: dict[str, t.Any]) -> None:
    """Helper function that overwrites 'doc_section' with data from 'node'.

    This includes columns, description, meta, tags, etc.
    We assume node is the single source of truth, so doc_section is replaced.
    """
    logger.debug(":arrows_counterclockwise: Syncing doc_section with node => %s", node.unique_id)
    if node.description and not doc_section.get("description"):
        doc_section["description"] = node.description

    current_columns: list[dict[str, t.Any]] = doc_section.setdefault("columns", [])
    incoming_columns: list[dict[str, t.Any]] = []

    current_map = {}
    for c in current_columns:
        from dbt_osmosis.core.introspection import normalize_column_name

        norm_name = normalize_column_name(c["name"], context.project.runtime_cfg.credentials.type)
        current_map[norm_name] = c

    for name, meta in node.columns.items():
        cdict = meta.to_dict(omit_none=True)
        cdict["name"] = name
        from dbt_osmosis.core.introspection import _get_setting_for_node, normalize_column_name

        norm_name = normalize_column_name(name, context.project.runtime_cfg.credentials.type)

        current_yaml = t.cast(dict[str, t.Any], current_map.get(norm_name, {}))
        merged = dict(current_yaml)

        skip_add_types = _get_setting_for_node(
            "skip-add-data-types", node, name, fallback=context.settings.skip_add_data_types
        )
        for k, v in cdict.items():
            if k != "data_type" and skip_add_types:
                # don't add data types if told not to
                continue
            if k == "constraints" and "constraints" in merged:
                # keep constraints as is if present, mashumaro dumps too much info :shrug:
                continue
            merged[k] = v

        if merged.get("description") is None:
            merged.pop("description", None)
        if merged.get("tags", []) == []:
            merged.pop("tags", None)
        if merged.get("meta", {}) == {}:
            merged.pop("meta", None)

        for k in set(merged.keys()) - {"name", "description", "tags", "meta"}:
            if merged[k] in (None, [], {}):
                merged.pop(k)

        if _get_setting_for_node(
            "output-to-lower", node, name, fallback=context.settings.output_to_lower
        ):
            merged["name"] = merged["name"].lower()

        incoming_columns.append(merged)

    doc_section["columns"] = incoming_columns
```
===== 3 =====
```
             "skip-add-data-types", node, name, fallback=context.settings.skip_add_data_types
         )
         for k, v in cdict.items():
-            if k == "data_type" and skip_add_types:
+            if k != "data_type" and skip_add_types:
                 # don't add data types if told not to
                 continue
             if k == "constraints" and "constraints" in merged:
@@ -58,4 +58,4 @@ 
         incoming_columns.append(merged)
 
-    doc_section["columns"] = incoming_columns+    doc_section["columns"] = incoming_columns
```
```
def _sync_doc_section(context: t.Any, node: ResultNode, doc_section: dict[str, t.Any]) -> None:
    """Helper function that overwrites 'doc_section' with data from 'node'.

    This includes columns, description, meta, tags, etc.
    We assume node is the single source of truth, so doc_section is replaced.
    """
    logger.debug(":arrows_counterclockwise: Syncing doc_section with node => %s", node.unique_id)
    if node.description and not doc_section.get("description"):
        doc_section["description"] = node.description

    current_columns: list[dict[str, t.Any]] = doc_section.setdefault("columns", [])
    incoming_columns: list[dict[str, t.Any]] = []

    current_map = {}
    for c in current_columns:
        from dbt_osmosis.core.introspection import normalize_column_name

        norm_name = normalize_column_name(c["name"], context.project.runtime_cfg.credentials.type)
        current_map[norm_name] = c

    for name, meta in node.columns.items():
        cdict = meta.to_dict(omit_none=True)
        cdict["name"] = name
        from dbt_osmosis.core.introspection import _get_setting_for_node, normalize_column_name

        norm_name = normalize_column_name(name, context.project.runtime_cfg.credentials.type)

        current_yaml = t.cast(dict[str, t.Any], current_map.get(norm_name, {}))
        merged = dict(current_yaml)

        skip_add_types = _get_setting_for_node(
            "skip-add-data-types", node, name, fallback=context.settings.skip_add_data_types
        )
        for k, v in cdict.items():
            if k != "data_type" and skip_add_types:
                # don't add data types if told not to
                continue
            if k == "constraints" and "constraints" in merged:
                # keep constraints as is if present, mashumaro dumps too much info :shrug:
                continue
            merged[k] = v

        if merged.get("description") is None:
            merged.pop("description", None)
        if merged.get("tags", []) == []:
            merged.pop("tags", None)
        if merged.get("meta", {}) == {}:
            merged.pop("meta", None)

        for k in set(merged.keys()) - {"name", "description", "tags", "meta"}:
            if merged[k] in (None, [], {}):
                merged.pop(k)

        if _get_setting_for_node(
            "output-to-lower", node, name, fallback=context.settings.output_to_lower
        ):
            merged["name"] = merged["name"].lower()

        incoming_columns.append(merged)

    doc_section["columns"] = incoming_columns

```
===== 4 =====
```
             "skip-add-data-types", node, name, fallback=context.settings.skip_add_data_types
         )
         for k, v in cdict.items():
-            if k == "data_type" and skip_add_types:
+            if k == "data_type" or skip_add_types:
                 # don't add data types if told not to
                 continue
             if k == "constraints" and "constraints" in merged:
```
```
def _sync_doc_section(context: t.Any, node: ResultNode, doc_section: dict[str, t.Any]) -> None:
    """Helper function that overwrites 'doc_section' with data from 'node'.

    This includes columns, description, meta, tags, etc.
    We assume node is the single source of truth, so doc_section is replaced.
    """
    logger.debug(":arrows_counterclockwise: Syncing doc_section with node => %s", node.unique_id)
    if node.description and not doc_section.get("description"):
        doc_section["description"] = node.description

    current_columns: list[dict[str, t.Any]] = doc_section.setdefault("columns", [])
    incoming_columns: list[dict[str, t.Any]] = []

    current_map = {}
    for c in current_columns:
        from dbt_osmosis.core.introspection import normalize_column_name

        norm_name = normalize_column_name(c["name"], context.project.runtime_cfg.credentials.type)
        current_map[norm_name] = c

    for name, meta in node.columns.items():
        cdict = meta.to_dict(omit_none=True)
        cdict["name"] = name
        from dbt_osmosis.core.introspection import _get_setting_for_node, normalize_column_name

        norm_name = normalize_column_name(name, context.project.runtime_cfg.credentials.type)

        current_yaml = t.cast(dict[str, t.Any], current_map.get(norm_name, {}))
        merged = dict(current_yaml)

        skip_add_types = _get_setting_for_node(
            "skip-add-data-types", node, name, fallback=context.settings.skip_add_data_types
        )
        for k, v in cdict.items():
            if k == "data_type" or skip_add_types:
                # don't add data types if told not to
                continue
            if k == "constraints" and "constraints" in merged:
                # keep constraints as is if present, mashumaro dumps too much info :shrug:
                continue
            merged[k] = v

        if merged.get("description") is None:
            merged.pop("description", None)
        if merged.get("tags", []) == []:
            merged.pop("tags", None)
        if merged.get("meta", {}) == {}:
            merged.pop("meta", None)

        for k in set(merged.keys()) - {"name", "description", "tags", "meta"}:
            if merged[k] in (None, [], {}):
                merged.pop(k)

        if _get_setting_for_node(
            "output-to-lower", node, name, fallback=context.settings.output_to_lower
        ):
            merged["name"] = merged["name"].lower()

        incoming_columns.append(merged)

    doc_section["columns"] = incoming_columns
```
===== 5 =====
```
             "skip-add-data-types", node, name, fallback=context.settings.skip_add_data_types
         )
         for k, v in cdict.items():
-            if k == "data_type" and skip_add_types:
+            if k == "data_type" or skip_add_types:
                 # don't add data types if told not to
                 continue
             if k == "constraints" and "constraints" in merged:
@@ -58,4 +58,4 @@ 
         incoming_columns.append(merged)
 
-    doc_section["columns"] = incoming_columns+    doc_section["columns"] = incoming_columns
```
```
def _sync_doc_section(context: t.Any, node: ResultNode, doc_section: dict[str, t.Any]) -> None:
    """Helper function that overwrites 'doc_section' with data from 'node'.

    This includes columns, description, meta, tags, etc.
    We assume node is the single source of truth, so doc_section is replaced.
    """
    logger.debug(":arrows_counterclockwise: Syncing doc_section with node => %s", node.unique_id)
    if node.description and not doc_section.get("description"):
        doc_section["description"] = node.description

    current_columns: list[dict[str, t.Any]] = doc_section.setdefault("columns", [])
    incoming_columns: list[dict[str, t.Any]] = []

    current_map = {}
    for c in current_columns:
        from dbt_osmosis.core.introspection import normalize_column_name

        norm_name = normalize_column_name(c["name"], context.project.runtime_cfg.credentials.type)
        current_map[norm_name] = c

    for name, meta in node.columns.items():
        cdict = meta.to_dict(omit_none=True)
        cdict["name"] = name
        from dbt_osmosis.core.introspection import _get_setting_for_node, normalize_column_name

        norm_name = normalize_column_name(name, context.project.runtime_cfg.credentials.type)

        current_yaml = t.cast(dict[str, t.Any], current_map.get(norm_name, {}))
        merged = dict(current_yaml)

        skip_add_types = _get_setting_for_node(
            "skip-add-data-types", node, name, fallback=context.settings.skip_add_data_types
        )
        for k, v in cdict.items():
            if k == "data_type" or skip_add_types:
                # don't add data types if told not to
                continue
            if k == "constraints" and "constraints" in merged:
                # keep constraints as is if present, mashumaro dumps too much info :shrug:
                continue
            merged[k] = v

        if merged.get("description") is None:
            merged.pop("description", None)
        if merged.get("tags", []) == []:
            merged.pop("tags", None)
        if merged.get("meta", {}) == {}:
            merged.pop("meta", None)

        for k in set(merged.keys()) - {"name", "description", "tags", "meta"}:
            if merged[k] in (None, [], {}):
                merged.pop(k)

        if _get_setting_for_node(
            "output-to-lower", node, name, fallback=context.settings.output_to_lower
        ):
            merged["name"] = merged["name"].lower()

        incoming_columns.append(merged)

    doc_section["columns"] = incoming_columns

```
===== 6 =====
```
         for k, v in cdict.items():
             if k == "data_type" and skip_add_types:
                 # don't add data types if told not to
-                continue
+                break
             if k == "constraints" and "constraints" in merged:
                 # keep constraints as is if present, mashumaro dumps too much info :shrug:
                 continue
@@ -58,4 +58,4 @@ 
         incoming_columns.append(merged)
 
-    doc_section["columns"] = incoming_columns+    doc_section["columns"] = incoming_columns
```
```
def _sync_doc_section(context: t.Any, node: ResultNode, doc_section: dict[str, t.Any]) -> None:
    """Helper function that overwrites 'doc_section' with data from 'node'.

    This includes columns, description, meta, tags, etc.
    We assume node is the single source of truth, so doc_section is replaced.
    """
    logger.debug(":arrows_counterclockwise: Syncing doc_section with node => %s", node.unique_id)
    if node.description and not doc_section.get("description"):
        doc_section["description"] = node.description

    current_columns: list[dict[str, t.Any]] = doc_section.setdefault("columns", [])
    incoming_columns: list[dict[str, t.Any]] = []

    current_map = {}
    for c in current_columns:
        from dbt_osmosis.core.introspection import normalize_column_name

        norm_name = normalize_column_name(c["name"], context.project.runtime_cfg.credentials.type)
        current_map[norm_name] = c

    for name, meta in node.columns.items():
        cdict = meta.to_dict(omit_none=True)
        cdict["name"] = name
        from dbt_osmosis.core.introspection import _get_setting_for_node, normalize_column_name

        norm_name = normalize_column_name(name, context.project.runtime_cfg.credentials.type)

        current_yaml = t.cast(dict[str, t.Any], current_map.get(norm_name, {}))
        merged = dict(current_yaml)

        skip_add_types = _get_setting_for_node(
            "skip-add-data-types", node, name, fallback=context.settings.skip_add_data_types
        )
        for k, v in cdict.items():
            if k == "data_type" and skip_add_types:
                # don't add data types if told not to
                break
            if k == "constraints" and "constraints" in merged:
                # keep constraints as is if present, mashumaro dumps too much info :shrug:
                continue
            merged[k] = v

        if merged.get("description") is None:
            merged.pop("description", None)
        if merged.get("tags", []) == []:
            merged.pop("tags", None)
        if merged.get("meta", {}) == {}:
            merged.pop("meta", None)

        for k in set(merged.keys()) - {"name", "description", "tags", "meta"}:
            if merged[k] in (None, [], {}):
                merged.pop(k)

        if _get_setting_for_node(
            "output-to-lower", node, name, fallback=context.settings.output_to_lower
        ):
            merged["name"] = merged["name"].lower()

        incoming_columns.append(merged)

    doc_section["columns"] = incoming_columns

```
===== 7 =====
```
             if k == "data_type" and skip_add_types:
                 # don't add data types if told not to
                 continue
-            if k == "constraints" and "constraints" in merged:
+            if k != "constraints" and "constraints" in merged:
                 # keep constraints as is if present, mashumaro dumps too much info :shrug:
                 continue
             merged[k] = v
@@ -58,4 +58,4 @@ 
         incoming_columns.append(merged)
 
-    doc_section["columns"] = incoming_columns+    doc_section["columns"] = incoming_columns
```
```
def _sync_doc_section(context: t.Any, node: ResultNode, doc_section: dict[str, t.Any]) -> None:
    """Helper function that overwrites 'doc_section' with data from 'node'.

    This includes columns, description, meta, tags, etc.
    We assume node is the single source of truth, so doc_section is replaced.
    """
    logger.debug(":arrows_counterclockwise: Syncing doc_section with node => %s", node.unique_id)
    if node.description and not doc_section.get("description"):
        doc_section["description"] = node.description

    current_columns: list[dict[str, t.Any]] = doc_section.setdefault("columns", [])
    incoming_columns: list[dict[str, t.Any]] = []

    current_map = {}
    for c in current_columns:
        from dbt_osmosis.core.introspection import normalize_column_name

        norm_name = normalize_column_name(c["name"], context.project.runtime_cfg.credentials.type)
        current_map[norm_name] = c

    for name, meta in node.columns.items():
        cdict = meta.to_dict(omit_none=True)
        cdict["name"] = name
        from dbt_osmosis.core.introspection import _get_setting_for_node, normalize_column_name

        norm_name = normalize_column_name(name, context.project.runtime_cfg.credentials.type)

        current_yaml = t.cast(dict[str, t.Any], current_map.get(norm_name, {}))
        merged = dict(current_yaml)

        skip_add_types = _get_setting_for_node(
            "skip-add-data-types", node, name, fallback=context.settings.skip_add_data_types
        )
        for k, v in cdict.items():
            if k == "data_type" and skip_add_types:
                # don't add data types if told not to
                continue
            if k != "constraints" and "constraints" in merged:
                # keep constraints as is if present, mashumaro dumps too much info :shrug:
                continue
            merged[k] = v

        if merged.get("description") is None:
            merged.pop("description", None)
        if merged.get("tags", []) == []:
            merged.pop("tags", None)
        if merged.get("meta", {}) == {}:
            merged.pop("meta", None)

        for k in set(merged.keys()) - {"name", "description", "tags", "meta"}:
            if merged[k] in (None, [], {}):
                merged.pop(k)

        if _get_setting_for_node(
            "output-to-lower", node, name, fallback=context.settings.output_to_lower
        ):
            merged["name"] = merged["name"].lower()

        incoming_columns.append(merged)

    doc_section["columns"] = incoming_columns

```
===== 8 =====
```
                 continue
             merged[k] = v
 
-        if merged.get("description") is None:
+        if "description" in merged and merged["description"] != "":
             merged.pop("description", None)
         if merged.get("tags", []) == []:
             merged.pop("tags", None)
```
```
def _sync_doc_section(context: t.Any, node: ResultNode, doc_section: dict[str, t.Any]) -> None:
    """Helper function that overwrites 'doc_section' with data from 'node'.

    This includes columns, description, meta, tags, etc.
    We assume node is the single source of truth, so doc_section is replaced.
    """
    logger.debug(":arrows_counterclockwise: Syncing doc_section with node => %s", node.unique_id)
    if node.description and not doc_section.get("description"):
        doc_section["description"] = node.description

    current_columns: list[dict[str, t.Any]] = doc_section.setdefault("columns", [])
    incoming_columns: list[dict[str, t.Any]] = []

    current_map = {}
    for c in current_columns:
        from dbt_osmosis.core.introspection import normalize_column_name

        norm_name = normalize_column_name(c["name"], context.project.runtime_cfg.credentials.type)
        current_map[norm_name] = c

    for name, meta in node.columns.items():
        cdict = meta.to_dict(omit_none=True)
        cdict["name"] = name
        from dbt_osmosis.core.introspection import _get_setting_for_node, normalize_column_name

        norm_name = normalize_column_name(name, context.project.runtime_cfg.credentials.type)

        current_yaml = t.cast(dict[str, t.Any], current_map.get(norm_name, {}))
        merged = dict(current_yaml)

        skip_add_types = _get_setting_for_node(
            "skip-add-data-types", node, name, fallback=context.settings.skip_add_data_types
        )
        for k, v in cdict.items():
            if k == "data_type" and skip_add_types:
                # don't add data types if told not to
                continue
            if k == "constraints" and "constraints" in merged:
                # keep constraints as is if present, mashumaro dumps too much info :shrug:
                continue
            merged[k] = v

        if "description" in merged and merged["description"] != "":
            merged.pop("description", None)
        if merged.get("tags", []) == []:
            merged.pop("tags", None)
        if merged.get("meta", {}) == {}:
            merged.pop("meta", None)

        for k in set(merged.keys()) - {"name", "description", "tags", "meta"}:
            if merged[k] in (None, [], {}):
                merged.pop(k)

        if _get_setting_for_node(
            "output-to-lower", node, name, fallback=context.settings.output_to_lower
        ):
            merged["name"] = merged["name"].lower()

        incoming_columns.append(merged)

    doc_section["columns"] = incoming_columns
```
===== 9 =====
```
                 continue
             merged[k] = v
 
-        if merged.get("description") is None:
+        if merged.get("DESCRIPTION") is None:
             merged.pop("description", None)
         if merged.get("tags", []) == []:
             merged.pop("tags", None)
@@ -58,4 +58,4 @@ 
         incoming_columns.append(merged)
 
-    doc_section["columns"] = incoming_columns+    doc_section["columns"] = incoming_columns
```
```
def _sync_doc_section(context: t.Any, node: ResultNode, doc_section: dict[str, t.Any]) -> None:
    """Helper function that overwrites 'doc_section' with data from 'node'.

    This includes columns, description, meta, tags, etc.
    We assume node is the single source of truth, so doc_section is replaced.
    """
    logger.debug(":arrows_counterclockwise: Syncing doc_section with node => %s", node.unique_id)
    if node.description and not doc_section.get("description"):
        doc_section["description"] = node.description

    current_columns: list[dict[str, t.Any]] = doc_section.setdefault("columns", [])
    incoming_columns: list[dict[str, t.Any]] = []

    current_map = {}
    for c in current_columns:
        from dbt_osmosis.core.introspection import normalize_column_name

        norm_name = normalize_column_name(c["name"], context.project.runtime_cfg.credentials.type)
        current_map[norm_name] = c

    for name, meta in node.columns.items():
        cdict = meta.to_dict(omit_none=True)
        cdict["name"] = name
        from dbt_osmosis.core.introspection import _get_setting_for_node, normalize_column_name

        norm_name = normalize_column_name(name, context.project.runtime_cfg.credentials.type)

        current_yaml = t.cast(dict[str, t.Any], current_map.get(norm_name, {}))
        merged = dict(current_yaml)

        skip_add_types = _get_setting_for_node(
            "skip-add-data-types", node, name, fallback=context.settings.skip_add_data_types
        )
        for k, v in cdict.items():
            if k == "data_type" and skip_add_types:
                # don't add data types if told not to
                continue
            if k == "constraints" and "constraints" in merged:
                # keep constraints as is if present, mashumaro dumps too much info :shrug:
                continue
            merged[k] = v

        if merged.get("DESCRIPTION") is None:
            merged.pop("description", None)
        if merged.get("tags", []) == []:
            merged.pop("tags", None)
        if merged.get("meta", {}) == {}:
            merged.pop("meta", None)

        for k in set(merged.keys()) - {"name", "description", "tags", "meta"}:
            if merged[k] in (None, [], {}):
                merged.pop(k)

        if _get_setting_for_node(
            "output-to-lower", node, name, fallback=context.settings.output_to_lower
        ):
            merged["name"] = merged["name"].lower()

        incoming_columns.append(merged)

    doc_section["columns"] = incoming_columns

```
===== 10 =====
```
                 continue
             merged[k] = v
 
-        if merged.get("description") is None:
+        if merged.get("XXdescriptionXX") is None:
             merged.pop("description", None)
         if merged.get("tags", []) == []:
             merged.pop("tags", None)
@@ -58,4 +58,4 @@ 
         incoming_columns.append(merged)
 
-    doc_section["columns"] = incoming_columns+    doc_section["columns"] = incoming_columns
```
```
def _sync_doc_section(context: t.Any, node: ResultNode, doc_section: dict[str, t.Any]) -> None:
    """Helper function that overwrites 'doc_section' with data from 'node'.

    This includes columns, description, meta, tags, etc.
    We assume node is the single source of truth, so doc_section is replaced.
    """
    logger.debug(":arrows_counterclockwise: Syncing doc_section with node => %s", node.unique_id)
    if node.description and not doc_section.get("description"):
        doc_section["description"] = node.description

    current_columns: list[dict[str, t.Any]] = doc_section.setdefault("columns", [])
    incoming_columns: list[dict[str, t.Any]] = []

    current_map = {}
    for c in current_columns:
        from dbt_osmosis.core.introspection import normalize_column_name

        norm_name = normalize_column_name(c["name"], context.project.runtime_cfg.credentials.type)
        current_map[norm_name] = c

    for name, meta in node.columns.items():
        cdict = meta.to_dict(omit_none=True)
        cdict["name"] = name
        from dbt_osmosis.core.introspection import _get_setting_for_node, normalize_column_name

        norm_name = normalize_column_name(name, context.project.runtime_cfg.credentials.type)

        current_yaml = t.cast(dict[str, t.Any], current_map.get(norm_name, {}))
        merged = dict(current_yaml)

        skip_add_types = _get_setting_for_node(
            "skip-add-data-types", node, name, fallback=context.settings.skip_add_data_types
        )
        for k, v in cdict.items():
            if k == "data_type" and skip_add_types:
                # don't add data types if told not to
                continue
            if k == "constraints" and "constraints" in merged:
                # keep constraints as is if present, mashumaro dumps too much info :shrug:
                continue
            merged[k] = v

        if merged.get("XXdescriptionXX") is None:
            merged.pop("description", None)
        if merged.get("tags", []) == []:
            merged.pop("tags", None)
        if merged.get("meta", {}) == {}:
            merged.pop("meta", None)

        for k in set(merged.keys()) - {"name", "description", "tags", "meta"}:
            if merged[k] in (None, [], {}):
                merged.pop(k)

        if _get_setting_for_node(
            "output-to-lower", node, name, fallback=context.settings.output_to_lower
        ):
            merged["name"] = merged["name"].lower()

        incoming_columns.append(merged)

    doc_section["columns"] = incoming_columns

```
===== 11 =====
```
                 continue
             merged[k] = v
 
-        if merged.get("description") is None:
+        if merged.get("description") is not None:
             merged.pop("description", None)
         if merged.get("tags", []) == []:
             merged.pop("tags", None)
```
```
def _sync_doc_section(context: t.Any, node: ResultNode, doc_section: dict[str, t.Any]) -> None:
    """Helper function that overwrites 'doc_section' with data from 'node'.

    This includes columns, description, meta, tags, etc.
    We assume node is the single source of truth, so doc_section is replaced.
    """
    logger.debug(":arrows_counterclockwise: Syncing doc_section with node => %s", node.unique_id)
    if node.description and not doc_section.get("description"):
        doc_section["description"] = node.description

    current_columns: list[dict[str, t.Any]] = doc_section.setdefault("columns", [])
    incoming_columns: list[dict[str, t.Any]] = []

    current_map = {}
    for c in current_columns:
        from dbt_osmosis.core.introspection import normalize_column_name

        norm_name = normalize_column_name(c["name"], context.project.runtime_cfg.credentials.type)
        current_map[norm_name] = c

    for name, meta in node.columns.items():
        cdict = meta.to_dict(omit_none=True)
        cdict["name"] = name
        from dbt_osmosis.core.introspection import _get_setting_for_node, normalize_column_name

        norm_name = normalize_column_name(name, context.project.runtime_cfg.credentials.type)

        current_yaml = t.cast(dict[str, t.Any], current_map.get(norm_name, {}))
        merged = dict(current_yaml)

        skip_add_types = _get_setting_for_node(
            "skip-add-data-types", node, name, fallback=context.settings.skip_add_data_types
        )
        for k, v in cdict.items():
            if k == "data_type" and skip_add_types:
                # don't add data types if told not to
                continue
            if k == "constraints" and "constraints" in merged:
                # keep constraints as is if present, mashumaro dumps too much info :shrug:
                continue
            merged[k] = v

        if merged.get("description") is not None:
            merged.pop("description", None)
        if merged.get("tags", []) == []:
            merged.pop("tags", None)
        if merged.get("meta", {}) == {}:
            merged.pop("meta", None)

        for k in set(merged.keys()) - {"name", "description", "tags", "meta"}:
            if merged[k] in (None, [], {}):
                merged.pop(k)

        if _get_setting_for_node(
            "output-to-lower", node, name, fallback=context.settings.output_to_lower
        ):
            merged["name"] = merged["name"].lower()

        incoming_columns.append(merged)

    doc_section["columns"] = incoming_columns
```
===== 12 =====
```
                 continue
             merged[k] = v
 
-        if merged.get("description") is None:
+        if merged.get("description") is not None:
             merged.pop("description", None)
         if merged.get("tags", []) == []:
             merged.pop("tags", None)
@@ -58,4 +58,4 @@ 
         incoming_columns.append(merged)
 
-    doc_section["columns"] = incoming_columns+    doc_section["columns"] = incoming_columns
```
```
def _sync_doc_section(context: t.Any, node: ResultNode, doc_section: dict[str, t.Any]) -> None:
    """Helper function that overwrites 'doc_section' with data from 'node'.

    This includes columns, description, meta, tags, etc.
    We assume node is the single source of truth, so doc_section is replaced.
    """
    logger.debug(":arrows_counterclockwise: Syncing doc_section with node => %s", node.unique_id)
    if node.description and not doc_section.get("description"):
        doc_section["description"] = node.description

    current_columns: list[dict[str, t.Any]] = doc_section.setdefault("columns", [])
    incoming_columns: list[dict[str, t.Any]] = []

    current_map = {}
    for c in current_columns:
        from dbt_osmosis.core.introspection import normalize_column_name

        norm_name = normalize_column_name(c["name"], context.project.runtime_cfg.credentials.type)
        current_map[norm_name] = c

    for name, meta in node.columns.items():
        cdict = meta.to_dict(omit_none=True)
        cdict["name"] = name
        from dbt_osmosis.core.introspection import _get_setting_for_node, normalize_column_name

        norm_name = normalize_column_name(name, context.project.runtime_cfg.credentials.type)

        current_yaml = t.cast(dict[str, t.Any], current_map.get(norm_name, {}))
        merged = dict(current_yaml)

        skip_add_types = _get_setting_for_node(
            "skip-add-data-types", node, name, fallback=context.settings.skip_add_data_types
        )
        for k, v in cdict.items():
            if k == "data_type" and skip_add_types:
                # don't add data types if told not to
                continue
            if k == "constraints" and "constraints" in merged:
                # keep constraints as is if present, mashumaro dumps too much info :shrug:
                continue
            merged[k] = v

        if merged.get("description") is not None:
            merged.pop("description", None)
        if merged.get("tags", []) == []:
            merged.pop("tags", None)
        if merged.get("meta", {}) == {}:
            merged.pop("meta", None)

        for k in set(merged.keys()) - {"name", "description", "tags", "meta"}:
            if merged[k] in (None, [], {}):
                merged.pop(k)

        if _get_setting_for_node(
            "output-to-lower", node, name, fallback=context.settings.output_to_lower
        ):
            merged["name"] = merged["name"].lower()

        incoming_columns.append(merged)

    doc_section["columns"] = incoming_columns

```
===== 13 =====
```
                 continue
             merged[k] = v
 
-        if merged.get("description") is None:
+        if merged.get(None) is None:
             merged.pop("description", None)
         if merged.get("tags", []) == []:
             merged.pop("tags", None)
@@ -58,4 +58,4 @@ 
         incoming_columns.append(merged)
 
-    doc_section["columns"] = incoming_columns+    doc_section["columns"] = incoming_columns
```
```
def _sync_doc_section(context: t.Any, node: ResultNode, doc_section: dict[str, t.Any]) -> None:
    """Helper function that overwrites 'doc_section' with data from 'node'.

    This includes columns, description, meta, tags, etc.
    We assume node is the single source of truth, so doc_section is replaced.
    """
    logger.debug(":arrows_counterclockwise: Syncing doc_section with node => %s", node.unique_id)
    if node.description and not doc_section.get("description"):
        doc_section["description"] = node.description

    current_columns: list[dict[str, t.Any]] = doc_section.setdefault("columns", [])
    incoming_columns: list[dict[str, t.Any]] = []

    current_map = {}
    for c in current_columns:
        from dbt_osmosis.core.introspection import normalize_column_name

        norm_name = normalize_column_name(c["name"], context.project.runtime_cfg.credentials.type)
        current_map[norm_name] = c

    for name, meta in node.columns.items():
        cdict = meta.to_dict(omit_none=True)
        cdict["name"] = name
        from dbt_osmosis.core.introspection import _get_setting_for_node, normalize_column_name

        norm_name = normalize_column_name(name, context.project.runtime_cfg.credentials.type)

        current_yaml = t.cast(dict[str, t.Any], current_map.get(norm_name, {}))
        merged = dict(current_yaml)

        skip_add_types = _get_setting_for_node(
            "skip-add-data-types", node, name, fallback=context.settings.skip_add_data_types
        )
        for k, v in cdict.items():
            if k == "data_type" and skip_add_types:
                # don't add data types if told not to
                continue
            if k == "constraints" and "constraints" in merged:
                # keep constraints as is if present, mashumaro dumps too much info :shrug:
                continue
            merged[k] = v

        if merged.get(None) is None:
            merged.pop("description", None)
        if merged.get("tags", []) == []:
            merged.pop("tags", None)
        if merged.get("meta", {}) == {}:
            merged.pop("meta", None)

        for k in set(merged.keys()) - {"name", "description", "tags", "meta"}:
            if merged[k] in (None, [], {}):
                merged.pop(k)

        if _get_setting_for_node(
            "output-to-lower", node, name, fallback=context.settings.output_to_lower
        ):
            merged["name"] = merged["name"].lower()

        incoming_columns.append(merged)

    doc_section["columns"] = incoming_columns

```
===== 14 =====
```
 
         if merged.get("description") is None:
             merged.pop("description", None)
-        if merged.get("tags", []) == []:
+        if merged.get("TAGS", []) == []:
             merged.pop("tags", None)
         if merged.get("meta", {}) == {}:
             merged.pop("meta", None)
@@ -58,4 +58,4 @@ 
         incoming_columns.append(merged)
 
-    doc_section["columns"] = incoming_columns+    doc_section["columns"] = incoming_columns
```
```
def _sync_doc_section(context: t.Any, node: ResultNode, doc_section: dict[str, t.Any]) -> None:
    """Helper function that overwrites 'doc_section' with data from 'node'.

    This includes columns, description, meta, tags, etc.
    We assume node is the single source of truth, so doc_section is replaced.
    """
    logger.debug(":arrows_counterclockwise: Syncing doc_section with node => %s", node.unique_id)
    if node.description and not doc_section.get("description"):
        doc_section["description"] = node.description

    current_columns: list[dict[str, t.Any]] = doc_section.setdefault("columns", [])
    incoming_columns: list[dict[str, t.Any]] = []

    current_map = {}
    for c in current_columns:
        from dbt_osmosis.core.introspection import normalize_column_name

        norm_name = normalize_column_name(c["name"], context.project.runtime_cfg.credentials.type)
        current_map[norm_name] = c

    for name, meta in node.columns.items():
        cdict = meta.to_dict(omit_none=True)
        cdict["name"] = name
        from dbt_osmosis.core.introspection import _get_setting_for_node, normalize_column_name

        norm_name = normalize_column_name(name, context.project.runtime_cfg.credentials.type)

        current_yaml = t.cast(dict[str, t.Any], current_map.get(norm_name, {}))
        merged = dict(current_yaml)

        skip_add_types = _get_setting_for_node(
            "skip-add-data-types", node, name, fallback=context.settings.skip_add_data_types
        )
        for k, v in cdict.items():
            if k == "data_type" and skip_add_types:
                # don't add data types if told not to
                continue
            if k == "constraints" and "constraints" in merged:
                # keep constraints as is if present, mashumaro dumps too much info :shrug:
                continue
            merged[k] = v

        if merged.get("description") is None:
            merged.pop("description", None)
        if merged.get("TAGS", []) == []:
            merged.pop("tags", None)
        if merged.get("meta", {}) == {}:
            merged.pop("meta", None)

        for k in set(merged.keys()) - {"name", "description", "tags", "meta"}:
            if merged[k] in (None, [], {}):
                merged.pop(k)

        if _get_setting_for_node(
            "output-to-lower", node, name, fallback=context.settings.output_to_lower
        ):
            merged["name"] = merged["name"].lower()

        incoming_columns.append(merged)

    doc_section["columns"] = incoming_columns

```
===== 15 =====
```
 
         if merged.get("description") is None:
             merged.pop("description", None)
-        if merged.get("tags", []) == []:
+        if merged.get("XXtagsXX", []) == []:
             merged.pop("tags", None)
         if merged.get("meta", {}) == {}:
             merged.pop("meta", None)
@@ -58,4 +58,4 @@ 
         incoming_columns.append(merged)
 
-    doc_section["columns"] = incoming_columns+    doc_section["columns"] = incoming_columns
```
```
def _sync_doc_section(context: t.Any, node: ResultNode, doc_section: dict[str, t.Any]) -> None:
    """Helper function that overwrites 'doc_section' with data from 'node'.

    This includes columns, description, meta, tags, etc.
    We assume node is the single source of truth, so doc_section is replaced.
    """
    logger.debug(":arrows_counterclockwise: Syncing doc_section with node => %s", node.unique_id)
    if node.description and not doc_section.get("description"):
        doc_section["description"] = node.description

    current_columns: list[dict[str, t.Any]] = doc_section.setdefault("columns", [])
    incoming_columns: list[dict[str, t.Any]] = []

    current_map = {}
    for c in current_columns:
        from dbt_osmosis.core.introspection import normalize_column_name

        norm_name = normalize_column_name(c["name"], context.project.runtime_cfg.credentials.type)
        current_map[norm_name] = c

    for name, meta in node.columns.items():
        cdict = meta.to_dict(omit_none=True)
        cdict["name"] = name
        from dbt_osmosis.core.introspection import _get_setting_for_node, normalize_column_name

        norm_name = normalize_column_name(name, context.project.runtime_cfg.credentials.type)

        current_yaml = t.cast(dict[str, t.Any], current_map.get(norm_name, {}))
        merged = dict(current_yaml)

        skip_add_types = _get_setting_for_node(
            "skip-add-data-types", node, name, fallback=context.settings.skip_add_data_types
        )
        for k, v in cdict.items():
            if k == "data_type" and skip_add_types:
                # don't add data types if told not to
                continue
            if k == "constraints" and "constraints" in merged:
                # keep constraints as is if present, mashumaro dumps too much info :shrug:
                continue
            merged[k] = v

        if merged.get("description") is None:
            merged.pop("description", None)
        if merged.get("XXtagsXX", []) == []:
            merged.pop("tags", None)
        if merged.get("meta", {}) == {}:
            merged.pop("meta", None)

        for k in set(merged.keys()) - {"name", "description", "tags", "meta"}:
            if merged[k] in (None, [], {}):
                merged.pop(k)

        if _get_setting_for_node(
            "output-to-lower", node, name, fallback=context.settings.output_to_lower
        ):
            merged["name"] = merged["name"].lower()

        incoming_columns.append(merged)

    doc_section["columns"] = incoming_columns

```
===== 16 =====
```
 
         if merged.get("description") is None:
             merged.pop("description", None)
-        if merged.get("tags", []) == []:
+        if merged.get("tags", []) != []:
             merged.pop("tags", None)
         if merged.get("meta", {}) == {}:
             merged.pop("meta", None)
```
```
def _sync_doc_section(context: t.Any, node: ResultNode, doc_section: dict[str, t.Any]) -> None:
    """Helper function that overwrites 'doc_section' with data from 'node'.

    This includes columns, description, meta, tags, etc.
    We assume node is the single source of truth, so doc_section is replaced.
    """
    logger.debug(":arrows_counterclockwise: Syncing doc_section with node => %s", node.unique_id)
    if node.description and not doc_section.get("description"):
        doc_section["description"] = node.description

    current_columns: list[dict[str, t.Any]] = doc_section.setdefault("columns", [])
    incoming_columns: list[dict[str, t.Any]] = []

    current_map = {}
    for c in current_columns:
        from dbt_osmosis.core.introspection import normalize_column_name

        norm_name = normalize_column_name(c["name"], context.project.runtime_cfg.credentials.type)
        current_map[norm_name] = c

    for name, meta in node.columns.items():
        cdict = meta.to_dict(omit_none=True)
        cdict["name"] = name
        from dbt_osmosis.core.introspection import _get_setting_for_node, normalize_column_name

        norm_name = normalize_column_name(name, context.project.runtime_cfg.credentials.type)

        current_yaml = t.cast(dict[str, t.Any], current_map.get(norm_name, {}))
        merged = dict(current_yaml)

        skip_add_types = _get_setting_for_node(
            "skip-add-data-types", node, name, fallback=context.settings.skip_add_data_types
        )
        for k, v in cdict.items():
            if k == "data_type" and skip_add_types:
                # don't add data types if told not to
                continue
            if k == "constraints" and "constraints" in merged:
                # keep constraints as is if present, mashumaro dumps too much info :shrug:
                continue
            merged[k] = v

        if merged.get("description") is None:
            merged.pop("description", None)
        if merged.get("tags", []) != []:
            merged.pop("tags", None)
        if merged.get("meta", {}) == {}:
            merged.pop("meta", None)

        for k in set(merged.keys()) - {"name", "description", "tags", "meta"}:
            if merged[k] in (None, [], {}):
                merged.pop(k)

        if _get_setting_for_node(
            "output-to-lower", node, name, fallback=context.settings.output_to_lower
        ):
            merged["name"] = merged["name"].lower()

        incoming_columns.append(merged)

    doc_section["columns"] = incoming_columns
```
===== 17 =====
```
 
         if merged.get("description") is None:
             merged.pop("description", None)
-        if merged.get("tags", []) == []:
+        if merged.get("tags", []) != []:
             merged.pop("tags", None)
         if merged.get("meta", {}) == {}:
             merged.pop("meta", None)
@@ -58,4 +58,4 @@ 
         incoming_columns.append(merged)
 
-    doc_section["columns"] = incoming_columns+    doc_section["columns"] = incoming_columns
```
```
def _sync_doc_section(context: t.Any, node: ResultNode, doc_section: dict[str, t.Any]) -> None:
    """Helper function that overwrites 'doc_section' with data from 'node'.

    This includes columns, description, meta, tags, etc.
    We assume node is the single source of truth, so doc_section is replaced.
    """
    logger.debug(":arrows_counterclockwise: Syncing doc_section with node => %s", node.unique_id)
    if node.description and not doc_section.get("description"):
        doc_section["description"] = node.description

    current_columns: list[dict[str, t.Any]] = doc_section.setdefault("columns", [])
    incoming_columns: list[dict[str, t.Any]] = []

    current_map = {}
    for c in current_columns:
        from dbt_osmosis.core.introspection import normalize_column_name

        norm_name = normalize_column_name(c["name"], context.project.runtime_cfg.credentials.type)
        current_map[norm_name] = c

    for name, meta in node.columns.items():
        cdict = meta.to_dict(omit_none=True)
        cdict["name"] = name
        from dbt_osmosis.core.introspection import _get_setting_for_node, normalize_column_name

        norm_name = normalize_column_name(name, context.project.runtime_cfg.credentials.type)

        current_yaml = t.cast(dict[str, t.Any], current_map.get(norm_name, {}))
        merged = dict(current_yaml)

        skip_add_types = _get_setting_for_node(
            "skip-add-data-types", node, name, fallback=context.settings.skip_add_data_types
        )
        for k, v in cdict.items():
            if k == "data_type" and skip_add_types:
                # don't add data types if told not to
                continue
            if k == "constraints" and "constraints" in merged:
                # keep constraints as is if present, mashumaro dumps too much info :shrug:
                continue
            merged[k] = v

        if merged.get("description") is None:
            merged.pop("description", None)
        if merged.get("tags", []) != []:
            merged.pop("tags", None)
        if merged.get("meta", {}) == {}:
            merged.pop("meta", None)

        for k in set(merged.keys()) - {"name", "description", "tags", "meta"}:
            if merged[k] in (None, [], {}):
                merged.pop(k)

        if _get_setting_for_node(
            "output-to-lower", node, name, fallback=context.settings.output_to_lower
        ):
            merged["name"] = merged["name"].lower()

        incoming_columns.append(merged)

    doc_section["columns"] = incoming_columns

```
===== 18 =====
```
 
         if merged.get("description") is None:
             merged.pop("description", None)
-        if merged.get("tags", []) == []:
+        if merged.get(None, []) == []:
             merged.pop("tags", None)
         if merged.get("meta", {}) == {}:
             merged.pop("meta", None)
@@ -58,4 +58,4 @@ 
         incoming_columns.append(merged)
 
-    doc_section["columns"] = incoming_columns+    doc_section["columns"] = incoming_columns
```
```
def _sync_doc_section(context: t.Any, node: ResultNode, doc_section: dict[str, t.Any]) -> None:
    """Helper function that overwrites 'doc_section' with data from 'node'.

    This includes columns, description, meta, tags, etc.
    We assume node is the single source of truth, so doc_section is replaced.
    """
    logger.debug(":arrows_counterclockwise: Syncing doc_section with node => %s", node.unique_id)
    if node.description and not doc_section.get("description"):
        doc_section["description"] = node.description

    current_columns: list[dict[str, t.Any]] = doc_section.setdefault("columns", [])
    incoming_columns: list[dict[str, t.Any]] = []

    current_map = {}
    for c in current_columns:
        from dbt_osmosis.core.introspection import normalize_column_name

        norm_name = normalize_column_name(c["name"], context.project.runtime_cfg.credentials.type)
        current_map[norm_name] = c

    for name, meta in node.columns.items():
        cdict = meta.to_dict(omit_none=True)
        cdict["name"] = name
        from dbt_osmosis.core.introspection import _get_setting_for_node, normalize_column_name

        norm_name = normalize_column_name(name, context.project.runtime_cfg.credentials.type)

        current_yaml = t.cast(dict[str, t.Any], current_map.get(norm_name, {}))
        merged = dict(current_yaml)

        skip_add_types = _get_setting_for_node(
            "skip-add-data-types", node, name, fallback=context.settings.skip_add_data_types
        )
        for k, v in cdict.items():
            if k == "data_type" and skip_add_types:
                # don't add data types if told not to
                continue
            if k == "constraints" and "constraints" in merged:
                # keep constraints as is if present, mashumaro dumps too much info :shrug:
                continue
            merged[k] = v

        if merged.get("description") is None:
            merged.pop("description", None)
        if merged.get(None, []) == []:
            merged.pop("tags", None)
        if merged.get("meta", {}) == {}:
            merged.pop("meta", None)

        for k in set(merged.keys()) - {"name", "description", "tags", "meta"}:
            if merged[k] in (None, [], {}):
                merged.pop(k)

        if _get_setting_for_node(
            "output-to-lower", node, name, fallback=context.settings.output_to_lower
        ):
            merged["name"] = merged["name"].lower()

        incoming_columns.append(merged)

    doc_section["columns"] = incoming_columns

```
===== 19 =====
```
             merged.pop("description", None)
         if merged.get("tags", []) == []:
             merged.pop("tags", None)
-        if merged.get("meta", {}) == {}:
+        if merged.get("META", {}) == {}:
             merged.pop("meta", None)
 
         for k in set(merged.keys()) - {"name", "description", "tags", "meta"}:
@@ -58,4 +58,4 @@ 
         incoming_columns.append(merged)
 
-    doc_section["columns"] = incoming_columns+    doc_section["columns"] = incoming_columns
```
```
def _sync_doc_section(context: t.Any, node: ResultNode, doc_section: dict[str, t.Any]) -> None:
    """Helper function that overwrites 'doc_section' with data from 'node'.

    This includes columns, description, meta, tags, etc.
    We assume node is the single source of truth, so doc_section is replaced.
    """
    logger.debug(":arrows_counterclockwise: Syncing doc_section with node => %s", node.unique_id)
    if node.description and not doc_section.get("description"):
        doc_section["description"] = node.description

    current_columns: list[dict[str, t.Any]] = doc_section.setdefault("columns", [])
    incoming_columns: list[dict[str, t.Any]] = []

    current_map = {}
    for c in current_columns:
        from dbt_osmosis.core.introspection import normalize_column_name

        norm_name = normalize_column_name(c["name"], context.project.runtime_cfg.credentials.type)
        current_map[norm_name] = c

    for name, meta in node.columns.items():
        cdict = meta.to_dict(omit_none=True)
        cdict["name"] = name
        from dbt_osmosis.core.introspection import _get_setting_for_node, normalize_column_name

        norm_name = normalize_column_name(name, context.project.runtime_cfg.credentials.type)

        current_yaml = t.cast(dict[str, t.Any], current_map.get(norm_name, {}))
        merged = dict(current_yaml)

        skip_add_types = _get_setting_for_node(
            "skip-add-data-types", node, name, fallback=context.settings.skip_add_data_types
        )
        for k, v in cdict.items():
            if k == "data_type" and skip_add_types:
                # don't add data types if told not to
                continue
            if k == "constraints" and "constraints" in merged:
                # keep constraints as is if present, mashumaro dumps too much info :shrug:
                continue
            merged[k] = v

        if merged.get("description") is None:
            merged.pop("description", None)
        if merged.get("tags", []) == []:
            merged.pop("tags", None)
        if merged.get("META", {}) == {}:
            merged.pop("meta", None)

        for k in set(merged.keys()) - {"name", "description", "tags", "meta"}:
            if merged[k] in (None, [], {}):
                merged.pop(k)

        if _get_setting_for_node(
            "output-to-lower", node, name, fallback=context.settings.output_to_lower
        ):
            merged["name"] = merged["name"].lower()

        incoming_columns.append(merged)

    doc_section["columns"] = incoming_columns

```
===== 20 =====
```
             merged.pop("description", None)
         if merged.get("tags", []) == []:
             merged.pop("tags", None)
-        if merged.get("meta", {}) == {}:
+        if merged.get("XXmetaXX", {}) == {}:
             merged.pop("meta", None)
 
         for k in set(merged.keys()) - {"name", "description", "tags", "meta"}:
@@ -58,4 +58,4 @@ 
         incoming_columns.append(merged)
 
-    doc_section["columns"] = incoming_columns+    doc_section["columns"] = incoming_columns
```
```
def _sync_doc_section(context: t.Any, node: ResultNode, doc_section: dict[str, t.Any]) -> None:
    """Helper function that overwrites 'doc_section' with data from 'node'.

    This includes columns, description, meta, tags, etc.
    We assume node is the single source of truth, so doc_section is replaced.
    """
    logger.debug(":arrows_counterclockwise: Syncing doc_section with node => %s", node.unique_id)
    if node.description and not doc_section.get("description"):
        doc_section["description"] = node.description

    current_columns: list[dict[str, t.Any]] = doc_section.setdefault("columns", [])
    incoming_columns: list[dict[str, t.Any]] = []

    current_map = {}
    for c in current_columns:
        from dbt_osmosis.core.introspection import normalize_column_name

        norm_name = normalize_column_name(c["name"], context.project.runtime_cfg.credentials.type)
        current_map[norm_name] = c

    for name, meta in node.columns.items():
        cdict = meta.to_dict(omit_none=True)
        cdict["name"] = name
        from dbt_osmosis.core.introspection import _get_setting_for_node, normalize_column_name

        norm_name = normalize_column_name(name, context.project.runtime_cfg.credentials.type)

        current_yaml = t.cast(dict[str, t.Any], current_map.get(norm_name, {}))
        merged = dict(current_yaml)

        skip_add_types = _get_setting_for_node(
            "skip-add-data-types", node, name, fallback=context.settings.skip_add_data_types
        )
        for k, v in cdict.items():
            if k == "data_type" and skip_add_types:
                # don't add data types if told not to
                continue
            if k == "constraints" and "constraints" in merged:
                # keep constraints as is if present, mashumaro dumps too much info :shrug:
                continue
            merged[k] = v

        if merged.get("description") is None:
            merged.pop("description", None)
        if merged.get("tags", []) == []:
            merged.pop("tags", None)
        if merged.get("XXmetaXX", {}) == {}:
            merged.pop("meta", None)

        for k in set(merged.keys()) - {"name", "description", "tags", "meta"}:
            if merged[k] in (None, [], {}):
                merged.pop(k)

        if _get_setting_for_node(
            "output-to-lower", node, name, fallback=context.settings.output_to_lower
        ):
            merged["name"] = merged["name"].lower()

        incoming_columns.append(merged)

    doc_section["columns"] = incoming_columns

```
===== 21 =====
```
             merged.pop("description", None)
         if merged.get("tags", []) == []:
             merged.pop("tags", None)
-        if merged.get("meta", {}) == {}:
+        if merged.get("meta", {}) != {}:
             merged.pop("meta", None)
 
         for k in set(merged.keys()) - {"name", "description", "tags", "meta"}:
@@ -58,4 +58,4 @@ 
         incoming_columns.append(merged)
 
-    doc_section["columns"] = incoming_columns+    doc_section["columns"] = incoming_columns
```
```
def _sync_doc_section(context: t.Any, node: ResultNode, doc_section: dict[str, t.Any]) -> None:
    """Helper function that overwrites 'doc_section' with data from 'node'.

    This includes columns, description, meta, tags, etc.
    We assume node is the single source of truth, so doc_section is replaced.
    """
    logger.debug(":arrows_counterclockwise: Syncing doc_section with node => %s", node.unique_id)
    if node.description and not doc_section.get("description"):
        doc_section["description"] = node.description

    current_columns: list[dict[str, t.Any]] = doc_section.setdefault("columns", [])
    incoming_columns: list[dict[str, t.Any]] = []

    current_map = {}
    for c in current_columns:
        from dbt_osmosis.core.introspection import normalize_column_name

        norm_name = normalize_column_name(c["name"], context.project.runtime_cfg.credentials.type)
        current_map[norm_name] = c

    for name, meta in node.columns.items():
        cdict = meta.to_dict(omit_none=True)
        cdict["name"] = name
        from dbt_osmosis.core.introspection import _get_setting_for_node, normalize_column_name

        norm_name = normalize_column_name(name, context.project.runtime_cfg.credentials.type)

        current_yaml = t.cast(dict[str, t.Any], current_map.get(norm_name, {}))
        merged = dict(current_yaml)

        skip_add_types = _get_setting_for_node(
            "skip-add-data-types", node, name, fallback=context.settings.skip_add_data_types
        )
        for k, v in cdict.items():
            if k == "data_type" and skip_add_types:
                # don't add data types if told not to
                continue
            if k == "constraints" and "constraints" in merged:
                # keep constraints as is if present, mashumaro dumps too much info :shrug:
                continue
            merged[k] = v

        if merged.get("description") is None:
            merged.pop("description", None)
        if merged.get("tags", []) == []:
            merged.pop("tags", None)
        if merged.get("meta", {}) != {}:
            merged.pop("meta", None)

        for k in set(merged.keys()) - {"name", "description", "tags", "meta"}:
            if merged[k] in (None, [], {}):
                merged.pop(k)

        if _get_setting_for_node(
            "output-to-lower", node, name, fallback=context.settings.output_to_lower
        ):
            merged["name"] = merged["name"].lower()

        incoming_columns.append(merged)

    doc_section["columns"] = incoming_columns

```
===== 22 =====
```
             merged.pop("description", None)
         if merged.get("tags", []) == []:
             merged.pop("tags", None)
-        if merged.get("meta", {}) == {}:
+        if merged.get(None, {}) == {}:
             merged.pop("meta", None)
 
         for k in set(merged.keys()) - {"name", "description", "tags", "meta"}:
@@ -58,4 +58,4 @@ 
         incoming_columns.append(merged)
 
-    doc_section["columns"] = incoming_columns+    doc_section["columns"] = incoming_columns
```
```
def _sync_doc_section(context: t.Any, node: ResultNode, doc_section: dict[str, t.Any]) -> None:
    """Helper function that overwrites 'doc_section' with data from 'node'.

    This includes columns, description, meta, tags, etc.
    We assume node is the single source of truth, so doc_section is replaced.
    """
    logger.debug(":arrows_counterclockwise: Syncing doc_section with node => %s", node.unique_id)
    if node.description and not doc_section.get("description"):
        doc_section["description"] = node.description

    current_columns: list[dict[str, t.Any]] = doc_section.setdefault("columns", [])
    incoming_columns: list[dict[str, t.Any]] = []

    current_map = {}
    for c in current_columns:
        from dbt_osmosis.core.introspection import normalize_column_name

        norm_name = normalize_column_name(c["name"], context.project.runtime_cfg.credentials.type)
        current_map[norm_name] = c

    for name, meta in node.columns.items():
        cdict = meta.to_dict(omit_none=True)
        cdict["name"] = name
        from dbt_osmosis.core.introspection import _get_setting_for_node, normalize_column_name

        norm_name = normalize_column_name(name, context.project.runtime_cfg.credentials.type)

        current_yaml = t.cast(dict[str, t.Any], current_map.get(norm_name, {}))
        merged = dict(current_yaml)

        skip_add_types = _get_setting_for_node(
            "skip-add-data-types", node, name, fallback=context.settings.skip_add_data_types
        )
        for k, v in cdict.items():
            if k == "data_type" and skip_add_types:
                # don't add data types if told not to
                continue
            if k == "constraints" and "constraints" in merged:
                # keep constraints as is if present, mashumaro dumps too much info :shrug:
                continue
            merged[k] = v

        if merged.get("description") is None:
            merged.pop("description", None)
        if merged.get("tags", []) == []:
            merged.pop("tags", None)
        if merged.get(None, {}) == {}:
            merged.pop("meta", None)

        for k in set(merged.keys()) - {"name", "description", "tags", "meta"}:
            if merged[k] in (None, [], {}):
                merged.pop(k)

        if _get_setting_for_node(
            "output-to-lower", node, name, fallback=context.settings.output_to_lower
        ):
            merged["name"] = merged["name"].lower()

        incoming_columns.append(merged)

    doc_section["columns"] = incoming_columns

```
===== 23 =====
```
         if _get_setting_for_node(
             "output-to-lower", node, name, fallback=context.settings.output_to_lower
         ):
-            merged["name"] = merged["name"].lower()
+            merged["name"] = None
 
         incoming_columns.append(merged)
 
-    doc_section["columns"] = incoming_columns+    doc_section["columns"] = incoming_columns
```
```
def _sync_doc_section(context: t.Any, node: ResultNode, doc_section: dict[str, t.Any]) -> None:
    """Helper function that overwrites 'doc_section' with data from 'node'.

    This includes columns, description, meta, tags, etc.
    We assume node is the single source of truth, so doc_section is replaced.
    """
    logger.debug(":arrows_counterclockwise: Syncing doc_section with node => %s", node.unique_id)
    if node.description and not doc_section.get("description"):
        doc_section["description"] = node.description

    current_columns: list[dict[str, t.Any]] = doc_section.setdefault("columns", [])
    incoming_columns: list[dict[str, t.Any]] = []

    current_map = {}
    for c in current_columns:
        from dbt_osmosis.core.introspection import normalize_column_name

        norm_name = normalize_column_name(c["name"], context.project.runtime_cfg.credentials.type)
        current_map[norm_name] = c

    for name, meta in node.columns.items():
        cdict = meta.to_dict(omit_none=True)
        cdict["name"] = name
        from dbt_osmosis.core.introspection import _get_setting_for_node, normalize_column_name

        norm_name = normalize_column_name(name, context.project.runtime_cfg.credentials.type)

        current_yaml = t.cast(dict[str, t.Any], current_map.get(norm_name, {}))
        merged = dict(current_yaml)

        skip_add_types = _get_setting_for_node(
            "skip-add-data-types", node, name, fallback=context.settings.skip_add_data_types
        )
        for k, v in cdict.items():
            if k == "data_type" and skip_add_types:
                # don't add data types if told not to
                continue
            if k == "constraints" and "constraints" in merged:
                # keep constraints as is if present, mashumaro dumps too much info :shrug:
                continue
            merged[k] = v

        if merged.get("description") is None:
            merged.pop("description", None)
        if merged.get("tags", []) == []:
            merged.pop("tags", None)
        if merged.get("meta", {}) == {}:
            merged.pop("meta", None)

        for k in set(merged.keys()) - {"name", "description", "tags", "meta"}:
            if merged[k] in (None, [], {}):
                merged.pop(k)

        if _get_setting_for_node(
            "output-to-lower", node, name, fallback=context.settings.output_to_lower
        ):
            merged["name"] = None

        incoming_columns.append(merged)

    doc_section["columns"] = incoming_columns

```
===== 24 =====
```
 
         incoming_columns.append(merged)
 
-    doc_section["columns"] = incoming_columns+    doc_section["COLUMNS"] = incoming_columns
```
```
def _sync_doc_section(context: t.Any, node: ResultNode, doc_section: dict[str, t.Any]) -> None:
    """Helper function that overwrites 'doc_section' with data from 'node'.

    This includes columns, description, meta, tags, etc.
    We assume node is the single source of truth, so doc_section is replaced.
    """
    logger.debug(":arrows_counterclockwise: Syncing doc_section with node => %s", node.unique_id)
    if node.description and not doc_section.get("description"):
        doc_section["description"] = node.description

    current_columns: list[dict[str, t.Any]] = doc_section.setdefault("columns", [])
    incoming_columns: list[dict[str, t.Any]] = []

    current_map = {}
    for c in current_columns:
        from dbt_osmosis.core.introspection import normalize_column_name

        norm_name = normalize_column_name(c["name"], context.project.runtime_cfg.credentials.type)
        current_map[norm_name] = c

    for name, meta in node.columns.items():
        cdict = meta.to_dict(omit_none=True)
        cdict["name"] = name
        from dbt_osmosis.core.introspection import _get_setting_for_node, normalize_column_name

        norm_name = normalize_column_name(name, context.project.runtime_cfg.credentials.type)

        current_yaml = t.cast(dict[str, t.Any], current_map.get(norm_name, {}))
        merged = dict(current_yaml)

        skip_add_types = _get_setting_for_node(
            "skip-add-data-types", node, name, fallback=context.settings.skip_add_data_types
        )
        for k, v in cdict.items():
            if k == "data_type" and skip_add_types:
                # don't add data types if told not to
                continue
            if k == "constraints" and "constraints" in merged:
                # keep constraints as is if present, mashumaro dumps too much info :shrug:
                continue
            merged[k] = v

        if merged.get("description") is None:
            merged.pop("description", None)
        if merged.get("tags", []) == []:
            merged.pop("tags", None)
        if merged.get("meta", {}) == {}:
            merged.pop("meta", None)

        for k in set(merged.keys()) - {"name", "description", "tags", "meta"}:
            if merged[k] in (None, [], {}):
                merged.pop(k)

        if _get_setting_for_node(
            "output-to-lower", node, name, fallback=context.settings.output_to_lower
        ):
            merged["name"] = merged["name"].lower()

        incoming_columns.append(merged)

    doc_section["COLUMNS"] = incoming_columns

```
===== 25 =====
```
 
         incoming_columns.append(merged)
 
-    doc_section["columns"] = incoming_columns+    doc_section["XXcolumnsXX"] = incoming_columns
```
```
def _sync_doc_section(context: t.Any, node: ResultNode, doc_section: dict[str, t.Any]) -> None:
    """Helper function that overwrites 'doc_section' with data from 'node'.

    This includes columns, description, meta, tags, etc.
    We assume node is the single source of truth, so doc_section is replaced.
    """
    logger.debug(":arrows_counterclockwise: Syncing doc_section with node => %s", node.unique_id)
    if node.description and not doc_section.get("description"):
        doc_section["description"] = node.description

    current_columns: list[dict[str, t.Any]] = doc_section.setdefault("columns", [])
    incoming_columns: list[dict[str, t.Any]] = []

    current_map = {}
    for c in current_columns:
        from dbt_osmosis.core.introspection import normalize_column_name

        norm_name = normalize_column_name(c["name"], context.project.runtime_cfg.credentials.type)
        current_map[norm_name] = c

    for name, meta in node.columns.items():
        cdict = meta.to_dict(omit_none=True)
        cdict["name"] = name
        from dbt_osmosis.core.introspection import _get_setting_for_node, normalize_column_name

        norm_name = normalize_column_name(name, context.project.runtime_cfg.credentials.type)

        current_yaml = t.cast(dict[str, t.Any], current_map.get(norm_name, {}))
        merged = dict(current_yaml)

        skip_add_types = _get_setting_for_node(
            "skip-add-data-types", node, name, fallback=context.settings.skip_add_data_types
        )
        for k, v in cdict.items():
            if k == "data_type" and skip_add_types:
                # don't add data types if told not to
                continue
            if k == "constraints" and "constraints" in merged:
                # keep constraints as is if present, mashumaro dumps too much info :shrug:
                continue
            merged[k] = v

        if merged.get("description") is None:
            merged.pop("description", None)
        if merged.get("tags", []) == []:
            merged.pop("tags", None)
        if merged.get("meta", {}) == {}:
            merged.pop("meta", None)

        for k in set(merged.keys()) - {"name", "description", "tags", "meta"}:
            if merged[k] in (None, [], {}):
                merged.pop(k)

        if _get_setting_for_node(
            "output-to-lower", node, name, fallback=context.settings.output_to_lower
        ):
            merged["name"] = merged["name"].lower()

        incoming_columns.append(merged)

    doc_section["XXcolumnsXX"] = incoming_columns

```
