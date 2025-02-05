from pydantic import BaseModel
from typing import List, Optional

class UserRequest(BaseModel):
    id_token: str
    email: str

class UserUpdate(BaseModel):
    email: Optional[str]

class UserResponse(BaseModel):
    id: str
    email: str
    recipes: List[str] # list of recipe ids
    preferences: List[str] # list of preference ids

    class Config:
        orm_mode = True 