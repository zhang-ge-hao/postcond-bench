# z3_fixedpoint_harness.py
from z3 import *

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
    # === LLM_END_DECLS ===

    # === LLM_BEGIN_RULES ===
    # LLM must:
    # - add fp.rule(...) clauses for:
    #   * initialization / entry state(s)
    #   * transition rules (loop body, branches, recursion)
    #   * normal-return final state(s)
    # - add fp.rule(Bad(), <negated-postcondition at final state>)  # the query target
    # Place ONLY valid Python (z3py) statements here.
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
