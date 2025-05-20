import pytest

import src.parser.parser_objects as po
import src.interpreter.interpreter_objects as io

from src.interpreter.util import DEFAULT_SORT


@pytest.mark.parametrize("amount", range(10))
def test_print(make_interpreter, capsys, amount):
    make_interpreter().eval(
        po.CallExpr(po.Identifier("print"), [po.IntExpr(5) for _ in range(amount)])
    )

    captured = capsys.readouterr()
    output = ["5" for _ in range(amount)]
    assert captured.out == " ".join(output) + "\n"


@pytest.mark.parametrize(
    "object, type",
    [
        (po.IntExpr(1), "Int"),
        (po.FloatExpr(1.5), "Float"),
        (po.StringExpr("hi"), "String"),
        (po.BoolExpr(True), "Bool"),
        (po.ItemExpr(po.StringExpr("key"), po.StringExpr("val")), "Item"),
        (po.ListExpr([]), "List"),
        (po.DictExpr([]), "Dict"),
        (po.FunctionExpr([], None), "Function"),
        (po.Identifier("print"), "Function"),
        (po.AccessExpr(po.ListExpr([]), po.Identifier("get")), "Function"),
    ],
)
def test_typeof(make_interpreter, object, type):
    assert make_interpreter().eval(
        po.CallExpr(po.Identifier("typeOf"), [object])
    ) == io.StringValue(type)


def test_Dict(make_interpreter):
    interpreter = make_interpreter()
    assert interpreter.eval(po.CallExpr(po.Identifier("Dict"), [])) == io.DictValue(
        [], DEFAULT_SORT
    )

    function = po.FunctionExpr(
        [po.Identifier("item1"), po.Identifier("item2")],
        po.Block([po.ReturnStmt(po.IntExpr(1))]),
    )

    assert interpreter.eval(
        po.CallExpr(po.Identifier("Dict"), [function])
    ) == io.DictValue([], io.UserFuncValue(["item1", "item2"], function))


def test_add_new_to_dict_default(make_interpreter):
    interpreter = make_interpreter(
        env=[
            (
                "x",
                io.DictValue(
                    [io.ItemValue(io.IntValue(1), io.IntValue(2))], DEFAULT_SORT
                ),
            )
        ]
    )

    interpreter.eval(
        po.CallExpr(
            po.AccessExpr(po.Identifier("x"), po.Identifier("addNew")),
            [po.IntExpr(3), po.IntExpr(4)],
        )
    )

    assert interpreter.global_env.get("x") == io.DictValue(
        [
            io.ItemValue(io.IntValue(1), io.IntValue(2)),
            io.ItemValue(io.IntValue(3), io.IntValue(4)),
        ],
        DEFAULT_SORT,
    )


def test_add_to_dict_default(make_interpreter):
    interpreter = make_interpreter(
        env=[
            (
                "x",
                io.DictValue(
                    [io.ItemValue(io.IntValue(1), io.IntValue(2))], DEFAULT_SORT
                ),
            )
        ]
    )

    interpreter.eval(
        po.CallExpr(
            po.AccessExpr(po.Identifier("x"), po.Identifier("add")),
            [po.ItemExpr(po.IntExpr(3), po.IntExpr(4))],
        )
    )

    assert interpreter.global_env.get("x") == io.DictValue(
        [
            io.ItemValue(io.IntValue(1), io.IntValue(2)),
            io.ItemValue(io.IntValue(3), io.IntValue(4)),
        ],
        DEFAULT_SORT,
    )