from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import aioredis

from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie

from config import CONFIG
from models import Prescription, User
from routers import prescription_router, user_router, schedule_router


def create_app():
    """
    redis: Redis instance / coroutine
    """
    app = FastAPI()

    origins = ["*"]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # include routers

    app.include_router(prescription_router, prefix="/prescriptions")
    app.include_router(user_router, prefix="/users")
    app.include_router(schedule_router, prefix="/scheduler")

    @app.on_event("startup")
    async def app_init():
        app.db = AsyncIOMotorClient(CONFIG.mongo_uri).fedmed
        await init_beanie(app.db, document_models=[Prescription, User])

    @app.get("/")
    async def read_root():
        return None

    return app


app = create_app()
