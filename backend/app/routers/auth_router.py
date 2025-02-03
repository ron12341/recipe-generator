from fastapi import APIRouter, Depends, Request, HTTPException, status
from fastapi.responses import JSONResponse
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

        print("Logging in...")
        # Parse the JSON data from the request
        body = await request.json()
        id_token = body.get("id_token")

        # Verify the Firebase ID token
        decoded_token = verify_firebase_token(id_token)
        uid = decoded_token.get("uid")

        # Check if the user already exists
        user : UserModel = db.query(UserModel).filter(UserModel.id == uid).first()

        print("USER: ", user)

        if not user:
            print("User does not exist in the database")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        # Create the user response
        user_response = UserResponse(
            **user.__dict__,
            recipes=[],
            preferences=[],
        )

        return {"message": "User logged in successfully", "user": user_response}
    
    except HTTPException as e:
        raise e
    except Exception as e:
        print("Unexpected error: ", e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")
    
@router.post("/signup")
async def signup(request: Request, db: Session = Depends(get_db)):
    
    try:
        # Parse the JSON data from the request
        body = await request.json()
        id_token = body.get("id_token")
        request_email = body.get("email")
        request_username = request_email.split("@")[0]

        # Verify the Firebase ID token
        decoded_token = verify_firebase_token(id_token)
        uid = decoded_token.get("uid")

        # Check if the user already exists
        user = db.query(UserModel).filter(UserModel.id == uid).first()

        if not user:

            new_user = UserCreate(
                id=uid,
                email=request_email,
                username=request_username
            )

            # Create the user and add it to the database
            user : UserModel = create_user(db, new_user)

            user_response = UserResponse(
                **user.__dict__,
                recipes=[],
                preferences=[]
            )

            return {"message": "User created successfully", "user": user_response}

        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

    except Exception as e:
        print("Error: ", e)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")