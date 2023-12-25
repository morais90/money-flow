import factory
import pendulum
from factory.alchemy import SQLAlchemyModelFactory
from faker import Faker

from app.core.models import PaymentRule

from .database import ScopedSession

faker = Faker()


class PaymentRuleFactory(SQLAlchemyModelFactory):
    id = factory.Sequence(lambda _: faker.uuid4())
    company_id = factory.Sequence(lambda _: faker.uuid4())
    created_at = factory.Sequence(lambda i: pendulum.now("UTC"))
    updated_at = factory.Sequence(lambda i: pendulum.now("UTC"))

    class Meta:
        model = PaymentRule
        sqlalchemy_session = ScopedSession
        sqlalchemy_session_persistence = "commit"
