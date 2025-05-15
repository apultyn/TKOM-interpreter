from src.interpreter.interpreter_objects import IntValue, FloatValue, StringValue

def test_int():
    obj = IntValue(5)

    assert obj == IntValue(5)
    assert obj.to_float() == FloatValue(5.0)
    assert obj.to_string() == StringValue("5")
    assert obj.truthy() == True
    assert obj.type_of() == StringValue("Int")

    assert not IntValue(0).truthy()

    obj2 = IntValue(-7)

    assert obj + obj2 == IntValue(-2)
    assert obj - obj2 == IntValue(12)
    assert obj * obj2 == IntValue(-35)
    assert obj // obj2 == IntValue(-1)
