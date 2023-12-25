from unittest.mock import ANY

from fastapi import status


class TestAPICreatePaymentRules:
    def test_create_payment_rules_condition_node(self, client):
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
            "created_at": "2023-12-24T12:00:00",
            "updated_at": "2023-12-24T12:00:00",
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

    def test_create_payment_rules_task_node(self, client):
        response = client.post(
            "/payment-rules/",
            json={
                "company_id": "12e301cc-8628-4dfc-89c1-e8e37a6e3221",
                "rules": [
                    {
                        "node_type": "task",
                        "node_id": "abort-flow-1",
                        "depends_on": [],
                        "task_name": "payment.tasks.abort_flow",
                        "parameters": None,
                    },
                ],
            },
        )

        assert response.json() == {
            "id": ANY,
            "created_at": "2023-12-24T12:00:00",
            "updated_at": "2023-12-24T12:00:00",
            "company_id": "12e301cc-8628-4dfc-89c1-e8e37a6e3221",
            "rules": [
                {
                    "node_id": "abort-flow-1",
                    "depends_on": [],
                    "node_type": "task",
                    "task_name": "payment.tasks.abort_flow",
                    "parameters": None,
                }
            ],
        }
        assert response.status_code == status.HTTP_201_CREATED

    def test_create_payment_rules_task_node_with_parameters(self, client):
        response = client.post(
            "/payment-rules/",
            json={
                "company_id": "12e301cc-8628-4dfc-89c1-e8e37a6e3221",
                "rules": [
                    {
                        "node_type": "task",
                        "node_id": "abort-flow-1",
                        "depends_on": [],
                        "task_name": "payment.tasks.abort_flow",
                        "parameters": {
                            "param1": "$context.event.payment_type",
                            "nested_param": {
                                "skip_on_fail": True,
                                "skip_message": "It is a optional task",
                            },
                        },
                    },
                ],
            },
        )

        assert response.json() == {
            "id": ANY,
            "created_at": "2023-12-24T12:00:00",
            "updated_at": "2023-12-24T12:00:00",
            "company_id": "12e301cc-8628-4dfc-89c1-e8e37a6e3221",
            "rules": [
                {
                    "node_id": "abort-flow-1",
                    "depends_on": [],
                    "node_type": "task",
                    "task_name": "payment.tasks.abort_flow",
                    "parameters": {
                        "param1": "$context.event.payment_type",
                        "nested_param": {"skip_on_fail": True, "skip_message": "It is a optional task"},
                    },
                }
            ],
        }
        assert response.status_code == status.HTTP_201_CREATED

    def test_create_payment_rules_invalid_node_type(self, client):
        response = client.post(
            "/payment-rules/",
            json={
                "company_id": "12e301cc-8628-4dfc-89c1-e8e37a6e3221",
                "rules": [
                    {
                        "node_type": "unknown",
                        "node_id": "condition-1",
                        "expect": [{"field": "$context.event.payment_type", "operator": "eq", "value": ["product"]}],
                    },
                ],
            },
        )

        msg = (
            "Input tag 'unknown' found using 'node_type' does not match any of the expected tags: 'condition', 'task'",
        )
        expected = {
            "detail": [
                {
                    "type": "union_tag_invalid",
                    "loc": ["body", "rules", 0],
                    "msg": msg,
                    "input": {
                        "node_type": "unknown",
                        "node_id": "condition-1",
                        "expect": [{"field": "$context.event.payment_type", "operator": "eq", "value": ["product"]}],
                    },
                    "ctx": {"discriminator": "'node_type'", "tag": "unknown", "expected_tags": "'condition', 'task'"},
                    "url": "https://errors.pydantic.dev/2.5/v/union_tag_invalid",
                }
            ]
        }
        assert response.json() == expected
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_create_payment_rules_condition_node_invalid_operator(self, client):
        response = client.post(
            "/payment-rules/",
            json={
                "company_id": "12e301cc-8628-4dfc-89c1-e8e37a6e3221",
                "rules": [
                    {
                        "node_type": "condition",
                        "node_id": "condition-1",
                        "expect": [
                            {"field": "$context.event.payment_type", "operator": "close_to", "value": ["product"]}
                        ],
                    },
                ],
            },
        )

        expected = {
            "detail": [
                {
                    "type": "enum",
                    "loc": ["body", "rules", 0, "condition", "expect", 0, "operator"],
                    "msg": (
                        "Input should be 'eq', 'neq', 'gt', 'gte', 'lt', 'lte', 'in', 'nin', 'startswith', 'endswith',"
                        " 'isnull' or 'isnotnull'"
                    ),
                    "input": "close_to",
                    "ctx": {
                        "expected": (
                            "'eq', 'neq', 'gt', 'gte', 'lt', 'lte', 'in', 'nin', 'startswith', 'endswith', "
                            "'isnull' or 'isnotnull'"
                        )
                    },
                }
            ]
        }
        assert response.json() == expected
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

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
