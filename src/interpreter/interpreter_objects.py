from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import Protocol, runtime_checkable, Self

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

    @abstractmethod
    def type_of(self) -> "StringValue":
        pass

    @staticmethod
    def typecheck(lhs: "Value", rhs: "Value", operation: str):
        if lhs.__class__ is not rhs.__class__:
            raise TypeError(
                f"Type missmatch in '{operation}' operation - got {lhs.__class__.__qualname__} and {rhs.__class__.__qualname__}"
            )


@runtime_checkable
class Additive(Protocol):
    @abstractmethod
    def __add__(self: Self, other: Self) -> Self:
        pass


@runtime_checkable
class Subtractive(Protocol):
    @abstractmethod
    def __sub__(self: Self, other: Self) -> Self:
        pass


@runtime_checkable
class Multiplicative(Protocol):
    @abstractmethod
    def __mul__(self: Self, other: Self) -> Self:
        pass


@dataclass(frozen=True, order=True)
class IntValue(Value, Additive, Subtractive, Multiplicative):
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
        if other.value == 0:
            raise ZeroDivisionError
        return IntValue(self.value // other.value)

    def __str__(self) -> str:
        return f"{self.value}"


@dataclass(frozen=True, order=True)
class FloatValue(Value, Additive, Subtractive, Multiplicative):
    value: float

    def truthy(self):
        return self.value != 0.0

    def to_string(self) -> "StringValue":
        return StringValue(str(self.value))

    def to_int(self) -> "IntValue":
        return IntValue(int(self.value))

    def type_of(self) -> "StringValue":
        return StringValue("Float")

    def __add__(self, other: "FloatValue") -> "FloatValue":
        return FloatValue(self.value + other.value)

    def __sub__(self, other: "FloatValue") -> "FloatValue":
        return FloatValue(self.value - other.value)

    def __mul__(self, other: "FloatValue") -> "FloatValue":
        return FloatValue(self.value * other.value)

    def __truediv__(self, other: "FloatValue") -> "FloatValue":
        if other.value == 0.0:
            raise ZeroDivisionError
        return FloatValue(self.value / other.value)

    def __str__(self) -> str:
        return f"{self.value}"


@dataclass(frozen=True, order=True)
class StringValue(Value, Additive):
    value: str

    def truthy(self):
        return self.value != ""

    def to_float(self, node: po.ParserObject) -> "FloatValue":
        try:
            return FloatValue(float(self.value))
        except ValueError:
            msg = f"Cannot cast '{self.value}' to Float"
            raise RuntimeException(msg, pos=node.pos)

    def to_int(self, node: po.ParserObject) -> "IntValue":
        try:
            return IntValue(int(self.value))
        except ValueError:
            msg = f"Cannot cast '{self.value}' to Int"
            raise RuntimeException(msg, pos=node.pos)

    def type_of(self) -> "StringValue":
        return StringValue("String")

    def __add__(self, other: "StringValue"):
        return StringValue(self.value + other.value)


@dataclass
class BoolValue(Value):
    value: bool

    def truthy(self):
        return self.value

    def type_of(self) -> "StringValue":
        return StringValue("Bool")


@dataclass
class ItemValue(Value):
    key: Value
    value: Value


@dataclass
class Collection(Value):
    elements: list[Value]

    def truthy(self):
        return len(self.elements) > 0

    def length(self) -> IntValue:
        return IntValue(len(self.elements))


@dataclass(order=False)
class ListValue(Collection, Additive):
    def __add__(self, other: "ListValue"):
        return ListValue(self.elements + other.elements)

    def type_of(self) -> "StringValue":
        return StringValue("List")

    def get(self, index: int) -> Value:
        if index < 0 or index >= self.length().value:
            raise IndexError(f"Index {index} out of range")
        return self.elements[index]

    def add(self, value: Value):
        self.elements.append(value)

    def set(self, index: int, value: Value):
        if index < 0 or index >= self.length().value:
            raise IndexError(f"Index {index} out of range")
        self.elements[index] = value

    def remove(self, index: int):
        if index < 0 or index >= self.length().value:
            raise IndexError(f"Index {index} out of range")
        self.elements.pop(index)


@dataclass
class Dict(Collection):
    order_func: "FuncValue"
    elements: list[ItemValue]


@dataclass
class FuncValue(Value):
    pass
