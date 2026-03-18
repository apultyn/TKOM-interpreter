from src.util.source import Source
from src.util.my_token import Token
from src.util.token_type import TokenType
from src.util.error_handler import ErrorHandler
from src.util.pyscript_exceptions import (
    LengthException,
    UnclosedException,
    InvalidValueException,
    TokenException,
)

from src.util.configs import LexerConfig

KEYWORDS = {
    "if": TokenType.IF_KEYWORD,
    "else": TokenType.ELSE_KEYWORD,
    "elif": TokenType.ELIF_KEYWORD,
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

OPERATORS = {
    "!": {
        "=": TokenType.NEQ_OPERATOR,
        "default": TokenType.LOGIC_NEG_OPERATOR,
    },
    "-": {
        "=": TokenType.ASSIGN_MINUS_OPERATOR,
        "default": TokenType.MINUS_OPERATOR,
    },
    "+": {"=": TokenType.ASSIGN_PLUS_OPERATOR, "default": TokenType.PLUS_OPERATOR},
    "=": {"=": TokenType.EQ_OPERATOR, "default": TokenType.ASSIGN_OPERATOR},
    ">": {"=": TokenType.GEQ_OPERATOR, "default": TokenType.GT_OPERATOR},
    "<": {"=": TokenType.LEQ_OPERATOR, "default": TokenType.LT_OPERATOR},
}

ESCAPING_SIGNS = {
    '"': '"',
    "n": "\n",
    "t": "\t",
    "\\": "\\",
}


class Lexer:
    def __init__(
        self,
        *,
        source: Source,
        error_handler: ErrorHandler | None = None,
        config: LexerConfig | None = None,
    ):
        self.source = Source(source)
        self.config = config or LexerConfig()
        self.error_handler = error_handler or ErrorHandler()

    def get_next_token(self):
        self.skip_whitespaces()
        token = (
            self.build_quick_token()
            or self.build_operator()
            or self.build_string_literal()
            or self.build_numeric_literal()
            or self.build_identifier()
        )

        if not token:
            self.error_handler.handle_error(
                TokenException(char=self.get_char(), pos=self.get_pos())
            )

        return token

    def build_quick_token(self):
        token_type = QUICK_TOKENS.get(self.get_char())
        start_pos = self.get_pos()

        if token_type:
            self.get_next_char()
            return Token(token_type, start_pos)
        else:
            return None

    def build_operator(self):
        char = self.get_char()
        start_pos = self.get_pos()
        token_type = None

        if char in OPERATORS:
            next_char = self.get_next_char()
            char_info = OPERATORS[char]
            if next_char in char_info:
                token_type = char_info[next_char]
                self.get_next_char()
            else:
                token_type = char_info["default"]

        if token_type is None and char == "/":
            next_char = self.get_next_char()
            if next_char == "*":
                token_type = self.build_block_comment()
                self.get_next_char()
            elif next_char == "/":
                token_type = self.build_line_comment()
                self.get_next_char()
            else:
                token_type = TokenType.DIV_OPERATOR

        return Token(token_type, start_pos) if token_type else None

    def build_block_comment(self):
        i = 0
        char = self.get_next_char()

        while i <= self.config.max_comment_length:
            if char == "*":
                char = self.get_next_char()
                if char == "/":
                    return TokenType.BLOCK_COMMENT
            elif char == "EOF":
                self.error_handler.handle_error(
                    UnclosedException(construct="Block comment", pos=self.get_pos())
                )
            else:
                char = self.get_next_char()
            i += 1
        else:
            self.error_handler.handle_error(
                LengthException(
                    kind="comment",
                    max_length=self.config.max_comment_length,
                    pos=self.get_prev_pos(),
                )
            )

    def build_line_comment(self):
        i = 0
        while i <= self.config.max_comment_length:
            if self.get_next_char() in ["\n", "EOF"]:
                return TokenType.LINE_COMMENT
            i += 1
        else:
            self.error_handler.handle_error(
                LengthException(
                    kind="comment",
                    max_length=self.config.max_comment_length,
                    pos=self.get_pos(),
                )
            )

    def build_identifier(self):
        start_pos = self.get_pos()
        chars = []
        char = self.get_char()
        i = 0

        while i <= self.config.max_identifier_length:
            if (char.isalnum() or char == "_") and char != "EOF":
                chars.append(char)
                i += 1
                char = self.get_next_char()
            else:
                break
        else:
            self.error_handler.handle_error(
                LengthException(
                    kind="identifier",
                    max_length=self.config.max_identifier_length,
                    pos=self.get_prev_pos(),
                )
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
        if char != '"':
            return None

        start_pos = self.get_pos()
        char = self.get_next_char()
        i = 0
        string_value = []

        while i <= self.config.max_string_literal_length:
            if char == "\\":
                next_char = self.get_next_char()
                if next_char in ESCAPING_SIGNS:
                    string_value.append(ESCAPING_SIGNS.get(next_char))
                else:
                    string_value.append(next_char)
                char = self.get_next_char()
                i += 1
            elif char == '"':
                self.get_next_char()
                break
            elif char == "EOF":
                self.error_handler.handle_error(
                    UnclosedException(construct="String literal", pos=self.get_pos())
                )
            else:
                string_value.append(char)
                char = self.get_next_char()
                i += 1
        else:
            self.error_handler.handle_error(
                LengthException(
                    kind="string literal",
                    max_length=self.config.max_string_literal_length,
                    pos=self.get_prev_pos(),
                )
            )

        return Token(TokenType.STRING_LITERAL, start_pos, "".join(string_value))

    def build_numeric_literal(self):
        char = self.get_char()

        if not char.isdigit():
            return None

        building_float = False
        num_value = 0
        i = 0
        start_pos = self.get_pos()

        if char == "0":
            next_char = self.get_next_char()
            if next_char.isdigit():
                self.error_handler.handle_error(
                    InvalidValueException(
                        msg="Integer can't have anything after starting 0",
                        pos=self.get_prev_pos(),
                    )
                )
            elif next_char == ".":
                building_float = True
                num_value = str(num_value) + "."
                i += 2
                char = self.get_next_char()
            else:
                return Token(TokenType.INT_LITERAL, start_pos, 0)

        while i <= self.config.max_num_literal_length:
            if char.isdigit():
                if building_float:
                    num_value += char
                else:
                    num_value *= 10
                    num_value += int(char)
                char = self.get_next_char()
                i += 1
            elif char == ".":
                if not building_float:
                    building_float = True
                    num_value = str(num_value) + "."
                    i += 1
                    char = self.get_next_char()
                else:
                    self.error_handler.handle_error(
                        InvalidValueException(
                            msg="Float can't have many decimal points",
                            pos=self.get_pos(),
                        )
                    )
            else:
                break
        else:
            self.error_handler.handle_error(
                LengthException(
                    kind="numeric literal",
                    max_length=self.config.max_num_literal_length,
                    pos=self.get_prev_pos(),
                )
            )

        if building_float:
            if num_value[-1:] == ".":
                self.error_handler.handle_error(
                    InvalidValueException(
                        msg="Missing digits after decimal point", pos=self.get_pos()
                    )
                )
            if num_value[-2:] == "00":
                self.error_handler.handle_error(
                    InvalidValueException(
                        msg="Float can't have many zeroes at the end",
                        pos=self.get_prev_pos(),
                    )
                )
            return Token(TokenType.FLOAT_LITERAL, start_pos, float(num_value))
        else:
            return Token(TokenType.INT_LITERAL, start_pos, num_value)

    def skip_whitespaces(self):
        while self.get_char() is None or self.get_char().isspace():
            self.get_next_char()

    def get_char(self):
        return self.source.get_char()

    def get_next_char(self):
        return self.source.get_next_char()

    def get_pos(self):
        return self.source.get_pos()

    def get_prev_pos(self):
        return (self.get_pos()[0], self.get_pos()[1] - 1)
