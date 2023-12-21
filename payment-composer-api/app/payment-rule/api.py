from app.core.database import Session
from fastapi import APIRouter

from .schemas import PaymentRuleSchema

router = APIRouter()


@router.get("/payment-rules/{company_id}")
async def get_payment_rules(company_id: str):
    pass


@router.post("/payment-rules/")
async def create_payment_rules(payload: PaymentRuleSchema, db: Session):
    pass
