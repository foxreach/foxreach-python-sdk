from __future__ import annotations

from dataclasses import asdict
from typing import Any, Dict, List, Optional, TYPE_CHECKING

from ..types import Campaign, CampaignCreate, CampaignUpdate, Sequence, SequenceCreate, SequenceUpdate
from .._pagination import (
    PaginatedResponse,
    AsyncPaginatedResponse,
    _fetch_page,
    _async_fetch_page,
)

if TYPE_CHECKING:
    from .._http import AsyncHttpClient, HttpClient


def _make_campaign(data: dict) -> Campaign:
    return Campaign(
        id=data.get("id", ""),
        name=data.get("name", ""),
        status=data.get("status", "draft"),
        timezone=data.get("timezone", "UTC"),
        sending_days=data.get("sending_days", [1, 2, 3, 4, 5]),
        sending_start_hour=data.get("sending_start_hour", 9),
        sending_end_hour=data.get("sending_end_hour", 17),
        daily_limit=data.get("daily_limit", 50),
        sent_today=data.get("sent_today", 0),
        total_leads=data.get("total_leads", 0),
        total_sent=data.get("total_sent", 0),
        total_delivered=data.get("total_delivered", 0),
        total_bounced=data.get("total_bounced", 0),
        total_replied=data.get("total_replied", 0),
        total_opened=data.get("total_opened", 0),
        created_at=data.get("created_at"),
        updated_at=data.get("updated_at"),
        started_at=data.get("started_at"),
        completed_at=data.get("completed_at"),
    )


def _make_sequence(data: dict) -> Sequence:
    return Sequence(
        id=data.get("id", ""),
        campaign_id=data.get("campaign_id", ""),
        step_number=data.get("step_number", 1),
        subject=data.get("subject"),
        body=data.get("body", ""),
        delay_days=data.get("delay_days", 1),
        template_type=data.get("template_type", "email"),
        created_at=data.get("created_at"),
        updated_at=data.get("updated_at"),
    )


def _unwrap(result: Any) -> Any:
    if isinstance(result, dict) and "data" in result:
        return result["data"]
    return result


# ---------------------------------------------------------------------------
# Sequences (nested resource)
# ---------------------------------------------------------------------------

class SequencesResource:
    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def list(self, campaign_id: str) -> List[Sequence]:
        result = self._http.request("GET", f"/campaigns/{campaign_id}/sequences")
        items = _unwrap(result)
        if isinstance(items, list):
            return [_make_sequence(d) for d in items]
        return []

    def create(self, campaign_id: str, data: SequenceCreate) -> Sequence:
        body = {k: v for k, v in asdict(data).items() if v is not None}
        result = self._http.request("POST", f"/campaigns/{campaign_id}/sequences", json_body=body)
        return _make_sequence(_unwrap(result))

    def update(self, campaign_id: str, sequence_id: str, data: SequenceUpdate) -> Sequence:
        body = {k: v for k, v in asdict(data).items() if v is not None}
        result = self._http.request(
            "PATCH",
            f"/campaigns/{campaign_id}/sequences/{sequence_id}",
            json_body=body,
        )
        return _make_sequence(_unwrap(result))

    def delete(self, campaign_id: str, sequence_id: str) -> None:
        self._http.request("DELETE", f"/campaigns/{campaign_id}/sequences/{sequence_id}")


class AsyncSequencesResource:
    def __init__(self, http: AsyncHttpClient) -> None:
        self._http = http

    async def list(self, campaign_id: str) -> List[Sequence]:
        result = await self._http.request("GET", f"/campaigns/{campaign_id}/sequences")
        items = _unwrap(result)
        if isinstance(items, list):
            return [_make_sequence(d) for d in items]
        return []

    async def create(self, campaign_id: str, data: SequenceCreate) -> Sequence:
        body = {k: v for k, v in asdict(data).items() if v is not None}
        result = await self._http.request("POST", f"/campaigns/{campaign_id}/sequences", json_body=body)
        return _make_sequence(_unwrap(result))

    async def update(self, campaign_id: str, sequence_id: str, data: SequenceUpdate) -> Sequence:
        body = {k: v for k, v in asdict(data).items() if v is not None}
        result = await self._http.request(
            "PATCH",
            f"/campaigns/{campaign_id}/sequences/{sequence_id}",
            json_body=body,
        )
        return _make_sequence(_unwrap(result))

    async def delete(self, campaign_id: str, sequence_id: str) -> None:
        await self._http.request("DELETE", f"/campaigns/{campaign_id}/sequences/{sequence_id}")


# ---------------------------------------------------------------------------
# Campaigns
# ---------------------------------------------------------------------------

