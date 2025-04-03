import io
import pytest

from src.lexer import Lexer
from src.token_type import TokenType


def test_code_integer():
    source = io.StringIO(
        """
{
    10;
    -50 +-29;
}
"""
    )
    lexer = Lexer(source)

    tokens = lexer.get_token_list()
    types = [t.get_type() for t in tokens]

    assert types == [
        TokenType.LEFT_CURLY_BRACKET,
        TokenType.INT_LITERAL,
        TokenType.SEMICOLON,
        TokenType.MINUS_OPERATOR,
        TokenType.INT_LITERAL,
        TokenType.PLUS_OPERATOR,
        TokenType.MINUS_OPERATOR,
        TokenType.INT_LITERAL,
        TokenType.SEMICOLON,
        TokenType.RIGHT_CURLY_BRACKET,
        TokenType.EOF,
    ]


def test_code_float():
    source = io.StringIO(
        """
{
    1.0;
    -15.38*2.0;
}
"""
    )
    lexer = Lexer(source)

    tokens = lexer.get_token_list()
    types = [t.get_type() for t in tokens]

    assert types == [
        TokenType.LEFT_CURLY_BRACKET,
        TokenType.FLOAT_LITERAL,
        TokenType.SEMICOLON,
        TokenType.MINUS_OPERATOR,
        TokenType.FLOAT_LITERAL,
        TokenType.MUL_OPERATOR,
        TokenType.FLOAT_LITERAL,
        TokenType.SEMICOLON,
        TokenType.RIGHT_CURLY_BRACKET,
        TokenType.EOF,
    ]


def test_string_code():
    source = io.StringIO(
        """
{
    "Hello World!";
    "Typing with quotes: \\"\\" and backslash: \\ there";
}
"""
    )
    lexer = Lexer(source)

    tokens = lexer.get_token_list()
    types = [t.get_type() for t in tokens]

    assert types == [
        TokenType.LEFT_CURLY_BRACKET,
        TokenType.STRING_LITERAL,
        TokenType.SEMICOLON,
        TokenType.STRING_LITERAL,
        TokenType.SEMICOLON,
        TokenType.RIGHT_CURLY_BRACKET,
        TokenType.EOF,
    ]


def test_bool_code():
    source = io.StringIO(
        """
{
    True;
    False;
}
"""
    )
    lexer = Lexer(source)

    tokens = lexer.get_token_list()
    types = [t.get_type() for t in tokens]

    assert types == [
        TokenType.LEFT_CURLY_BRACKET,
        TokenType.TRUE_LITERAL,
        TokenType.SEMICOLON,
        TokenType.FALSE_LITERAL,
        TokenType.SEMICOLON,
        TokenType.RIGHT_CURLY_BRACKET,
        TokenType.EOF,
    ]


def test_list_code():
    source = io.StringIO(
        """
{
    [];
    [1, "Hello", -10.5, ("key": 5),
        ["hello", "from", "sublist"],
        {("name": "dict"), ("value": 5)})
    ];
}
"""
    )
    lexer = Lexer(source)

    tokens = lexer.get_token_list()
    types = [t.get_type() for t in tokens]

    assert types == [
        TokenType.LEFT_CURLY_BRACKET,
        TokenType.LEFT_SQUARE_BRACKET,
        TokenType.RIGHT_SQUARE_BRACKET,
        TokenType.SEMICOLON,
        TokenType.LEFT_SQUARE_BRACKET,
        TokenType.INT_LITERAL,
        TokenType.COMMA,
        TokenType.STRING_LITERAL,
        TokenType.COMMA,
        TokenType.MINUS_OPERATOR,
        TokenType.FLOAT_LITERAL,
        TokenType.COMMA,
        TokenType.LEFT_BRACKET,
        TokenType.STRING_LITERAL,
        TokenType.COLON,
        TokenType.INT_LITERAL,
        TokenType.RIGHT_BRACKET,
        TokenType.COMMA,
        TokenType.LEFT_SQUARE_BRACKET,
        TokenType.STRING_LITERAL,
        TokenType.COMMA,
        TokenType.STRING_LITERAL,
        TokenType.COMMA,
        TokenType.STRING_LITERAL,
        TokenType.RIGHT_SQUARE_BRACKET,
        TokenType.COMMA,
        TokenType.LEFT_CURLY_BRACKET,
        TokenType.LEFT_BRACKET,
        TokenType.STRING_LITERAL,
        TokenType.COLON,
        TokenType.STRING_LITERAL,
        TokenType.RIGHT_BRACKET,
        TokenType.COMMA,
        TokenType.LEFT_BRACKET,
        TokenType.STRING_LITERAL,
        TokenType.COLON,
        TokenType.INT_LITERAL,
        TokenType.RIGHT_BRACKET,
        TokenType.RIGHT_CURLY_BRACKET,
        TokenType.RIGHT_BRACKET,
        TokenType.RIGHT_SQUARE_BRACKET,
        TokenType.SEMICOLON,
        TokenType.RIGHT_CURLY_BRACKET,
        TokenType.EOF,
    ]


