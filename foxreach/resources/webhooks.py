from __future__ import annotations

from dataclasses import asdict
from typing import Any, Dict, List, Optional, TYPE_CHECKING

from ..types import Webhook, WebhookCreate, WebhookUpdate
from .._pagination import (
    PaginatedResponse,
    AsyncPaginatedResponse,
    _fetch_page,
    _async_fetch_page,
)

if TYPE_CHECKING:
    from .._http import AsyncHttpClient, HttpClient


def _make_webhook(data: dict) -> Webhook:
    return Webhook(
        id=data.get("id", ""),
        url=data.get("url", ""),
        is_active=data.get("is_active", True),
        events=data.get("events", []),
        secret=data.get("secret"),
        last_delivered_at=data.get("last_delivered_at"),
        consecutive_failures=data.get("consecutive_failures", 0),
        created_at=data.get("created_at"),
        updated_at=data.get("updated_at"),
    )


def _unwrap(result: Any) -> Any:
    if isinstance(result, dict) and "data" in result:
        return result["data"]
    return result


class WebhooksResource:
    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def list_events(self) -> List[str]:
        result = self._http.request("GET", "/webhooks/events")
        data = _unwrap(result)
        if isinstance(data, list):
            return data
        return []

    def list(
        self,
        *,
        page: int = 1,
        page_size: int = 50,
    ) -> PaginatedResponse[Webhook]:
        params: Dict[str, Any] = {
            "page": page,
            "pageSize": page_size,
        }
        return _fetch_page(self._http, "/webhooks", params, _make_webhook)

    def create(self, data: WebhookCreate) -> Webhook:
        body = {k: v for k, v in asdict(data).items() if v is not None}
        result = self._http.request("POST", "/webhooks", json_body=body)
        return _make_webhook(_unwrap(result))

    def update(self, webhook_id: str, data: WebhookUpdate) -> Webhook:
        body = {k: v for k, v in asdict(data).items() if v is not None}
        result = self._http.request("PATCH", f"/webhooks/{webhook_id}", json_body=body)
        return _make_webhook(_unwrap(result))

    def delete(self, webhook_id: str) -> None:
        self._http.request("DELETE", f"/webhooks/{webhook_id}")


class AsyncWebhooksResource:
    def __init__(self, http: AsyncHttpClient) -> None:
        self._http = http

    async def list_events(self) -> List[str]:
        result = await self._http.request("GET", "/webhooks/events")
        data = _unwrap(result)
        if isinstance(data, list):
            return data
        return []

    async def list(
        self,
        *,
        page: int = 1,
        page_size: int = 50,
    ) -> AsyncPaginatedResponse[Webhook]:
        params: Dict[str, Any] = {
            "page": page,
            "pageSize": page_size,
        }
        return await _async_fetch_page(self._http, "/webhooks", params, _make_webhook)

    async def create(self, data: WebhookCreate) -> Webhook:
        body = {k: v for k, v in asdict(data).items() if v is not None}
        result = await self._http.request("POST", "/webhooks", json_body=body)
        return _make_webhook(_unwrap(result))

    async def update(self, webhook_id: str, data: WebhookUpdate) -> Webhook:
        body = {k: v for k, v in asdict(data).items() if v is not None}
        result = await self._http.request("PATCH", f"/webhooks/{webhook_id}", json_body=body)
        return _make_webhook(_unwrap(result))

    async def delete(self, webhook_id: str) -> None:
        await self._http.request("DELETE", f"/webhooks/{webhook_id}")
