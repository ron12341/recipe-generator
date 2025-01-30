from fastapi import APIRouter , Depends
from app.core.auth import get_current_user

router = APIRouter(
    prefix="/profile",
    tags=["profile"],
)


@router.get("/", response_model=dict, rummary="Get current user profile")
async def get_profile(user : dict = Depends(get_current_user)):
    return {"id": user["id"], "email": user.get("email", "No email")}