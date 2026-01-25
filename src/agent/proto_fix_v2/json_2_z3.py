import json
from typing import Any, Dict, List, Tuple, Set


class HornIRCompileError(Exception):
    pass


def compile_horn_ir_to_z3py_sections(ir: Dict[str, Any]) -> Tuple[str, str]:
    """
    Compile the Horn-IR JSON object (as Python dict) into two strings:
      (decls_str, rules_str)
    that fit exactly into:
      BEGIN_DECLS ... END_DECLS
      BEGIN_RULES ... END_RULES

    Assumptions about the harness:
    - `from z3 import *` (or equivalent) is already available.
    - `fp` is a z3.Fixedpoint instance.
    - `Bad = Function("Bad", BoolSort())` and `fp.register_relation(Bad)` already exist.
    """

    # --------------------------
    # Validate top-level schema
    # --------------------------
    if not isinstance(ir, dict):
        raise HornIRCompileError("IR must be a JSON object (dict).")
    relations = ir.get("relations")
    vars_ = ir.get("vars")
    rules = ir.get("rules")

    if not isinstance(relations, list) or not isinstance(vars_, list) or not isinstance(rules, list):
        raise HornIRCompileError("IR must contain 'relations' (list), 'vars' (list), 'rules' (list).")

    # Disallow redefining Bad as a relation
    for r in relations:
        if r.get("name") == "Bad":
            raise HornIRCompileError("Do NOT include 'Bad' in relations; harness defines it.")

    # Must have Final relation
    if "Final" not in {r.get("name") for r in relations}:
        raise HornIRCompileError("Missing required relation named 'Final'.")

    # Rule list must end with Bad head
    if len(rules) == 0:
        raise HornIRCompileError("No rules provided.")
    last_head = rules[-1].get("head", {})
    if last_head.get("rel") != "Bad" or last_head.get("args") != []:
        raise HornIRCompileError("Last rule must have head rel='Bad' with args=[].")

    # --------------------------
    # Sort helpers
    # --------------------------
    def sort_to_z3(sort_name: str) -> str:
        if sort_name == "Int":
            return "IntSort()"
        if sort_name == "Bool":
            return "BoolSort()"
        raise HornIRCompileError(f"Unsupported sort: {sort_name}. Use only 'Int' or 'Bool'.")

    def var_decl(sort_name: str, var_name: str) -> str:
        if sort_name == "Int":
            return f'{var_name} = Int("{var_name}")'
        if sort_name == "Bool":
            return f'{var_name} = Bool("{var_name}")'
        raise HornIRCompileError(f"Unsupported var sort: {sort_name}.")

    # --------------------------
    # Collect relation signatures
    # --------------------------
    rel_sigs: Dict[str, List[str]] = {}  # name -> list of arg sort strings ("Int"/"Bool")
    for r in relations:
        name = r.get("name")
        args = r.get("args")
        if not isinstance(name, str) or not isinstance(args, list):
            raise HornIRCompileError("Each relation needs {name:str, args:list}.")
        if name in rel_sigs:
            raise HornIRCompileError(f"Duplicate relation name: {name}")
        arg_sorts: List[str] = []
        for a in args:
            if not isinstance(a, dict) or "sort" not in a:
                raise HornIRCompileError(f"Relation {name} arg must be dict with 'sort'.")
            s = a["sort"]
            if s not in ("Int", "Bool"):
                raise HornIRCompileError(f"Relation {name} uses unsupported sort: {s}")
            arg_sorts.append(s)
        rel_sigs[name] = arg_sorts

    # --------------------------
    # Collect variables
    # --------------------------
    var_sorts: Dict[str, str] = {}
    for v in vars_:
        if not isinstance(v, dict):
            raise HornIRCompileError("Each var must be an object {name, sort}.")
        n = v.get("name")
        s = v.get("sort")
        if not isinstance(n, str) or s not in ("Int", "Bool"):
            raise HornIRCompileError("Var entries must have 'name' (str) and 'sort' in {'Int','Bool'}.")
        if n in var_sorts and var_sorts[n] != s:
            raise HornIRCompileError(f"Variable {n} declared with conflicting sorts.")
        var_sorts[n] = s

    # --------------------------
    # Expression compiler
    # --------------------------
    def compile_term(t: Any) -> str:
        # term: {"var":"x"} | {"int":0} | {"bool":True} | {"op":...}
        if isinstance(t, dict):
            if "var" in t:
                vn = t["var"]
                if vn not in var_sorts:
                    raise HornIRCompileError(f"Undeclared variable used: {vn}")
                return vn
            if "int" in t:
                val = t["int"]
                if not isinstance(val, int):
                    raise HornIRCompileError("int literal must be an integer.")
                return f"IntVal({val})"
            if "bool" in t:
                val = t["bool"]
                if not isinstance(val, bool):
                    raise HornIRCompileError("bool literal must be True/False.")
                return f"BoolVal({str(val)})"
            if "op" in t:
                return compile_expr(t)
        raise HornIRCompileError(f"Invalid term: {t}")

    def compile_pred_app(pred_obj: Dict[str, Any]) -> str:
        rel = pred_obj.get("rel")
        args = pred_obj.get("args")
        if rel == "Bad":
            # Only allow Bad() in head ideally, but if it appears in body, still 0-arity.
            if args != []:
                raise HornIRCompileError("Bad predicate must have 0 args.")
            return "Bad()"
        if rel not in rel_sigs:
            raise HornIRCompileError(f"Predicate uses unknown relation: {rel}")
        if not isinstance(args, list):
            raise HornIRCompileError("Predicate 'args' must be a list.")
        expected = rel_sigs[rel]
        if len(args) != len(expected):
            raise HornIRCompileError(
                f"Arity mismatch for {rel}: expected {len(expected)} args, got {len(args)}"
            )
        compiled_args = [compile_term(a) for a in args]
        return f"{rel}({', '.join(compiled_args)})"

    def compile_atom(a: Any) -> str:
        # atom: {"pred": {...}} OR expression object (op/var/int/bool)
        if isinstance(a, dict) and "pred" in a:
            if not isinstance(a["pred"], dict):
                raise HornIRCompileError("pred must be an object.")
            return compile_pred_app(a["pred"])
        # otherwise treat as expression
        return compile_expr(a)

    def compile_expr(e: Any) -> str:
        if isinstance(e, dict):
            if "pred" in e:
                return compile_atom(e)
            if "var" in e or "int" in e or "bool" in e:
                return compile_term(e)
            op = e.get("op")
            args = e.get("args", [])
            if not isinstance(op, str) or not isinstance(args, list):
                raise HornIRCompileError(f"Expression must have 'op' (str) and 'args' (list): {e}")

            # N-ary Bool ops
            if op in ("And", "Or"):
                if len(args) == 0:
                    return "True" if op == "And" else "False"
                compiled = [compile_atom(x) for x in args]
                return f"{op}({', '.join(compiled)})"

            # Unary
            if op == "Not":
                if len(args) != 1:
                    raise HornIRCompileError("Not expects 1 arg.")
                return f"Not({compile_atom(args[0])})"

            # Binary Bool connectives
            if op == "Implies":
                if len(args) != 2:
                    raise HornIRCompileError("Implies expects 2 args.")
                return f"Implies({compile_atom(args[0])}, {compile_atom(args[1])})"

            # Comparisons
            if op in ("Eq", "Ne", "Lt", "Le", "Gt", "Ge"):
                if len(args) != 2:
                    raise HornIRCompileError(f"{op} expects 2 args.")
                a1 = compile_term(args[0])
                a2 = compile_term(args[1])
                z3op = {
                    "Eq": "==",
                    "Ne": "!=",
                    "Lt": "<",
                    "Le": "<=",
                    "Gt": ">",
                    "Ge": ">=",
                }[op]
                return f"({a1} {z3op} {a2})"

            # Integer arithmetic
            if op in ("Add", "Sub", "Mul"):
                if len(args) < 2:
                    raise HornIRCompileError(f"{op} expects at least 2 args.")
                compiled = [compile_term(x) for x in args]
                sym = {"Add": "+", "Sub": "-", "Mul": "*"}[op]
                # Left-associative chaining
                expr = compiled[0]
                for part in compiled[1:]:
                    expr = f"({expr} {sym} {part})"
                return expr

            # If-then-else (term-y)
            if op == "Ite":
                if len(args) != 3:
                    raise HornIRCompileError("Ite expects 3 args: cond, then, else.")
                c = compile_atom(args[0])
                t_ = compile_term(args[1])
                f_ = compile_term(args[2])
                return f"If({c}, {t_}, {f_})"

        raise HornIRCompileError(f"Invalid expression: {e}")

    # --------------------------
    # Compile DECLS
    # --------------------------
    decl_lines: List[str] = []

    # relations
    for rel_name, arg_sorts in rel_sigs.items():
        z3_sorts = [sort_to_z3(s) for s in arg_sorts] + ["BoolSort()"]
        decl_lines.append(f'{rel_name} = Function("{rel_name}", {", ".join(z3_sorts)})')

    # register relations
    for rel_name in rel_sigs.keys():
        decl_lines.append(f"fp.register_relation({rel_name})")

    # variables
    # We only declare variables listed in var_sorts. (You may list extras; it's fine.)
    for vn, s in var_sorts.items():
        decl_lines.append(var_decl(s, vn))

    # declare_var
    if len(var_sorts) > 0:
        decl_lines.append(f"fp.declare_var({', '.join(var_sorts.keys())})")

    # --------------------------
    # Compile RULES
    # --------------------------
    rule_lines: List[str] = []

    for idx, rule in enumerate(rules):
        head = rule.get("head")
        body = rule.get("body", [])
        if not isinstance(head, dict) or "rel" not in head or "args" not in head:
            raise HornIRCompileError("Each rule must have 'head' with {rel, args}.")
        if not isinstance(body, list):
            raise HornIRCompileError("Each rule body must be a list (can be empty).")

        head_rel = head.get("rel")
        head_args = head.get("args")

        # compile head predicate
        if head_rel == "Bad":
            if head_args != []:
                raise HornIRCompileError("Bad head must have args=[].")
            head_str = "Bad()"
        else:
            head_str = compile_pred_app({"rel": head_rel, "args": head_args})

        # compile body
        if len(body) == 0:
            body_str = "True"
        elif len(body) == 1:
            body_str = compile_atom(body[0])
        else:
            compiled_atoms = [compile_atom(a) for a in body]
            body_str = f"And({', '.join(compiled_atoms)})"

        rule_lines.append(f"fp.rule({head_str}, {body_str})")

    decls_str = "\n".join(decl_lines)
    rules_str = "\n".join(rule_lines)
    return decls_str, rules_str


