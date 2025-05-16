from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from typing import Protocol, runtime_checkable, Self

import src.parser.parser_objects as po
from src.util.pyscript_exceptions import RuntimeException


@dataclass
class Cell:
    value: "Value"


class Env:
    def __init__(self, parent: "Env | None" = None, symbols: dict[str, Cell] = {}):
        self.parent = parent
        self.symbols = symbols

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

    def length(self):
        return IntValue(len(self.value))

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

    def __str__(self) -> str:
        return f"{self.value}"


@dataclass
class BoolValue(Value):
    value: bool

    def truthy(self):
        return self.value

    def type_of(self) -> "StringValue":
        return StringValue("Bool")

    def __str__(self) -> str:
        return f"{self.value}"


@dataclass
class ItemValue(Value):
    key: Value
    value: Value

    def get_key(self) -> Value:
        return self.key

    def get_value(self) -> Value:
        return self.value

    def type_of(self):
        return StringValue("Item")

    def __str__(self) -> str:
        return f"({self.key}: {self.value})"


@dataclass(order=False)
class Collection(Value):
    elements: list[Value] = field(default_factory=list)

    def truthy(self):
        return len(self.elements) > 0

    def length(self) -> IntValue:
        return IntValue(len(self.elements))


@dataclass
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

    def __str__(self) -> str:
        return f"List({self.length().value})"

    def str_long(self) -> str:
        elements = ", ".join([str(item) for item in self.elements])
        return "[" + elements + "]"


@dataclass
class DictValue(Collection, Additive):
    order_func: "FuncValue" = None

    def add_new(self, key: Value, value: Value):
        if self.contains(key).value:
            raise KeyError(f"Key {key} already exists in the dictionary")
        for i, item in enumerate(self.elements):
            if self.order_func(key, item.get_key()) < 0:
                self.elements.insert(i, ItemValue(key, value))
                return
        self.elements.append(ItemValue(key, value))

    def add(self, item: ItemValue):
        self.add_new(item.get_key(), item.get_value())

    def remove(self, key: Value):
        for i, item in enumerate(self.elements):
            if item.get_key() == key:
                self.elements.pop(i)
                return
        raise KeyError(f"Key {key} not found in the dictionary")

    def contains(self, key: Value) -> BoolValue:
        for item in self.elements:
            if item.get_key() == key:
                return BoolValue(True)
        return BoolValue(False)

    def get(self, key: Value) -> Value:
        for item in self.elements:
            if item.get_key() == key:
                return item
        raise KeyError(f"Key {key} not found in the dictionary")

    def type_of(self) -> "StringValue":
        return StringValue("Dict")

    def __add__(self, other: "DictValue"):
        for item in other.elements:
            self.add(item)
        return self

    def __str__(self) -> str:
        return f"Dict({self.length().value})"

    def str_long(self) -> str:
        elements = ", ".join([str(item) for item in self.elements])
        return "{" + elements + "}"


@dataclass
class FuncValue(Value):
    params: list[str]
    body: po.Block
    closure: Env

    def get_call_env(
        self, args: list["Value"], call_pos: tuple[int, int]
    ) -> "Value | None":
        if len(args) != len(self.params):
            raise RuntimeException(
                msg=f"Function takes {len(self.params)} arguments, {len(args)} given",
                pos=call_pos,
            )

        local_env = Env(self.closure)

        for name, arg in zip(self.params, args):
            local_env.define(name, arg)

        return local_env



_SIMPLE_TYPES = (IntValue, FloatValue, StringValue, BoolValue)


def is_simple(val: "Value") -> bool:
    return isinstance(val, _SIMPLE_TYPES)
