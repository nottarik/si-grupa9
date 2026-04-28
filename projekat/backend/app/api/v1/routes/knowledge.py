from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.session import get_db
from app.db.models.user import Korisnik, UlogaTip
from app.db.models.knowledge import UnosBazeZnanja
from app.api.v1.deps import require_role

router = APIRouter(prefix="/knowledge", tags=["knowledge"])


@router.get("/pending", response_model=list[dict])
async def list_pending(
    db: AsyncSession = Depends(get_db),
    current_user: Korisnik = Depends(require_role(UlogaTip.administrator)),
):
    result = await db.execute(
        select(UnosBazeZnanja).where(UnosBazeZnanja.status_aprovacije == "NaCekanju")
    )
    items = result.scalars().all()
    return [
        {
            "id": i.id,
            "pitanje": i.pitanje,
            "odgovor": i.odgovor,
            "id_kategorije": i.id_kategorije,
        }
        for i in items
    ]


@router.post("/{item_id}/approve")
async def approve_item(
    item_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: Korisnik = Depends(require_role(UlogaTip.administrator)),
):
    result = await db.execute(select(UnosBazeZnanja).where(UnosBazeZnanja.id == item_id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    item.status_aprovacije = "Odobren"
    item.aktivan = True
    await db.commit()
    return {"message": "Item approved"}


@router.post("/{item_id}/reject")
async def reject_item(
    item_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: Korisnik = Depends(require_role(UlogaTip.administrator)),
):
    result = await db.execute(select(UnosBazeZnanja).where(UnosBazeZnanja.id == item_id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    item.status_aprovacije = "Odbijen"
    item.aktivan = False
    await db.commit()
    return {"message": "Item rejected"}
