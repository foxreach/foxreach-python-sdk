from __future__ import annotations

from dataclasses import asdict
from typing import Any, Dict, List, Optional, TYPE_CHECKING

from ..types import (
    Campaign, CampaignCreate, CampaignUpdate, Sequence, SequenceCreate, SequenceUpdate,
    SequenceVariant, VariantCreate, VariantStats, VariantUpdate,
)
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
        esp_matching=data.get("esp_matching", False),
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
        name=data.get("name"),
        subject=data.get("subject"),
        body=data.get("body", ""),
        delay_days=data.get("delay_days", 0),
        delay_hours=data.get("delay_hours", 0),
        send_only_if_no_reply=data.get("send_only_if_no_reply", True),
        send_as_html=data.get("send_as_html", False),
        created_at=data.get("created_at"),
        updated_at=data.get("updated_at"),
    )


def _make_variant(data: dict) -> SequenceVariant:
    return SequenceVariant(
        id=data.get("id", ""),
        sequence_id=data.get("sequence_id", data.get("sequenceId", "")),
        label=data.get("label", ""),
        subject=data.get("subject", ""),
        body=data.get("body", ""),
        weight=data.get("weight", 1),
        send_as_html=data.get("send_as_html", data.get("sendAsHtml", False)),
        created_at=data.get("created_at", data.get("createdAt")),
        updated_at=data.get("updated_at", data.get("updatedAt")),
    )


def _make_variant_stats(data: dict) -> VariantStats:
    return VariantStats(
        variant_id=data.get("variant_id", data.get("variantId", "")),
        label=data.get("label", ""),
        sent=data.get("sent", 0),
        opened=data.get("opened", 0),
        replied=data.get("replied", 0),
        bounced=data.get("bounced", 0),
        open_rate=data.get("open_rate", data.get("openRate", 0.0)),
        reply_rate=data.get("reply_rate", data.get("replyRate", 0.0)),
    )


