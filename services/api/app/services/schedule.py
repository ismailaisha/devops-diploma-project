from sqlalchemy.orm import Session
from app.models.schedule import Schedule
from app.schemas.schedule import ScheduleCreate, ScheduleUpdate


def create_schedule(db: Session, data: ScheduleCreate, trainer_id: int):
    schedule = Schedule(trainer_id=trainer_id, **data.model_dump())
    db.add(schedule)
    db.commit()
    db.refresh(schedule)
    return schedule


def get_schedules_by_trainer(db: Session, trainer_id: int):
    return db.query(Schedule).filter(Schedule.trainer_id == trainer_id).all()


def get_schedules_by_client(db: Session, client_id: int):
    return db.query(Schedule).filter(Schedule.client_id == client_id).all()


def get_schedule_by_id(db: Session, schedule_id: int):
    return db.query(Schedule).filter(Schedule.id == schedule_id).first()


def update_schedule(db: Session, schedule_id: int, data: ScheduleUpdate):
    schedule = get_schedule_by_id(db, schedule_id)
    if not schedule:
        return None
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(schedule, key, value)
    db.commit()
    db.refresh(schedule)
    return schedule