from __future__ import annotations

from dataclasses import asdict
from typing import Any, Dict, Optional, TYPE_CHECKING

from ..types import Lead, LeadCreate, LeadUpdate
from .._pagination import (
    PaginatedResponse,
    AsyncPaginatedResponse,
    _fetch_page,
    _async_fetch_page,
)

if TYPE_CHECKING:
    from .._http import AsyncHttpClient, HttpClient


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
    ) -> PaginatedResponse[Lead]:
        params: Dict[str, Any] = {
            "page": page,
            "pageSize": page_size,
            "search": search,
            "status": status,
            "tags": tags,
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

    def update(self, lead_id: str, data: LeadUpdate) -> Lead:
        body = {k: v for k, v in asdict(data).items() if v is not None}
        result = self._http.request("PATCH", f"/leads/{lead_id}", json_body=body)
        d = result.get("data", result) if isinstance(result, dict) else result
        return _make_lead(d)

    def delete(self, lead_id: str) -> None:
        self._http.request("DELETE", f"/leads/{lead_id}")


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
    ) -> AsyncPaginatedResponse[Lead]:
        params: Dict[str, Any] = {
            "page": page,
            "pageSize": page_size,
            "search": search,
            "status": status,
            "tags": tags,
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

    async def update(self, lead_id: str, data: LeadUpdate) -> Lead:
        body = {k: v for k, v in asdict(data).items() if v is not None}
        result = await self._http.request("PATCH", f"/leads/{lead_id}", json_body=body)
        d = result.get("data", result) if isinstance(result, dict) else result
        return _make_lead(d)

    async def delete(self, lead_id: str) -> None:
        await self._http.request("DELETE", f"/leads/{lead_id}")
