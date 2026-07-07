from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.models.schedule import ScheduleStatus


class ScheduleCreate(BaseModel):
    program_id: int
    client_id: int
    scheduled_at: datetime
    duration_minutes: Optional[int] = 60
    notes: Optional[str] = None


class ScheduleUpdate(BaseModel):
    scheduled_at: Optional[datetime] = None
    duration_minutes: Optional[int] = None
    status: Optional[ScheduleStatus] = None
    notes: Optional[str] = None


class ScheduleResponse(BaseModel):
    id: int
    program_id: int
    trainer_id: int
    client_id: int
    scheduled_at: datetime
    duration_minutes: int
    status: ScheduleStatus
    notes: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True