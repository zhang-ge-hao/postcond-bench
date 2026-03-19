from __future__ import annotations

import csv
import json
from pathlib import Path

from openpyxl import Workbook

from src.agent.conf_sum.models import PaperRecord


FIELDNAMES = [
    "conference",
    "year",
    "title",
    "paper_url",
    "crawl_timestamp",
    "status",
    "notes",
]


def export_csv(records: list[PaperRecord], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES)
        writer.writeheader()
        for record in records:
            writer.writerow(record.to_dict())


def export_jsonl(records: list[PaperRecord], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record.to_dict(), ensure_ascii=False) + "\n")


def export_xlsx(records: list[PaperRecord], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    workbook = Workbook()
    worksheet = workbook.active
    worksheet.title = "latest_sample"
    worksheet.append(FIELDNAMES)
    for record in records:
        data = record.to_dict()
        worksheet.append([data[field] for field in FIELDNAMES])
    workbook.save(path)