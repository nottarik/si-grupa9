from collections import defaultdict
from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.db.models.user import Korisnik
from app.api.v1.deps import get_current_user, require_admin
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
        # Persist user message to escalation history
        history = list(active.razgovor or [])
        history.append({"role": "user", "content": payload.question})
        active.razgovor = history
        await db.commit()

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


@router.get("/logs")
async def chat_logs(
    db: AsyncSession = Depends(get_db),
    _: Korisnik = Depends(require_admin),
    limit: int = Query(default=50, le=200),
    search: Optional[str] = Query(default=None),
    date: Optional[str] = Query(default=None),
    min_rating: Optional[int] = Query(default=None),
):
    """Admin endpoint: list recent chat interactions with answers and ratings."""
    from app.db.models.knowledge import Poruka, Odgovor, Feedback

    query = (
        select(
            Poruka.id,
            Poruka.tekst,
            Poruka.timestamp_msg,
            Odgovor.tekst_odgovora,
            Odgovor.skor_pouzdanosti,
            Odgovor.metoda_generisanja,
            func.avg(Feedback.ocjena).label("avg_rating"),
        )
        .join(Odgovor, Poruka.id_odgovora == Odgovor.id)
        .outerjoin(Feedback, Feedback.id_odgovora == Odgovor.id)
        .group_by(Poruka.id, Poruka.tekst, Poruka.timestamp_msg, Odgovor.tekst_odgovora, Odgovor.skor_pouzdanosti, Odgovor.metoda_generisanja)
    )

    if search:
        pattern = f"%{search}%"
        query = query.where(Poruka.tekst.ilike(pattern) | Odgovor.tekst_odgovora.ilike(pattern))

    if date:
        try:
            d = datetime.strptime(date, "%Y-%m-%d").replace(tzinfo=timezone.utc)
            query = query.where(
                Poruka.timestamp_msg >= d,
                Poruka.timestamp_msg < d + timedelta(days=1),
            )
        except ValueError:
            pass

    if min_rating is not None:
        query = query.having(func.avg(Feedback.ocjena) >= min_rating)

    query = query.order_by(Poruka.timestamp_msg.desc()).limit(limit)
    rows = (await db.execute(query)).all()

    return [
        {
            "id": row.id,
            "question": row.tekst,
            "answer": row.tekst_odgovora,
            "time": row.timestamp_msg.strftime("%H:%M") if row.timestamp_msg else None,
            "date": row.timestamp_msg.strftime("%Y-%m-%d") if row.timestamp_msg else None,
            "confidence": round(float(row.skor_pouzdanosti or 0), 2),
            "method": row.metoda_generisanja,
            "rating": round(float(row.avg_rating), 1) if row.avg_rating else None,
        }
        for row in rows
    ]


@router.get("/sessions")
async def list_sessions(
    db: AsyncSession = Depends(get_db),
    current_user: Korisnik = Depends(get_current_user),
    limit: int = Query(default=20, le=50),
):
    """List chat sessions for the current user, newest first."""
    from app.db.models.knowledge import ChatSesija, Poruka

    result = await db.execute(
        select(ChatSesija)
        .where(ChatSesija.id_korisnika == current_user.id)
        .order_by(ChatSesija.datum_pocetka.desc())
        .limit(limit)
    )
    sessions = result.scalars().all()

    items = []
    for s in sessions:
        first_msg = (await db.execute(
            select(Poruka.tekst)
            .where(Poruka.id_sesije == s.id, Poruka.tip == "KorisnickoP")
            .order_by(Poruka.timestamp_msg.asc())
            .limit(1)
        )).scalar_one_or_none()

        items.append({
            "id": s.id,
            "started_at": s.datum_pocetka.isoformat() if s.datum_pocetka else None,
            "status": s.status,
            "message_count": s.broj_poruka or 0,
            "preview": (first_msg[:80] + "…") if first_msg and len(first_msg) > 80 else first_msg,
        })

    return items


