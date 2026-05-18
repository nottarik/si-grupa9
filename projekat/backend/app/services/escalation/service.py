import re
from datetime import datetime, timezone
from typing import List, Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.db.models.escalation import Eskalacija, StatusAgenta
from app.db.models.knowledge import UnosBazeZnanja

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
    pitanje: Optional[str] = None,
    odgovor: Optional[str] = None,
) -> Optional[Eskalacija]:
    result = await db.execute(select(Eskalacija).where(Eskalacija.id == escalation_id))
    eskal = result.scalar_one_or_none()
    if not eskal:
        return None

    eskal.status = "Rijesena"
    eskal.datum_rjesavanja = datetime.now(timezone.utc)
    eskal.napomena_rjesavanja = napomena

    agent_row = (await db.execute(
        select(StatusAgenta).where(StatusAgenta.agent_id == agent_id)
    )).scalar_one_or_none()
    if agent_row:
        agent_row.status = "Online"
        agent_row.trenutna_eskalacija_id = None
        agent_row.zadnje_aktivno = datetime.now(timezone.utc)

    if submit_to_kb and pitanje and odgovor:
        db.add(UnosBazeZnanja(
            pitanje=pitanje,
            odgovor=odgovor,
            status_aprovacije="NaCekanju",
            aktivan=True,
            verzija_broj=1,
        ))

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
