import pytest

from tests.interpreter_tests.util import default_sort
from src.interpreter.interpreter_objects import (
    IntValue,
    FloatValue,
    StringValue,
    BoolValue,
    ListValue,
    ItemValue,
    DictValue,
)
from src.parser.parser_objects import CallExpr, Identifier
from src.util.pyscript_exceptions import RuntimeException


def test_int():
    obj = IntValue(5)

    assert obj == IntValue(5)
    assert obj.to_float() == FloatValue(5.0)
    assert obj.to_string() == StringValue("5")
    assert obj.truthy()
    assert obj.type_of() == StringValue("Int")

    assert not IntValue(0).truthy()

    obj2 = IntValue(-7)

    assert obj + obj2 == IntValue(-2)
    assert obj - obj2 == IntValue(12)
    assert obj * obj2 == IntValue(-35)
    assert obj // obj2 == IntValue(-1)

    assert obj > obj2
    assert obj >= obj2
    assert not obj == obj2
    assert obj != obj2
    assert not obj < obj2
    assert not obj <= obj2


def test_float():
    obj = FloatValue(3.4)

    assert obj == FloatValue(3.4)
    assert obj.to_int() == IntValue(3)
    assert obj.to_string() == StringValue("3.4")
    assert obj.truthy()
    assert obj.type_of() == StringValue("Float")

    assert not FloatValue(0.0).truthy()

    obj2 = FloatValue(-0.9)

    assert obj + obj2 == FloatValue(2.5)
    assert obj - obj2 == FloatValue(4.3)
    assert obj * obj2 == FloatValue(-3.06)
    assert obj / obj2 == FloatValue(-3.7777777777777777)

    assert obj > obj2
    assert obj >= obj2
    assert not obj == obj2
    assert obj != obj2
    assert not obj < obj2
    assert not obj <= obj2


def test_zero_division():
    int1 = IntValue(5)
    int2 = IntValue(0)

    float1 = FloatValue(5.0)
    float2 = FloatValue(0.0)

    assert int2 // int1 == IntValue(0)
    assert float2 / float1 == FloatValue(0.0)

    with pytest.raises(ZeroDivisionError):
        int1 // int2

    with pytest.raises(ZeroDivisionError):
        float1 / float2


def test_string():
    obj = StringValue("My string")

    assert obj == StringValue("My string")
    assert obj.type_of() == StringValue("String")
    assert obj.truthy()

    assert not StringValue("").truthy()

    obj2 = StringValue("Ale")

    assert obj + obj2 == StringValue("My stringAle")
    assert obj > obj2
    assert obj >= obj2
    assert not obj == obj2
    assert obj != obj2
    assert not obj < obj2
    assert not obj <= obj2


def test_string_casting():
    node = CallExpr(callee=Identifier("to_smth", pos=(1, 1)), args=[], pos=(1, 5))

    assert StringValue("12345").to_int(node) == IntValue(12345)
    assert StringValue("-0.56").to_float(node) == FloatValue(-0.56)

    with pytest.raises(RuntimeException) as excinfo:
        StringValue("Hello").to_int(node)

    exc = excinfo.value
    assert exc.pos == (1, 5)
    assert exc.msg == "Cannot cast 'Hello' to Int"

    with pytest.raises(RuntimeException) as excinfo:
        StringValue("Hello").to_float(node)

    exc = excinfo.value
    assert exc.pos == (1, 5)
    assert exc.msg == "Cannot cast 'Hello' to Float"


def test_bool():
    obj_true = BoolValue(True)
    obj_false = BoolValue(False)

    assert obj_true.truthy() and not obj_false.truthy()
    assert obj_true.type_of() == StringValue("Bool")


def test_list():
    obj = ListValue([IntValue(1), IntValue(2), IntValue(3)])
    obj2 = ListValue([IntValue(1), IntValue(2), IntValue(3)])

    assert obj == obj2
    assert obj.length() == IntValue(3)
    assert obj.truthy()

    assert obj + obj2 == ListValue(
        [IntValue(1), IntValue(2), IntValue(3), IntValue(1), IntValue(2), IntValue(3)]
    )
    assert obj.type_of() == StringValue("List")
    assert obj.get(0) == IntValue(1)

    obj.set(0, IntValue(5))
    assert obj == ListValue([IntValue(5), IntValue(2), IntValue(3)])

    obj.remove(1)
    assert obj == ListValue([IntValue(5), IntValue(3)])

    with pytest.raises(IndexError):
        obj.get(2)
    with pytest.raises(IndexError):
        obj.set(2, IntValue(10))


def test_item():
    obj = ItemValue(IntValue(1), StringValue("one"))

    assert obj == ItemValue(IntValue(1), StringValue("one"))
    assert obj.get_key() == IntValue(1)
    assert obj.get_value() == StringValue("one")
    assert obj.type_of() == StringValue("Item")


def test_dict_no_sort():
    obj = DictValue(
        [
            ItemValue(IntValue(1), StringValue("one")),
            ItemValue(IntValue(2), StringValue("two")),
            ItemValue(IntValue("hello"), StringValue("there")),
        ],
        order_func=default_sort,
    )

    assert obj == DictValue(
        [
            ItemValue(IntValue(1), StringValue("one")),
            ItemValue(IntValue(2), StringValue("two")),
            ItemValue(IntValue("hello"), StringValue("there")),
        ],
        order_func=default_sort,
    )

    assert obj.length() == IntValue(3)
    assert obj.truthy()
    assert obj.type_of() == StringValue("Dict")

    # Adding
    obj.add_new(StringValue("general"), StringValue("kenobi"))
    assert obj == DictValue(
        [
            ItemValue(IntValue(1), StringValue("one")),
            ItemValue(IntValue(2), StringValue("two")),
            ItemValue(IntValue("hello"), StringValue("there")),
            ItemValue(StringValue("general"), StringValue("kenobi")),
        ],
        order_func=default_sort,
    )

    obj.add(ItemValue(BoolValue(True), StringValue("yes")))
    assert obj == DictValue(
        [
            ItemValue(IntValue(1), StringValue("one")),
            ItemValue(IntValue(2), StringValue("two")),
            ItemValue(IntValue("hello"), StringValue("there")),
            ItemValue(StringValue("general"), StringValue("kenobi")),
            ItemValue(BoolValue(True), StringValue("yes")),
        ],
        order_func=default_sort,
    )

    with pytest.raises(KeyError):
        obj.add_new(IntValue(1), StringValue("duplicate"))

    with pytest.raises(KeyError):
        obj.add(ItemValue(BoolValue(True), StringValue("duplicate")))

    # Removing
    obj.remove(IntValue(1))
    assert obj == DictValue(
        [
            ItemValue(IntValue(2), StringValue("two")),
            ItemValue(IntValue("hello"), StringValue("there")),
            ItemValue(StringValue("general"), StringValue("kenobi")),
            ItemValue(BoolValue(True), StringValue("yes")),
        ],
        order_func=default_sort,
    )

    with pytest.raises(KeyError):
        obj.remove(IntValue(1))

    # Contains
    assert obj.contains(StringValue("general")) == BoolValue(True)
    assert obj.contains(StringValue("General")) == BoolValue(False)

    # Get
    assert obj.get(BoolValue(True)) == ItemValue(BoolValue(True), StringValue("yes"))

    with pytest.raises(KeyError):
        obj.get(IntValue(1))
