from collections import Counter
from pathlib import Path
import re


ISSUE_SHEET_PATH = Path(
    "data/reasoning/9.gpt-oss-120b--native-bedrock/analysis_res/issue_sheet.md"
)

FILE_HEADER_RE = re.compile(r"^## (?P<file_name>.+)$")
ISSUE_LINE_RE = re.compile(r"^- \[(?P<checked>[xX ])\] (?P<issue_name>.+?)\s*$")


def parse_issue_sheet(text: str) -> dict[str, list[str]]:
    per_file_issues: dict[str, list[str]] = {}
    current_file: str | None = None

    for raw_line in text.splitlines():
        line = raw_line.rstrip()

        file_match = FILE_HEADER_RE.match(line)
        if file_match is not None:
            current_file = file_match.group("file_name")
            per_file_issues[current_file] = []
            continue

        if current_file is None:
            continue

        issue_match = ISSUE_LINE_RE.match(line)
        if issue_match is None:
            continue

        if issue_match.group("checked").lower() != "x":
            continue

        per_file_issues[current_file].append(issue_match.group("issue_name").strip())

    return per_file_issues


def compute_issue_count_distribution(per_file_issues: dict[str, list[str]]) -> Counter:
    return Counter(len(issues) for issues in per_file_issues.values())


def compute_issue_type_counts(per_file_issues: dict[str, list[str]]) -> Counter:
    return Counter(issue for issues in per_file_issues.values() for issue in issues)


def render_stats_report(issue_sheet_path: Path = ISSUE_SHEET_PATH) -> str:
    per_file_issues = parse_issue_sheet(issue_sheet_path.read_text())
    issue_count_distribution = compute_issue_count_distribution(per_file_issues)
    issue_type_counts = compute_issue_type_counts(per_file_issues)
    max_issue_count = max(issue_count_distribution, default=0)
    zero_issue_files = sorted(
        file_name
        for file_name, issues in per_file_issues.items()
        if len(issues) == 0
    )

    lines = [
        f"Issue sheet: {issue_sheet_path}",
        f"Total files: {len(per_file_issues)}",
        "",
        "Per-file issue count distribution:",
    ]

    for issue_count in range(max_issue_count + 1):
        file_count = issue_count_distribution[issue_count]
        lines.append(f"{issue_count} issue(s): {file_count} trace(s)")

    lines.append("")
    lines.append("Files with 0 issues:")
    if zero_issue_files:
        lines.extend(zero_issue_files)
    else:
        lines.append("(none)")

    lines.append("")
    lines.append("Issue type counts:")

    for issue_name, count in sorted(
        issue_type_counts.items(),
        key=lambda item: (-item[1], item[0]),
    ):
        lines.append(f"{issue_name}: {count} / {len(per_file_issues)} = {count / len(per_file_issues)}")

    return "\n".join(lines)


def test_parse_issue_sheet_counts_checked_issues_only():
    text = """# Issue Sheet

## file_a.md
- [x] Wordy/Back and forth
- [ ] Broken thought
### Wordy/Back and forth
- extra note

## file_zero.md
- [ ] Wordy/Back and forth
- [ ] Broken thought

## file_b.md
- [x] Broken thought
- [x] Lost constraint
"""

    per_file_issues = parse_issue_sheet(text)

    assert per_file_issues == {
        "file_a.md": ["Wordy/Back and forth"],
        "file_zero.md": [],
        "file_b.md": ["Broken thought", "Lost constraint"],
    }
    assert compute_issue_count_distribution(per_file_issues) == Counter({0: 1, 1: 1, 2: 1})
    assert compute_issue_type_counts(per_file_issues) == Counter(
        {
            "Wordy/Back and forth": 1,
            "Broken thought": 1,
            "Lost constraint": 1,
        }
    )


if __name__ == "__main__":
    print(render_stats_report())