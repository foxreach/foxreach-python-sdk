"""jobs resource: request shape and parsing (MagicMock transport)."""

import os
import sys
from unittest.mock import MagicMock

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from foxreach.resources.jobs import JobsResource  # noqa: E402


def test_get_parses_camel_case_job():
    http = MagicMock()
    http.request.return_value = {"data": {
        "id": "j1", "type": "lead_import", "status": "running", "progress": 40,
        "totalItems": 10, "completedItems": 4, "result": None, "error": None,
        "startedAt": None, "completedAt": None, "createdAt": "2026-11-04T09:00:00",
    }}
    job = JobsResource(http).get("j1")
    http.request.assert_called_once_with("GET", "/jobs/j1")
    assert (job.total_items, job.completed_items, job.created_at) == (10, 4, "2026-11-04T09:00:00")


def test_list_sends_filters_as_query():
    http = MagicMock()
    http.request_paginated.return_value = ([], {"page": 1, "pageSize": 25, "total": 0, "totalPages": 1})
    JobsResource(http).list(type="email_verification", status="failed")
    args = http.request_paginated.call_args
    assert args[0][0] == "/jobs"
    assert args[1]["params"] == {"page": 1, "pageSize": 25, "type": "email_verification", "status": "failed"}


def test_client_me_parses_response():
    from foxreach import FoxReach

    client = FoxReach(api_key="otr_test")
    client._http = MagicMock()
    client._http.request.return_value = {"data": {
        "key": {"id": "k1"}, "workspace": {"id": "ws1"}, "plan": {"name": "free"},
        "rate_limit": {"scope": "workspace", "buckets": {"read": {"limit_per_minute": 300}}}, "credits": {},
    }}
    me = client.me()
    client._http.request.assert_called_once_with("GET", "/me")
    assert (me.workspace["id"], me.plan["name"], me.rate_limit["buckets"]["read"]["limit_per_minute"]) == ("ws1", "free", 300)
