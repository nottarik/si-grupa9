import re
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.db.models.user import Korisnik
from app.api.v1.deps import get_current_user, require_admin
from app.schemas.chat import ChatRequest, ChatResponse, FeedbackRequest, SessionRateRequest, IssueBulkDelete, ChatLogBulkDelete
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
    # If this user has an active agent session *for this chat*, bypass RAG entirely.
    # Messages typed in a different/new chat are NOT hijacked into the agent chat —
    # they go to the bot, and an explicit agent request there is rejected (409).
    active = await eskal_svc.get_active_for_user(db, current_user.id)
    if active and active.status == "UToku" and active.sesija_id == payload.session_id:
        msg_payload = {
            "type": "user_message",
            "session_id": active.sesija_id,
            "content": payload.question,
            "escalation_id": active.id,
        }
        if active.dodjeljeni_agent_id:
            await manager.send_to_agent(str(active.dodjeljeni_agent_id), msg_payload)
            await manager.broadcast_to_agents(
                {**msg_payload, "type": "chat_message", "role": "user"},
                exclude_agent_id=str(active.dodjeljeni_agent_id),
            )
        else:
            await manager.broadcast_to_agents(msg_payload)
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

    trigger = (result.escalation_trigger or "NiskaPouz") if result.needs_escalation else None
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

    # A low rating or an explicit "incorrect answer" flag means the bot answered
    # but got it wrong. A confidently-wrong answer never trips escalation, so this
    # is the only way it surfaces as an Issue for admin follow-up.
    is_negative = payload.is_incorrect or (ocjena is not None and ocjena <= 2)
    if is_negative and payload.interaction_id:
        from app.db.models.knowledge import Odgovor, Anomalija

        already = (await db.execute(
            select(Anomalija.id).where(Anomalija.id_odgovora == payload.interaction_id)
        )).scalar_one_or_none()

        if already is None:
            id_poruke = (await db.execute(
                select(Odgovor.id_poruke).where(Odgovor.id == payload.interaction_id)
            )).scalar_one_or_none()

            opis = f"Negative feedback (rating={ocjena})"
            if komentar:
                opis = f"{opis}: {komentar[:200]}"
            db.add(Anomalija(
                tip="NevalidanPodatak",
                nivo_ozbiljnosti="Visoka" if payload.is_incorrect else "Niska",
                status="Otvorena",
                opis=opis,
                id_poruke=id_poruke,
                id_odgovora=payload.interaction_id,
            ))

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

    # Top rated must count BOTH per-response ratings (thumbs on an answer) and the
    # end-of-conversation session rating, otherwise it's empty when users only rate
    # the whole session. Coalesce them per Q&A, same as the chat logs.
    from sqlalchemy.orm import aliased

    SessFb = aliased(Feedback)
    session_rating_sq = (
        select(func.avg(SessFb.ocjena))
        .where(SessFb.id_sesije == Poruka.id_sesije, SessFb.ocjena.isnot(None))
        .correlate(Poruka)
        .scalar_subquery()
    )
    rating_expr = func.coalesce(func.avg(Feedback.ocjena), session_rating_sq)
    top_rows = (
        await db.execute(
            select(
                Poruka.tekst,
                Odgovor.tekst_odgovora,
                Odgovor.skor_pouzdanosti,
                Poruka.timestamp_msg,
                rating_expr.label("rating"),
            )
            .join(Odgovor, Poruka.id_odgovora == Odgovor.id)
            .outerjoin(Feedback, Feedback.id_odgovora == Odgovor.id)
            .group_by(
                Poruka.id, Poruka.id_sesije, Poruka.tekst, Poruka.timestamp_msg,
                Odgovor.tekst_odgovora, Odgovor.skor_pouzdanosti,
            )
            .having(rating_expr.isnot(None))
            .order_by(rating_expr.desc(), Poruka.timestamp_msg.desc())
            .limit(5)
        )
    ).all()
    top_rated = [
        {
            "question": row.tekst,
            "answer": row.tekst_odgovora,
            "confidence": round(float(row.skor_pouzdanosti), 2) if row.skor_pouzdanosti is not None else None,
            "rating": int(round(float(row.rating))),
            "date": row.timestamp_msg.strftime("%Y-%m-%d") if row.timestamp_msg else "",
        }
        for row in top_rows
    ]

    comment_rows = (
        await db.execute(
            select(
                Feedback.ocjena,
                Feedback.komentar,
                Feedback.timestamp,
                Feedback.id_sesije,
                Poruka.tekst.label("question"),
            )
            .outerjoin(Odgovor, Feedback.id_odgovora == Odgovor.id)
            .outerjoin(Poruka, Odgovor.id_poruke == Poruka.id)
            .where(Feedback.komentar.isnot(None), Feedback.komentar != "")
            .order_by(Feedback.timestamp.desc())
            .limit(20)
        )
    ).all()
    recent_comments = [
        {
            "comment": row.komentar,
            "rating": int(row.ocjena) if row.ocjena is not None else None,
            "date": row.timestamp.strftime("%Y-%m-%d") if row.timestamp else None,
            "question": row.question,
            "sesija_id": row.id_sesije,
        }
        for row in comment_rows
    ]

    return {
        "average_score": avg_score,
        "total_rated": total,
        "five_star_pct": five_star_pct,
        "below_three_pct": below_three_pct,
        "distribution": distribution,
        "trend": trend,
        "top_rated": top_rated,
        "recent_comments": recent_comments,
    }


