__all__ = ["run_iclr_latest_sample"]


def run_iclr_latest_sample(*args, **kwargs):
	from src.agent.conf_sum.pipeline import run_conference_latest_sample

	return run_conference_latest_sample(*args, **kwargs)


def run_conference_latest_sample(*args, **kwargs):
	from src.agent.conf_sum.pipeline import run_conference_latest_sample as _run_conference_latest_sample

	return _run_conference_latest_sample(*args, **kwargs)