import sys, os
from unittest.mock import MagicMock

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from foxreach.resources.lead_finder import LeadFinderResource


def test_create_list_calls_post_lead_finder_lists():
    http = MagicMock()
    http.request.return_value = {"data": {"ok": True}}
    http.request_text.return_value = "csv"
    r = LeadFinderResource(http)
    r.create_list("name_v", "kind_v")
    call = (http.request_text if False else http.request).call_args
    assert call.args[0] == "POST"
    assert call.args[1] == "/lead-finder/lists"


def test_get_list_calls_get_lead_finder_lists_id_1():
    http = MagicMock()
    http.request.return_value = {"data": {"ok": True}}
    http.request_text.return_value = "csv"
    r = LeadFinderResource(http)
    r.get_list("id_1")
    call = (http.request_text if False else http.request).call_args
    assert call.args[0] == "GET"
    assert call.args[1] == "/lead-finder/lists/id_1"


def test_rename_list_calls_patch_lead_finder_lists_id_1():
    http = MagicMock()
    http.request.return_value = {"data": {"ok": True}}
    http.request_text.return_value = "csv"
    r = LeadFinderResource(http)
    r.rename_list("id_1", "name_v")
    call = (http.request_text if False else http.request).call_args
    assert call.args[0] == "PATCH"
    assert call.args[1] == "/lead-finder/lists/id_1"


def test_delete_list_calls_delete_lead_finder_lists_id_1():
    http = MagicMock()
    http.request.return_value = {"data": {"ok": True}}
    http.request_text.return_value = "csv"
    r = LeadFinderResource(http)
    r.delete_list("id_1")
    call = (http.request_text if False else http.request).call_args
    assert call.args[0] == "DELETE"
    assert call.args[1] == "/lead-finder/lists/id_1"


def test_list_items_calls_get_lead_finder_lists_id_1_items():
    http = MagicMock()
    http.request.return_value = {"data": {"ok": True}}
    http.request_text.return_value = "csv"
    r = LeadFinderResource(http)
    r.list_items("id_1")
    call = (http.request_text if False else http.request).call_args
    assert call.args[0] == "GET"
    assert call.args[1] == "/lead-finder/lists/id_1/items"


def test_add_items_calls_post_lead_finder_lists_id_1_items():
    http = MagicMock()
    http.request.return_value = {"data": {"ok": True}}
    http.request_text.return_value = "csv"
    r = LeadFinderResource(http)
    r.add_items("id_1", "items_v")
    call = (http.request_text if False else http.request).call_args
    assert call.args[0] == "POST"
    assert call.args[1] == "/lead-finder/lists/id_1/items"


def test_remove_items_calls_delete_lead_finder_lists_id_1_items():
    http = MagicMock()
    http.request.return_value = {"data": {"ok": True}}
    http.request_text.return_value = "csv"
    r = LeadFinderResource(http)
    r.remove_items("id_1", "keys_v")
    call = (http.request_text if False else http.request).call_args
    assert call.args[0] == "DELETE"
    assert call.args[1] == "/lead-finder/lists/id_1/items"


def test_reveal_list_calls_post_lead_finder_lists_id_1_reveal():
    http = MagicMock()
    http.request.return_value = {"data": {"ok": True}}
    http.request_text.return_value = "csv"
    r = LeadFinderResource(http)
    r.reveal_list("id_1", "keys_v")
    call = (http.request_text if False else http.request).call_args
    assert call.args[0] == "POST"
    assert call.args[1] == "/lead-finder/lists/id_1/reveal"


def test_add_list_to_leads_calls_post_lead_finder_lists_id_1_add_to_leads():
    http = MagicMock()
    http.request.return_value = {"data": {"ok": True}}
    http.request_text.return_value = "csv"
    r = LeadFinderResource(http)
    r.add_list_to_leads("id_1")
    call = (http.request_text if False else http.request).call_args
    assert call.args[0] == "POST"
    assert call.args[1] == "/lead-finder/lists/id_1/add-to-leads"


def test_export_list_calls_get_lead_finder_lists_id_1_export():
    http = MagicMock()
    http.request.return_value = {"data": {"ok": True}}
    http.request_text.return_value = "csv"
    r = LeadFinderResource(http)
    r.export_list("id_1")
    call = (http.request_text if True else http.request).call_args
    assert call.args[0] == "GET"
    assert call.args[1] == "/lead-finder/lists/id_1/export"


def test_create_saved_search_calls_post_lead_finder_saved_searches():
    http = MagicMock()
    http.request.return_value = {"data": {"ok": True}}
    http.request_text.return_value = "csv"
    r = LeadFinderResource(http)
    r.create_saved_search("name_v", "kind_v")
    call = (http.request_text if False else http.request).call_args
    assert call.args[0] == "POST"
    assert call.args[1] == "/lead-finder/saved-searches"


def test_get_saved_search_calls_get_lead_finder_saved_searches_id_1():
    http = MagicMock()
    http.request.return_value = {"data": {"ok": True}}
    http.request_text.return_value = "csv"
    r = LeadFinderResource(http)
    r.get_saved_search("id_1")
    call = (http.request_text if False else http.request).call_args
    assert call.args[0] == "GET"
    assert call.args[1] == "/lead-finder/saved-searches/id_1"


def test_update_saved_search_calls_patch_lead_finder_saved_searches_id_1():
    http = MagicMock()
    http.request.return_value = {"data": {"ok": True}}
    http.request_text.return_value = "csv"
    r = LeadFinderResource(http)
    r.update_saved_search("id_1")
    call = (http.request_text if False else http.request).call_args
    assert call.args[0] == "PATCH"
    assert call.args[1] == "/lead-finder/saved-searches/id_1"


def test_delete_saved_search_calls_delete_lead_finder_saved_searches_id_1():
    http = MagicMock()
    http.request.return_value = {"data": {"ok": True}}
    http.request_text.return_value = "csv"
    r = LeadFinderResource(http)
    r.delete_saved_search("id_1")
    call = (http.request_text if False else http.request).call_args
    assert call.args[0] == "DELETE"
    assert call.args[1] == "/lead-finder/saved-searches/id_1"


def test_run_saved_search_calls_post_lead_finder_saved_searches_id_1_run():
    http = MagicMock()
    http.request.return_value = {"data": {"ok": True}}
    http.request_text.return_value = "csv"
    r = LeadFinderResource(http)
    r.run_saved_search("id_1")
    call = (http.request_text if False else http.request).call_args
    assert call.args[0] == "POST"
    assert call.args[1] == "/lead-finder/saved-searches/id_1/run"
