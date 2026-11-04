from __future__ import annotations

from typing import Any, Dict, List, Optional, TYPE_CHECKING

from .._pagination import (
    PaginatedResponse,
    AsyncPaginatedResponse,
    _fetch_page,
    _async_fetch_page,
)

if TYPE_CHECKING:
    from .._http import AsyncHttpClient, HttpClient


def _unwrap(result: Any) -> Any:
    if isinstance(result, dict) and "data" in result:
        return result["data"]
    return result


class WorkspaceResource:
    """The workspace the key works in: profile, team, invites and defaults (``client.workspace``).
    Team changes need an API key with the ``admin`` scope; see the API reference."""

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def get(self) -> dict:
        """The workspace the key works in. ``role`` is the role of the user who created the key."""
        return _unwrap(self._http.request("GET", "/workspace")) or {}

    def update(self, *, name: Optional[str] = None, slug: Optional[str] = None) -> dict:
        body = {k: v for k, v in {"name": name, "slug": slug}.items() if v is not None}
        return _unwrap(self._http.request("PATCH", "/workspace", json_body=body)) or {}

    def members(self, *, page: int = 1, page_size: int = 50) -> PaginatedResponse[dict]:
        return _fetch_page(self._http, "/workspace/members", {"page": page, "pageSize": page_size}, lambda d: d)

    def invite(self, email: str, *, role: str = "member") -> dict:
        """Invite by email. Sends a real email. Needs an API key with the ``admin`` scope."""
        return _unwrap(self._http.request(
            "POST", "/workspace/members/invite", json_body={"email": email, "role": role}
        )) or {}

    def update_member_role(self, member_id: str, role: str) -> dict:
        """``admin`` or ``member`` only. Needs the ``admin`` scope and a key created by the owner."""
        return _unwrap(self._http.request(
            "PATCH", f"/workspace/members/{member_id}", json_body={"role": role}
        )) or {}

    def remove_member(self, member_id: str) -> dict:
        """Removes the member and revokes the API keys they created in this workspace."""
        return _unwrap(self._http.request("DELETE", f"/workspace/members/{member_id}")) or {}

    def invites(self) -> list:
        return _unwrap(self._http.request("GET", "/workspace/invites")) or []

    def revoke_invite(self, invite_id: str) -> dict:
        return _unwrap(self._http.request("DELETE", f"/workspace/invites/{invite_id}")) or {}

    def resend_invite(self, invite_id: str) -> dict:
        """Sends the invitation email again with a fresh link."""
        return _unwrap(self._http.request("POST", f"/workspace/invites/{invite_id}/resend")) or {}

    def defaults(self) -> dict:
        return _unwrap(self._http.request("GET", "/workspace/defaults")) or {}

    def update_defaults(
        self,
        *,
        daily_limit: Optional[int] = None,
        sending_start_hour: Optional[int] = None,
        sending_start_minute: Optional[int] = None,
        sending_end_hour: Optional[int] = None,
        sending_end_minute: Optional[int] = None,
        warmup_ramp_up_days: Optional[int] = None,
        warmup_daily_limit: Optional[int] = None,
    ) -> dict:
        body = {
            "dailyLimit": daily_limit, "sendingStartHour": sending_start_hour,
            "sendingStartMinute": sending_start_minute, "sendingEndHour": sending_end_hour,
            "sendingEndMinute": sending_end_minute, "warmupRampUpDays": warmup_ramp_up_days,
            "warmupDailyLimit": warmup_daily_limit,
        }
        body = {k: v for k, v in body.items() if v is not None}
        return _unwrap(self._http.request("PATCH", "/workspace/defaults", json_body=body)) or {}


class AsyncWorkspaceResource:
    def __init__(self, http: AsyncHttpClient) -> None:
        self._http = http

    async def get(self) -> dict:
        """The workspace the key works in. ``role`` is the role of the user who created the key."""
        return _unwrap(await self._http.request("GET", "/workspace")) or {}

    async def update(self, *, name: Optional[str] = None, slug: Optional[str] = None) -> dict:
        body = {k: v for k, v in {"name": name, "slug": slug}.items() if v is not None}
        return _unwrap(await self._http.request("PATCH", "/workspace", json_body=body)) or {}

    async def members(self, *, page: int = 1, page_size: int = 50) -> AsyncPaginatedResponse[dict]:
        return await _async_fetch_page(self._http, "/workspace/members", {"page": page, "pageSize": page_size}, lambda d: d)

    async def invite(self, email: str, *, role: str = "member") -> dict:
        """Invite by email. Sends a real email. Needs an API key with the ``admin`` scope."""
        return _unwrap(await self._http.request(
            "POST", "/workspace/members/invite", json_body={"email": email, "role": role}
        )) or {}

    async def update_member_role(self, member_id: str, role: str) -> dict:
        """``admin`` or ``member`` only. Needs the ``admin`` scope and a key created by the owner."""
        return _unwrap(await self._http.request(
            "PATCH", f"/workspace/members/{member_id}", json_body={"role": role}
        )) or {}

    async def remove_member(self, member_id: str) -> dict:
        """Removes the member and revokes the API keys they created in this workspace."""
        return _unwrap(await self._http.request("DELETE", f"/workspace/members/{member_id}")) or {}

    async def invites(self) -> list:
        return _unwrap(await self._http.request("GET", "/workspace/invites")) or []

    async def revoke_invite(self, invite_id: str) -> dict:
        return _unwrap(await self._http.request("DELETE", f"/workspace/invites/{invite_id}")) or {}

    async def resend_invite(self, invite_id: str) -> dict:
        """Sends the invitation email again with a fresh link."""
        return _unwrap(await self._http.request("POST", f"/workspace/invites/{invite_id}/resend")) or {}

    async def defaults(self) -> dict:
        return _unwrap(await self._http.request("GET", "/workspace/defaults")) or {}

    async def update_defaults(
        self,
        *,
        daily_limit: Optional[int] = None,
        sending_start_hour: Optional[int] = None,
        sending_start_minute: Optional[int] = None,
        sending_end_hour: Optional[int] = None,
        sending_end_minute: Optional[int] = None,
        warmup_ramp_up_days: Optional[int] = None,
        warmup_daily_limit: Optional[int] = None,
    ) -> dict:
        body = {
            "dailyLimit": daily_limit, "sendingStartHour": sending_start_hour,
            "sendingStartMinute": sending_start_minute, "sendingEndHour": sending_end_hour,
            "sendingEndMinute": sending_end_minute, "warmupRampUpDays": warmup_ramp_up_days,
            "warmupDailyLimit": warmup_daily_limit,
        }
        body = {k: v for k, v in body.items() if v is not None}
        return _unwrap(await self._http.request("PATCH", "/workspace/defaults", json_body=body)) or {}