@router.get("/sessions/{session_id}/messages")
async def get_session_messages(
    session_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: Korisnik = Depends(get_current_user),
):
    """Get all messages for a specific session (must belong to current user)."""
    from app.db.models.knowledge import ChatSesija, Poruka, Odgovor

    sess = (await db.execute(
        select(ChatSesija).where(
            ChatSesija.id == session_id,
            ChatSesija.id_korisnika == current_user.id,
        )
    )).scalar_one_or_none()
    if not sess:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Session not found")

    rows = (await db.execute(
        select(Poruka)
        .where(Poruka.id_sesije == session_id)
        .order_by(Poruka.timestamp_msg.asc())
    )).scalars().all()

    messages = []
    for p in rows:
        messages.append({
            "role": "user",
            "content": p.tekst,
            "timestamp": p.timestamp_msg.isoformat() if p.timestamp_msg else None,
        })
        if p.id_odgovora:
            odg = (await db.execute(
                select(Odgovor).where(Odgovor.id == p.id_odgovora)
            )).scalar_one_or_none()
            if odg:
                messages.append({
                    "role": "assistant",
                    "content": odg.tekst_odgovora,
                    "timestamp": None,
                    "confidence_score": odg.skor_pouzdanosti,
                })

    return {"session_id": session_id, "messages": messages}


@router.get("/issues")
async def list_issues(
    db: AsyncSession = Depends(get_db),
    _: Korisnik = Depends(require_admin),
    status_filter: Optional[str] = Query(default=None),
):
    """Admin endpoint: list anomalies as issues."""
    from app.db.models.knowledge import Anomalija, Poruka

    query = select(Anomalija).order_by(Anomalija.datum_kreiranja.desc()).limit(50)
    if status_filter and status_filter != "All":
        mapped = {"Open": "Otvorena", "Resolved": "Rijesena", "Dismissed": "Ignorisana"}
        db_status = mapped.get(status_filter, status_filter)
        query = select(Anomalija).where(Anomalija.status == db_status).order_by(Anomalija.datum_kreiranja.desc()).limit(50)

    rows = (await db.execute(query)).scalars().all()

    items = []
    for a in rows:
        question_text = None
        if a.id_poruke:
            msg = (await db.execute(select(Poruka.tekst).where(Poruka.id == a.id_poruke))).scalar_one_or_none()
            question_text = msg

        status_map = {"Otvorena": "Open", "Rijesena": "Resolved", "Ignorisana": "Dismissed"}
        severity_map = {"Kriticna": "High", "Visoka": "High", "Niska": "Low"}

        items.append({
            "id": a.id,
            "title": question_text or a.opis or f"Anomaly #{a.id}",
            "severity": severity_map.get(a.nivo_ozbiljnosti, "Medium"),
            "status": status_map.get(a.status, a.status),
            "date": a.datum_kreiranja.strftime("%Y-%m-%d") if a.datum_kreiranja else None,
            "type": a.tip,
            "description": a.opis,
        })

    return items


@router.patch("/issues/{issue_id}")
async def update_issue(
    issue_id: int,
    db: AsyncSession = Depends(get_db),
    _: Korisnik = Depends(require_admin),
    status: Optional[str] = None,
    note: Optional[str] = None,
):
    """Update anomaly status or add a note."""
    from app.db.models.knowledge import Anomalija

    result = await db.execute(select(Anomalija).where(Anomalija.id == issue_id))
    anomalija = result.scalar_one_or_none()
    if not anomalija:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Not found")

    if status:
        status_map = {"Open": "Otvorena", "Resolved": "Rijesena", "Dismissed": "Ignorisana"}
        anomalija.status = status_map.get(status, anomalija.status)

    if note:
        existing = anomalija.opis or ""
        anomalija.opis = f"{existing}\n[Note] {note}".strip()

    await db.commit()
    return {"ok": True}
