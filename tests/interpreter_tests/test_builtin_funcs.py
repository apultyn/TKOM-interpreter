import pytest

from src.parser.parser_objects import (
    CallExpr,
    Identifier,
    IntExpr,
    AccessExpr,
    FloatExpr,
    StringExpr,
    BoolExpr,
    ItemExpr,
    ListExpr,
    DictExpr,
    FunctionExpr,
    ReturnStmt,
    Block,
    Program,
    NormalAssignmentStmt,
)
from src.interpreter.interpreter_objects import (
    ListValue,
    UserFuncValue,
    IntValue,
    ItemValue,
    StringValue,
    DictValue,
    BoolValue,
)

from src.interpreter.util import DEFAULT_SORT
from tests.interpreter_tests.util import get


@pytest.mark.parametrize("amount", range(10))
def test_print(make_interpreter, capsys, amount):
    make_interpreter().eval(
        CallExpr(Identifier("print"), [IntExpr(5) for _ in range(amount)])
    )

    captured = capsys.readouterr()
    output = ["5" for _ in range(amount)]
    assert captured.out == " ".join(output) + "\n"


@pytest.mark.parametrize(
    "object, type",
    [
        (IntExpr(1), "Int"),
        (FloatExpr(1.5), "Float"),
        (StringExpr("hi"), "String"),
        (BoolExpr(True), "Bool"),
        (ItemExpr(StringExpr("key"), StringExpr("val")), "Item"),
        (ListExpr([]), "List"),
        (DictExpr([]), "Dict"),
        (FunctionExpr([], None), "Function"),
        (Identifier("print"), "Function"),
        (AccessExpr(ListExpr([]), Identifier("get")), "Function"),
    ],
)
def test_typeof(make_interpreter, object, type):
    assert make_interpreter().eval(
        CallExpr(Identifier("typeOf"), [object])
    ) == StringValue(type)


def test_Dict(make_interpreter):
    interpreter = make_interpreter()
    assert interpreter.eval(CallExpr(Identifier("Dict"), [])) == DictValue(
        [], DEFAULT_SORT
    )

    function = FunctionExpr(
        [Identifier("item1"), Identifier("item2")],
        Block([ReturnStmt(IntExpr(1))]),
    )

    assert interpreter.eval(CallExpr(Identifier("Dict"), [function])) == DictValue(
        [], UserFuncValue(["item1", "item2"], function)
    )


def test_add_new_to_dict_default(make_interpreter):
    interpreter = make_interpreter(
        env=[
            (
                "x",
                DictValue([ItemValue(IntValue(1), IntValue(2))], DEFAULT_SORT),
            )
        ]
    )

    interpreter.eval(
        CallExpr(
            AccessExpr(Identifier("x"), Identifier("addNew")),
            [IntExpr(3), IntExpr(4)],
        )
    )

    assert interpreter.global_env.get("x") == DictValue(
        [
            ItemValue(IntValue(1), IntValue(2)),
            ItemValue(IntValue(3), IntValue(4)),
        ],
        DEFAULT_SORT,
    )


def test_add_to_dict_default(make_interpreter):
    interpreter = make_interpreter(
        env=[
            (
                "x",
                DictValue([ItemValue(IntValue(1), IntValue(2))], DEFAULT_SORT),
            )
        ]
    )

    interpreter.eval(
        CallExpr(
            AccessExpr(Identifier("x"), Identifier("add")),
            [ItemExpr(IntExpr(3), IntExpr(4))],
        )
    )

    assert interpreter.global_env.get("x") == DictValue(
        [
            ItemValue(IntValue(1), IntValue(2)),
            ItemValue(IntValue(3), IntValue(4)),
        ],
        DEFAULT_SORT,
    )


def test_list_get(make_interpreter):
    assert make_interpreter().eval(
        CallExpr(
            AccessExpr(
                ListExpr([IntExpr(1), IntExpr(2), IntExpr(3)]), Identifier("get")
            ),
            [IntExpr(1)],
        )
    ) == IntValue(2)


def test_list_set(make_interpreter):
    interpreter = make_interpreter(
        env=[
            (
                "x",
                ListValue([IntValue(1), IntValue(2), IntValue(3)]),
            )
        ]
    )

    interpreter.eval(
        CallExpr(
            AccessExpr(Identifier("x"), Identifier("set")),
            [IntExpr(1), StringExpr("hi")],
        )
    )

    assert interpreter.global_env.get("x") == ListValue(
        [IntValue(1), StringValue("hi"), IntValue(3)]
    )


