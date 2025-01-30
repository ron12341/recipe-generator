from fastapi import APIRouter, Depends, Request, HTTPException, status
from app.core.database import get_db
from sqlalchemy.orm import Session
from firebase_admin import auth
from app.models.user_model import User as UserModel

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post("/login")
async def login(request: Request, db: Session = Depends(get_db)):
    """
    Logs in a user with the given Bearer token.

    Args:
        request (Request): The request object.
        db (Session): The database session.

    Returns:
        dict: A dictionary containing the message and the user object.
    """
    
    auth_header = request.headers.get("Authorization")

    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    
    token = auth_header.split("Bearer ")[1]

    try:
        decoded_token = auth.verify_id_token(token)
        uid = decoded_token.get("uid")

        user = db.query(UserModel).filter(UserModel.id == uid).first()

        if not user:
            firebase_user = auth.get_user(uid)

            new_user = UserModel(
                id=uid,
                username=firebase_user.email.split("@")[0],
                email=firebase_user.email,
                hashed_password="",
                is_active=True
            )

            db.add(new_user)
            db.commit()
            db.refresh(new_user)

            user = new_user

        return {"message": "Login successful", "user": {"id": user.id, "email": user.email, "username": user.username}}

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")