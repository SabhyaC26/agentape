"""OpenAI client wrapper for agentape."""

from __future__ import annotations

import time
from typing import TYPE_CHECKING, Any, Generator, Iterator

from agentape.clients.base import BaseWrappedClient

if TYPE_CHECKING:
    from openai import OpenAI
    from openai.types.chat import ChatCompletion, ChatCompletionChunk

    from agentape.core.context import TapeContext


class WrappedCompletions:
    """Wrapper for OpenAI chat completions."""

    def __init__(self, completions: Any, get_context: callable):
        self._completions = completions
        self._get_context = get_context

    def create(self, **kwargs) -> ChatCompletion | Iterator[ChatCompletionChunk]:
        """Create a chat completion, with recording/replay support."""
        context = self._get_context()

        if context is None or context.mode == "off":
            return self._completions.create(**kwargs)

        is_streaming = kwargs.get("stream", False)

        if context.mode == "record":
            return self._record_create(kwargs, is_streaming)
        elif context.mode == "replay":
            return self._replay_create(kwargs, is_streaming)
        else:
            return self._completions.create(**kwargs)

    def _record_create(
        self, kwargs: dict[str, Any], is_streaming: bool
    ) -> ChatCompletion | Generator[ChatCompletionChunk, None, None]:
        """Record an API call."""
        context = self._get_context()
        request = self._build_request(kwargs)

        start_time = time.time()

        if is_streaming:
            return self._record_streaming(kwargs, request, start_time, context)
        else:
            response = self._completions.create(**kwargs)
            latency_ms = int((time.time() - start_time) * 1000)
            context.tape.add_interaction(request, response, latency_ms)
            return response

    def _record_streaming(
        self,
        kwargs: dict[str, Any],
        request: dict[str, Any],
        start_time: float,
        context: TapeContext,
    ) -> Generator[ChatCompletionChunk, None, None]:
        """Record a streaming API call."""
        chunks = []
        for chunk in self._completions.create(**kwargs):
            chunks.append(chunk)
            yield chunk

        latency_ms = int((time.time() - start_time) * 1000)
        context.tape.add_streaming_interaction(request, chunks, latency_ms)

    def _replay_create(
        self, kwargs: dict[str, Any], is_streaming: bool
    ) -> ChatCompletion | Generator[ChatCompletionChunk, None, None]:
        """Replay a recorded API call."""
        context = self._get_context()
        request = self._build_request(kwargs)

        if is_streaming:
            return self._replay_streaming(request, context)
        else:
            response_data = context.tape.match_and_return(request, context.match_fn)
            return self._reconstruct_response(response_data)

    def _replay_streaming(
        self, request: dict[str, Any], context: TapeContext
    ) -> Generator[dict[str, Any], None, None]:
        """Replay a streaming API call."""
        chunks = context.tape.match_and_return_chunks(request, context.match_fn)
        for chunk in chunks:
            yield chunk

    def _build_request(self, kwargs: dict[str, Any]) -> dict[str, Any]:
        """Build a request dict from kwargs."""
        request = {"method": "chat.completions.create"}
        request.update(kwargs)
        return request

    def _reconstruct_response(self, data: dict[str, Any]) -> Any:
        """Reconstruct a response object from stored data."""
        try:
            from openai.types.chat import ChatCompletion

            return ChatCompletion.model_validate(data)
        except Exception:
            return data


class WrappedChat:
    """Wrapper for OpenAI chat namespace."""

    def __init__(self, chat: Any, get_context: callable):
        self._chat = chat
        self._get_context = get_context
        self._completions = WrappedCompletions(chat.completions, get_context)

    @property
    def completions(self) -> WrappedCompletions:
        """Return the wrapped completions object."""
        return self._completions


class WrappedOpenAIClient(BaseWrappedClient):
    """Wrapper for OpenAI client."""

    def __init__(self, client: OpenAI):
        super().__init__(client)
        self._chat = WrappedChat(client.chat, self._get_context)

    @property
    def provider(self) -> str:
        """Return the provider name."""
        return "openai"

    @property
    def chat(self) -> WrappedChat:
        """Return the wrapped chat namespace."""
        return self._chat

    def _get_context(self) -> TapeContext | None:
        """Get the current tape context."""
        return self._tape_context

    def __getattr__(self, name: str) -> Any:
        """Proxy other attributes to the underlying client."""
        return getattr(self._client, name)
