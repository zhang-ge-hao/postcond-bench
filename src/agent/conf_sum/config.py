from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


DEFAULT_USER_AGENT = "postcond-bench-conf-sum/0.1"


@dataclass(frozen=True)
class ConferenceConfig:
    name: str
    year: int
    proceedings_url: str
    source_type: str = "virtual_list"


@dataclass(frozen=True)
class PrototypeConfig:
    conference: ConferenceConfig
    sample_size: int | None = 10
    crawl_all: bool = False
    timeout_seconds: float = 30.0
    user_agent: str = DEFAULT_USER_AGENT
    show_progress: bool = True
    output_dir: Path = field(default_factory=lambda: Path("data/conf_sum"))


ICLR_2025 = ConferenceConfig(
    name="ICLR",
    year=2025,
    proceedings_url="https://iclr.cc/virtual/2025/papers.html?filter=titles",
)

ICML_2025 = ConferenceConfig(
    name="ICML",
    year=2025,
    proceedings_url="https://icml.cc/virtual/2025/papers.html?filter=titles",
)

NEURIPS_2025 = ConferenceConfig(
    name="NeurIPS",
    year=2025,
    proceedings_url="https://neurips.cc/Conferences/2025/AcceptedPapersInitial",
    source_type="neurips_cards",
)

FSE_2025 = ConferenceConfig(
    name="FSE",
    year=2025,
    proceedings_url="https://dblp.org/db/journals/pacmse/pacmse2.html#nrFSE",
    source_type="dblp_api",
)

ICSE_2025 = ConferenceConfig(
    name="ICSE",
    year=2025,
    proceedings_url="https://dblp.org/db/conf/icse/icse2025.html",
    source_type="dblp_api",
)

CONFERENCE_BY_KEY = {
    "iclr": ICLR_2025,
    "icml": ICML_2025,
    "neurips": NEURIPS_2025,
    "fse": FSE_2025,
    "icse": ICSE_2025,
}


def default_iclr_config(sample_size: int | None = 10, crawl_all: bool = False) -> PrototypeConfig:
    return PrototypeConfig(conference=ICLR_2025, sample_size=sample_size, crawl_all=crawl_all)


def default_conference_config(
    conference_key: str,
    sample_size: int | None = 10,
    crawl_all: bool = False,
) -> PrototypeConfig:
    conference = CONFERENCE_BY_KEY[conference_key.casefold()]
    return PrototypeConfig(conference=conference, sample_size=sample_size, crawl_all=crawl_all)