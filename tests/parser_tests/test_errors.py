import pytest

from ..util import AbortExecution, check_error
from src.util.pyscript_exceptions import SyntaxException


def test_program_not_statement(mocked_error_handler, make_parser):
    src = "[1, 2, 3]"
    parser = make_parser(src, err=mocked_error_handler)

    with pytest.raises(AbortExecution):
        parser.parse_program()

    check_error(mocked_error_handler, SyntaxException, (1, 1), msg="Statement expected")


def test_stmt_with_ident_not_created(mocked_error_handler, make_parser):
    src = "a;"
    parser = make_parser(src, err=mocked_error_handler)

    with pytest.raises(AbortExecution):
        parser.parse_program()

    check_error(
        mocked_error_handler,
        SyntaxException,
        (1, 2),
        msg="Assignment or function call expected",
    )


def test_stmt_with_ident_no_semicolon(mocked_error_handler, make_parser):
    src = "a = 2"
    parser = make_parser(src, err=mocked_error_handler)

    with pytest.raises(AbortExecution):
        parser.parse_program()

    check_error(mocked_error_handler, SyntaxException, (1, 6), msg="';' expected")


def test_assignment_no_expr(mocked_error_handler, make_parser):
    src = "a ="
    parser = make_parser(src, err=mocked_error_handler)

    with pytest.raises(AbortExecution):
        parser.parse_program()

    check_error(
        mocked_error_handler, SyntaxException, (1, 4), msg="Expression expected"
    )


def test_access_no_ident(mocked_error_handler, make_parser):
    src = "a = dict.5"
    parser = make_parser(src, err=mocked_error_handler)

    with pytest.raises(AbortExecution):
        parser.parse_program()

    check_error(
        mocked_error_handler, SyntaxException, (1, 10), msg="Identifier expected"
    )


def test_call_no_right_bracket(mocked_error_handler, make_parser):
    src = "print(5, 7, hello"
    parser = make_parser(src, err=mocked_error_handler)

    with pytest.raises(AbortExecution):
        parser.parse_program()

    check_error(
        mocked_error_handler, SyntaxException, (1, 18), msg="')' or ',' expected"
    )


def test_if_no_left_bracket(mocked_error_handler, make_parser):
    src = """
if a==10 {
    return a;
}
"""
    parser = make_parser(src, err=mocked_error_handler)

    with pytest.raises(AbortExecution):
        parser.parse_program()

    check_error(mocked_error_handler, SyntaxException, (2, 4), msg="'(' expected")


def test_if_no_expr(mocked_error_handler, make_parser):
    src = """
if () {
    return a;
}
"""
    parser = make_parser(src, err=mocked_error_handler)

    with pytest.raises(AbortExecution):
        parser.parse_program()

    check_error(
        mocked_error_handler, SyntaxException, (2, 5), msg="Expression expected"
    )


def test_if_no_right_bracket(mocked_error_handler, make_parser):
    src = """
if (a {
    return a;
}
"""
    parser = make_parser(src, err=mocked_error_handler)

    with pytest.raises(AbortExecution):
        parser.parse_program()

    check_error(mocked_error_handler, SyntaxException, (2, 7), msg="')' expected")


def test_if_no_block(mocked_error_handler, make_parser):
    src = "if (a==10);"
    parser = make_parser(src, err=mocked_error_handler)

    with pytest.raises(AbortExecution):
        parser.parse_program()

    check_error(mocked_error_handler, SyntaxException, (1, 11), msg="Body expected")


def test_elif_no_left_bracket(mocked_error_handler, make_parser):
    src = """
if (a==10) {
    return 1;
} elif {
    return 5;
}"""
    parser = make_parser(src, err=mocked_error_handler)

    with pytest.raises(AbortExecution):
        parser.parse_program()

    check_error(mocked_error_handler, SyntaxException, (4, 8), msg="'(' expected")


def test_elif_no_expr(mocked_error_handler, make_parser):
    src = """
if (a==10) {
    return 1;
} elif () {
    return 5;
}"""
    parser = make_parser(src, err=mocked_error_handler)

    with pytest.raises(AbortExecution):
        parser.parse_program()

    check_error(
        mocked_error_handler, SyntaxException, (4, 9), msg="Expression expected"
    )


def test_elif_no_right_bracket(mocked_error_handler, make_parser):
    src = """
if (a==10) {
    return 1;
} elif (a == 5 {
    return 5;
}"""
    parser = make_parser(src, err=mocked_error_handler)

    with pytest.raises(AbortExecution):
        parser.parse_program()

    check_error(mocked_error_handler, SyntaxException, (4, 16), msg="')' expected")


