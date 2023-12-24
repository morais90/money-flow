from typing_extensions import TypedDict

from .enums import ConditionOperator


class Conditional(TypedDict):
    field: str
    operator: ConditionOperator
    value: list[str]


class ConditionInput(TypedDict):
    expect: list[Conditional]
