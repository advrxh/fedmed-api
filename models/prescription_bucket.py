from datetime import datetime
from typing import List
from enum import Enum
from datetime import datetime
from uuid import uuid4


from beanie import Document
from pydantic import BaseModel, Field


def get_uuid():
    return str(uuid4())


class MedicationType(Enum):
    tablet: str = "tablet"
    capsule: str = "capsule"
    syrup: str = "syrup"
    drops: str = "drops"


class CourseTiming(BaseModel):
    before_food: bool
    timestamp: datetime
    dose: int


class Duration(BaseModel):
    start_date: datetime = None
    end_date: datetime = None
    is_symptomatic: bool = False


class Medication(BaseModel):
    id: str = Field(default_factory=get_uuid)
    name: str
    type: MedicationType
    course_timings: List[CourseTiming] = []
    duration: Duration


class PrescriptionIn(BaseModel):
    user_id: str
    medications: List[Medication]


class Prescription(PrescriptionIn, Document):
    class Settings:
        name = "prescriptionBucket"
