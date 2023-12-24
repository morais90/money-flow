from typing import Callable

from .abort_flow import abort_flow
from .generate_invoice import generate_invoice
from .generate_royalty import generate_royalty

TASKS = {
    "payments.tasks.abort_flow": abort_flow,
    "payments.tasks.generate_invoice": generate_invoice,
    "payments.tasks.generate_royalty": generate_royalty,
}


def get_task_by_name(task_name: str) -> Callable:
    return TASKS[task_name]
