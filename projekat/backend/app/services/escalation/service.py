import logging
import re
from datetime import datetime, timezone
from typing import List, Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.db.models.escalation import Eskalacija, StatusAgenta
from app.db.models.knowledge import ChatSesija, UnosBazeZnanja
from app.services.ai.kb_indexing import embed_and_index_item

logger = logging.getLogger(__name__)


async def _close_chat_session(db: AsyncSession, sesija_id: int) -> None:
    """Mark the chat session closed so it shows as 'Closed' in the user's history,
    regardless of whether the user's client was around to call /close itself."""
    sess = (await db.execute(
        select(ChatSesija).where(ChatSesija.id == sesija_id)
    )).scalar_one_or_none()
    if sess and sess.status != "Zatvorena":
        sess.status = "Zatvorena"
        sess.datum_zavrsetka = datetime.now(timezone.utc)


def _free_agent(agent_row: Optional[StatusAgenta]) -> None:
    if agent_row:
        agent_row.status = "Online"
        agent_row.trenutna_eskalacija_id = None
        agent_row.zadnje_aktivno = datetime.now(timezone.utc)


def format_question(text: str) -> str:
    """Light cleanup of a raw chat message before it becomes a KB question:
    collapse whitespace, capitalize the first letter, ensure a trailing '?'."""
    q = re.sub(r"\s+", " ", text or "").strip()
    if not q:
        return ""
    q = q[0].upper() + q[1:]
    if not q.endswith("?"):
        q = q.rstrip(".!,;: ") + "?"
    return q


def detect_trigger(confidence: float) -> Optional[str]:
    """Auto-escalate only when the bot cannot answer confidently."""
    if confidence < settings.RAG_CONFIDENCE_THRESHOLD:
        return "NiskaPouz"
    return None


async def get_active_for_user(db: AsyncSession, korisnik_id: UUID) -> Optional[Eskalacija]:
    result = await db.execute(
        select(Eskalacija)
        .where(
            Eskalacija.korisnik_id == korisnik_id,
            Eskalacija.status.in_(["Cekanje", "UToku"]),
        )
        .order_by(Eskalacija.id.desc())
        .limit(1)
    )
    return result.scalar_one_or_none()


async def create_escalation(
    db: AsyncSession,
    sesija_id: int,
    korisnik_id: UUID,
    trigger: str,
    razgovor: Optional[List[dict]] = None,
    tema: Optional[str] = None,
) -> Eskalacija:
    # One user, one active queue entry
    existing = await get_active_for_user(db, korisnik_id)
    if existing:
        return existing

    prioritet = "Visok" if trigger == "EksplicitanZahtjev" else "Normalan"
    eskal = Eskalacija(
        sesija_id=sesija_id,
        korisnik_id=korisnik_id,
        trigger_tip=trigger,
        prioritet=prioritet,
        status="Cekanje",
        tema=tema,
        razgovor=razgovor or [],
    )
    db.add(eskal)
    await db.flush()
    await db.refresh(eskal)
    return eskal


async def queue_position(db: AsyncSession, escalation_id: int) -> int:
    """1-based queue position among 'Cekanje' escalations ordered by id."""
    result = await db.execute(
        select(Eskalacija.id)
        .where(Eskalacija.status == "Cekanje")
        .order_by(Eskalacija.id)
    )
    ids = [row[0] for row in result.all()]
    try:
        return ids.index(escalation_id) + 1
    except ValueError:
        return 1


async def get_queue(db: AsyncSession) -> List[Eskalacija]:
    result = await db.execute(
        select(Eskalacija)
        .where(Eskalacija.status.in_(["Cekanje", "UToku"]))
        .order_by(Eskalacija.datum_kreiranja.asc())
    )
    return list(result.scalars().all())


async def accept_escalation(
    db: AsyncSession, escalation_id: int, agent_id: UUID
) -> Optional[Eskalacija]:
    result = await db.execute(
        select(Eskalacija).where(Eskalacija.id == escalation_id).with_for_update()
    )
    eskal = result.scalar_one_or_none()
    if not eskal or eskal.status != "Cekanje":
        return None

    eskal.status = "UToku"
    eskal.dodjeljeni_agent_id = agent_id
    eskal.datum_azuriranja = datetime.now(timezone.utc)

    agent_row = (await db.execute(
        select(StatusAgenta).where(StatusAgenta.agent_id == agent_id)
    )).scalar_one_or_none()
    if agent_row:
        agent_row.status = "Zauzet"
        agent_row.trenutna_eskalacija_id = escalation_id
        agent_row.zadnje_aktivno = datetime.now(timezone.utc)
    else:
        db.add(StatusAgenta(
            agent_id=agent_id,
            status="Zauzet",
            trenutna_eskalacija_id=escalation_id,
        ))

    await db.flush()
    await db.refresh(eskal)
    return eskal


