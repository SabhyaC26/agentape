"""Replay context manager for agentape."""

from __future__ import annotations

from collections.abc import Generator
from contextlib import contextmanager
from typing import TYPE_CHECKING

from agentape.core.context import (
    TapeContext,
    reset_context,
    set_current_context,
)
from agentape.core.matching import EXACT, MatchMode, get_match_fn
from agentape.core.tape import Tape

if TYPE_CHECKING:
    pass


@contextmanager
def replay(
    path: str,
    match: MatchMode = EXACT,
) -> Generator[Tape, None, None]:
    """Context manager for replaying recorded LLM interactions.

    Usage:
        with agentape.replay("tapes/my_flow.yaml"):
            response = client.chat.completions.create(...)
            # Returns cached response, no API call made

    Args:
        path: Path to the tape file.
        match: Matching mode (EXACT, SEMANTIC, or FUZZY).

    Yields:
        The Tape object being replayed.
    """
    tape = Tape.load(path)
    match_fn = get_match_fn(match)

    context = TapeContext(
        mode="replay",
        tape=tape,
        path=path,
        match_mode=match,
        match_fn=match_fn,
    )

    # Register context with any active wrapped clients
    from agentape.core.registry import get_registered_clients

    token = set_current_context(context)

    for client in get_registered_clients():
        client._set_tape_context(context)

    try:
        yield tape
    finally:
        # Clean up context
        for client in get_registered_clients():
            client._set_tape_context(None)

        reset_context(token)