def test_dict_code():
    source = io.StringIO(
        """
{
    {};
    {
        ("first_key": 5),
        ("another_key": "value"),
        ("one_more": [1, 5, "hello"]),
        ("last_one": {("key": "value")})
    };
}
"""
    )
    lexer = Lexer(source)

    tokens = lexer.get_token_list()
    types = [t.get_type() for t in tokens]

    assert types == [
        TokenType.LEFT_CURLY_BRACKET,
        TokenType.LEFT_CURLY_BRACKET,
        TokenType.RIGHT_CURLY_BRACKET,
        TokenType.SEMICOLON,
        TokenType.LEFT_CURLY_BRACKET,
        TokenType.LEFT_BRACKET,
        TokenType.STRING_LITERAL,
        TokenType.COLON,
        TokenType.INT_LITERAL,
        TokenType.RIGHT_BRACKET,
        TokenType.COMMA,
        TokenType.LEFT_BRACKET,
        TokenType.STRING_LITERAL,
        TokenType.COLON,
        TokenType.STRING_LITERAL,
        TokenType.RIGHT_BRACKET,
        TokenType.COMMA,
        TokenType.LEFT_BRACKET,
        TokenType.STRING_LITERAL,
        TokenType.COLON,
        TokenType.LEFT_SQUARE_BRACKET,
        TokenType.INT_LITERAL,
        TokenType.COMMA,
        TokenType.INT_LITERAL,
        TokenType.COMMA,
        TokenType.STRING_LITERAL,
        TokenType.RIGHT_SQUARE_BRACKET,
        TokenType.RIGHT_BRACKET,
        TokenType.COMMA,
        TokenType.LEFT_BRACKET,
        TokenType.STRING_LITERAL,
        TokenType.COLON,
        TokenType.LEFT_CURLY_BRACKET,
        TokenType.LEFT_BRACKET,
        TokenType.STRING_LITERAL,
        TokenType.COLON,
        TokenType.STRING_LITERAL,
        TokenType.RIGHT_BRACKET,
        TokenType.RIGHT_CURLY_BRACKET,
        TokenType.RIGHT_BRACKET,
        TokenType.RIGHT_CURLY_BRACKET,
        TokenType.SEMICOLON,
        TokenType.RIGHT_CURLY_BRACKET,
        TokenType.EOF,
    ]


def test_variable_code():
    source = io.StringIO(
        """
{
    a = "Hello there";
    my_list = [1, "Hello", {
        (False: True),
        (-52.48: [1, 2, "Hello"])
    }];
}
"""
    )
    lexer = Lexer(source)

    tokens = lexer.get_token_list()
    types = [t.get_type() for t in tokens]

    assert types == [
        TokenType.LEFT_CURLY_BRACKET,
        TokenType.IDENTIFIER,
        TokenType.ASSIGN_OPERATOR,
        TokenType.STRING_LITERAL,
        TokenType.SEMICOLON,
        TokenType.IDENTIFIER,
        TokenType.ASSIGN_OPERATOR,
        TokenType.LEFT_SQUARE_BRACKET,
        TokenType.INT_LITERAL,
        TokenType.COMMA,
        TokenType.STRING_LITERAL,
        TokenType.COMMA,
        TokenType.LEFT_CURLY_BRACKET,
        TokenType.LEFT_BRACKET,
        TokenType.FALSE_LITERAL,
        TokenType.COLON,
        TokenType.TRUE_LITERAL,
        TokenType.RIGHT_BRACKET,
        TokenType.COMMA,
        TokenType.LEFT_BRACKET,
        TokenType.MINUS_OPERATOR,
        TokenType.FLOAT_LITERAL,
        TokenType.COLON,
        TokenType.LEFT_SQUARE_BRACKET,
        TokenType.INT_LITERAL,
        TokenType.COMMA,
        TokenType.INT_LITERAL,
        TokenType.COMMA,
        TokenType.STRING_LITERAL,
        TokenType.RIGHT_SQUARE_BRACKET,
        TokenType.RIGHT_BRACKET,
        TokenType.RIGHT_CURLY_BRACKET,
        TokenType.RIGHT_SQUARE_BRACKET,
        TokenType.SEMICOLON,
        TokenType.RIGHT_CURLY_BRACKET,
        TokenType.EOF,
    ]


