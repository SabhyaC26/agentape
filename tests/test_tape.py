"""Tests for Tape class."""

import os
import tempfile

import pytest

from agentape.core.tape import Tape
from agentape.exceptions import NoMatchingInteractionError, TapeNotFoundError


class TestTape:
    """Tests for the Tape class."""

    def test_create_empty_tape(self):
        """Test creating an empty tape."""
        tape = Tape()
        assert tape.version == "1.0"
        assert tape.interactions == []
        assert tape.provider is None
        assert tape.recorded_at is not None

    def test_create_tape_with_provider(self):
        """Test creating a tape with a provider."""
        tape = Tape(provider="openai")
        assert tape.provider == "openai"

    def test_add_interaction(self):
        """Test adding an interaction to the tape."""
        tape = Tape()
        request = {"method": "chat.completions.create", "model": "gpt-4o"}
        response = {"id": "chatcmpl-123", "choices": []}

        tape.add_interaction(request, response, latency_ms=100)

        assert len(tape.interactions) == 1
        assert tape.interactions[0]["request"] == request
        assert tape.interactions[0]["response"] == response
        assert tape.interactions[0]["latency_ms"] == 100
        assert tape.interactions[0]["id"] == 1

    def test_add_multiple_interactions(self):
        """Test adding multiple interactions."""
        tape = Tape()

        for i in range(3):
            tape.add_interaction(
                {"method": "chat.completions.create", "index": i},
                {"response": i},
            )

        assert len(tape.interactions) == 3
        assert tape.interactions[0]["id"] == 1
        assert tape.interactions[1]["id"] == 2
        assert tape.interactions[2]["id"] == 3

    def test_add_streaming_interaction(self):
        """Test adding a streaming interaction."""
        tape = Tape()
        request = {"method": "chat.completions.create", "stream": True}
        chunks = [{"chunk": 1}, {"chunk": 2}, {"chunk": 3}]

        tape.add_streaming_interaction(request, chunks, latency_ms=500)

        assert len(tape.interactions) == 1
        assert tape.interactions[0]["request"] == request
        assert tape.interactions[0]["streaming_chunks"] == chunks
        assert tape.interactions[0]["latency_ms"] == 500

    def test_save_and_load_tape(self):
        """Test saving and loading a tape."""
        tape = Tape(provider="openai")
        tape.add_interaction(
            {"method": "chat.completions.create", "model": "gpt-4o"},
            {"id": "chatcmpl-123", "choices": []},
        )

        with tempfile.NamedTemporaryFile(suffix=".yaml", delete=False) as f:
            path = f.name

        try:
            tape.save(path)
            loaded = Tape.load(path)

            assert loaded.version == tape.version
            assert loaded.provider == tape.provider
            assert len(loaded.interactions) == 1
            assert loaded.interactions[0]["request"]["model"] == "gpt-4o"
        finally:
            os.unlink(path)

    def test_load_nonexistent_tape(self):
        """Test loading a tape that doesn't exist."""
        with pytest.raises(TapeNotFoundError):
            Tape.load("/nonexistent/path/tape.yaml")

    def test_match_and_return(self):
        """Test matching a request and returning the response."""
        tape = Tape()
        tape.add_interaction(
            {"method": "chat.completions.create", "model": "gpt-4o"},
            {"id": "chatcmpl-123", "content": "Hello!"},
        )

        result = tape.match_and_return(
            {"method": "chat.completions.create", "model": "gpt-4o"}
        )

        assert result["id"] == "chatcmpl-123"
        assert result["content"] == "Hello!"

    def test_match_and_return_no_match(self):
        """Test matching when no interaction matches."""
        tape = Tape()
        tape.add_interaction(
            {"method": "chat.completions.create", "model": "gpt-4o"},
            {"id": "chatcmpl-123"},
        )

        with pytest.raises(NoMatchingInteractionError):
            tape.match_and_return(
                {"method": "chat.completions.create", "model": "gpt-3.5-turbo"}
            )

    def test_match_and_return_chunks(self):
        """Test matching a streaming request and returning chunks."""
        tape = Tape()
        chunks = [{"delta": "Hello"}, {"delta": " world"}]
        tape.add_streaming_interaction(
            {"method": "chat.completions.create", "model": "gpt-4o", "stream": True},
            chunks,
        )

        result = tape.match_and_return_chunks(
            {"method": "chat.completions.create", "model": "gpt-4o", "stream": True}
        )

        assert result == chunks
