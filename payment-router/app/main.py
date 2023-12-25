from fastapi import FastAPI

from app.webhook.api import router as webhook_router

app = FastAPI()
app.include_router(webhook_router)


@app.get("/", status_code=200)
async def health_check():
    return {"status": "ok"}
