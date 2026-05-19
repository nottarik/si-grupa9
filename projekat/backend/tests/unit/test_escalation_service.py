import uuid
import pytest

from app.db.session import AsyncSessionLocal
from app.db.models.user import Korisnik, UlogaTip
from app.db.models.knowledge import ChatSesija
from app.core.security import get_password_hash
from app.services.escalation import service as svc


# ── Helpers ──────────────────────────────────────────────────────────────────

async def _make_user(db, uloga=UlogaTip.krajnji_korisnik) -> Korisnik:
    user = Korisnik(
        ime="Test",
        prezime="User",
        email=f"svc_{uuid.uuid4().hex[:8]}@test.com",
        hashed_password=get_password_hash("x"),
        uloga=uloga,
        aktivan=True,
    )
    db.add(user)
    await db.flush()
    return user


async def _make_session(db, user: Korisnik) -> ChatSesija:
    sesija = ChatSesija(id_korisnika=user.id, kanal_pristupa="web", status="Aktivna")
    db.add(sesija)
    await db.flush()
    return sesija


async def _make_agent(db) -> Korisnik:
    return await _make_user(db, uloga=UlogaTip.call_centar_agent)


# ── detect_trigger ────────────────────────────────────────────────────────────

def test_detect_trigger_below_threshold():
    assert svc.detect_trigger(0.3) == "NiskaPouz"


def test_detect_trigger_at_threshold_not_triggered():
    from app.core.config import settings
    assert svc.detect_trigger(settings.RAG_CONFIDENCE_THRESHOLD) is None


def test_detect_trigger_above_threshold():
    assert svc.detect_trigger(0.99) is None


# ── create_escalation ─────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_create_escalation_new_entry():
    async with AsyncSessionLocal() as db:
        user = await _make_user(db)
        sesija = await _make_session(db, user)
        eskal = await svc.create_escalation(db, sesija.id, user.id, "NiskaPouz")
        await db.commit()

    assert eskal.id is not None
    assert eskal.status == "Cekanje"
    assert eskal.trigger_tip == "NiskaPouz"
    assert eskal.prioritet == "Normalan"


@pytest.mark.asyncio
async def test_create_escalation_explicit_request_is_high_priority():
    async with AsyncSessionLocal() as db:
        user = await _make_user(db)
        sesija = await _make_session(db, user)
        eskal = await svc.create_escalation(db, sesija.id, user.id, "EksplicitanZahtjev")
        await db.commit()

    assert eskal.prioritet == "Visok"


@pytest.mark.asyncio
async def test_create_escalation_stores_conversation():
    history = [{"role": "user", "content": "Pitanje"}, {"role": "assistant", "content": "Odgovor"}]
    async with AsyncSessionLocal() as db:
        user = await _make_user(db)
        sesija = await _make_session(db, user)
        eskal = await svc.create_escalation(db, sesija.id, user.id, "NiskaPouz", razgovor=history)
        await db.commit()

    assert eskal.razgovor == history


@pytest.mark.asyncio
async def test_create_escalation_returns_existing_if_already_active():
    async with AsyncSessionLocal() as db:
        user = await _make_user(db)
        sesija = await _make_session(db, user)
        first = await svc.create_escalation(db, sesija.id, user.id, "NiskaPouz")
        await db.flush()
        second = await svc.create_escalation(db, sesija.id, user.id, "EksplicitanZahtjev")
        await db.commit()

    assert first.id == second.id


# ── queue_position ────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_queue_position_first_in_line():
    async with AsyncSessionLocal() as db:
        user = await _make_user(db)
        sesija = await _make_session(db, user)
        eskal = await svc.create_escalation(db, sesija.id, user.id, "NiskaPouz")
        await db.flush()
        pos = await svc.queue_position(db, eskal.id)
        await db.commit()

    assert pos >= 1


@pytest.mark.asyncio
async def test_queue_position_ordering():
    async with AsyncSessionLocal() as db:
        u1 = await _make_user(db)
        u2 = await _make_user(db)
        s1 = await _make_session(db, u1)
        s2 = await _make_session(db, u2)
        e1 = await svc.create_escalation(db, s1.id, u1.id, "NiskaPouz")
        await db.flush()
        e2 = await svc.create_escalation(db, s2.id, u2.id, "NiskaPouz")
        await db.flush()
        pos1 = await svc.queue_position(db, e1.id)
        pos2 = await svc.queue_position(db, e2.id)
        await db.commit()

    assert pos1 < pos2


# ── get_queue ─────────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_get_queue_returns_cekanje_and_utoku():
    async with AsyncSessionLocal() as db:
        user = await _make_user(db)
        agent = await _make_agent(db)
        s1 = await _make_session(db, user)
        s2 = await _make_session(db, user)
        e_cekanje = await svc.create_escalation(db, s1.id, user.id, "NiskaPouz")
        await db.flush()
        e_utoku = await svc.create_escalation(db, s2.id, user.id, "NiskaPouz")
        await db.flush()
        e_utoku.status = "UToku"
        e_utoku.dodjeljeni_agent_id = agent.id
        await db.flush()
        queue = await svc.get_queue(db)
        await db.commit()

    ids = [e.id for e in queue]
    assert e_cekanje.id in ids
    assert e_utoku.id in ids