def test_elif_no_body(mocked_error_handler, make_parser):
    src = """
if (a==10) {
    return 1;
} elif (a == 5)"""
    parser = make_parser(src, err=mocked_error_handler)

    with pytest.raises(AbortExecution):
        parser.parse_program()

    check_error(mocked_error_handler, SyntaxException, (4, 16), msg="Body expected")


def test_while_no_left_bracket(mocked_error_handler, make_parser):
    src = """
while {
    print("hi");
}
"""
    parser = make_parser(src, err=mocked_error_handler)

    with pytest.raises(AbortExecution):
        parser.parse_program()

    check_error(mocked_error_handler, SyntaxException, (2, 7), msg="'(' expected")


def test_while_no_condition(mocked_error_handler, make_parser):
    src = """
while (){
    print("hi");
}
"""
    parser = make_parser(src, err=mocked_error_handler)

    with pytest.raises(AbortExecution):
        parser.parse_program()

    check_error(
        mocked_error_handler, SyntaxException, (2, 8), msg="Expression expected"
    )


def test_while_no_right_bracket(mocked_error_handler, make_parser):
    src = """
while (a==10 {
    print("hi");
}
"""
    parser = make_parser(src, err=mocked_error_handler)

    with pytest.raises(AbortExecution):
        parser.parse_program()

    check_error(mocked_error_handler, SyntaxException, (2, 14), msg="')' expected")


def test_while_no_body(mocked_error_handler, make_parser):
    src = "while (a==10);"
    parser = make_parser(src, err=mocked_error_handler)

    with pytest.raises(AbortExecution):
        parser.parse_program()

    check_error(mocked_error_handler, SyntaxException, (1, 14), msg="Body expected")


def test_for_no_ident(mocked_error_handler, make_parser):
    src = "for 5+5"
    parser = make_parser(src, err=mocked_error_handler)

    with pytest.raises(AbortExecution):
        parser.parse_program()

    check_error(
        mocked_error_handler, SyntaxException, (1, 5), msg="Identifier expected"
    )


def test_for_no_in(mocked_error_handler, make_parser):
    src = "for var {}"
    parser = make_parser(src, err=mocked_error_handler)

    with pytest.raises(AbortExecution):
        parser.parse_program()

    check_error(
        mocked_error_handler, SyntaxException, (1, 9), msg="'in' keyword expected"
    )


def test_for_no_expression(mocked_error_handler, make_parser):
    src = "for var in ;"
    parser = make_parser(src, err=mocked_error_handler)

    with pytest.raises(AbortExecution):
        parser.parse_program()

    check_error(
        mocked_error_handler, SyntaxException, (1, 12), msg="Expression expected"
    )


def test_for_no_body(mocked_error_handler, make_parser):
    src = "for var in {};"  # curly brackets are dictionary here
    parser = make_parser(src, err=mocked_error_handler)

    with pytest.raises(AbortExecution):
        parser.parse_program()

    check_error(mocked_error_handler, SyntaxException, (1, 14), msg="Body expected")


def test_return_no_semicolon(mocked_error_handler, make_parser):
    src = "return"  # curly brackets are dictionary here
    parser = make_parser(src, err=mocked_error_handler)

    with pytest.raises(AbortExecution):
        parser.parse_program()

    check_error(mocked_error_handler, SyntaxException, (1, 7), msg="';' expected")


def test_block_wrong_statement(mocked_error_handler, make_parser):
    src = "{5}"
    parser = make_parser(src, err=mocked_error_handler)

    with pytest.raises(AbortExecution):
        parser.parse_program()

    check_error(
        mocked_error_handler, SyntaxException, (1, 2), msg="'}' or statement expected"
    )


def test_block_no_right_bracket(mocked_error_handler, make_parser):
    src = "{a=10;"
    parser = make_parser(src, err=mocked_error_handler)

    with pytest.raises(AbortExecution):
        parser.parse_program()

    check_error(
        mocked_error_handler, SyntaxException, (1, 7), msg="'}' or statement expected"
    )


def test_list_wrong_elem(mocked_error_handler, make_parser):
    src = "a = [5,5;]"
    parser = make_parser(src, err=mocked_error_handler)

    with pytest.raises(AbortExecution):
        parser.parse_program()

    check_error(
        mocked_error_handler, SyntaxException, (1, 9), msg="']' or ',' expected"
    )


def test_list_no_commas(mocked_error_handler, make_parser):
    src = "a = [5 10 15]"
    parser = make_parser(src, err=mocked_error_handler)

    with pytest.raises(AbortExecution):
        parser.parse_program()

    check_error(mocked_error_handler, SyntaxException, (1, 8), msg="',' expected")


