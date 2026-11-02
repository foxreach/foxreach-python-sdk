from __future__ import annotations

from dataclasses import asdict
from typing import Any, Dict, Optional, TYPE_CHECKING

from ..types import EmailAccount, EmailAccountCreate, EmailAccountUpdate, HealthPayload, ReconnectRequest
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


def _make_health_payload(data: dict) -> HealthPayload:
    return HealthPayload(
        health_score=data.get("healthScore", data.get("health_score")),
        health_basis=data.get("healthBasis", data.get("health_basis")),
        bounce_7d=data.get("bounce7d", data.get("bounce_7d")),
        warmup_enabled=data.get("warmupEnabled", data.get("warmup_enabled")),
        warmup_progress=data.get("warmupProgress", data.get("warmup_progress")),
    )


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

    def create(self, data: EmailAccountCreate) -> EmailAccount:
        """Create a new email account with SMTP/IMAP credentials. Requires write scope."""
        body = {k: v for k, v in asdict(data).items() if v is not None}
        result = self._http.request("POST", "/email-accounts", json_body=body)
        return _make_email_account(_unwrap(result))

    def update(self, account_id: str, data: EmailAccountUpdate) -> EmailAccount:
        """Update an email account's settings. Requires write scope."""
        body = {k: v for k, v in asdict(data).items() if v is not None}
        result = self._http.request("PATCH", f"/email-accounts/{account_id}", json_body=body)
        return _make_email_account(_unwrap(result))

    def reconnect(self, account_id: str, data: ReconnectRequest) -> EmailAccount:
        """Reconnect an account with a new app password. Requires write scope."""
        body = asdict(data)
        result = self._http.request("POST", f"/email-accounts/{account_id}/reconnect", json_body=body)
        return _make_email_account(_unwrap(result))

    def enable_warmup(self, account_id: str) -> EmailAccount:
        """Enable warmup for an account. Requires write scope."""
        result = self._http.request("POST", f"/email-accounts/{account_id}/warmup/enable")
        return _make_email_account(_unwrap(result))

    def disable_warmup(self, account_id: str) -> EmailAccount:
        """Disable warmup for an account. Requires write scope."""
        result = self._http.request("POST", f"/email-accounts/{account_id}/warmup/disable")
        return _make_email_account(_unwrap(result))

    def health(self, account_id: str) -> HealthPayload:
        """Deliverability and warmup health metrics.

        healthScore is None until 20 warmup sends are measured.
        """
        result = self._http.request("GET", f"/email-accounts/{account_id}/health")
        data = _unwrap(result) if isinstance(result, dict) else {}
        return _make_health_payload(data if isinstance(data, dict) else {})

    def warmup_detail(self, account_id: str) -> dict:
        """Warmup progress, pool stats, and the account's last 20 warmup logs."""
        result = self._http.request("GET", f"/email-accounts/{account_id}/warmup")
        return _unwrap(result) if isinstance(result, dict) else {}

    def google_oauth_start(self) -> dict:
        """Begin connecting a Gmail account with Google sign-in.

        Returns a dict with a 'url' key. Open that URL in a browser to complete
        the OAuth consent flow. Requires write scope.
        """
        result = self._http.request("POST", "/email-accounts/google-oauth/start")
        return _unwrap(result) if isinstance(result, dict) else {}


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

    async def create(self, data: EmailAccountCreate) -> EmailAccount:
        """Create a new email account with SMTP/IMAP credentials. Requires write scope."""
        body = {k: v for k, v in asdict(data).items() if v is not None}
        result = await self._http.request("POST", "/email-accounts", json_body=body)
        return _make_email_account(_unwrap(result))

    async def update(self, account_id: str, data: EmailAccountUpdate) -> EmailAccount:
        """Update an email account's settings. Requires write scope."""
        body = {k: v for k, v in asdict(data).items() if v is not None}
        result = await self._http.request("PATCH", f"/email-accounts/{account_id}", json_body=body)
        return _make_email_account(_unwrap(result))

    async def reconnect(self, account_id: str, data: ReconnectRequest) -> EmailAccount:
        """Reconnect an account with a new app password. Requires write scope."""
        body = asdict(data)
        result = await self._http.request("POST", f"/email-accounts/{account_id}/reconnect", json_body=body)
        return _make_email_account(_unwrap(result))

    async def enable_warmup(self, account_id: str) -> EmailAccount:
        """Enable warmup for an account. Requires write scope."""
        result = await self._http.request("POST", f"/email-accounts/{account_id}/warmup/enable")
        return _make_email_account(_unwrap(result))

    async def disable_warmup(self, account_id: str) -> EmailAccount:
        """Disable warmup for an account. Requires write scope."""
        result = await self._http.request("POST", f"/email-accounts/{account_id}/warmup/disable")
        return _make_email_account(_unwrap(result))

    async def health(self, account_id: str) -> HealthPayload:
        """Deliverability and warmup health metrics.

        healthScore is None until 20 warmup sends are measured.
        """
        result = await self._http.request("GET", f"/email-accounts/{account_id}/health")
        data = _unwrap(result) if isinstance(result, dict) else {}
        return _make_health_payload(data if isinstance(data, dict) else {})

    async def warmup_detail(self, account_id: str) -> dict:
        """Warmup progress, pool stats, and the account's last 20 warmup logs."""
        result = await self._http.request("GET", f"/email-accounts/{account_id}/warmup")
        return _unwrap(result) if isinstance(result, dict) else {}

    async def google_oauth_start(self) -> dict:
        """Begin connecting a Gmail account with Google sign-in.

        Returns a dict with a 'url' key. Open that URL in a browser to complete
        the OAuth consent flow. Requires write scope.
        """
        result = await self._http.request("POST", "/email-accounts/google-oauth/start")
        return _unwrap(result) if isinstance(result, dict) else {}
