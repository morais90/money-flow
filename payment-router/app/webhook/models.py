from datetime import datetime

from pydantic import BaseModel

from .enums import PaymentType


class PaymentItem(BaseModel):
    id: str
    name: str
    price: float


class Product(PaymentItem):
    amount: int


class DigitalProduct(PaymentItem):
    expires_in: datetime


class Subscription(PaymentItem):
    start_date: datetime
    end_date: datetime


class Service(PaymentItem):
    pass


class PaymentEvent(BaseModel):
    company_id: str
    type: PaymentType
    total: float
    discount: float = 0.0
    tax: float = 0.0
    fees: float = 0.0

    product: Product = None
    digital_product: DigitalProduct = None
    subscription: Subscription = None
    service: Service = None