def test_list_add(make_interpreter):
    interpreter = make_interpreter(
        env=[
            (
                "x",
                ListValue([IntValue(1), IntValue(2), IntValue(3)]),
            )
        ]
    )

    interpreter.eval(
        CallExpr(
            AccessExpr(Identifier("x"), Identifier("add")),
            [IntExpr(4)],
        )
    )

    assert interpreter.global_env.get("x") == ListValue(
        [IntValue(1), IntValue(2), IntValue(3), IntValue(4)]
    )


def test_list_remove(make_interpreter):
    interpreter = make_interpreter(
        env=[
            (
                "x",
                ListValue([IntValue(1), IntValue(2), IntValue(3)]),
            )
        ]
    )

    interpreter.eval(
        CallExpr(
            AccessExpr(Identifier("x"), Identifier("remove")),
            [IntExpr(0)],
        )
    )

    assert interpreter.global_env.get("x") == ListValue([IntValue(2), IntValue(3)])


def test_dict_contains(make_interpreter):
    assert make_interpreter().eval(
        CallExpr(
            AccessExpr(
                DictExpr(
                    [ItemExpr(IntExpr(1), IntExpr(2)), ItemExpr(IntExpr(3), IntExpr(4))]
                ),
                Identifier("contains"),
            ),
            [IntExpr(3)],
        )
    ) == BoolValue(True)


def test_dict_remove(make_interpreter):
    interpreter = make_interpreter(
        env=[
            (
                "x",
                DictValue(
                    [
                        ItemValue(IntValue(1), IntValue(1)),
                        ItemValue(IntValue(2), IntValue(2)),
                    ],
                    DEFAULT_SORT,
                ),
            )
        ]
    )

    interpreter.eval(
        CallExpr(
            AccessExpr(
                Identifier("x"),
                Identifier("remove"),
            ),
            [IntExpr(2)],
        )
    )

    assert interpreter.global_env.get("x") == DictValue(
        [ItemValue(IntValue(1), IntValue(1))], DEFAULT_SORT
    )


def test_copying_values(make_interpreter):
    interpreter = make_interpreter(
        env=[
            ("list", ListValue([IntValue(1), IntValue(2), IntValue(3)])),
            (
                "dict",
                DictValue(
                    [
                        ItemValue(StringValue("key"), StringValue("value")),
                        ItemValue(StringValue("other"), StringValue("other value")),
                    ],
                    DEFAULT_SORT,
                ),
            ),
        ]
    )

    interpreter.eval(
        Program(
            [
                NormalAssignmentStmt(
                    Identifier("list2"),
                    CallExpr(AccessExpr(Identifier("list"), Identifier("copy")), []),
                ),
                NormalAssignmentStmt(
                    Identifier("dict2"),
                    CallExpr(AccessExpr(Identifier("dict"), Identifier("copy")), []),
                ),
                CallExpr(
                    AccessExpr(Identifier("list2"), Identifier("add")), [IntExpr(4)]
                ),
                CallExpr(
                    AccessExpr(Identifier("dict2"), Identifier("add")),
                    [ItemExpr(StringExpr("one_more"), StringExpr("tkom"))],
                ),
            ]
        )
    )

    assert get(interpreter, "list") is not get(interpreter, "list2")
    assert get(interpreter, "dict") is not get(interpreter, "dict2")

    assert get(interpreter, "list") == ListValue(
        [IntValue(1), IntValue(2), IntValue(3)]
    )
    assert get(interpreter, "list2") == ListValue(
        [IntValue(1), IntValue(2), IntValue(3), IntValue(4)]
    )

    assert get(interpreter, "dict") == DictValue(
        [
            ItemValue(StringValue("key"), StringValue("value")),
            ItemValue(StringValue("other"), StringValue("other value")),
        ],
        DEFAULT_SORT,
    )

    assert get(interpreter, "dict2") == DictValue(
        [
            ItemValue(StringValue("key"), StringValue("value")),
            ItemValue(StringValue("other"), StringValue("other value")),
            ItemValue(StringValue("one_more"), StringValue("tkom")),
        ],
        DEFAULT_SORT,
    )
