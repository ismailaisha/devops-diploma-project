from sqlalchemy.orm import Session
from app.models.exercise import Exercise
from app.schemas.exercise import ExerciseCreate, ExerciseUpdate


def create_exercise(db: Session, data: ExerciseCreate):
    exercise = Exercise(**data.model_dump())
    db.add(exercise)
    db.commit()
    db.refresh(exercise)
    return exercise


def get_all_exercises(db: Session):
    return db.query(Exercise).all()


def get_exercise_by_id(db: Session, exercise_id: int):
    return db.query(Exercise).filter(Exercise.id == exercise_id).first()


def update_exercise(db: Session, exercise_id: int, data: ExerciseUpdate):
    exercise = get_exercise_by_id(db, exercise_id)
    if not exercise:
        return None
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(exercise, key, value)
    db.commit()
    db.refresh(exercise)
    return exercise


def delete_exercise(db: Session, exercise_id: int):
    exercise = get_exercise_by_id(db, exercise_id)
    if exercise:
        db.delete(exercise)
        db.commit()
    return exercise