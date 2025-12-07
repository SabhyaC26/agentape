"""Request matching strategies for agentape."""

from __future__ import annotations

from enum import Enum
from typing import Any


class MatchMode(Enum):
    """Matching modes for replay."""

    EXACT = "exact"


# Convenience constants
EXACT = MatchMode.EXACT

# Fields to exclude from matching (non-deterministic or irrelevant)
EXCLUDED_FIELDS = frozenset(
    {
        "stream",
        "timeout",
        "extra_headers",
        "extra_query",
        "extra_body",
    }
)


def normalize_request(request: dict[str, Any]) -> dict[str, Any]:
    """Normalize a request for comparison.

    Removes non-deterministic fields and sorts keys for consistent comparison.
    """
    normalized = {}
    for key, value in sorted(request.items()):
        if key in EXCLUDED_FIELDS:
            continue
        if value is None:
            continue
        if isinstance(value, dict):
            normalized[key] = normalize_request(value)
        elif isinstance(value, list):
            normalized[key] = [
                normalize_request(item) if isinstance(item, dict) else item
                for item in value
            ]
        else:
            normalized[key] = value
    return normalized


def match_exact(request: dict[str, Any], recorded: dict[str, Any]) -> bool:
    """Check if two requests match exactly (after normalization)."""
    return normalize_request(request) == normalize_request(recorded)


def get_match_fn(mode: MatchMode) -> callable:
    """Get the matching function for a given mode."""
    if mode == MatchMode.EXACT:
        return match_exact
    else:
        raise ValueError(f"Unknown match mode: {mode}")
