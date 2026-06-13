from pydantic import BaseModel, EmailStr
from typing import Optional
from app.models.user import UserRole


class UserBase(BaseModel):
    email: EmailStr
    full_name: str


class UserCreate(UserBase):
    password: str
    role: UserRole


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None


class UserResponse(UserBase):
    id: int
    role: UserRole
    is_active: bool

    class Config:
        from_attributes = True


class TrainerProfileCreate(BaseModel):
    specialization: Optional[str] = None
    experience_years: Optional[int] = 0
    bio: Optional[str] = None


class TrainerProfileResponse(TrainerProfileCreate):
    id: int
    user_id: int
    photo_url: Optional[str] = None

    class Config:
        from_attributes = True


class ClientProfileCreate(BaseModel):
    age: Optional[int] = None
    weight: Optional[int] = None
    height: Optional[int] = None
    fitness_level: Optional[str] = None
    goal: Optional[str] = None


class ClientProfileResponse(ClientProfileCreate):
    id: int
    user_id: int

    class Config:
        from_attributes = True