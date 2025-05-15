from dataclasses import dataclass
from abc import ABC

import src.parser.parser_objects as po
from src.util.pyscript_exceptions import RuntimeException


@dataclass
class Cell:
    value: "Value"


class Env:
    parent: "Env|None" = None
    symbols: dict[str, tuple[int, "Value"]]

    def lookup_cell(self, name: str) -> Cell:
        if name in self.symbols:
            return self.symbols[name]
        if self.parent:
            return self.parent.lookup_cell(name)
        raise RuntimeException(msg=f"'{name}' is not defined in this scope")

    def get(self, name: str) -> "Value":
        return self.lookup_cell(name).value

    def set(self, name: str, val: "Value"):
        self.lookup_cell(name).value = val

    def define(self, name: str, val: "Value"):
        self.symbols[name] = Cell(val)

class Value(ABC):
    def truthy(self) -> bool:
        return True

    @staticmethod
    def typecheck(lhs: "Value", rhs: "Value", operation: po.ParserObject):
        if lhs.__class__ != rhs.__class__:
            raise RuntimeException(
                f"Type missmatch in operation {operation._name} - got {lhs.__class__.__qualname__} and {rhs.__class__.__qualname__}",
                pos=operation.pos,
            )


@dataclass(frozen=True, order=True)
class IntValue(Value):
    value: int

    def truthy(self) -> bool:
        return self.value != 0

    def add(self, other: "IntValue"):
        return IntValue(self.value + other.value)


@dataclass(frozen=True, order=True)
class FloatValue(Value):
    value: float

    def truthy(self):
        return self.value != 0.0

    def __add__(self, other: "FloatValue"):
        return FloatValue(self.value + other.value)


@dataclass(frozen=True, order=True)
class StringValue(Value):
    value: str

    def truthy(self):
        return self.value != ""

    def __add__(self, other: "StringValue"):
        return StringValue(self.value + other.value)


@dataclass
class ItemValue(Value):
    key: Value
    value: Value


@dataclass
class BoolValue(Value):
    value: bool

    def truthy(self):
        return self.value


@dataclass
class Collection(Value):
    elements: list[Value]

    def truthy(self):
        return len(self.elements) > 0


@dataclass
class List(Collection):
    pass


@dataclass
class Dict(Collection):
    order_func: "FuncValue"
    elements: list[ItemValue]


@dataclass
class FuncValue(Value):
    pass
