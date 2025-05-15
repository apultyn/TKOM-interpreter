from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import Protocol, runtime_checkable, TypeVar

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
    def typecheck(lhs: "Value", rhs: "Value", node: po.ParserObject):
        if lhs.__class__ is not rhs.__class__:
            raise RuntimeException(
                f"Type missmatch in operation {node._name} - got {lhs.__class__.__qualname__} and {rhs.__class__.__qualname__}",
                pos=node.pos,
            )


T = TypeVar("T", bound="Additive")


@runtime_checkable
class Additive(Protocol):
    @abstractmethod
    def __add__(self: T, other: T) -> T:
        pass


@dataclass(frozen=True, order=True)
class IntValue(Additive):
    value: int

    def truthy(self) -> bool:
        return self.value != 0

    def to_string(self) -> "StringValue":
        return StringValue(str(self.value))

    def to_float(self) -> "FloatValue":
        return FloatValue(float(self.value))

    def type_of(self) -> "StringValue":
        return StringValue("Int")

    def __add__(self, other: "IntValue") -> "IntValue":
        return IntValue(self.value + other.value)

    def __sub__(self, other: "IntValue") -> "IntValue":
        return IntValue(self.value - other.value)

    def __mul__(self, other: "IntValue") -> "IntValue":
        return IntValue(self.value * other.value)

    def __floordiv__(self, other: "IntValue") -> "IntValue":
        return IntValue(self.value // other.value)

    def __str__(self) -> str:
        return f"{self.value}"


@dataclass(frozen=True, order=True)
class FloatValue(Additive):
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
class BoolValue(Value):
    value: bool

    def truthy(self):
        return self.value


@dataclass
class ItemValue(Value):
    key: Value
    value: Value


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