def test_assign_minus_operator():
    source = io.StringIO(
        """
a-=5  a-= 5 a -=5 a -= 5
"""
    )
    lexer = Lexer(source)

    tokens = lexer.get_token_list()
    types = [t.get_type() for t in tokens]

    assert types == [
        TokenType.IDENTIFIER,
        TokenType.ASSIGN_MINUS_OPERATOR,
        TokenType.INT_LITERAL,
        TokenType.IDENTIFIER,
        TokenType.ASSIGN_MINUS_OPERATOR,
        TokenType.INT_LITERAL,
        TokenType.IDENTIFIER,
        TokenType.ASSIGN_MINUS_OPERATOR,
        TokenType.INT_LITERAL,
        TokenType.IDENTIFIER,
        TokenType.ASSIGN_MINUS_OPERATOR,
        TokenType.INT_LITERAL,
        TokenType.EOF,
    ]


def test_assign_operator():
    source = io.StringIO(
        """
a=5  a= 5 a =5 a = 5
"""
    )
    lexer = Lexer(source)

    tokens = lexer.get_token_list()
    types = [t.get_type() for t in tokens]

    assert types == [
        TokenType.IDENTIFIER,
        TokenType.ASSIGN_OPERATOR,
        TokenType.INT_LITERAL,
        TokenType.IDENTIFIER,
        TokenType.ASSIGN_OPERATOR,
        TokenType.INT_LITERAL,
        TokenType.IDENTIFIER,
        TokenType.ASSIGN_OPERATOR,
        TokenType.INT_LITERAL,
        TokenType.IDENTIFIER,
        TokenType.ASSIGN_OPERATOR,
        TokenType.INT_LITERAL,
        TokenType.EOF,
    ]


def test_assign_plus_operator():
    source = io.StringIO(
        """
a+=5  a+= 5 a +=5 a += 5
"""
    )
    lexer = Lexer(source)

    tokens = lexer.get_token_list()
    types = [t.get_type() for t in tokens]

    assert types == [
        TokenType.IDENTIFIER,
        TokenType.ASSIGN_PLUS_OPERATOR,
        TokenType.INT_LITERAL,
        TokenType.IDENTIFIER,
        TokenType.ASSIGN_PLUS_OPERATOR,
        TokenType.INT_LITERAL,
        TokenType.IDENTIFIER,
        TokenType.ASSIGN_PLUS_OPERATOR,
        TokenType.INT_LITERAL,
        TokenType.IDENTIFIER,
        TokenType.ASSIGN_PLUS_OPERATOR,
        TokenType.INT_LITERAL,
        TokenType.EOF,
    ]


def test_or_operator():
    source = io.StringIO(
        """
a or b (a)or(b)
"""
    )
    lexer = Lexer(source)

    tokens = lexer.get_token_list()
    types = [t.get_type() for t in tokens]

    assert types == [
        TokenType.IDENTIFIER,
        TokenType.OR_OPERATOR,
        TokenType.IDENTIFIER,
        TokenType.LEFT_BRACKET,
        TokenType.IDENTIFIER,
        TokenType.RIGHT_BRACKET,
        TokenType.OR_OPERATOR,
        TokenType.LEFT_BRACKET,
        TokenType.IDENTIFIER,
        TokenType.RIGHT_BRACKET,
        TokenType.EOF,
    ]


def test_and_operator():
    source = io.StringIO(
        """
a and b (a)and(b)
"""
    )
    lexer = Lexer(source)

    tokens = lexer.get_token_list()
    types = [t.get_type() for t in tokens]

    assert types == [
        TokenType.IDENTIFIER,
        TokenType.AND_OPERATOR,
        TokenType.IDENTIFIER,
        TokenType.LEFT_BRACKET,
        TokenType.IDENTIFIER,
        TokenType.RIGHT_BRACKET,
        TokenType.AND_OPERATOR,
        TokenType.LEFT_BRACKET,
        TokenType.IDENTIFIER,
        TokenType.RIGHT_BRACKET,
        TokenType.EOF,
    ]


