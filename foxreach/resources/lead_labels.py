from __future__ import annotations

from typing import Any, List, Optional, TYPE_CHECKING

from ..types import LeadLabel

if TYPE_CHECKING:
    from .._http import AsyncHttpClient, HttpClient


def _unwrap(result: Any) -> Any:
    if isinstance(result, dict) and "data" in result:
        return result["data"]
    return result


def _make_label(data: dict) -> LeadLabel:
    return LeadLabel(
        id=data.get("id", ""),
        name=data.get("name", ""),
        color=data.get("color", "neutral"),
        meaning=data.get("meaning", "neutral"),
        created_at=data.get("created_at"),
    )


def _body(name: Optional[str], color: Optional[str], meaning: Optional[str]) -> dict:
    return {k: v for k, v in {"name": name, "color": color, "meaning": meaning}.items() if v is not None}


class LeadLabelsResource:
    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def list(self) -> List[LeadLabel]:
        """The workspace's lead labels, sorted by name (at most 100)."""
        entries = _unwrap(self._http.request("GET", "/lead-labels"))
        return [_make_label(e) for e in entries] if isinstance(entries, list) else []

    def create(self, name: str, *, color: Optional[str] = None, meaning: Optional[str] = None) -> LeadLabel:
        """color: neutral, brand, success, warning, error or info. meaning: positive, neutral or negative."""
        return _make_label(_unwrap(self._http.request("POST", "/lead-labels", json_body=_body(name, color, meaning))))

    def update(
        self, label_id: str, *, name: Optional[str] = None, color: Optional[str] = None, meaning: Optional[str] = None
    ) -> LeadLabel:
        return _make_label(
            _unwrap(self._http.request("PATCH", f"/lead-labels/{label_id}", json_body=_body(name, color, meaning)))
        )

    def delete(self, label_id: str) -> None:
        self._http.request("DELETE", f"/lead-labels/{label_id}")

    def assign(self, lead_id: str, label_id: str) -> None:
        self._http.request("POST", f"/leads/{lead_id}/labels/{label_id}")

    def unassign(self, lead_id: str, label_id: str) -> None:
        self._http.request("DELETE", f"/leads/{lead_id}/labels/{label_id}")


class AsyncLeadLabelsResource:
    def __init__(self, http: AsyncHttpClient) -> None:
        self._http = http

    async def list(self) -> List[LeadLabel]:
        """Async variant of `LeadLabelsResource.list`."""
        entries = _unwrap(await self._http.request("GET", "/lead-labels"))
        return [_make_label(e) for e in entries] if isinstance(entries, list) else []

    async def create(self, name: str, *, color: Optional[str] = None, meaning: Optional[str] = None) -> LeadLabel:
        """color: neutral, brand, success, warning, error or info. meaning: positive, neutral or negative."""
        return _make_label(_unwrap(await self._http.request("POST", "/lead-labels", json_body=_body(name, color, meaning))))

    async def update(
        self, label_id: str, *, name: Optional[str] = None, color: Optional[str] = None, meaning: Optional[str] = None
    ) -> LeadLabel:
        return _make_label(
            _unwrap(await self._http.request("PATCH", f"/lead-labels/{label_id}", json_body=_body(name, color, meaning)))
        )

    async def delete(self, label_id: str) -> None:
        await self._http.request("DELETE", f"/lead-labels/{label_id}")

    async def assign(self, lead_id: str, label_id: str) -> None:
        await self._http.request("POST", f"/leads/{lead_id}/labels/{label_id}")

    async def unassign(self, lead_id: str, label_id: str) -> None:
        await self._http.request("DELETE", f"/leads/{lead_id}/labels/{label_id}")
