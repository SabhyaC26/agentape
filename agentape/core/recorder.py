"""Recording context manager for agentape."""

from __future__ import annotations

from contextlib import contextmanager
from typing import TYPE_CHECKING, Generator

from agentape.core.context import (
    TapeContext,
    get_current_context,
    reset_context,
    set_current_context,
)
from agentape.core.tape import Tape

if TYPE_CHECKING:
    pass


@contextmanager
def record(path: str) -> Generator[Tape, None, None]:
    """Context manager for recording LLM interactions.

    Usage:
        with agentape.record("tapes/my_flow.yaml"):
            response = client.chat.completions.create(...)

    Args:
        path: Path to save the tape file.

    Yields:
        The Tape object being recorded.
    """
    tape = Tape()
    context = TapeContext(mode="record", tape=tape, path=path)

    # Register context with any active wrapped clients
    from agentape.core.registry import get_registered_clients

    token = set_current_context(context)

    for client in get_registered_clients():
        client._set_tape_context(context)

    try:
        yield tape
    finally:
        # Save the tape
        tape.save(path)

        # Clean up context
        for client in get_registered_clients():
            client._set_tape_context(None)

        reset_context(token)
