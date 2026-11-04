from __future__ import annotations

from typing import Any, Dict, Optional, TYPE_CHECKING

from .._pagination import (
    PaginatedResponse,
    AsyncPaginatedResponse,
    _fetch_page,
    _async_fetch_page,
)

if TYPE_CHECKING:
    from .._http import AsyncHttpClient, HttpClient


def _params(page: int, page_size: int, type: Optional[str], start_date: Optional[str], end_date: Optional[str]) -> Dict[str, Any]:
    return {"page": page, "pageSize": page_size, "type": type, "startDate": start_date, "endDate": end_date}


class EventsResource:
    """The workspace event log (``GET /events``). Not the subscribable event types:
    that is ``client.webhooks.list_events()``."""

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def list(
        self,
        *,
        type: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        page: int = 1,
        page_size: int = 50,
    ) -> PaginatedResponse[dict]:
        return _fetch_page(self._http, "/events", _params(page, page_size, type, start_date, end_date), lambda d: d)


class AsyncEventsResource:
    def __init__(self, http: AsyncHttpClient) -> None:
        self._http = http

    async def list(
        self,
        *,
        type: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        page: int = 1,
        page_size: int = 50,
    ) -> AsyncPaginatedResponse[dict]:
        return await _async_fetch_page(self._http, "/events", _params(page, page_size, type, start_date, end_date), lambda d: d)
