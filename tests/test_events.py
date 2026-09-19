import pytest

from xangi_stackchan.events import normalize_xangi_stream_url
from xangi_stackchan.app import xangi_chat_payload


def test_normalize_base_url():
    assert (
        normalize_xangi_stream_url("http://127.0.0.1:18890")
        == "http://127.0.0.1:18890/api/events/stream"
    )


def test_normalize_stream_url():
    assert (
        normalize_xangi_stream_url("http://127.0.0.1:18890/api/events/stream")
        == "http://127.0.0.1:18890/api/events/stream"
    )


def test_normalize_rejects_empty():
    with pytest.raises(ValueError):
        normalize_xangi_stream_url("")


def test_xangi_chat_payload_uses_configured_web_session():
    assert xangi_chat_payload("こんにちは", "web:voice-session") == {
        "message": "こんにちは",
        "appSessionId": "voice-session",
    }


def test_xangi_chat_payload_keeps_default_for_other_threads():
    assert xangi_chat_payload("こんにちは", "discord:123") == {"message": "こんにちは"}
