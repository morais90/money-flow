import httpx
from app.core.settings import settings
from faker import Faker

Faker.seed(0)
faker = Faker(["pt_BR"])


class PaymentComposerService:
    def __init__(self) -> None:
        self.client = httpx.AsyncClient(base_url=settings.PAYMENT_COMPOSER_API)

    async def get_rules(self, company_id: str) -> dict:
        response = await self.client.get(f"/rules/{company_id}")
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