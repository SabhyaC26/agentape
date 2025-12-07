"""Tests for request matching."""

import pytest

from agentape.core.matching import (
    EXACT,
    FUZZY,
    SEMANTIC,
    MatchMode,
    get_match_fn,
    match_exact,
    match_fuzzy,
    match_semantic,
    normalize_request,
)


class TestNormalizeRequest:
    """Tests for request normalization."""

    def test_removes_excluded_fields(self):
        """Test that excluded fields are removed."""
        request = {
            "model": "gpt-4o",
            "messages": [],
            "stream": True,
            "timeout": 30,
            "extra_headers": {"X-Custom": "value"},
        }

        normalized = normalize_request(request)

        assert "model" in normalized
        assert "messages" in normalized
        assert "stream" not in normalized
        assert "timeout" not in normalized
        assert "extra_headers" not in normalized

    def test_removes_none_values(self):
        """Test that None values are removed."""
        request = {"model": "gpt-4o", "temperature": None, "tools": None}

        normalized = normalize_request(request)

        assert normalized == {"model": "gpt-4o"}

    def test_sorts_keys(self):
        """Test that keys are sorted."""
        request = {"z": 1, "a": 2, "m": 3}

        normalized = normalize_request(request)

        assert list(normalized.keys()) == ["a", "m", "z"]

    def test_normalizes_nested_dicts(self):
        """Test that nested dicts are normalized."""
        request = {
            "model": "gpt-4o",
            "messages": [{"role": "user", "content": "Hello"}],
        }

        normalized = normalize_request(request)

        assert normalized["messages"][0] == {"content": "Hello", "role": "user"}


class TestMatchExact:
    """Tests for exact matching."""

    def test_identical_requests_match(self):
        """Test that identical requests match."""
        request = {
            "model": "gpt-4o",
            "messages": [{"role": "user", "content": "Hello"}],
        }

        assert match_exact(request, request.copy()) is True

    def test_different_requests_dont_match(self):
        """Test that different requests don't match."""
        request1 = {"model": "gpt-4o", "messages": []}
        request2 = {"model": "gpt-3.5-turbo", "messages": []}

        assert match_exact(request1, request2) is False

    def test_ignores_excluded_fields(self):
        """Test that excluded fields are ignored in matching."""
        request1 = {"model": "gpt-4o", "stream": True}
        request2 = {"model": "gpt-4o", "stream": False}

        assert match_exact(request1, request2) is True

    def test_ignores_none_values(self):
        """Test that None values are ignored."""
        request1 = {"model": "gpt-4o", "temperature": None}
        request2 = {"model": "gpt-4o"}

        assert match_exact(request1, request2) is True


class TestMatchSemantic:
    """Tests for semantic matching (Phase 2)."""

    def test_raises_not_implemented(self):
        """Test that semantic matching raises NotImplementedError."""
        with pytest.raises(NotImplementedError):
            match_semantic({}, {})


class TestMatchFuzzy:
    """Tests for fuzzy matching (Phase 2)."""

    def test_raises_not_implemented(self):
        """Test that fuzzy matching raises NotImplementedError."""
        with pytest.raises(NotImplementedError):
            match_fuzzy({}, {})


class TestGetMatchFn:
    """Tests for getting match function by mode."""

    def test_get_exact_fn(self):
        """Test getting exact match function."""
        fn = get_match_fn(EXACT)
        assert fn is match_exact

    def test_get_semantic_fn(self):
        """Test getting semantic match function."""
        fn = get_match_fn(SEMANTIC)
        assert fn is match_semantic

    def test_get_fuzzy_fn(self):
        """Test getting fuzzy match function."""
        fn = get_match_fn(FUZZY)
        assert fn is match_fuzzy

    def test_invalid_mode(self):
        """Test getting function for invalid mode."""
        with pytest.raises(ValueError):
            get_match_fn("invalid")  # type: ignore
