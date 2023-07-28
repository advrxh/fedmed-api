from fastapi import APIRouter, Depends
from beanie import PydanticObjectId

from models import Prescription, User, DaySchedule, MedSchedule
from models.prescription_bucket import Medication

from util import get_redis, json_serial

from datetime import datetime
from pytz import timezone, utc

from util import get_redis
import json

router = APIRouter()
redis = get_redis()


def create_schedule(medication: Medication, schedule: DaySchedule):
    schedules = []
    if (
        (medication.type.value == "tablet") or (medication.type.value == "capsule")
    ) and schedule.tc < 3:
        schedule.tc += 1
        for course in medication.course_timings:
            schedules.append(
                MedSchedule(
                    name=medication.name,
                    id=f"tablet:{schedule.tc}",
                    timestamp=course.timestamp,
                    dose=course.dose,
                )
            )

    elif (medication.type.value == "drops") and schedule.dc < 3:
        schedule.dc += 1
        for course in medication.course_timings:
            schedules.append(
                MedSchedule(
                    name=medication.name,
                    id=f"drop:{schedule.dc}",
                    timestamp=course.timestamp,
                    dose=1,
                )
            )

    return schedules


@router.get("/")
async def get_schedule():
    schedule = await redis.get("schedule")

    return json.loads(schedule)


@router.post("/{user_id}")
async def schedule(user_id: str):
    _user = await User.get(user_id)

    _prescription = await Prescription.get(_user.active_prescription)

    time = datetime.now()
    time = time.replace(tzinfo=utc)
    localtime = time.astimezone(timezone("Asia/Kolkata"))

    _schedule = DaySchedule(schedules=[])

    for medication in _prescription.medications:
        _start = medication.duration.start_date.replace(tzinfo=utc)
        _end = medication.duration.end_date.replace(tzinfo=utc)
        if _start <= localtime <= _end:
            course_list = create_schedule(medication, _schedule)
            _schedule.schedules.extend(course_list)

    return await redis.set(
        "schedule", json.dumps(_schedule.dict()["schedules"], default=json_serial)
    )
