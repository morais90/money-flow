from app.webhook.api import router as webhook_router
from fastapi import FastAPI

app = FastAPI()
app.include_router(webhook_router)
