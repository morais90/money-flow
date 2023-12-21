from uuid import uuid4

from app.core.database import Base
from sqlalchemy import (
    Column,
    DateTime,
    String,
)
from sqlalchemy.dialects.postgresql import JSON, UUID
from sqlalchemy.sql import func


class Model(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), server_onupdate=func.now())

    __abstract__ = True
    __mapper_args__ = {"eager_defaults": True}


class PaymentRule(Model):
    company_id = Column(String, nullable=False)
    rules = Column(JSON, nullable=False, default=dict)
