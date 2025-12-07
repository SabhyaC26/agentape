"""Tests for client wrapping."""

from unittest.mock import MagicMock, patch

import pytest


class TestWrap:
    """Tests for the wrap function."""

    def test_wrap_openai_client(self):
        """Test wrapping an OpenAI client."""
        import agentape

        # Create a mock OpenAI client
        mock_client = MagicMock()
        mock_client.__class__.__name__ = "OpenAI"
        mock_client.__class__.__module__ = "openai._client"

        with patch("agentape.clients.openai_client.WrappedOpenAIClient") as MockWrapped:
            MockWrapped.return_value = MagicMock()
            wrapped = agentape.wrap(mock_client)
            MockWrapped.assert_called_once_with(mock_client)

    def test_wrap_unsupported_client(self):
        """Test wrapping an unsupported client raises TypeError."""
        import agentape

        mock_client = MagicMock()
        mock_client.__class__.__name__ = "UnsupportedClient"
        mock_client.__class__.__module__ = "some_module"

        with pytest.raises(TypeError, match="Unsupported client type"):
            agentape.wrap(mock_client)


class TestWrappedOpenAIClient:
    """Tests for the WrappedOpenAIClient."""

    def test_has_chat_attribute(self):
        """Test that wrapped client has chat attribute."""
        from agentape.clients.openai_client import WrappedOpenAIClient

        mock_client = MagicMock()
        mock_client.chat = MagicMock()
        mock_client.chat.completions = MagicMock()

        wrapped = WrappedOpenAIClient(mock_client)

        assert hasattr(wrapped, "chat")
        assert hasattr(wrapped.chat, "completions")

    def test_provider_is_openai(self):
        """Test that provider is 'openai'."""
        from agentape.clients.openai_client import WrappedOpenAIClient

        mock_client = MagicMock()
        mock_client.chat = MagicMock()
        mock_client.chat.completions = MagicMock()

        wrapped = WrappedOpenAIClient(mock_client)

        assert wrapped.provider == "openai"

    def test_proxies_unknown_attributes(self):
        """Test that unknown attributes are proxied to underlying client."""
        from agentape.clients.openai_client import WrappedOpenAIClient

        mock_client = MagicMock()
        mock_client.chat = MagicMock()
        mock_client.chat.completions = MagicMock()
        mock_client.api_key = "test-key"
        mock_client.some_method.return_value = "result"

        wrapped = WrappedOpenAIClient(mock_client)

        assert wrapped.api_key == "test-key"
        assert wrapped.some_method() == "result"
