import factory
import pendulum
from factory.alchemy import SQLAlchemyModelFactory
from faker import Faker

from app.core.models import PaymentRule

from .database import ScopedSession

Faker.seed(0)
faker = Faker()


class PaymentRuleFactory(SQLAlchemyModelFactory):
    id = factory.Sequence(lambda _: faker.uuid4())
    company_id = factory.Sequence(lambda _: faker.uuid4())
    created_at = factory.Sequence(lambda i: pendulum.now("UTC").add(days=i))
    updated_at = factory.Sequence(lambda i: pendulum.now("UTC").add(days=i))

    class Meta:
        model = PaymentRule
        sqlalchemy_session = ScopedSession
        sqlalchemy_session_persistence = "commit"
