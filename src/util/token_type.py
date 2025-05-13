from enum import Enum, auto


class TokenType(Enum):
    # Operators
    ASSIGN_MINUS_OPERATOR = auto()
    ASSIGN_PLUS_OPERATOR = auto()
    ASSIGN_OPERATOR = auto()
    OR_OPERATOR = auto()
    AND_OPERATOR = auto()
    NEQ_OPERATOR = auto()
    EQ_OPERATOR = auto()
    LEQ_OPERATOR = auto()
    LT_OPERATOR = auto()
    GEQ_OPERATOR = auto()
    GT_OPERATOR = auto()
    PLUS_OPERATOR = auto()
    DIV_OPERATOR = auto()
    MUL_OPERATOR = auto()
    LOGIC_NEG_OPERATOR = auto()
    DOT_OPERATOR = auto()

    # Many purpose operators
    MINUS_OPERATOR = auto()

    # Literals or with values
    INT_LITERAL = auto()
    FLOAT_LITERAL = auto()
    STRING_LITERAL = auto()
    TRUE_LITERAL = auto()
    FALSE_LITERAL = auto()
    IDENTIFIER = auto()

    # Keywords
    IF_KEYWORD = auto()
    ELSE_KEYWORD = auto()
    ELIF_KEYWORD = auto()
    FUNCTION_KEYWORD = auto()
    RETURN_KEYWORD = auto()
    WHILE_KEYWORD = auto()
    FOR_KEYWORD = auto()
    FROM_KEYWORD = auto()
    IN_KEYWORD = auto()
    SELECT_KEYWORD = auto()
    WHERE_KEYWORD = auto()
    ORDER_KEYWORD = auto()
    BY_KEYWORD = auto()
    DESCENDING_KEYWORD = auto()

    # Reserved chars
    LEFT_BRACKET = auto()
    RIGHT_BRACKET = auto()
    LEFT_CURLY_BRACKET = auto()
    RIGHT_CURLY_BRACKET = auto()
    LEFT_SQUARE_BRACKET = auto()
    RIGHT_SQUARE_BRACKET = auto()
    SEMICOLON = auto()
    LINE_COMMENT = auto()
    BLOCK_COMMENT = auto()
    COMMA = auto()
    COLON = auto()
    EOF = auto()

    def __str__(self) -> str:
        return self.name
