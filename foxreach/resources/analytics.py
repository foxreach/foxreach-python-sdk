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

    def account(self, account_id: Any) -> Any:
        """Sends, rates, health score and the last 14 days of sends for one email account. Requires read scope."""
        result = self._http.request("GET", f"/analytics/accounts/{account_id}")
        return _pa3_data(result)

    def report(self, *, start: Any = None, end: Any = None, campaign_ids: Any = None, account_ids: Any = None) -> Any:
        """Totals and daily, campaign, step and inbox breakdowns for a date range (up to 365 days). Requires read scope."""
        params = {k: v for k, v in {"start": start, "end": end, "campaignIds": campaign_ids, "accountIds": account_ids}.items() if v is not None}
        result = self._http.request("GET", "/analytics/reports", params=params)
        return _pa3_data(result)

    def export_report(self, *, type: Any = None, start: Any = None, end: Any = None, campaign_ids: Any = None, account_ids: Any = None) -> Any:
        """Download a report as CSV text (type summary, daily, campaigns, steps, accounts or activity). Requires read scope."""
        params = {k: v for k, v in {"type": type, "start": start, "end": end, "campaignIds": campaign_ids, "accountIds": account_ids}.items() if v is not None}
        return self._http.request_text("GET", "/analytics/reports/export", params=params)

    def leaderboard(self) -> Any:
        """The five campaigns with the most replies. Requires read scope."""
        result = self._http.request("GET", "/analytics/leaderboard")
        return _pa3_data(result)

    def activity(self, *, limit: Any = None) -> Any:
        """The latest sent emails and replies, 1 to 100. Requires read scope."""
        params = {k: v for k, v in {"limit": limit}.items() if v is not None}
        result = self._http.request("GET", "/analytics/activity", params=params)
        return _pa3_data(result)

    def campaign_daily(self, campaign_id: Any, *, start: Any = None, end: Any = None) -> Any:
        """One campaign's day-by-day sends and replies, counted by the Reports rules. Requires read scope."""
        params = {k: v for k, v in {"start": start, "end": end}.items() if v is not None}
        result = self._http.request("GET", f"/analytics/campaigns/{campaign_id}/daily", params=params)
        return _pa3_data(result)

    def campaign_steps(self, campaign_id: Any, *, start: Any = None, end: Any = None) -> Any:
        """One campaign's results per step and variant, counted by the Reports rules. Requires read scope."""
        params = {k: v for k, v in {"start": start, "end": end}.items() if v is not None}
        result = self._http.request("GET", f"/analytics/campaigns/{campaign_id}/steps", params=params)
        return _pa3_data(result)


class AsyncAnalyticsResource:
    def __init__(self, http: AsyncHttpClient) -> None:
        self._http = http

    async def overview(self) -> OverviewStats:
        result = await self._http.request("GET", "/analytics/overview")
        return _make_overview(_unwrap(result))

    async def campaign(self, campaign_id: str) -> CampaignAnalytics:
        result = await self._http.request("GET", f"/analytics/campaigns/{campaign_id}")
        return _make_campaign_analytics(_unwrap(result))

    async def account(self, account_id: Any) -> Any:
        """Sends, rates, health score and the last 14 days of sends for one email account. Requires read scope."""
        result = await self._http.request("GET", f"/analytics/accounts/{account_id}")
        return _pa3_data(result)

    async def report(self, *, start: Any = None, end: Any = None, campaign_ids: Any = None, account_ids: Any = None) -> Any:
        """Totals and daily, campaign, step and inbox breakdowns for a date range (up to 365 days). Requires read scope."""
        params = {k: v for k, v in {"start": start, "end": end, "campaignIds": campaign_ids, "accountIds": account_ids}.items() if v is not None}
        result = await self._http.request("GET", "/analytics/reports", params=params)
        return _pa3_data(result)

    async def export_report(self, *, type: Any = None, start: Any = None, end: Any = None, campaign_ids: Any = None, account_ids: Any = None) -> Any:
        """Download a report as CSV text (type summary, daily, campaigns, steps, accounts or activity). Requires read scope."""
        params = {k: v for k, v in {"type": type, "start": start, "end": end, "campaignIds": campaign_ids, "accountIds": account_ids}.items() if v is not None}
        return await self._http.request_text("GET", "/analytics/reports/export", params=params)

    async def leaderboard(self) -> Any:
        """The five campaigns with the most replies. Requires read scope."""
        result = await self._http.request("GET", "/analytics/leaderboard")
        return _pa3_data(result)

    async def activity(self, *, limit: Any = None) -> Any:
        """The latest sent emails and replies, 1 to 100. Requires read scope."""
        params = {k: v for k, v in {"limit": limit}.items() if v is not None}
        result = await self._http.request("GET", "/analytics/activity", params=params)
        return _pa3_data(result)

    async def campaign_daily(self, campaign_id: Any, *, start: Any = None, end: Any = None) -> Any:
        """One campaign's day-by-day sends and replies, counted by the Reports rules. Requires read scope."""
        params = {k: v for k, v in {"start": start, "end": end}.items() if v is not None}
        result = await self._http.request("GET", f"/analytics/campaigns/{campaign_id}/daily", params=params)
        return _pa3_data(result)

    async def campaign_steps(self, campaign_id: Any, *, start: Any = None, end: Any = None) -> Any:
        """One campaign's results per step and variant, counted by the Reports rules. Requires read scope."""
        params = {k: v for k, v in {"start": start, "end": end}.items() if v is not None}
        result = await self._http.request("GET", f"/analytics/campaigns/{campaign_id}/steps", params=params)
        return _pa3_data(result)


def _pa3_data(result: Any) -> Any:
    if isinstance(result, dict) and "data" in result and "meta" not in result:
        return result["data"]
    return result
