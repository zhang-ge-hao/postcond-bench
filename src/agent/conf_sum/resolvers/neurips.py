from __future__ import annotations

from src.agent.conf_sum.resolvers.generic import OfficialListResolver
from src.agent.conf_sum.sources.official_pages import NeuripsAcceptedPapersClient


class NeuripsResolver(OfficialListResolver):
    def __init__(
        self,
        conference,
        timeout_seconds: float,
        user_agent: str,
        official_client: NeuripsAcceptedPapersClient | None = None,
        show_progress: bool = True,
    ) -> None:
        client = official_client or NeuripsAcceptedPapersClient(
            proceedings_url=conference.proceedings_url,
            year=conference.year,
            timeout_seconds=timeout_seconds,
            user_agent=user_agent,
        )
        super().__init__(conference=conference, client=client, show_progress=show_progress)