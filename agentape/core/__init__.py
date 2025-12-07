"""Core agentape functionality."""

from agentape.core.context import TapeContext, get_current_context
from agentape.core.matching import EXACT, MatchMode
from agentape.core.recorder import record
from agentape.core.registry import get_registered_clients, register_client
from agentape.core.replayer import replay
from agentape.core.tape import Tape

__all__ = [
    "EXACT",
    "MatchMode",
    "Tape",
    "TapeContext",
    "get_current_context",
    "get_registered_clients",
    "record",
    "register_client",
    "replay",
]
