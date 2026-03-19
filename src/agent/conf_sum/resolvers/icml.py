from __future__ import annotations

from src.agent.conf_sum.resolvers.generic import OfficialListResolver
from src.agent.conf_sum.sources.official_pages import IcmlVirtualSiteClient


class IcmlResolver(OfficialListResolver):
    def __init__(
        self,
        conference,
        timeout_seconds: float,
        user_agent: str,
        official_client: IcmlVirtualSiteClient | None = None,
        show_progress: bool = True,
    ) -> None:
        client = official_client or IcmlVirtualSiteClient(
            proceedings_url=conference.proceedings_url,
            timeout_seconds=timeout_seconds,
            user_agent=user_agent,
        )
        super().__init__(conference=conference, client=client, show_progress=show_progress)