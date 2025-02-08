from pydantic import BaseModel
from typing import Optional

class RecipeIngredientCreate(BaseModel):
    quantity: float
    unit: str
    recipe_id: int
    ingredient_id: int

class RecipeIngredientResponse(RecipeIngredientCreate):
    id: int

    class Config:
        orm_mode = True