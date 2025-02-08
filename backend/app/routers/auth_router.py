from fastapi import APIRouter, Depends, Request, HTTPException, status
from app.core.database import get_db
from sqlalchemy.orm import Session
from app.services.auth_service import verify_firebase_token
from app.services.user_service import create_user
from app.models.user_model import User as UserModel
from app.schemas.user_schema import UserRequest, UserResponse

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)

@router.post("/login", response_model=UserResponse, summary="Login a user", status_code=status.HTTP_200_OK)
async def login(request: UserRequest, db: Session = Depends(get_db)):
    
    """
    Login a user using a Firebase ID token.

    Parameters:
    - request: The request containing the ID token.
    - db: The database session.

    Returns:
    - A UserResponse object with the user's details.

    Raises:
    - HTTPException: If the user is not found or if there is an internal error.
    """
    try:
        id_token = request.id_token

        # Verify the Firebase ID token
        decoded_token = verify_firebase_token(id_token)
        uid = decoded_token.get("uid")

        # Check if the user already exists
        user : UserModel = db.query(UserModel).filter(UserModel.id == uid).first()

        print("USER: ", user)

        if not user:
            print("User does not exist in the database")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        recipe_ids = [recipe.id for recipe in user.recipes]

        # Create the user response
        user_response = UserResponse(
            id=user.id,
            email=user.email,
            recipes=recipe_ids,
            preferences=[],
        )

        return user_response
    
    except HTTPException as e:
        raise e
    except Exception as e:
        print("Unexpected error: ", e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")
    
@router.post("/signup", response_model=UserResponse, summary="Create a new user", status_code=status.HTTP_201_CREATED)
async def signup(request: UserRequest, db: Session = Depends(get_db)):
    
    """
    Creates a new user using a Firebase ID token.

    Parameters:
    - request: The request containing the ID token and the email address.
    - db: The database session.

    Returns:
    - A UserResponse object with the user's details.

    Raises:
    - HTTPException: If the user is not found or if there is an internal error.
    - HTTPException: If the user already exists.
    """
    try:
        id_token = request.id_token

        # Verify the Firebase ID token
        decoded_token = verify_firebase_token(id_token)
        uid = decoded_token.get("uid")

        print("UID: ", uid)

        # Check if the user already exists
        user = db.query(UserModel).filter(UserModel.id == uid).first()

        if not user:

            user : UserModel = create_user(db, uid, request.email)

            user_response = UserResponse(
                **user.__dict__,
                recipes=[],
                preferences=[]
            )

            return user_response

        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User already exists")

    except HTTPException as e:
        raise e
    except Exception as e:
        print("Unexpected error: ", e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")