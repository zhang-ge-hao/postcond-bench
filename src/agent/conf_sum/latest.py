from __future__ import annotations

from src.agent.conf_sum.config import ConferenceConfig


def get_latest_year(config: ConferenceConfig) -> int:
    return config.year