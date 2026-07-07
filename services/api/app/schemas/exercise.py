from pydantic import BaseModel
from typing import Optional
from app.models.exercise import MuscleGroup, ExerciseType


class ExerciseCreate(BaseModel):
    name: str
    description: Optional[str] = None
    muscle_group: MuscleGroup
    exercise_type: ExerciseType
    photo_url: Optional[str] = None
    video_url: Optional[str] = None


class ExerciseUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    muscle_group: Optional[MuscleGroup] = None
    exercise_type: Optional[ExerciseType] = None
    photo_url: Optional[str] = None
    video_url: Optional[str] = None


class ExerciseResponse(ExerciseCreate):
    id: int

    class Config:
        from_attributes = True