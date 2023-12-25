from prefect import Flow

from .context import Context
from .product import product_workflow

__all__ = ["create_workflow", "Context"]


def create_workflow(workflow_name: str) -> Flow:
    """Create a workflow based on the workflow name

    Args:
        workflow_name (str): Workflow name
    """

    if workflow_name == "product":
        return product_workflow

    raise RuntimeError(f"Workflow {workflow_name} not found")
