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
from .util import get


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

    assert get(interpreter, "int") == IntValue(1)
    assert get(interpreter, "string") == StringValue("Hi")
    assert get(interpreter, "float") == FloatValue(-5.0)
    assert get(interpreter, "bool") == BoolValue(True)

    assert get(interpreter, "a") == IntValue(2)
    assert get(interpreter, "b") == StringValue("Hithere")
    assert get(interpreter, "c") == FloatValue(-2.5)
    assert get(interpreter, "d") == BoolValue(False)


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

    assert get(interpreter, "a") is get(interpreter, "item")
    assert get(interpreter, "b") is get(interpreter, "list")
    assert get(interpreter, "c") is get(interpreter, "dict")

    assert get(interpreter, "a") == ItemValue(
        StringValue("key"), ListValue([IntValue(1)])
    )
    assert get(interpreter, "item") == ItemValue(
        StringValue("key"), ListValue([IntValue(1)])
    )

    assert get(interpreter, "b") == ListValue(
        [IntValue(1), IntValue(2), IntValue(3), IntValue(1)]
    )
    assert get(interpreter, "list") == ListValue(
        [IntValue(1), IntValue(2), IntValue(3), IntValue(1)]
    )

    assert get(interpreter, "c") == DictValue(
        [
            ItemValue(StringValue("key"), StringValue("value")),
            ItemValue(StringValue("other"), StringValue("other value")),
            ItemValue(StringValue("one_more"), StringValue("gimmie break")),
        ],
        DEFAULT_SORT,
    )
    assert get(interpreter, "dict") == DictValue(
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

    assert get(interpreter, "int") == IntValue(1)
    assert get(interpreter, "int2") == IntValue(2)

    assert get(interpreter, "float") == FloatValue(-5.0)
    assert get(interpreter, "float2") == FloatValue(-3.5)

    assert get(interpreter, "string") == StringValue("Hi")
    assert get(interpreter, "string2") == StringValue("HiHi")

    assert get(interpreter, "bool") == BoolValue(True)
    assert get(interpreter, "bool2") == BoolValue(False)


def test_passing_complex(make_interpreter):
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
            (
                "func_item",
                UserFuncValue(
                    ["arg1"],
                    FunctionExpr(
                        [Identifier("arg1")],
                        Block(
                            [
                                CallExpr(
                                    AccessExpr(
                                        CallExpr(
                                            AccessExpr(
                                                Identifier("arg1"), Identifier("value")
                                            ),
                                            args=[],
                                        ),
                                        Identifier("add"),
                                    ),
                                    args=[IntExpr(1)],
                                ),
                                ReturnStmt(Identifier("arg1")),
                            ]
                        ),
                    ),
                ),
            ),
            (
                "func_list",
                UserFuncValue(
                    ["arg1"],
                    FunctionExpr(
                        [Identifier("arg1")],
                        Block(
                            [
                                CallExpr(
                                    AccessExpr(Identifier("arg1"), Identifier("add")),
                                    args=[IntExpr(1)],
                                ),
                                ReturnStmt(Identifier("arg1")),
                            ]
                        ),
                    ),
                ),
            ),
            (
                "func_dict",
                UserFuncValue(
                    ["arg1"],
                    FunctionExpr(
                        [Identifier("arg1")],
                        Block(
                            [
                                CallExpr(
                                    AccessExpr(Identifier("arg1"), Identifier("add")),
                                    args=[
                                        ItemExpr(
                                            StringExpr("one_more"),
                                            StringExpr("gimmie break"),
                                        )
                                    ],
                                ),
                                ReturnStmt(Identifier("arg1")),
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
                    Identifier("item2"),
                    CallExpr(Identifier("func_item"), [Identifier("item")]),
                ),
                NormalAssignmentStmt(
                    Identifier("list2"),
                    CallExpr(Identifier("func_list"), [Identifier("list")]),
                ),
                NormalAssignmentStmt(
                    Identifier("dict2"),
                    CallExpr(Identifier("func_dict"), [Identifier("dict")]),
                ),
            ]
        )
    )

    assert get(interpreter, "item") is get(interpreter, "item2")
    assert get(interpreter, "list") is get(interpreter, "list2")
    assert get(interpreter, "dict") is get(interpreter, "dict2")
