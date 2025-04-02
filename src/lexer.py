from source import Source
from token_type import TokenType

KEYWORDS = {
    "if": TokenType.IF_KEYWORD,
    "else": TokenType.ELSE_KEYWORD,
    "function": TokenType.FUNCTION_KEYWORD,
    "return": TokenType.RETURN_KEYWORD,
    "while": TokenType.WHILE_KEYWORD,
    "for": TokenType.FOR_KEYWORD,
    "from": TokenType.FROM_KEYWORD,
    "in": TokenType.IN_KEYWORD,
    "select": TokenType.SELECT_KEYWORD,
    "where": TokenType.WHERE_KEYWORD,
    "order": TokenType.ORDER_KEYWORD,
    "by": TokenType.BY_KEYWORD,
    "descending": TokenType.DESCENDING_KEYWORD,
    "True": TokenType.TRUE_LITERAL,
    "False": TokenType.FALSE_LITERAL,
    "or": TokenType.OR_OPERATOR,
    "and": TokenType.AND_OPERATOR,
}

QUICK_TOKENS = {
    ".": TokenType.DOT_OPERATOR,
    ",": TokenType.COMMA,
    ":": TokenType.COLON,
    ";": TokenType.SEMICOLON,
    "(": TokenType.LEFT_BRACKET,
    ")": TokenType.RIGHT_BRACKET,
    "{": TokenType.LEFT_CURLY_BRACKET,
    "}": TokenType.RIGHT_CURLY_BRACKET,
    "[": TokenType.LEFT_SQUARE_BRACKET,
    "]": TokenType.RIGHT_SQUARE_BRACKET,
}


class Lexer:
    def __init__(self, source):
        self._source = Source(source)

    def get_next_token(self):
        self.skip_whitespaces()

        token = self.build_quick_tokens or True

    def skip_whitespaces(self):
        while not self.get_char().isspace():
            self.get_next_char()

    def build_quick_tokens(self):
        return QUICK_TOKENS.get(self.get_char())

    def get_char(self):
        return self._source.get_char()

    def get_next_char(self):
        return self._source.get_next_char()

    def get_pos(self):
        return self._source.get_pos()
