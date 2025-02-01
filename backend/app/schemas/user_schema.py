from pydantic import BaseModel
from typing import List, Optional

class UserCreate(BaseModel):
    id: str
    email: str
    username: str | None = None

class UserUpdate(BaseModel):
    username: Optional[str]
    email: Optional[str]

class UserResponse(BaseModel):
    id: str
    email: str
    username: str | None
    recipes: List[int] # list of recipe ids
    preferences: List[int] # list of preference ids

    class Config:
        orm_mode = True 