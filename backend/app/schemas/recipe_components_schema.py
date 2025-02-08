from pydantic import BaseModel

class CookTime(BaseModel):
    hours: str
    minutes: str

    class Config:
        orm_mode = True

class Instruction(BaseModel):
    step: str
    title: str
    description: str

    class Config:
        orm_mode = True

class Serving(BaseModel):
    number: str
    unit: str

    class Config:
        orm_mode = True
