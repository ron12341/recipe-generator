from pydantic import BaseModel
from typing import Optional

class PreferenceCreate(BaseModel):
    name: str # e.g., "Vegetarian", "Vegan", "Gluten Free"
    description: Optional[str]

class PreferenceUpdate(BaseModel):
    name: Optional[str]
    description: Optional[str]

class Preference(BaseModel):
    name: str
    description: Optional[str]

    class Config:
        orm_mode = True