from pydantic import BaseModel
from typing import List, Optional

class UserCreate(BaseModel):
    username: str
    email: str
    password: str   # password should be hashed

class UserUpdate(BaseModel):
    username: Optional[str]
    email: Optional[str]
    password: Optional[str]

class User(BaseModel):
    id: int
    username: str
    email: str
    recipes: List[int] # list of recipe ids
    preferences: List[int] # list of preference ids

    class Config:
        orm_mode = True 