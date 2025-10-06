import os
import uuid
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Tuple


@dataclass
class JavaTestResult:
    failed_tests: Optional[List[str]]
    running_time: Optional[float]
    interrupted: bool
    timeout: bool
    compile_failure: bool
    reports_exist: bool
    jml_fail: bool
    cmd: str
    test_summary: Optional[str]  # 去除栈轨迹后的精简 stdout（并可拼接 XML 汇总）
    stdout: Optional[str]        # 完整 stdout

    def to_flag(self) -> str:
        if self.timeout:
            return "timeout"
        if not self.reports_exist and self.compile_failure:
            return "compile_failure"
        if not self.reports_exist:
            return "reports_not_exist"
        if self.interrupted:
            return "interrupted"
        if self.failed_tests is not None and len(self.failed_tests) == 0:
            return "passed"
        if self.jml_fail:
            return "jml_fail"
        return "failed"

    def to_string(self) -> str:
        def format_list(title: str, items: Optional[List[str]]):
            if items is None:
                return f"{title}: None"
            if len(items) == 0:
                return f"{title}: []"
            lines = [f"{title}:"]
            lines += [f"    - {x}" for x in items]
            return "\n".join(lines)

        parts = []
        parts.append("=== Java (Maven) Test Result ===")
        parts.append(format_list("Failed tests ", self.failed_tests))
        parts.append(f"Running time : {self.running_time:.2f}s" if self.running_time is not None else "Running time : None")
        parts.append(f"Interrupted  : {self.interrupted}")
        parts.append(f"Timeout      : {self.timeout}")
        parts.append(f"Reports exist: {self.reports_exist}")
        parts.append(f"CMD          : \n    {self.cmd if self.cmd else 'None'}")

        # if self.test_summary:
        #     parts.append("Test Summary (stackless):")
        #     parts += [f"    {line}" for line in self.test_summary.strip().split("\n")]
        # else:
        #     parts.append("Test Summary : None")

        if self.stdout:
            output_dir = "/tmp/sb_tmp_sbout"
            os.makedirs(output_dir, exist_ok=True)
            file_path = os.path.join(output_dir, f"{uuid.uuid4().hex}.log")
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(self.stdout)
            parts.append(f"Stdout file  : {file_path}")
        else:
            parts.append("Stdout file  : None")

        return "\n".join(parts)
