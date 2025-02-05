from pydantic import BaseModel
from typing import Optional

class RecipeCreate(BaseModel):
    name: str
    description: Optional[str]
    instructions: str
    instructions: str
    cooking_time: int
    difficulty: str
    rating: float
    servings: int

class RecipeUpdate(BaseModel):
    name: Optional[str]
    description: Optional[str]
    instructions: Optional[str]
    cooking_time: Optional[int]
    difficulty: Optional[str]
    rating: Optional[float]
    servings: Optional[int]

class RecipeResponse(BaseModel):
    id: str
    name: str
    description: Optional[str]
    instructions: str
    cooking_time: int
    difficulty: str
    rating: float
    servings: int
    user_id: int # foreign key to user

    class Config:
        orm_mode = True