import io

from src.source import Source


def test_get_next_char():
    source = io.StringIO("Hello")
    my_source = Source(source)

    my_source.get_next_char()
    assert my_source._char == 'H'

    my_source.get_next_char()
    assert my_source._char == 'e'

    my_source.get_next_char()
    assert my_source._char == 'l'

    my_source.get_next_char()
    assert my_source._char == 'l'

    my_source.get_next_char()
    assert my_source._char == 'o'

    my_source.get_next_char()
    assert my_source._char == 'EOF'
