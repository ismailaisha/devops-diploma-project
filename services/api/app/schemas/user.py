
from pydantic import BaseModel, EmailStr

from app.models.user import UserRole


class UserBase(BaseModel):
    email: EmailStr
    full_name: str


class UserCreate(UserBase):
    password: str
    role: UserRole


class UserUpdate(BaseModel):
    full_name: str | None = None
    email: EmailStr | None = None


class UserResponse(UserBase):
    id: int
    role: UserRole
    is_active: bool

    class Config:
        from_attributes = True


class TrainerProfileCreate(BaseModel):
    specialization: str | None = None
    experience_years: int | None = 0
    bio: str | None = None


class TrainerProfileResponse(TrainerProfileCreate):
    id: int
    user_id: int
    photo_url: str | None = None

    class Config:
        from_attributes = True


class ClientProfileCreate(BaseModel):
    age: int | None = None
    weight: int | None = None
    height: int | None = None
    fitness_level: str | None = None
    goal: str | None = None


class ClientProfileResponse(ClientProfileCreate):
    id: int
    user_id: int

    class Config:
        from_attributes = True