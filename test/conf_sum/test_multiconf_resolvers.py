from src.agent.conf_sum.config import FSE_2025, ICML_2025, ICSE_2025, NEURIPS_2025
from src.agent.conf_sum.resolvers.fse import FseResolver
from src.agent.conf_sum.resolvers.icml import IcmlResolver
from src.agent.conf_sum.resolvers.icse import IcseResolver
from src.agent.conf_sum.resolvers.neurips import NeuripsResolver
from src.agent.conf_sum.sources.official_pages import PaperCandidate


class FakePaperListClient:
    def __init__(self, papers: list[PaperCandidate]) -> None:
        self._papers = papers

    def list_papers(self) -> list[PaperCandidate]:
        return self._papers


def test_icml_resolver_builds_minimal_record_from_list_page() -> None:
    resolver = IcmlResolver(
        conference=ICML_2025,
        timeout_seconds=5.0,
        user_agent="test-agent",
        official_client=FakePaperListClient(
            [PaperCandidate(title="Adaptive Partitioning Schemes for Optimistic Optimization", detail_url="https://icml.cc/virtual/2025/poster/43904")]
        ),
        show_progress=False,
    )
    result = resolver.resolve_latest_sample(sample_size=1)
    assert result.errors == []
    assert len(result.records) == 1
    assert result.records[0].conference == "ICML"
    assert result.records[0].paper_url == "https://icml.cc/virtual/2025/poster/43904"


def test_neurips_resolver_builds_minimal_record_from_list_page() -> None:
    resolver = NeuripsResolver(
        conference=NEURIPS_2025,
        timeout_seconds=5.0,
        user_agent="test-agent",
        official_client=FakePaperListClient(
            [PaperCandidate(title="Noisy Multi-Label Learning through Co-Occurrence-Aware Diffusion", detail_url="https://neurips.cc/Conferences/2025/Schedule?showEvent=115033")]
        ),
        show_progress=False,
    )
    result = resolver.resolve_latest_sample(sample_size=1)
    assert result.errors == []
    assert len(result.records) == 1
    assert result.records[0].conference == "NeurIPS"
    assert result.records[0].paper_url == "https://neurips.cc/Conferences/2025/Schedule?showEvent=115033"


def test_icse_resolver_builds_minimal_record_from_dblp_api() -> None:
    resolver = IcseResolver(
        conference=ICSE_2025,
        timeout_seconds=5.0,
        user_agent="test-agent",
        official_client=FakePaperListClient(
            [PaperCandidate(title="Accounting for Missing Events in Statistical Information Leakage Analysis.", detail_url="https://dblp.org/rec/conf/icse/0001MB25")]
        ),
        show_progress=False,
    )
    result = resolver.resolve_latest_sample(sample_size=1)
    assert result.errors == []
    assert len(result.records) == 1
    assert result.records[0].conference == "ICSE"
    assert result.records[0].paper_url == "https://dblp.org/rec/conf/icse/0001MB25"


def test_fse_resolver_marks_missing_url_as_partial() -> None:
    resolver = FseResolver(
        conference=FSE_2025,
        timeout_seconds=5.0,
        user_agent="test-agent",
        official_client=FakePaperListClient(
            [PaperCandidate(title="LLM-Based Method Name Suggestion with Automatically Generated Context-Rich Prompts.", detail_url="")]
        ),
        show_progress=False,
    )
    result = resolver.resolve_latest_sample(sample_size=1)
    assert result.errors == []
    assert len(result.records) == 1
    assert result.records[0].conference == "FSE"
    assert result.records[0].status == "partial"
    assert result.records[0].notes == "paper_url_missing"