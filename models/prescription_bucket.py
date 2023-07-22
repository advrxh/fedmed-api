from datetime import datetime
from typing import Optional, List, Any
from enum import Enum
from datetime import date, datetime


from beanie import Document, PydanticObjectId
from pydantic import BaseModel, Field


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
    name: str
    type: MedicationType
    course_timings: List[CourseTiming] = []
    duration: Duration


class PrescriptionIn(BaseModel):
    medications: List[Medication]


class Prescription(PrescriptionIn, Document):
    class Settings:
        name = "prescriptionBucket"
