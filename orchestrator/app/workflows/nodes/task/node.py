from prefect import task

from app.workflows.context import Context
from app.workflows.tasks import get_task_by_name

from .typing import TaskInput


@task
def task_node(input: TaskInput, context: Context):
    """Task Node

    Args:
        input (TaskInput): Task Input
        context (Context): Data Context
    """
    func = get_task_by_name(input["name"])
    params = {}

    for key, value in input.get("parameters", {}):
        if value.startswith("$context"):
            params[key] = context.get_field_by_path(value)

    return func(context=context, **params)
