from __future__ import annotations

from src.agent.conf_sum.resolvers.generic import OfficialListResolver
from src.agent.conf_sum.sources.official_pages import DblpSearchApiClient


class IcseResolver(OfficialListResolver):
    def __init__(
        self,
        conference,
        timeout_seconds: float,
        user_agent: str,
        official_client: DblpSearchApiClient | None = None,
        show_progress: bool = True,
    ) -> None:
        client = official_client or DblpSearchApiClient(
            query=f"toc:db/conf/icse/icse{conference.year}.bht:",
            timeout_seconds=timeout_seconds,
            user_agent=user_agent,
            required_year=conference.year,
            required_venue=conference.name,
        )
        super().__init__(conference=conference, client=client, show_progress=show_progress)