from prefect import task

from app.workflows.context import Context

from .enums import ConditionOperator
from .typing import ConditionInput

OPERATION_MAP = {
    ConditionOperator.EQ: lambda x, y: x == y,
    ConditionOperator.NEQ: lambda x, y: x != y,
    ConditionOperator.GT: lambda x, y: x > y,
    ConditionOperator.GTE: lambda x, y: x >= y,
    ConditionOperator.LT: lambda x, y: x < y,
    ConditionOperator.LTE: lambda x, y: x <= y,
    ConditionOperator.IN: lambda x, y: x in y,
    ConditionOperator.NIN: lambda x, y: x not in y,
    ConditionOperator.STARTSWITH: lambda x, y: x.startswith(y),
    ConditionOperator.ENDSWITH: lambda x, y: x.endswith(y),
    ConditionOperator.ISNULL: lambda x, y: x is None,
    ConditionOperator.ISNOTNULL: lambda x, y: x is not None,
}


@task
def condition_node(input: ConditionInput, context: Context):
    """Condition Node

    Args:
        input (ConditionInput): Condition Input
        context (Context): Data Context
    """

    for expect in input["expect"]:
        is_sequence_operator = expect["operator"] in [ConditionOperator.IN, ConditionOperator.NIN]

        operation = OPERATION_MAP[expect["operator"]]
        field = context.get_field_by_path(expect["field"])
        value = expect["value"] if is_sequence_operator else expect["value"][0]

        if not operation(field, value):
            raise ValueError(f"Condition {expect} not satisfied")
