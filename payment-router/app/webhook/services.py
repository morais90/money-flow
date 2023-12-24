import httpx
from faker import Faker

from app.core.settings import settings

from .exceptions import ServiceException

Faker.seed(0)
faker = Faker(["pt_BR"])


class PaymentComposerService:
    def __init__(self) -> None:
        self.client = httpx.AsyncClient(base_url=settings.PAYMENT_COMPOSER_API)

    async def get_payment_rules(self, company_id: str) -> dict:
        response = await self.client.get(f"/payment-rules/{company_id}")

        if response.status_code != httpx.codes.OK:
            raise ServiceException("There was an error fetching the payment rules")

        return response.json()


class CompanyService:
    async def get_company(self, company_id: str) -> dict:
        return {
            "company_id": company_id,
            "company_name": faker.company(),
            "cnpj": faker.cnpj(),
            "address": {
                "street_address": faker.street_address(),
                "neighborhood": faker.neighborhood(),
                "city": faker.city(),
                "state": faker.state(),
            },
        }
