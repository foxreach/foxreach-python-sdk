"""Assert that the Python SDK inbox resource calls the canonical /inbox/threads/{id} paths.

These tests fail without the path fix in resources/inbox.py -- before the fix,
get() called /inbox/{reply_id} and update() called /inbox/{reply_id}, both of
which are 404s against the real API.
"""

import sys
import os
from unittest.mock import MagicMock, patch
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from foxreach.resources.inbox import InboxResource, AsyncInboxResource
from foxreach.types import ThreadUpdate
from foxreach._http import _keys_to_camel, _keys_to_snake


def _make_http(return_value=None):
    http = MagicMock()
    http.request.return_value = return_value or {"data": {"id": "rpl_1"}}
    return http


def test_get_calls_threads_path():
    http = _make_http()
    resource = InboxResource(http)
    resource.get("rpl_abc")
    http.request.assert_called_once()
    args = http.request.call_args
    assert args[0][0] == "GET"
    assert args[0][1] == "/inbox/threads/rpl_abc", (
        f"Expected /inbox/threads/rpl_abc, got {args[0][1]}"
    )


def test_update_calls_threads_path():
    http = _make_http()
    resource = InboxResource(http)
    resource.update("rpl_abc", ThreadUpdate(is_read=True))
    http.request.assert_called_once()
    args = http.request.call_args
    assert args[0][0] == "PATCH"
    assert args[0][1] == "/inbox/threads/rpl_abc", (
        f"Expected /inbox/threads/rpl_abc, got {args[0][1]}"
    )


def test_list_leads_calls_correct_path():
    http = _make_http({"data": [], "meta": {"total": 0, "page": 1, "pageSize": 50, "totalPages": 0}})
    from foxreach.resources.campaigns import CampaignsResource
    resource = CampaignsResource(http)
    resource.list_leads("cmp_abc")
    http.request.assert_called_once()
    args = http.request.call_args
    assert args[0][0] == "GET"
    assert args[0][1] == "/campaigns/cmp_abc/leads"


def test_list_accounts_calls_correct_path():
    http = _make_http({"data": []})
    from foxreach.resources.campaigns import CampaignsResource
    resource = CampaignsResource(http)
    resource.list_accounts("cmp_abc")
    http.request.assert_called_once()
    args = http.request.call_args
    assert args[0][0] == "GET"
    assert args[0][1] == "/campaigns/cmp_abc/accounts"


def test_get_esp_mix_calls_correct_path():
    http = _make_http({"data": {}})
    from foxreach.resources.campaigns import CampaignsResource
    resource = CampaignsResource(http)
    resource.get_esp_mix("cmp_abc")
    http.request.assert_called_once()
    args = http.request.call_args
    assert args[0][0] == "GET"
    assert args[0][1] == "/campaigns/cmp_abc/esp-mix"


# ---------------------------------------------------------------------------
# Async categorize_stats: sequenceStep (not sequenceId)
# ---------------------------------------------------------------------------

def test_sync_categorize_stats_sends_sequence_step():
    http = _make_http({"data": {"groups": []}})
    resource = InboxResource(http)
    resource.categorize_stats(sequence_step=3)
    args = http.request.call_args
    assert args[0][0] == "GET"
    assert args[0][1] == "/inbox/categorize-stats"
    params = args[1]["params"]
    assert params.get("sequenceStep") == 3
    assert "sequenceId" not in params


def test_async_categorize_stats_params_contain_sequence_step():
    import asyncio
    captured = {}

    async def _async_request(method, path, *, params=None, json_body=None):
        captured["method"] = method
        captured["path"] = path
        captured["params"] = params
        return {"data": {"groups": []}}

    http = MagicMock()
    http.request = _async_request
    resource = AsyncInboxResource(http)
    asyncio.run(resource.categorize_stats(sequence_step=7))
    assert captured["params"].get("sequenceStep") == 7
    assert "sequenceId" not in captured["params"]


# ---------------------------------------------------------------------------
# custom_fields key conversion exemption
# ---------------------------------------------------------------------------

def test_keys_to_camel_does_not_recurse_into_custom_fields():
    result = _keys_to_camel({"custom_fields": {"company_size": 50, "ARR": 1000000}})
    assert result == {"customFields": {"company_size": 50, "ARR": 1000000}}


def test_keys_to_snake_does_not_recurse_into_custom_fields():
    result = _keys_to_snake({"customFields": {"companySize": 50, "ARR": 1000000}})
    assert result == {"custom_fields": {"companySize": 50, "ARR": 1000000}}


def test_keys_to_camel_converts_sibling_keys_normally():
    result = _keys_to_camel({"first_name": "John", "custom_fields": {"my_key": "val"}})
    assert result == {"firstName": "John", "customFields": {"my_key": "val"}}


def test_keys_to_snake_converts_sibling_keys_normally():
    result = _keys_to_snake({"firstName": "John", "customFields": {"myKey": "val"}})
    assert result == {"first_name": "John", "custom_fields": {"myKey": "val"}}