# Words that, on their own, mark a message as smalltalk: greetings + "connect me to
# an agent" requests + fillers (Bosnian + English). A message made up entirely of
# these is skipped when looking for the real question.
_SMALLTALK_WORDS = {
    "zdravo", "cao", "ćao", "hej", "pozdrav", "hello", "hi", "hey", "yo",
    "dobar", "dobro", "jutro", "dan", "vece", "veče", "noc", "noć",
    "good", "morning", "afternoon", "evening", "night", "thanks", "hvala",
    "agent", "agenta", "agentom", "agentu", "operater", "operatera", "operator",
    "predstavnik", "predstavnika", "ljudski", "covjek", "čovjek", "human", "person",
    "molim", "please", "te", "vas", "bih", "bi", "da", "sa", "se", "mogu", "mogli",
    "want", "need", "trebam", "treba", "zelim", "želim", "htio", "htjela",
    "razgovarati", "razgovor", "spojite", "spoji", "prebacite", "talk", "speak", "to",
    "can", "could", "with", "i", "a", "the", "me", "for", "real", "live", "you",
}


def _is_smalltalk(text: str) -> bool:
    tokens = re.findall(r"\w+", (text or "").lower())
    if not tokens:
        return True
    return all(t in _SMALLTALK_WORDS for t in tokens)


