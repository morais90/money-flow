from collections import defaultdict
from functools import partial

from prefect import flow

from app.workflows.context import Context

from .nodes import condition_node, task_node
from .typing import Rules


@flow(name="Product Worlflow")
def product_workflow(context: Context, rules: Rules):
    """Product Workflow

    Args:
        context (Context): Context
        rules (Rules): Rules
    """

    # TODO Node class with upstream and downstream methods
    execution_order = {}
    depedencie_graph = defaultdict(list)

    for rule in rules:
        node_id = rule["node_id"]
        depends_on = rule.get("depends_on") or []

        # TODO: Node factory to abstract the node creation
        if rule["node_type"] == "condition":
            node = partial(condition_node, rule["expect"], context=context)

        elif rule["node_type"] == "task":
            node = partial(task_node, rule.get("parameters", {}), context=context)

        if depends_on:
            depedencie_graph[node_id].extend(depends_on)
        else:
            execution_order[node_id] = {"task": node, "state": None}

    # TODO: Execute the graph
