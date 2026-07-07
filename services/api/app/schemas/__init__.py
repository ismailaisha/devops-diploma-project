from app.schemas.token import Token, TokenData
from app.schemas.user import (
    UserCreate, UserUpdate, UserResponse,
    TrainerProfileCreate, TrainerProfileResponse,
    ClientProfileCreate, ClientProfileResponse
)
from app.schemas.exercise import (
    ExerciseCreate, ExerciseUpdate, ExerciseResponse
)
from app.schemas.program import (
    ProgramCreate, ProgramUpdate, ProgramResponse,
    ProgramExerciseCreate, ProgramExerciseResponse
)
from app.schemas.schedule import (
    ScheduleCreate, ScheduleUpdate, ScheduleResponse
)
from app.schemas.attendance import (
    AttendanceCreate, AttendanceUpdate, AttendanceResponse
)