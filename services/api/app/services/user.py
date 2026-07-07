from sqlalchemy.orm import Session
from app.models.user import User, TrainerProfile, ClientProfile, UserRole
from app.schemas.user import UserCreate, TrainerProfileCreate, ClientProfileCreate
from app.core.security import hash_password


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def create_user(db: Session, user_data: UserCreate):
    hashed = hash_password(user_data.password)
    user = User(
        email=user_data.email,
        full_name=user_data.full_name,
        hashed_password=hashed,
        role=user_data.role
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def create_trainer_profile(db: Session, user_id: int, data: TrainerProfileCreate):
    profile = TrainerProfile(user_id=user_id, **data.model_dump())
    db.add(profile)
    db.commit()
    db.refresh(profile)
    return profile


def create_client_profile(db: Session, user_id: int, data: ClientProfileCreate):
    profile = ClientProfile(user_id=user_id, **data.model_dump())
    db.add(profile)
    db.commit()
    db.refresh(profile)
    return profile


def get_all_clients(db: Session):
    return db.query(ClientProfile).all()