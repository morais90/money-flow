from prefect import task

from app.workflows.context import Context


@task
def abort_flow(parameters: dict | None, context: Context):
    print(f"Abort Flow {parameters}")
