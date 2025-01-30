from pydantic import BaseModel
from typing import Optional

class RecipeIngredientCreate(BaseModel):
    quantity: float
    unit: str
    recipe_id: int
    ingredient_id: int

class RecipeIngredient(BaseModel):
    id: int
    quantity: float
    unit: str
    recipe_id: int
    ingredient_id: int

    class Config:
        orm_mode = True