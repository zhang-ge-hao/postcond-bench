from __future__ import annotations

import json
from typing import Any
from urllib.parse import urlencode
from urllib.request import Request, urlopen


class HttpClient:
    def __init__(self, timeout_seconds: float, user_agent: str) -> None:
        self.timeout_seconds = timeout_seconds
        self.user_agent = user_agent

    def get_text(self, url: str, params: dict[str, Any] | None = None) -> str:
        full_url = self._build_url(url, params)
        request = Request(full_url, headers={"User-Agent": self.user_agent})
        with urlopen(request, timeout=self.timeout_seconds) as response:
            return response.read().decode("utf-8", errors="replace")

    def get_json(self, url: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        return json.loads(self.get_text(url, params=params))

    @staticmethod
    def _build_url(url: str, params: dict[str, Any] | None) -> str:
        if not params:
            return url
        return f"{url}?{urlencode(params)}"