class CampaignsResource:
    def __init__(self, http: HttpClient) -> None:
        self._http = http
        self.sequences = SequencesResource(http)

    def list(
        self,
        *,
        page: int = 1,
        page_size: int = 50,
        status: Optional[str] = None,
    ) -> PaginatedResponse[Campaign]:
        params: Dict[str, Any] = {
            "page": page,
            "pageSize": page_size,
            "status": status,
        }
        return _fetch_page(self._http, "/campaigns", params, _make_campaign)

    def get(self, campaign_id: str) -> Campaign:
        result = self._http.request("GET", f"/campaigns/{campaign_id}")
        return _make_campaign(_unwrap(result))

    def create(self, data: CampaignCreate) -> Campaign:
        body = {k: v for k, v in asdict(data).items() if v is not None}
        result = self._http.request("POST", "/campaigns", json_body=body)
        return _make_campaign(_unwrap(result))

    def update(self, campaign_id: str, data: CampaignUpdate) -> Campaign:
        body = {k: v for k, v in asdict(data).items() if v is not None}
        result = self._http.request("PATCH", f"/campaigns/{campaign_id}", json_body=body)
        return _make_campaign(_unwrap(result))

    def delete(self, campaign_id: str) -> None:
        self._http.request("DELETE", f"/campaigns/{campaign_id}")

    def start(self, campaign_id: str) -> Campaign:
        result = self._http.request("POST", f"/campaigns/{campaign_id}/start")
        return _make_campaign(_unwrap(result))

    def pause(self, campaign_id: str) -> Campaign:
        result = self._http.request("POST", f"/campaigns/{campaign_id}/pause")
        return _make_campaign(_unwrap(result))

    def add_leads(self, campaign_id: str, lead_ids: List[str]) -> Dict[str, Any]:
        result = self._http.request(
            "POST",
            f"/campaigns/{campaign_id}/leads",
            json_body={"lead_ids": lead_ids},
        )
        return _unwrap(result) if isinstance(result, dict) else {}

    def add_accounts(self, campaign_id: str, account_ids: List[str]) -> Dict[str, Any]:
        result = self._http.request(
            "POST",
            f"/campaigns/{campaign_id}/accounts",
            json_body={"account_ids": account_ids},
        )
        return _unwrap(result) if isinstance(result, dict) else {}


class AsyncCampaignsResource:
    def __init__(self, http: AsyncHttpClient) -> None:
        self._http = http
        self.sequences = AsyncSequencesResource(http)

    async def list(
        self,
        *,
        page: int = 1,
        page_size: int = 50,
        status: Optional[str] = None,
    ) -> AsyncPaginatedResponse[Campaign]:
        params: Dict[str, Any] = {
            "page": page,
            "pageSize": page_size,
            "status": status,
        }
        return await _async_fetch_page(self._http, "/campaigns", params, _make_campaign)

    async def get(self, campaign_id: str) -> Campaign:
        result = await self._http.request("GET", f"/campaigns/{campaign_id}")
        return _make_campaign(_unwrap(result))

    async def create(self, data: CampaignCreate) -> Campaign:
        body = {k: v for k, v in asdict(data).items() if v is not None}
        result = await self._http.request("POST", "/campaigns", json_body=body)
        return _make_campaign(_unwrap(result))

    async def update(self, campaign_id: str, data: CampaignUpdate) -> Campaign:
        body = {k: v for k, v in asdict(data).items() if v is not None}
        result = await self._http.request("PATCH", f"/campaigns/{campaign_id}", json_body=body)
        return _make_campaign(_unwrap(result))

    async def delete(self, campaign_id: str) -> None:
        await self._http.request("DELETE", f"/campaigns/{campaign_id}")

    async def start(self, campaign_id: str) -> Campaign:
        result = await self._http.request("POST", f"/campaigns/{campaign_id}/start")
        return _make_campaign(_unwrap(result))

    async def pause(self, campaign_id: str) -> Campaign:
        result = await self._http.request("POST", f"/campaigns/{campaign_id}/pause")
        return _make_campaign(_unwrap(result))

    async def add_leads(self, campaign_id: str, lead_ids: List[str]) -> Dict[str, Any]:
        result = await self._http.request(
            "POST",
            f"/campaigns/{campaign_id}/leads",
            json_body={"lead_ids": lead_ids},
        )
        return _unwrap(result) if isinstance(result, dict) else {}

    async def add_accounts(self, campaign_id: str, account_ids: List[str]) -> Dict[str, Any]:
        result = await self._http.request(
            "POST",
            f"/campaigns/{campaign_id}/accounts",
            json_body={"account_ids": account_ids},
        )
        return _unwrap(result) if isinstance(result, dict) else {}
