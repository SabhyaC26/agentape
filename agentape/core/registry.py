"""Registry for wrapped clients."""

from __future__ import annotations

import weakref
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from agentape.clients.base import BaseWrappedClient

# Use weak references so clients can be garbage collected
_registered_clients: weakref.WeakSet[BaseWrappedClient] = weakref.WeakSet()


def register_client(client: BaseWrappedClient) -> None:
    """Register a wrapped client."""
    _registered_clients.add(client)


def unregister_client(client: BaseWrappedClient) -> None:
    """Unregister a wrapped client."""
    _registered_clients.discard(client)


def get_registered_clients() -> list[BaseWrappedClient]:
    """Get all registered wrapped clients."""
    return list(_registered_clients)


def clear_registry() -> None:
    """Clear all registered clients."""
    _registered_clients.clear()