def test_neq_operator():
    source = io.StringIO(
        """
a!=5  a!= 5 a !=5 a != 5
"""
    )
    lexer = Lexer(source)

    tokens = lexer.get_token_list()
    types = [t.get_type() for t in tokens]

    assert types == [
        TokenType.IDENTIFIER,
        TokenType.NEQ_OPERATOR,
        TokenType.INT_LITERAL,
        TokenType.IDENTIFIER,
        TokenType.NEQ_OPERATOR,
        TokenType.INT_LITERAL,
        TokenType.IDENTIFIER,
        TokenType.NEQ_OPERATOR,
        TokenType.INT_LITERAL,
        TokenType.IDENTIFIER,
        TokenType.NEQ_OPERATOR,
        TokenType.INT_LITERAL,
        TokenType.EOF,
    ]


def test_eq_operator():
    source = io.StringIO(
        """
a==5  a== 5 a ==5 a == 5
"""
    )
    lexer = Lexer(source)

    tokens = lexer.get_token_list()
    types = [t.get_type() for t in tokens]

    assert types == [
        TokenType.IDENTIFIER,
        TokenType.EQ_OPERATOR,
        TokenType.INT_LITERAL,
        TokenType.IDENTIFIER,
        TokenType.EQ_OPERATOR,
        TokenType.INT_LITERAL,
        TokenType.IDENTIFIER,
        TokenType.EQ_OPERATOR,
        TokenType.INT_LITERAL,
        TokenType.IDENTIFIER,
        TokenType.EQ_OPERATOR,
        TokenType.INT_LITERAL,
        TokenType.EOF,
    ]


def test_leq_operator():
    source = io.StringIO(
        """
a<=5  a<= 5 a <=5 a <= 5
"""
    )
    lexer = Lexer(source)

    tokens = lexer.get_token_list()
    types = [t.get_type() for t in tokens]

    assert types == [
        TokenType.IDENTIFIER,
        TokenType.LEQ_OPERATOR,
        TokenType.INT_LITERAL,
        TokenType.IDENTIFIER,
        TokenType.LEQ_OPERATOR,
        TokenType.INT_LITERAL,
        TokenType.IDENTIFIER,
        TokenType.LEQ_OPERATOR,
        TokenType.INT_LITERAL,
        TokenType.IDENTIFIER,
        TokenType.LEQ_OPERATOR,
        TokenType.INT_LITERAL,
        TokenType.EOF,
    ]


def test_geq_operator():
    source = io.StringIO(
        """
a>=5  a>= 5 a >=5 a >= 5
"""
    )
    lexer = Lexer(source)

    tokens = lexer.get_token_list()
    types = [t.get_type() for t in tokens]

    assert types == [
        TokenType.IDENTIFIER,
        TokenType.GEQ_OPERATOR,
        TokenType.INT_LITERAL,
        TokenType.IDENTIFIER,
        TokenType.GEQ_OPERATOR,
        TokenType.INT_LITERAL,
        TokenType.IDENTIFIER,
        TokenType.GEQ_OPERATOR,
        TokenType.INT_LITERAL,
        TokenType.IDENTIFIER,
        TokenType.GEQ_OPERATOR,
        TokenType.INT_LITERAL,
        TokenType.EOF,
    ]


def test_less_operator():
    source = io.StringIO(
        """
a<5  a< 5 a <5 a < 5
"""
    )
    lexer = Lexer(source)

    tokens = lexer.get_token_list()
    types = [t.get_type() for t in tokens]

    assert types == [
        TokenType.IDENTIFIER,
        TokenType.LESS_OPERATOR,
        TokenType.INT_LITERAL,
        TokenType.IDENTIFIER,
        TokenType.LESS_OPERATOR,
        TokenType.INT_LITERAL,
        TokenType.IDENTIFIER,
        TokenType.LESS_OPERATOR,
        TokenType.INT_LITERAL,
        TokenType.IDENTIFIER,
        TokenType.LESS_OPERATOR,
        TokenType.INT_LITERAL,
        TokenType.EOF,
    ]


def test_greater_operator():
    source = io.StringIO(
        """
a>5  a> 5 a >5 a > 5
"""
    )
    lexer = Lexer(source)

    tokens = lexer.get_token_list()
    types = [t.get_type() for t in tokens]

    assert types == [
        TokenType.IDENTIFIER,
        TokenType.GREATER_OPERATOR,
        TokenType.INT_LITERAL,
        TokenType.IDENTIFIER,
        TokenType.GREATER_OPERATOR,
        TokenType.INT_LITERAL,
        TokenType.IDENTIFIER,
        TokenType.GREATER_OPERATOR,
        TokenType.INT_LITERAL,
        TokenType.IDENTIFIER,
        TokenType.GREATER_OPERATOR,
        TokenType.INT_LITERAL,
        TokenType.EOF,
    ]