def test_list_nothing_after_comma(mocked_error_handler, make_parser):
    src = "a = [5,10,]"
    parser = make_parser(src, err=mocked_error_handler)

    with pytest.raises(AbortExecution):
        parser.parse_program()

    check_error(
        mocked_error_handler, SyntaxException, (1, 11), msg="Expression expected"
    )


def test_list_no_right_bracket(mocked_error_handler, make_parser):
    src = "a = [5, 10, 15"
    parser = make_parser(src, err=mocked_error_handler)

    with pytest.raises(AbortExecution):
        parser.parse_program()

    check_error(
        mocked_error_handler, SyntaxException, (1, 15), msg="']' or ',' expected"
    )


def test_list_no_right_bracket_empty(mocked_error_handler, make_parser):
    src = "a = ["
    parser = make_parser(src, err=mocked_error_handler)

    with pytest.raises(AbortExecution):
        parser.parse_program()

    check_error(
        mocked_error_handler, SyntaxException, (1, 6), msg="']' or expression expected"
    )


def test_dict_wrong_elem(mocked_error_handler, make_parser):
    src = "a = {(5:10)5]"
    parser = make_parser(src, err=mocked_error_handler)

    with pytest.raises(AbortExecution):
        parser.parse_program()

    check_error(
        mocked_error_handler, SyntaxException, (1, 12), msg="'}' or ',' expected"
    )


def test_dict_no_commas(mocked_error_handler, make_parser):
    src = "a = {(5:5) (10:10)}"
    parser = make_parser(src, err=mocked_error_handler)

    with pytest.raises(AbortExecution):
        parser.parse_program()

    check_error(mocked_error_handler, SyntaxException, (1, 12), msg="',' expected")


def test_dict_nothing_after_comma(mocked_error_handler, make_parser):
    src = "a = {(5:5),(1:10),}"
    parser = make_parser(src, err=mocked_error_handler)

    with pytest.raises(AbortExecution):
        parser.parse_program()

    check_error(
        mocked_error_handler, SyntaxException, (1, 19), msg="Item literal expected"
    )


def test_dict_no_right_bracket(mocked_error_handler, make_parser):
    src = "a = {(5:5),(10:10),(15:15)"
    parser = make_parser(src, err=mocked_error_handler)

    with pytest.raises(AbortExecution):
        parser.parse_program()

    check_error(
        mocked_error_handler, SyntaxException, (1, 27), msg="'}' or ',' expected"
    )


def test_dict_no_right_bracket_empty(mocked_error_handler, make_parser):
    src = "a = {"
    parser = make_parser(src, err=mocked_error_handler)

    with pytest.raises(AbortExecution):
        parser.parse_program()

    check_error(
        mocked_error_handler,
        SyntaxException,
        (1, 6),
        msg="'}' or item literal expected",
    )


def test_func_wrong_elem(mocked_error_handler, make_parser):
    src = "a = function(arg1 5)"
    parser = make_parser(src, err=mocked_error_handler)

    with pytest.raises(AbortExecution):
        parser.parse_program()

    check_error(
        mocked_error_handler, SyntaxException, (1, 19), msg="')' or ',' expected"
    )


def test_func_no_commas(mocked_error_handler, make_parser):
    src = "a = function(arg1 arg2)"
    parser = make_parser(src, err=mocked_error_handler)

    with pytest.raises(AbortExecution):
        parser.parse_program()

    check_error(mocked_error_handler, SyntaxException, (1, 19), msg="',' expected")


def test_func_nothing_after_comma(mocked_error_handler, make_parser):
    src = "a = function(arg1,)"
    parser = make_parser(src, err=mocked_error_handler)

    with pytest.raises(AbortExecution):
        parser.parse_program()

    check_error(
        mocked_error_handler, SyntaxException, (1, 19), msg="Identifier expected"
    )


def test_func_no_right_bracket(mocked_error_handler, make_parser):
    src = "a = function(arg1, arg2"
    parser = make_parser(src, err=mocked_error_handler)

    with pytest.raises(AbortExecution):
        parser.parse_program()

    check_error(
        mocked_error_handler, SyntaxException, (1, 24), msg="')' or ',' expected"
    )


def test_func_no_right_bracket_empty(mocked_error_handler, make_parser):
    src = "a = function("
    parser = make_parser(src, err=mocked_error_handler)

    with pytest.raises(AbortExecution):
        parser.parse_program()

    check_error(
        mocked_error_handler, SyntaxException, (1, 14), msg="')' or identifier expected"
    )


def test_linq_no_var(mocked_error_handler, make_parser):
    src = "a = from 5+5"
    parser = make_parser(src, err=mocked_error_handler)

    with pytest.raises(AbortExecution):
        parser.parse_program()

    check_error(
        mocked_error_handler, SyntaxException, (1, 10), msg="Identifier expected"
    )


