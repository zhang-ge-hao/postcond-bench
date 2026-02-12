import inspect
import random
import coverage


# ===== method metadata start =====
src_path = "src/agent/proto_v4/_cov_demo/something.py"
func_start = 2
func_end = 12
# ===== method metadata end =====

# ===== construct_inputs_and_run start =====
def construct_inputs_and_run():
    from src.agent.proto_v4._cov_demo.something import func
    func(1, 2)
    func(-1, -2)
# ===== construct_inputs_and_run end =====

def line_coverage_for_range(
    cov: coverage.Coverage,
    filename: str,
    start: int,
    end: int,
    src_lines: list[str],
    uncovered_tag: str = "UNCOVERED",
):
    _, statements, _, missing, _ = cov.analysis2(filename)

    statements_set = set(statements)
    missing_set = set(missing)

    stmts_in_range = [ln for ln in statements if start <= ln <= end]
    missing_in_range = [ln for ln in missing if start <= ln <= end]
    covered_in_range = [ln for ln in stmts_in_range if ln not in set(missing_in_range)]

    total = len(stmts_in_range)
    covered = len(covered_in_range)
    rate = (covered / total) if total else 1.0

    report = {
        "start": start,
        "end": end,
        "total_statements": total,
        "covered_statements": covered,
        "rate": rate,
        "covered_lines": covered_in_range,
        "missing_lines": missing_in_range,
    }
    out_lines = [
        f"Total Statements: {total}",
        f"Covered Statements: {covered}",
        f"Code Coverage: {rate}"
    ]
    for lineno in range(start, end + 1):
        idx = lineno - 1
        code = src_lines[idx] if 0 <= idx < len(src_lines) else ""
        if (lineno in statements_set) and (lineno in missing_set):
            if code.strip() == "":
                annotated = code
            else:
                annotated = f"{code}  # {uncovered_tag}"
        else:
            annotated = code

        out_lines.append(f"{lineno:4d}: {annotated}")

    annotated_code_str = "\n".join(out_lines)

    return report, annotated_code_str


if __name__ == "__main__":
    random.seed(0)

    with open(src_path) as file:
        src_file = file.read()
    src_lines = src_file.split("\n")

    cov = coverage.Coverage(
        branch=False,
        include=[src_path],
    )

    cov.start()
    construct_inputs_and_run()
    cov.stop()
    cov.save()

    func_report, annotated = line_coverage_for_range(
        cov, src_path, start=func_start, end=func_end, src_lines=src_lines
    )

    # print("\n=== func line coverage ===")
    # print(func_report)

    # print("\n=== func code (annotated) ===")
    print(annotated)