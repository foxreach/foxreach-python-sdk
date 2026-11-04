import sys, os
from unittest.mock import MagicMock

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from foxreach.resources.analytics import AnalyticsResource


def test_account_calls_get_analytics_accounts_id_1():
    http = MagicMock()
    http.request.return_value = {"data": {"ok": True}}
    http.request_text.return_value = "csv"
    r = AnalyticsResource(http)
    r.account("id_1")
    call = (http.request_text if False else http.request).call_args
    assert call.args[0] == "GET"
    assert call.args[1] == "/analytics/accounts/id_1"


def test_report_calls_get_analytics_reports():
    http = MagicMock()
    http.request.return_value = {"data": {"ok": True}}
    http.request_text.return_value = "csv"
    r = AnalyticsResource(http)
    r.report()
    call = (http.request_text if False else http.request).call_args
    assert call.args[0] == "GET"
    assert call.args[1] == "/analytics/reports"


def test_export_report_calls_get_analytics_reports_export():
    http = MagicMock()
    http.request.return_value = {"data": {"ok": True}}
    http.request_text.return_value = "csv"
    r = AnalyticsResource(http)
    r.export_report()
    call = (http.request_text if True else http.request).call_args
    assert call.args[0] == "GET"
    assert call.args[1] == "/analytics/reports/export"


def test_leaderboard_calls_get_analytics_leaderboard():
    http = MagicMock()
    http.request.return_value = {"data": {"ok": True}}
    http.request_text.return_value = "csv"
    r = AnalyticsResource(http)
    r.leaderboard()
    call = (http.request_text if False else http.request).call_args
    assert call.args[0] == "GET"
    assert call.args[1] == "/analytics/leaderboard"


def test_activity_calls_get_analytics_activity():
    http = MagicMock()
    http.request.return_value = {"data": {"ok": True}}
    http.request_text.return_value = "csv"
    r = AnalyticsResource(http)
    r.activity()
    call = (http.request_text if False else http.request).call_args
    assert call.args[0] == "GET"
    assert call.args[1] == "/analytics/activity"


def test_campaign_daily_calls_get_analytics_campaigns_id_1_daily():
    http = MagicMock()
    http.request.return_value = {"data": {"ok": True}}
    http.request_text.return_value = "csv"
    r = AnalyticsResource(http)
    r.campaign_daily("id_1")
    call = (http.request_text if False else http.request).call_args
    assert call.args[0] == "GET"
    assert call.args[1] == "/analytics/campaigns/id_1/daily"


def test_campaign_steps_calls_get_analytics_campaigns_id_1_steps():
    http = MagicMock()
    http.request.return_value = {"data": {"ok": True}}
    http.request_text.return_value = "csv"
    r = AnalyticsResource(http)
    r.campaign_steps("id_1")
    call = (http.request_text if False else http.request).call_args
    assert call.args[0] == "GET"
    assert call.args[1] == "/analytics/campaigns/id_1/steps"
