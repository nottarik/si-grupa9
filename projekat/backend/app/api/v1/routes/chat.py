from collections import defaultdict
from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.db.models.user import Korisnik
from app.api.v1.deps import get_current_user
from app.schemas.chat import ChatRequest, ChatResponse, FeedbackRequest
from app.schemas.escalation import EscalationInfo
from app.services.ai.rag_service import RagService
from app.services.escalation import service as eskal_svc
from app.services.ws.connection_manager import manager

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("/ask", response_model=ChatResponse)
async def ask(
    payload: ChatRequest,
    db: AsyncSession = Depends(get_db),
    current_user: Korisnik = Depends(get_current_user),
):
    # If this user has an active agent session, bypass RAG entirely
    active = await eskal_svc.get_active_for_user(db, current_user.id)
    if active and active.status == "UToku":
        await manager.broadcast_to_agents({
            "type": "user_message",
            "session_id": active.sesija_id,
            "content": payload.question,
            "escalation_id": active.id,
        })
        return ChatResponse(
            session_id=payload.session_id or active.sesija_id,
            escalation=EscalationInfo(
                escalation_id=active.id,
                status=active.status,
                queue_position=0,
                trigger_tip=active.trigger_tip or "NiskaPouz",
            ),
            is_agent_chat=True,
        )

    rag = RagService(db)
    history = [{"role": m.role, "content": m.content} for m in payload.history]
    result = await rag.answer(
        question=payload.question,
        user_id=current_user.id,
        history=history,
        session_id=payload.session_id,
    )

    trigger = "NiskaPouz" if result.needs_escalation else None
    if trigger:
        conversation_snapshot = history + [
            {"role": "user", "content": payload.question},
            {"role": "assistant", "content": result.answer},
        ]
        eskal = await eskal_svc.create_escalation(
            db,
            sesija_id=result.session_id,
            korisnik_id=current_user.id,
            trigger=trigger,
            razgovor=conversation_snapshot,
        )
        pos = await eskal_svc.queue_position(db, eskal.id)
        await db.commit()

        queue = await eskal_svc.get_queue(db)
        await manager.broadcast_to_agents({
            "type": "queue_update",
            "data": [
                {
                    "id": e.id,
                    "sesija_id": e.sesija_id,
                    "korisnik_id": str(e.korisnik_id),
                    "prioritet": e.prioritet,
                    "status": e.status,
                    "trigger_tip": e.trigger_tip,
                    "datum_kreiranja": e.datum_kreiranja.isoformat() if e.datum_kreiranja else None,
                    "razgovor": e.razgovor or [],
                    "queue_position": i + 1,
                }
                for i, e in enumerate(queue)
            ],
        })

        result.escalation = EscalationInfo(
            escalation_id=eskal.id,
            status=eskal.status,
            queue_position=pos,
            trigger_tip=trigger,
        )

    return result


@router.post("/feedback")
async def submit_feedback(
    payload: FeedbackRequest,
    db: AsyncSession = Depends(get_db),
    current_user: Korisnik = Depends(get_current_user),
):
    from app.db.models.knowledge import Feedback

    ocjena: float | None = payload.rating
    if ocjena is None and payload.is_positive is not None:
        ocjena = 5.0 if payload.is_positive else 1.0

    komentar = payload.comment or ""
    if payload.is_incorrect:
        komentar = f"[Netačan odgovor] {komentar}".strip()

    feedback = Feedback(
        id_odgovora=payload.interaction_id,
        id_korisnika=current_user.id,
        ocjena=ocjena,
        komentar=komentar or None,
        tip="KorisnikOcjena",
    )
    db.add(feedback)
    await db.commit()
    return {"message": "Feedback saved"}


@router.get("/ratings")
async def ratings_stats(
    db: AsyncSession = Depends(get_db),
    _: Korisnik = Depends(get_current_user),
):
    from app.db.models.knowledge import Feedback, Odgovor, Poruka

    rated = Feedback.ocjena.isnot(None)

    total = (await db.execute(select(func.count(Feedback.id)).where(rated))).scalar() or 0
    avg_raw = (await db.execute(select(func.avg(Feedback.ocjena)).where(rated))).scalar()
    avg_score = round(float(avg_raw or 0), 2)

    five_star = (
        await db.execute(select(func.count(Feedback.id)).where(rated, Feedback.ocjena >= 5))
    ).scalar() or 0
    below_three = (
        await db.execute(select(func.count(Feedback.id)).where(rated, Feedback.ocjena < 3))
    ).scalar() or 0

    five_star_pct = round(five_star / total * 100, 1) if total else 0.0
    below_three_pct = round(below_three / total * 100, 1) if total else 0.0

    all_ocjena = (await db.execute(select(Feedback.ocjena).where(rated))).scalars().all()
    dist_counts: dict[int, int] = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
    for val in all_ocjena:
        star = min(5, max(1, round(float(val))))
        dist_counts[star] += 1
    distribution = {
        str(star): round(count / total * 100, 1) if total else 0.0
        for star, count in dist_counts.items()
    }

    since = datetime.now(timezone.utc) - timedelta(days=14)
    recent_rows = (
        await db.execute(
            select(Feedback.timestamp, Feedback.ocjena)
            .where(rated, Feedback.timestamp >= since)
            .order_by(Feedback.timestamp)
        )
    ).all()
    day_scores: dict[str, list[float]] = defaultdict(list)
    for row in recent_rows:
        if row.timestamp:
            day_scores[row.timestamp.strftime("%Y-%m-%d")].append(float(row.ocjena))
    trend = [
        {"date": day, "avg": round(sum(scores) / len(scores), 2)}
        for day, scores in sorted(day_scores.items())
    ]

    top_rows = (
        await db.execute(
            select(Poruka.tekst, Feedback.ocjena, Feedback.timestamp)
            .join(Odgovor, Feedback.id_odgovora == Odgovor.id)
            .join(Poruka, Odgovor.id_poruke == Poruka.id)
            .where(rated)
            .order_by(Feedback.ocjena.desc(), Feedback.timestamp.desc())
            .limit(10)
        )
    ).all()
    top_rated = [
        {
            "question": row.tekst,
            "rating": int(row.ocjena),
            "date": row.timestamp.strftime("%Y-%m-%d") if row.timestamp else "",
        }
        for row in top_rows
    ]

    return {
        "average_score": avg_score,
        "total_rated": total,
        "five_star_pct": five_star_pct,
        "below_three_pct": below_three_pct,
        "distribution": distribution,
        "trend": trend,
        "top_rated": top_rated,
    }
