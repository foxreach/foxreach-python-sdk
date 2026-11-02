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
