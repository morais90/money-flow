from unittest.mock import ANY

from fastapi import status


class TestAPICreatePaymentRules:
    def test_create_payment_rules(self, client):
        response = client.post(
            "/payment-rules/",
            json={
                "company_id": "12e301cc-8628-4dfc-89c1-e8e37a6e3221",
                "rules": [
                    {
                        "node_type": "condition",
                        "node_id": "condition-1",
                        "expect": [{"field": "$context.event.payment_type", "operator": "eq", "value": ["product"]}],
                    },
                ],
            },
        )

        assert response.json() == {
            "id": ANY,
            "created_at": ANY,
            "updated_at": ANY,
            "company_id": "12e301cc-8628-4dfc-89c1-e8e37a6e3221",
            "rules": [
                {
                    "node_type": "condition",
                    "node_id": "condition-1",
                    "depends_on": [],
                    "expect": [{"field": "$context.event.payment_type", "operator": "eq", "value": ["product"]}],
                }
            ],
        }
        assert response.status_code == status.HTTP_201_CREATED

    def test_create_payment_rules_required_fields(self, client):
        response = client.post("/payment-rules/", json={})

        assert response.json() == {
            "detail": [
                {
                    "type": "missing",
                    "loc": ["body", "company_id"],
                    "msg": "Field required",
                    "input": {},
                    "url": "https://errors.pydantic.dev/2.5/v/missing",
                },
                {
                    "type": "missing",
                    "loc": ["body", "rules"],
                    "msg": "Field required",
                    "input": {},
                    "url": "https://errors.pydantic.dev/2.5/v/missing",
                },
            ]
        }
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
