"""Exact outgoing requests for the 0.4.2 fixes, checked at the HTTP transport.

Each test drives a real ``HttpClient`` / ``AsyncHttpClient`` through respx, so
what is asserted is the query string and JSON body that would reach the API
after snake_case -> camelCase conversion, not the arguments handed to a mock.

Backend sources these shapes are checked against:
- GET /leads ``email`` query param: backend/app/routers/v1/leads.py (list_leads)
- GET /inbox/threads/{id} ``markRead``: backend/app/routers/v1/inbox.py (get_thread)
- POST /campaigns/{id}/sequences body: SequenceCreateRequest in
  backend/app/routers/v1/campaigns.py (subject + body required, no stepNumber,
  no templateType)
- POST/PATCH /templates body: TemplateCreate / TemplateUpdate in
  backend/app/routers/v1/templates.py (``category``, not ``templateType``)
"""

import dataclasses
import json
import os
import re
import sys

import httpx
import pytest
import respx

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from foxreach import AsyncFoxReach, FoxReach  # noqa: E402
from foxreach._version import __version__  # noqa: E402
from foxreach.types import (  # noqa: E402
    SequenceCreate,
    SequenceUpdate,
    TemplateCreate,
    TemplateUpdate,
)

BASE = "https://api.test.io/api/v1"
PAGE = {"data": [], "meta": {"total": 0, "page": 1, "pageSize": 50, "totalPages": 0}}


def _client() -> FoxReach:
    return FoxReach(api_key="otr_test", base_url=BASE, max_retries=0)


def _aclient() -> AsyncFoxReach:
    return AsyncFoxReach(api_key="otr_test", base_url=BASE, max_retries=0)


def _body(route) -> dict:
    return json.loads(route.calls.last.request.content)


def _query(route) -> dict:
    return dict(route.calls.last.request.url.params)


# ---------------------------------------------------------------------------
# 1. leads.list(email=...)
# ---------------------------------------------------------------------------

@respx.mock
def test_leads_list_sends_exact_email_param():
    route = respx.get(f"{BASE}/leads").mock(return_value=httpx.Response(200, json=PAGE))
    _client().leads.list(email="Jane_Doe@Example.com")
    assert _query(route) == {"page": "1", "pageSize": "50", "email": "Jane_Doe@Example.com"}


@respx.mock
def test_leads_list_omits_email_when_not_given():
    route = respx.get(f"{BASE}/leads").mock(return_value=httpx.Response(200, json=PAGE))
    _client().leads.list()
    assert "email" not in _query(route)


@respx.mock
@pytest.mark.asyncio
async def test_async_leads_list_sends_exact_email_param():
    route = respx.get(f"{BASE}/leads").mock(return_value=httpx.Response(200, json=PAGE))
    await _aclient().leads.list(email="jane@example.com")
    assert _query(route) == {"page": "1", "pageSize": "50", "email": "jane@example.com"}


@respx.mock
def test_leads_list_sends_provider_param():
    route = respx.get(f"{BASE}/leads").mock(return_value=httpx.Response(200, json=PAGE))
    _client().leads.list(provider="gateway")
    assert _query(route) == {"page": "1", "pageSize": "50", "provider": "gateway"}


@respx.mock
def test_leads_list_omits_provider_when_not_given():
    route = respx.get(f"{BASE}/leads").mock(return_value=httpx.Response(200, json=PAGE))
    _client().leads.list()
    assert "provider" not in _query(route)


@respx.mock
def test_leads_providers_calls_summary_path():
    body = {"data": {"counts": {"google": 3}, "gateway": 1, "total": 4, "resolvedPct": 75}}
    route = respx.get(f"{BASE}/leads/providers").mock(return_value=httpx.Response(200, json=body))
    result = _client().leads.providers()
    assert route.called
    assert result["data"]["counts"] == {"google": 3}
    assert result["data"]["gateway"] == 1
    assert result["data"]["resolved_pct"] == 75


@respx.mock
@pytest.mark.asyncio
async def test_async_leads_providers_calls_summary_path():
    body = {"data": {"counts": {}, "gateway": 0, "total": 0, "resolvedPct": 0}}
    respx.get(f"{BASE}/leads/providers").mock(return_value=httpx.Response(200, json=body))
    result = await _aclient().leads.providers()
    assert result["data"]["total"] == 0
    assert result["data"]["resolved_pct"] == 0


# ---------------------------------------------------------------------------
# 2. inbox.get(mark_read=...)
# ---------------------------------------------------------------------------

THREAD = {"data": {"id": "rpl_1", "fromEmail": "a@b.com"}}


@respx.mock
def test_inbox_get_does_not_ask_to_mark_read_by_default():
    route = respx.get(f"{BASE}/inbox/threads/rpl_1").mock(return_value=httpx.Response(200, json=THREAD))
    _client().inbox.get("rpl_1")
    assert _query(route) == {}


