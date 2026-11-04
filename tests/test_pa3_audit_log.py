import sys, os
from unittest.mock import MagicMock

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from foxreach.resources.audit_log import AuditLogResource


def test_list_calls_get_audit_log():
    http = MagicMock()
    http.request.return_value = {"data": {"ok": True}}
    http.request_text.return_value = "csv"
    r = AuditLogResource(http)
    r.list()
    call = (http.request_text if False else http.request).call_args
    assert call.args[0] == "GET"
    assert call.args[1] == "/audit-log"
