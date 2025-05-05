import pytest

from ..util import AbortExecution, check_error_position
from src.util.pyscript_exceptions import SyntaxException


def test_program_not_statement(mocked_error_handler, make_parser):
    src = "[1, 2, 3]"
    parser = make_parser(src, err=mocked_error_handler)

    with pytest.raises(AbortExecution):
        parser.parse_program()

    check_error_position(
        mocked_error_handler, SyntaxException, (1, 1), msg="Statement expected"
    )


def test_stmt_with_ident_not_created(mocked_error_handler, make_parser):
    src = "a;"
    parser = make_parser(src, err=mocked_error_handler)

    with pytest.raises(AbortExecution):
        parser.parse_program()

    check_error_position(
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

    check_error_position(
        mocked_error_handler, SyntaxException, (1, 6), msg="';' expected"
    )


def test_assignment_no_expr(mocked_error_handler, make_parser):
    src = "a ="
    parser = make_parser(src, err=mocked_error_handler)

    with pytest.raises(AbortExecution):
        parser.parse_program()

    check_error_position(
        mocked_error_handler, SyntaxException, (1, 4), msg="Expression expected"
    )


def test_access_no_ident(mocked_error_handler, make_parser):
    src = "a = dict.5"
    parser = make_parser(src, err=mocked_error_handler)

    with pytest.raises(AbortExecution):
        parser.parse_program()

    check_error_position(
        mocked_error_handler, SyntaxException, (1, 10), msg="Identifier expected"
    )


def test_call_no_right_bracket(mocked_error_handler, make_parser):
    src = "print(5, 7, hello"
    parser = make_parser(src, err=mocked_error_handler)

    with pytest.raises(AbortExecution):
        parser.parse_program()

    check_error_position(
        mocked_error_handler, SyntaxException, (1, 18), msg="')' expected"
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

    check_error_position(
        mocked_error_handler, SyntaxException, (2, 4), msg="'(' expected"
    )


def test_if_no_expr(mocked_error_handler, make_parser):
    src = """
if () {
    return a;
}
"""
    parser = make_parser(src, err=mocked_error_handler)

    with pytest.raises(AbortExecution):
        parser.parse_program()

    check_error_position(
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

    check_error_position(
        mocked_error_handler, SyntaxException, (2, 7), msg="')' expected"
    )


def test_if_no_block(mocked_error_handler, make_parser):
    src = "if (a==10);"
    parser = make_parser(src, err=mocked_error_handler)

    with pytest.raises(AbortExecution):
        parser.parse_program()

    check_error_position(
        mocked_error_handler, SyntaxException, (1, 11), msg="Body expected"
    )


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

    check_error_position(
        mocked_error_handler, SyntaxException, (4, 8), msg="'(' expected"
    )


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

    check_error_position(
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

    check_error_position(
        mocked_error_handler, SyntaxException, (4, 16), msg="')' expected"
    )


def test_elif_no_body(mocked_error_handler, make_parser):
    src = """
if (a==10) {
    return 1;
} elif (a == 5)"""
    parser = make_parser(src, err=mocked_error_handler)

    with pytest.raises(AbortExecution):
        parser.parse_program()

    check_error_position(
        mocked_error_handler, SyntaxException, (4, 16), msg="Body expected"
    )
