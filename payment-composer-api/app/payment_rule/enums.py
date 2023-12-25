from enum import Enum


class NodeType(str, Enum):
    CONDITION = "condition"
    TASK = "task"


class NodeState(str, Enum):
    SUCCESS = "success"
    FAILURE = "failure"


class ConditionOperator(str, Enum):
    EQ = "eq"
    NEQ = "neq"
    GT = "gt"
    GTE = "gte"
    LT = "lt"
    LTE = "lte"
    IN = "in"
    NIN = "nin"
    STARTSWITH = "startswith"
    ENDSWITH = "endswith"
    ISNULL = "isnull"
    ISNOTNULL = "isnotnull"