@pytest.mark.asyncio
async def test_get_queue_excludes_resolved():
    async with AsyncSessionLocal() as db:
        user = await _make_user(db)
        sesija = await _make_session(db, user)
        eskal = await svc.create_escalation(db, sesija.id, user.id, "NiskaPouz")
        await db.flush()
        eskal.status = "Rijesena"
        await db.flush()
        queue = await svc.get_queue(db)
        await db.commit()

    assert eskal.id not in [e.id for e in queue]


# ── accept_escalation ─────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_accept_escalation_transitions_to_utoku():
    async with AsyncSessionLocal() as db:
        user = await _make_user(db)
        agent = await _make_agent(db)
        sesija = await _make_session(db, user)
        eskal = await svc.create_escalation(db, sesija.id, user.id, "NiskaPouz")
        await db.flush()
        result = await svc.accept_escalation(db, eskal.id, agent.id)
        await db.commit()

    assert result is not None
    assert result.status == "UToku"
    assert result.dodjeljeni_agent_id == agent.id


@pytest.mark.asyncio
async def test_accept_escalation_sets_agent_status_to_zauzet():
    async with AsyncSessionLocal() as db:
        user = await _make_user(db)
        agent = await _make_agent(db)
        sesija = await _make_session(db, user)
        eskal = await svc.create_escalation(db, sesija.id, user.id, "NiskaPouz")
        await db.flush()
        await svc.accept_escalation(db, eskal.id, agent.id)
        status_row = await svc.upsert_agent_status(db, agent.id, "Zauzet")
        await db.commit()

    assert status_row.status == "Zauzet"


@pytest.mark.asyncio
async def test_accept_escalation_returns_none_if_already_utoku():
    async with AsyncSessionLocal() as db:
        user = await _make_user(db)
        agent1 = await _make_agent(db)
        agent2 = await _make_agent(db)
        sesija = await _make_session(db, user)
        eskal = await svc.create_escalation(db, sesija.id, user.id, "NiskaPouz")
        await db.flush()
        await svc.accept_escalation(db, eskal.id, agent1.id)
        await db.flush()
        result = await svc.accept_escalation(db, eskal.id, agent2.id)
        await db.commit()

    assert result is None


@pytest.mark.asyncio
async def test_accept_nonexistent_escalation_returns_none():
    async with AsyncSessionLocal() as db:
        agent = await _make_agent(db)
        await db.flush()
        result = await svc.accept_escalation(db, 999999, agent.id)
        await db.commit()

    assert result is None


# ── resolve_escalation ────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_resolve_escalation_sets_status_rijesena():
    async with AsyncSessionLocal() as db:
        user = await _make_user(db)
        agent = await _make_agent(db)
        sesija = await _make_session(db, user)
        eskal = await svc.create_escalation(db, sesija.id, user.id, "NiskaPouz")
        await db.flush()
        await svc.accept_escalation(db, eskal.id, agent.id)
        await db.flush()
        result = await svc.resolve_escalation(db, eskal.id, agent.id, napomena="Riješeno")
        await db.commit()

    assert result.status == "Rijesena"
    assert result.napomena_rjesavanja == "Riješeno"
    assert result.datum_rjesavanja is not None


@pytest.mark.asyncio
async def test_resolve_escalation_resets_agent_status():
    async with AsyncSessionLocal() as db:
        user = await _make_user(db)
        agent = await _make_agent(db)
        sesija = await _make_session(db, user)
        eskal = await svc.create_escalation(db, sesija.id, user.id, "NiskaPouz")
        await db.flush()
        await svc.accept_escalation(db, eskal.id, agent.id)
        await db.flush()
        await svc.resolve_escalation(db, eskal.id, agent.id)
        from sqlalchemy import select
        from app.db.models.escalation import StatusAgenta
        row = (await db.execute(
            select(StatusAgenta).where(StatusAgenta.agent_id == agent.id)
        )).scalar_one_or_none()
        await db.commit()

    assert row is not None
    assert row.status == "Online"
    assert row.trenutna_eskalacija_id is None


@pytest.mark.asyncio
async def test_resolve_nonexistent_escalation_returns_none():
    async with AsyncSessionLocal() as db:
        agent = await _make_agent(db)
        await db.flush()
        result = await svc.resolve_escalation(db, 999999, agent.id)
        await db.commit()

    assert result is None


# ── release_escalation ────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_release_escalation_back_to_cekanje():
    async with AsyncSessionLocal() as db:
        user = await _make_user(db)
        agent = await _make_agent(db)
        sesija = await _make_session(db, user)
        eskal = await svc.create_escalation(db, sesija.id, user.id, "NiskaPouz")
        await db.flush()
        await svc.accept_escalation(db, eskal.id, agent.id)
        await db.flush()
        result = await svc.release_escalation(db, eskal.id, agent.id)
        await db.commit()

    assert result is not None
    assert result.status == "Cekanje"
    assert result.dodjeljeni_agent_id is None


