from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.deps import require_role
from app.db.models.user import Korisnik, UlogaTip
from app.db.session import get_db
from app.schemas.auth import UserRead, UserRoleUpdate, api_role_to_db

router = APIRouter(prefix="/users", tags=["users"])


@router.get("", response_model=list[UserRead])
async def list_users(
    db: AsyncSession = Depends(get_db),
    current_user: Korisnik = Depends(require_role(UlogaTip.administrator)),
):
    result = await db.execute(select(Korisnik).order_by(Korisnik.datum_kreiranja.desc()))
    return result.scalars().all()


@router.patch("/{user_id}/role", response_model=UserRead)
async def update_user_role(
    user_id: UUID,
    payload: UserRoleUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: Korisnik = Depends(require_role(UlogaTip.administrator)),
):
    result = await db.execute(select(Korisnik).where(Korisnik.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.uloga = api_role_to_db(payload.role)
    await db.commit()
    await db.refresh(user)
    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: Korisnik = Depends(require_role(UlogaTip.administrator)),
):
    if user_id == current_user.id:
        raise HTTPException(status_code=400, detail="Cannot delete your own account")

    result = await db.execute(select(Korisnik).where(Korisnik.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    await db.delete(user)
    await db.commit()
