"""Tests for record and replay functionality."""

import os
import tempfile
from unittest.mock import MagicMock, patch

import pytest

import agentape
from agentape.core.context import TapeContext
from agentape.core.recorder import record
from agentape.core.registry import clear_registry
from agentape.core.replayer import replay
from agentape.core.tape import Tape
from agentape.exceptions import NoMatchingInteractionError, TapeNotFoundError


class TestRecord:
    """Tests for the record context manager."""

    def setup_method(self):
        """Clear registry before each test."""
        clear_registry()

    def test_record_creates_tape_file(self):
        """Test that recording creates a tape file."""
        with tempfile.NamedTemporaryFile(suffix=".yaml", delete=False) as f:
            path = f.name

        try:
            os.unlink(path)  # Remove the file so record creates it

            with record(path) as tape:
                tape.add_interaction(
                    {"method": "test", "data": "value"},
                    {"result": "success"},
                )

            assert os.path.exists(path)
        finally:
            if os.path.exists(path):
                os.unlink(path)

    def test_record_yields_tape(self):
        """Test that record yields a Tape object."""
        with tempfile.NamedTemporaryFile(suffix=".yaml", delete=False) as f:
            path = f.name

        try:
            with record(path) as tape:
                assert isinstance(tape, Tape)
                assert tape.interactions == []
        finally:
            if os.path.exists(path):
                os.unlink(path)

    def test_record_saves_on_exit(self):
        """Test that tape is saved when exiting context."""
        with tempfile.NamedTemporaryFile(suffix=".yaml", delete=False) as f:
            path = f.name

        try:
            os.unlink(path)

            with record(path) as tape:
                tape.add_interaction({"test": True}, {"result": "ok"})

            # Verify the file was saved with correct content
            loaded = Tape.load(path)
            assert len(loaded.interactions) == 1
        finally:
            if os.path.exists(path):
                os.unlink(path)


class TestReplay:
    """Tests for the replay context manager."""

    def setup_method(self):
        """Clear registry before each test."""
        clear_registry()

    def test_replay_loads_tape(self):
        """Test that replay loads an existing tape."""
        with tempfile.NamedTemporaryFile(suffix=".yaml", delete=False) as f:
            path = f.name

        try:
            # First create a tape
            tape = Tape()
            tape.add_interaction({"test": True}, {"result": "ok"})
            tape.save(path)

            # Then replay it
            with replay(path) as replayed_tape:
                assert len(replayed_tape.interactions) == 1
        finally:
            os.unlink(path)

    def test_replay_nonexistent_tape_raises(self):
        """Test that replaying a nonexistent tape raises error."""
        with pytest.raises(TapeNotFoundError):
            with replay("/nonexistent/tape.yaml"):
                pass

    def test_replay_with_match_mode(self):
        """Test that replay accepts match mode."""
        with tempfile.NamedTemporaryFile(suffix=".yaml", delete=False) as f:
            path = f.name

        try:
            tape = Tape()
            tape.add_interaction({"test": True}, {"result": "ok"})
            tape.save(path)

            with replay(path, match=agentape.EXACT) as replayed_tape:
                assert replayed_tape is not None
        finally:
            os.unlink(path)


class TestRecordReplayIntegration:
    """Integration tests for record and replay."""

    def setup_method(self):
        """Clear registry before each test."""
        clear_registry()

    def test_record_then_replay(self):
        """Test recording and then replaying interactions."""
        with tempfile.NamedTemporaryFile(suffix=".yaml", delete=False) as f:
            path = f.name

        try:
            os.unlink(path)

            # Record
            with record(path) as tape:
                tape.add_interaction(
                    {"method": "chat.completions.create", "model": "gpt-4o"},
                    {"id": "chatcmpl-123", "content": "Hello!"},
                )

            # Replay
            with replay(path) as tape:
                response = tape.match_and_return(
                    {"method": "chat.completions.create", "model": "gpt-4o"}
                )
                assert response["content"] == "Hello!"
        finally:
            if os.path.exists(path):
                os.unlink(path)

    def test_replay_no_match_raises(self):
        """Test that replaying with no match raises error."""
        with tempfile.NamedTemporaryFile(suffix=".yaml", delete=False) as f:
            path = f.name

        try:
            # Create tape with one interaction
            tape = Tape()
            tape.add_interaction(
                {"method": "chat.completions.create", "model": "gpt-4o"},
                {"content": "Hello"},
            )
            tape.save(path)

            # Try to replay with different request
            with replay(path) as tape:
                with pytest.raises(NoMatchingInteractionError):
                    tape.match_and_return(
                        {"method": "chat.completions.create", "model": "gpt-3.5-turbo"}
                    )
        finally:
            os.unlink(path)
