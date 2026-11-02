
from pydantic import BaseModel

from app.models.program import ProgramStatus


class ProgramExerciseCreate(BaseModel):
    exercise_id: int
    sets: int
    reps: int
    weight_kg: int | None = None
    rest_seconds: int | None = 60
    day_of_week: int
    notes: str | None = None


class ProgramExerciseResponse(ProgramExerciseCreate):
    id: int
    program_id: int

    class Config:
        from_attributes = True


class ProgramCreate(BaseModel):
    title: str
    description: str | None = None
    client_id: int
    duration_weeks: int
    sessions_per_week: int
    exercises: list[ProgramExerciseCreate] | None = []


class ProgramUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    status: ProgramStatus | None = None
    duration_weeks: int | None = None
    sessions_per_week: int | None = None


class ProgramResponse(BaseModel):
    id: int
    title: str
    description: str | None = None
    trainer_id: int
    client_id: int
    status: ProgramStatus
    duration_weeks: int
    sessions_per_week: int
    exercises: list[ProgramExerciseResponse] | None = []

    class Config:
        from_attributes = True