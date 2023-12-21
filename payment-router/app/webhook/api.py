from app.core.broker import push_to_queue
from fastapi import APIRouter, HTTPException

from .exceptions import ServiceException
from .models import PaymentEvent
from .services import CompanyService, PaymentComposerService

router = APIRouter()


@router.post("/payment", status_code=204, tags=["webhook"])
async def payment_webhook(event: PaymentEvent):
    try:
        company = await CompanyService().get_company(event.company_id)
        composer_rules = await PaymentComposerService().get_rules(event.company_id)

        payload = {"company": company, "payment": event.dict(), "rules": composer_rules}
        push_to_queue("payment", payload)

    except ServiceException:
        raise HTTPException(status_code=500, detail="Internal server error")
