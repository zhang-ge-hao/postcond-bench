from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(slots=True)
class PaperRecord:
    conference: str
    year: int
    title: str
    paper_url: str
    crawl_timestamp: str
    status: str
    notes: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class ConferenceRunResult:
    conference: str
    year: int
    records: list[PaperRecord] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    source_summary: dict[str, str | int] = field(default_factory=dict)

    @property
    def ok_count(self) -> int:
        return len(self.records)

    def to_dict(self) -> dict[str, Any]:
        return {
            "conference": self.conference,
            "year": self.year,
            "record_count": len(self.records),
            "errors": self.errors,
            "source_summary": self.source_summary,
        }