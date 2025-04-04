from .source import Source
from .my_token import Token
from .token_type import TokenType
from .pyscript_exceptions import (
    LengthException,
    UnclosedException,
    InvalidValueException,
    SyntaxException,
)
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

    def get_token_list(self):
        tokens = []
        token = self.get_next_token()

        while token.get_type() != TokenType.EOF:
            tokens.append(token)
            token = self.get_next_token()

        tokens.append(token)
        return tokens

    def get_next_token(self):
        self.skip_whitespaces()
        token = (
            self.build_quick_tokens()
            or self.build_operators()
            or self.build_string_literal()
            or self.build_numeric_literal()
            or self.build_identifier()
        )

        if not token:
            raise SyntaxException("Unknown token", self.get_pos())

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
                        raise UnclosedException(f"Comment not closed", self.get_pos())
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
        elif char == "+":
            if self.get_next_char() == "=":
                token_type = TokenType.ASSIGN_PLUS_OPERATOR
                self.get_next_char()
            else:
                token_type = TokenType.PLUS_OPERATOR
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
            if (char.isalnum() or char == "_") and char != "EOF":
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
        if char != '"':
            return None

        start_pos = self.get_pos()
        char = self.get_next_char()
        prev_char = ""
        i = 0
        string_value = []

        while i <= self._config.max_string_literal_length:
            if char == "\\":
                next_char = self.get_next_char()
                if next_char == '"':
                    string_value.append('"')
                elif next_char == "n":
                    string_value.append("\n")
                elif next_char == "t":
                    string_value.append("\t")
                elif next_char == "\\":
                    string_value.append("\\")
                else:
                    string_value.append(next_char)
                char = self.get_next_char()
                i += 1
            elif char == '"' and prev_char != "\\":
                self.get_next_char()
                break
            elif char == "EOF":
                raise UnclosedException("String literal unclosed", self.get_pos())
            else:
                string_value.append(char)
                prev_char = char
                char = self.get_next_char()
                i += 1
        else:
            raise LengthException(
                f"Maximum string literal length ({self._config.max_string_literal_length}) exceeded",
                self.get_pos(),
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
                raise InvalidValueException(
                    "Integer can't have anything after starting 0", self.get_pos()
                )
            elif next_char == ".":
                building_float = True
                num_value = str(num_value) + "."
                i += 2
                char = self.get_next_char()
            else:
                return Token(TokenType.INT_LITERAL, start_pos, 0)

        while i <= self._config.max_num_literal_length:
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
                    raise InvalidValueException(
                        "Float can't have many decimal points", self.get_pos()
                    )
            else:
                break
        else:
            raise LengthException(
                f"Maximum int literal length ({self._config.max_num_literal_length}) exceeded",
                self.get_pos(),
            )

        if building_float:
            if num_value[-1:] == ".":
                raise InvalidValueException(
                    "Missing digits after decimal point", self.get_pos()
                )
            if num_value[-2:] == "00":
                raise InvalidValueException(
                    "Float can't have many zeroes at the end", self.get_pos()
                )
            return Token(TokenType.FLOAT_LITERAL, start_pos, float(num_value))
        else:
            return Token(TokenType.INT_LITERAL, start_pos, num_value)

    def skip_whitespaces(self):
        while self.get_char() is None or self.get_char().isspace():
            self.get_next_char()

    def get_char(self):
        return self._source.get_char()

    def get_next_char(self):
        return self._source.get_next_char()

    def get_pos(self):
        return self._source.get_pos()
