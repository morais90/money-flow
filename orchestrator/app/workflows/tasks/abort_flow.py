from prefect import task

from app.workflows.context import Context


@task
def abort_flow(parameters: dict | None, context: Context):
    """Abort Flow

    Args:
        parameters (dict | None): An arbitrary dictionary of parameters
        context (Context): Data Context
    """

    print(f"Abort Flow {parameters}")
