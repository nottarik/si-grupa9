from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.session import get_db
from app.db.models.user import Korisnik
from app.core.security import verify_password, get_password_hash, create_access_token
from app.schemas.auth import LoginRequest, Token, UserCreate, UserRead, UserNameUpdate, api_role_to_db
from app.api.v1.deps import get_current_user

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register(payload: UserCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Korisnik).where(Korisnik.email == payload.email))
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Email already registered")

    parts = payload.full_name.strip().split(" ", 1)
    user = Korisnik(
        email=payload.email,
        hashed_password=get_password_hash(payload.password),
        ime=parts[0],
        prezime=parts[1] if len(parts) > 1 else "",
        uloga=api_role_to_db(payload.role),
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


@router.post("/login", response_model=Token)
async def login(payload: LoginRequest, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Korisnik).where(Korisnik.email == payload.email))
    user = result.scalar_one_or_none()

    if not user or not user.hashed_password or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(subject=str(user.id))
    return Token(access_token=token)


@router.get("/me", response_model=UserRead)
async def me(current_user: Korisnik = Depends(get_current_user)):
    return current_user


@router.patch("/me", response_model=UserRead)
async def update_me(
    payload: UserNameUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: Korisnik = Depends(get_current_user),
):
    parts = payload.full_name.strip().split(" ", 1)
    current_user.ime = parts[0]
    current_user.prezime = parts[1] if len(parts) > 1 else ""
    await db.commit()
    await db.refresh(current_user)
    return current_user


@router.delete("/me/history")
async def delete_my_history(
    db: AsyncSession = Depends(get_db),
    current_user: Korisnik = Depends(get_current_user),
):
    from sqlalchemy import update as sa_update, delete as sa_delete
    from app.db.models.knowledge import ChatSesija, Poruka, Odgovor, Feedback, Anomalija
    from app.db.models.escalation import Eskalacija

    session_ids = list((await db.execute(
        select(ChatSesija.id).where(ChatSesija.id_korisnika == current_user.id)
    )).scalars().all())

    if session_ids:
        poruka_ids = list((await db.execute(
            select(Poruka.id).where(Poruka.id_sesije.in_(session_ids))
        )).scalars().all())

        odgovor_ids: list = []
        if poruka_ids:
            odgovor_ids = list((await db.execute(
                select(Odgovor.id).where(Odgovor.id_poruke.in_(poruka_ids))
            )).scalars().all())

        if poruka_ids:
            await db.execute(sa_update(Anomalija).where(Anomalija.id_poruke.in_(poruka_ids)).values(id_poruke=None))
        if odgovor_ids:
            await db.execute(sa_update(Anomalija).where(Anomalija.id_odgovora.in_(odgovor_ids)).values(id_odgovora=None))
            await db.execute(sa_delete(Feedback).where(Feedback.id_odgovora.in_(odgovor_ids)))

        await db.execute(sa_delete(Feedback).where(Feedback.id_sesije.in_(session_ids)))
        await db.execute(sa_delete(Eskalacija).where(Eskalacija.sesija_id.in_(session_ids)))

        if poruka_ids:
            await db.execute(sa_update(Poruka).where(Poruka.id_sesije.in_(session_ids)).values(id_odgovora=None))
        if odgovor_ids:
            await db.execute(sa_delete(Odgovor).where(Odgovor.id.in_(odgovor_ids)))

        await db.execute(sa_delete(Poruka).where(Poruka.id_sesije.in_(session_ids)))
        await db.execute(sa_delete(ChatSesija).where(ChatSesija.id_korisnika == current_user.id))

    await db.commit()
    return {"ok": True}


@router.delete("/me")
async def delete_my_account(
    db: AsyncSession = Depends(get_db),
    current_user: Korisnik = Depends(get_current_user),
):
    from sqlalchemy import update as sa_update, delete as sa_delete
    from app.db.models.knowledge import ChatSesija, Poruka, Odgovor, Feedback, Anomalija
    from app.db.models.escalation import Eskalacija

    session_ids = list((await db.execute(
        select(ChatSesija.id).where(ChatSesija.id_korisnika == current_user.id)
    )).scalars().all())

    if session_ids:
        poruka_ids = list((await db.execute(
            select(Poruka.id).where(Poruka.id_sesije.in_(session_ids))
        )).scalars().all())

        odgovor_ids: list = []
        if poruka_ids:
            odgovor_ids = list((await db.execute(
                select(Odgovor.id).where(Odgovor.id_poruke.in_(poruka_ids))
            )).scalars().all())

        if poruka_ids:
            await db.execute(sa_update(Anomalija).where(Anomalija.id_poruke.in_(poruka_ids)).values(id_poruke=None))
        if odgovor_ids:
            await db.execute(sa_update(Anomalija).where(Anomalija.id_odgovora.in_(odgovor_ids)).values(id_odgovora=None))
            await db.execute(sa_delete(Feedback).where(Feedback.id_odgovora.in_(odgovor_ids)))

        await db.execute(sa_delete(Feedback).where(Feedback.id_sesije.in_(session_ids)))
        await db.execute(sa_delete(Eskalacija).where(Eskalacija.sesija_id.in_(session_ids)))

        if poruka_ids:
            await db.execute(sa_update(Poruka).where(Poruka.id_sesije.in_(session_ids)).values(id_odgovora=None))
        if odgovor_ids:
            await db.execute(sa_delete(Odgovor).where(Odgovor.id.in_(odgovor_ids)))

        await db.execute(sa_delete(Poruka).where(Poruka.id_sesije.in_(session_ids)))
        await db.execute(sa_delete(ChatSesija).where(ChatSesija.id_korisnika == current_user.id))

    # Nullify agent assignments held by this user, remove remaining feedback
    await db.execute(sa_update(Eskalacija).where(Eskalacija.dodjeljeni_agent_id == current_user.id).values(dodjeljeni_agent_id=None))
    await db.execute(sa_delete(Feedback).where(Feedback.id_korisnika == current_user.id))

    await db.delete(current_user)
    await db.commit()
    return {"ok": True}
