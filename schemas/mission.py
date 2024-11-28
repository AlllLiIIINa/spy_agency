from typing import List, Optional
from pydantic import BaseModel
from schemas.target import TargetCreate


class MissionCreate(BaseModel):
    spy_cat_id: Optional[int] = None
    targets: List[TargetCreate]
    complete: bool = False
