from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.orm import relationship
import enum
from app.core.database import Base


class MuscleGroup(enum.Enum):
    chest = "chest"
    back = "back"
    legs = "legs"
    shoulders = "shoulders"
    arms = "arms"
    core = "core"
    cardio = "cardio"
    full_body = "full_body"


class ExerciseType(enum.Enum):
    strength = "strength"
    cardio = "cardio"
    stretching = "stretching"


class Exercise(Base):
    __tablename__ = "exercises"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=True)
    muscle_group = Column(Enum(MuscleGroup), nullable=False)
    exercise_type = Column(Enum(ExerciseType), nullable=False)
    photo_url = Column(String, nullable=True)
    video_url = Column(String, nullable=True)

    program_exercises = relationship(
        "ProgramExercise",
        back_populates="exercise"
    )