def _extract_agent_question(razgovor: list) -> tuple[Optional[str], Optional[str]]:
    """The real question is usually asked to the agent after connecting. Return the
    first substantive user message in the escalation transcript and the agent reply
    that follows it (question, answer)."""
    msgs = [m for m in (razgovor or []) if isinstance(m, dict)]
    for i, m in enumerate(msgs):
        if m.get("role") != "user":
            continue
        content = (m.get("content") or "").strip()
        if not content or _is_smalltalk(content):
            continue
        answer = None
        for j in range(i + 1, len(msgs)):
            role = msgs[j].get("role")
            if role == "user":
                break
            if role == "agent":
                answer = (msgs[j].get("content") or "").strip() or None
                break
        return content, answer
    return None, None


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
    from sqlalchemy.orm import aliased

    # Ratings can be left per-response (Feedback.id_odgovora) or per-session
    # (Feedback.id_sesije, the end-of-conversation rating). Surface either one.
    SessFb = aliased(Feedback)
    session_rating_sq = (
        select(func.avg(SessFb.ocjena))
        .where(SessFb.id_sesije == Poruka.id_sesije, SessFb.ocjena.isnot(None))
        .correlate(Poruka)
        .scalar_subquery()
    )

    query = (
        select(
            Poruka.id,
            Poruka.id_sesije,
            Poruka.tekst,
            Poruka.timestamp_msg,
            Odgovor.tekst_odgovora,
            Odgovor.skor_pouzdanosti,
            Odgovor.metoda_generisanja,
            func.coalesce(func.avg(Feedback.ocjena), session_rating_sq).label("avg_rating"),
        )
        .join(Odgovor, Poruka.id_odgovora == Odgovor.id)
        .outerjoin(Feedback, Feedback.id_odgovora == Odgovor.id)
        .group_by(Poruka.id, Poruka.id_sesije, Poruka.tekst, Poruka.timestamp_msg, Odgovor.tekst_odgovora, Odgovor.skor_pouzdanosti, Odgovor.metoda_generisanja)
    )

    from app.services.ai.rag_service import _EXPLICIT_ESCALATION_MSG

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

    # Fetch recent turns newest-first, then fold them into ONE entry per conversation
    # so every conversation shows once. The title is the first *real* question asked —
    # greetings/smalltalk ("Generativno") and "talk to an agent" requests are skipped
    # as titles (but the conversation still appears).
    query = query.order_by(Poruka.timestamp_msg.desc()).limit(1000)
    rows = (await db.execute(query)).all()

    def _is_real(row) -> bool:
        return (
            (row.metoda_generisanja or "") != "Generativno"
            and (row.tekst_odgovora or "") != _EXPLICIT_ESCALATION_MSG
            and not _is_smalltalk(row.tekst or "")
        )

    grouped: dict = {}
    order: list = []
    for row in rows:
        key = row.id_sesije if row.id_sesije is not None else f"_msg{row.id}"
        if key not in grouped:
            grouped[key] = []
            order.append(key)
        grouped[key].append(row)

    _epoch = datetime.min.replace(tzinfo=timezone.utc)
    results = []
    for key in order:
        group = grouped[key]
        real = [r for r in group if _is_real(r)]
        rep = min(real or group, key=lambda r: r.timestamp_msg or _epoch)
        ratings = [float(r.avg_rating) for r in group if r.avg_rating is not None]
        rating = round(sum(ratings) / len(ratings), 1) if ratings else None
        if min_rating is not None and (rating is None or rating < min_rating):
            continue
        latest = max((r.timestamp_msg for r in group if r.timestamp_msg), default=rep.timestamp_msg)
        results.append({
            "id": rep.id,
            "session_id": rep.id_sesije,
            "question": rep.tekst,
            "answer": rep.tekst_odgovora,
            "time": latest.strftime("%H:%M") if latest else None,
            "date": latest.strftime("%Y-%m-%d") if latest else None,
            "confidence": round(float(rep.skor_pouzdanosti or 0), 2),
            "method": rep.metoda_generisanja,
            "rating": rating,
        })
        if len(results) >= limit:
            break

    # For escalated conversations the bot turn is often just "talk to an agent"; the
    # real question is asked to the agent. Pull it from the escalation transcript and
    # use it as the title (and the agent's reply as the answer).
    from app.db.models.escalation import Eskalacija

    session_ids = [r["session_id"] for r in results if r["session_id"] is not None]
    if session_ids:
        esk_rows = (await db.execute(
            select(Eskalacija.sesija_id, Eskalacija.razgovor)
            .where(Eskalacija.sesija_id.in_(session_ids))
            .order_by(Eskalacija.id.desc())
        )).all()
        real_by_session: dict = {}
        for sid, razgovor in esk_rows:
            if sid in real_by_session:
                continue  # keep the most recent escalation (id desc)
            q, a = _extract_agent_question(razgovor)
            if q:
                real_by_session[sid] = (q, a)
        for r in results:
            pair = real_by_session.get(r["session_id"])
            if pair:
                r["question"] = pair[0]
                if pair[1]:
                    r["answer"] = pair[1]
                    r["method"] = "Agent"

    return results


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

    return {"session_id": session_id, "is_closed": sess.status == "Zatvorena", "messages": messages}


