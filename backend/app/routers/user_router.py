from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.schemas.user_schema import UserResponse, UserCreate
from app.models.user_model import User as UserModel
from app.services.user_service import update_user

router = APIRouter(
    prefix="/users",
    tags=["users"],
)

# Get all users
@router.get("/", response_model=List[UserResponse])
async def get_users(db: Session = Depends(get_db)):
    """
    Get all users

    Returns:
        List[User]: A list of user objects
    """
    users = db.query(UserModel).all()
    return users

# Get a User by ID
@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a user by their ID.

    Args:
        user_id (int): The ID of the user to retrieve.
        db (Session): The database session dependency.

    Returns:
        User: The user object if found.

    Raises:
        HTTPException: If the user is not found, raises a 404 error.
    """

    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Update a User by ID
@router.put("/{user_id}", response_model=UserResponse)
async def update_user(user_id: int, user: UserCreate, db: Session = Depends(get_db)):
    """
    Update a user by their ID.

    Args:
        user_id (int): The ID of the user to update.
        user (UserCreate): The updated user object.
        db (Session): The database session dependency.

    Returns:
        User: The updated user object.

    Raises:
        HTTPException: If the user is not found, raises a 404 error.
    """
    return update_user(db, user_id, user)

# Delete a User by ID
@router.delete("/{user_id}")
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    """
    Delete a user by their ID.

    Args:
        user_id (int): The ID of the user to delete.

    Raises:
        HTTPException: If the user is not found, raises a 404 error.

    Returns:
        dict: A JSON response that indicates the user was deleted successfully.
    """
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"detail": "User deleted successfully"}