import io
import pytest

from src.source import Source
from src.pyscript_exceptions import NewLineException


def test_get_next_char():
    source = io.StringIO("Hello")
    my_source = Source(source)

    my_source.get_next_char()
    assert my_source.get_char() == "H"
    assert my_source.get_pos() == (1, 1)

    my_source.get_next_char()
    assert my_source.get_char() == "e"
    assert my_source.get_pos() == (1, 2)

    my_source.get_next_char()
    assert my_source.get_char() == "l"
    assert my_source.get_pos() == (1, 3)

    my_source.get_next_char()
    assert my_source.get_char() == "l"
    assert my_source.get_pos() == (1, 4)

    my_source.get_next_char()
    assert my_source.get_char() == "o"
    assert my_source.get_pos() == (1, 5)

    my_source.get_next_char()
    assert my_source.get_char() == "EOF"
    assert my_source.get_pos() == (1, 6)


def test_empty():
    source = io.StringIO("")
    my_source = Source(source)

    my_source.get_next_char()
    assert my_source.get_char() == "EOF"
    assert my_source.get_pos() == (1, 1)

    my_source.get_next_char()
    assert my_source.get_char() == "EOF"
    assert my_source.get_pos() == (1, 1)


def test_linux_newline():
    source = io.StringIO("Hi\nMe\nHe")
    my_source = Source(source)

    my_source.get_next_char()
    assert my_source.get_char() == "H"
    assert my_source.get_pos() == (1, 1)

    my_source.get_next_char()
    assert my_source.get_char() == "i"
    assert my_source.get_pos() == (1, 2)

    my_source.get_next_char()
    assert my_source.get_char() == "\n"
    assert my_source.get_pos() == (1, 3)

    my_source.get_next_char()
    assert my_source.get_char() == "M"
    assert my_source.get_pos() == (2, 1)

    my_source.get_next_char()
    assert my_source.get_char() == "e"
    assert my_source.get_pos() == (2, 2)

    my_source.get_next_char()
    assert my_source.get_char() == "\n"
    assert my_source.get_pos() == (2, 3)

    my_source.get_next_char()
    assert my_source.get_char() == "H"
    assert my_source.get_pos() == (3, 1)

    my_source.get_next_char()
    assert my_source.get_char() == "e"
    assert my_source.get_pos() == (3, 2)

    my_source.get_next_char()
    assert my_source.get_char() == "EOF"
    assert my_source.get_pos() == (3, 3)

    my_source.get_next_char()
    assert my_source.get_char() == "EOF"
    assert my_source.get_pos() == (3, 3)


def test_windows_newline():
    source = io.StringIO("Hi\r\nMe\r\nHe")
    my_source = Source(source)

    my_source.get_next_char()
    assert my_source.get_char() == "H"
    assert my_source.get_pos() == (1, 1)

    my_source.get_next_char()
    assert my_source.get_char() == "i"
    assert my_source.get_pos() == (1, 2)

    my_source.get_next_char()
    assert my_source.get_char() == "\n"
    assert my_source.get_pos() == (1, 3)

    my_source.get_next_char()
    assert my_source.get_char() == "M"
    assert my_source.get_pos() == (2, 1)

    my_source.get_next_char()
    assert my_source.get_char() == "e"
    assert my_source.get_pos() == (2, 2)

    my_source.get_next_char()
    assert my_source.get_char() == "\n"
    assert my_source.get_pos() == (2, 3)

    my_source.get_next_char()
    assert my_source.get_char() == "H"
    assert my_source.get_pos() == (3, 1)

    my_source.get_next_char()
    assert my_source.get_char() == "e"
    assert my_source.get_pos() == (3, 2)

    my_source.get_next_char()
    assert my_source.get_char() == "EOF"
    assert my_source.get_pos() == (3, 3)

    my_source.get_next_char()
    assert my_source.get_char() == "EOF"
    assert my_source.get_pos() == (3, 3)


