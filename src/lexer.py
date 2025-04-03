from .source import Source
from .my_token import Token
from .token_type import TokenType
from .pyscript_exceptions import LengthException, CommentException
from .lexer_config import LexerConfig

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
    "*": TokenType.MUL_OPERATOR,
    "(": TokenType.LEFT_BRACKET,
    ")": TokenType.RIGHT_BRACKET,
    "{": TokenType.LEFT_CURLY_BRACKET,
    "}": TokenType.RIGHT_CURLY_BRACKET,
    "[": TokenType.LEFT_SQUARE_BRACKET,
    "]": TokenType.RIGHT_SQUARE_BRACKET,
    "EOF": TokenType.EOF,
}


class Lexer:
    def __init__(self, source: Source, config: LexerConfig = LexerConfig()):
        self._source = Source(source)
        self._config = config

    def get_next_token(self):
        self.skip_whitespaces()
        token = (
            self.build_quick_tokens()
            or self.build_operators()
            or self.build_identifier()
            or self.build_string_literal()
            or self.build_integer_literal()
        )

        return token

    def build_quick_tokens(self):
        token_type = QUICK_TOKENS.get(self.get_char())
        start_pos = self.get_pos()

        if token_type:
            self.get_next_char()
            return Token(token_type, start_pos)
        else:
            return None

    def build_operators(self):
        char = self.get_char()
        start_pos = self.get_pos()
        token_type = None

        if char == "!":
            if self.get_next_char() == "=":
                token_type = TokenType.NEQ_OPERATOR
                self.get_next_char()
            else:
                token_type = TokenType.LOGIC_NEG_OPERATOR
        elif char == "-":
            if self.get_next_char() == "=":
                token_type = TokenType.ASSIGN_MINUS_OPERATOR
                self.get_next_char()
            else:
                token_type = TokenType.MINUS_OPERATOR
        elif char == "/":
            next_char = self.get_next_char()

            # Block Comment
            if next_char == "*":
                token_type = TokenType.BLOCK_COMMENT
                i = 0
                char = self.get_next_char()

                while i <= self._config.max_comment_length:
                    if char == "*":
                        if char := self.get_next_char() == "/":
                            self.get_next_char()
                            break
                        else:
                            i += 1
                    elif char == "EOF":
                        raise CommentException(f"Comment not closed", self.get_pos())
                    else:
                        i += 1
                        char = self.get_next_char()
                else:
                    raise LengthException(
                        f"Maximum comment length ({self._config.max_comment_length}) exceeded",
                        self.get_pos(),
                    )

            # Line comment
            elif next_char == "/":
                token_type = TokenType.LINE_COMMENT
                i = 0
                while i <= self._config.max_comment_length:
                    if self.get_next_char() == "\n":
                        self.get_next_char()
                        break
                    i += 1
                else:
                    raise LengthException(
                        f"Maximum comment length ({self._config.max_comment_length}) exceeded",
                        self.get_pos(),
                    )
            else:
                token_type = TokenType.DIV_OPERATOR
                self.get_next_char()
        elif char == "+":
            if self.get_next_char() == "=":
                token_type = TokenType.ASSIGN_PLUS_OPERATOR
                self.get_next_char()
            else:
                token_type = TokenType.ADD_OPERATOR
        elif char == "=":
            if self.get_next_char() == "=":
                token_type = TokenType.EQ_OPERATOR
                self.get_next_char()
            else:
                token_type = TokenType.ASSIGN_OPERATOR
        elif char == ">":
            if self.get_next_char() == "=":
                token_type = TokenType.GEQ_OPERATOR
                self.get_next_char()
            else:
                token_type = TokenType.GREATER_OPERATOR
        elif char == "<":
            if self.get_next_char() == "=":
                token_type = TokenType.LEQ_OPERATOR
                self.get_next_char()
            else:
                token_type = TokenType.LESS_OPERATOR
        return Token(token_type, start_pos) if token_type else None

    def build_identifier(self):
        start_pos = self.get_pos()
        chars = []
        char = self.get_char()
        i = 0

        while i <= self._config.max_identifier_length:
            if (char.isalpha() or char == "_") and char != "EOF":
                chars.append(char)
                i += 1
                char = self.get_next_char()
            else:
                break
        else:
            raise LengthException(
                f"Maximum identifier length ({self._config.max_identifier_length}) exceeded",
                self.get_pos(),
            )

        if len(chars) == 0:
            return None

        identifier = "".join(chars)
        if identifier in KEYWORDS:
            return Token(KEYWORDS[identifier], start_pos)
        else:
            return Token(TokenType.IDENTIFIER, start_pos, identifier)

    def build_string_literal(self):
        char = self.get_char()
        start_pos = self.get_pos()
        if char != '"':
            return None

        prev_char = '"'
        char = self.get_next_char()
        i = 0
        value = []

        while char != '"' or prev_char == "\\":
            if i == self._config.max_string_literal_length:
                raise LengthException(
                    f"Maximum string literal length ({self._config.max_string_literal_length}) exceeded",
                    self.get_pos(),
                )
            value.append(char)
            prev_char = char
            char = self.get_next_char()
            i += 1

        return Token(TokenType.STRING_LITERAL, start_pos, "".join(value))

    def build_integer_literal(self):
        pass

    def skip_whitespaces(self):
        while self.get_char() is None or self.get_char().isspace():
            self.get_next_char()

    def get_char(self):
        return self._source.get_char()

    def get_next_char(self):
        return self._source.get_next_char()

    def get_pos(self):
        return self._source.get_pos()
