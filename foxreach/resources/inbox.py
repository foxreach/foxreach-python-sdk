from __future__ import annotations

from dataclasses import asdict
from typing import Any, Dict, Optional, TYPE_CHECKING

from ..types import Thread, ThreadUpdate
from .._pagination import (
    PaginatedResponse,
    AsyncPaginatedResponse,
    _fetch_page,
    _async_fetch_page,
)

if TYPE_CHECKING:
    from .._http import AsyncHttpClient, HttpClient


def _make_thread(data: dict) -> Thread:
    return Thread(
        id=data.get("id", ""),
        from_email=data.get("from_email"),
        to_email=data.get("to_email"),
        subject=data.get("subject"),
        body=data.get("body"),
        body_plain=data.get("body_plain"),
        category=data.get("category"),
        is_read=data.get("is_read", False),
        is_starred=data.get("is_starred", False),
        campaign_id=data.get("campaign_id"),
        lead_id=data.get("lead_id"),
        account_id=data.get("account_id"),
        received_at=data.get("received_at"),
    )


def _unwrap(result: Any) -> Any:
    if isinstance(result, dict) and "data" in result:
        return result["data"]
    return result


class InboxResource:
    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def list_threads(
        self,
        *,
        page: int = 1,
        page_size: int = 50,
        category: Optional[str] = None,
        is_read: Optional[bool] = None,
        is_starred: Optional[bool] = None,
        account_id: Optional[str] = None,
        campaign_id: Optional[str] = None,
        search: Optional[str] = None,
    ) -> PaginatedResponse[Thread]:
        params: Dict[str, Any] = {
            "page": page,
            "pageSize": page_size,
            "category": category,
            "isRead": is_read,
            "isStarred": is_starred,
            "accountId": account_id,
            "campaignId": campaign_id,
            "search": search,
        }
        return _fetch_page(self._http, "/inbox/threads", params, _make_thread)

    def get(self, reply_id: str, *, mark_read: bool = False) -> Thread:
        """Get a thread. Reading does not mark it read unless ``mark_read=True``."""
        params = {"markRead": True} if mark_read else None
        result = self._http.request("GET", f"/inbox/threads/{reply_id}", params=params)
        return _make_thread(_unwrap(result))

    def update(self, reply_id: str, data: ThreadUpdate) -> Thread:
        body = {k: v for k, v in asdict(data).items() if v is not None}
        result = self._http.request("PATCH", f"/inbox/threads/{reply_id}", json_body=body)
        return _make_thread(_unwrap(result))

    def delete(self, reply_id: str) -> None:
        """Delete an inbox thread by ID. Requires write scope."""
        self._http.request("DELETE", f"/inbox/threads/{reply_id}")

    def get_conversation(self, reply_id: str) -> dict:
        result = self._http.request("GET", f"/inbox/threads/{reply_id}/conversation")
        return _unwrap(result) if isinstance(result, dict) else {}

    def send_reply(self, reply_id: str, body: str, *, subject: Optional[str] = None) -> dict:
        json_body: Dict[str, Any] = {"body": body}
        if subject:
            json_body["subject"] = subject
        result = self._http.request("POST", f"/inbox/threads/{reply_id}/reply", json_body=json_body)
        return _unwrap(result) if isinstance(result, dict) else {}

    def stats(self) -> dict:
        result = self._http.request("GET", "/inbox/stats")
        return _unwrap(result) if isinstance(result, dict) else {}

    def categorize_stats(
        self,
        *,
        campaign_id: Optional[str] = None,
        sequence_step: Optional[int] = None,
        variant_id: Optional[str] = None,
        group_by: Optional[str] = None,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
    ) -> dict:
        """Per-variant/step/day reply categorization stats for the autoresearch loop."""
        params: Dict[str, Any] = {}
        if campaign_id:
            params["campaignId"] = campaign_id
        if sequence_step is not None:
            params["sequenceStep"] = sequence_step
        if variant_id:
            params["variantId"] = variant_id
        if group_by:
            params["groupBy"] = group_by
        if from_date:
            params["fromDate"] = from_date
        if to_date:
            params["toDate"] = to_date
        result = self._http.request("GET", "/inbox/categorize-stats", params=params)
        return _unwrap(result) if isinstance(result, dict) else {}


class AsyncInboxResource:
    def __init__(self, http: AsyncHttpClient) -> None:
        self._http = http

    async def list_threads(
        self,
        *,
        page: int = 1,
        page_size: int = 50,
        category: Optional[str] = None,
        is_read: Optional[bool] = None,
        is_starred: Optional[bool] = None,
        account_id: Optional[str] = None,
        campaign_id: Optional[str] = None,
        search: Optional[str] = None,
    ) -> AsyncPaginatedResponse[Thread]:
        params: Dict[str, Any] = {
            "page": page,
            "pageSize": page_size,
            "category": category,
            "isRead": is_read,
            "isStarred": is_starred,
            "accountId": account_id,
            "campaignId": campaign_id,
            "search": search,
        }
        return await _async_fetch_page(self._http, "/inbox/threads", params, _make_thread)

    async def get(self, reply_id: str, *, mark_read: bool = False) -> Thread:
        """Get a thread. Reading does not mark it read unless ``mark_read=True``."""
        params = {"markRead": True} if mark_read else None
        result = await self._http.request("GET", f"/inbox/threads/{reply_id}", params=params)
        return _make_thread(_unwrap(result))

    async def update(self, reply_id: str, data: ThreadUpdate) -> Thread:
        body = {k: v for k, v in asdict(data).items() if v is not None}
        result = await self._http.request("PATCH", f"/inbox/threads/{reply_id}", json_body=body)
        return _make_thread(_unwrap(result))

    async def delete(self, reply_id: str) -> None:
        """Delete an inbox thread by ID. Requires write scope."""
        await self._http.request("DELETE", f"/inbox/threads/{reply_id}")

    async def get_conversation(self, reply_id: str) -> dict:
        result = await self._http.request("GET", f"/inbox/threads/{reply_id}/conversation")
        return _unwrap(result) if isinstance(result, dict) else {}

    async def send_reply(self, reply_id: str, body: str, *, subject: Optional[str] = None) -> dict:
        json_body: Dict[str, Any] = {"body": body}
        if subject:
            json_body["subject"] = subject
        result = await self._http.request("POST", f"/inbox/threads/{reply_id}/reply", json_body=json_body)
        return _unwrap(result) if isinstance(result, dict) else {}

    async def stats(self) -> dict:
        result = await self._http.request("GET", "/inbox/stats")
        return _unwrap(result) if isinstance(result, dict) else {}

    async def categorize_stats(
        self,
        *,
        campaign_id: Optional[str] = None,
        sequence_step: Optional[int] = None,
        variant_id: Optional[str] = None,
        group_by: Optional[str] = None,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
    ) -> dict:
        """Per-variant/step/day reply categorization stats for the autoresearch loop."""
        params: Dict[str, Any] = {}
        if campaign_id:
            params["campaignId"] = campaign_id
        if sequence_step is not None:
            params["sequenceStep"] = sequence_step
        if variant_id:
            params["variantId"] = variant_id
        if group_by:
            params["groupBy"] = group_by
        if from_date:
            params["fromDate"] = from_date
        if to_date:
            params["toDate"] = to_date
        result = await self._http.request("GET", "/inbox/categorize-stats", params=params)
        return _unwrap(result) if isinstance(result, dict) else {}
