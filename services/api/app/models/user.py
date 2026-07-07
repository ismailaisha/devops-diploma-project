from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.core.database import Base
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum, ForeignKey

class UserRole(enum.Enum):
    trainer = "trainer"
    client = "client"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(Enum(UserRole), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Связи
    trainer_profile = relationship("TrainerProfile", back_populates="user", uselist=False)
    client_profile = relationship("ClientProfile", back_populates="user", uselist=False)

class TrainerProfile(Base):
    __tablename__ = "trainer_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    specialization = Column(String, nullable=True)
    experience_years = Column(Integer, default=0)
    bio = Column(String, nullable=True)
    photo_url = Column(String, nullable=True)

    user = relationship("User", back_populates="trainer_profile")
    programs = relationship("Program", back_populates="trainer")


class ClientProfile(Base):
    __tablename__ = "client_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    age = Column(Integer, nullable=True)
    weight = Column(Integer, nullable=True)
    height = Column(Integer, nullable=True)
    fitness_level = Column(String, nullable=True)
    goal = Column(String, nullable=True)

    user = relationship("User", back_populates="client_profile")
    programs = relationship("Program", back_populates="client")