def test_linq_no_in(mocked_error_handler, make_parser):
    src = "a = from var select"
    parser = make_parser(src, err=mocked_error_handler)

    with pytest.raises(AbortExecution):
        parser.parse_program()

    check_error(
        mocked_error_handler, SyntaxException, (1, 14), msg="'in' keyword expected"
    )


def test_linq_no_source(mocked_error_handler, make_parser):
    src = "a = from var in ; select"
    parser = make_parser(src, err=mocked_error_handler)

    with pytest.raises(AbortExecution):
        parser.parse_program()

    check_error(
        mocked_error_handler, SyntaxException, (1, 17), msg="Expression expected"
    )


def test_linq_no_select(mocked_error_handler, make_parser):
    src = "a = from var in list;"
    parser = make_parser(src, err=mocked_error_handler)

    with pytest.raises(AbortExecution):
        parser.parse_program()

    check_error(
        mocked_error_handler, SyntaxException, (1, 21), msg="'select' keyword expected"
    )


def test_linq_no_selects(mocked_error_handler, make_parser):
    src = "a = from var in list select where"
    parser = make_parser(src, err=mocked_error_handler)

    with pytest.raises(AbortExecution):
        parser.parse_program()

    check_error(
        mocked_error_handler, SyntaxException, (1, 29), msg="Expression expected"
    )


def test_linq_no_comma_between_selects(mocked_error_handler, make_parser):
    src = "a = from var in list select var.key() var.value() "
    parser = make_parser(src, err=mocked_error_handler)

    with pytest.raises(AbortExecution):
        parser.parse_program()

    check_error(mocked_error_handler, SyntaxException, (1, 39), msg="',' expected")


def test_linq_wrong_after_comma(mocked_error_handler, make_parser):
    src = "a = from var in list select var.key(),; "
    parser = make_parser(src, err=mocked_error_handler)

    with pytest.raises(AbortExecution):
        parser.parse_program()

    check_error(
        mocked_error_handler, SyntaxException, (1, 39), msg="Expression expected"
    )


def test_linq_where_no_expr(mocked_error_handler, make_parser):
    src = "a = from var in list select var.key() where ; "
    parser = make_parser(src, err=mocked_error_handler)

    with pytest.raises(AbortExecution):
        parser.parse_program()

    check_error(
        mocked_error_handler, SyntaxException, (1, 45), msg="Expression expected"
    )


def test_linq_order_no_by(mocked_error_handler, make_parser):
    src = "a = from var in list select var.key() order ; "
    parser = make_parser(src, err=mocked_error_handler)

    with pytest.raises(AbortExecution):
        parser.parse_program()

    check_error(
        mocked_error_handler, SyntaxException, (1, 45), msg="'by' keyword expected"
    )


def test_linq_order_by_no_expr(mocked_error_handler, make_parser):
    src = "a = from var in list select var.key() order by ; "
    parser = make_parser(src, err=mocked_error_handler)

    with pytest.raises(AbortExecution):
        parser.parse_program()

    check_error(
        mocked_error_handler, SyntaxException, (1, 48), msg="Expression expected"
    )


def test_linq_descending_no_order(mocked_error_handler, make_parser):
    src = "a = from var in list select var.key() descending; "
    parser = make_parser(src, err=mocked_error_handler)

    with pytest.raises(AbortExecution):
        parser.parse_program()

    check_error(mocked_error_handler, SyntaxException, (1, 39), msg="';' expected")


def test_no_expr_after_bracket(mocked_error_handler, make_parser):
    src = "a = (;)"
    parser = make_parser(src, err=mocked_error_handler)

    with pytest.raises(AbortExecution):
        parser.parse_program()

    check_error(
        mocked_error_handler, SyntaxException, (1, 6), msg="Expression expected"
    )


def test_no_right_bracket(mocked_error_handler, make_parser):
    src = "a = (5<5 ;"
    parser = make_parser(src, err=mocked_error_handler)

    with pytest.raises(AbortExecution):
        parser.parse_program()

    check_error(mocked_error_handler, SyntaxException, (1, 10), msg="')' expected")


def test_item_no_value(mocked_error_handler, make_parser):
    src = "a = (5<5:;) ;"
    parser = make_parser(src, err=mocked_error_handler)

    with pytest.raises(AbortExecution):
        parser.parse_program()

    check_error(
        mocked_error_handler, SyntaxException, (1, 10), msg="Expression expected"
    )


def test_item_no_right_bracket(mocked_error_handler, make_parser):
    src = r'a = (5<5:"hello"'
    parser = make_parser(src, err=mocked_error_handler)

    with pytest.raises(AbortExecution):
        parser.parse_program()

    check_error(mocked_error_handler, SyntaxException, (1, 17), msg="')' expected")
