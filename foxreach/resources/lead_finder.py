from __future__ import annotations

from typing import Any, Dict, List, Optional, TYPE_CHECKING

from ..types import LeadFinderCredits, LeadFinderList, LeadFinderSavedSearch, RevealBatch

if TYPE_CHECKING:
    from .._http import AsyncHttpClient, HttpClient


def _unwrap(result: Any) -> Any:
    if isinstance(result, dict) and "data" in result:
        return result["data"]
    return result


def _make_credits(data: dict) -> LeadFinderCredits:
    return LeadFinderCredits(
        balance=data.get("balance", 0),
        expires_at=data.get("expiresAt", data.get("expires_at")),
        monthly_included=data.get("monthlyIncluded", data.get("monthly_included", 0)),
        allowed_countries=data.get("allowedCountries", data.get("allowed_countries", [])),
        blocked_countries=data.get("blockedCountries", data.get("blocked_countries", [])),
        coverage=data.get("coverage"),
        credits_per_pack=data.get("creditsPerPack", data.get("credits_per_pack", 0)),
        price_per_pack_cents=data.get("pricePerPackCents", data.get("price_per_pack_cents", 0)),
        search_pages_used_today=data.get("searchPagesUsedToday", data.get("search_pages_used_today", 0)),
        search_pages_allowed_today=data.get("searchPagesAllowedToday", data.get("search_pages_allowed_today", 0)),
        search_pages_per_reveal=data.get("searchPagesPerReveal", data.get("search_pages_per_reveal", 0)),
    )


def _make_reveal_batch(data: dict) -> RevealBatch:
    return RevealBatch(
        batch_id=data.get("batchId", data.get("batch_id", "")),
        reveals=data.get("reveals", []),
        pending=data.get("pending", 0),
        found=data.get("found", 0),
        not_found=data.get("notFound", data.get("not_found", 0)),
        errors=data.get("errors", 0),
        balance=data.get("balance", 0),
    )


def _make_list(data: dict) -> LeadFinderList:
    return LeadFinderList(
        id=data.get("id", ""),
        name=data.get("name", ""),
        kind=data.get("kind"),
        item_count=data.get("itemCount", data.get("item_count", 0)),
        created_at=data.get("createdAt", data.get("created_at")),
    )


def _make_saved_search(data: dict) -> LeadFinderSavedSearch:
    return LeadFinderSavedSearch(
        id=data.get("id", ""),
        name=data.get("name", ""),
        filters=data.get("filters"),
        last_count=data.get("lastCount", data.get("last_count")),
        created_at=data.get("createdAt", data.get("created_at")),
    )


