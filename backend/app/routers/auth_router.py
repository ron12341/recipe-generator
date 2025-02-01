from fastapi import APIRouter, Depends, Request, HTTPException, status
from app.core.database import get_db
from sqlalchemy.orm import Session
from firebase_admin import auth
from app.services.auth_service import verify_firebase_token
from app.services.user_service import create_user
from app.models.user_model import User as UserModel
from app.schemas.user_schema import UserCreate, UserResponse

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

    try:
        decoded_token = verify_firebase_token()
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
    
@router.post("/signup")
async def signup(request: Request, db: Session = Depends(get_db)):
    
    try:
        # Parse the JSON data from the request
        body = await request.json()
        id_token = body.get("id_token")

        # Verify the Firebase ID token
        decoded_token = verify_firebase_token(id_token)
        uid = decoded_token.get("uid")

        # Check if the user already exists
        user = db.query(UserModel).filter(UserModel.id == uid).first()

        if not user:
            # If the user doesn't exist, create a new user
            firebase_user = auth.get_user(uid)

            new_user = UserCreate(
                id=uid,
                username=firebase_user.email.split("@")[0],
                email=firebase_user.email,
            )

            user = create_user(db, new_user)

        user_response = UserResponse(
            id=user.id,
            email=user.email,
            username=user.username,
            recipes=[],
            preferences=[],
        )

        return {"message": "Signup successful", "user": user_response}

    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")