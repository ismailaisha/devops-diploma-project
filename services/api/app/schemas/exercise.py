
from pydantic import BaseModel

from app.models.exercise import ExerciseType, MuscleGroup


class ExerciseCreate(BaseModel):
    name: str
    description: str | None = None
    muscle_group: MuscleGroup
    exercise_type: ExerciseType
    photo_url: str | None = None
    video_url: str | None = None


class ExerciseUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    muscle_group: MuscleGroup | None = None
    exercise_type: ExerciseType | None = None
    photo_url: str | None = None
    video_url: str | None = None


class ExerciseResponse(ExerciseCreate):
    id: int

    class Config:
        from_attributes = True