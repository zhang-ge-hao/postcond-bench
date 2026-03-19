from src.agent.conf_sum.normalize import normalize_title


def test_normalize_title_removes_spacing_and_punctuation() -> None:
    assert normalize_title("DarkBench: Benchmarking Dark Patterns") == "darkbenchbenchmarkingdarkpatterns"