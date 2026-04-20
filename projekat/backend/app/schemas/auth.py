from pydantic import BaseModel, EmailStr
from uuid import UUID
from app.db.models.user import UserRole


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str | None = None
    role: UserRole = UserRole.user


class UserRead(BaseModel):
    id: UUID
    email: EmailStr
    full_name: str | None
    role: UserRole
    is_active: bool

    model_config = {"from_attributes": True}


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class LoginRequest(BaseModel):
    email: EmailStr
    password: str
