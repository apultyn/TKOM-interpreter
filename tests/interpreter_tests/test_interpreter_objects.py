import pytest

from src.interpreter.interpreter_objects import IntValue, FloatValue, StringValue
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


def test_string():
    obj = StringValue("My string")

    assert obj == StringValue("My string")
    assert obj.type_of() == StringValue("String")
    assert obj.truthy()

    assert not StringValue("").truthy()


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
