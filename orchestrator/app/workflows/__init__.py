from .context import Context
from .product import product_workflow

__all__ = ["create_workflow", "Context"]


def create_workflow(workflow_name: str):
    if workflow_name == "product":
        return product_workflow

    raise RuntimeError(f"Workflow {workflow_name} not found")
