from src.agent.conf_sum.sources.official_pages import extract_iclr_paper_links


LIST_HTML = """
<html>
  <body>
    <li><a href="/virtual/2025/poster/28346">DarkBench: Benchmarking Dark Patterns in Large Language Models</a></li>
    <li><a href="/virtual/2025/poster/29033">LiveCodeBench: Holistic and Contamination Free Evaluation of Large Language Models for Code</a></li>
    <a href="/virtual/2025/events/oral">Orals</a>
  </body>
</html>
"""


def test_extract_iclr_paper_links_reads_paper_entries() -> None:
    papers = extract_iclr_paper_links(LIST_HTML)
    assert [paper.title for paper in papers] == [
        "DarkBench: Benchmarking Dark Patterns in Large Language Models",
        "LiveCodeBench: Holistic and Contamination Free Evaluation of Large Language Models for Code",
    ]
    assert papers[0].detail_url == "https://iclr.cc/virtual/2025/poster/28346"