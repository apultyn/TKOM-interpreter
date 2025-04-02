import io

from src.source import Source


def test_get_next_char():
    source = io.StringIO("Hello")
    my_source = Source(source)

    my_source.get_next_char()
    assert my_source._char == 'H'
    assert my_source._row == 1
    assert my_source._col == 1

    my_source.get_next_char()
    assert my_source._char == 'e'
    assert my_source._row == 1
    assert my_source._col == 2

    my_source.get_next_char()
    assert my_source._char == 'l'
    assert my_source._row == 1
    assert my_source._col == 3

    my_source.get_next_char()
    assert my_source._char == 'l'
    assert my_source._row == 1
    assert my_source._col == 4

    my_source.get_next_char()
    assert my_source._char == 'o'
    assert my_source._row == 1
    assert my_source._col == 5

    my_source.get_next_char()
    assert my_source._char == 'EOF'
    assert my_source._row == 1
    assert my_source._col == 6


def test_get_next_char_empty():
    source = io.StringIO("")
    my_source = Source(source)

    my_source.get_next_char()
    assert my_source._char == 'EOF'
    assert my_source._row == 1
    assert my_source._col == 1

    my_source.get_next_char()
    assert my_source._char == 'EOF'
    assert my_source._row == 1
    assert my_source._col == 1


def test_get_next_char_linux_newline():
    source = io.StringIO("Hi\nMe\nHe")
    my_source = Source(source)

    my_source.get_next_char()
    assert my_source._char == 'H'
    assert my_source._row == 1
    assert my_source._col == 1

    my_source.get_next_char()
    assert my_source._char == 'i'
    assert my_source._row == 1
    assert my_source._col == 2

    my_source.get_next_char()
    assert my_source._char == '\n'
    assert my_source._row == 1
    assert my_source._col == 3

    my_source.get_next_char()
    assert my_source._char == 'M'
    assert my_source._row == 2
    assert my_source._col == 1

    my_source.get_next_char()
    assert my_source._char == 'e'
    assert my_source._row == 2
    assert my_source._col == 2

    my_source.get_next_char()
    assert my_source._char == '\n'
    assert my_source._row == 2
    assert my_source._col == 3

    my_source.get_next_char()
    assert my_source._char == 'H'
    assert my_source._row == 3
    assert my_source._col == 1

    my_source.get_next_char()
    assert my_source._char == 'e'
    assert my_source._row == 3
    assert my_source._col == 2

    my_source.get_next_char()
    assert my_source._char == 'EOF'
    assert my_source._row == 3
    assert my_source._col == 3

    my_source.get_next_char()
    assert my_source._char == 'EOF'
    assert my_source._row == 3
    assert my_source._col == 3


def test_get_next_char_windows_newline():
    source = io.StringIO("Hi\r\nMe\r\nHe")
    my_source = Source(source)

    my_source.get_next_char()
    assert my_source._char == 'H'
    assert my_source._row == 1
    assert my_source._col == 1

    my_source.get_next_char()
    assert my_source._char == 'i'
    assert my_source._row == 1
    assert my_source._col == 2

    my_source.get_next_char()
    assert my_source._char == '\n'
    assert my_source._row == 1
    assert my_source._col == 3

    my_source.get_next_char()
    assert my_source._char == 'M'
    assert my_source._row == 2
    assert my_source._col == 1

    my_source.get_next_char()
    assert my_source._char == 'e'
    assert my_source._row == 2
    assert my_source._col == 2

    my_source.get_next_char()
    assert my_source._char == '\n'
    assert my_source._row == 2
    assert my_source._col == 3

    my_source.get_next_char()
    assert my_source._char == 'H'
    assert my_source._row == 3
    assert my_source._col == 1

    my_source.get_next_char()
    assert my_source._char == 'e'
    assert my_source._row == 3
    assert my_source._col == 2

    my_source.get_next_char()
    assert my_source._char == 'EOF'
    assert my_source._row == 3
    assert my_source._col == 3

    my_source.get_next_char()
    assert my_source._char == 'EOF'
    assert my_source._row == 3
    assert my_source._col == 3


def test_get_next_char_mixed():
    source = io.StringIO("Hi\nMe\r\nHe\n\n\r\nHi")
    my_source = Source(source)

    my_source.get_next_char()
    assert my_source._char == 'H'
    assert my_source._row == 1
    assert my_source._col == 1

    my_source.get_next_char()
    assert my_source._char == 'i'
    assert my_source._row == 1
    assert my_source._col == 2

    my_source.get_next_char()
    assert my_source._char == '\n'
    assert my_source._row == 1
    assert my_source._col == 3

    my_source.get_next_char()
    assert my_source._char == 'M'
    assert my_source._row == 2
    assert my_source._col == 1

    my_source.get_next_char()
    assert my_source._char == 'e'
    assert my_source._row == 2
    assert my_source._col == 2

    my_source.get_next_char()
    assert my_source._char == '\n'
    assert my_source._row == 2
    assert my_source._col == 3

    my_source.get_next_char()
    assert my_source._char == 'H'
    assert my_source._row == 3
    assert my_source._col == 1

    my_source.get_next_char()
    assert my_source._char == 'e'
    assert my_source._row == 3
    assert my_source._col == 2

    my_source.get_next_char()
    assert my_source._char == '\n'
    assert my_source._row == 3
    assert my_source._col == 3

    my_source.get_next_char()
    assert my_source._char == '\n'
    assert my_source._row == 4
    assert my_source._col == 1

    my_source.get_next_char()
    assert my_source._char == '\n'
    assert my_source._row == 5
    assert my_source._col == 1

    my_source.get_next_char()
    assert my_source._char == 'H'
    assert my_source._row == 6
    assert my_source._col == 1

    my_source.get_next_char()
    assert my_source._char == 'i'
    assert my_source._row == 6
    assert my_source._col == 2

    my_source.get_next_char()
    assert my_source._char == 'EOF'
    assert my_source._row == 6
    assert my_source._col == 3

    my_source.get_next_char()
    assert my_source._char == 'EOF'
    assert my_source._row == 6
    assert my_source._col == 3
