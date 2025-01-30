from http.client import HTTPException
from sqlalchemy.orm import Session
from app.models.user_model import User as UserModel
from app.schemas.user_schema import UserCreate, UserUpdate
from app.core.security import get_password_hash


def create_user(db: Session, user: UserCreate) -> UserModel:
    # Hash the password
    hashed_password = get_password_hash(user.password)
    new_user = UserModel(
        username=user.username,
        email=user.email,
        hashed_password=user.password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def update_user(db: Session, user_id: int, user: UserUpdate) -> UserModel:
    db_user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db_user.username = user.username
    db_user.email = user.email
    db_user.password = user.password
    db.commit()
    db.refresh(db_user)
    return db_user

