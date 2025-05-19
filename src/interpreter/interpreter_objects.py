from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from typing import Protocol, runtime_checkable, Self, Callable
import src.parser.parser_objects as po
from src.util.pyscript_exceptions import RuntimeException


@dataclass
class Cell:
    value: "Value"


class Env:
    def __init__(
        self,
        context: po.ParserObject,
        parent: "Env | None" = None,
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
        return f"Env with context: '{self.context.__class__.__qualname__}' at row: {self.context.pos[0]}, col: {self.context.pos[1]}"


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
    param_variants: list[list[type[Value]]]

    def type_of(self) -> "StringValue":
        return StringValue("FuncValue")


@dataclass
class UserFuncValue(FuncValue):
    body: po.Block


@dataclass
class BuiltInFuncValue(FuncValue):
    body: Callable[..., Value | None]
    needs_inter: bool = False


@dataclass
class AccessedFuncValue(FuncValue):
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
            raise RuntimeException(f"Cannot cast '{self.value}' to Float")

    def to_int(self) -> "IntValue":
        try:
            return IntValue(int(self.value))
        except ValueError:
            raise RuntimeException(f"Cannot cast '{self.value}' to Int")

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
    members: dict[str, Cell] = field(init=False, repr=False, compare=False)

    def __post_init__(self):
        self.members = {
            "key": Cell(BuiltInFuncValue("key", [[]], lambda *_: self.get_key())),
            "value": Cell(BuiltInFuncValue("value", [[]], lambda *_: self.get_value())),
        }

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
    def __init__(self, statement: po.ReturnStmt, return_value: Value | None = None):
        self.return_statement = statement
        self.return_value = return_value
        super().__init__(f"Return signal with {self.return_value}")


@dataclass
class DictValue(Collection):
    order_func: "UserFuncValue" = field(default=None, repr=False, compare=False)
    members: dict[str, Cell] = field(init=False, repr=False, compare=False)

    def __post_init__(self):
        self.members = {
            "addNew": Cell(
                BuiltInFuncValue(
                    "addNew",
                    [[Value, Value]],
                    lambda inter, env, val1, val2: self.add_new(inter, env, val1, val2),
                )
            ),
            "add": Cell(
                BuiltInFuncValue(
                    "add",
                    [[ItemValue]],
                    lambda inter, env, item: self.add(inter, env, item),
                )
            ),
            "remove": Cell(
                BuiltInFuncValue(
                    "remove", [[Value]], lambda _, __, val: self.remove(val)
                )
            ),
            "contains": Cell(
                BuiltInFuncValue(
                    "contains", [[Value]], lambda _, __, val: self.contains(val)
                )
            ),
            "get": Cell(
                BuiltInFuncValue("get", [[Value]], lambda _, __, val: self.get(val))
            ),
        }

    def add_new(self, method, env, key: Value, value: Value):
        if self.contains(key).value:
            raise KeyError(f"Key {key} already exists in the dictionary")
        if not is_simple(key):
            raise KeyError(f"{key.__class__.__qualname__} can't be an item key")

        new_item = ItemValue(key, value)

        if isinstance(self.order_func, BuiltInFuncValue):
            for i, item in enumerate(self.elements):
                if self.order_func(new_item, item) < IntValue(0):
                    self.elements.insert(i, new_item)
                    return
            self.elements.append(new_item)

        if isinstance(self.order_func, UserFuncValue):
            for i, item in enumerate(self.elements):
                env = self.order_func.get_call_env([new_item, item], None)

                comp_value = None
                try:
                    comp_value = method(self.order_func.body, env)
                except ReturnSignal as ret:
                    comp_value = ret.return_value

                if not isinstance(comp_value, IntValue):
                    raise RuntimeException(
                        msg=f"Function '{self.order_func.name}' should return IntValue",
                        pos=self.order_func.body.pos,
                    )

                if comp_value < IntValue(0):
                    self.elements.insert(i, new_item)
                    return
            self.elements.append(new_item)

    def add(self, method, env, item: ItemValue):
        self.add_new(method, env, item.get_key(), item.get_value())

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
