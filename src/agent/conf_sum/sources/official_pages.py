from __future__ import annotations

import html
import re
from dataclasses import dataclass
from typing import Any

from src.agent.conf_sum.normalize import normalize_whitespace
from src.agent.conf_sum.sources.base import HttpClient


PAPER_LINK_RE = re.compile(
    r'<li><a href="(?P<href>/virtual/(?P<year>\d{4})/(?P<kind>poster|oral)/(?P<id>\d+))">(?P<title>.*?)</a></li>',
    re.DOTALL,
)
NEURIPS_CARD_RE = re.compile(
    r'<div class="showDetailBtn"\s+data-event-id="(?P<event_id>\d+)">.*?'
    r'<div class="maincardBody">(?P<title>.*?)</div>',
    re.DOTALL,
)


@dataclass(slots=True)
class PaperCandidate:
    title: str
    detail_url: str


def _as_list(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def extract_iclr_paper_links(html_text: str, base_url: str = "https://iclr.cc") -> list[PaperCandidate]:
    candidates: list[PaperCandidate] = []
    seen: set[str] = set()
    for match in PAPER_LINK_RE.finditer(html_text):
        href = html.unescape(match.group("href"))
        title = normalize_whitespace(html.unescape(match.group("title")))
        if not title:
            continue
        if href in seen:
            continue
        seen.add(href)
        candidates.append(PaperCandidate(title=title, detail_url=f"{base_url}{href}"))
    return candidates


def extract_icml_paper_links(html_text: str, base_url: str = "https://icml.cc") -> list[PaperCandidate]:
    candidates: list[PaperCandidate] = []
    seen: set[str] = set()
    for match in PAPER_LINK_RE.finditer(html_text):
        href = html.unescape(match.group("href"))
        title = normalize_whitespace(html.unescape(match.group("title")))
        if not title or href in seen:
            continue
        seen.add(href)
        candidates.append(PaperCandidate(title=title, detail_url=f"{base_url}{href}"))
    return candidates


def extract_neurips_paper_links(html_text: str, year: int, base_url: str = "https://neurips.cc") -> list[PaperCandidate]:
    candidates: list[PaperCandidate] = []
    seen: set[str] = set()
    for match in NEURIPS_CARD_RE.finditer(html_text):
        event_id = match.group("event_id")
        title = normalize_whitespace(html.unescape(match.group("title")))
        detail_url = f"{base_url}/Conferences/{year}/Schedule?showEvent={event_id}"
        if not title or detail_url in seen:
            continue
        seen.add(detail_url)
        candidates.append(PaperCandidate(title=title, detail_url=detail_url))
    return candidates


def extract_dblp_api_paper_links(
    payload: dict[str, Any],
    *,
    required_year: int | None = None,
    required_venue: str | None = None,
    required_number: str | None = None,
) -> list[PaperCandidate]:
    hits = _as_list(payload.get("result", {}).get("hits", {}).get("hit"))
    candidates: list[PaperCandidate] = []
    seen: set[tuple[str, str]] = set()

    for hit in hits:
        info = hit.get("info", {})
        year_text = str(info.get("year", "")).strip()
        venue = normalize_whitespace(html.unescape(str(info.get("venue", ""))))
        number = normalize_whitespace(html.unescape(str(info.get("number", ""))))
        title = normalize_whitespace(html.unescape(str(info.get("title", ""))))
        detail_url = normalize_whitespace(str(info.get("url", "")))

        if required_year is not None and year_text != str(required_year):
            continue
        if required_venue is not None and venue != required_venue:
            continue
        if required_number is not None and number != required_number:
            continue
        if not title:
            continue

        dedupe_key = (title, detail_url)
        if dedupe_key in seen:
            continue
        seen.add(dedupe_key)
        candidates.append(PaperCandidate(title=title, detail_url=detail_url))

    return candidates


class IclrVirtualSiteClient:
    def __init__(self, proceedings_url: str, timeout_seconds: float, user_agent: str) -> None:
        self.proceedings_url = proceedings_url
        self.http = HttpClient(timeout_seconds=timeout_seconds, user_agent=user_agent)

    def list_papers(self) -> list[PaperCandidate]:
        html_text = self.http.get_text(self.proceedings_url)
        return extract_iclr_paper_links(html_text)


class IcmlVirtualSiteClient:
    def __init__(self, proceedings_url: str, timeout_seconds: float, user_agent: str) -> None:
        self.proceedings_url = proceedings_url
        self.http = HttpClient(timeout_seconds=timeout_seconds, user_agent=user_agent)

    def list_papers(self) -> list[PaperCandidate]:
        html_text = self.http.get_text(self.proceedings_url)
        return extract_icml_paper_links(html_text)


class NeuripsAcceptedPapersClient:
    def __init__(self, proceedings_url: str, year: int, timeout_seconds: float, user_agent: str) -> None:
        self.proceedings_url = proceedings_url
        self.year = year
        self.http = HttpClient(timeout_seconds=timeout_seconds, user_agent=user_agent)

    def list_papers(self) -> list[PaperCandidate]:
        html_text = self.http.get_text(self.proceedings_url)
        return extract_neurips_paper_links(html_text, year=self.year)


class DblpSearchApiClient:
    API_URL = "https://dblp.org/search/publ/api"

    def __init__(
        self,
        query: str,
        timeout_seconds: float,
        user_agent: str,
        *,
        required_year: int | None = None,
        required_venue: str | None = None,
        required_number: str | None = None,
        page_size: int = 100,
    ) -> None:
        self.query = query
        self.required_year = required_year
        self.required_venue = required_venue
        self.required_number = required_number
        self.page_size = page_size
        self.http = HttpClient(timeout_seconds=timeout_seconds, user_agent=user_agent)

    def list_papers(self) -> list[PaperCandidate]:
        candidates: list[PaperCandidate] = []
        offset = 0

        while True:
            payload = self.http.get_json(
                self.API_URL,
                params={
                    "q": self.query,
                    "h": self.page_size,
                    "f": offset,
                    "format": "json",
                },
            )
            hits = payload.get("result", {}).get("hits", {})
            sent = int(hits.get("@sent", 0))
            total = int(hits.get("@total", 0))
            candidates.extend(
                extract_dblp_api_paper_links(
                    payload,
                    required_year=self.required_year,
                    required_venue=self.required_venue,
                    required_number=self.required_number,
                )
            )
            offset += sent
            if sent == 0 or offset >= total:
                break

        return candidates