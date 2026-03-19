from src.agent.conf_sum.config import ICLR_2025
from src.agent.conf_sum.resolvers.iclr import IclrResolver
from src.agent.conf_sum.sources.official_pages import PaperCandidate


class FakeOfficialClient:
    def list_papers(self) -> list[PaperCandidate]:
        return [
            PaperCandidate(
                title="DarkBench: Benchmarking Dark Patterns in Large Language Models",
                detail_url="https://iclr.cc/virtual/2025/poster/28346",
            )
        ]


def test_iclr_resolver_builds_minimal_record_from_list_page() -> None:
    resolver = IclrResolver(
        conference=ICLR_2025,
        timeout_seconds=5.0,
        user_agent="test-agent",
        official_client=FakeOfficialClient(),
        show_progress=False,
    )
    result = resolver.resolve_latest_sample(sample_size=1)
    assert result.errors == []
    assert len(result.records) == 1
    record = result.records[0]
    assert record.conference == "ICLR"
    assert record.year == 2025
    assert record.title == "DarkBench: Benchmarking Dark Patterns in Large Language Models"
    assert record.paper_url == "https://iclr.cc/virtual/2025/poster/28346"
    assert record.status == "ok"
    assert result.source_summary == {
        "strategy": "official_list_page_only",
        "listed_paper_count": 1,
        "selected_paper_count": 1,
    }