import uuid

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.security import decode_token
from app.db.session import get_db
from app.db.models.user import Korisnik, UlogaTip

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
) -> Korisnik:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_token(token)
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    result = await db.execute(select(Korisnik).where(Korisnik.id == uuid.UUID(user_id)))
    user = result.scalar_one_or_none()
    if user is None or not user.aktivan:
        raise credentials_exception
    return user


def require_role(*roles: UlogaTip):
    async def role_checker(current_user: Korisnik = Depends(get_current_user)) -> Korisnik:
        if current_user.uloga not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions",
            )
        return current_user
    return role_checker


require_admin = require_role(UlogaTip.administrator)
require_admin_or_agent = require_role(UlogaTip.administrator, UlogaTip.call_centar_agent)
