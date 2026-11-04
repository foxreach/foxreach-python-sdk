import sys, os
from unittest.mock import MagicMock

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from foxreach.resources.email_accounts import EmailAccountsResource


def test_test_connection_calls_post_email_accounts_test():
    http = MagicMock()
    http.request.return_value = {"data": {"ok": True}}
    http.request_text.return_value = "csv"
    r = EmailAccountsResource(http)
    r.test_connection("email_v", "password_v", "smtp_host_v", "imap_host_v")
    call = (http.request_text if False else http.request).call_args
    assert call.args[0] == "POST"
    assert call.args[1] == "/email-accounts/test"


def test_check_domain_auth_calls_post_email_accounts_id_1_domain_auth_check():
    http = MagicMock()
    http.request.return_value = {"data": {"ok": True}}
    http.request_text.return_value = "csv"
    r = EmailAccountsResource(http)
    r.check_domain_auth("id_1")
    call = (http.request_text if False else http.request).call_args
    assert call.args[0] == "POST"
    assert call.args[1] == "/email-accounts/id_1/domain-auth/check"
