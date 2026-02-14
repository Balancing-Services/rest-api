"""Tests for the auto-pagination helper."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from balancing_services_cli.pagination import fetch_all_pages, fetch_first_page


@dataclass
class StubParsed:
    data: list[Any]
    has_more: bool
    next_cursor: str | None = None


@dataclass
class StubResponse:
    status_code: int
    parsed: StubParsed | None = None
    content: bytes = b""


def test_single_page():
    def fetch_fn(**kwargs):
        return StubResponse(status_code=200, parsed=StubParsed(data=["a", "b"], has_more=False))

    result = fetch_all_pages(fetch_fn)
    assert result == ["a", "b"]


def test_multiple_pages():
    call_count = 0

    def fetch_fn(**kwargs):
        nonlocal call_count
        call_count += 1
        if call_count == 1:
            assert "cursor" not in kwargs or kwargs.get("cursor") is None
            return StubResponse(status_code=200, parsed=StubParsed(data=["a"], has_more=True, next_cursor="c1"))
        if call_count == 2:
            assert kwargs["cursor"] == "c1"
            return StubResponse(status_code=200, parsed=StubParsed(data=["b"], has_more=True, next_cursor="c2"))
        assert kwargs["cursor"] == "c2"
        return StubResponse(status_code=200, parsed=StubParsed(data=["c"], has_more=False))

    result = fetch_all_pages(fetch_fn)
    assert result == ["a", "b", "c"]
    assert call_count == 3


def test_api_error():
    def fetch_fn(**kwargs):
        return StubResponse(status_code=500, content=b"Internal Server Error")

    import pytest

    with pytest.raises(SystemExit, match="API error"):
        fetch_all_pages(fetch_fn)


def test_empty_data():
    def fetch_fn(**kwargs):
        return StubResponse(status_code=200, parsed=StubParsed(data=[], has_more=False))

    result = fetch_all_pages(fetch_fn)
    assert result == []


# ── fetch_first_page tests ───────────────────────────────────────────────


def test_first_page_single_page():
    def fetch_fn(**kwargs):
        return StubResponse(status_code=200, parsed=StubParsed(data=["a", "b"], has_more=False))

    result = fetch_first_page(fetch_fn)
    assert result == ["a", "b"]


def test_first_page_has_more():
    """Even when there are more pages, fetch_first_page returns only the first."""
    call_count = 0

    def fetch_fn(**kwargs):
        nonlocal call_count
        call_count += 1
        return StubResponse(status_code=200, parsed=StubParsed(data=["a"], has_more=True, next_cursor="c1"))

    result = fetch_first_page(fetch_fn)
    assert result == ["a"]
    assert call_count == 1


def test_first_page_api_error():
    def fetch_fn(**kwargs):
        return StubResponse(status_code=500, content=b"Internal Server Error")

    import pytest

    with pytest.raises(SystemExit, match="API error"):
        fetch_first_page(fetch_fn)