def test_plus_operator():
    source = io.StringIO(
        """
a+5  a+ 5 a +5 a + 5
"""
    )
    lexer = Lexer(source)

    tokens = lexer.get_token_list()
    types = [t.get_type() for t in tokens]

    assert types == [
        TokenType.IDENTIFIER,
        TokenType.PLUS_OPERATOR,
        TokenType.INT_LITERAL,
        TokenType.IDENTIFIER,
        TokenType.PLUS_OPERATOR,
        TokenType.INT_LITERAL,
        TokenType.IDENTIFIER,
        TokenType.PLUS_OPERATOR,
        TokenType.INT_LITERAL,
        TokenType.IDENTIFIER,
        TokenType.PLUS_OPERATOR,
        TokenType.INT_LITERAL,
        TokenType.EOF,
    ]


def test_div_operator():
    source = io.StringIO(
        """
a/5  a/ 5 a /5 a / 5
"""
    )
    lexer = Lexer(source)

    tokens = lexer.get_token_list()
    types = [t.get_type() for t in tokens]

    assert types == [
        TokenType.IDENTIFIER,
        TokenType.DIV_OPERATOR,
        TokenType.INT_LITERAL,
        TokenType.IDENTIFIER,
        TokenType.DIV_OPERATOR,
        TokenType.INT_LITERAL,
        TokenType.IDENTIFIER,
        TokenType.DIV_OPERATOR,
        TokenType.INT_LITERAL,
        TokenType.IDENTIFIER,
        TokenType.DIV_OPERATOR,
        TokenType.INT_LITERAL,
        TokenType.EOF,
    ]


def test_mul_operator():
    source = io.StringIO(
        """
a*5  a* 5 a *5 a * 5
"""
    )
    lexer = Lexer(source)

    tokens = lexer.get_token_list()
    types = [t.get_type() for t in tokens]

    assert types == [
        TokenType.IDENTIFIER,
        TokenType.MUL_OPERATOR,
        TokenType.INT_LITERAL,
        TokenType.IDENTIFIER,
        TokenType.MUL_OPERATOR,
        TokenType.INT_LITERAL,
        TokenType.IDENTIFIER,
        TokenType.MUL_OPERATOR,
        TokenType.INT_LITERAL,
        TokenType.IDENTIFIER,
        TokenType.MUL_OPERATOR,
        TokenType.INT_LITERAL,
        TokenType.EOF,
    ]


def test_log_neg_operator():
    source = io.StringIO(
        """
!a !True ! a ! True
"""
    )
    lexer = Lexer(source)

    tokens = lexer.get_token_list()
    types = [t.get_type() for t in tokens]

    assert types == [
        TokenType.LOGIC_NEG_OPERATOR,
        TokenType.IDENTIFIER,
        TokenType.LOGIC_NEG_OPERATOR,
        TokenType.TRUE_LITERAL,
        TokenType.LOGIC_NEG_OPERATOR,
        TokenType.IDENTIFIER,
        TokenType.LOGIC_NEG_OPERATOR,
        TokenType.TRUE_LITERAL,
        TokenType.EOF,
    ]


def test_dot_operator():
    source = io.StringIO(
        """
a.copy()  [1, 2, 3] .get(). length() "string" . length()
"""
    )
    lexer = Lexer(source)

    tokens = lexer.get_token_list()
    types = [t.get_type() for t in tokens]

    assert types == [
        TokenType.IDENTIFIER,
        TokenType.DOT_OPERATOR,
        TokenType.IDENTIFIER,
        TokenType.LEFT_BRACKET,
        TokenType.RIGHT_BRACKET,
        TokenType.LEFT_SQUARE_BRACKET,
        TokenType.INT_LITERAL,
        TokenType.COMMA,
        TokenType.INT_LITERAL,
        TokenType.COMMA,
        TokenType.INT_LITERAL,
        TokenType.RIGHT_SQUARE_BRACKET,
        TokenType.DOT_OPERATOR,
        TokenType.IDENTIFIER,
        TokenType.LEFT_BRACKET,
        TokenType.RIGHT_BRACKET,
        TokenType.DOT_OPERATOR,
        TokenType.IDENTIFIER,
        TokenType.LEFT_BRACKET,
        TokenType.RIGHT_BRACKET,
        TokenType.STRING_LITERAL,
        TokenType.DOT_OPERATOR,
        TokenType.IDENTIFIER,
        TokenType.LEFT_BRACKET,
        TokenType.RIGHT_BRACKET,
        TokenType.EOF,
    ]


