https://github.com/z3z1ma/dbt-osmosis/blob/cd453ea69e9473e45df5390d8bb2a41e201dd4ee/./src/dbt_osmosis/core/introspection.py#L83-L159
```
@icontract.ensure(lambda result, node, col, fallback: node is not None or col is None or result == fallback, 
                  "If node is None but column name is provided, result must be fallback since column metadata requires a node")
@icontract.ensure(lambda result, fallback: fallback is None or result is not None or fallback is None,
                  "Result is either found value or fallback value")
```
```
return value - 3rd party type


return value content

3rd party type
```
passed
```
@icontract.snapshot(lambda opt: opt.replace("_", "-"), name="k")
@icontract.snapshot(lambda opt: opt.replace("-", "_"), name="identifier")
@icontract.snapshot(lambda node: None if node is None else node, name="node")
@icontract.snapshot(lambda fallback: fallback, name="fallback")
@icontract.snapshot(
    lambda opt, node, col: (
        []
        if node is None
        else (
            [
                node.meta,
                node.meta.get("dbt-osmosis-options", {}),
                node.meta.get("dbt_osmosis_options", {}),
                node.config.extra,
                node.config.extra.get("dbt-osmosis-options", {}),
                node.config.extra.get("dbt_osmosis_options", {}),
            ]
        )
    ),
    name="sources",
)
@icontract.snapshot(lambda node: None if node is None else (node.config.extra if hasattr(node, "config") else None), name="node_config_extra")
@icontract.ensure(
    lambda result, OLD: (
        # If node was None, function must return the provided fallback
        (OLD.node is None and result == OLD.fallback)
        or
        # Otherwise the result must equal the first matching value found (by original precedence),
        # or be the fallback when no matching keys exist.
        (
            OLD.node is not None
            and (
                (lambda sources, node_conf, k, identifier, fallback:
                    next(
                        (
                            val
                            for s in sources
                            for val in [
                                # first check the explicit "dbt-osmosis-<k>" variation
                                s.get(f"dbt-osmosis-{k}")
                                # then the "dbt_osmosis_<identifier>" variation
                                or s.get(f"dbt_osmosis_{identifier}")
                                # then, only for sources that are NOT node.config.extra, check plain k and identifier
                                or (s.get(k) if s is not node_conf else None)
                                or (s.get(identifier) if s is not node_conf else None)
                            ]
                            if val is not None
                        ),
                        fallback,
                    )
                )(OLD.sources, OLD.node_config_extra, OLD.k, OLD.identifier, OLD.fallback)
                == result
            )
        )
    )
)
```
===== 2: failed =====
```
     k, identifier = opt.replace("_", "-"), opt.replace("-", "_")
     sources = [
         node.meta,
-        node.meta.get("dbt-osmosis-options", {}),
+        node.meta.get("XXdbt-osmosis-optionsXX", {}),
         node.meta.get("dbt_osmosis_options", {}),
         node.config.extra,
         node.config.extra.get("dbt-osmosis-options", {}),
@@ -74,4 +74,4 @@                 return source[k]
             if identifier in source:
                 return source[identifier]
-    return fallback+    return fallback
```
```
def _get_setting_for_node(
    opt: str,
    /,
    node: ResultNode | None = None,
    col: str | None = None,
    *,
    fallback: t.Any | None = None,
) -> t.Any:
    """Get a configuration value for a dbt node from the node's meta and config.

    models: # dbt_project
      project:
        staging:
          +dbt-osmosis: path/spec.yml
          +dbt-osmosis-options:
            string-length: true
            numeric-precision-and-scale: true
            skip-add-columns: true
          +dbt-osmosis-skip-add-tags: true

    models: # schema
      - name: foo
        meta:
          string-length: false
          prefix: user_ # we strip this prefix to inherit from columns upstream, useful in staging models that prefix everything
        columns:
          - bar:
            meta:
              dbt-osmosis-skip-meta-merge: true # per-column options
              dbt-osmosis-options:
                output-to-lower: true

    {{ config(..., dbt_osmosis_options={"prefix": "account_"}) }} -- sql

    We check for
    From node column meta
    - <key>
    - dbt-osmosis-<key>
    - dbt-osmosis-options.<key>
    From node meta
    - <key>
    - dbt-osmosis-<key>
    - dbt-osmosis-options.<key>
    From node config
    - dbt-osmosis-<key>
    - dbt-osmosis-options.<key>
    - dbt_osmosis_<key> # allows use in {{ config(...) }} by being a valid python identifier
    - dbt_osmosis_options.<key> # allows use in {{ config(...) }} by being a valid python identifier
    """
    if node is None:
        return fallback
    k, identifier = opt.replace("_", "-"), opt.replace("-", "_")
    sources = [
        node.meta,
        node.meta.get("XXdbt-osmosis-optionsXX", {}),
        node.meta.get("dbt_osmosis_options", {}),
        node.config.extra,
        node.config.extra.get("dbt-osmosis-options", {}),
        node.config.extra.get("dbt_osmosis_options", {}),
    ]
    if col and (column := node.columns.get(col)):
        sources = [
            column.meta,
            column.meta.get("dbt-osmosis-options", {}),
            column.meta.get("dbt_osmosis_options", {}),
            *sources,
        ]
    for source in sources:
        for variation in (f"dbt-osmosis-{k}", f"dbt_osmosis_{identifier}"):
            if variation in source:
                return source[variation]
        if source is not node.config.extra:
            if k in source:
                return source[k]
            if identifier in source:
                return source[identifier]
    return fallback

```
