from __future__ import annotations

from typing import Any, List, Optional, TYPE_CHECKING

from .._pagination import AsyncPaginatedResponse, PaginatedResponse, _async_fetch_page, _fetch_page
from ..types import BlockListBulkResult, BlockListEntry

if TYPE_CHECKING:
    from .._http import AsyncHttpClient, HttpClient


def _unwrap(result: Any) -> Any:
    if isinstance(result, dict) and "data" in result:
        return result["data"]
    return result


def _make_entry(data: dict) -> BlockListEntry:
    return BlockListEntry(
        id=data.get("id", ""),
        kind=data.get("kind", "email"),
        value=data.get("value", ""),
        source=data.get("source", "manual"),
        note=data.get("note"),
        created_by=data.get("created_by"),
        created_at=data.get("created_at"),
    )


def _make_bulk(data: Any) -> BlockListBulkResult:
    data = data if isinstance(data, dict) else {}
    return BlockListBulkResult(
        created=data.get("created", 0),
        duplicates=data.get("duplicates", 0),
        invalid=data.get("invalid", 0),
        invalid_details=data.get("invalid_details", []),
    )


def _list_params(page: int, page_size: int, search: Optional[str], kind: Optional[str]) -> dict:
    return {"page": page, "pageSize": page_size, "search": search, "kind": kind}


class BlockListResource:
    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def list(
        self,
        *,
        page: int = 1,
        page_size: int = 50,
        search: Optional[str] = None,
        kind: Optional[str] = None,
    ) -> PaginatedResponse[BlockListEntry]:
        """List blocked emails and domains. Requires read scope."""
        return _fetch_page(self._http, "/block-list", _list_params(page, page_size, search, kind), _make_entry)

    def add(self, value: str, *, note: Optional[str] = None) -> BlockListEntry:
        """Block one email or domain. Requires write scope."""
        body: dict = {"value": value}
        if note is not None:
            body["note"] = note
        result = self._http.request("POST", "/block-list", json_body=body)
        data = _unwrap(result) if isinstance(result, dict) else {}
        return _make_entry(data if isinstance(data, dict) else {})

    def bulk_add(self, values: List[str], *, note: Optional[str] = None) -> BlockListBulkResult:
        """Block up to 1,000 emails or domains. Requires write scope."""
        body: dict = {"values": values}
        if note is not None:
            body["note"] = note
        result = self._http.request("POST", "/block-list/bulk", json_body=body)
        return _make_bulk(_unwrap(result) if isinstance(result, dict) else {})

    def remove(self, entry_id: str) -> None:
        """Remove one entry. Requires write scope."""
        self._http.request("DELETE", f"/block-list/{entry_id}")

    def bulk_remove(self, ids: List[str]) -> int:
        """Remove up to 1,000 entries and return how many were deleted."""
        result = self._http.request("POST", "/block-list/bulk-delete", json_body={"ids": ids})
        data = _unwrap(result) if isinstance(result, dict) else {}
        return int(data.get("deleted", 0)) if isinstance(data, dict) else 0

    def export(self, *, search: Optional[str] = None, kind: Optional[str] = None) -> str:
        """Download the list as CSV text. Requires read scope."""
        return self._http.request_text(
            "GET", "/block-list/export", params={"search": search, "kind": kind},
        )


class AsyncBlockListResource:
    def __init__(self, http: AsyncHttpClient) -> None:
        self._http = http

    async def list(
        self,
        *,
        page: int = 1,
        page_size: int = 50,
        search: Optional[str] = None,
        kind: Optional[str] = None,
    ) -> AsyncPaginatedResponse[BlockListEntry]:
        """List blocked emails and domains."""
        return await _async_fetch_page(
            self._http, "/block-list", _list_params(page, page_size, search, kind), _make_entry,
        )

    async def add(self, value: str, *, note: Optional[str] = None) -> BlockListEntry:
        """Block one email or domain."""
        body: dict = {"value": value}
        if note is not None:
            body["note"] = note
        result = await self._http.request("POST", "/block-list", json_body=body)
        data = _unwrap(result) if isinstance(result, dict) else {}
        return _make_entry(data if isinstance(data, dict) else {})

    async def bulk_add(self, values: List[str], *, note: Optional[str] = None) -> BlockListBulkResult:
        """Block up to 1,000 emails or domains."""
        body: dict = {"values": values}
        if note is not None:
            body["note"] = note
        result = await self._http.request("POST", "/block-list/bulk", json_body=body)
        return _make_bulk(_unwrap(result) if isinstance(result, dict) else {})

    async def remove(self, entry_id: str) -> None:
        """Remove one entry."""
        await self._http.request("DELETE", f"/block-list/{entry_id}")

    async def bulk_remove(self, ids: List[str]) -> int:
        """Remove up to 1,000 entries and return how many were deleted."""
        result = await self._http.request("POST", "/block-list/bulk-delete", json_body={"ids": ids})
        data = _unwrap(result) if isinstance(result, dict) else {}
        return int(data.get("deleted", 0)) if isinstance(data, dict) else 0

    async def export(self, *, search: Optional[str] = None, kind: Optional[str] = None) -> str:
        """Download the list as CSV text."""
        return await self._http.request_text(
            "GET", "/block-list/export", params={"search": search, "kind": kind},
        )
