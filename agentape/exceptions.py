"""Custom exceptions for agentape."""


class AgentapeError(Exception):
    """Base exception for agentape."""


class TapeNotFoundError(AgentapeError):
    """Tape file doesn't exist in replay mode."""


class NoMatchingInteractionError(AgentapeError):
    """No recorded interaction matches the request."""


class TapeFormatError(AgentapeError):
    """Invalid tape file format."""
