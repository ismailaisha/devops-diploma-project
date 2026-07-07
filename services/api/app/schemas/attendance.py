from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from app.models.attendance import AttendanceStatus


class AttendanceCreate(BaseModel):
    schedule_id: int
    status: AttendanceStatus
    feeling: Optional[int] = Field(None, ge=1, le=5)
    actual_weight_kg: Optional[int] = None
    actual_reps: Optional[int] = None
    notes: Optional[str] = None


class AttendanceUpdate(BaseModel):
    status: Optional[AttendanceStatus] = None
    feeling: Optional[int] = Field(None, ge=1, le=5)
    actual_weight_kg: Optional[int] = None
    actual_reps: Optional[int] = None
    notes: Optional[str] = None


class AttendanceResponse(BaseModel):
    id: int
    schedule_id: int
    client_id: int
    status: AttendanceStatus
    completed_at: Optional[datetime] = None
    feeling: Optional[int] = None
    actual_weight_kg: Optional[int] = None
    actual_reps: Optional[int] = None
    notes: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True