class LeadFinderResource:
    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def filter_options(self) -> dict:
        """Lead Finder filter vocabularies (industries, company types, etc.)."""
        result = self._http.request("GET", "/lead-finder/filter-options")
        return _unwrap(result) if isinstance(result, dict) else {}

    def count(self, filters: dict) -> dict:
        """Count people matching the given filters. Does not consume search budget."""
        result = self._http.request("POST", "/lead-finder/count", json_body={"filters": filters})
        return _unwrap(result) if isinstance(result, dict) else {}

    def search(
        self,
        filters: dict,
        *,
        page_size: int = 25,
        page_token: Optional[str] = None,
    ) -> dict:
        """Search people matching the given filters. Consumes one search page."""
        body: Dict[str, Any] = {"filters": filters, "pageSize": page_size}
        if page_token is not None:
            body["pageToken"] = page_token
        result = self._http.request("POST", "/lead-finder/search", json_body=body)
        return _unwrap(result) if isinstance(result, dict) else {}

    def count_companies(self, filters: dict) -> dict:
        """Count companies matching the given filters."""
        result = self._http.request("POST", "/lead-finder/companies/count", json_body={"filters": filters})
        return _unwrap(result) if isinstance(result, dict) else {}

    def search_companies(
        self,
        filters: dict,
        *,
        page_size: int = 25,
        page_token: Optional[str] = None,
    ) -> dict:
        """Search companies matching the given filters."""
        body: Dict[str, Any] = {"filters": filters, "pageSize": page_size}
        if page_token is not None:
            body["pageToken"] = page_token
        result = self._http.request("POST", "/lead-finder/companies/search", json_body=body)
        return _unwrap(result) if isinstance(result, dict) else {}

    def reveal(self, people: List[dict], *, campaign_id: Optional[str] = None) -> dict:
        """Reveal work emails for up to 100 people. Spends reveal credits.

        Requires write scope.
        """
        body: Dict[str, Any] = {"people": people}
        if campaign_id is not None:
            body["campaignId"] = campaign_id
        result = self._http.request("POST", "/lead-finder/reveal", json_body=body)
        return _unwrap(result) if isinstance(result, dict) else {}

    def add_to_leads(
        self,
        *,
        reveal_ids: Optional[List[str]] = None,
        person_ids: Optional[List[str]] = None,
        campaign_id: Optional[str] = None,
    ) -> dict:
        """Add revealed people into Leads. Requires write scope."""
        body: Dict[str, Any] = {}
        if reveal_ids is not None:
            body["revealIds"] = reveal_ids
        if person_ids is not None:
            body["personIds"] = person_ids
        if campaign_id is not None:
            body["campaignId"] = campaign_id
        result = self._http.request("POST", "/lead-finder/add-to-leads", json_body=body)
        return _unwrap(result) if isinstance(result, dict) else {}

    def list_reveals(
        self,
        *,
        month: Optional[str] = None,
        status: Optional[str] = None,
        q: Optional[str] = None,
        page: int = 1,
        page_size: int = 50,
    ) -> dict:
        """The workspace's reveal history for one month."""
        params: Dict[str, Any] = {"page": page, "pageSize": page_size}
        if month is not None:
            params["month"] = month
        if status is not None:
            params["status"] = status
        if q is not None:
            params["q"] = q
        result = self._http.request("GET", "/lead-finder/reveals", params=params)
        return _unwrap(result) if isinstance(result, dict) else {}

    def get_reveal_batch(self, batch_id: str) -> RevealBatch:
        """Get a specific reveal batch by ID."""
        result = self._http.request("GET", f"/lead-finder/reveals/{batch_id}")
        data = _unwrap(result) if isinstance(result, dict) else {}
        return _make_reveal_batch(data if isinstance(data, dict) else {})

    def credits(self) -> LeadFinderCredits:
        """Get Lead Finder credit balance and search budget."""
        result = self._http.request("GET", "/lead-finder/credits")
        data = _unwrap(result) if isinstance(result, dict) else {}
        return _make_credits(data if isinstance(data, dict) else {})

    def list_lead_finder_lists(self, *, kind: Optional[str] = None) -> List[LeadFinderList]:
        """The workspace's Lead Finder lists."""
        params: Dict[str, Any] = {}
        if kind is not None:
            params["kind"] = kind
        result = self._http.request("GET", "/lead-finder/lists", params=params or None)
        data = _unwrap(result) if isinstance(result, dict) else {}
        items = data.get("lists", []) if isinstance(data, dict) else []
        return [_make_list(i) for i in items]

    def list_saved_searches(self) -> List[LeadFinderSavedSearch]:
        """The workspace's Lead Finder saved searches."""
        result = self._http.request("GET", "/lead-finder/saved-searches")
        data = _unwrap(result) if isinstance(result, dict) else {}
        items = data.get("savedSearches", data.get("saved_searches", [])) if isinstance(data, dict) else []
        return [_make_saved_search(i) for i in items]


