from beanie import Document
from pydantic import BaseModel, EmailStr


class UserIn(BaseModel):
    name: str
    email: EmailStr
    active_prescription: str = None


class User(UserIn, Document):
    class Settings:
        name = "users"
