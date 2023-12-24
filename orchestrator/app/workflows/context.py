from functools import reduce
from types import MappingProxyType
from typing import Any


class Context:
    def __init__(self, data: dict):
        self.data = MappingProxyType({"$context": data})

    def get_field_by_path(self, path: str) -> Any:
        """Deep find value from dict by path

        Args:
            path (str): Full path to the field denoted by dot notation
                Example:
                    "payment.amount" -> 100
                    "event.payment.currency" -> "USD"

        Returns:
            Any: Value of the field
        """

        return reduce(lambda data, key: data.get(key) if isinstance(data, dict) else None, path.split("."), self.data)
