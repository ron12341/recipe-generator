from http.client import HTTPException
from sqlalchemy.orm import Session
from app.models.user_model import User as UserModel
from app.schemas.user_schema import UserRequest, UserUpdate
from app.core.security import get_password_hash


def create_user(db: Session, uid: str, email: str) -> UserModel:

    new_user = UserModel(
        id=uid,
        email=email,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def update_user(db: Session, user_id: int, user: UserUpdate) -> UserModel:
    db_user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db_user.email = user.email
    db_user.password = user.password
    db.commit()
    db.refresh(db_user)
    return db_user

