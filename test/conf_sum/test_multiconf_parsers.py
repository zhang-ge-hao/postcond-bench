from src.agent.conf_sum.sources.official_pages import (
  extract_dblp_api_paper_links,
  extract_icml_paper_links,
  extract_neurips_paper_links,
)


ICML_LIST_HTML = """
<html>
  <body>
    <li><a href="/virtual/2025/poster/43904">Adaptive Partitioning Schemes for Optimistic Optimization</a></li>
    <li><a href="/virtual/2025/poster/46533">In-Context Linear Regression Demystified</a></li>
  </body>
</html>
"""


NEURIPS_LIST_HTML = """
<html>
  <body>
    <div class="showDetailBtn" data-event-id="115033">
      <div class="maincard narrower poster" id="maincard_115033">
        <div class="maincardBody">Noisy Multi-Label Learning through Co-Occurrence-Aware Diffusion</div>
      </div>
    </div>
    <div class="showDetailBtn" data-event-id="120330">
      <div class="maincard narrower poster" id="maincard_120330">
        <div class="maincardBody">DSCS: Fast CPDAG-Based Verification of Collapsible Submodels in High-Dimensional Bayesian Networks</div>
      </div>
    </div>
  </body>
</html>
"""


ICSE_API_PAYLOAD = {
    "result": {
        "hits": {
            "hit": [
                {
                    "info": {
                        "title": "Accounting for Missing Events in Statistical Information Leakage Analysis.",
                        "venue": "ICSE",
                        "year": "2025",
                        "url": "https://dblp.org/rec/conf/icse/0001MB25",
                    }
                },
                {
                    "info": {
                        "title": "RLCoder: Reinforcement Learning for Repository-Level Code Completion.",
                        "venue": "ICSE",
                        "year": "2025",
                        "url": "https://dblp.org/rec/conf/icse/0001WGCZMZ25",
                    }
                },
            ]
        }
    }
}


PACMSE_API_PAYLOAD = {
    "result": {
        "hits": {
            "hit": [
                {
                    "info": {
                        "title": "LLM-Based Method Name Suggestion with Automatically Generated Context-Rich Prompts.",
                        "venue": "Proc. ACM Softw. Eng.",
                        "number": "FSE",
                        "year": "2025",
                        "url": "",
                    }
                },
                {
                    "info": {
                        "title": "Protecting Privacy in Software Logs: What Should Be Anonymized?",
                        "venue": "Proc. ACM Softw. Eng.",
                        "number": "ISSTA",
                        "year": "2025",
                        "url": "https://dblp.org/rec/journals/pacmse/AghiliLK25",
                    }
                },
            ]
        }
    }
}


def test_extract_icml_paper_links_reads_paper_entries() -> None:
    papers = extract_icml_paper_links(ICML_LIST_HTML)
    assert [paper.title for paper in papers] == [
        "Adaptive Partitioning Schemes for Optimistic Optimization",
        "In-Context Linear Regression Demystified",
    ]
    assert papers[0].detail_url == "https://icml.cc/virtual/2025/poster/43904"


def test_extract_neurips_paper_links_reads_card_entries() -> None:
    papers = extract_neurips_paper_links(NEURIPS_LIST_HTML, year=2025)
    assert [paper.title for paper in papers] == [
        "Noisy Multi-Label Learning through Co-Occurrence-Aware Diffusion",
        "DSCS: Fast CPDAG-Based Verification of Collapsible Submodels in High-Dimensional Bayesian Networks",
    ]
    assert papers[0].detail_url == "https://neurips.cc/Conferences/2025/Schedule?showEvent=115033"


def test_extract_dblp_api_paper_links_reads_icse_entries() -> None:
    papers = extract_dblp_api_paper_links(ICSE_API_PAYLOAD, required_year=2025, required_venue="ICSE")
    assert [paper.title for paper in papers] == [
        "Accounting for Missing Events in Statistical Information Leakage Analysis.",
        "RLCoder: Reinforcement Learning for Repository-Level Code Completion.",
    ]
    assert papers[0].detail_url == "https://dblp.org/rec/conf/icse/0001MB25"


def test_extract_dblp_api_paper_links_filters_pacmse_to_fse() -> None:
    papers = extract_dblp_api_paper_links(PACMSE_API_PAYLOAD, required_year=2025, required_number="FSE")
    assert [paper.title for paper in papers] == [
        "LLM-Based Method Name Suggestion with Automatically Generated Context-Rich Prompts.",
    ]
    assert papers[0].detail_url == ""