def _variant_body(data: Any) -> Dict[str, Any]:
    return {k: v for k, v in asdict(data).items() if v is not None}


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

    def list_variants(self, campaign_id: str, sequence_id: str) -> List[SequenceVariant]:
        """A/B variants of a step, ordered by label."""
        result = self._http.request("GET", f"/campaigns/{campaign_id}/sequences/{sequence_id}/variants")
        items = _unwrap(result)
        return [_make_variant(d) for d in items] if isinstance(items, list) else []

    def create_variant(self, campaign_id: str, sequence_id: str, data: VariantCreate) -> SequenceVariant:
        """Add a variant. Not allowed while the campaign is active."""
        result = self._http.request(
            "POST", f"/campaigns/{campaign_id}/sequences/{sequence_id}/variants", json_body=_variant_body(data),
        )
        return _make_variant(_unwrap(result))

    def update_variant(self, campaign_id: str, sequence_id: str, variant_id: str, data: VariantUpdate) -> SequenceVariant:
        result = self._http.request(
            "PATCH", f"/campaigns/{campaign_id}/sequences/{sequence_id}/variants/{variant_id}",
            json_body=_variant_body(data),
        )
        return _make_variant(_unwrap(result))

    def delete_variant(self, campaign_id: str, sequence_id: str, variant_id: str) -> None:
        """Delete a variant. With two variants on the step, the other is deleted too."""
        self._http.request("DELETE", f"/campaigns/{campaign_id}/sequences/{sequence_id}/variants/{variant_id}")

    def variant_stats(self, campaign_id: str, sequence_id: str) -> List[VariantStats]:
        """Sent, opened, replied and bounced per variant; empty when the step has none."""
        result = self._http.request("GET", f"/campaigns/{campaign_id}/sequences/{sequence_id}/variant-stats")
        items = _unwrap(result)
        return [_make_variant_stats(d) for d in items] if isinstance(items, list) else []


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

    async def list_variants(self, campaign_id: str, sequence_id: str) -> List[SequenceVariant]:
        """A/B variants of a step, ordered by label."""
        result = await self._http.request("GET", f"/campaigns/{campaign_id}/sequences/{sequence_id}/variants")
        items = _unwrap(result)
        return [_make_variant(d) for d in items] if isinstance(items, list) else []

    async def create_variant(self, campaign_id: str, sequence_id: str, data: VariantCreate) -> SequenceVariant:
        """Add a variant. Not allowed while the campaign is active."""
        result = await self._http.request(
            "POST", f"/campaigns/{campaign_id}/sequences/{sequence_id}/variants", json_body=_variant_body(data),
        )
        return _make_variant(_unwrap(result))

    async def update_variant(self, campaign_id: str, sequence_id: str, variant_id: str, data: VariantUpdate) -> SequenceVariant:
        result = await self._http.request(
            "PATCH", f"/campaigns/{campaign_id}/sequences/{sequence_id}/variants/{variant_id}",
            json_body=_variant_body(data),
        )
        return _make_variant(_unwrap(result))

    async def delete_variant(self, campaign_id: str, sequence_id: str, variant_id: str) -> None:
        """Delete a variant. With two variants on the step, the other is deleted too."""
        await self._http.request("DELETE", f"/campaigns/{campaign_id}/sequences/{sequence_id}/variants/{variant_id}")

    async def variant_stats(self, campaign_id: str, sequence_id: str) -> List[VariantStats]:
        """Sent, opened, replied and bounced per variant; empty when the step has none."""
        result = await self._http.request("GET", f"/campaigns/{campaign_id}/sequences/{sequence_id}/variant-stats")
        items = _unwrap(result)
        return [_make_variant_stats(d) for d in items] if isinstance(items, list) else []


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

    def resume(self, campaign_id: str) -> Campaign:
        result = self._http.request("POST", f"/campaigns/{campaign_id}/resume")
        return _make_campaign(_unwrap(result))

    def remove_lead(self, campaign_id: str, lead_id: str) -> Dict[str, Any]:
        result = self._http.request("DELETE", f"/campaigns/{campaign_id}/leads/{lead_id}")
        return _unwrap(result) if isinstance(result, dict) else {}

    def remove_account(self, campaign_id: str, account_id: str) -> Dict[str, Any]:
        result = self._http.request("DELETE", f"/campaigns/{campaign_id}/accounts/{account_id}")
        return _unwrap(result) if isinstance(result, dict) else {}

    def list_leads(
        self,
        campaign_id: str,
        *,
        page: int = 1,
        page_size: int = 50,
        status: Optional[str] = None,
        search: Optional[str] = None,
    ) -> Dict[str, Any]:
        params: Dict[str, Any] = {"page": page, "pageSize": page_size}
        if status is not None:
            params["status"] = status
        if search is not None:
            params["search"] = search
        result = self._http.request("GET", f"/campaigns/{campaign_id}/leads", params=params)
        return result if isinstance(result, dict) else {}

    def list_accounts(self, campaign_id: str) -> Dict[str, Any]:
        result = self._http.request("GET", f"/campaigns/{campaign_id}/accounts")
        return result if isinstance(result, dict) else {}

    def duplicate(self, campaign_id: str) -> Campaign:
        """Copy settings, steps, A/B variants and sending accounts into a new draft named "<name> (Copy)". Leads are not copied."""
        result = self._http.request("POST", f"/campaigns/{campaign_id}/duplicate")
        return _make_campaign(_unwrap(result))

    def share(self, campaign_id: str) -> Dict[str, Any]:
        """Turn on the public report page. Returns ``share_slug`` and ``share_url``. Anyone with the link sees the campaign name, its totals and rates, not leads or copy."""
        result = self._http.request("POST", f"/campaigns/{campaign_id}/share")
        return _unwrap(result) if isinstance(result, dict) else {}

    def unshare(self, campaign_id: str) -> Dict[str, Any]:
        """Turn the public report page off. The old link stops working."""
        result = self._http.request("DELETE", f"/campaigns/{campaign_id}/share")
        return _unwrap(result) if isinstance(result, dict) else {}

    def preview(self, campaign_id: str, subject: str, body: str, *, lead_id: Optional[str] = None) -> Dict[str, Any]:
        """Render a subject and body with spin syntax and merge tags filled in. Sends nothing."""
        payload: Dict[str, Any] = {"subject": subject, "body": body}
        if lead_id is not None:
            payload["lead_id"] = lead_id
        result = self._http.request("POST", f"/campaigns/{campaign_id}/preview", json_body=payload)
        return _unwrap(result) if isinstance(result, dict) else {}

    def send_test_email(
        self,
        campaign_id: str,
        *,
        to_email: str,
        account_id: str,
        subject: str,
        body: str,
        is_html: bool = False,
        preheader: Optional[str] = None,
        lead_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Send one REAL email through one of the campaign's accounts to ``to_email``.
        It counts against the account's daily and the workspace's monthly send
        limits. Returns ``success``, ``message_id`` and ``error``."""
        payload: Dict[str, Any] = {
            "to_email": to_email, "account_id": account_id, "subject": subject, "body": body, "is_html": is_html,
        }
        if preheader is not None:
            payload["preheader"] = preheader
        if lead_id is not None:
            payload["lead_id"] = lead_id
        result = self._http.request("POST", f"/campaigns/{campaign_id}/test-email", json_body=payload)
        return _unwrap(result) if isinstance(result, dict) else {}

    def bulk_remove_leads(self, campaign_id: str, lead_ids: List[str]) -> Dict[str, Any]:
        """Remove up to 5,000 leads from a campaign that is not active. Returns ``removed``."""
        result = self._http.request(
            "POST", f"/campaigns/{campaign_id}/leads/bulk-remove", json_body={"lead_ids": lead_ids},
        )
        return _unwrap(result) if isinstance(result, dict) else {}

    def activity(
        self,
        campaign_id: str,
        *,
        type: Optional[str] = None,
        account_id: Optional[str] = None,
        step: Optional[str] = None,
        search: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        sort_by: Optional[str] = None,
        sort_order: Optional[str] = None,
        page: int = 1,
        page_size: int = 50,
    ) -> Dict[str, Any]:
        """Summary, 30-day sparkline, pause or block reason and a paginated event feed."""
        raw = {
            "type": type, "accountId": account_id, "step": step, "search": search, "startDate": start_date,
            "endDate": end_date, "sortBy": sort_by, "sortOrder": sort_order, "page": page, "pageSize": page_size,
        }
        params = {k: v for k, v in raw.items() if v is not None}
        result = self._http.request("GET", f"/campaigns/{campaign_id}/activity", params=params)
        return _unwrap(result) if isinstance(result, dict) else {}

    def cohorts(self, campaign_id: str, *, days: int = 30) -> List[Dict[str, Any]]:
        """Sent, opened, replied, bounced and unique leads per UTC day for the last 1 to 90 days."""
        result = self._http.request("GET", f"/campaigns/{campaign_id}/cohorts", params={"days": days})
        data = _unwrap(result) if isinstance(result, dict) else []
        return data if isinstance(data, list) else []

    def cohort_detail(self, campaign_id: str, date: str) -> Dict[str, Any]:
        """Emails and replies of one UTC day (``YYYY-MM-DD``). Each side is cut at 200 rows."""
        result = self._http.request("GET", f"/campaigns/{campaign_id}/cohorts/{date}")
        return _unwrap(result) if isinstance(result, dict) else {}

    def lead_emails(self, campaign_id: str, lead_id: str) -> List[Dict[str, Any]]:
        """The newest 20 emails and replies for one lead in this campaign."""
        result = self._http.request("GET", f"/campaigns/{campaign_id}/leads/{lead_id}/emails")
        data = _unwrap(result) if isinstance(result, dict) else []
        return data if isinstance(data, list) else []

    def get_esp_mix(self, campaign_id: str) -> Dict[str, Any]:
        result = self._http.request("GET", f"/campaigns/{campaign_id}/esp-mix")
        return result if isinstance(result, dict) else {}


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

    async def resume(self, campaign_id: str) -> Campaign:
        result = await self._http.request("POST", f"/campaigns/{campaign_id}/resume")
        return _make_campaign(_unwrap(result))

    async def remove_lead(self, campaign_id: str, lead_id: str) -> Dict[str, Any]:
        result = await self._http.request("DELETE", f"/campaigns/{campaign_id}/leads/{lead_id}")
        return _unwrap(result) if isinstance(result, dict) else {}

    async def remove_account(self, campaign_id: str, account_id: str) -> Dict[str, Any]:
        result = await self._http.request("DELETE", f"/campaigns/{campaign_id}/accounts/{account_id}")
        return _unwrap(result) if isinstance(result, dict) else {}

    async def list_leads(
        self,
        campaign_id: str,
        *,
        page: int = 1,
        page_size: int = 50,
        status: Optional[str] = None,
        search: Optional[str] = None,
    ) -> Dict[str, Any]:
        params: Dict[str, Any] = {"page": page, "pageSize": page_size}
        if status is not None:
            params["status"] = status
        if search is not None:
            params["search"] = search
        result = await self._http.request("GET", f"/campaigns/{campaign_id}/leads", params=params)
        return result if isinstance(result, dict) else {}

    async def list_accounts(self, campaign_id: str) -> Dict[str, Any]:
        result = await self._http.request("GET", f"/campaigns/{campaign_id}/accounts")
        return result if isinstance(result, dict) else {}

    async def duplicate(self, campaign_id: str) -> Campaign:
        """Copy settings, steps, A/B variants and sending accounts into a new draft named "<name> (Copy)". Leads are not copied."""
        result = await self._http.request("POST", f"/campaigns/{campaign_id}/duplicate")
        return _make_campaign(_unwrap(result))

    async def share(self, campaign_id: str) -> Dict[str, Any]:
        """Turn on the public report page. Returns ``share_slug`` and ``share_url``. Anyone with the link sees the campaign name, its totals and rates, not leads or copy."""
        result = await self._http.request("POST", f"/campaigns/{campaign_id}/share")
        return _unwrap(result) if isinstance(result, dict) else {}

    async def unshare(self, campaign_id: str) -> Dict[str, Any]:
        """Turn the public report page off. The old link stops working."""
        result = await self._http.request("DELETE", f"/campaigns/{campaign_id}/share")
        return _unwrap(result) if isinstance(result, dict) else {}

    async def preview(self, campaign_id: str, subject: str, body: str, *, lead_id: Optional[str] = None) -> Dict[str, Any]:
        """Render a subject and body with spin syntax and merge tags filled in. Sends nothing."""
        payload: Dict[str, Any] = {"subject": subject, "body": body}
        if lead_id is not None:
            payload["lead_id"] = lead_id
        result = await self._http.request("POST", f"/campaigns/{campaign_id}/preview", json_body=payload)
        return _unwrap(result) if isinstance(result, dict) else {}

    async def send_test_email(
        self,
        campaign_id: str,
        *,
        to_email: str,
        account_id: str,
        subject: str,
        body: str,
        is_html: bool = False,
        preheader: Optional[str] = None,
        lead_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Send one REAL email through one of the campaign's accounts to ``to_email``.
        It counts against the account's daily and the workspace's monthly send
        limits. Returns ``success``, ``message_id`` and ``error``."""
        payload: Dict[str, Any] = {
            "to_email": to_email, "account_id": account_id, "subject": subject, "body": body, "is_html": is_html,
        }
        if preheader is not None:
            payload["preheader"] = preheader
        if lead_id is not None:
            payload["lead_id"] = lead_id
        result = await self._http.request("POST", f"/campaigns/{campaign_id}/test-email", json_body=payload)
        return _unwrap(result) if isinstance(result, dict) else {}

    async def bulk_remove_leads(self, campaign_id: str, lead_ids: List[str]) -> Dict[str, Any]:
        """Remove up to 5,000 leads from a campaign that is not active. Returns ``removed``."""
        result = await self._http.request(
            "POST", f"/campaigns/{campaign_id}/leads/bulk-remove", json_body={"lead_ids": lead_ids},
        )
        return _unwrap(result) if isinstance(result, dict) else {}

    async def activity(
        self,
        campaign_id: str,
        *,
        type: Optional[str] = None,
        account_id: Optional[str] = None,
        step: Optional[str] = None,
        search: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        sort_by: Optional[str] = None,
        sort_order: Optional[str] = None,
        page: int = 1,
        page_size: int = 50,
    ) -> Dict[str, Any]:
        """Summary, 30-day sparkline, pause or block reason and a paginated event feed."""
        raw = {
            "type": type, "accountId": account_id, "step": step, "search": search, "startDate": start_date,
            "endDate": end_date, "sortBy": sort_by, "sortOrder": sort_order, "page": page, "pageSize": page_size,
        }
        params = {k: v for k, v in raw.items() if v is not None}
        result = await self._http.request("GET", f"/campaigns/{campaign_id}/activity", params=params)
        return _unwrap(result) if isinstance(result, dict) else {}

    async def cohorts(self, campaign_id: str, *, days: int = 30) -> List[Dict[str, Any]]:
        """Sent, opened, replied, bounced and unique leads per UTC day for the last 1 to 90 days."""
        result = await self._http.request("GET", f"/campaigns/{campaign_id}/cohorts", params={"days": days})
        data = _unwrap(result) if isinstance(result, dict) else []
        return data if isinstance(data, list) else []

    async def cohort_detail(self, campaign_id: str, date: str) -> Dict[str, Any]:
        """Emails and replies of one UTC day (``YYYY-MM-DD``). Each side is cut at 200 rows."""
        result = await self._http.request("GET", f"/campaigns/{campaign_id}/cohorts/{date}")
        return _unwrap(result) if isinstance(result, dict) else {}

    async def lead_emails(self, campaign_id: str, lead_id: str) -> List[Dict[str, Any]]:
        """The newest 20 emails and replies for one lead in this campaign."""
        result = await self._http.request("GET", f"/campaigns/{campaign_id}/leads/{lead_id}/emails")
        data = _unwrap(result) if isinstance(result, dict) else []
        return data if isinstance(data, list) else []

    async def get_esp_mix(self, campaign_id: str) -> Dict[str, Any]:
        result = await self._http.request("GET", f"/campaigns/{campaign_id}/esp-mix")
        return result if isinstance(result, dict) else {}
