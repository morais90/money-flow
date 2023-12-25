from fastapi import status

from app.tests.factories import PaymentRuleFactory


class TestAPIGetPaymentRules:
    def test_get_payment_rules(self, client):
        payment_rule = PaymentRuleFactory(
            rules=[
                {
                    "node_type": "condition",
                    "node_id": "condition-1",
                    "expect": [{"field": "$context.event.payment_type", "operator": "eq", "value": ["product"]}],
                },
            ]
        )
        response = client.get(f"/payment-rules/{payment_rule.company_id}")

        assert response.json() == {
            "id": "e3e70682-c209-4cac-a29f-6fbed82c07cd",
            "created_at": "2023-12-24T12:00:00",
            "updated_at": "2023-12-24T12:00:00",
            "company_id": "f728b4fa-4248-4e3a-8a5d-2f346baa9455",
            "rules": [
                {
                    "node_type": "condition",
                    "node_id": "condition-1",
                    "depends_on": [],
                    "expect": [{"field": "$context.event.payment_type", "operator": "eq", "value": ["product"]}],
                }
            ],
        }
        assert response.status_code == status.HTTP_200_OK

    def test_get_payment_rules_not_found(self, client):
        response = client.get("/payment-rules/123e4567-e89b-12d3-a456-426614174000")

        assert response.status_code == status.HTTP_404_NOT_FOUND
