"""pytest plugin for agentape."""

from __future__ import annotations

import os
from functools import wraps
from typing import Callable, TypeVar

import pytest

F = TypeVar("F", bound=Callable)

# Global variable to track current tape mode from pytest
_pytest_tape_mode: str | None = None


def pytest_addoption(parser: pytest.Parser) -> None:
    """Add agentape command line options to pytest."""
    parser.addoption(
        "--tape-mode",
        action="store",
        default="replay",
        choices=["record", "replay", "off"],
        help="Tape mode: record (create new tapes), replay (use existing), or off (pass-through)",
    )


def pytest_configure(config: pytest.Config) -> None:
    """Configure agentape based on pytest options."""
    global _pytest_tape_mode
    _pytest_tape_mode = config.getoption("--tape-mode")


@pytest.fixture
def tape_mode(request: pytest.FixtureRequest) -> str:
    """Fixture to access the current tape mode."""
    return request.config.getoption("--tape-mode")


def get_tape_mode() -> str:
    """Get the current tape mode from pytest or environment variable."""
    # Check pytest global first
    if _pytest_tape_mode is not None:
        return _pytest_tape_mode

    # Fall back to environment variable
    return os.environ.get("AGENTAPE_MODE", "replay")


def use_tape(path_template: str) -> Callable[[F], F]:
    """Decorator to enable tape recording/replay for a test function.

    Usage:
        @agentape.use_tape("tapes/{test_name}.yaml")
        def test_my_feature(openai_client):
            response = openai_client.chat.completions.create(...)

    Args:
        path_template: Path template for the tape file. Supports {test_name} placeholder.

    Returns:
        Decorated test function.
    """

    def decorator(func: F) -> F:
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Import here to avoid circular imports
            from agentape.core.recorder import record
            from agentape.core.replayer import replay

            test_name = func.__name__
            path = path_template.format(test_name=test_name)
            mode = get_tape_mode()

            if mode == "record":
                with record(path):
                    return func(*args, **kwargs)
            elif mode == "replay":
                with replay(path):
                    return func(*args, **kwargs)
            else:
                # mode == "off"
                return func(*args, **kwargs)

        return wrapper  # type: ignore

    return decorator
