from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from .enums import ConditionOperator, NodeState, NodeType


class NodeDependency(BaseModel):
    node_id: str
    state: NodeState


class Node(BaseModel):
    node_type: NodeType
    node_id: str
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


class PaymentRuleSchema(BaseModel):
    id: UUID
    created_at: datetime
    updated_at: datetime
    company_id: str
    rules: list[Condition | Task]


class PaymentRuleCreate(BaseModel):
    company_id: str
    rules: list[Condition | Task]
