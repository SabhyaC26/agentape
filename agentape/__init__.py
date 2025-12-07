"""agentape - Record/replay testing for LLM agents.

Usage:
    import agentape
    from openai import OpenAI

    # Wrap the client
    client = agentape.wrap(OpenAI())

    # Record interactions
    with agentape.record("tapes/my_flow.yaml"):
        response = client.chat.completions.create(...)

    # Replay interactions
    with agentape.replay("tapes/my_flow.yaml"):
        response = client.chat.completions.create(...)
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, TypeVar, overload

from agentape.core.matching import EXACT, FUZZY, SEMANTIC, MatchMode
from agentape.core.recorder import record
from agentape.core.registry import register_client
from agentape.core.replayer import replay
from agentape.exceptions import (
    AgentapeError,
    NoMatchingInteractionError,
    TapeFormatError,
    TapeNotFoundError,
)
from agentape.pytest_plugin import use_tape

if TYPE_CHECKING:
    from openai import OpenAI

    from agentape.clients.openai_client import WrappedOpenAIClient

__version__ = "0.1.0"

T = TypeVar("T")


@overload
def wrap(client: OpenAI) -> WrappedOpenAIClient: ...


@overload
def wrap(client: T) -> T: ...


def wrap(client: Any) -> Any:
    """Wrap an LLM client for record/replay functionality.

    Currently supports:
        - OpenAI client

    Args:
        client: The LLM client to wrap.

    Returns:
        A wrapped client that supports recording and replaying interactions.

    Example:
        from openai import OpenAI
        import agentape

        client = agentape.wrap(OpenAI())
    """
    # Detect client type
    client_type = type(client).__name__
    client_module = type(client).__module__

    if client_type == "OpenAI" and "openai" in client_module:
        from agentape.clients.openai_client import WrappedOpenAIClient

        wrapped = WrappedOpenAIClient(client)
        register_client(wrapped)
        return wrapped

    # Phase 2: Anthropic support
    # if client_type == "Anthropic" and "anthropic" in client_module:
    #     from agentape.clients.anthropic import WrappedAnthropicClient
    #     wrapped = WrappedAnthropicClient(client)
    #     register_client(wrapped)
    #     return wrapped

    raise TypeError(
        f"Unsupported client type: {client_type}. "
        "Currently supported: OpenAI. "
        "Anthropic support coming in Phase 2."
    )


__all__ = [
    # Main API
    "wrap",
    "record",
    "replay",
    "use_tape",
    # Matching modes
    "EXACT",
    "SEMANTIC",
    "FUZZY",
    "MatchMode",
    # Exceptions
    "AgentapeError",
    "TapeNotFoundError",
    "NoMatchingInteractionError",
    "TapeFormatError",
    # Version
    "__version__",
]
