"""Core agentape functionality."""

from agentape.core.tape import Tape
from agentape.core.recorder import record
from agentape.core.replayer import replay
from agentape.core.matching import EXACT, MatchMode
from agentape.core.context import TapeContext, get_current_context
from agentape.core.registry import register_client, get_registered_clients

__all__ = [
    "Tape",
    "record",
    "replay",
    "EXACT",
    "MatchMode",
    "TapeContext",
    "get_current_context",
    "register_client",
    "get_registered_clients",
]
