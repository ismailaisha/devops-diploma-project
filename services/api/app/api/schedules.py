from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.auth import get_current_user
from app.core.database import get_db
from app.schemas.schedule import ScheduleCreate, ScheduleResponse, ScheduleUpdate
from app.services.schedule import (
    create_schedule,
    get_schedule_by_id,
    get_schedules_by_client,
    get_schedules_by_trainer,
    update_schedule,
)

router = APIRouter()


@router.post("/", response_model=ScheduleResponse)
def add_schedule(
    data: ScheduleCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return create_schedule(db, data, trainer_id=current_user.id)


@router.get("/my", response_model=list[ScheduleResponse])
def my_schedules(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    if current_user.role.value == "trainer":
        return get_schedules_by_trainer(db, current_user.id)
    return get_schedules_by_client(db, current_user.id)


@router.get("/{schedule_id}", response_model=ScheduleResponse)
def get_schedule(schedule_id: int, db: Session = Depends(get_db)):
    schedule = get_schedule_by_id(db, schedule_id)
    if not schedule:
        raise HTTPException(status_code=404, detail="Расписание не найдено")
    return schedule


@router.put("/{schedule_id}", response_model=ScheduleResponse)
def edit_schedule(
    schedule_id: int,
    data: ScheduleUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    schedule = update_schedule(db, schedule_id, data)
    if not schedule:
        raise HTTPException(status_code=404, detail="Расписание не найдено")
    return schedule