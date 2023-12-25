from prefect import task

from app.workflows.context import Context


@task
def generate_royalty(parameters: dict | None, context: Context):
    """Generate Royalty

    Args:
        parameters (dict | None): An arbitrary dictionary of parameters
        context (Context): Data Context
    """

    print(f"Generate Royalty {parameters}")
