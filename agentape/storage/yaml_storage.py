"""YAML storage for tape files."""

from __future__ import annotations

import os
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING, Any

import yaml

from agentape.exceptions import TapeFormatError, TapeNotFoundError

if TYPE_CHECKING:
    from agentape.core.tape import Tape


def save_tape(tape: Tape, path: str) -> None:
    """Save a tape to a YAML file."""
    path_obj = Path(path)
    path_obj.parent.mkdir(parents=True, exist_ok=True)

    data = {
        "version": tape.version,
        "recorded_at": tape.recorded_at.isoformat() if tape.recorded_at else None,
        "provider": tape.provider,
        "interactions": [
            _serialize_interaction(interaction) for interaction in tape.interactions
        ],
    }

    with open(path_obj, "w") as f:
        yaml.dump(data, f, default_flow_style=False, sort_keys=False, allow_unicode=True)


def load_tape(path: str) -> dict[str, Any]:
    """Load a tape from a YAML file."""
    path_obj = Path(path)

    if not path_obj.exists():
        raise TapeNotFoundError(f"Tape file not found: {path}")

    with open(path_obj) as f:
        try:
            data = yaml.safe_load(f)
        except yaml.YAMLError as e:
            raise TapeFormatError(f"Invalid YAML in tape file: {e}") from e

    if not isinstance(data, dict):
        raise TapeFormatError("Tape file must contain a YAML mapping")

    if "version" not in data:
        raise TapeFormatError("Tape file missing 'version' field")

    if "interactions" not in data:
        raise TapeFormatError("Tape file missing 'interactions' field")

    return data


def _serialize_interaction(interaction: dict[str, Any]) -> dict[str, Any]:
    """Serialize an interaction for YAML storage."""
    result = {
        "id": interaction.get("id"),
        "timestamp": interaction.get("timestamp"),
        "request": _serialize_request(interaction.get("request", {})),
        "response": _serialize_response(interaction.get("response", {})),
    }

    if "latency_ms" in interaction:
        result["latency_ms"] = interaction["latency_ms"]

    if "streaming_chunks" in interaction:
        result["streaming_chunks"] = interaction["streaming_chunks"]

    return result


def _serialize_request(request: dict[str, Any]) -> dict[str, Any]:
    """Serialize a request for YAML storage."""
    return dict(request)


def _serialize_response(response: Any) -> dict[str, Any]:
    """Serialize a response for YAML storage."""
    if hasattr(response, "model_dump"):
        return response.model_dump()
    if isinstance(response, dict):
        return response
    return {"raw": str(response)}