@router.get("/admin/sessions/{session_id}/messages")
async def admin_get_session_messages(
    session_id: int,
    db: AsyncSession = Depends(get_db),
    _: Korisnik = Depends(require_admin),
):
    """Admin endpoint: get all messages for any session (no ownership check)."""
    from app.db.models.knowledge import ChatSesija, Poruka, Odgovor
    from app.db.models.escalation import Eskalacija
    from fastapi import HTTPException

    sess = (await db.execute(
        select(ChatSesija).where(ChatSesija.id == session_id)
    )).scalar_one_or_none()
    if not sess:
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
                })

    # Human-agent (escalated) chat messages live only in the escalation
    # razgovor JSON, not as Poruka rows. Merge them in so the admin sees the
    # full conversation. Dedupe by (role, content) since the razgovor snapshot
    # repeats the bot turns already captured above.
    seen = {(m["role"], m["content"]) for m in messages}
    escalations = (await db.execute(
        select(Eskalacija.razgovor)
        .where(Eskalacija.sesija_id == session_id)
        .order_by(Eskalacija.datum_kreiranja.asc())
    )).scalars().all()
    for razgovor in escalations:
        for entry in razgovor or []:
            role = entry.get("role")
            content = entry.get("content")
            if content is None or (role, content) in seen:
                continue
            seen.add((role, content))
            messages.append({"role": role, "content": content, "timestamp": None})

    return {"session_id": session_id, "messages": messages}


@router.post("/sessions/{session_id}/close")
async def close_session(
    session_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: Korisnik = Depends(get_current_user),
):
    """Mark a chat session as closed (Zatvorena)."""
    from app.db.models.knowledge import ChatSesija
    from datetime import datetime, timezone
    from fastapi import HTTPException

    sess = (await db.execute(
        select(ChatSesija).where(
            ChatSesija.id == session_id,
            ChatSesija.id_korisnika == current_user.id,
        )
    )).scalar_one_or_none()
    if not sess:
        raise HTTPException(status_code=404, detail="Session not found")
    if sess.status != "Zatvorena":
        sess.status = "Zatvorena"
        sess.datum_zavrsetka = datetime.now(timezone.utc)
        await db.commit()
    return {"ok": True}


async def _purge_session_data(db: AsyncSession, session_id: int) -> None:
    """Delete all child rows for a session (messages, answers, feedback, anomalies,
    escalations). Does NOT delete the ChatSesija row itself and does NOT commit —
    the caller owns both."""
    from app.db.models.knowledge import Poruka, Odgovor, Feedback, Anomalija
    from app.db.models.escalation import Eskalacija, StatusAgenta
    from sqlalchemy import update as sa_update, delete as sa_delete

    poruka_ids = list((await db.execute(
        select(Poruka.id).where(Poruka.id_sesije == session_id)
    )).scalars().all())

    odgovor_ids: list = []
    if poruka_ids:
        odgovor_ids = list((await db.execute(
            select(Odgovor.id).where(Odgovor.id_poruke.in_(poruka_ids))
        )).scalars().all())

    # Nullify Anomalija references before deleting
    if poruka_ids:
        await db.execute(sa_update(Anomalija).where(Anomalija.id_poruke.in_(poruka_ids)).values(id_poruke=None))
    if odgovor_ids:
        await db.execute(sa_update(Anomalija).where(Anomalija.id_odgovora.in_(odgovor_ids)).values(id_odgovora=None))
        await db.execute(sa_delete(Feedback).where(Feedback.id_odgovora.in_(odgovor_ids)))

    await db.execute(sa_delete(Feedback).where(Feedback.id_sesije == session_id))

    # Break circular FK (Poruka.id_odgovora ↔ Odgovor.id_poruke) before deleting
    if poruka_ids:
        await db.execute(sa_update(Poruka).where(Poruka.id_sesije == session_id).values(id_odgovora=None))
    if odgovor_ids:
        await db.execute(sa_delete(Odgovor).where(Odgovor.id.in_(odgovor_ids)))

    await db.execute(sa_delete(Poruka).where(Poruka.id_sesije == session_id))

    eskal_ids = list((await db.execute(
        select(Eskalacija.id).where(Eskalacija.sesija_id == session_id)
    )).scalars().all())
    if eskal_ids:
        await db.execute(sa_update(StatusAgenta).where(StatusAgenta.trenutna_eskalacija_id.in_(eskal_ids)).values(trenutna_eskalacija_id=None))
    await db.execute(sa_delete(Eskalacija).where(Eskalacija.sesija_id == session_id))


