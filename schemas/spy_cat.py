from pydantic import BaseModel


class SpyCatCreate(BaseModel):
    name: str
    years_of_experience: int
    breed: str
    salary: int


class SpyCatUpdate(BaseModel):
    salary: int
