import json
import logging
from typing import Dict, Set

from fastapi import WebSocket

logger = logging.getLogger(__name__)


class ConnectionManager:
    def __init__(self) -> None:
        # session_id → WebSocket (one per user session)
        self._user_connections: Dict[int, WebSocket] = {}
        # All connected agent WebSockets
        self._agent_connections: Set[WebSocket] = set()

    async def connect_user(self, session_id: int, ws: WebSocket) -> None:
        await ws.accept()
        self._user_connections[session_id] = ws
        logger.info("User WS connected: session=%s", session_id)

    async def connect_agent(self, ws: WebSocket) -> None:
        await ws.accept()
        self._agent_connections.add(ws)
        logger.info("Agent WS connected, total=%d", len(self._agent_connections))

    def disconnect_user(self, session_id: int) -> None:
        self._user_connections.pop(session_id, None)

    def disconnect_agent(self, ws: WebSocket) -> None:
        self._agent_connections.discard(ws)

    async def send_to_user(self, session_id: int, data: dict) -> bool:
        ws = self._user_connections.get(session_id)
        if ws is None:
            return False
        try:
            await ws.send_text(json.dumps(data))
            return True
        except Exception as exc:
            logger.warning("send_to_user session=%s failed: %s", session_id, exc)
            self._user_connections.pop(session_id, None)
            return False

    async def broadcast_to_agents(self, data: dict) -> None:
        dead: Set[WebSocket] = set()
        payload = json.dumps(data)
        for ws in list(self._agent_connections):
            try:
                await ws.send_text(payload)
            except Exception:
                dead.add(ws)
        for ws in dead:
            self._agent_connections.discard(ws)


# Global singleton shared across requests
manager = ConnectionManager()
