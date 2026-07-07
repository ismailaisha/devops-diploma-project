from sqlalchemy.orm import Session
from datetime import datetime, timezone
from app.models.attendance import Attendance, AttendanceStatus
from app.schemas.attendance import AttendanceCreate, AttendanceUpdate


def create_attendance(db: Session, data: AttendanceCreate, client_id: int):
    attendance = Attendance(client_id=client_id, **data.model_dump())
    if data.status == AttendanceStatus.completed:
        attendance.completed_at = datetime.now(timezone.utc)
    db.add(attendance)
    db.commit()
    db.refresh(attendance)
    return attendance


def get_attendance_by_client(db: Session, client_id: int):
    return db.query(Attendance).filter(Attendance.client_id == client_id).all()


def get_attendance_by_schedule(db: Session, schedule_id: int):
    return db.query(Attendance).filter(Attendance.schedule_id == schedule_id).first()


def update_attendance(db: Session, attendance_id: int, data: AttendanceUpdate):
    attendance = db.query(Attendance).filter(Attendance.id == attendance_id).first()
    if not attendance:
        return None
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(attendance, key, value)
    if data.status == AttendanceStatus.completed:
        attendance.completed_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(attendance)
    return attendance