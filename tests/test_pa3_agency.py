import sys, os
from unittest.mock import MagicMock

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from foxreach.resources.agency import AgencyResource


def test_overview_calls_get_agency_overview():
    http = MagicMock()
    http.request.return_value = {"data": {"ok": True}}
    http.request_text.return_value = "csv"
    r = AgencyResource(http)
    r.overview()
    call = (http.request_text if False else http.request).call_args
    assert call.args[0] == "GET"
    assert call.args[1] == "/agency/overview"


def test_list_clients_calls_get_agency_clients():
    http = MagicMock()
    http.request.return_value = {"data": {"ok": True}}
    http.request_text.return_value = "csv"
    r = AgencyResource(http)
    r.list_clients()
    call = (http.request_text if False else http.request).call_args
    assert call.args[0] == "GET"
    assert call.args[1] == "/agency/clients"


def test_create_client_calls_post_agency_clients():
    http = MagicMock()
    http.request.return_value = {"data": {"ok": True}}
    http.request_text.return_value = "csv"
    r = AgencyResource(http)
    r.create_client("name_v")
    call = (http.request_text if False else http.request).call_args
    assert call.args[0] == "POST"
    assert call.args[1] == "/agency/clients"


def test_rename_client_calls_patch_agency_clients_id_1():
    http = MagicMock()
    http.request.return_value = {"data": {"ok": True}}
    http.request_text.return_value = "csv"
    r = AgencyResource(http)
    r.rename_client("id_1", "name_v")
    call = (http.request_text if False else http.request).call_args
    assert call.args[0] == "PATCH"
    assert call.args[1] == "/agency/clients/id_1"


def test_delete_client_calls_delete_agency_clients_id_1():
    http = MagicMock()
    http.request.return_value = {"data": {"ok": True}}
    http.request_text.return_value = "csv"
    r = AgencyResource(http)
    r.delete_client("id_1")
    call = (http.request_text if False else http.request).call_args
    assert call.args[0] == "DELETE"
    assert call.args[1] == "/agency/clients/id_1"


def test_get_branding_calls_get_agency_branding():
    http = MagicMock()
    http.request.return_value = {"data": {"ok": True}}
    http.request_text.return_value = "csv"
    r = AgencyResource(http)
    r.get_branding()
    call = (http.request_text if False else http.request).call_args
    assert call.args[0] == "GET"
    assert call.args[1] == "/agency/branding"


def test_update_branding_calls_put_agency_branding():
    http = MagicMock()
    http.request.return_value = {"data": {"ok": True}}
    http.request_text.return_value = "csv"
    r = AgencyResource(http)
    r.update_branding()
    call = (http.request_text if False else http.request).call_args
    assert call.args[0] == "PUT"
    assert call.args[1] == "/agency/branding"
