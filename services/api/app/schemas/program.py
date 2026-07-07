from pydantic import BaseModel
from typing import Optional, List
from app.models.program import ProgramStatus


class ProgramExerciseCreate(BaseModel):
    exercise_id: int
    sets: int
    reps: int
    weight_kg: Optional[int] = None
    rest_seconds: Optional[int] = 60
    day_of_week: int
    notes: Optional[str] = None


class ProgramExerciseResponse(ProgramExerciseCreate):
    id: int
    program_id: int

    class Config:
        from_attributes = True


class ProgramCreate(BaseModel):
    title: str
    description: Optional[str] = None
    client_id: int
    duration_weeks: int
    sessions_per_week: int
    exercises: Optional[List[ProgramExerciseCreate]] = []


class ProgramUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[ProgramStatus] = None
    duration_weeks: Optional[int] = None
    sessions_per_week: Optional[int] = None


class ProgramResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    trainer_id: int
    client_id: int
    status: ProgramStatus
    duration_weeks: int
    sessions_per_week: int
    exercises: Optional[List[ProgramExerciseResponse]] = []

    class Config:
        from_attributes = True