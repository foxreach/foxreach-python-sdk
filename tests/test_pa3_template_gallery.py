import sys, os
from unittest.mock import MagicMock

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from foxreach.resources.templates import TemplatesResource


def test_publish_calls_post_templates_id_1_publish():
    http = MagicMock()
    http.request.return_value = {"data": {"ok": True}}
    http.request_text.return_value = "csv"
    r = TemplatesResource(http)
    r.publish("id_1", "share_description_v", "share_category_v")
    call = (http.request_text if False else http.request).call_args
    assert call.args[0] == "POST"
    assert call.args[1] == "/templates/id_1/publish"


def test_unpublish_calls_delete_templates_id_1_publish():
    http = MagicMock()
    http.request.return_value = {"data": {"ok": True}}
    http.request_text.return_value = "csv"
    r = TemplatesResource(http)
    r.unpublish("id_1")
    call = (http.request_text if False else http.request).call_args
    assert call.args[0] == "DELETE"
    assert call.args[1] == "/templates/id_1/publish"


def test_clone_calls_post_templates_clone_id_1():
    http = MagicMock()
    http.request.return_value = {"data": {"ok": True}}
    http.request_text.return_value = "csv"
    r = TemplatesResource(http)
    r.clone("id_1")
    call = (http.request_text if False else http.request).call_args
    assert call.args[0] == "POST"
    assert call.args[1] == "/templates/clone/id_1"
