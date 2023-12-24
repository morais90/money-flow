from typing_extensions import TypedDict


class TaskInput(TypedDict):
    task_name: str
    parameters: dict
