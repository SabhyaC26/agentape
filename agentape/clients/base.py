"""Base class for wrapped clients."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from agentape.core.context import TapeContext


class BaseWrappedClient(ABC):
    """Abstract base class for wrapped LLM clients."""

    def __init__(self, client: Any):
        self._client = client
        self._tape_context: TapeContext | None = None

    def _set_tape_context(self, context: TapeContext | None) -> None:
        """Set the tape context for recording/replay."""
        self._tape_context = context

    @property
    @abstractmethod
    def provider(self) -> str:
        """Return the provider name."""
        ...
