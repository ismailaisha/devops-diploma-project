from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.core.database import Base


class ScheduleStatus(enum.Enum):
    scheduled = "scheduled"
    completed = "completed"
    cancelled = "cancelled"
    missed = "missed"


class Schedule(Base):
    __tablename__ = "schedules"

    id = Column(Integer, primary_key=True, index=True)
    program_id = Column(Integer, ForeignKey("programs.id"), nullable=False)
    trainer_id = Column(Integer, ForeignKey("trainer_profiles.id"), nullable=False)
    client_id = Column(Integer, ForeignKey("client_profiles.id"), nullable=False)
    scheduled_at = Column(DateTime(timezone=True), nullable=False)
    duration_minutes = Column(Integer, default=60)
    status = Column(Enum(ScheduleStatus), default=ScheduleStatus.scheduled)
    notes = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    program = relationship("Program", back_populates="schedules")
    trainer = relationship("TrainerProfile")
    client = relationship("ClientProfile")
    attendance = relationship("Attendance", back_populates="schedule")