@respx.mock
def test_inbox_get_mark_read_true_sends_markRead():
    route = respx.get(f"{BASE}/inbox/threads/rpl_1").mock(return_value=httpx.Response(200, json=THREAD))
    _client().inbox.get("rpl_1", mark_read=True)
    assert _query(route) == {"markRead": "true"}


@respx.mock
@pytest.mark.asyncio
async def test_async_inbox_get_mark_read_true_sends_markRead():
    route = respx.get(f"{BASE}/inbox/threads/rpl_1").mock(return_value=httpx.Response(200, json=THREAD))
    await _aclient().inbox.get("rpl_1", mark_read=True)
    assert _query(route) == {"markRead": "true"}


# ---------------------------------------------------------------------------
# 3a. Sequence create/update bodies
# ---------------------------------------------------------------------------

SEQ = {"data": {"id": "seq_1", "campaignId": "cmp_1", "stepNumber": 2, "subject": "Hi", "body": "B"}}
SEQ_CREATE_FIELDS = {"subject", "body", "name", "delayDays", "delayHours", "sendOnlyIfNoReply", "sendAsHtml"}


def test_sequence_create_requires_subject():
    with pytest.raises(TypeError):
        SequenceCreate(body="Hello")  # type: ignore[call-arg]


def test_sequence_create_has_no_fields_the_backend_drops():
    names = {f.name for f in dataclasses.fields(SequenceCreate)}
    assert "step_number" not in names
    assert "template_type" not in names
    update_names = {f.name for f in dataclasses.fields(SequenceUpdate)}
    assert "step_number" not in update_names


@respx.mock
def test_sequence_create_exact_body():
    route = respx.post(f"{BASE}/campaigns/cmp_1/sequences").mock(return_value=httpx.Response(200, json=SEQ))
    _client().campaigns.sequences.create("cmp_1", SequenceCreate(body="Hello {{firstName}}", subject="Hi"))
    assert _body(route) == {"body": "Hello {{firstName}}", "subject": "Hi", "delayDays": 1}


@respx.mock
def test_sequence_create_all_fields_use_backend_names():
    route = respx.post(f"{BASE}/campaigns/cmp_1/sequences").mock(return_value=httpx.Response(200, json=SEQ))
    _client().campaigns.sequences.create("cmp_1", SequenceCreate(
        body="B", subject="S", name="Step two", delay_days=3, delay_hours=4,
        send_only_if_no_reply=False, send_as_html=True,
    ))
    body = _body(route)
    assert body == {
        "body": "B", "subject": "S", "name": "Step two", "delayDays": 3, "delayHours": 4,
        "sendOnlyIfNoReply": False, "sendAsHtml": True,
    }
    assert set(body) <= SEQ_CREATE_FIELDS


@respx.mock
def test_sequence_update_exact_body():
    route = respx.patch(f"{BASE}/campaigns/cmp_1/sequences/seq_1").mock(return_value=httpx.Response(200, json=SEQ))
    _client().campaigns.sequences.update("cmp_1", "seq_1", SequenceUpdate(delay_hours=6, send_as_html=True))
    assert _body(route) == {"delayHours": 6, "sendAsHtml": True}


@respx.mock
@pytest.mark.asyncio
async def test_async_sequence_create_exact_body():
    route = respx.post(f"{BASE}/campaigns/cmp_1/sequences").mock(return_value=httpx.Response(200, json=SEQ))
    await _aclient().campaigns.sequences.create("cmp_1", SequenceCreate(body="B", subject="S", delay_days=0))
    assert _body(route) == {"body": "B", "subject": "S", "delayDays": 0}


@respx.mock
def test_sequence_response_reads_backend_fields():
    payload = {"data": {
        "id": "seq_1", "campaignId": "cmp_1", "stepNumber": 2, "name": "Bump", "subject": "S",
        "body": "B", "delayDays": 2, "delayHours": 5, "sendOnlyIfNoReply": False, "sendAsHtml": True,
    }}
    respx.post(f"{BASE}/campaigns/cmp_1/sequences").mock(return_value=httpx.Response(200, json=payload))
    seq = _client().campaigns.sequences.create("cmp_1", SequenceCreate(body="B", subject="S"))
    assert (seq.step_number, seq.name, seq.delay_hours, seq.send_only_if_no_reply, seq.send_as_html) == (
        2, "Bump", 5, False, True,
    )


# ---------------------------------------------------------------------------
# 3b. Template create/update bodies: category, not templateType
# ---------------------------------------------------------------------------

TPL = {"data": {"id": "tpl_1", "name": "N", "body": "B", "category": "reply_macro", "sendAsHtml": False}}


@respx.mock
def test_template_create_exact_body_default():
    route = respx.post(f"{BASE}/templates").mock(return_value=httpx.Response(200, json=TPL))
    _client().templates.create(TemplateCreate(name="N", body="B"))
    assert _body(route) == {"name": "N", "body": "B", "sendAsHtml": False}