@router.delete("/sessions/{session_id}")
async def delete_session(
    session_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: Korisnik = Depends(get_current_user),
):
    from app.db.models.knowledge import ChatSesija
    from fastapi import HTTPException

    sess = (await db.execute(
        select(ChatSesija).where(
            ChatSesija.id == session_id,
            ChatSesija.id_korisnika == current_user.id,
        )
    )).scalar_one_or_none()
    if not sess:
        raise HTTPException(status_code=404, detail="Session not found")

    await _purge_session_data(db, session_id)
    await db.delete(sess)
    await db.commit()
    return {"ok": True}


@router.post("/logs/bulk-delete")
async def bulk_delete_chat_logs(
    payload: ChatLogBulkDelete,
    db: AsyncSession = Depends(get_db),
    _: Korisnik = Depends(require_admin),
):
    """Admin endpoint: delete the given chat conversations (sessions) by id, including
    all their messages, answers, feedback, anomalies and escalations."""
    from app.db.models.knowledge import ChatSesija

    if not payload.session_ids:
        return {"ok": True, "deleted": 0}

    sessions = (await db.execute(
        select(ChatSesija).where(ChatSesija.id.in_(payload.session_ids))
    )).scalars().all()

    for sess in sessions:
        await _purge_session_data(db, sess.id)
        await db.delete(sess)

    await db.commit()
    return {"ok": True, "deleted": len(sessions)}


@router.post("/sessions/{session_id}/rate")
async def rate_session(
    session_id: int,
    payload: SessionRateRequest,
    db: AsyncSession = Depends(get_db),
    current_user: Korisnik = Depends(get_current_user),
):
    """Submit an end-of-conversation rating for a session."""
    from app.db.models.knowledge import ChatSesija, Feedback
    from fastapi import HTTPException

    sess = (await db.execute(
        select(ChatSesija).where(
            ChatSesija.id == session_id,
            ChatSesija.id_korisnika == current_user.id,
        )
    )).scalar_one_or_none()
    if not sess:
        raise HTTPException(status_code=404, detail="Session not found")

    ocjena = max(1.0, min(5.0, float(payload.rating)))
    feedback = Feedback(
        id_sesije=session_id,
        id_korisnika=current_user.id,
        ocjena=ocjena,
        komentar=payload.comment or None,
        tip="KorisnikOcjena",
    )
    db.add(feedback)
    await db.commit()
    return {"ok": True}


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


@router.delete("/issues/{issue_id}")
async def delete_issue(
    issue_id: int,
    db: AsyncSession = Depends(get_db),
    _: Korisnik = Depends(require_admin),
):
    """Delete a single anomaly (issue)."""
    from app.db.models.knowledge import Anomalija

    result = await db.execute(select(Anomalija).where(Anomalija.id == issue_id))
    anomalija = result.scalar_one_or_none()
    if not anomalija:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Not found")

    await db.delete(anomalija)
    await db.commit()
    return {"ok": True}


@router.post("/issues/bulk-delete")
async def bulk_delete_issues(
    payload: IssueBulkDelete,
    db: AsyncSession = Depends(get_db),
    _: Korisnik = Depends(require_admin),
):
    """Delete the given anomalies (issues) by id."""
    from app.db.models.knowledge import Anomalija
    from sqlalchemy import delete as sa_delete

    if not payload.ids:
        return {"ok": True, "deleted": 0}

    result = await db.execute(sa_delete(Anomalija).where(Anomalija.id.in_(payload.ids)))
    await db.commit()
    return {"ok": True, "deleted": result.rowcount or 0}
