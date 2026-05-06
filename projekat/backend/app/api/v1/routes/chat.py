from collections import defaultdict
from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.db.models.user import Korisnik
from app.api.v1.deps import get_current_user
from app.schemas.chat import ChatRequest, ChatResponse, FeedbackRequest
from app.services.ai.rag_service import RagService

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("/ask", response_model=ChatResponse)
async def ask(
    payload: ChatRequest,
    db: AsyncSession = Depends(get_db),
    current_user: Korisnik = Depends(get_current_user),
):
    rag = RagService(db)
    result = await rag.answer(question=payload.question, user_id=current_user.id)
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

    # Distribution: fetch all ocjena values and bucket in Python
    all_ocjena = (await db.execute(select(Feedback.ocjena).where(rated))).scalars().all()
    dist_counts: dict[int, int] = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
    for val in all_ocjena:
        star = min(5, max(1, round(float(val))))
        dist_counts[star] += 1
    distribution = {
        str(star): round(count / total * 100, 1) if total else 0.0
        for star, count in dist_counts.items()
    }

    # Trend: fetch raw rows and group by date in Python (avoids cast/Date dialect issues)
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

    # Top rated — join to user question Poruka
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
