from pydantic import BaseModel, Field

from .enums import ConditionOperator, NodeState, NodeType

# {
#     "rules": [
#         {
#             "node_type": "condition",
#             "id": "condition-1",
#             "expect": [
#                 {
#                     "field": "$context.event.payment_type",
#                     "operator": "eq",
#                     "value": ["product"],
#                 }
#             ],
#         },
#         {
#             "node_type": "task",
#             "id": "abort-flow-1",
#             "depends_on": [{"node_id": "conditional-1", "state": "failure"}],
#             "task_name": "abort_flow",
#             "parameters": None,
#         },
#         {
#             "node_type": "task",
#             "id": "generate-invoice-1",
#             "depends_on": [{"node_id": "conditional-1", "state": "success"}],
#             "task_name": "generate_invoice",
#             "parameters": {
#                 "company_id": "$context.event.company_id",
#                 "product_id": "$context.event.product.id",
#             },
#         },
#         {
#             "node_type": "condition",
#             "id": "condition-2",
#             "depends_on": [{"node_id": "condition-1", "state": "success"}],
#             "expect": [
#                 {
#                     "field": "$context.event.product.type",
#                     "operator": "eq",
#                     "value": ["book", "ebook"],
#                 }
#             ],
#         },
#         {
#             "node_type": "task",
#             "id": "",
#             "task_name": "generate_royalty",
#             "parameters": {
#                 "company_id": "$context.event.company_id",
#                 "product_id": "$context.event.product.id",
#             },
#         },
#     ],
# }


class NodeDependency(BaseModel):
    node_id: str
    state: NodeState


class Node(BaseModel):
    node_type: NodeType
    id: str
    depends_on: list[NodeDependency] = Field(default_factory=list)


class ConditionContext(BaseModel):
    field: str
    operator: ConditionOperator
    value: list[str]


class Condition(Node):
    expect: list[ConditionContext] = Field(default_factory=list)


class Task(Node):
    task_name: str
    parameters: dict = None


class PaymentRule(BaseModel):
    rules: list[Condition | Task]


class PaymentRuleCreate(BaseModel):
    company_id: str
    rules: list[Condition | Task]
