from __future__ import annotations

from src.agent.conf_sum.resolvers.generic import OfficialListResolver
from src.agent.conf_sum.sources.official_pages import IclrVirtualSiteClient


class IclrResolver(OfficialListResolver):
    def __init__(
        self,
        conference,
        timeout_seconds: float,
        user_agent: str,
        official_client: IclrVirtualSiteClient | None = None,
        show_progress: bool = True,
    ) -> None:
        client = official_client or IclrVirtualSiteClient(
            proceedings_url=conference.proceedings_url,
            timeout_seconds=timeout_seconds,
            user_agent=user_agent,
        )
        super().__init__(conference=conference, client=client, show_progress=show_progress)