def compile_json_text_to_sections(json_text: str) -> Tuple[str, str]:
    """
    Convenience wrapper: parse JSON text then compile.
    """
    ir = json.loads(json_text)
    return compile_horn_ir_to_z3py_sections(ir)


# Example usage (for your integration/testing):
if __name__ == "__main__":
    example_ir = {
  "relations": [
    { "name": "Init",  "args": [ {"name":"node_is_none","sort":"Bool"} ] },
    { "name": "Final", "args": [ {"name":"result_eq_fallback","sort":"Bool"}, {"name":"node_is_none","sort":"Bool"} ] }
  ],
  "vars": [
    {"name": "node_is_none", "sort": "Bool"},
    {"name": "result_eq_fallback", "sort": "Bool"}
  ],
  "rules": [
    {
      "head": { "rel": "Init", "args": [ {"var": "node_is_none"} ] },
      "body": []
    },
    {
      "head": { "rel": "Final", "args": [ {"var": "result_eq_fallback"}, {"var": "node_is_none"} ] },
      "body": [
        { "pred": { "rel": "Init", "args": [ {"var": "node_is_none"} ] } },
        {
          "op": "Implies",
          "args": [
            { "op": "Eq", "args": [ { "var": "node_is_none" }, { "bool": True } ] },
            { "op": "Eq", "args": [ { "var": "result_eq_fallback" }, { "bool": True } ] }
          ]
        }
      ]
    },
    {
      "head": { "rel": "Bad", "args": [] },
      "body": [
        { "pred": { "rel": "Final", "args": [ {"var": "result_eq_fallback"}, {"var": "node_is_none"} ] }},
        { "op": "Eq", "args": [ {"var": "node_is_none"}, {"bool": True} ] },
        { "op": "Ne", "args": [ {"var": "result_eq_fallback"}, {"bool": True} ] }
      ]
    }
  ]
}


    decls, rules = compile_horn_ir_to_z3py_sections(example_ir)
    print("BEGIN_DECLS")
    print(decls)
    print("END_DECLS\n")
    print("BEGIN_RULES")
    print(rules)
    print("END_RULES")
