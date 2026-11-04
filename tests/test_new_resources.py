"""Tests for all new SDK resource methods (0.4.0).

Uses MagicMock transport — no real HTTP calls.
"""

import sys
import os
from unittest.mock import MagicMock, call

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from foxreach.resources.warmup import WarmupResource
from foxreach.resources.lead_finder import LeadFinderResource
from foxreach.resources.managed_inboxes import ManagedInboxesResource
from foxreach.resources.tracking_domains import TrackingDomainsResource
from foxreach.resources.email_accounts import EmailAccountsResource
from foxreach.resources.leads import LeadsResource
from foxreach.resources.inbox import InboxResource
from foxreach.types import (
    EmailAccountCreate, EmailAccountUpdate, ReconnectRequest,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _http(return_value=None):
    m = MagicMock()
    m.request.return_value = return_value
    m.request_paginated.return_value = ([], {"page": 1, "page_size": 50, "total": 0, "total_pages": 0})
    return m


# ---------------------------------------------------------------------------
# Warmup: 4 methods
# ---------------------------------------------------------------------------

class TestWarmupResource:
    def test_get_pool_calls_correct_path(self):
        http = _http({"data": []})
        r = WarmupResource(http)
        result = r.get_pool()
        http.request.assert_called_once_with("GET", "/warmup/pool", params=None)
        assert isinstance(result, list)

    def test_get_pool_with_tag(self):
        http = _http({"data": []})
        r = WarmupResource(http)
        r.get_pool(tag="tag_abc")
        http.request.assert_called_once_with("GET", "/warmup/pool", params={"tag": "tag_abc"})

    def test_get_pool_parses_health_score_null(self):
        http = _http({"data": [{"accountId": "acc_1", "email": "a@b.com", "healthScore": None}]})
        r = WarmupResource(http)
        entries = r.get_pool()
        assert len(entries) == 1
        assert entries[0].health_score is None

    def test_get_pool_parses_health_score_value(self):
        http = _http({"data": [{"accountId": "acc_1", "email": "a@b.com", "healthScore": 78}]})
        r = WarmupResource(http)
        entries = r.get_pool()
        assert entries[0].health_score == 78

    def test_get_stats_calls_correct_path(self):
        http = _http({"data": {"totalAccounts": 5, "activeWarmupAccounts": 3,
                               "totalSent": 100, "totalReplied": 10,
                               "averageHealthScore": None, "healthMeasuredAccounts": 0}})
        r = WarmupResource(http)
        stats = r.get_stats()
        http.request.assert_called_once_with("GET", "/warmup/stats")
        assert stats.total_accounts == 5

    def test_get_stats_average_health_score_null(self):
        http = _http({"data": {"averageHealthScore": None, "healthMeasuredAccounts": 0,
                               "totalAccounts": 1, "activeWarmupAccounts": 1,
                               "totalSent": 0, "totalReplied": 0}})
        r = WarmupResource(http)
        stats = r.get_stats()
        assert stats.average_health_score is None
        assert stats.health_measured_accounts == 0

    def test_get_stats_average_health_score_value(self):
        http = _http({"data": {"averageHealthScore": 72.5, "healthMeasuredAccounts": 2,
                               "totalAccounts": 2, "activeWarmupAccounts": 2,
                               "totalSent": 40, "totalReplied": 5}})
        r = WarmupResource(http)
        stats = r.get_stats()
        assert stats.average_health_score == 72.5
        assert stats.health_measured_accounts == 2

    def test_get_logs_calls_correct_path(self):
        http = _http({"data": []})
        r = WarmupResource(http)
        logs = r.get_logs()
        http.request.assert_called_once_with("GET", "/warmup/logs")
        assert isinstance(logs, list)

    def test_get_logs_parses_entries(self):
        http = _http({"data": [{"id": "wl_1", "senderEmail": "a@b.com", "receiverEmail": "c@d.com",
                                 "status": "replied", "createdAt": "2026-10-01T10:00:00Z"}]})
        r = WarmupResource(http)
        logs = r.get_logs()
        assert len(logs) == 1
        assert logs[0].id == "wl_1"
        assert logs[0].sender_email == "a@b.com"
        assert logs[0].status == "replied"

    def test_get_tags_calls_correct_path(self):
        http = _http({"data": []})
        r = WarmupResource(http)
        tags = r.get_tags()
        http.request.assert_called_once_with("GET", "/warmup/tags")
        assert isinstance(tags, list)

    def test_get_tags_parses_entries(self):
        http = _http({"data": [{"id": "tag_1", "name": "Onboarding", "color": "#ff0000"}]})
        r = WarmupResource(http)
        tags = r.get_tags()
        assert len(tags) == 1
        assert tags[0].id == "tag_1"
        assert tags[0].name == "Onboarding"
        assert tags[0].color == "#ff0000"


# ---------------------------------------------------------------------------
# Lead Finder: 12 methods
# ---------------------------------------------------------------------------

class TestLeadFinderResource:
    def test_filter_options_calls_correct_path(self):
        http = _http({"data": {"industries": []}})
        r = LeadFinderResource(http)
        result = r.filter_options()
        http.request.assert_called_once_with("GET", "/lead-finder/filter-options")
        assert "industries" in result

    def test_count_calls_correct_path(self):
        http = _http({"data": {"total": 500}})
        r = LeadFinderResource(http)
        result = r.count({"jobTitle": "engineer"})
        http.request.assert_called_once_with("POST", "/lead-finder/count", json_body={"filters": {"jobTitle": "engineer"}})
        assert result.get("total") == 500

    def test_search_calls_correct_path(self):
        http = _http({"data": {"total": 10, "people": []}})
        r = LeadFinderResource(http)
        r.search({"jobTitle": "cto"}, page_size=10)
        args = http.request.call_args
        assert args[0][0] == "POST"
        assert args[0][1] == "/lead-finder/search"
        assert args[1]["json_body"]["pageSize"] == 10

    def test_search_with_page_token(self):
        http = _http({"data": {}})
        r = LeadFinderResource(http)
        r.search({}, page_size=25, page_token="tok_abc")
        body = http.request.call_args[1]["json_body"]
        assert body["pageToken"] == "tok_abc"

    def test_count_companies_calls_correct_path(self):
        http = _http({"data": {"total": 20}})
        r = LeadFinderResource(http)
        r.count_companies({"industry": "SaaS"})
        args = http.request.call_args
        assert args[0][1] == "/lead-finder/companies/count"

    def test_search_companies_calls_correct_path(self):
        http = _http({"data": {}})
        r = LeadFinderResource(http)
        r.search_companies({"industry": "SaaS"}, page_size=20)
        args = http.request.call_args
        assert args[0][1] == "/lead-finder/companies/search"

    def test_reveal_calls_correct_path(self):
        http = _http({"data": {"charged": 2}})
        r = LeadFinderResource(http)
        r.reveal([{"id": "p1"}, {"id": "p2"}])
        args = http.request.call_args
        assert args[0][0] == "POST"
        assert args[0][1] == "/lead-finder/reveal"

    def test_reveal_with_campaign_id(self):
        http = _http({"data": {}})
        r = LeadFinderResource(http)
        r.reveal([{"id": "p1"}], campaign_id="cmp_abc")
        body = http.request.call_args[1]["json_body"]
        assert body["campaignId"] == "cmp_abc"

    def test_add_to_leads_calls_correct_path(self):
        http = _http({"data": {"added": 1}})
        r = LeadFinderResource(http)
        r.add_to_leads(reveal_ids=["rev_1"])
        args = http.request.call_args
        assert args[0][0] == "POST"
        assert args[0][1] == "/lead-finder/add-to-leads"
        assert args[1]["json_body"]["revealIds"] == ["rev_1"]

    def test_list_reveals_calls_correct_path(self):
        http = _http({"data": {"reveals": []}})
        r = LeadFinderResource(http)
        r.list_reveals(month="2026-10", page=1, page_size=25)
        args = http.request.call_args
        assert args[0][0] == "GET"
        assert args[0][1] == "/lead-finder/reveals"
        assert args[1]["params"]["month"] == "2026-10"

    def test_get_reveal_batch_calls_correct_path(self):
        http = _http({"data": {"batchId": "bat_1", "reveals": [], "pending": 0,
                               "found": 0, "notFound": 0, "errors": 0, "balance": 10}})
        r = LeadFinderResource(http)
        batch = r.get_reveal_batch("bat_1")
        args = http.request.call_args
        assert args[0][1] == "/lead-finder/reveals/bat_1"
        assert batch.batch_id == "bat_1"

    def test_credits_calls_correct_path(self):
        http = _http({"data": {"balance": 50, "monthlyIncluded": 100,
                               "searchPagesUsedToday": 0, "searchPagesAllowedToday": 5,
                               "searchPagesPerReveal": 1, "creditsPerPack": 500,
                               "pricePerPackCents": 9900, "allowedCountries": [],
                               "blockedCountries": [], "coverage": "global"}})
        r = LeadFinderResource(http)
        creds = r.credits()
        http.request.assert_called_once_with("GET", "/lead-finder/credits")
        assert creds.balance == 50
        assert creds.monthly_included == 100

    def test_list_lead_finder_lists_calls_correct_path(self):
        http = _http({"data": {"lists": [{"id": "l_1", "name": "SaaS CTOs", "kind": "people", "itemCount": 10}]}})
        r = LeadFinderResource(http)
        items = r.list_lead_finder_lists()
        http.request.assert_called_once_with("GET", "/lead-finder/lists", params=None)
        assert len(items) == 1
        assert items[0].id == "l_1"
        assert items[0].item_count == 10

    def test_list_saved_searches_calls_correct_path(self):
        http = _http({"data": {"savedSearches": [{"id": "ss_1", "name": "Devs", "lastCount": 200}]}})
        r = LeadFinderResource(http)
        items = r.list_saved_searches()
        http.request.assert_called_once_with("GET", "/lead-finder/saved-searches")
        assert len(items) == 1
        assert items[0].name == "Devs"
        assert items[0].last_count == 200


# ---------------------------------------------------------------------------
# Managed Inboxes: 8 methods
# ---------------------------------------------------------------------------

class TestManagedInboxesResource:
    def test_config_calls_correct_path(self):
        http = _http({"data": {"platforms": [], "maxMailboxesPerDomain": 5,
                               "maxDomainsPerOrder": 10, "registrationYears": 1,
                               "defaultDailyLimit": 30}})
        r = ManagedInboxesResource(http)
        cfg = r.config()
        http.request.assert_called_once_with("GET", "/managed-inboxes/config")
        assert cfg.max_mailboxes_per_domain == 5

    def test_check_domain_calls_correct_path(self):
        http = _http({"data": {"domain": "test.com", "available": True}})
        r = ManagedInboxesResource(http)
        result = r.check_domain("test.com")
        args = http.request.call_args
        assert args[0][1] == "/managed-inboxes/domains/check"
        assert args[1]["params"]["domain"] == "test.com"

    def test_search_domains_calls_correct_path(self):
        http = _http({"data": []})
        r = ManagedInboxesResource(http)
        r.search_domains("mybrand")
        args = http.request.call_args
        assert args[0][1] == "/managed-inboxes/domains/search"
        assert args[1]["params"]["q"] == "mybrand"

    def test_suggest_domains_calls_correct_path(self):
        http = _http({"data": {"items": []}})
        r = ManagedInboxesResource(http)
        r.suggest_domains("mybrand.com", limit=5)
        args = http.request.call_args
        assert args[0][1] == "/managed-inboxes/domains/suggest"
        assert args[1]["params"]["limit"] == 5

    def test_quote_order_calls_correct_path(self):
        http = _http({"data": {"totalCents": 2000}})
        r = ManagedInboxesResource(http)
        result = r.quote_order({"domains": ["test.com"]})
        args = http.request.call_args
        assert args[0][0] == "POST"
        assert args[0][1] == "/managed-inboxes/orders/quote"
        assert result.get("totalCents") == 2000

    def test_list_orders_calls_correct_path(self):
        http = _http({"data": {"items": []}})
        r = ManagedInboxesResource(http)
        orders = r.list_orders()
        http.request.assert_called_once_with("GET", "/managed-inboxes/orders")
        assert isinstance(orders, list)

    def test_get_order_calls_correct_path(self):
        http = _http({"data": {"id": "ord_1", "status": "active", "totalCents": 999}})
        r = ManagedInboxesResource(http)
        order = r.get_order("ord_1")
        args = http.request.call_args
        assert args[0][1] == "/managed-inboxes/orders/ord_1"
        assert order.id == "ord_1"

    def test_list_mailboxes_calls_correct_path(self):
        http = _http({"data": {"items": [{"id": "mb_1", "email": "hello@test.com", "status": "active"}]}})
        r = ManagedInboxesResource(http)
        mailboxes = r.list_mailboxes()
        http.request.assert_called_once_with("GET", "/managed-inboxes/mailboxes")
        assert len(mailboxes) == 1
        assert mailboxes[0].id == "mb_1"


# ---------------------------------------------------------------------------
# Tracking Domains: 4 methods
# ---------------------------------------------------------------------------

class TestTrackingDomainsResource:
    def test_list_calls_correct_path(self):
        http = _http({"data": {"domains": [], "defaultDomain": "track.foxreach.io", "configured": True}})
        r = TrackingDomainsResource(http)
        result = r.list()
        http.request.assert_called_once_with("GET", "/tracking-domains")
        assert "domains" in result

    def test_add_calls_correct_path(self):
        http = _http({"data": {"id": "td_1", "domain": "track.mybrand.com", "status": "pending",
                               "cnameTarget": "cname.foxreach.io"}})
        r = TrackingDomainsResource(http)
        td = r.add("track.mybrand.com")
        args = http.request.call_args
        assert args[0][0] == "POST"
        assert args[0][1] == "/tracking-domains"
        assert args[1]["json_body"] == {"domain": "track.mybrand.com"}
        assert td.id == "td_1"
        assert td.cname_target == "cname.foxreach.io"

    def test_verify_calls_correct_path(self):
        http = _http({"data": {"id": "td_1", "domain": "track.mybrand.com", "status": "verified"}})
        r = TrackingDomainsResource(http)
        td = r.verify("td_1")
        args = http.request.call_args
        assert args[0][0] == "POST"
        assert args[0][1] == "/tracking-domains/td_1/verify"
        assert td.status == "verified"

    def test_delete_calls_correct_path(self):
        http = _http(None)
        r = TrackingDomainsResource(http)
        r.delete("td_1")
        args = http.request.call_args
        assert args[0][0] == "DELETE"
        assert args[0][1] == "/tracking-domains/td_1"


# ---------------------------------------------------------------------------
# EmailAccounts: 8 new methods
# ---------------------------------------------------------------------------

_ACCOUNT_DATA = {
    "id": "acc_1", "email": "test@example.com", "provider": "other",
    "displayName": None, "dailyLimit": 50, "sentToday": 0,
    "warmupEnabled": False, "warmupDailyLimit": 5, "warmupRampUpDays": 30,
    "healthScore": None, "bounceRate": 0.0, "replyRate": 0.0,
    "isActive": True, "connectionStatus": "ok",
    "createdAt": "2026-01-01T00:00:00Z", "updatedAt": "2026-01-01T00:00:00Z",
    "smtpHost": "smtp.test.com", "smtpPort": 587, "imapHost": "imap.test.com", "imapPort": 993,
    "timezone": "UTC",
}


class TestEmailAccountsExtended:
    def test_create_calls_correct_path(self):
        http = _http({"data": _ACCOUNT_DATA})
        r = EmailAccountsResource(http)
        data = EmailAccountCreate(
            email="test@example.com", password="pass",
            smtp_host="smtp.test.com", smtp_port=587,
            imap_host="imap.test.com", imap_port=993,
        )
        account = r.create(data)
        args = http.request.call_args
        assert args[0][0] == "POST"
        assert args[0][1] == "/email-accounts"
        assert account.id == "acc_1"

    def test_update_calls_correct_path(self):
        http = _http({"data": _ACCOUNT_DATA})
        r = EmailAccountsResource(http)
        account = r.update("acc_1", EmailAccountUpdate(daily_limit=100))
        args = http.request.call_args
        assert args[0][0] == "PATCH"
        assert args[0][1] == "/email-accounts/acc_1"
        assert account.id == "acc_1"

    def test_reconnect_calls_correct_path(self):
        http = _http({"data": _ACCOUNT_DATA})
        r = EmailAccountsResource(http)
        r.reconnect("acc_1", ReconnectRequest(password="newpass"))
        args = http.request.call_args
        assert args[0][0] == "POST"
        assert args[0][1] == "/email-accounts/acc_1/reconnect"
        assert args[1]["json_body"]["password"] == "newpass"

    def test_enable_warmup_calls_correct_path(self):
        http = _http({"data": _ACCOUNT_DATA})
        r = EmailAccountsResource(http)
        r.enable_warmup("acc_1")
        args = http.request.call_args
        assert args[0][0] == "POST"
        assert args[0][1] == "/email-accounts/acc_1/warmup/enable"

    def test_disable_warmup_calls_correct_path(self):
        http = _http({"data": _ACCOUNT_DATA})
        r = EmailAccountsResource(http)
        r.disable_warmup("acc_1")
        args = http.request.call_args
        assert args[0][0] == "POST"
        assert args[0][1] == "/email-accounts/acc_1/warmup/disable"

    def test_health_calls_correct_path(self):
        http = _http({"data": {"healthScore": None, "warmupEnabled": True}})
        r = EmailAccountsResource(http)
        h = r.health("acc_1")
        args = http.request.call_args
        assert args[0][0] == "GET"
        assert args[0][1] == "/email-accounts/acc_1/health"
        assert h.health_score is None

    def test_health_score_null_when_api_returns_null(self):
        http = _http({"data": {"healthScore": None}})
        r = EmailAccountsResource(http)
        h = r.health("acc_1")
        assert h.health_score is None

    def test_health_score_value_when_measured(self):
        http = _http({"data": {"healthScore": 85}})
        r = EmailAccountsResource(http)
        h = r.health("acc_1")
        assert h.health_score == 85

    def test_warmup_detail_calls_correct_path(self):
        http = _http({"data": {"progress": 20, "poolStats": {}}})
        r = EmailAccountsResource(http)
        result = r.warmup_detail("acc_1")
        args = http.request.call_args
        assert args[0][0] == "GET"
        assert args[0][1] == "/email-accounts/acc_1/warmup"
        assert isinstance(result, dict)

    def test_google_oauth_start_calls_correct_path(self):
        http = _http({"data": {"url": "https://accounts.google.com/o/oauth2/auth?..."}})
        r = EmailAccountsResource(http)
        result = r.google_oauth_start()
        args = http.request.call_args
        assert args[0][0] == "POST"
        assert args[0][1] == "/email-accounts/google-oauth/start"
        assert "url" in result


# ---------------------------------------------------------------------------
# Leads: list_tags
# ---------------------------------------------------------------------------

class TestLeadsExtended:
    def test_list_tags_calls_correct_path(self):
        http = _http({"data": [{"name": "hot", "count": 5}, {"name": "cold", "count": 3}]})
        r = LeadsResource(http)
        tags = r.list_tags()
        http.request.assert_called_once_with("GET", "/leads/tags")
        assert len(tags) == 2
        assert tags[0].name == "hot"
        assert tags[0].count == 5

    def test_list_tags_returns_empty_list_on_empty_response(self):
        http = _http({"data": []})
        r = LeadsResource(http)
        tags = r.list_tags()
        assert tags == []


# ---------------------------------------------------------------------------
# Inbox: delete
# ---------------------------------------------------------------------------

class TestInboxExtended:
    def test_delete_calls_correct_path(self):
        http = _http(None)
        r = InboxResource(http)
        r.delete("rpl_abc")
        args = http.request.call_args
        assert args[0][0] == "DELETE"
        assert args[0][1] == "/inbox/threads/rpl_abc"


class TestWorkspacesAndActingAs:
    def test_workspaces_list_path_and_shape(self):
        from foxreach.resources.workspaces import WorkspacesResource

        http = _http({"data": [{"id": "w1", "name": "A", "is_agency_client": False}]})
        rows = WorkspacesResource(http).list()
        http.request.assert_called_once_with("GET", "/workspaces")
        assert rows[0]["id"] == "w1"

    def test_workspace_id_sets_header(self):
        from foxreach import FoxReach

        client = FoxReach(api_key="otr_x", workspace_id="ws_client")
        assert client._http._client.headers["X-Workspace-Id"] == "ws_client"
        assert client.workspaces is not None

    def test_no_header_by_default(self):
        from foxreach import FoxReach

        assert "X-Workspace-Id" not in FoxReach(api_key="otr_x")._http._client.headers

    def test_async_workspace_id_sets_header(self):
        from foxreach import AsyncFoxReach

        client = AsyncFoxReach(api_key="otr_x", workspace_id="ws_client")
        assert client._http._client.headers["X-Workspace-Id"] == "ws_client"


class TestCopyResource:
    def test_judge_posts_draft(self):
        from foxreach.resources.copy import CopyResource
        http = _http({"data": {"verdict": {"score": 90}}})
        result = CopyResource(http).judge("Hi", "Body", step_number=2)
        http.request.assert_called_once_with(
            "POST", "/copy/judge",
            json_body={"subject": "Hi", "body": "Body", "sendAsHtml": False, "stepNumber": 2},
        )
        assert result["verdict"]["score"] == 90

    def test_rewrite_defaults_to_whole_email(self):
        from foxreach.resources.copy import CopyResource
        http = _http({"data": {"kind": "email"}})
        CopyResource(http).rewrite("Hi", "Body")
        assert http.request.call_args.args == ("POST", "/copy/rewrite")
        assert http.request.call_args.kwargs["json_body"]["target"] == {"kind": "email"}


class TestDraftsResource:
    def test_paths_and_bodies(self):
        http = _http({"data": {"id": "r1"}})
        r = InboxResource(http)
        r.drafts.update("r1", "New")
        http.request.assert_called_with("PATCH", "/inbox/threads/r1/draft", json_body={"draftReply": "New"})
        r.drafts.send("r1")
        http.request.assert_called_with("POST", "/inbox/threads/r1/draft/send")
        r.drafts.regenerate("r1")
        http.request.assert_called_with("POST", "/inbox/threads/r1/draft/regenerate")
        r.drafts.dismiss("r1")
        http.request.assert_called_with("POST", "/inbox/threads/r1/draft/dismiss")
        r.drafts.get("r1")
        http.request.assert_called_with("GET", "/inbox/threads/r1/draft")


# ---------------------------------------------------------------------------
# Block list: 6 methods
# ---------------------------------------------------------------------------

class TestBlockListResource:
    def test_list_calls_correct_path_and_params(self):
        from foxreach.resources.block_list import BlockListResource
        http = MagicMock()
        http.request_paginated.return_value = (
            [{"id": "b1", "kind": "domain", "value": "acme.com", "source": "api", "created_at": "t"}],
            {"page": 1, "page_size": 50, "total": 1, "total_pages": 1},
        )
        page = BlockListResource(http).list(kind="domain", search="acme")
        args = http.request_paginated.call_args
        assert args[0][0] == "/block-list"
        assert args[1]["params"] == {"page": 1, "pageSize": 50, "search": "acme", "kind": "domain"}
        assert page.data[0].value == "acme.com" and page.data[0].kind == "domain"

    def test_add_and_bulk_add(self):
        from foxreach.resources.block_list import BlockListResource
        http = _http({"data": {"id": "b1", "kind": "email", "value": "a@x.com", "source": "api"}})
        entry = BlockListResource(http).add("a@x.com", note="n")
        args = http.request.call_args
        assert args[0][:2] == ("POST", "/block-list")
        assert args[1]["json_body"] == {"value": "a@x.com", "note": "n"}
        assert entry.id == "b1"
        http = _http({"data": {"created": 2, "duplicates": 1, "invalid": 1, "invalid_details": [{"value": "x"}]}})
        res = BlockListResource(http).bulk_add(["a@x.com", "b.com"])
        assert http.request.call_args[0][:2] == ("POST", "/block-list/bulk")
        assert (res.created, res.duplicates, res.invalid) == (2, 1, 1)

    def test_remove_bulk_remove_export(self):
        from foxreach.resources.block_list import BlockListResource
        http = _http(None)
        BlockListResource(http).remove("b1")
        assert http.request.call_args[0][:2] == ("DELETE", "/block-list/b1")
        http = _http({"data": {"deleted": 3}})
        assert BlockListResource(http).bulk_remove(["a", "b", "c"]) == 3
        assert http.request.call_args[0][:2] == ("POST", "/block-list/bulk-delete")
        assert http.request.call_args[1]["json_body"] == {"ids": ["a", "b", "c"]}
        http = MagicMock()
        http.request_text.return_value = "value,kind\n"
        assert BlockListResource(http).export(kind="email") == "value,kind\n"
        assert http.request_text.call_args[0][:2] == ("GET", "/block-list/export")


# ---------------------------------------------------------------------------
# Leads: bulk actions, export, variables (pa1)
# ---------------------------------------------------------------------------

class TestLeadsBulk:
    JOB = {"data": {"id": "j1", "type": "lead_bulk", "status": "completed", "totalItems": 2,
                    "completedItems": 2, "result": {"deleted": 2}}}

    def test_bulk_delete_by_ids(self):
        http = _http(self.JOB)
        job = LeadsResource(http).bulk_delete(lead_ids=["a", "b"])
        http.request.assert_called_once_with("POST", "/leads/bulk/delete", json_body={"leadIds": ["a", "b"]})
        assert (job.id, job.status, job.result) == ("j1", "completed", {"deleted": 2})

    def test_bulk_tag_by_filter(self):
        http = _http(self.JOB)
        LeadsResource(http).bulk_tag(["hot"], filter={"search": "acme"})
        http.request.assert_called_once_with(
            "POST", "/leads/bulk/tag", json_body={"filter": {"search": "acme"}, "tags": ["hot"]})

    def test_bulk_untag_and_verify_paths(self):
        http = _http(self.JOB)
        r = LeadsResource(http)
        r.bulk_untag(["hot"], lead_ids=["a"])
        r.bulk_verify(lead_ids=["a"])
        paths = [c.args[1] for c in http.request.call_args_list]
        assert paths == ["/leads/bulk/untag", "/leads/bulk/verify"]

    def test_selection_requires_exactly_one(self):
        r = LeadsResource(_http(self.JOB))
        with pytest.raises(ValueError):
            r.bulk_delete()
        with pytest.raises(ValueError):
            r.bulk_delete(lead_ids=["a"], filter={})

    def test_impact_export_download_variables(self):
        http = _http({"data": {"campaigns": [], "leadsInCampaigns": 0}})
        http.request_text.return_value = "email\n"
        r = LeadsResource(http)
        assert r.bulk_delete_impact(lead_ids=["a"]) == {"campaigns": [], "leadsInCampaigns": 0}
        r.export(tags="q4")
        http.request.assert_called_with("POST", "/leads/export", json_body={"tags": "q4"})
        assert r.download_export("j9") == "email\n"
        http.request_text.assert_called_once_with("GET", "/leads/export/j9/download")
        r.variables()
        http.request.assert_called_with("GET", "/leads/variables")


# ---------------------------------------------------------------------------
# Sequence variants (pa1)
# ---------------------------------------------------------------------------

class TestSequenceVariants:
    VARIANT = {"data": {"id": "v1", "sequenceId": "s1", "label": "A", "subject": "S", "body": "B",
                        "weight": 2, "sendAsHtml": True}}

    def test_create_sends_the_given_fields(self):
        from foxreach.resources.campaigns import SequencesResource
        from foxreach.types import VariantCreate

        http = _http(self.VARIANT)
        v = SequencesResource(http).create_variant("c1", "s1", VariantCreate(subject="S", body="B", weight=2, send_as_html=True))
        http.request.assert_called_once_with(
            "POST", "/campaigns/c1/sequences/s1/variants",
            json_body={"subject": "S", "body": "B", "label": "A", "weight": 2, "send_as_html": True})
        assert (v.id, v.sequence_id, v.weight, v.send_as_html) == ("v1", "s1", 2, True)

    def test_update_sends_only_given_fields(self):
        from foxreach.resources.campaigns import SequencesResource
        from foxreach.types import VariantUpdate

        http = _http(self.VARIANT)
        SequencesResource(http).update_variant("c1", "s1", "v1", VariantUpdate(weight=3))
        http.request.assert_called_once_with(
            "PATCH", "/campaigns/c1/sequences/s1/variants/v1", json_body={"weight": 3})

    def test_list_delete_and_stats(self):
        from foxreach.resources.campaigns import SequencesResource

        http = _http({"data": [{"variantId": "v1", "label": "A", "sent": 4, "openRate": 50.0, "replyRate": 25.0}]})
        r = SequencesResource(http)
        stats = r.variant_stats("c1", "s1")
        assert (stats[0].variant_id, stats[0].sent, stats[0].open_rate, stats[0].reply_rate) == ("v1", 4, 50.0, 25.0)
        assert http.request.call_args[0][:2] == ("GET", "/campaigns/c1/sequences/s1/variant-stats")
        r.delete_variant("c1", "s1", "v1")
        assert http.request.call_args[0][:2] == ("DELETE", "/campaigns/c1/sequences/s1/variants/v1")
        http.request.return_value = {"data": [{"id": "v1", "sequenceId": "s1", "label": "B"}]}
        listed = r.list_variants("c1", "s1")
        assert http.request.call_args[0][:2] == ("GET", "/campaigns/c1/sequences/s1/variants")
        assert [(v.id, v.label) for v in listed] == [("v1", "B")]


class TestCampaignOperations:
    def test_each_method_reaches_its_route(self):
        from foxreach.resources.campaigns import CampaignsResource

        http = _http({"data": {"id": "c2", "name": "x (Copy)", "status": "draft"}})
        r = CampaignsResource(http)
        copy = r.duplicate("c1")
        assert http.request.call_args[0][:2] == ("POST", "/campaigns/c1/duplicate") and copy.status == "draft"

        http.request.return_value = {"data": {"share_slug": "s", "share_url": "https://x/r/s"}}
        assert r.share("c1")["share_url"] == "https://x/r/s"
        assert http.request.call_args[0][:2] == ("POST", "/campaigns/c1/share")
        r.unshare("c1")
        assert http.request.call_args[0][:2] == ("DELETE", "/campaigns/c1/share")

        r.preview("c1", "s", "b", lead_id="l1")
        assert http.request.call_args.kwargs["json_body"] == {"subject": "s", "body": "b", "lead_id": "l1"}
        r.send_test_email("c1", to_email="a@b.test", account_id="acc", subject="s", body="b", preheader="p")
        assert http.request.call_args[0][:2] == ("POST", "/campaigns/c1/test-email")
        assert http.request.call_args.kwargs["json_body"] == {
            "to_email": "a@b.test", "account_id": "acc", "subject": "s", "body": "b", "is_html": False, "preheader": "p"}
        r.bulk_remove_leads("c1", ["l1"])
        assert http.request.call_args[0][:2] == ("POST", "/campaigns/c1/leads/bulk-remove")
        assert http.request.call_args.kwargs["json_body"] == {"lead_ids": ["l1"]}

        r.activity("c1", type="reply", account_id="a1", page_size=10)
        assert http.request.call_args[0][:2] == ("GET", "/campaigns/c1/activity")
        assert http.request.call_args.kwargs["params"] == {"type": "reply", "accountId": "a1", "page": 1, "pageSize": 10}
        http.request.return_value = {"data": [{"date": "2026-11-01", "sent": 2}]}
        assert r.cohorts("c1", days=7)[0]["sent"] == 2
        assert http.request.call_args.kwargs["params"] == {"days": 7}
        http.request.return_value = {"data": {"date": "2026-11-01", "emails": []}}
        assert r.cohort_detail("c1", "2026-11-01")["emails"] == []
        assert http.request.call_args[0][:2] == ("GET", "/campaigns/c1/cohorts/2026-11-01")
        http.request.return_value = {"data": [{"id": "e1"}]}
        assert r.lead_emails("c1", "l1")[0]["id"] == "e1"
        assert http.request.call_args[0][:2] == ("GET", "/campaigns/c1/leads/l1/emails")


class TestInboxActions:
    def test_mark_read_and_mark_all_read(self):
        http = _http({"data": {"id": "r1", "isRead": True}})
        InboxResource(http).mark_read("r1")
        http.request.assert_called_with("POST", "/inbox/threads/r1/mark-read")
        http = _http({"data": {"updated": 3}})
        assert InboxResource(http).mark_all_read(category="interested") == {"updated": 3}
        http.request.assert_called_with("POST", "/inbox/mark-all-read", json_body={"category": "interested"})
        InboxResource(http).mark_all_read()
        http.request.assert_called_with("POST", "/inbox/mark-all-read", json_body={})

    def test_bulk_update_drops_unset_fields_and_bulk_delete(self):
        http = _http({"data": {"updated": 2}})
        InboxResource(http).bulk_update(["a", "b"], is_read=True, category=None)
        http.request.assert_called_with("POST", "/inbox/threads/bulk-update", json_body={"ids": ["a", "b"], "isRead": True})
        http = _http({"data": {"deleted": 2}})
        assert InboxResource(http).bulk_delete(["a", "b"]) == {"deleted": 2}
        http.request.assert_called_with("POST", "/inbox/threads/bulk-delete", json_body={"ids": ["a", "b"]})

    def test_notes_and_sent(self):
        http = _http({"data": [{"id": "n1"}]})
        assert InboxResource(http).list_notes("r1") == [{"id": "n1"}]
        http.request.assert_called_with("GET", "/inbox/threads/r1/notes")
        InboxResource(http).add_note("r1", "hello")
        http.request.assert_called_with("POST", "/inbox/threads/r1/notes", json_body={"content": "hello"})
        InboxResource(http).delete_note("n1")
        http.request.assert_called_with("DELETE", "/inbox/notes/n1")
        InboxResource(http).list_sent(campaign_id="c1", search="x")
        args = http.request_paginated.call_args
        assert args[0][0] == "/inbox/sent"
        assert {k: v for k, v in args[1]["params"].items() if v is not None} == {"page": 1, "pageSize": 50, "campaignId": "c1", "search": "x"}


class TestWebhookOpsAndEvents:
    def test_test_and_deliveries(self):
        from foxreach.resources.webhooks import WebhooksResource
        http = _http({"data": {"success": True, "statusCode": 200, "durationMs": 12}})
        assert WebhooksResource(http).test("w1")["success"] is True
        http.request.assert_called_with("POST", "/webhooks/w1/test")
        http = MagicMock()
        http.request_paginated.return_value = ([], {"page": 1, "page_size": 50, "total": 0, "total_pages": 0})
        WebhooksResource(http).deliveries("w1", status="failed")
        args = http.request_paginated.call_args
        assert args[0][0] == "/webhooks/w1/deliveries"
        assert {k: v for k, v in args[1]["params"].items() if v is not None} == {"page": 1, "pageSize": 50, "status": "failed"}

    def test_events_list(self):
        from foxreach.resources.events import EventsResource
        http = MagicMock()
        http.request_paginated.return_value = ([], {"page": 1, "page_size": 50, "total": 0, "total_pages": 0})
        EventsResource(http).list(type="lead.created", start_date="2026-11-01T00:00:00Z")
        args = http.request_paginated.call_args
        assert args[0][0] == "/events"
        assert {k: v for k, v in args[1]["params"].items() if v is not None} == {
            "page": 1, "pageSize": 50, "type": "lead.created", "startDate": "2026-11-01T00:00:00Z"}


class TestWorkspaceTeamAndApiKeys:
    def test_team_calls(self):
        from foxreach.resources.workspace import WorkspaceResource
        http = _http({"data": {"id": "m1"}})
        r = WorkspaceResource(http)
        r.invite("a@x.com", role="admin")
        http.request.assert_called_with("POST", "/workspace/members/invite", json_body={"email": "a@x.com", "role": "admin"})
        r.update_member_role("m1", "member")
        http.request.assert_called_with("PATCH", "/workspace/members/m1", json_body={"role": "member"})
        r.remove_member("m1")
        http.request.assert_called_with("DELETE", "/workspace/members/m1")
        r.revoke_invite("i1")
        http.request.assert_called_with("DELETE", "/workspace/invites/i1")
        r.resend_invite("i1")
        http.request.assert_called_with("POST", "/workspace/invites/i1/resend")
        r.update(name="N")
        http.request.assert_called_with("PATCH", "/workspace", json_body={"name": "N"})
        r.update_defaults(daily_limit=40, sending_start_hour=8)
        http.request.assert_called_with("PATCH", "/workspace/defaults", json_body={"dailyLimit": 40, "sendingStartHour": 8})

    def test_members_page_and_api_keys(self):
        from foxreach.resources.api_keys import ApiKeysResource
        from foxreach.resources.workspace import WorkspaceResource
        http = MagicMock()
        http.request_paginated.return_value = ([], {"page": 1, "page_size": 50, "total": 0, "total_pages": 0})
        WorkspaceResource(http).members(page=2, page_size=10)
        assert http.request_paginated.call_args[0][0] == "/workspace/members"
        ApiKeysResource(http).list()
        assert http.request_paginated.call_args[0][0] == "/api-keys"
        http = _http({"data": {"id": "k1", "key": "otr_x"}})
        out = ApiKeysResource(http).create("ci", scopes=["read"])
        http.request.assert_called_with("POST", "/api-keys", json_body={"name": "ci", "scopes": ["read"]})
        assert out["key"] == "otr_x"
        ApiKeysResource(http).create("ci2")
        http.request.assert_called_with("POST", "/api-keys", json_body={"name": "ci2"})
        ApiKeysResource(http).revoke("k1")
        http.request.assert_called_with("DELETE", "/api-keys/k1")