def test_just_slash_r():
    source = io.StringIO("Hi\rMe\rHe")
    my_source = Source(source)

    my_source.get_next_char()
    assert my_source.get_char() == "H"
    assert my_source.get_pos() == (1, 1)

    my_source.get_next_char()
    assert my_source.get_char() == "i"
    assert my_source.get_pos() == (1, 2)

    my_source.get_next_char()
    assert my_source.get_char() == "\r"
    assert my_source.get_pos() == (1, 3)

    my_source.get_next_char()
    assert my_source.get_char() == "M"
    assert my_source.get_pos() == (1, 4)

    my_source.get_next_char()
    assert my_source.get_char() == "e"
    assert my_source.get_pos() == (1, 5)

    my_source.get_next_char()
    assert my_source.get_char() == "\r"
    assert my_source.get_pos() == (1, 6)

    my_source.get_next_char()
    assert my_source.get_char() == "H"
    assert my_source.get_pos() == (1, 7)

    my_source.get_next_char()
    assert my_source.get_char() == "e"
    assert my_source.get_pos() == (1, 8)


def test_unix_to_windows():
    source = io.StringIO("Hi\nMe \nH\ne\n\r\nHi")
    my_source = Source(source)

    my_source.get_next_char()
    assert my_source.get_char() == "H"
    assert my_source.get_pos() == (1, 1)

    my_source.get_next_char()
    assert my_source.get_char() == "i"
    assert my_source.get_pos() == (1, 2)

    my_source.get_next_char()
    assert my_source.get_char() == "\n"
    assert my_source.get_pos() == (1, 3)

    my_source.get_next_char()
    assert my_source.get_char() == "M"
    assert my_source.get_pos() == (2, 1)

    my_source.get_next_char()
    assert my_source.get_char() == "e"
    assert my_source.get_pos() == (2, 2)

    my_source.get_next_char()
    assert my_source.get_char() == " "
    assert my_source.get_pos() == (2, 3)

    my_source.get_next_char()
    assert my_source.get_char() == "\n"
    assert my_source.get_pos() == (2, 4)

    my_source.get_next_char()
    assert my_source.get_char() == "H"
    assert my_source.get_pos() == (3, 1)

    my_source.get_next_char()
    assert my_source.get_char() == "\n"
    assert my_source.get_pos() == (3, 2)

    my_source.get_next_char()
    assert my_source.get_char() == "e"
    assert my_source.get_pos() == (4, 1)

    my_source.get_next_char()
    assert my_source.get_char() == "\n"
    assert my_source.get_pos() == (4, 2)

    with pytest.raises(NewLineException):
        my_source.get_next_char()


def test_windows_to_unix():
    source = io.StringIO("Hi\r\nMe \r\nH\r\ne\r\n\nHi")
    my_source = Source(source)

    my_source.get_next_char()
    assert my_source.get_char() == "H"
    assert my_source.get_pos() == (1, 1)

    my_source.get_next_char()
    assert my_source.get_char() == "i"
    assert my_source.get_pos() == (1, 2)

    my_source.get_next_char()
    assert my_source.get_char() == "\n"
    assert my_source.get_pos() == (1, 3)

    my_source.get_next_char()
    assert my_source.get_char() == "M"
    assert my_source.get_pos() == (2, 1)

    my_source.get_next_char()
    assert my_source.get_char() == "e"
    assert my_source.get_pos() == (2, 2)

    my_source.get_next_char()
    assert my_source.get_char() == " "
    assert my_source.get_pos() == (2, 3)

    my_source.get_next_char()
    assert my_source.get_char() == "\n"
    assert my_source.get_pos() == (2, 4)

    my_source.get_next_char()
    assert my_source.get_char() == "H"
    assert my_source.get_pos() == (3, 1)

    my_source.get_next_char()
    assert my_source.get_char() == "\n"
    assert my_source.get_pos() == (3, 2)

    my_source.get_next_char()
    assert my_source.get_char() == "e"
    assert my_source.get_pos() == (4, 1)

    my_source.get_next_char()
    assert my_source.get_char() == "\n"
    assert my_source.get_pos() == (4, 2)

    with pytest.raises(NewLineException):
        my_source.get_next_char()


def test_escaping():
    source = io.StringIO(r'\""\"')
    my_source = Source(source)

    my_source.get_next_char()
    assert my_source.get_char() == "\\"
    my_source.get_next_char()
    assert my_source.get_char() == '"'
    my_source.get_next_char()
    assert my_source.get_char() == '"'
    my_source.get_next_char()
    assert my_source.get_char() == "\\"
    my_source.get_next_char()
    assert my_source.get_char() == '"'
