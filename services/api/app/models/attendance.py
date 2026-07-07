from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.core.database import Base


class AttendanceStatus(enum.Enum):
    completed = "completed"
    missed = "missed"
    cancelled = "cancelled"


class Attendance(Base):
    __tablename__ = "attendance"

    id = Column(Integer, primary_key=True, index=True)
    schedule_id = Column(Integer, ForeignKey("schedules.id"), nullable=False)
    client_id = Column(Integer, ForeignKey("client_profiles.id"), nullable=False)
    status = Column(Enum(AttendanceStatus), nullable=False)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    feeling = Column(Integer, nullable=True)
    actual_weight_kg = Column(Integer, nullable=True)
    actual_reps = Column(Integer, nullable=True)
    notes = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    schedule = relationship("Schedule", back_populates="attendance")
    client = relationship("ClientProfile")