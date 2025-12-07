"""Tests for pytest plugin."""

import os
import tempfile
from unittest.mock import patch

from agentape.pytest_plugin import get_tape_mode, use_tape


class TestGetTapeMode:
    """Tests for get_tape_mode function."""

    def test_returns_env_var_when_set(self):
        """Test that environment variable is used."""
        with patch.dict(os.environ, {"AGENTAPE_MODE": "record"}):
            with patch("agentape.pytest_plugin._pytest_tape_mode", None):
                assert get_tape_mode() == "record"

    def test_returns_replay_by_default(self):
        """Test that replay is the default mode."""
        with patch.dict(os.environ, {}, clear=True):
            with patch("agentape.pytest_plugin._pytest_tape_mode", None):
                # Remove AGENTAPE_MODE if present
                os.environ.pop("AGENTAPE_MODE", None)
                assert get_tape_mode() == "replay"


class TestUseTapeDecorator:
    """Tests for use_tape decorator."""

    def test_decorator_preserves_function_name(self):
        """Test that decorator preserves function metadata."""

        @use_tape("tapes/{test_name}.yaml")
        def my_test_function():
            pass

        assert my_test_function.__name__ == "my_test_function"

    def test_decorator_formats_path_with_test_name(self):
        """Test that path is formatted with test name."""

        @use_tape("tapes/{test_name}.yaml")
        def test_example():
            pass

        with patch("agentape.pytest_plugin.get_tape_mode", return_value="off"):
            test_example()

    def test_decorator_in_record_mode(self):
        """Test decorator behavior in record mode."""
        with tempfile.TemporaryDirectory() as tmpdir:
            os.path.join(tmpdir, "tapes", "test_func.yaml")

            @use_tape(os.path.join(tmpdir, "tapes", "{test_name}.yaml"))
            def test_func():
                return "result"

            with patch("agentape.pytest_plugin.get_tape_mode", return_value="record"):
                result = test_func()
                assert result == "result"

    def test_decorator_in_off_mode(self):
        """Test decorator behavior in off mode."""

        @use_tape("tapes/{test_name}.yaml")
        def test_func():
            return "result"

        with patch("agentape.pytest_plugin.get_tape_mode", return_value="off"):
            result = test_func()
            assert result == "result"
