from dataclasses import dataclass

from src.util.pyscript_exceptions import RuntimeException


class Env:
    parent: "Env|None" = None
    symbols: dict[str, "Value"]


class Value:
    def truthy(self) -> bool:
        return True

    def typecheck(lhs: "Value", rhs: "Value", operation: str):
        if lhs.__class__ != rhs.__class__:
            raise RuntimeException(
                f"Type missmatch in operation {operation} - got {lhs.__class__.__qualname__} and {rhs.__class__.__qualname__}"
            )


@dataclass(order=True)
class IntValue(Value):
    value: int

    def truthy(self) -> bool:
        return self.value != 0

    def __add__(self, other: "IntValue"):
        Value.typecheck(self, other, "addition")
        return IntValue(self.value + other.value)
