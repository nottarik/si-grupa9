from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.deps import get_current_user, require_role
from app.db.models.announcement import SistemskaPoruka
from app.db.models.user import Korisnik, UlogaTip
from app.db.session import get_db
from app.schemas.announcement import AnnouncementCreate, AnnouncementUpdate

router = APIRouter(prefix="/announcements", tags=["announcements"])


def _to_dict(obj: SistemskaPoruka) -> dict:
    return {
        "id": obj.id,
        "naslov": obj.naslov,
        "tekst": obj.tekst,
        "aktivna": obj.aktivna,
        "datum_kreiranja": obj.datum_kreiranja.isoformat() if obj.datum_kreiranja else None,
        "datum_azuriranja": obj.datum_azuriranja.isoformat() if obj.datum_azuriranja else None,
        "id_administratora": str(obj.id_administratora),
    }


@router.get("/active")
async def list_active(
    db: AsyncSession = Depends(get_db),
    _: Korisnik = Depends(get_current_user),
):
    result = await db.execute(
        select(SistemskaPoruka)
        .where(SistemskaPoruka.aktivna == True)
        .order_by(SistemskaPoruka.datum_kreiranja.desc())
    )
    return [_to_dict(i) for i in result.scalars().all()]


@router.get("")
async def list_all(
    db: AsyncSession = Depends(get_db),
    _: Korisnik = Depends(require_role(UlogaTip.administrator)),
):
    result = await db.execute(
        select(SistemskaPoruka).order_by(SistemskaPoruka.datum_kreiranja.desc())
    )
    return [_to_dict(i) for i in result.scalars().all()]


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_announcement(
    body: AnnouncementCreate,
    db: AsyncSession = Depends(get_db),
    current_user: Korisnik = Depends(require_role(UlogaTip.administrator)),
):
    obj = SistemskaPoruka(
        naslov=body.naslov,
        tekst=body.tekst,
        aktivna=True,
        id_administratora=current_user.id,
    )
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return _to_dict(obj)


@router.patch("/{announcement_id}")
async def update_announcement(
    announcement_id: int,
    body: AnnouncementUpdate,
    db: AsyncSession = Depends(get_db),
    _: Korisnik = Depends(require_role(UlogaTip.administrator)),
):
    result = await db.execute(
        select(SistemskaPoruka).where(SistemskaPoruka.id == announcement_id)
    )
    obj = result.scalar_one_or_none()
    if not obj:
        raise HTTPException(status_code=404, detail="Announcement not found")

    if body.naslov is not None:
        obj.naslov = body.naslov
    if body.tekst is not None:
        obj.tekst = body.tekst
    if body.aktivna is not None:
        obj.aktivna = body.aktivna

    await db.commit()
    await db.refresh(obj)
    return _to_dict(obj)


@router.delete("/{announcement_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_announcement(
    announcement_id: int,
    db: AsyncSession = Depends(get_db),
    _: Korisnik = Depends(require_role(UlogaTip.administrator)),
):
    result = await db.execute(
        select(SistemskaPoruka).where(SistemskaPoruka.id == announcement_id)
    )
    obj = result.scalar_one_or_none()
    if not obj:
        raise HTTPException(status_code=404, detail="Announcement not found")

    await db.delete(obj)
    await db.commit()
