from typing import List

from drtpy_core import FunctionCallBuilder, TransactionPayload

from passwords_manager.account_key_value import AccountKeyValue


class SaveKeyValuesBuilder:
    def __init__(self) -> None:
        self.items: List[AccountKeyValue] = []

    def add_items(self, items: List[AccountKeyValue]) -> 'SaveKeyValuesBuilder':
        self.items.extend(items)
        return self

    def build(self) -> TransactionPayload:
        backing_builder = FunctionCallBuilder()
        backing_builder.set_function("SaveKeyValue")

        for item in self.items:
            backing_builder.add_argument(item.key)
            backing_builder.add_argument(item.value)

        return backing_builder.build()
