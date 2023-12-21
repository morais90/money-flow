from uuid import UUID

from app.core.database import Session
from app.core.dependencies import get_session
from app.core.models import PaymentRule
from fastapi import APIRouter, Depends
from sqlalchemy import select

from .schemas import PaymentRuleCreate

router = APIRouter()


@router.get("/payment-rules/{company_id}")
async def get_payment_rules(company_id: UUID, db: Session = Depends(get_session)):
    statement = select(PaymentRule).where(PaymentRule.company_id == str(company_id))
    payment_rule = (await db.scalars(statement)).one()

    return payment_rule


@router.post("/payment-rules/")
async def create_payment_rules(
    payload: PaymentRuleCreate, db: Session = Depends(get_session)
):
    payment_rule = PaymentRule(**payload.dict())

    async with db.begin():
        db.add(payment_rule)
