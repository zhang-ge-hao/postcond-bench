from pathlib import Path
from typing import *
import xml.etree.ElementTree as ET


def _collect_maven_summary_from_xml(surefire_dir: Path) -> Tuple[str, List[str]]:
    """
    扫描 target/surefire-reports/*.xml，汇总总数与失败的 nodeid（classname#method）。
    """
    if not surefire_dir.exists():
        return ("", [])
    total_tests = total_failures = total_errors = total_skipped = 0
    failed: List[str] = []

    for xml_path in surefire_dir.glob("*.xml"):
        try:
            tree = ET.parse(xml_path)
            root = tree.getroot()
        except Exception:
            continue

        ts_tests = int(root.get("tests", "0"))
        ts_fail = int(root.get("failures", "0"))
        ts_err = int(root.get("errors", "0"))
        ts_skip = int(root.get("skipped", root.get("disabled", "0")))

        total_tests += ts_tests
        total_failures += ts_fail
        total_errors += ts_err
        total_skipped += ts_skip

        for case in root.findall(".//testcase"):
            classname = case.get("classname", "")
            name = case.get("name", "")
            name = name.split("(")[0] # negativeExclusiveInteger() -> negativeExclusiveInteger
            name = name.split("[")[0] # testUsesClassLookup[TEXT] -> testUsesClassLookup
            nodeid = f"{classname}#{name}" if classname else name
            if case.find("failure") is not None or case.find("error") is not None:
                failed.append(nodeid)

    summary = f"Tests run: {total_tests}, Failures: {total_failures}, Errors: {total_errors}, Skipped: {total_skipped}"
    failed = list(set(failed))
    failed.sort()
    return (summary, failed)