@respx.mock
def test_template_create_sends_category():
    route = respx.post(f"{BASE}/templates").mock(return_value=httpx.Response(200, json=TPL))
    _client().templates.create(TemplateCreate(name="N", body="B", subject="S", category="reply_macro"))
    assert _body(route) == {"name": "N", "body": "B", "subject": "S", "category": "reply_macro", "sendAsHtml": False}


@respx.mock
def test_template_update_sends_category():
    route = respx.patch(f"{BASE}/templates/tpl_1").mock(return_value=httpx.Response(200, json=TPL))
    _client().templates.update("tpl_1", TemplateUpdate(category="reply_macro"))
    assert _body(route) == {"category": "reply_macro"}


@respx.mock
@pytest.mark.asyncio
async def test_async_template_create_sends_category():
    route = respx.post(f"{BASE}/templates").mock(return_value=httpx.Response(200, json=TPL))
    await _aclient().templates.create(TemplateCreate(name="N", body="B", category="reply_macro"))
    assert _body(route) == {"name": "N", "body": "B", "category": "reply_macro", "sendAsHtml": False}


@respx.mock
def test_template_response_reads_category():
    respx.get(f"{BASE}/templates/tpl_1").mock(return_value=httpx.Response(200, json=TPL))
    assert _client().templates.get("tpl_1").category == "reply_macro"


# ---------------------------------------------------------------------------
# 5. Version sources agree
# ---------------------------------------------------------------------------

def test_pyproject_version_matches_dunder_version():
    path = os.path.join(os.path.dirname(__file__), "..", "pyproject.toml")
    with open(path) as fh:
        match = re.search(r'^version\s*=\s*"([^"]+)"', fh.read(), re.MULTILINE)
    assert match is not None
    assert match.group(1) == __version__ == "0.6.0"


@respx.mock
def test_user_agent_carries_version():
    route = respx.get(f"{BASE}/leads").mock(return_value=httpx.Response(200, json=PAGE))
    _client().leads.list()
    assert route.calls.last.request.headers["User-Agent"] == "foxreach-python/0.6.0"


@respx.mock
def test_leads_list_interest_and_label_filters_and_parsing():
    route = respx.get(f"{BASE}/leads").mock(return_value=httpx.Response(200, json={
        "data": [{"id": "l1", "email": "a@b.co", "interestStatus": "interested",
                  "interestStatusSource": "auto", "labels": [{"id": "x", "name": "Hot", "color": "success", "meaning": "positive"}]}],
        "meta": {"total": 1, "page": 1, "pageSize": 50, "totalPages": 1},
    }))
    page = _client().leads.list(interest_status="interested", label_id="x")
    q = route.calls[0].request.url.params
    assert q["interestStatus"] == "interested" and q["labelId"] == "x"
    lead = page.data[0]
    assert lead.interest_status == "interested" and lead.labels[0].name == "Hot"


@respx.mock
def test_set_interest_status_sends_explicit_null_to_clear():
    route = respx.patch(f"{BASE}/leads/l1").mock(return_value=httpx.Response(200, json={"data": {"id": "l1", "email": "a@b.co"}}))
    _client().leads.set_interest_status("l1", None)
    assert _body(route) == {"interestStatus": None}


@respx.mock
def test_lead_labels_requests():
    create = respx.post(f"{BASE}/lead-labels").mock(return_value=httpx.Response(201, json={"data": {"id": "x", "name": "Hot"}}))
    assign = respx.post(f"{BASE}/leads/l1/labels/x").mock(return_value=httpx.Response(204))
    unassign = respx.delete(f"{BASE}/leads/l1/labels/x").mock(return_value=httpx.Response(204))
    c = _client()
    assert c.lead_labels.create("Hot", color="success", meaning="positive").id == "x"
    assert _body(create) == {"name": "Hot", "color": "success", "meaning": "positive"}
    c.lead_labels.assign("l1", "x")
    c.lead_labels.unassign("l1", "x")
    assert assign.called and unassign.called


@respx.mock
def test_webhook_resume_and_reply_categories():
    resume = respx.post(f"{BASE}/webhooks/w1/resume").mock(return_value=httpx.Response(200, json={"data": {"id": "w1", "url": "u", "isActive": True, "pausedAt": None}}))
    create = respx.post(f"{BASE}/webhooks").mock(return_value=httpx.Response(200, json={"data": {"id": "w2", "url": "u", "replyCategories": ["interested"]}}))
    from foxreach.types import WebhookCreate
    c = _client()
    assert c.webhooks.resume("w1").is_active is True and resume.called
    hook = c.webhooks.create(WebhookCreate(url="u", events=["*"], reply_categories=["interested"]))
    assert _body(create)["replyCategories"] == ["interested"] and hook.reply_categories == ["interested"]
