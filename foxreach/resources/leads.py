from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Optional, TYPE_CHECKING

from ..types import Lead, LeadCreate, LeadTag, LeadUpdate
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


@dataclass
class BulkImportResult:
    """Structured response from POST /leads/import.

    Use this instead of looping `create()` to avoid per-row 409s and to
    automatically restore soft-deleted leads."""

    created: int = 0
    restored: int = 0
    duplicates: int = 0
    errors: int = 0
    duplicate_emails: List[str] = field(default_factory=list)
    error_details: List[Dict[str, Any]] = field(default_factory=list)


def _make_bulk_import_result(data: dict) -> BulkImportResult:
    return BulkImportResult(
        created=data.get("created", 0),
        restored=data.get("restored", 0),
        duplicates=data.get("duplicates", 0),
        errors=data.get("errors", 0),
        duplicate_emails=data.get("duplicate_emails") or data.get("duplicateEmails", []),
        error_details=data.get("error_details") or data.get("errorDetails", []),
    )


def _make_lead(data: dict) -> Lead:
    return Lead(
        id=data.get("id", ""),
        email=data.get("email", ""),
        first_name=data.get("first_name"),
        last_name=data.get("last_name"),
        company=data.get("company"),
        title=data.get("title"),
        phone=data.get("phone"),
        linkedin_url=data.get("linkedin_url"),
        website=data.get("website"),
        custom_fields=data.get("custom_fields"),
        notes=data.get("notes"),
        tags=data.get("tags", []),
        status=data.get("status", "active"),
        source=data.get("source"),
        created_at=data.get("created_at"),
        updated_at=data.get("updated_at"),
    )


class LeadsResource:
    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def list(
        self,
        *,
        page: int = 1,
        page_size: int = 50,
        search: Optional[str] = None,
        status: Optional[str] = None,
        tags: Optional[str] = None,
        email: Optional[str] = None,
        provider: Optional[str] = None,
    ) -> PaginatedResponse[Lead]:
        """List leads. ``email`` is an exact, case-insensitive match (``%`` and
        ``_`` are literal), unlike ``search`` which matches substrings.
        ``provider`` filters by the recipient's mail provider: google, microsoft,
        zoho, yahoo, godaddy, other, gateway or unresolved."""
        params: Dict[str, Any] = {
            "page": page,
            "pageSize": page_size,
            "search": search,
            "status": status,
            "tags": tags,
            "email": email,
            "provider": provider,
        }
        return _fetch_page(self._http, "/leads", params, _make_lead)

    def get(self, lead_id: str) -> Lead:
        result = self._http.request("GET", f"/leads/{lead_id}")
        data = result.get("data", result) if isinstance(result, dict) else result
        return _make_lead(data)

    def create(self, data: LeadCreate) -> Lead:
        body = {k: v for k, v in asdict(data).items() if v is not None}
        result = self._http.request("POST", "/leads", json_body=body)
        d = result.get("data", result) if isinstance(result, dict) else result
        return _make_lead(d)

    def bulk_import(
        self,
        leads: List[LeadCreate],
        *,
        restore_soft_deleted: bool = True,
    ) -> BulkImportResult:
        """Import many leads in one call.

        Returns a structured result with counts of created / restored /
        duplicates / errors instead of raising on per-row conflicts.
        Soft-deleted leads with matching emails are restored automatically
        (toggle with ``restore_soft_deleted=False``).

        Limit: 1000 leads per request.
        """
        body = {
            "leads": [
                {k: v for k, v in asdict(item).items() if v is not None}
                for item in leads
            ],
            "restore_soft_deleted": restore_soft_deleted,
        }
        result = self._http.request("POST", "/leads/import", json_body=body)
        d = result.get("data", result) if isinstance(result, dict) else result
        return _make_bulk_import_result(d)

    def update(self, lead_id: str, data: LeadUpdate) -> Lead:
        body = {k: v for k, v in asdict(data).items() if v is not None}
        result = self._http.request("PATCH", f"/leads/{lead_id}", json_body=body)
        d = result.get("data", result) if isinstance(result, dict) else result
        return _make_lead(d)

    def delete(self, lead_id: str) -> None:
        self._http.request("DELETE", f"/leads/{lead_id}")

    def activity(self, lead_id: str) -> dict:
        result = self._http.request("GET", f"/leads/{lead_id}/activity")
        return _unwrap(result) if isinstance(result, dict) else {}

    def list_tags(self) -> List[LeadTag]:
        """Get all tags used across the workspace's leads."""
        result = self._http.request("GET", "/leads/tags")
        entries = _unwrap(result) if isinstance(result, dict) else result
        if not isinstance(entries, list):
            entries = []
        return [
            LeadTag(name=t.get("name", "") if isinstance(t, dict) else str(t),
                    count=t.get("count", 0) if isinstance(t, dict) else 0)
            for t in entries
        ]

    def providers(self) -> Dict[str, Any]:
        result = self._http.request("GET", "/leads/providers")
        return result if isinstance(result, dict) else {}


