from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.api.auth import get_current_user
from app.schemas.exercise import ExerciseCreate, ExerciseUpdate, ExerciseResponse
from app.services.exercise import (
    create_exercise, get_all_exercises,
    get_exercise_by_id, update_exercise, delete_exercise
)

router = APIRouter()


@router.get("/", response_model=List[ExerciseResponse])
def list_exercises(db: Session = Depends(get_db)):
    return get_all_exercises(db)


@router.post("/", response_model=ExerciseResponse)
def add_exercise(
    data: ExerciseCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return create_exercise(db, data)


@router.get("/{exercise_id}", response_model=ExerciseResponse)
def get_exercise(exercise_id: int, db: Session = Depends(get_db)):
    exercise = get_exercise_by_id(db, exercise_id)
    if not exercise:
        raise HTTPException(status_code=404, detail="Упражнение не найдено")
    return exercise


@router.put("/{exercise_id}", response_model=ExerciseResponse)
def edit_exercise(
    exercise_id: int,
    data: ExerciseUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    exercise = update_exercise(db, exercise_id, data)
    if not exercise:
        raise HTTPException(status_code=404, detail="Упражнение не найдено")
    return exercise


@router.delete("/{exercise_id}")
def remove_exercise(
    exercise_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    delete_exercise(db, exercise_id)
    return {"message": "Упражнение удалено"}