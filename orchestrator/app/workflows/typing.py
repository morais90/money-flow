from typing import Literal

from typing_extensions import TypedDict

from .enums import ConditionOperator, NodeState


class NodeDependency(TypedDict):
    node_id: str
    state: NodeState


class Node(TypedDict):
    node_id: str
    depends_on: list[NodeDependency]


class Conditional(TypedDict):
    field: str
    operator: ConditionOperator
    value: list[str]


class ConditionNode(Node):
    node_type: Literal["condition"]
    expect: list[Conditional]


class TaskNode(Node):
    node_type: Literal["task"]
    task_name: str
    parameters: dict | None


Rules = list[ConditionNode | TaskNode]
