from datetime import datetime

from pydantic import BaseModel, Field

from app.models.attendance import AttendanceStatus


class AttendanceCreate(BaseModel):
    schedule_id: int
    status: AttendanceStatus
    feeling: int | None = Field(None, ge=1, le=5)
    actual_weight_kg: int | None = None
    actual_reps: int | None = None
    notes: str | None = None


class AttendanceUpdate(BaseModel):
    status: AttendanceStatus | None = None
    feeling: int | None = Field(None, ge=1, le=5)
    actual_weight_kg: int | None = None
    actual_reps: int | None = None
    notes: str | None = None


class AttendanceResponse(BaseModel):
    id: int
    schedule_id: int
    client_id: int
    status: AttendanceStatus
    completed_at: datetime | None = None
    feeling: int | None = None
    actual_weight_kg: int | None = None
    actual_reps: int | None = None
    notes: str | None = None
    created_at: datetime

    class Config:
        from_attributes = True