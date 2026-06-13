from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.core.database import Base


class ProgramStatus(enum.Enum):
    active = "active"
    completed = "completed"
    paused = "paused"


class Program(Base):
    __tablename__ = "programs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    trainer_id = Column(Integer, ForeignKey("trainer_profiles.id"), nullable=False)
    client_id = Column(Integer, ForeignKey("client_profiles.id"), nullable=False)
    status = Column(Enum(ProgramStatus), default=ProgramStatus.active)
    duration_weeks = Column(Integer, nullable=False)
    sessions_per_week = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    trainer = relationship("TrainerProfile", back_populates="programs")
    client = relationship("ClientProfile", back_populates="programs")
    exercises = relationship("ProgramExercise", back_populates="program")
    schedules = relationship("Schedule", back_populates="program")


class ProgramExercise(Base):
    __tablename__ = "program_exercises"

    id = Column(Integer, primary_key=True, index=True)
    program_id = Column(Integer, ForeignKey("programs.id"), nullable=False)
    exercise_id = Column(Integer, ForeignKey("exercises.id"), nullable=False)
    sets = Column(Integer, nullable=False)
    reps = Column(Integer, nullable=False)
    weight_kg = Column(Integer, nullable=True)
    rest_seconds = Column(Integer, default=60)
    day_of_week = Column(Integer, nullable=False)
    notes = Column(String, nullable=True)

    program = relationship("Program", back_populates="exercises")
    exercise = relationship("Exercise", back_populates="program_exercises")