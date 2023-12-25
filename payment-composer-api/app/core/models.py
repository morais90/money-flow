from uuid import uuid4

import pendulum
from sqlalchemy import Column, DateTime, String
from sqlalchemy.dialects.postgresql import JSON, UUID

from app.core.database import Base


def utc_now():
    return pendulum.now().naive()


class Model(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    created_at = Column(DateTime, default=utc_now)
    updated_at = Column(DateTime, default=utc_now, onupdate=utc_now)

    __abstract__ = True
    __mapper_args__ = {"eager_defaults": True}


class PaymentRule(Model):
    __tablename__ = "payment_rules"

    company_id = Column(String, nullable=False)
    rules = Column(JSON, nullable=False, default=dict)
