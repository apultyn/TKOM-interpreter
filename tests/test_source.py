import io

from src.source import Source


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


def test_get_next_char_empty():
    source = io.StringIO("")
    my_source = Source(source)

    my_source.get_next_char()
    assert my_source.get_char() == "EOF"
    assert my_source.get_pos() == (1, 1)

    my_source.get_next_char()
    assert my_source.get_char() == "EOF"
    assert my_source.get_pos() == (1, 1)


def test_get_next_char_linux_newline():
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


def test_get_next_char_windows_newline():
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


def test_get_next_char_mixed():
    source = io.StringIO("Hi\nMe\r\nHe\n\n\r\nHi")
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
    assert my_source.get_char() == "\n"
    assert my_source.get_pos() == (3, 3)

    my_source.get_next_char()
    assert my_source.get_char() == "\n"
    assert my_source.get_pos() == (4, 1)

    my_source.get_next_char()
    assert my_source.get_char() == "\n"
    assert my_source.get_pos() == (5, 1)

    my_source.get_next_char()
    assert my_source.get_char() == "H"
    assert my_source.get_pos() == (6, 1)

    my_source.get_next_char()
    assert my_source.get_char() == "i"
    assert my_source.get_pos() == (6, 2)

    my_source.get_next_char()
    assert my_source.get_char() == "EOF"
    assert my_source.get_pos() == (6, 3)

    my_source.get_next_char()
    assert my_source.get_char() == "EOF"
    assert my_source.get_pos() == (6, 3)
