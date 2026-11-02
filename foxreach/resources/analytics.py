from __future__ import annotations

from typing import Any, TYPE_CHECKING

from ..types import CampaignAnalytics, DailyStat, OverviewStats

if TYPE_CHECKING:
    from .._http import AsyncHttpClient, HttpClient


def _unwrap(result: Any) -> Any:
    if isinstance(result, dict) and "data" in result:
        return result["data"]
    return result


def _make_overview(data: dict) -> OverviewStats:
    return OverviewStats(
        total_accounts=data.get("total_accounts", 0),
        active_accounts=data.get("active_accounts", 0),
        total_campaigns=data.get("total_campaigns", 0),
        active_campaigns=data.get("active_campaigns", 0),
        total_leads=data.get("total_leads", 0),
        total_sent=data.get("total_sent", 0),
        total_replies=data.get("total_replies", 0),
        reply_rate=data.get("reply_rate", 0.0),
        account_health_avg=data.get("account_health_avg"),
    )


def _make_campaign_analytics(data: dict) -> CampaignAnalytics:
    daily = [
        DailyStat(
            date=d.get("date", ""),
            sent=d.get("sent", 0),
            delivered=d.get("delivered", 0),
            bounced=d.get("bounced", 0),
            replied=d.get("replied", 0),
            opened=d.get("opened", 0),
        )
        for d in data.get("daily_stats", [])
    ]
    return CampaignAnalytics(
        sent=data.get("sent", 0),
        delivered=data.get("delivered", 0),
        bounced=data.get("bounced", 0),
        replied=data.get("replied", 0),
        opened=data.get("opened", 0),
        reply_rate=data.get("reply_rate", 0.0),
        bounce_rate=data.get("bounce_rate", 0.0),
        daily_stats=daily,
    )


class AnalyticsResource:
    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def overview(self) -> OverviewStats:
        result = self._http.request("GET", "/analytics/overview")
        return _make_overview(_unwrap(result))

    def campaign(self, campaign_id: str) -> CampaignAnalytics:
        result = self._http.request("GET", f"/analytics/campaigns/{campaign_id}")
        return _make_campaign_analytics(_unwrap(result))


class AsyncAnalyticsResource:
    def __init__(self, http: AsyncHttpClient) -> None:
        self._http = http

    async def overview(self) -> OverviewStats:
        result = await self._http.request("GET", "/analytics/overview")
        return _make_overview(_unwrap(result))

    async def campaign(self, campaign_id: str) -> CampaignAnalytics:
        result = await self._http.request("GET", f"/analytics/campaigns/{campaign_id}")
        return _make_campaign_analytics(_unwrap(result))
