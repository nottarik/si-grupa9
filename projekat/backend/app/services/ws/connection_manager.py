import json
import logging
from typing import Dict, Optional

from fastapi import WebSocket

logger = logging.getLogger(__name__)


class ConnectionManager:
    def __init__(self) -> None:
        self._user_connections: Dict[int, WebSocket] = {}
        # agent_id (str) → WebSocket — one connection per agent, prevents duplicates
        self._agent_connections: Dict[str, WebSocket] = {}

    async def connect_user(self, session_id: int, ws: WebSocket) -> None:
        await ws.accept()
        self._user_connections[session_id] = ws
        logger.info("User WS connected: session=%s", session_id)

    async def connect_agent(self, agent_id: str, ws: WebSocket) -> None:
        await ws.accept()
        old = self._agent_connections.get(agent_id)
        if old:
            try:
                await old.close(code=4000)
            except Exception:
                pass
        self._agent_connections[agent_id] = ws
        logger.info("Agent WS connected: agent=%s, total=%d", agent_id, len(self._agent_connections))

    def disconnect_user(self, session_id: int) -> None:
        self._user_connections.pop(session_id, None)

    def is_user_connected(self, session_id: int) -> bool:
        return session_id in self._user_connections

    def disconnect_agent(self, agent_id: str, ws: WebSocket) -> None:
        if self._agent_connections.get(agent_id) is ws:
            self._agent_connections.pop(agent_id, None)

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

    async def send_to_agent(self, agent_id: str, data: dict) -> bool:
        ws = self._agent_connections.get(agent_id)
        if ws is None:
            return False
        try:
            await ws.send_text(json.dumps(data))
            return True
        except Exception as exc:
            logger.warning("send_to_agent agent=%s failed: %s", agent_id, exc)
            self._agent_connections.pop(agent_id, None)
            return False

    async def broadcast_to_agents(
        self, data: dict, exclude_agent_id: Optional[str] = None
    ) -> None:
        dead: list[str] = []
        payload = json.dumps(data)
        for agent_id, ws in list(self._agent_connections.items()):
            if agent_id == exclude_agent_id:
                continue
            try:
                await ws.send_text(payload)
            except Exception:
                dead.append(agent_id)
        for agent_id in dead:
            self._agent_connections.pop(agent_id, None)


# Global singleton shared across requests
manager = ConnectionManager()
