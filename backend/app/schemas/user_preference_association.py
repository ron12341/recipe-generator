from pydantic import BaseModel

class UserPreferenceAssociation(BaseModel):
    user_id: int
    preference_id: int

    class Config:
        orm_mode = True