from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from typing import Protocol, runtime_checkable, Self, Callable
import src.parser.parser_objects as po


@dataclass
class Cell:
    value: "Value"


class Env:
    def __init__(
        self,
        parent: "Env | None" = None,
        context: po.ParserObject | str = None,
        symbols: dict[str, Cell] | None = None,
    ):
        self.context = context
        self.parent = parent
        self.symbols = symbols if symbols is not None else {}

    def lookup_cell(self, name: str) -> Cell:
        if name in self.symbols:
            return self.symbols[name]
        if self.parent:
            return self.parent.lookup_cell(name)
        raise ValueError(f"'{name}' is not defined in this scope")

    def get(self, name: str) -> "Value":
        return self.lookup_cell(name).value

    def set(self, name: str, val: "Value"):
        self.lookup_cell(name).value = val

    def define(self, name: str, val: "Value"):
        self.symbols[name] = Cell(val)

    def __str__(self) -> str:
        msg_suff = (
            f"'{self.context.__class__.__qualname__}' at row: {self.context.pos[0]}, col: {self.context.pos[1]}"
            if isinstance(self.context, po.ParserObject)
            else self.context
        )
        return f"Env with context: {msg_suff}"


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
                f"Type missmatch in '{operation}' operation - got '{lhs.type_of()}' and '{rhs.type_of()}'"
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


@dataclass
class FuncValue(Value):
    def type_of(self) -> "StringValue":
        return StringValue("FuncValue")


@dataclass
class UserFuncValue(FuncValue):
    params: list[str]
    expression: po.FunctionExpr

    def __str__(self) -> str:
        return "UserFunc"


@dataclass
class BuiltInFuncValue(FuncValue):
    param_variants: list[list[type[Value]]]
    body: Callable[..., Value | None]


@dataclass
class AccessedFuncValue(FuncValue):
    param_variants: list[list[type[Value]]]
    body: Callable[..., Value | None]
    needs_inter: bool = False
    owner: "Value | None" = None


@dataclass(order=True)
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


@dataclass(order=True)
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


@dataclass(order=True)
class StringValue(Value, Additive):
    value: str

    def truthy(self):
        return self.value != ""

    def length(self):
        return IntValue(len(self.value))

    def to_float(self) -> "FloatValue":
        try:
            return FloatValue(float(self.value))
        except ValueError:
            raise ValueError(f"Cannot cast '{self.value}' to Float")

    def to_int(self) -> "IntValue":
        try:
            return IntValue(int(self.value))
        except ValueError:
            raise ValueError(f"Cannot cast '{self.value}' to Int")

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


_SIMPLE_TYPES = (IntValue, FloatValue, StringValue, BoolValue)


def is_simple(val: "Value") -> bool:
    return isinstance(val, _SIMPLE_TYPES)


@dataclass
class ItemValue(Value):
    key: Value
    value: Value

    def get_key(self) -> Value:
        return self.key

    def get_value(self) -> Value:
        return self.value

    def to_string(self) -> StringValue:
        return StringValue(f"{self.key}: {self.value}")

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

    def get(self, index: IntValue) -> Value:
        if index.value < 0 or index.value >= self.length().value:
            raise IndexError(f"Index {index.value} out of range")
        return self.elements[index.value]

    def add(self, value: Value):
        self.elements.append(value)

    def set(self, index: IntValue, value: Value):
        if index.value < 0 or index.value >= self.length().value:
            raise IndexError(f"Index {index.value} out of range")
        self.elements[index.value] = value

    def remove(self, index: IntValue):
        if index.value < 0 or index.value >= self.length().value:
            raise IndexError(f"Index {index.value} out of range")
        self.elements.pop(index.value)

    def to_string(self) -> StringValue:
        return StringValue(self.str_long())

    def __str__(self) -> str:
        return f"List({self.length().value})"

    def str_long(self) -> str:
        elements = ", ".join([str(item) for item in self.elements])
        return "[" + elements + "]"


class ReturnSignal(Exception):
    def __init__(
        self, return_value: Value | None = None, statement: po.ReturnStmt | None = None
    ):
        self.return_value = return_value
        self.return_statement = statement
        super().__init__(f"Return signal with {self.return_value}")


@dataclass
class DictValue(Collection):
    order_func: "UserFuncValue" = field(default=None, compare=False)

    def check_add(self, item: ItemValue):
        if self.contains(item.key).value:
            raise KeyError(f"Key {item.key} already exists in the dictionary")
        if not is_simple(item.key):
            raise KeyError(f"'{item.key.type_of}' can't be an item key")

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

    def to_string(self) -> StringValue:
        return StringValue(self.str_long())

    def type_of(self) -> "StringValue":
        return StringValue("Dict")

    def __str__(self) -> str:
        return f"Dict({self.length().value})"

    def str_long(self) -> str:
        elements = ", ".join([str(item) for item in self.elements])
        return "{" + elements + "}"
