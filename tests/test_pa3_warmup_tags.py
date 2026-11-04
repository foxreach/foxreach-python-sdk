import sys, os
from unittest.mock import MagicMock

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from foxreach.resources.warmup import WarmupResource


def test_create_tag_calls_post_warmup_tags():
    http = MagicMock()
    http.request.return_value = {"data": {"ok": True}}
    http.request_text.return_value = "csv"
    r = WarmupResource(http)
    r.create_tag("name_v")
    call = (http.request_text if False else http.request).call_args
    assert call.args[0] == "POST"
    assert call.args[1] == "/warmup/tags"


def test_update_tag_calls_patch_warmup_tags_id_1():
    http = MagicMock()
    http.request.return_value = {"data": {"ok": True}}
    http.request_text.return_value = "csv"
    r = WarmupResource(http)
    r.update_tag("id_1")
    call = (http.request_text if False else http.request).call_args
    assert call.args[0] == "PATCH"
    assert call.args[1] == "/warmup/tags/id_1"


def test_delete_tag_calls_delete_warmup_tags_id_1():
    http = MagicMock()
    http.request.return_value = {"data": {"ok": True}}
    http.request_text.return_value = "csv"
    r = WarmupResource(http)
    r.delete_tag("id_1")
    call = (http.request_text if False else http.request).call_args
    assert call.args[0] == "DELETE"
    assert call.args[1] == "/warmup/tags/id_1"


def test_assign_tag_calls_post_warmup_pool_id_1_tags_id_1():
    http = MagicMock()
    http.request.return_value = {"data": {"ok": True}}
    http.request_text.return_value = "csv"
    r = WarmupResource(http)
    r.assign_tag("id_1", "id_1")
    call = (http.request_text if False else http.request).call_args
    assert call.args[0] == "POST"
    assert call.args[1] == "/warmup/pool/id_1/tags/id_1"


def test_unassign_tag_calls_delete_warmup_pool_id_1_tags_id_1():
    http = MagicMock()
    http.request.return_value = {"data": {"ok": True}}
    http.request_text.return_value = "csv"
    r = WarmupResource(http)
    r.unassign_tag("id_1", "id_1")
    call = (http.request_text if False else http.request).call_args
    assert call.args[0] == "DELETE"
    assert call.args[1] == "/warmup/pool/id_1/tags/id_1"
