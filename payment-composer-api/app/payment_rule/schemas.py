from datetime import datetime
from typing import Literal, Union
from uuid import UUID

from pydantic import BaseModel, Field, Tag
from typing_extensions import Annotated

from .enums import ConditionOperator, NodeState


class NodeDependency(BaseModel):
    node_id: str
    state: NodeState


class Node(BaseModel):
    node_id: str
    depends_on: list[NodeDependency] = Field(default_factory=list)


class ConditionContext(BaseModel):
    field: str
    operator: ConditionOperator
    value: list[str]


class Condition(Node):
    node_type: Literal["condition"] = "condition"
    expect: list[ConditionContext] = Field(default_factory=list)


class Task(Node):
    node_type: Literal["task"] = "task"
    task_name: str
    parameters: dict | None = None


class PaymentRuleSchema(BaseModel):
    id: UUID
    created_at: datetime
    updated_at: datetime
    company_id: str
    rules: list[Condition | Task]


def get_node_type(value):
    return value["node_type"]


Nodes = Annotated[
    Union[Annotated[Condition, Tag("condition")], Annotated[Task, Tag("task")]], Field(discriminator="node_type")
]


class PaymentRuleCreate(BaseModel):
    company_id: str
    rules: list[Nodes]
