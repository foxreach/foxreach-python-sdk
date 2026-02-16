from __future__ import annotations

from typing import Any, Dict, Optional, TYPE_CHECKING

from ..types import EmailAccount
from .._pagination import (
    PaginatedResponse,
    AsyncPaginatedResponse,
    _fetch_page,
    _async_fetch_page,
)

if TYPE_CHECKING:
    from .._http import AsyncHttpClient, HttpClient


def _make_email_account(data: dict) -> EmailAccount:
    return EmailAccount(
        id=data.get("id", ""),
        email=data.get("email", ""),
        display_name=data.get("display_name"),
        provider=data.get("provider"),
        daily_limit=data.get("daily_limit", 50),
        sent_today=data.get("sent_today", 0),
        is_active=data.get("is_active", True),
        warmup_enabled=data.get("warmup_enabled", False),
        health_score=data.get("health_score"),
        bounce_rate=data.get("bounce_rate"),
        reply_rate=data.get("reply_rate"),
        connection_status=data.get("connection_status"),
        created_at=data.get("created_at"),
        updated_at=data.get("updated_at"),
    )


def _unwrap(result: Any) -> Any:
    if isinstance(result, dict) and "data" in result:
        return result["data"]
    return result


class EmailAccountsResource:
    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def list(
        self,
        *,
        page: int = 1,
        page_size: int = 50,
    ) -> PaginatedResponse[EmailAccount]:
        params: Dict[str, Any] = {"page": page, "pageSize": page_size}
        return _fetch_page(self._http, "/email-accounts", params, _make_email_account)

    def get(self, account_id: str) -> EmailAccount:
        result = self._http.request("GET", f"/email-accounts/{account_id}")
        return _make_email_account(_unwrap(result))

    def delete(self, account_id: str) -> None:
        self._http.request("DELETE", f"/email-accounts/{account_id}")


class AsyncEmailAccountsResource:
    def __init__(self, http: AsyncHttpClient) -> None:
        self._http = http

    async def list(
        self,
        *,
        page: int = 1,
        page_size: int = 50,
    ) -> AsyncPaginatedResponse[EmailAccount]:
        params: Dict[str, Any] = {"page": page, "pageSize": page_size}
        return await _async_fetch_page(self._http, "/email-accounts", params, _make_email_account)

    async def get(self, account_id: str) -> EmailAccount:
        result = await self._http.request("GET", f"/email-accounts/{account_id}")
        return _make_email_account(_unwrap(result))

    async def delete(self, account_id: str) -> None:
        await self._http.request("DELETE", f"/email-accounts/{account_id}")
