from typing import Optional
from pydantic import BaseModel


class TargetCreate(BaseModel):
    name: str
    country: str
    notes: Optional[str] = None
    complete: bool = False


class TargetUpdate(BaseModel):
    notes: Optional[str] = None
    complete: Optional[bool] = None