class AsyncLeadsResource:
    def __init__(self, http: AsyncHttpClient) -> None:
        self._http = http

    async def list(
        self,
        *,
        page: int = 1,
        page_size: int = 50,
        search: Optional[str] = None,
        status: Optional[str] = None,
        tags: Optional[str] = None,
        email: Optional[str] = None,
        provider: Optional[str] = None,
    ) -> AsyncPaginatedResponse[Lead]:
        """Async variant of `LeadsResource.list`. ``email`` is an exact,
        case-insensitive match. ``provider`` filters by mail provider."""
        params: Dict[str, Any] = {
            "page": page,
            "pageSize": page_size,
            "search": search,
            "status": status,
            "tags": tags,
            "email": email,
            "provider": provider,
        }
        return await _async_fetch_page(self._http, "/leads", params, _make_lead)

    async def get(self, lead_id: str) -> Lead:
        result = await self._http.request("GET", f"/leads/{lead_id}")
        data = result.get("data", result) if isinstance(result, dict) else result
        return _make_lead(data)

    async def create(self, data: LeadCreate) -> Lead:
        body = {k: v for k, v in asdict(data).items() if v is not None}
        result = await self._http.request("POST", "/leads", json_body=body)
        d = result.get("data", result) if isinstance(result, dict) else result
        return _make_lead(d)

    async def bulk_import(
        self,
        leads: List[LeadCreate],
        *,
        restore_soft_deleted: bool = True,
    ) -> BulkImportResult:
        """Async variant of `LeadsResource.bulk_import`. See that method for details."""
        body = {
            "leads": [
                {k: v for k, v in asdict(item).items() if v is not None}
                for item in leads
            ],
            "restore_soft_deleted": restore_soft_deleted,
        }
        result = await self._http.request("POST", "/leads/import", json_body=body)
        d = result.get("data", result) if isinstance(result, dict) else result
        return _make_bulk_import_result(d)

    async def update(self, lead_id: str, data: LeadUpdate) -> Lead:
        body = {k: v for k, v in asdict(data).items() if v is not None}
        result = await self._http.request("PATCH", f"/leads/{lead_id}", json_body=body)
        d = result.get("data", result) if isinstance(result, dict) else result
        return _make_lead(d)

    async def delete(self, lead_id: str) -> None:
        await self._http.request("DELETE", f"/leads/{lead_id}")

    async def activity(self, lead_id: str) -> dict:
        result = await self._http.request("GET", f"/leads/{lead_id}/activity")
        return _unwrap(result) if isinstance(result, dict) else {}

    async def list_tags(self) -> List[LeadTag]:
        """Get all tags used across the workspace's leads."""
        result = await self._http.request("GET", "/leads/tags")
        entries = _unwrap(result) if isinstance(result, dict) else result
        if not isinstance(entries, list):
            entries = []
        return [
            LeadTag(name=t.get("name", "") if isinstance(t, dict) else str(t),
                    count=t.get("count", 0) if isinstance(t, dict) else 0)
            for t in entries
        ]

    async def providers(self) -> Dict[str, Any]:
        result = await self._http.request("GET", "/leads/providers")
        return result if isinstance(result, dict) else {}
