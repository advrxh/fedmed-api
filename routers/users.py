from fastapi import APIRouter
from fastapi.responses import RedirectResponse
from beanie import PydanticObjectId
from pydantic import EmailStr

from models import UserIn, User
from qr import get_qr_b64

router = APIRouter()


@router.put("/")
async def create(user: UserIn):
    _user = await User(**user.dict()).create()
    return {"id": str(_user.id)}


@router.get("/{email}")
async def get_user(email: EmailStr):
    _user = await User.find_one(User.email == email)

    if _user is None:
        return "Invalid email, user does not exist."

    return UserIn(**_user.dict())

@router.get("/{email}")
async def get_user_id_by_email(email: EmailStr):
    _user = await User.find_one(User.email == email)

    if _user is None:
        return "Invalid email, user does not exist."

    return {"id": str(_user.id)}


@router.get("/qr/{id}")
async def get_user_qr(id: str):
    return get_qr_b64(id)


@router.post("/active_prescription/{user_id}")
async def get_user(user_id: str, id: str):
    _user = await User.get(user_id)

    _user.active_prescription = id

    update = await _user.save()

    return {"active_prescription": _user.active_prescription}