def test_minus_operator():
    source = io.StringIO(
        """
-5 -10.23 50 --- 10; -a.length()
"""
    )
    lexer = Lexer(source)

    tokens = lexer.get_token_list()
    types = [t.get_type() for t in tokens]

    assert types == [
        TokenType.MINUS_OPERATOR,
        TokenType.INT_LITERAL,
        TokenType.MINUS_OPERATOR,
        TokenType.FLOAT_LITERAL,
        TokenType.INT_LITERAL,
        TokenType.MINUS_OPERATOR,
        TokenType.MINUS_OPERATOR,
        TokenType.MINUS_OPERATOR,
        TokenType.INT_LITERAL,
        TokenType.SEMICOLON,
        TokenType.MINUS_OPERATOR,
        TokenType.IDENTIFIER,
        TokenType.DOT_OPERATOR,
        TokenType.IDENTIFIER,
        TokenType.LEFT_BRACKET,
        TokenType.RIGHT_BRACKET,
        TokenType.EOF,
    ]

def test_if_statement():
    source = io.StringIO(
        """
if(a < 4) {
    do_something();
} else if (a > 4) {
    do_something_else();
} else {
    do_something_differently();
}
"""
    )
    lexer = Lexer(source)

    tokens = lexer.get_token_list()
    types = [t.get_type() for t in tokens]

    assert types == [
        TokenType.IF_KEYWORD,
        TokenType.LEFT_BRACKET,
        TokenType.IDENTIFIER,
        TokenType.LESS_OPERATOR,
        TokenType.INT_LITERAL,
        TokenType.RIGHT_BRACKET,
        TokenType.LEFT_CURLY_BRACKET,
        TokenType.IDENTIFIER,
        TokenType.LEFT_BRACKET,
        TokenType.RIGHT_BRACKET,
        TokenType.SEMICOLON,
        TokenType.RIGHT_CURLY_BRACKET,
        TokenType.ELSE_KEYWORD,
        TokenType.IF_KEYWORD,
        TokenType.LEFT_BRACKET,
        TokenType.IDENTIFIER,
        TokenType.GREATER_OPERATOR,
        TokenType.INT_LITERAL,
        TokenType.RIGHT_BRACKET,
        TokenType.LEFT_CURLY_BRACKET,
        TokenType.IDENTIFIER,
        TokenType.LEFT_BRACKET,
        TokenType.RIGHT_BRACKET,
        TokenType.SEMICOLON,
        TokenType.RIGHT_CURLY_BRACKET,
        TokenType.ELSE_KEYWORD,
        TokenType.LEFT_CURLY_BRACKET,
        TokenType.IDENTIFIER,
        TokenType.LEFT_BRACKET,
        TokenType.RIGHT_BRACKET,
        TokenType.SEMICOLON,
        TokenType.RIGHT_CURLY_BRACKET,
        TokenType.EOF
    ]


def test_while_loop():
    source = io.StringIO(
        """
a = 0;
while(a < 10) {
    do_something_ten_times();
    a += 1;
}
"""
    )
    lexer = Lexer(source)

    tokens = lexer.get_token_list()
    types = [t.get_type() for t in tokens]

    assert types == [
        TokenType.IDENTIFIER,
        TokenType.ASSIGN_OPERATOR,
        TokenType.INT_LITERAL,
        TokenType.SEMICOLON,
        TokenType.WHILE_KEYWORD,
        TokenType.LEFT_BRACKET,
        TokenType.IDENTIFIER,
        TokenType.LESS_OPERATOR,
        TokenType.INT_LITERAL,
        TokenType.RIGHT_BRACKET,
        TokenType.LEFT_CURLY_BRACKET,
        TokenType.IDENTIFIER,
        TokenType.LEFT_BRACKET,
        TokenType.RIGHT_BRACKET,
        TokenType.SEMICOLON,
        TokenType.IDENTIFIER,
        TokenType.ASSIGN_PLUS_OPERATOR,
        TokenType.INT_LITERAL,
        TokenType.SEMICOLON,
        TokenType.RIGHT_CURLY_BRACKET,
        TokenType.EOF
    ]