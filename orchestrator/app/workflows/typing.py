from typing_extensions import TypedDict

from .enums import ConditionOperator, NodeState, NodeType


class NodeDependency(TypedDict):
    node_id: str
    state: NodeState


class Node(TypedDict):
    node_type: NodeType
    node_id: str
    depends_on: list[NodeDependency]


class Conditional(TypedDict):
    field: str
    operator: ConditionOperator
    value: list[str]


class ConditionNode(Node):
    expect: list[Conditional]


class TaskNode(Node):
    task_name: str
    parameters: dict | None


Rules = list[ConditionNode | TaskNode]