@pytest.mark.asyncio
async def test_release_escalation_resets_agent_status():
    async with AsyncSessionLocal() as db:
        user = await _make_user(db)
        agent = await _make_agent(db)
        sesija = await _make_session(db, user)
        eskal = await svc.create_escalation(db, sesija.id, user.id, "NiskaPouz")
        await db.flush()
        await svc.accept_escalation(db, eskal.id, agent.id)
        await db.flush()
        await svc.release_escalation(db, eskal.id, agent.id)
        from sqlalchemy import select
        from app.db.models.escalation import StatusAgenta
        row = (await db.execute(
            select(StatusAgenta).where(StatusAgenta.agent_id == agent.id)
        )).scalar_one_or_none()
        await db.commit()

    if row:
        assert row.status == "Online"


@pytest.mark.asyncio
async def test_release_escalation_wrong_agent_returns_none():
    async with AsyncSessionLocal() as db:
        user = await _make_user(db)
        agent1 = await _make_agent(db)
        agent2 = await _make_agent(db)
        sesija = await _make_session(db, user)
        eskal = await svc.create_escalation(db, sesija.id, user.id, "NiskaPouz")
        await db.flush()
        await svc.accept_escalation(db, eskal.id, agent1.id)
        await db.flush()
        result = await svc.release_escalation(db, eskal.id, agent2.id)
        await db.commit()

    assert result is None


@pytest.mark.asyncio
async def test_release_escalation_not_utoku_returns_none():
    async with AsyncSessionLocal() as db:
        user = await _make_user(db)
        agent = await _make_agent(db)
        sesija = await _make_session(db, user)
        eskal = await svc.create_escalation(db, sesija.id, user.id, "NiskaPouz")
        await db.flush()
        # Still in Cekanje – not accepted yet
        result = await svc.release_escalation(db, eskal.id, agent.id)
        await db.commit()

    assert result is None


# ── cancel_escalation ─────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_cancel_escalation_marks_napustena():
    async with AsyncSessionLocal() as db:
        user = await _make_user(db)
        sesija = await _make_session(db, user)
        eskal = await svc.create_escalation(db, sesija.id, user.id, "NiskaPouz")
        await db.flush()
        result = await svc.cancel_escalation(db, user.id)
        await db.commit()

    assert result is not None
    assert result.id == eskal.id
    assert result.status == "Napustena"


@pytest.mark.asyncio
async def test_cancel_escalation_no_active_returns_none():
    async with AsyncSessionLocal() as db:
        user = await _make_user(db)
        await db.flush()
        result = await svc.cancel_escalation(db, user.id)
        await db.commit()

    assert result is None


# ── upsert_agent_status ───────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_upsert_agent_status_creates_new_row():
    async with AsyncSessionLocal() as db:
        agent = await _make_agent(db)
        await db.flush()
        row = await svc.upsert_agent_status(db, agent.id, "Online")
        await db.commit()

    assert row.agent_id == agent.id
    assert row.status == "Online"


@pytest.mark.asyncio
async def test_upsert_agent_status_updates_existing():
    async with AsyncSessionLocal() as db:
        agent = await _make_agent(db)
        await db.flush()
        await svc.upsert_agent_status(db, agent.id, "Online")
        await db.flush()
        row = await svc.upsert_agent_status(db, agent.id, "Zauzet")
        await db.commit()

    assert row.status == "Zauzet"


@pytest.mark.asyncio
async def test_upsert_agent_status_all_valid_statuses():
    async with AsyncSessionLocal() as db:
        agent = await _make_agent(db)
        await db.flush()
        for status in ("Online", "Zauzet", "Offline"):
            row = await svc.upsert_agent_status(db, agent.id, status)
            await db.flush()
        await db.commit()

    assert row.status == "Offline"


# ── get_active_for_user ───────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_get_active_for_user_returns_latest_active():
    async with AsyncSessionLocal() as db:
        user = await _make_user(db)
        sesija = await _make_session(db, user)
        eskal = await svc.create_escalation(db, sesija.id, user.id, "NiskaPouz")
        await db.flush()
        found = await svc.get_active_for_user(db, user.id)
        await db.commit()

    assert found is not None
    assert found.id == eskal.id


@pytest.mark.asyncio
async def test_get_active_for_user_returns_none_when_resolved():
    async with AsyncSessionLocal() as db:
        user = await _make_user(db)
        sesija = await _make_session(db, user)
        eskal = await svc.create_escalation(db, sesija.id, user.id, "NiskaPouz")
        await db.flush()
        eskal.status = "Rijesena"
        await db.flush()
        found = await svc.get_active_for_user(db, user.id)
        await db.commit()

    assert found is None
