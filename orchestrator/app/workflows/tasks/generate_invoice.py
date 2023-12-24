
from app.workflows.context import Context


def generate_invoice(parameters: dict | None, context: Context):
    print(f"Generate Invoice {parameters}")
