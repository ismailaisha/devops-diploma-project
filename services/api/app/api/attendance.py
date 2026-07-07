from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.api.auth import get_current_user
from app.schemas.attendance import AttendanceCreate, AttendanceUpdate, AttendanceResponse
from app.services.attendance import (
    create_attendance, get_attendance_by_client,
    get_attendance_by_schedule, update_attendance
)

router = APIRouter()


@router.post("/", response_model=AttendanceResponse)
def add_attendance(
    data: AttendanceCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return create_attendance(db, data, client_id=current_user.id)


@router.get("/my", response_model=List[AttendanceResponse])
def my_attendance(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return get_attendance_by_client(db, current_user.id)


@router.get("/schedule/{schedule_id}", response_model=AttendanceResponse)
def get_by_schedule(schedule_id: int, db: Session = Depends(get_db)):
    attendance = get_attendance_by_schedule(db, schedule_id)
    if not attendance:
        raise HTTPException(status_code=404, detail="Посещаемость не найдена")
    return attendance


@router.put("/{attendance_id}", response_model=AttendanceResponse)
def edit_attendance(
    attendance_id: int,
    data: AttendanceUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    attendance = update_attendance(db, attendance_id, data)
    if not attendance:
        raise HTTPException(status_code=404, detail="Посещаемость не найдена")
    return attendance