from datetime import datetime
from typing import List
from pydantic import BaseModel


class MedSchedule(BaseModel):
    name: str
    id: str
    timestamp: datetime
    dose: int
    before_food: bool


class DaySchedule(BaseModel):
    tc: int = 0
    dc: int = 0
    schedules: List[MedSchedule]
