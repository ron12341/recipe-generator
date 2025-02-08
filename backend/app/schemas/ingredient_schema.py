from pydantic import BaseModel
from typing import Optional

class IngredientCreate(BaseModel):
    name: str
    description: Optional[str]

class Ingredient(BaseModel):
    id: int
    name: str
    description: Optional[str]

    class Config:
        orm_mode = True

class IngredientResponse(BaseModel):
    name: str
    quantity: str
    unit: str

    class Config:
        orm_mode = True