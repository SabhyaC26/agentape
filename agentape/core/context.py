"""Tape context for managing recording/replay state."""

from __future__ import annotations

import contextvars
from dataclasses import dataclass
from typing import TYPE_CHECKING, Literal

if TYPE_CHECKING:
    from agentape.core.matching import MatchMode
    from agentape.core.tape import Tape

# Thread-safe context variable for current tape context
_current_tape_context: contextvars.ContextVar[TapeContext | None] = (
    contextvars.ContextVar("tape_context", default=None)
)


@dataclass
class TapeContext:
    """Context for tape operations."""

    mode: Literal["record", "replay", "off"]
    tape: Tape
    path: str
    match_mode: MatchMode | None = None
    match_fn: callable | None = None


def get_current_context() -> TapeContext | None:
    """Get the current tape context."""
    return _current_tape_context.get()


def set_current_context(context: TapeContext | None) -> contextvars.Token:
    """Set the current tape context and return a token for resetting."""
    return _current_tape_context.set(context)


def reset_context(token: contextvars.Token) -> None:
    """Reset the tape context using a token."""
    _current_tape_context.reset(token)
