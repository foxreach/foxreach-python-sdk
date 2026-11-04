from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Optional, TYPE_CHECKING

from ..types import Job, Lead, LeadCreate, LeadLabel, LeadTag, LeadUpdate
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
    blocked: int = 0
    duplicate_emails: List[str] = field(default_factory=list)
    blocked_emails: List[str] = field(default_factory=list)
    error_details: List[Dict[str, Any]] = field(default_factory=list)


def _make_bulk_import_result(data: dict) -> BulkImportResult:
    return BulkImportResult(
        created=data.get("created", 0),
        restored=data.get("restored", 0),
        duplicates=data.get("duplicates", 0),
        errors=data.get("errors", 0),
        blocked=data.get("blocked", 0),
        blocked_emails=data.get("blocked_emails") or data.get("blockedEmails", []),
        duplicate_emails=data.get("duplicate_emails") or data.get("duplicateEmails", []),
        error_details=data.get("error_details") or data.get("errorDetails", []),
    )


def _selection(lead_ids: Optional[List[str]], filter: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    """Body for the bulk lead routes: exactly one of lead_ids or filter."""
    if (lead_ids is None) == (filter is None):
        raise ValueError("Pass exactly one of lead_ids or filter")
    body: Dict[str, Any] = {}
    if lead_ids is not None:
        body["leadIds"] = lead_ids
    if filter is not None:
        body["filter"] = filter
    return body


def _job(result: Any) -> Job:
    from .jobs import _make_job

    data = _unwrap(result) if isinstance(result, dict) else {}
    return _make_job(data if isinstance(data, dict) else {})


def _make_label(data: dict) -> LeadLabel:
    return LeadLabel(
        id=data.get("id", ""),
        name=data.get("name", ""),
        color=data.get("color", "neutral"),
        meaning=data.get("meaning", "neutral"),
        created_at=data.get("created_at"),
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
        interest_status=data.get("interest_status"),
        interest_status_source=data.get("interest_status_source"),
        interest_status_updated_at=data.get("interest_status_updated_at"),
        labels=[_make_label(l) for l in data.get("labels") or []],
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
        interest_status: Optional[str] = None,
        label_id: Optional[str] = None,
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
            "interestStatus": interest_status,
            "labelId": label_id,
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

    def set_interest_status(self, lead_id: str, status: Optional[str]) -> Lead:
        """Set the lead's interest status (interested, not_interested or
        out_of_office) by hand, or pass ``None`` to clear it."""
        result = self._http.request("PATCH", f"/leads/{lead_id}", json_body={"interestStatus": status})
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

    def bulk_delete_impact(
        self, *, lead_ids: Optional[List[str]] = None, filter: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Which running campaigns would lose leads if these leads were deleted.
        Read only. Select with ``lead_ids`` or ``filter`` (keys: search, status,
        tags, provider, interestStatus, labelId), not both."""
        result = self._http.request("POST", "/leads/bulk/delete/impact", json_body=_selection(lead_ids, filter))
        data = _unwrap(result) if isinstance(result, dict) else {}
        return data if isinstance(data, dict) else {}

    def bulk_delete(
        self, *, lead_ids: Optional[List[str]] = None, filter: Optional[Dict[str, Any]] = None,
    ) -> Job:
        """Delete many leads and cancel them in every campaign. Irreversible for
        campaign membership: importing a lead again does not put it back in a
        campaign. Up to 1,000 leads finish in the call; more return a pending
        job to poll with ``client.jobs.get``."""
        return _job(self._http.request("POST", "/leads/bulk/delete", json_body=_selection(lead_ids, filter)))

    def bulk_tag(
        self, tags: List[str], *, lead_ids: Optional[List[str]] = None, filter: Optional[Dict[str, Any]] = None,
    ) -> Job:
        """Add tags to many leads (tags are created when missing)."""
        body = {**_selection(lead_ids, filter), "tags": tags}
        return _job(self._http.request("POST", "/leads/bulk/tag", json_body=body))

    def bulk_untag(
        self, tags: List[str], *, lead_ids: Optional[List[str]] = None, filter: Optional[Dict[str, Any]] = None,
    ) -> Job:
        """Remove tags from many leads."""
        body = {**_selection(lead_ids, filter), "tags": tags}
        return _job(self._http.request("POST", "/leads/bulk/untag", json_body=body))

    def bulk_verify(
        self, *, lead_ids: Optional[List[str]] = None, filter: Optional[Dict[str, Any]] = None,
    ) -> Job:
        """Verify up to 10,000 leads' email addresses in the background. Spends
        verification credits (one per good or bad verdict). Returns the job."""
        return _job(self._http.request("POST", "/leads/bulk/verify", json_body=_selection(lead_ids, filter)))

    def export(self, *, search: Optional[str] = None, tags: Optional[str] = None) -> Job:
        """Start a CSV export (up to 100,000 leads). When the job completes, read
        the file with ``download_export(job.id)`` within one hour."""
        body = {k: v for k, v in {"search": search, "tags": tags}.items() if v is not None}
        return _job(self._http.request("POST", "/leads/export", json_body=body))

    def download_export(self, job_id: str) -> str:
        """The CSV text of a completed export job."""
        return self._http.request_text("GET", f"/leads/export/{job_id}/download")

    def variables(self) -> Dict[str, Any]:
        """Merge-tag variables: standard, custom (from your leads) and account."""
        result = self._http.request("GET", "/leads/variables")
        data = _unwrap(result) if isinstance(result, dict) else {}
        return data if isinstance(data, dict) else {}


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
        interest_status: Optional[str] = None,
        label_id: Optional[str] = None,
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
            "interestStatus": interest_status,
            "labelId": label_id,
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

    async def set_interest_status(self, lead_id: str, status: Optional[str]) -> Lead:
        """Async variant of `LeadsResource.set_interest_status`."""
        result = await self._http.request("PATCH", f"/leads/{lead_id}", json_body={"interestStatus": status})
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

    async def bulk_delete_impact(
        self, *, lead_ids: Optional[List[str]] = None, filter: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Async variant of ``LeadsResource.bulk_delete_impact``. Which running campaigns would lose leads if these leads were deleted.
        Read only. Select with ``lead_ids`` or ``filter`` (keys: search, status,
        tags, provider, interestStatus, labelId), not both."""
        result = await self._http.request("POST", "/leads/bulk/delete/impact", json_body=_selection(lead_ids, filter))
        data = _unwrap(result) if isinstance(result, dict) else {}
        return data if isinstance(data, dict) else {}

    async def bulk_delete(
        self, *, lead_ids: Optional[List[str]] = None, filter: Optional[Dict[str, Any]] = None,
    ) -> Job:
        """Delete many leads and cancel them in every campaign. Irreversible for
        campaign membership: importing a lead again does not put it back in a
        campaign. Up to 1,000 leads finish in the call; more return a pending
        job to poll with ``client.jobs.get``."""
        return _job(await self._http.request("POST", "/leads/bulk/delete", json_body=_selection(lead_ids, filter)))

    async def bulk_tag(
        self, tags: List[str], *, lead_ids: Optional[List[str]] = None, filter: Optional[Dict[str, Any]] = None,
    ) -> Job:
        """Add tags to many leads (tags are created when missing)."""
        body = {**_selection(lead_ids, filter), "tags": tags}
        return _job(await self._http.request("POST", "/leads/bulk/tag", json_body=body))

    async def bulk_untag(
        self, tags: List[str], *, lead_ids: Optional[List[str]] = None, filter: Optional[Dict[str, Any]] = None,
    ) -> Job:
        """Remove tags from many leads."""
        body = {**_selection(lead_ids, filter), "tags": tags}
        return _job(await self._http.request("POST", "/leads/bulk/untag", json_body=body))

    async def bulk_verify(
        self, *, lead_ids: Optional[List[str]] = None, filter: Optional[Dict[str, Any]] = None,
    ) -> Job:
        """Verify up to 10,000 leads' email addresses in the background. Spends
        verification credits (one per good or bad verdict). Returns the job."""
        return _job(await self._http.request("POST", "/leads/bulk/verify", json_body=_selection(lead_ids, filter)))

    async def export(self, *, search: Optional[str] = None, tags: Optional[str] = None) -> Job:
        """Start a CSV export (up to 100,000 leads). When the job completes, read
        the file with ``download_export(job.id)`` within one hour."""
        body = {k: v for k, v in {"search": search, "tags": tags}.items() if v is not None}
        return _job(await self._http.request("POST", "/leads/export", json_body=body))

    async def download_export(self, job_id: str) -> str:
        """The CSV text of a completed export job."""
        return await self._http.request_text("GET", f"/leads/export/{job_id}/download")

    async def variables(self) -> Dict[str, Any]:
        """Merge-tag variables: standard, custom (from your leads) and account."""
        result = await self._http.request("GET", "/leads/variables")
        data = _unwrap(result) if isinstance(result, dict) else {}
        return data if isinstance(data, dict) else {}
