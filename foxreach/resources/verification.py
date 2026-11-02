from __future__ import annotations

from typing import Any, Dict, List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .._http import AsyncHttpClient, HttpClient


def _unwrap(result: Any) -> Any:
    if isinstance(result, dict) and "data" in result:
        return result["data"]
    return result


class VerificationResource:
    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def credits(self) -> dict:
        return _unwrap(self._http.request("GET", "/verification/credits")) or {}

    def verify(self, email: str, *, lead_id: Optional[str] = None) -> dict:
        body: Dict[str, Any] = {"email": email}
        if lead_id:
            body["leadId"] = lead_id
        return _unwrap(self._http.request("POST", "/verification/verify", json_body=body)) or {}

    def verify_bulk(self, emails: List[str]) -> dict:
        return _unwrap(
            self._http.request("POST", "/verification/verify/bulk", json_body={"emails": emails})
        ) or {}


class AsyncVerificationResource:
    def __init__(self, http: AsyncHttpClient) -> None:
        self._http = http

    async def credits(self) -> dict:
        return _unwrap(await self._http.request("GET", "/verification/credits")) or {}

    async def verify(self, email: str, *, lead_id: Optional[str] = None) -> dict:
        body: Dict[str, Any] = {"email": email}
        if lead_id:
            body["leadId"] = lead_id
        return _unwrap(await self._http.request("POST", "/verification/verify", json_body=body)) or {}

    async def verify_bulk(self, emails: List[str]) -> dict:
        return _unwrap(
            await self._http.request("POST", "/verification/verify/bulk", json_body={"emails": emails})
        ) or {}
