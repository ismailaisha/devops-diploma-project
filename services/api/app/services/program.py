from sqlalchemy.orm import Session
from app.models.program import Program, ProgramExercise
from app.schemas.program import ProgramCreate, ProgramUpdate


def create_program(db: Session, data: ProgramCreate, trainer_id: int):
    exercises = data.exercises or []
    program = Program(
        title=data.title,
        description=data.description,
        trainer_id=trainer_id,
        client_id=data.client_id,
        duration_weeks=data.duration_weeks,
        sessions_per_week=data.sessions_per_week
    )
    db.add(program)
    db.commit()
    db.refresh(program)
    for ex in exercises:
        program_exercise = ProgramExercise(
            program_id=program.id,
            **ex.model_dump()
        )
        db.add(program_exercise)
    db.commit()
    db.refresh(program)
    return program


def get_programs_by_trainer(db: Session, trainer_id: int):
    return db.query(Program).filter(Program.trainer_id == trainer_id).all()


def get_programs_by_client(db: Session, client_id: int):
    return db.query(Program).filter(Program.client_id == client_id).all()


def get_program_by_id(db: Session, program_id: int):
    return db.query(Program).filter(Program.id == program_id).first()


def update_program(db: Session, program_id: int, data: ProgramUpdate):
    program = get_program_by_id(db, program_id)
    if not program:
        return None
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(program, key, value)
    db.commit()
    db.refresh(program)
    return program