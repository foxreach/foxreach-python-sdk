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


class ApiKeysResource:
    """Manage the workspace's API keys (``client.api_keys``). Needs an API key with the ``admin`` scope."""

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def list(self, *, page: int = 1, page_size: int = 50) -> PaginatedResponse[dict]:
        """Live keys: name, prefix, scopes. Never a secret. Needs the ``admin`` scope."""
        return _fetch_page(self._http, "/api-keys", {"page": page, "pageSize": page_size}, lambda d: d)

    def create(self, name: str, *, scopes: Optional[List[str]] = None) -> dict:
        """Create a key within the calling key's own scopes. The returned ``key`` is shown once."""
        body: Dict[str, Any] = {"name": name}
        if scopes is not None:
            body["scopes"] = scopes
        return _unwrap(self._http.request("POST", "/api-keys", json_body=body)) or {}

    def revoke(self, key_id: str) -> dict:
        return _unwrap(self._http.request("DELETE", f"/api-keys/{key_id}")) or {}


class AsyncApiKeysResource:
    def __init__(self, http: AsyncHttpClient) -> None:
        self._http = http

    async def list(self, *, page: int = 1, page_size: int = 50) -> AsyncPaginatedResponse[dict]:
        """Live keys: name, prefix, scopes. Never a secret. Needs the ``admin`` scope."""
        return await _async_fetch_page(self._http, "/api-keys", {"page": page, "pageSize": page_size}, lambda d: d)

    async def create(self, name: str, *, scopes: Optional[List[str]] = None) -> dict:
        """Create a key within the calling key's own scopes. The returned ``key`` is shown once."""
        body: Dict[str, Any] = {"name": name}
        if scopes is not None:
            body["scopes"] = scopes
        return _unwrap(await self._http.request("POST", "/api-keys", json_body=body)) or {}

    async def revoke(self, key_id: str) -> dict:
        return _unwrap(await self._http.request("DELETE", f"/api-keys/{key_id}")) or {}
