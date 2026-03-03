from fastapi import FastAPI
from app.router import router

app = FastAPI(title="Silkov. The second version")

app.include_router(router)