async def resolve_escalation(
    db: AsyncSession,
    escalation_id: int,
    agent_id: UUID,
    napomena: str = "",
    submit_to_kb: bool = False,
    kb_unosi: Optional[List[tuple[str, str]]] = None,
) -> Optional[Eskalacija]:
    result = await db.execute(select(Eskalacija).where(Eskalacija.id == escalation_id))
    eskal = result.scalar_one_or_none()
    if not eskal:
        return None

    eskal.status = "Rijesena"
    eskal.datum_rjesavanja = datetime.now(timezone.utc)
    eskal.napomena_rjesavanja = napomena
    # Close the chat session so the user's history shows it as Closed even if their
    # client wasn't connected to call /close (e.g. they walked away before resolve).
    await _close_chat_session(db, eskal.sesija_id)

    agent_row = (await db.execute(
        select(StatusAgenta).where(StatusAgenta.agent_id == agent_id)
    )).scalar_one_or_none()
    _free_agent(agent_row)

    if submit_to_kb and kb_unosi:
        # Auto-publish: each ticked Q&A pair becomes an approved, live KB entry
        # (no separate moderation step), still editable/deletable in the admin UI.
        new_items = []
        for raw_q, raw_a in kb_unosi:
            pitanje = format_question(raw_q)
            odgovor = (raw_a or "").strip()
            if not pitanje or not odgovor:
                continue
            item = UnosBazeZnanja(
                pitanje=pitanje,
                odgovor=odgovor,
                status_aprovacije="Odobren",
                aktivan=True,
                pregledano=True,
                verzija_broj=1,
            )
            db.add(item)
            new_items.append(item)

        await db.flush()  # assign ids before embedding

        for item in new_items:
            try:
                await embed_and_index_item(item)
            except Exception:
                logger.warning(
                    "Qdrant indexing failed for KB item %s from escalation %s; "
                    "saved without vector.", item.id, escalation_id
                )

    await db.flush()
    await db.refresh(eskal)
    return eskal


async def expire_escalation(db: AsyncSession, escalation_id: int) -> Optional[Eskalacija]:
    """End an in-progress escalation whose user didn't return within the grace window.
    Marks it Napustena, frees the agent, and closes the chat session. Returns None if
    the escalation is no longer UToku (e.g. the agent resolved it meanwhile)."""
    eskal = (await db.execute(
        select(Eskalacija).where(Eskalacija.id == escalation_id)
    )).scalar_one_or_none()
    if not eskal or eskal.status != "UToku":
        return None

    eskal.status = "Napustena"
    eskal.datum_rjesavanja = datetime.now(timezone.utc)
    eskal.napomena_rjesavanja = "Korisnik se nije vratio u razgovor"
    await _close_chat_session(db, eskal.sesija_id)

    if eskal.dodjeljeni_agent_id:
        agent_row = (await db.execute(
            select(StatusAgenta).where(StatusAgenta.agent_id == eskal.dodjeljeni_agent_id)
        )).scalar_one_or_none()
        _free_agent(agent_row)

    await db.flush()
    await db.refresh(eskal)
    return eskal


async def release_escalation(
    db: AsyncSession, escalation_id: int, agent_id: UUID
) -> Optional[Eskalacija]:
    """Owner agent releases the escalation back to the waiting queue."""
    result = await db.execute(
        select(Eskalacija).where(Eskalacija.id == escalation_id).with_for_update()
    )
    eskal = result.scalar_one_or_none()
    if not eskal or eskal.dodjeljeni_agent_id != agent_id or eskal.status != "UToku":
        return None

    eskal.status = "Cekanje"
    eskal.dodjeljeni_agent_id = None
    eskal.datum_azuriranja = datetime.now(timezone.utc)

    agent_row = (await db.execute(
        select(StatusAgenta).where(StatusAgenta.agent_id == agent_id)
    )).scalar_one_or_none()
    if agent_row:
        agent_row.status = "Online"
        agent_row.trenutna_eskalacija_id = None
        agent_row.zadnje_aktivno = datetime.now(timezone.utc)

    await db.flush()
    await db.refresh(eskal)
    return eskal


async def cancel_escalation(db: AsyncSession, korisnik_id: UUID) -> Optional[Eskalacija]:
    """Mark the user's active escalation as Napustena (user left)."""
    existing = await get_active_for_user(db, korisnik_id)
    if not existing:
        return None
    existing.status = "Napustena"
    existing.datum_rjesavanja = datetime.now(timezone.utc)
    existing.napomena_rjesavanja = "Korisnik se odjavio"

    # Free the assigned agent — same cleanup as resolve/release. Without this the
    # agent stays "Zauzet" pinned to a dead escalation after the user walks away.
    if existing.dodjeljeni_agent_id:
        agent_row = (await db.execute(
            select(StatusAgenta).where(StatusAgenta.agent_id == existing.dodjeljeni_agent_id)
        )).scalar_one_or_none()
        if agent_row:
            agent_row.status = "Online"
            agent_row.trenutna_eskalacija_id = None
            agent_row.zadnje_aktivno = datetime.now(timezone.utc)

    await db.flush()
    await db.refresh(existing)
    return existing


async def upsert_agent_status(
    db: AsyncSession, agent_id: UUID, status: str
) -> StatusAgenta:
    row = (await db.execute(
        select(StatusAgenta).where(StatusAgenta.agent_id == agent_id)
    )).scalar_one_or_none()
    now = datetime.now(timezone.utc)
    if row:
        row.status = status
        row.zadnje_aktivno = now
    else:
        row = StatusAgenta(agent_id=agent_id, status=status, zadnje_aktivno=now)
        db.add(row)
    await db.flush()
    await db.refresh(row)
    return row