class AsyncLeadFinderResource:
    def __init__(self, http: AsyncHttpClient) -> None:
        self._http = http

    async def filter_options(self) -> dict:
        """Lead Finder filter vocabularies."""
        result = await self._http.request("GET", "/lead-finder/filter-options")
        return _unwrap(result) if isinstance(result, dict) else {}

    async def count(self, filters: dict) -> dict:
        """Count people matching the given filters."""
        result = await self._http.request("POST", "/lead-finder/count", json_body={"filters": filters})
        return _unwrap(result) if isinstance(result, dict) else {}

    async def search(
        self,
        filters: dict,
        *,
        page_size: int = 25,
        page_token: Optional[str] = None,
    ) -> dict:
        """Search people matching the given filters."""
        body: Dict[str, Any] = {"filters": filters, "pageSize": page_size}
        if page_token is not None:
            body["pageToken"] = page_token
        result = await self._http.request("POST", "/lead-finder/search", json_body=body)
        return _unwrap(result) if isinstance(result, dict) else {}

    async def count_companies(self, filters: dict) -> dict:
        """Count companies matching the given filters."""
        result = await self._http.request("POST", "/lead-finder/companies/count", json_body={"filters": filters})
        return _unwrap(result) if isinstance(result, dict) else {}

    async def search_companies(
        self,
        filters: dict,
        *,
        page_size: int = 25,
        page_token: Optional[str] = None,
    ) -> dict:
        """Search companies matching the given filters."""
        body: Dict[str, Any] = {"filters": filters, "pageSize": page_size}
        if page_token is not None:
            body["pageToken"] = page_token
        result = await self._http.request("POST", "/lead-finder/companies/search", json_body=body)
        return _unwrap(result) if isinstance(result, dict) else {}

    async def reveal(self, people: List[dict], *, campaign_id: Optional[str] = None) -> dict:
        """Reveal work emails for up to 100 people. Requires write scope."""
        body: Dict[str, Any] = {"people": people}
        if campaign_id is not None:
            body["campaignId"] = campaign_id
        result = await self._http.request("POST", "/lead-finder/reveal", json_body=body)
        return _unwrap(result) if isinstance(result, dict) else {}

    async def add_to_leads(
        self,
        *,
        reveal_ids: Optional[List[str]] = None,
        person_ids: Optional[List[str]] = None,
        campaign_id: Optional[str] = None,
    ) -> dict:
        """Add revealed people into Leads. Requires write scope."""
        body: Dict[str, Any] = {}
        if reveal_ids is not None:
            body["revealIds"] = reveal_ids
        if person_ids is not None:
            body["personIds"] = person_ids
        if campaign_id is not None:
            body["campaignId"] = campaign_id
        result = await self._http.request("POST", "/lead-finder/add-to-leads", json_body=body)
        return _unwrap(result) if isinstance(result, dict) else {}

    async def list_reveals(
        self,
        *,
        month: Optional[str] = None,
        status: Optional[str] = None,
        q: Optional[str] = None,
        page: int = 1,
        page_size: int = 50,
    ) -> dict:
        """The workspace's reveal history for one month."""
        params: Dict[str, Any] = {"page": page, "pageSize": page_size}
        if month is not None:
            params["month"] = month
        if status is not None:
            params["status"] = status
        if q is not None:
            params["q"] = q
        result = await self._http.request("GET", "/lead-finder/reveals", params=params)
        return _unwrap(result) if isinstance(result, dict) else {}

    async def get_reveal_batch(self, batch_id: str) -> RevealBatch:
        """Get a specific reveal batch by ID."""
        result = await self._http.request("GET", f"/lead-finder/reveals/{batch_id}")
        data = _unwrap(result) if isinstance(result, dict) else {}
        return _make_reveal_batch(data if isinstance(data, dict) else {})

    async def credits(self) -> LeadFinderCredits:
        """Get Lead Finder credit balance and search budget."""
        result = await self._http.request("GET", "/lead-finder/credits")
        data = _unwrap(result) if isinstance(result, dict) else {}
        return _make_credits(data if isinstance(data, dict) else {})

    async def list_lead_finder_lists(self, *, kind: Optional[str] = None) -> List[LeadFinderList]:
        """The workspace's Lead Finder lists."""
        params: Dict[str, Any] = {}
        if kind is not None:
            params["kind"] = kind
        result = await self._http.request("GET", "/lead-finder/lists", params=params or None)
        data = _unwrap(result) if isinstance(result, dict) else {}
        items = data.get("lists", []) if isinstance(data, dict) else []
        return [_make_list(i) for i in items]

    async def list_saved_searches(self) -> List[LeadFinderSavedSearch]:
        """The workspace's Lead Finder saved searches."""
        result = await self._http.request("GET", "/lead-finder/saved-searches")
        data = _unwrap(result) if isinstance(result, dict) else {}
        items = data.get("savedSearches", data.get("saved_searches", [])) if isinstance(data, dict) else []
        return [_make_saved_search(i) for i in items]
