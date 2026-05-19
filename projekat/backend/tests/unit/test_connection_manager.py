import json
import pytest
from unittest.mock import AsyncMock

from app.services.ws.connection_manager import ConnectionManager


@pytest.mark.asyncio
async def test_connect_user_accepts_and_registers():
    cm = ConnectionManager()
    ws = AsyncMock()
    await cm.connect_user(42, ws)
    ws.accept.assert_awaited_once()
    assert cm._user_connections[42] is ws


@pytest.mark.asyncio
async def test_connect_user_overwrites_previous():
    cm = ConnectionManager()
    ws1, ws2 = AsyncMock(), AsyncMock()
    await cm.connect_user(1, ws1)
    await cm.connect_user(1, ws2)
    assert cm._user_connections[1] is ws2


@pytest.mark.asyncio
async def test_disconnect_user_removes_entry():
    cm = ConnectionManager()
    ws = AsyncMock()
    await cm.connect_user(42, ws)
    cm.disconnect_user(42)
    assert 42 not in cm._user_connections


@pytest.mark.asyncio
async def test_disconnect_user_noop_when_missing():
    cm = ConnectionManager()
    cm.disconnect_user(999)  # must not raise


@pytest.mark.asyncio
async def test_connect_agent_accepts_and_registers():
    cm = ConnectionManager()
    ws = AsyncMock()
    await cm.connect_agent("a1", ws)
    ws.accept.assert_awaited_once()
    assert cm._agent_connections["a1"] is ws


@pytest.mark.asyncio
async def test_connect_agent_closes_old_connection():
    cm = ConnectionManager()
    old, new = AsyncMock(), AsyncMock()
    await cm.connect_agent("a1", old)
    await cm.connect_agent("a1", new)
    old.close.assert_awaited_once_with(code=4000)
    assert cm._agent_connections["a1"] is new


@pytest.mark.asyncio
async def test_connect_agent_tolerates_old_close_failure():
    cm = ConnectionManager()
    old = AsyncMock()
    old.close.side_effect = Exception("already closed")
    new = AsyncMock()
    await cm.connect_agent("a1", old)
    await cm.connect_agent("a1", new)
    assert cm._agent_connections["a1"] is new


@pytest.mark.asyncio
async def test_disconnect_agent_removes_matching_ws():
    cm = ConnectionManager()
    ws = AsyncMock()
    await cm.connect_agent("a1", ws)
    cm.disconnect_agent("a1", ws)
    assert "a1" not in cm._agent_connections


@pytest.mark.asyncio
async def test_disconnect_agent_ignores_different_ws():
    cm = ConnectionManager()
    ws1, ws2 = AsyncMock(), AsyncMock()
    await cm.connect_agent("a1", ws1)
    cm.disconnect_agent("a1", ws2)
    assert "a1" in cm._agent_connections


@pytest.mark.asyncio
async def test_send_to_user_success():
    cm = ConnectionManager()
    ws = AsyncMock()
    await cm.connect_user(1, ws)
    result = await cm.send_to_user(1, {"type": "ping"})
    assert result is True
    ws.send_text.assert_awaited_once_with(json.dumps({"type": "ping"}))


@pytest.mark.asyncio
async def test_send_to_user_not_connected_returns_false():
    cm = ConnectionManager()
    result = await cm.send_to_user(999, {"type": "ping"})
    assert result is False


@pytest.mark.asyncio
async def test_send_to_user_removes_dead_connection():
    cm = ConnectionManager()
    ws = AsyncMock()
    ws.send_text.side_effect = Exception("broken pipe")
    await cm.connect_user(7, ws)
    result = await cm.send_to_user(7, {"type": "ping"})
    assert result is False
    assert 7 not in cm._user_connections


@pytest.mark.asyncio
async def test_send_to_agent_success():
    cm = ConnectionManager()
    ws = AsyncMock()
    await cm.connect_agent("a1", ws)
    result = await cm.send_to_agent("a1", {"type": "queue_update", "data": []})
    assert result is True
    ws.send_text.assert_awaited_once()


@pytest.mark.asyncio
async def test_send_to_agent_not_connected_returns_false():
    cm = ConnectionManager()
    result = await cm.send_to_agent("nobody", {"type": "x"})
    assert result is False


@pytest.mark.asyncio
async def test_send_to_agent_removes_dead_connection():
    cm = ConnectionManager()
    ws = AsyncMock()
    ws.send_text.side_effect = Exception("gone")
    await cm.connect_agent("a1", ws)
    result = await cm.send_to_agent("a1", {"type": "x"})
    assert result is False
    assert "a1" not in cm._agent_connections


@pytest.mark.asyncio
async def test_broadcast_to_agents_sends_to_all():
    cm = ConnectionManager()
    ws1, ws2 = AsyncMock(), AsyncMock()
    await cm.connect_agent("a1", ws1)
    await cm.connect_agent("a2", ws2)
    await cm.broadcast_to_agents({"type": "update"})
    ws1.send_text.assert_awaited_once()
    ws2.send_text.assert_awaited_once()


@pytest.mark.asyncio
async def test_broadcast_to_agents_excludes_sender():
    cm = ConnectionManager()
    ws1, ws2 = AsyncMock(), AsyncMock()
    await cm.connect_agent("a1", ws1)
    await cm.connect_agent("a2", ws2)
    await cm.broadcast_to_agents({"type": "update"}, exclude_agent_id="a1")
    ws1.send_text.assert_not_called()
    ws2.send_text.assert_awaited_once()


@pytest.mark.asyncio
async def test_broadcast_to_agents_removes_dead_connections():
    cm = ConnectionManager()
    dead, alive = AsyncMock(), AsyncMock()
    dead.send_text.side_effect = Exception("connection reset")
    await cm.connect_agent("dead", dead)
    await cm.connect_agent("alive", alive)
    await cm.broadcast_to_agents({"type": "update"})
    assert "dead" not in cm._agent_connections
    assert "alive" in cm._agent_connections


@pytest.mark.asyncio
async def test_broadcast_sends_same_payload_to_all():
    cm = ConnectionManager()
    ws1, ws2 = AsyncMock(), AsyncMock()
    await cm.connect_agent("a1", ws1)
    await cm.connect_agent("a2", ws2)
    payload = {"type": "queue_update", "data": [1, 2]}
    await cm.broadcast_to_agents(payload)
    expected = json.dumps(payload)
    ws1.send_text.assert_awaited_once_with(expected)
    ws2.send_text.assert_awaited_once_with(expected)
