"""Tape class for managing recorded interactions."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from agentape.exceptions import NoMatchingInteractionError
from agentape.storage.yaml_storage import load_tape, save_tape


class Tape:
    """Manages a collection of recorded LLM interactions."""

    def __init__(
        self,
        version: str = "1.0",
        provider: str | None = None,
        recorded_at: datetime | None = None,
    ):
        self.version = version
        self.provider = provider
        self.recorded_at = recorded_at or datetime.now(timezone.utc)
        self.interactions: list[dict[str, Any]] = []
        self._replay_index = 0

    @classmethod
    def load(cls, path: str) -> Tape:
        """Load a tape from a file."""
        data = load_tape(path)
        tape = cls(
            version=data.get("version", "1.0"),
            provider=data.get("provider"),
            recorded_at=(
                datetime.fromisoformat(data["recorded_at"])
                if data.get("recorded_at")
                else None
            ),
        )
        tape.interactions = data.get("interactions", [])
        return tape

    def save(self, path: str) -> None:
        """Save the tape to a file."""
        save_tape(self, path)

    def add_interaction(
        self,
        request: dict[str, Any],
        response: Any,
        latency_ms: int | None = None,
        provider: str | None = None,
    ) -> None:
        """Add a new interaction to the tape."""
        # Set provider lazily on first interaction
        if self.provider is None and provider is not None:
            self.provider = provider
        
        interaction = {
            "id": len(self.interactions) + 1,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "request": request,
            "response": response,
        }
        if latency_ms is not None:
            interaction["latency_ms"] = latency_ms
        self.interactions.append(interaction)

    def add_streaming_interaction(
        self,
        request: dict[str, Any],
        chunks: list[Any],
        latency_ms: int | None = None,
        provider: str | None = None,
    ) -> None:
        """Add a streaming interaction to the tape."""
        # Set provider lazily on first interaction
        if self.provider is None and provider is not None:
            self.provider = provider
        
        serialized_chunks = []
        for chunk in chunks:
            if hasattr(chunk, "model_dump"):
                serialized_chunks.append(chunk.model_dump())
            elif isinstance(chunk, dict):
                serialized_chunks.append(chunk)
            else:
                serialized_chunks.append({"raw": str(chunk)})

        interaction = {
            "id": len(self.interactions) + 1,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "request": request,
            "streaming_chunks": serialized_chunks,
        }
        if latency_ms is not None:
            interaction["latency_ms"] = latency_ms
        self.interactions.append(interaction)

    def match_and_return(
        self,
        request: dict[str, Any],
        match_fn: callable | None = None,
    ) -> Any:
        """Find a matching interaction and return its response."""
        from agentape.core.matching import match_exact

        if match_fn is None:
            match_fn = match_exact

        for interaction in self.interactions:
            recorded_request = interaction.get("request", {})
            if match_fn(request, recorded_request):
                return interaction.get("response")

        raise NoMatchingInteractionError(
            f"No matching interaction found for request: {request}"
        )

    def match_and_return_chunks(
        self,
        request: dict[str, Any],
        match_fn: callable | None = None,
    ) -> list[Any]:
        """Find a matching streaming interaction and return its chunks."""
        from agentape.core.matching import match_exact

        if match_fn is None:
            match_fn = match_exact

        for interaction in self.interactions:
            recorded_request = interaction.get("request", {})
            if match_fn(request, recorded_request):
                return interaction.get("streaming_chunks", [])

        raise NoMatchingInteractionError(
            f"No matching streaming interaction found for request: {request}"
        )

    def reset_replay(self) -> None:
        """Reset the replay index to the beginning."""
        self._replay_index = 0
