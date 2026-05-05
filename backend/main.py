from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.router import router
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from contextlib import asynccontextmanager
from utils.storage_sync import storage_sync


scheduler = AsyncIOScheduler()

@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler.add_job(
        storage_sync.start_synchronization,
        CronTrigger(minute=24, hour='*', second=0),
        id="sync_storage"
    )
    scheduler.start()
    yield
    scheduler.shutdown()

app = FastAPI(title="Silkov. The second version", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(router)