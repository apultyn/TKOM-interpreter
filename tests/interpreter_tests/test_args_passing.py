import pytest

from src.interpreter.interpreter_objects import (
    IntValue,
    StringValue,
    FloatValue,
    BoolValue,
    ItemValue,
    DictValue,
    ListValue,
    UserFuncValue,
)
from src.parser.parser_objects import (
    NormalAssignmentStmt,
    Identifier,
    Program,
    PlusAssignmentStmt,
    IntExpr,
    FloatExpr,
    StringExpr,
    LogicNegExpr,
    CallExpr,
    AccessExpr,
    ItemExpr,
    FunctionExpr,
    Block,
    ReturnStmt,
)

from src.interpreter.util import DEFAULT_SORT


def test_assigning_copies(make_interpreter):
    interpreter = make_interpreter(
        env=[
            ("int", IntValue(1)),
            ("string", StringValue("Hi")),
            ("float", FloatValue(-5.0)),
            ("bool", BoolValue(True)),
        ]
    )

    interpreter.eval(
        Program(
            [
                NormalAssignmentStmt(Identifier("a"), Identifier("int")),
                NormalAssignmentStmt(Identifier("b"), Identifier("string")),
                NormalAssignmentStmt(Identifier("c"), Identifier("float")),
                NormalAssignmentStmt(Identifier("d"), Identifier("bool")),
                PlusAssignmentStmt(Identifier("a"), IntExpr(1)),
                PlusAssignmentStmt(Identifier("b"), StringExpr("there")),
                PlusAssignmentStmt(Identifier("c"), FloatExpr(2.5)),
                NormalAssignmentStmt(Identifier("d"), LogicNegExpr(Identifier("d"))),
            ]
        )
    )

    assert interpreter.global_env.get("int") == IntValue(1)
    assert interpreter.global_env.get("string") == StringValue("Hi")
    assert interpreter.global_env.get("float") == FloatValue(-5.0)
    assert interpreter.global_env.get("bool") == BoolValue(True)

    assert interpreter.global_env.get("a") == IntValue(2)
    assert interpreter.global_env.get("b") == StringValue("Hithere")
    assert interpreter.global_env.get("c") == FloatValue(-2.5)
    assert interpreter.global_env.get("d") == BoolValue(False)


def test_assigning_ref(make_interpreter):
    interpreter = make_interpreter(
        env=[
            ("item", ItemValue(StringValue("key"), ListValue([]))),
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
                NormalAssignmentStmt(Identifier("a"), Identifier("item")),
                NormalAssignmentStmt(Identifier("b"), Identifier("list")),
                NormalAssignmentStmt(Identifier("c"), Identifier("dict")),
                CallExpr(
                    AccessExpr(
                        CallExpr(
                            AccessExpr(Identifier("a"), Identifier("value")), args=[]
                        ),
                        Identifier("add"),
                    ),
                    args=[IntExpr(1)],
                ),
                CallExpr(
                    AccessExpr(Identifier("b"), Identifier("add")), args=[IntExpr(1)]
                ),
                CallExpr(
                    AccessExpr(Identifier("c"), Identifier("add")),
                    args=[ItemExpr(StringExpr("one_more"), StringExpr("gimmie break"))],
                ),
            ]
        )
    )

    assert interpreter.global_env.get("a") is interpreter.global_env.get("item")
    assert interpreter.global_env.get("b") is interpreter.global_env.get("list")
    assert interpreter.global_env.get("c") is interpreter.global_env.get("dict")

    assert interpreter.global_env.get("a") == ItemValue(
        StringValue("key"), ListValue([IntValue(1)])
    )
    assert interpreter.global_env.get("item") == ItemValue(
        StringValue("key"), ListValue([IntValue(1)])
    )

    assert interpreter.global_env.get("b") == ListValue(
        [IntValue(1), IntValue(2), IntValue(3), IntValue(1)]
    )
    assert interpreter.global_env.get("list") == ListValue(
        [IntValue(1), IntValue(2), IntValue(3), IntValue(1)]
    )

    assert interpreter.global_env.get("c") == DictValue(
        [
            ItemValue(StringValue("key"), StringValue("value")),
            ItemValue(StringValue("other"), StringValue("other value")),
            ItemValue(StringValue("one_more"), StringValue("gimmie break")),
        ],
        DEFAULT_SORT,
    )
    assert interpreter.global_env.get("dict") == DictValue(
        [
            ItemValue(StringValue("key"), StringValue("value")),
            ItemValue(StringValue("other"), StringValue("other value")),
            ItemValue(StringValue("one_more"), StringValue("gimmie break")),
        ],
        DEFAULT_SORT,
    )


def test_passing_simple(make_interpreter):
    interpreter = make_interpreter(
        env=[
            ("int", IntValue(1)),
            ("string", StringValue("Hi")),
            ("float", FloatValue(-5.0)),
            ("bool", BoolValue(True)),
            (
                "func_add",
                UserFuncValue(
                    ["input", "val"],
                    FunctionExpr(
                        [Identifier("input"), Identifier("val")],
                        Block(
                            [
                                PlusAssignmentStmt(
                                    Identifier("input"), Identifier("val")
                                ),
                                ReturnStmt(Identifier("input")),
                            ]
                        ),
                    ),
                ),
            ),
            (
                "func_neg",
                UserFuncValue(
                    ["input"],
                    FunctionExpr(
                        [Identifier("input")],
                        Block(
                            [
                                NormalAssignmentStmt(
                                    Identifier("input"),
                                    LogicNegExpr(Identifier("input")),
                                ),
                                ReturnStmt(Identifier("input")),
                            ]
                        ),
                    ),
                ),
            ),
        ]
    )

    interpreter.eval(
        Program(
            [
                NormalAssignmentStmt(
                    Identifier("int2"),
                    CallExpr(Identifier("func_add"), [Identifier("int"), IntExpr(1)]),
                ),
                NormalAssignmentStmt(
                    Identifier("float2"),
                    CallExpr(
                        Identifier("func_add"), [Identifier("float"), FloatExpr(1.5)]
                    ),
                ),
                NormalAssignmentStmt(
                    Identifier("string2"),
                    CallExpr(
                        Identifier("func_add"), [Identifier("string"), StringExpr("Hi")]
                    ),
                ),
                NormalAssignmentStmt(
                    Identifier("bool2"),
                    CallExpr(Identifier("func_neg"), [Identifier("bool")]),
                ),
            ]
        )
    )

    assert interpreter.global_env.get("int") == IntValue(1)
    assert interpreter.global_env.get("int2") == IntValue(2)

    assert interpreter.global_env.get("float") == FloatValue(-5.0)
    assert interpreter.global_env.get("float2") == FloatValue(-3.5)

    assert interpreter.global_env.get("string") == StringValue("Hi")
    assert interpreter.global_env.get("string2") == StringValue("HiHi")

    assert interpreter.global_env.get("bool") == BoolValue(True)
    assert interpreter.global_env.get("bool2") == BoolValue(False)
