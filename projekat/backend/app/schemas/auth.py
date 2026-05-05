from enum import Enum
from typing import Any
from uuid import UUID

from pydantic import BaseModel, EmailStr, model_validator

from app.db.models.user import Korisnik, UlogaTip


class UserRole(str, Enum):
    admin = "admin"
    manager = "manager"
    agent = "agent"
    user = "user"


_DB_TO_API_ROLE: dict[str, UserRole] = {
    UlogaTip.administrator.value: UserRole.admin,
    UlogaTip.supervizor.value: UserRole.manager,
    UlogaTip.call_centar_agent.value: UserRole.agent,
    UlogaTip.krajnji_korisnik.value: UserRole.user,
}

_API_TO_DB_ROLE: dict[UserRole, UlogaTip] = {v: UlogaTip(k) for k, v in _DB_TO_API_ROLE.items()}


def api_role_to_db(role: UserRole) -> str:
    return _API_TO_DB_ROLE[role].value


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    role: UserRole = UserRole.user


class UserRead(BaseModel):
    id: UUID
    email: EmailStr
    full_name: str
    role: UserRole
    is_active: bool

    model_config = {"from_attributes": True}

    @model_validator(mode="before")
    @classmethod
    def _from_orm(cls, data: Any) -> Any:
        if isinstance(data, Korisnik):
            full = data.ime if not data.prezime else f"{data.ime} {data.prezime}"
            role_value = data.uloga.value if hasattr(data.uloga, "value") else data.uloga
            return {
                "id": data.id,
                "email": data.email,
                "full_name": full,
                "role": _DB_TO_API_ROLE[role_value],
                "is_active": data.aktivan,
            }
        return data


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserRoleUpdate(BaseModel):
    role: UserRole


class LoginRequest(BaseModel):
    email: EmailStr
    password: str
