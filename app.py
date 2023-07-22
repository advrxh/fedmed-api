from fastapi import FastAPI

from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie

from config import CONFIG

from models import Prescription

from routers import prescription_router

app = FastAPI()

# include routers

app.include_router(prescription_router, prefix="/prescriptions")


@app.on_event("startup")
async def app_init():
    app.db = AsyncIOMotorClient(CONFIG.mongo_uri).fedmed
    await init_beanie(app.db, document_models=[Prescription])


@app.get("/")
async def read_root():
    return None
