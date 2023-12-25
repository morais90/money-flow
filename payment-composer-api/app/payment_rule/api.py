from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm.exc import NoResultFound

from app.core.database import Session
from app.core.dependencies import get_session
from app.core.models import PaymentRule

from .schemas import PaymentRuleCreate, PaymentRuleSchema

router = APIRouter()


@router.get("/payment-rules/{company_id}")
async def get_payment_rules(company_id: UUID, db: Session = Depends(get_session)) -> PaymentRuleSchema:
    statement = select(PaymentRule).where(PaymentRule.company_id == str(company_id))

    try:
        payment_rule = (await db.scalars(statement)).one()
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Not Found")

    return payment_rule


@router.post("/payment-rules/", status_code=201)
async def create_payment_rules(payload: PaymentRuleCreate, db: Session = Depends(get_session)) -> PaymentRuleSchema:
    payment_rule = PaymentRule(**payload.model_dump())

    async with db.begin():
        db.add(payment_rule)

    return payment_rule
