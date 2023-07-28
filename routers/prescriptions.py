from fastapi import APIRouter

from models import PrescriptionIn, Prescription
from beanie import PydanticObjectId

from bson.errors import InvalidId
from typing import List

from config import CONFIG
from qr import get_qr_b64

router = APIRouter()


@router.put("/")
async def create(prescription: PrescriptionIn):
    _prescription = await Prescription(**prescription.dict()).create()

    return {"id": str(_prescription.id)}


@router.get("/{prescription_id}")
async def get(prescription_id: str):
    try:
        _prescription = await Prescription.find_one(
            Prescription.id == PydanticObjectId(prescription_id)
        )
    except InvalidId:
        return "Invalid id, it must be a 12-byte input or a 24-character hex string."

    return PrescriptionIn(**_prescription.dict()) if _prescription is not None else {}


@router.get("/all/{user_id}")
async def get(user_id: str):
    _prescriptions: List[Prescription] = await Prescription.find_many(
        Prescription.user_id == user_id
    ).to_list()

    _ret_prescs: List[PrescriptionIn] = []

    for prescription in _prescriptions:
        _ret_prescs.append(
            {
                "id": str(prescription.id),
                "prescription": PrescriptionIn(**prescription.dict()).dict(),
            }
        )

    return _ret_prescs
