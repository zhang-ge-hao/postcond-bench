from __future__ import annotations

from datetime import datetime, timezone
from typing import Iterable, Protocol

from tqdm import tqdm

from src.agent.conf_sum.models import ConferenceRunResult, PaperRecord
from src.agent.conf_sum.normalize import normalize_title
from src.agent.conf_sum.sample import stable_head_sample
from src.agent.conf_sum.sources.official_pages import PaperCandidate


class PaperListClient(Protocol):
    def list_papers(self) -> list[PaperCandidate]: ...


def build_paper_record(conference: str, year: int, candidate: PaperCandidate) -> PaperRecord:
    crawl_timestamp = datetime.now(timezone.utc).isoformat()
    title = candidate.title
    paper_url = candidate.detail_url
    status = "ok" if title and paper_url else "partial"

    notes_parts: list[str] = []
    if not title:
        notes_parts.append("title_missing")
    if not paper_url:
        notes_parts.append("paper_url_missing")

    return PaperRecord(
        conference=conference,
        year=year,
        title=title,
        paper_url=paper_url,
        crawl_timestamp=crawl_timestamp,
        status=status,
        notes="; ".join(notes_parts),
    )


def _with_progress(items: list[PaperCandidate], conference_name: str, year: int, enabled: bool) -> Iterable[PaperCandidate]:
    if not enabled:
        return items
    return tqdm(items, desc=f"{conference_name} {year}", unit="paper")


class OfficialListResolver:
    def __init__(self, conference, client: PaperListClient, show_progress: bool = True) -> None:
        self.conference = conference
        self.client = client
        self.show_progress = show_progress

    def resolve_latest_sample(self, sample_size: int | None = 10) -> ConferenceRunResult:
        candidates = self.client.list_papers()
        selected = stable_head_sample(candidates, sample_size=sample_size, key=lambda item: normalize_title(item.title))
        result = ConferenceRunResult(
            conference=self.conference.name,
            year=self.conference.year,
            source_summary={
                "strategy": "official_list_page_only",
                "listed_paper_count": len(candidates),
                "selected_paper_count": len(selected),
            },
        )
        for candidate in _with_progress(selected, self.conference.name, self.conference.year, self.show_progress):
            try:
                result.records.append(
                    build_paper_record(
                        conference=self.conference.name,
                        year=self.conference.year,
                        candidate=candidate,
                    )
                )
            except Exception as exc:
                result.errors.append(f"{candidate.title}: {exc}")
        return result