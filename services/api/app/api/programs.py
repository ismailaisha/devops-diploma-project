from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.api.auth import get_current_user
from app.schemas.program import ProgramCreate, ProgramUpdate, ProgramResponse
from app.services.program import (
    create_program, get_programs_by_trainer,
    get_programs_by_client, get_program_by_id, update_program
)

router = APIRouter()


@router.post("/", response_model=ProgramResponse)
def add_program(
    data: ProgramCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return create_program(db, data, trainer_id=current_user.id)


@router.get("/my", response_model=List[ProgramResponse])
def my_programs(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    if current_user.role.value == "trainer":
        return get_programs_by_trainer(db, current_user.id)
    return get_programs_by_client(db, current_user.id)


@router.get("/{program_id}", response_model=ProgramResponse)
def get_program(program_id: int, db: Session = Depends(get_db)):
    program = get_program_by_id(db, program_id)
    if not program:
        raise HTTPException(status_code=404, detail="Программа не найдена")
    return program


@router.put("/{program_id}", response_model=ProgramResponse)
def edit_program(
    program_id: int,
    data: ProgramUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    program = update_program(db, program_id, data)
    if not program:
        raise HTTPException(status_code=404, detail="Программа не найдена")
    return program