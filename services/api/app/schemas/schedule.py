from datetime import datetime

from pydantic import BaseModel

from app.models.schedule import ScheduleStatus


class ScheduleCreate(BaseModel):
    program_id: int
    client_id: int
    scheduled_at: datetime
    duration_minutes: int | None = 60
    notes: str | None = None


class ScheduleUpdate(BaseModel):
    scheduled_at: datetime | None = None
    duration_minutes: int | None = None
    status: ScheduleStatus | None = None
    notes: str | None = None


class ScheduleResponse(BaseModel):
    id: int
    program_id: int
    trainer_id: int
    client_id: int
    scheduled_at: datetime
    duration_minutes: int
    status: ScheduleStatus
    notes: str | None = None
    created_at: datetime

    class Config:
        from_attributes = True