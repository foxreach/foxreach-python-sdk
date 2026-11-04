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

    def create_list(self, name: Any, kind: Any) -> Any:
        """Create an empty people or companies list. Requires write scope."""
        body = {k: v for k, v in {"name": name, "kind": kind}.items() if v is not None}
        result = self._http.request("POST", "/lead-finder/lists", json_body=body)
        return _pa3_data(result)

    def get_list(self, list_id: Any) -> Any:
        """Read one list with its item count. Requires read scope."""
        result = self._http.request("GET", f"/lead-finder/lists/{list_id}")
        return _pa3_data(result)

    def rename_list(self, list_id: Any, name: Any) -> Any:
        """Rename a list. Requires write scope."""
        body = {k: v for k, v in {"name": name}.items() if v is not None}
        result = self._http.request("PATCH", f"/lead-finder/lists/{list_id}", json_body=body)
        return _pa3_data(result)

    def delete_list(self, list_id: Any) -> Any:
        """Delete a list and its items. Reveals and leads already created stay. Requires write scope."""
        result = self._http.request("DELETE", f"/lead-finder/lists/{list_id}")
        return _pa3_data(result)

    def list_items(self, list_id: Any, *, page: Any = None, page_size: Any = None) -> Any:
        """One page of a list's items with reveal status and lead link (page size 1 to 100). Requires read scope."""
        params = {k: v for k, v in {"page": page, "pageSize": page_size}.items() if v is not None}
        result = self._http.request("GET", f"/lead-finder/lists/{list_id}/items", params=params)
        return result if isinstance(result, dict) else {}

    def add_items(self, list_id: Any, items: Any) -> Any:
        """Save up to 200 people or companies, each {key, snapshot}. Requires write scope."""
        body = {k: v for k, v in {"items": items}.items() if v is not None}
        result = self._http.request("POST", f"/lead-finder/lists/{list_id}/items", json_body=body)
        return _pa3_data(result)

    def remove_items(self, list_id: Any, keys: Any) -> Any:
        """Remove up to 5,000 items by key. Requires write scope."""
        body = {k: v for k, v in {"keys": keys}.items() if v is not None}
        result = self._http.request("DELETE", f"/lead-finder/lists/{list_id}/items", json_body=body)
        return _pa3_data(result)

    def reveal_list(self, list_id: Any, keys: Any, *, campaign_id: Any = None) -> Any:
        """Reveal work emails for up to 100 people in a list. SPENDS REVEAL CREDITS, one per newly looked-up person. Requires write scope."""
        body = {k: v for k, v in {"keys": keys, "campaign_id": campaign_id}.items() if v is not None}
        result = self._http.request("POST", f"/lead-finder/lists/{list_id}/reveal", json_body=body)
        return _pa3_data(result)

    def add_list_to_leads(self, list_id: Any, *, keys: Any = None, campaign_id: Any = None) -> Any:
        """Add the revealed people of a list to Leads. Free; counts toward the contact limit. Requires write scope."""
        body = {k: v for k, v in {"keys": keys, "campaign_id": campaign_id}.items() if v is not None}
        result = self._http.request("POST", f"/lead-finder/lists/{list_id}/add-to-leads", json_body=body)
        return _pa3_data(result)

    def export_list(self, list_id: Any) -> Any:
        """Download a list as CSV text (at most 5,000 rows). Requires read scope."""
        return self._http.request_text("GET", f"/lead-finder/lists/{list_id}/export")

    def create_saved_search(self, name: Any, kind: Any, *, filters: Any = None) -> Any:
        """Store a set of filters to re-run later. Requires write scope."""
        body = {k: v for k, v in {"name": name, "kind": kind, "filters": filters}.items() if v is not None}
        result = self._http.request("POST", "/lead-finder/saved-searches", json_body=body)
        return _pa3_data(result)

    def get_saved_search(self, saved_search_id: Any) -> Any:
        """Read one saved search. Requires read scope."""
        result = self._http.request("GET", f"/lead-finder/saved-searches/{saved_search_id}")
        return _pa3_data(result)

    def update_saved_search(self, saved_search_id: Any, *, name: Any = None, alert_enabled: Any = None) -> Any:
        """Rename a saved search or switch its alert. Requires write scope."""
        body = {k: v for k, v in {"name": name, "alert_enabled": alert_enabled}.items() if v is not None}
        result = self._http.request("PATCH", f"/lead-finder/saved-searches/{saved_search_id}", json_body=body)
        return _pa3_data(result)

    def delete_saved_search(self, saved_search_id: Any) -> Any:
        """Delete a saved search. Requires write scope."""
        result = self._http.request("DELETE", f"/lead-finder/saved-searches/{saved_search_id}")
        return _pa3_data(result)

    def run_saved_search(self, saved_search_id: Any) -> Any:
        """Count the current matches of a saved search. Free: no reveal credits or search budget. Requires write scope."""
        result = self._http.request("POST", f"/lead-finder/saved-searches/{saved_search_id}/run", json_body={})
        return _pa3_data(result)


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

    async def create_list(self, name: Any, kind: Any) -> Any:
        """Create an empty people or companies list. Requires write scope."""
        body = {k: v for k, v in {"name": name, "kind": kind}.items() if v is not None}
        result = await self._http.request("POST", "/lead-finder/lists", json_body=body)
        return _pa3_data(result)

    async def get_list(self, list_id: Any) -> Any:
        """Read one list with its item count. Requires read scope."""
        result = await self._http.request("GET", f"/lead-finder/lists/{list_id}")
        return _pa3_data(result)

    async def rename_list(self, list_id: Any, name: Any) -> Any:
        """Rename a list. Requires write scope."""
        body = {k: v for k, v in {"name": name}.items() if v is not None}
        result = await self._http.request("PATCH", f"/lead-finder/lists/{list_id}", json_body=body)
        return _pa3_data(result)

    async def delete_list(self, list_id: Any) -> Any:
        """Delete a list and its items. Reveals and leads already created stay. Requires write scope."""
        result = await self._http.request("DELETE", f"/lead-finder/lists/{list_id}")
        return _pa3_data(result)

    async def list_items(self, list_id: Any, *, page: Any = None, page_size: Any = None) -> Any:
        """One page of a list's items with reveal status and lead link (page size 1 to 100). Requires read scope."""
        params = {k: v for k, v in {"page": page, "pageSize": page_size}.items() if v is not None}
        result = await self._http.request("GET", f"/lead-finder/lists/{list_id}/items", params=params)
        return result if isinstance(result, dict) else {}

    async def add_items(self, list_id: Any, items: Any) -> Any:
        """Save up to 200 people or companies, each {key, snapshot}. Requires write scope."""
        body = {k: v for k, v in {"items": items}.items() if v is not None}
        result = await self._http.request("POST", f"/lead-finder/lists/{list_id}/items", json_body=body)
        return _pa3_data(result)

    async def remove_items(self, list_id: Any, keys: Any) -> Any:
        """Remove up to 5,000 items by key. Requires write scope."""
        body = {k: v for k, v in {"keys": keys}.items() if v is not None}
        result = await self._http.request("DELETE", f"/lead-finder/lists/{list_id}/items", json_body=body)
        return _pa3_data(result)

    async def reveal_list(self, list_id: Any, keys: Any, *, campaign_id: Any = None) -> Any:
        """Reveal work emails for up to 100 people in a list. SPENDS REVEAL CREDITS, one per newly looked-up person. Requires write scope."""
        body = {k: v for k, v in {"keys": keys, "campaign_id": campaign_id}.items() if v is not None}
        result = await self._http.request("POST", f"/lead-finder/lists/{list_id}/reveal", json_body=body)
        return _pa3_data(result)

    async def add_list_to_leads(self, list_id: Any, *, keys: Any = None, campaign_id: Any = None) -> Any:
        """Add the revealed people of a list to Leads. Free; counts toward the contact limit. Requires write scope."""
        body = {k: v for k, v in {"keys": keys, "campaign_id": campaign_id}.items() if v is not None}
        result = await self._http.request("POST", f"/lead-finder/lists/{list_id}/add-to-leads", json_body=body)
        return _pa3_data(result)

    async def export_list(self, list_id: Any) -> Any:
        """Download a list as CSV text (at most 5,000 rows). Requires read scope."""
        return await self._http.request_text("GET", f"/lead-finder/lists/{list_id}/export")

    async def create_saved_search(self, name: Any, kind: Any, *, filters: Any = None) -> Any:
        """Store a set of filters to re-run later. Requires write scope."""
        body = {k: v for k, v in {"name": name, "kind": kind, "filters": filters}.items() if v is not None}
        result = await self._http.request("POST", "/lead-finder/saved-searches", json_body=body)
        return _pa3_data(result)

    async def get_saved_search(self, saved_search_id: Any) -> Any:
        """Read one saved search. Requires read scope."""
        result = await self._http.request("GET", f"/lead-finder/saved-searches/{saved_search_id}")
        return _pa3_data(result)

    async def update_saved_search(self, saved_search_id: Any, *, name: Any = None, alert_enabled: Any = None) -> Any:
        """Rename a saved search or switch its alert. Requires write scope."""
        body = {k: v for k, v in {"name": name, "alert_enabled": alert_enabled}.items() if v is not None}
        result = await self._http.request("PATCH", f"/lead-finder/saved-searches/{saved_search_id}", json_body=body)
        return _pa3_data(result)

    async def delete_saved_search(self, saved_search_id: Any) -> Any:
        """Delete a saved search. Requires write scope."""
        result = await self._http.request("DELETE", f"/lead-finder/saved-searches/{saved_search_id}")
        return _pa3_data(result)

    async def run_saved_search(self, saved_search_id: Any) -> Any:
        """Count the current matches of a saved search. Free: no reveal credits or search budget. Requires write scope."""
        result = await self._http.request("POST", f"/lead-finder/saved-searches/{saved_search_id}/run", json_body={})
        return _pa3_data(result)


def _pa3_data(result: Any) -> Any:
    if isinstance(result, dict) and "data" in result and "meta" not in result:
        return result["data"]
    return result
