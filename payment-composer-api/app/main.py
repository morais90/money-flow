from app.payment_rule.api import router as payment_rule_router
from fastapi import FastAPI

app = FastAPI()
app.include_router(payment_rule_router)


@app.get("/", status_code=200)
async def health_check():
    return {"status": "ok"}
