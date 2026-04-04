"""EventBus — fan-out of Incus events to all connected clients.

The daemon subscribes to the Incus event stream once (via IncusClient) and
publishes each event here. HTTP SSE connections and D-Bus signal emission
both subscribe to this bus.
"""

from __future__ import annotations

import asyncio
import logging
from collections.abc import AsyncIterator
from typing import Any

logger = logging.getLogger(__name__)


class EventBus:
    """Async pub/sub bus for Incus events."""

    def __init__(self) -> None:
        self._subscribers: list[asyncio.Queue[dict[str, Any]]] = []

    def subscribe(self) -> asyncio.Queue[dict[str, Any]]:
        """Return a queue that will receive all future events."""
        q: asyncio.Queue[dict[str, Any]] = asyncio.Queue(maxsize=256)
        self._subscribers.append(q)
        return q

    def unsubscribe(self, q: asyncio.Queue[dict[str, Any]]) -> None:
        try:
            self._subscribers.remove(q)
        except ValueError:
            pass

    async def publish(self, event: dict[str, Any]) -> None:
        """Publish an event to all subscribers, dropping if a queue is full."""
        dead: list[asyncio.Queue[dict[str, Any]]] = []
        for q in self._subscribers:
            try:
                q.put_nowait(event)
            except asyncio.QueueFull:
                logger.warning("EventBus: subscriber queue full, dropping event")
            except Exception:
                dead.append(q)
        for q in dead:
            self.unsubscribe(q)

    async def iter_events(
        self,
        type_filter: str = "",
        project_filter: str = "",
    ) -> AsyncIterator[dict[str, Any]]:
        """Async generator that yields events matching the given filters."""
        q = self.subscribe()
        try:
            while True:
                event = await q.get()
                if type_filter and event.get("type") != type_filter:
                    continue
                if project_filter and event.get("project") != project_filter:
                    continue
                yield event
        finally:
            self.unsubscribe(q)
