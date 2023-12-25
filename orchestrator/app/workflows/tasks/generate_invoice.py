from prefect import task

from app.workflows.context import Context


@task
def generate_invoice(parameters: dict | None, context: Context):
    """Generate Invoice

    Args:
        parameters (dict | None): An arbitrary dictionary of parameters
        context (Context): Data Context
    """

    print(f"Generate Invoice {parameters}")
