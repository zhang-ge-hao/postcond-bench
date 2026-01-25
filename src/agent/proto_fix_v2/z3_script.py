# z3_fixedpoint_harness.py
from z3 import *


# icontract.snapshot(lambda node: node.meta if node is not None else {}, name="node_meta")
# icontract.snapshot(lambda node: node.config.extra if node is not None else {}, name="node_config_extra")
# icontract.ensure(
#     lambda result, node, opt, fallback, OLD: 
#         (node is not None and result == fallback and not any(
#             opt.replace("_", "-") in source or 
#             opt.replace("-", "_") in source or 
#             f"dbt-osmosis-{opt.replace('_', '-')}" in source or 
#             f"dbt_osmosis_{opt.replace('-', '_')}" in source 
#             for source in [OLD.node_meta, OLD.node_config_extra]
#         ))
# )

# def _get_setting_for_node(
#     opt: str,
#     /,
#     node: ResultNode | None = None,
#     col: str | None = None,
#     *,
#     fallback: t.Any | None = None,
# ) -> t.Any:
#     """Get a configuration value for a dbt node from the node's meta and config.

#     models: # dbt_project
#       project:
#         staging:
#           +dbt-osmosis: path/spec.yml
#           +dbt-osmosis-options:
#             string-length: true
#             numeric-precision-and-scale: true
#             skip-add-columns: true
#           +dbt-osmosis-skip-add-tags: true

#     models: # schema
#       - name: foo
#         meta:
#           string-length: false
#           prefix: user_ # we strip this prefix to inherit from columns upstream, useful in staging models that prefix everything
#         columns:
#           - bar:
#             meta:
#               dbt-osmosis-skip-meta-merge: true # per-column options
#               dbt-osmosis-options:
#                 output-to-lower: true

#     {{ config(..., dbt_osmosis_options={"prefix": "account_"}) }} -- sql

#     We check for
#     From node column meta
#     - <key>
#     - dbt-osmosis-<key>
#     - dbt-osmosis-options.<key>
#     From node meta
#     - <key>
#     - dbt-osmosis-<key>
#     - dbt-osmosis-options.<key>
#     From node config
#     - dbt-osmosis-<key>
#     - dbt-osmosis-options.<key>
#     - dbt_osmosis_<key> # allows use in {{ config(...) }} by being a valid python identifier
#     - dbt_osmosis_options.<key> # allows use in {{ config(...) }} by being a valid python identifier
#     """
#     if node is None:
#         return fallback
#     k, identifier = opt.replace("_", "-"), opt.replace("-", "_")
#     sources = [
#         node.meta,
#         node.meta.get("dbt-osmosis-options", {}),
#         node.meta.get("dbt_osmosis_options", {}),
#         node.config.extra,
#         node.config.extra.get("dbt-osmosis-options", {}),
#         node.config.extra.get("dbt_osmosis_options", {}),
#     ]
#     if col and (column := node.columns.get(col)):
#         sources = [
#             column.meta,
#             column.meta.get("dbt-osmosis-options", {}),
#             column.meta.get("dbt_osmosis_options", {}),
#             *sources,
#         ]
#     for source in sources:
#         for variation in (f"dbt-osmosis-{k}", f"dbt_osmosis_{identifier}"):
#             if variation in source:
#                 return source[variation]
#         if source is not node.config.extra:
#             if k in source:
#                 return source[k]
#             if identifier in source:
#                 return source[identifier]
#     return fallback


def run_check():
    fp = Fixedpoint()
    fp.set(engine="spacer")

    # ---- Standard relations (you may add more in LLM block if needed) ----
    # Bad() must exist and mean: "there exists a counterexample run"
    Bad = Function("Bad", BoolSort())
    fp.register_relation(Bad)

    # === LLM_BEGIN_DECLS ===
    # LLM must:
    # - declare additional relations (Function(...BoolSort()))
    # - register them via fp.register_relation(...)
    # - declare rule variables via fp.declare_var(...)
    # - declare any helper uninterpreted functions (e.g., A(i) for arrays) if needed
    # Place ONLY valid Python (z3py) statements here.

    Init = Function("Init", BoolSort(), BoolSort())
    Final = Function("Final", BoolSort(), BoolSort(), BoolSort())
    fp.register_relation(Init)
    fp.register_relation(Final)
    node_is_none = Bool("node_is_none")
    result_eq_fallback = Bool("result_eq_fallback")
    fp.declare_var(node_is_none, result_eq_fallback)

    # === LLM_END_DECLS ===

    # === LLM_BEGIN_RULES ===
    # LLM must:
    # - add fp.rule(...) clauses for:
    #   * initialization / entry state(s)
    #   * transition rules (loop body, branches, recursion)
    #   * normal-return final state(s)
    # - add fp.rule(Bad(), <negated-postcondition at final state>)  # the query target
    # Place ONLY valid Python (z3py) statements here.

    fp.rule(Init(node_is_none), True)
    fp.rule(Final(result_eq_fallback, node_is_none), And(Init(node_is_none), Implies((node_is_none == BoolVal(True)), (result_eq_fallback == BoolVal(True)))))
    fp.rule(Bad(), And(Final(result_eq_fallback, node_is_none), (node_is_none == BoolVal(True)), (result_eq_fallback != BoolVal(True))))

    # === LLM_END_RULES ===

    # ---- Query ----
    res = fp.query(Bad())
    print("Query(Bad()) =", res)
    if res == sat:
        print("SAT: counterexample exists")
        print(fp.get_answer())
    elif res == unsat:
        print("UNSAT: postcondition holds (under encoded assumptions/model)")
    else:
        print("UNKNOWN")
        try:
            print(fp.get_answer())
        except Exception:
            pass

if __name__ == "__main__":
    run_check()
