from mteam_cli.automation.runner import _compose_body
from mteam_cli.core.config import Account
from mteam_cli.core.models import CheckinResult


def _acct(digest_enabled):
    return Account(username="u", api_key="k", digest_enabled=digest_enabled)


def test_compose_body_failure_returns_error():
    r = CheckinResult(username="u", ok=False, error="boom")
    assert _compose_body(r, _acct(True), "DIGEST") == "boom"


def test_compose_body_enabled_appends_digest():
    r = CheckinResult(username="u", ok=True, profile_text="PROFILE")
    out = _compose_body(r, _acct(True), "DIGEST")
    assert out == "PROFILE\n\nDIGEST"


def test_compose_body_disabled_omits_digest():
    r = CheckinResult(username="u", ok=True, profile_text="PROFILE")
    assert _compose_body(r, _acct(False), "DIGEST") == "PROFILE"


def test_compose_body_enabled_but_empty_digest():
    r = CheckinResult(username="u", ok=True, profile_text="PROFILE")
    assert _compose_body(r, _acct(True), "") == "PROFILE"
