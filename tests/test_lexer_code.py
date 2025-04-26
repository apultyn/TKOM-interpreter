import io

from tests.util import get_token_list

from src.lexer.lexer import Lexer

from src.util.token_type import TokenType
from src.util.my_token import Token


def test_code_integer():
    source = io.StringIO(
        """{
    10;
    -50 +-29;
}"""
    )
    lexer = Lexer(source)

    tokens = get_token_list(lexer)

    assert tokens == [
        Token(TokenType.LEFT_CURLY_BRACKET, (1, 1)),
        Token(TokenType.INT_LITERAL, (2, 5), 10),
        Token(TokenType.SEMICOLON, (2, 7)),
        Token(TokenType.MINUS_OPERATOR, (3, 5)),
        Token(TokenType.INT_LITERAL, (3, 6), 50),
        Token(TokenType.PLUS_OPERATOR, (3, 9)),
        Token(TokenType.MINUS_OPERATOR, (3, 10)),
        Token(TokenType.INT_LITERAL, (3, 11), 29),
        Token(TokenType.SEMICOLON, (3, 13)),
        Token(TokenType.RIGHT_CURLY_BRACKET, (4, 1)),
        Token(TokenType.EOF, (4, 2)),
    ]


def test_code_float():
    source = io.StringIO(
        """{
    1.0;
    -15.38*2.0;
}"""
    )
    lexer = Lexer(source)

    tokens = get_token_list(lexer)

    assert tokens == [
        Token(TokenType.LEFT_CURLY_BRACKET, (1, 1)),
        Token(TokenType.FLOAT_LITERAL, (2, 5), 1.0),
        Token(TokenType.SEMICOLON, (2, 8)),
        Token(TokenType.MINUS_OPERATOR, (3, 5)),
        Token(TokenType.FLOAT_LITERAL, (3, 6), 15.38),
        Token(TokenType.MUL_OPERATOR, (3, 11)),
        Token(TokenType.FLOAT_LITERAL, (3, 12), 2.0),
        Token(TokenType.SEMICOLON, (3, 15)),
        Token(TokenType.RIGHT_CURLY_BRACKET, (4, 1)),
        Token(TokenType.EOF, (4, 2)),
    ]


def test_string_code():
    source = io.StringIO(
        """{
    "Hello World!";
    "Typing with quotes: \\"\\" and backslash: \\\\ there";
}"""
    )
    lexer = Lexer(source)

    tokens = get_token_list(lexer)

    assert tokens == [
        Token(TokenType.LEFT_CURLY_BRACKET, (1, 1)),
        Token(TokenType.STRING_LITERAL, (2, 5), "Hello World!"),
        Token(TokenType.SEMICOLON, (2, 19)),
        Token(
            TokenType.STRING_LITERAL,
            (3, 5),
            r'Typing with quotes: "" and backslash: \ there',
        ),
        Token(TokenType.SEMICOLON, (3, 55)),
        Token(TokenType.RIGHT_CURLY_BRACKET, (4, 1)),
        Token(TokenType.EOF, (4, 2)),
    ]


def test_bool_code():
    source = io.StringIO(
        """{
    True;
    False;
}"""
    )
    lexer = Lexer(source)

    tokens = get_token_list(lexer)

    assert tokens == [
        Token(TokenType.LEFT_CURLY_BRACKET, (1, 1)),
        Token(TokenType.TRUE_LITERAL, (2, 5)),
        Token(TokenType.SEMICOLON, (2, 9)),
        Token(TokenType.FALSE_LITERAL, (3, 5)),
        Token(TokenType.SEMICOLON, (3, 10)),
        Token(TokenType.RIGHT_CURLY_BRACKET, (4, 1)),
        Token(TokenType.EOF, (4, 2)),
    ]


def test_list_code():
    source = io.StringIO(
        """{
    [];
    [1, "Hello", -10.5, ("key": 5),
        ["hello", "from", "sublist"],
        {("name": "dict"), ("value": 5)})
    ];
}"""
    )
    lexer = Lexer(source)

    tokens = get_token_list(lexer)
    assert tokens == [
        Token(TokenType.LEFT_CURLY_BRACKET, (1, 1)),
        Token(TokenType.LEFT_SQUARE_BRACKET, (2, 5)),
        Token(TokenType.RIGHT_SQUARE_BRACKET, (2, 6)),
        Token(TokenType.SEMICOLON, (2, 7)),
        Token(TokenType.LEFT_SQUARE_BRACKET, (3, 5)),
        Token(TokenType.INT_LITERAL, (3, 6), 1),
        Token(TokenType.COMMA, (3, 7)),
        Token(TokenType.STRING_LITERAL, (3, 9), "Hello"),
        Token(TokenType.COMMA, (3, 16)),
        Token(TokenType.MINUS_OPERATOR, (3, 18)),
        Token(TokenType.FLOAT_LITERAL, (3, 19), 10.5),
        Token(TokenType.COMMA, (3, 23)),
        Token(TokenType.LEFT_BRACKET, (3, 25)),
        Token(TokenType.STRING_LITERAL, (3, 26), "key"),
        Token(TokenType.COLON, (3, 31)),
        Token(TokenType.INT_LITERAL, (3, 33), 5),
        Token(TokenType.RIGHT_BRACKET, (3, 34)),
        Token(TokenType.COMMA, (3, 35)),
        Token(TokenType.LEFT_SQUARE_BRACKET, (4, 9)),
        Token(TokenType.STRING_LITERAL, (4, 10), "hello"),
        Token(TokenType.COMMA, (4, 17)),
        Token(TokenType.STRING_LITERAL, (4, 19), "from"),
        Token(TokenType.COMMA, (4, 25)),
        Token(TokenType.STRING_LITERAL, (4, 27), "sublist"),
        Token(TokenType.RIGHT_SQUARE_BRACKET, (4, 36)),
        Token(TokenType.COMMA, (4, 37)),
        Token(TokenType.LEFT_CURLY_BRACKET, (5, 9)),
        Token(TokenType.LEFT_BRACKET, (5, 10)),
        Token(TokenType.STRING_LITERAL, (5, 11), "name"),
        Token(TokenType.COLON, (5, 17)),
        Token(TokenType.STRING_LITERAL, (5, 19), "dict"),
        Token(TokenType.RIGHT_BRACKET, (5, 25)),
        Token(TokenType.COMMA, (5, 26)),
        Token(TokenType.LEFT_BRACKET, (5, 28)),
        Token(TokenType.STRING_LITERAL, (5, 29), "value"),
        Token(TokenType.COLON, (5, 36)),
        Token(TokenType.INT_LITERAL, (5, 38), 5),
        Token(TokenType.RIGHT_BRACKET, (5, 39)),
        Token(TokenType.RIGHT_CURLY_BRACKET, (5, 40)),
        Token(TokenType.RIGHT_BRACKET, (5, 41)),
        Token(TokenType.RIGHT_SQUARE_BRACKET, (6, 5)),
        Token(TokenType.SEMICOLON, (6, 6)),
        Token(TokenType.RIGHT_CURLY_BRACKET, (7, 1)),
        Token(TokenType.EOF, (7, 2)),
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

    tokens = get_token_list(lexer)
    types = [t.type for t in tokens]

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

    tokens = get_token_list(lexer)
    types = [t.type for t in tokens]

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

    tokens = get_token_list(lexer)
    types = [t.type for t in tokens]

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

    tokens = get_token_list(lexer)
    types = [t.type for t in tokens]

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

    tokens = get_token_list(lexer)
    types = [t.type for t in tokens]

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

    tokens = get_token_list(lexer)
    types = [t.type for t in tokens]

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

    tokens = get_token_list(lexer)
    types = [t.type for t in tokens]

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

    tokens = get_token_list(lexer)
    types = [t.type for t in tokens]

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

    tokens = get_token_list(lexer)
    types = [t.type for t in tokens]

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

    tokens = get_token_list(lexer)
    types = [t.type for t in tokens]

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

    tokens = get_token_list(lexer)
    types = [t.type for t in tokens]

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

    tokens = get_token_list(lexer)
    types = [t.type for t in tokens]

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

    tokens = get_token_list(lexer)
    types = [t.type for t in tokens]

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

    tokens = get_token_list(lexer)
    types = [t.type for t in tokens]

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

    tokens = get_token_list(lexer)
    types = [t.type for t in tokens]

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

    tokens = get_token_list(lexer)
    types = [t.type for t in tokens]

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

    tokens = get_token_list(lexer)
    types = [t.type for t in tokens]

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

    tokens = get_token_list(lexer)
    types = [t.type for t in tokens]

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

    tokens = get_token_list(lexer)
    types = [t.type for t in tokens]

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
} elif (a > 4) {
    do_something_else();
} else {
    do_something_differently();
}
"""
    )
    lexer = Lexer(source)

    tokens = get_token_list(lexer)
    types = [t.type for t in tokens]

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
        TokenType.ELIF_KEYWORD,
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
        TokenType.EOF,
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

    tokens = get_token_list(lexer)
    types = [t.type for t in tokens]

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
        TokenType.EOF,
    ]


def test_for_loop():
    source = io.StringIO(
        """
my_dict = {("first": 1), ("second": 10)};
for element in my_dict {
print(element.key()); // "first" "second"
}

"""
    )
    lexer = Lexer(source)

    tokens = get_token_list(lexer)
    types = [t.type for t in tokens]

    assert types == [
        TokenType.IDENTIFIER,
        TokenType.ASSIGN_OPERATOR,
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
        TokenType.INT_LITERAL,
        TokenType.RIGHT_BRACKET,
        TokenType.RIGHT_CURLY_BRACKET,
        TokenType.SEMICOLON,
        TokenType.FOR_KEYWORD,
        TokenType.IDENTIFIER,
        TokenType.IN_KEYWORD,
        TokenType.IDENTIFIER,
        TokenType.LEFT_CURLY_BRACKET,
        TokenType.IDENTIFIER,
        TokenType.LEFT_BRACKET,
        TokenType.IDENTIFIER,
        TokenType.DOT_OPERATOR,
        TokenType.IDENTIFIER,
        TokenType.LEFT_BRACKET,
        TokenType.RIGHT_BRACKET,
        TokenType.RIGHT_BRACKET,
        TokenType.SEMICOLON,
        TokenType.LINE_COMMENT,
        TokenType.RIGHT_CURLY_BRACKET,
        TokenType.EOF,
    ]


def test_function_definition():
    source = io.StringIO(
        """
my_func = function(arg1, arg2) {
    return arg1 + arg2;
}
print(my_func(5, 10)); // 15
"""
    )
    lexer = Lexer(source)

    tokens = get_token_list(lexer)
    types = [t.type for t in tokens]

    assert types == [
        TokenType.IDENTIFIER,
        TokenType.ASSIGN_OPERATOR,
        TokenType.FUNCTION_KEYWORD,
        TokenType.LEFT_BRACKET,
        TokenType.IDENTIFIER,
        TokenType.COMMA,
        TokenType.IDENTIFIER,
        TokenType.RIGHT_BRACKET,
        TokenType.LEFT_CURLY_BRACKET,
        TokenType.RETURN_KEYWORD,
        TokenType.IDENTIFIER,
        TokenType.PLUS_OPERATOR,
        TokenType.IDENTIFIER,
        TokenType.SEMICOLON,
        TokenType.RIGHT_CURLY_BRACKET,
        TokenType.IDENTIFIER,
        TokenType.LEFT_BRACKET,
        TokenType.IDENTIFIER,
        TokenType.LEFT_BRACKET,
        TokenType.INT_LITERAL,
        TokenType.COMMA,
        TokenType.INT_LITERAL,
        TokenType.RIGHT_BRACKET,
        TokenType.RIGHT_BRACKET,
        TokenType.SEMICOLON,
        TokenType.LINE_COMMENT,
        TokenType.EOF,
    ]


def test_function_passing():
    source = io.StringIO(
        """
passed_func = function(a, b) {
    return a + b;
}
another_function = function(func, a) {
    return func(a, 5);
}
print(another_function(passed_func, 10));
// 15

"""
    )
    lexer = Lexer(source)

    tokens = get_token_list(lexer)
    types = [t.type for t in tokens]

    assert types == [
        TokenType.IDENTIFIER,
        TokenType.ASSIGN_OPERATOR,
        TokenType.FUNCTION_KEYWORD,
        TokenType.LEFT_BRACKET,
        TokenType.IDENTIFIER,
        TokenType.COMMA,
        TokenType.IDENTIFIER,
        TokenType.RIGHT_BRACKET,
        TokenType.LEFT_CURLY_BRACKET,
        TokenType.RETURN_KEYWORD,
        TokenType.IDENTIFIER,
        TokenType.PLUS_OPERATOR,
        TokenType.IDENTIFIER,
        TokenType.SEMICOLON,
        TokenType.RIGHT_CURLY_BRACKET,
        TokenType.IDENTIFIER,
        TokenType.ASSIGN_OPERATOR,
        TokenType.FUNCTION_KEYWORD,
        TokenType.LEFT_BRACKET,
        TokenType.IDENTIFIER,
        TokenType.COMMA,
        TokenType.IDENTIFIER,
        TokenType.RIGHT_BRACKET,
        TokenType.LEFT_CURLY_BRACKET,
        TokenType.RETURN_KEYWORD,
        TokenType.IDENTIFIER,
        TokenType.LEFT_BRACKET,
        TokenType.IDENTIFIER,
        TokenType.COMMA,
        TokenType.INT_LITERAL,
        TokenType.RIGHT_BRACKET,
        TokenType.SEMICOLON,
        TokenType.RIGHT_CURLY_BRACKET,
        TokenType.IDENTIFIER,
        TokenType.LEFT_BRACKET,
        TokenType.IDENTIFIER,
        TokenType.LEFT_BRACKET,
        TokenType.IDENTIFIER,
        TokenType.COMMA,
        TokenType.INT_LITERAL,
        TokenType.RIGHT_BRACKET,
        TokenType.RIGHT_BRACKET,
        TokenType.SEMICOLON,
        TokenType.LINE_COMMENT,
        TokenType.EOF,
    ]


def test_line_comment():
    source = io.StringIO(
        """
//My first comment //
//Comment with /* block comment */
//Comment with =<>5# operators
//Comment with 7.5 4.2; "string"
"""
    )
    lexer = Lexer(source)

    tokens = get_token_list(lexer)
    types = [t.type for t in tokens]

    assert types == [
        TokenType.LINE_COMMENT,
        TokenType.LINE_COMMENT,
        TokenType.LINE_COMMENT,
        TokenType.LINE_COMMENT,
        TokenType.EOF,
    ]


def test_block_comment():
    source = io.StringIO(
        """
/*Random Block Comment */a=5;
/*Block comment with line //*/b="hello";
/*Multiline
Comment*/select;
a = (arg1,/*Comment*/arg2);
"""
    )
    lexer = Lexer(source)

    tokens = get_token_list(lexer)
    types = [t.type for t in tokens]

    assert types == [
        TokenType.BLOCK_COMMENT,
        TokenType.IDENTIFIER,
        TokenType.ASSIGN_OPERATOR,
        TokenType.INT_LITERAL,
        TokenType.SEMICOLON,
        TokenType.BLOCK_COMMENT,
        TokenType.IDENTIFIER,
        TokenType.ASSIGN_OPERATOR,
        TokenType.STRING_LITERAL,
        TokenType.SEMICOLON,
        TokenType.BLOCK_COMMENT,
        TokenType.SELECT_KEYWORD,
        TokenType.SEMICOLON,
        TokenType.IDENTIFIER,
        TokenType.ASSIGN_OPERATOR,
        TokenType.LEFT_BRACKET,
        TokenType.IDENTIFIER,
        TokenType.COMMA,
        TokenType.BLOCK_COMMENT,
        TokenType.IDENTIFIER,
        TokenType.RIGHT_BRACKET,
        TokenType.SEMICOLON,
        TokenType.EOF,
    ]


def test_linq_queries():
    source = io.StringIO(
        """
my_dict = {
("Warszawa", 2000000),
("Tokio", 37000000),
("Delhi", 30000000),
("Szczecinek", 40000),
("Buenos Aires", 15000000)
}
small_cities=from city in my_dict
select city.key(),city.value()/1000
where city.value()<5000000
order by city.key()descending;
// small_cities = [["Warszawa", 2000], ["Szczecinek", 40]]
"""
    )
    lexer = Lexer(source)

    tokens = get_token_list(lexer)
    types = [t.type for t in tokens]

    assert types == [
        TokenType.IDENTIFIER,
        TokenType.ASSIGN_OPERATOR,
        TokenType.LEFT_CURLY_BRACKET,
        TokenType.LEFT_BRACKET,
        TokenType.STRING_LITERAL,
        TokenType.COMMA,
        TokenType.INT_LITERAL,
        TokenType.RIGHT_BRACKET,
        TokenType.COMMA,
        TokenType.LEFT_BRACKET,
        TokenType.STRING_LITERAL,
        TokenType.COMMA,
        TokenType.INT_LITERAL,
        TokenType.RIGHT_BRACKET,
        TokenType.COMMA,
        TokenType.LEFT_BRACKET,
        TokenType.STRING_LITERAL,
        TokenType.COMMA,
        TokenType.INT_LITERAL,
        TokenType.RIGHT_BRACKET,
        TokenType.COMMA,
        TokenType.LEFT_BRACKET,
        TokenType.STRING_LITERAL,
        TokenType.COMMA,
        TokenType.INT_LITERAL,
        TokenType.RIGHT_BRACKET,
        TokenType.COMMA,
        TokenType.LEFT_BRACKET,
        TokenType.STRING_LITERAL,
        TokenType.COMMA,
        TokenType.INT_LITERAL,
        TokenType.RIGHT_BRACKET,
        TokenType.RIGHT_CURLY_BRACKET,
        TokenType.IDENTIFIER,
        TokenType.ASSIGN_OPERATOR,
        TokenType.FROM_KEYWORD,
        TokenType.IDENTIFIER,
        TokenType.IN_KEYWORD,
        TokenType.IDENTIFIER,
        TokenType.SELECT_KEYWORD,
        TokenType.IDENTIFIER,
        TokenType.DOT_OPERATOR,
        TokenType.IDENTIFIER,
        TokenType.LEFT_BRACKET,
        TokenType.RIGHT_BRACKET,
        TokenType.COMMA,
        TokenType.IDENTIFIER,
        TokenType.DOT_OPERATOR,
        TokenType.IDENTIFIER,
        TokenType.LEFT_BRACKET,
        TokenType.RIGHT_BRACKET,
        TokenType.DIV_OPERATOR,
        TokenType.INT_LITERAL,
        TokenType.WHERE_KEYWORD,
        TokenType.IDENTIFIER,
        TokenType.DOT_OPERATOR,
        TokenType.IDENTIFIER,
        TokenType.LEFT_BRACKET,
        TokenType.RIGHT_BRACKET,
        TokenType.LESS_OPERATOR,
        TokenType.INT_LITERAL,
        TokenType.ORDER_KEYWORD,
        TokenType.BY_KEYWORD,
        TokenType.IDENTIFIER,
        TokenType.DOT_OPERATOR,
        TokenType.IDENTIFIER,
        TokenType.LEFT_BRACKET,
        TokenType.RIGHT_BRACKET,
        TokenType.DESCENDING_KEYWORD,
        TokenType.SEMICOLON,
        TokenType.LINE_COMMENT,
        TokenType.EOF,
    ]


def test_all_with_pos():
    source = io.StringIO(
        """/*komentarz blokowy*///komentarz liniowy

function myFunc(a,b){
    while(a!=b){
        a+=1;
        b-=1;
        if(a==b and a<=10 or b>=0){
            return Dict(("key1":1),("key2":2.5));}elif (typeOf(a)!="Int"){return [a*b/2];}
            else {
            return "done";}}
    for i in myList{i =-i;
    }
}

myList = [1,0.07,3,2.01,0.1];
myList.add(4);
another=42.0;
flag=True;
message="Text with \\"escaping\\"";message2="Another";
value =(3.14 + 2) * (5 - 1);
result = -value;
notFlag = !flag;
from item in myList
select item
where item != 2
order by item descending;"""
    )
    lexer = Lexer(source)

    tokens = get_token_list(lexer)

    assert tokens == [
        Token(TokenType.BLOCK_COMMENT, (1, 1)),
        Token(TokenType.LINE_COMMENT, (1, 22)),
        Token(TokenType.FUNCTION_KEYWORD, (3, 1)),
        Token(TokenType.IDENTIFIER, (3, 10), "myFunc"),
        Token(TokenType.LEFT_BRACKET, (3, 16)),
        Token(TokenType.IDENTIFIER, (3, 17), "a"),
        Token(TokenType.COMMA, (3, 18)),
        Token(TokenType.IDENTIFIER, (3, 19), "b"),
        Token(TokenType.RIGHT_BRACKET, (3, 20)),
        Token(TokenType.LEFT_CURLY_BRACKET, (3, 21)),
        Token(TokenType.WHILE_KEYWORD, (4, 5)),
        Token(TokenType.LEFT_BRACKET, (4, 10)),
        Token(TokenType.IDENTIFIER, (4, 11), "a"),
        Token(TokenType.NEQ_OPERATOR, (4, 12)),
        Token(TokenType.IDENTIFIER, (4, 14), "b"),
        Token(TokenType.RIGHT_BRACKET, (4, 15)),
        Token(TokenType.LEFT_CURLY_BRACKET, (4, 16)),
        Token(TokenType.IDENTIFIER, (5, 9), "a"),
        Token(TokenType.ASSIGN_PLUS_OPERATOR, (5, 10)),
        Token(TokenType.INT_LITERAL, (5, 12), 1),
        Token(TokenType.SEMICOLON, (5, 13)),
        Token(TokenType.IDENTIFIER, (6, 9), "b"),
        Token(TokenType.ASSIGN_MINUS_OPERATOR, (6, 10)),
        Token(TokenType.INT_LITERAL, (6, 12), 1),
        Token(TokenType.SEMICOLON, (6, 13)),
        Token(TokenType.IF_KEYWORD, (7, 9)),
        Token(TokenType.LEFT_BRACKET, (7, 11)),
        Token(TokenType.IDENTIFIER, (7, 12), "a"),
        Token(TokenType.EQ_OPERATOR, (7, 13)),
        Token(TokenType.IDENTIFIER, (7, 15), "b"),
        Token(TokenType.AND_OPERATOR, (7, 17)),
        Token(TokenType.IDENTIFIER, (7, 21), "a"),
        Token(TokenType.LEQ_OPERATOR, (7, 22)),
        Token(TokenType.INT_LITERAL, (7, 24), 10),
        Token(TokenType.OR_OPERATOR, (7, 27)),
        Token(TokenType.IDENTIFIER, (7, 30), "b"),
        Token(TokenType.GEQ_OPERATOR, (7, 31)),
        Token(TokenType.INT_LITERAL, (7, 33), 0),
        Token(TokenType.RIGHT_BRACKET, (7, 34)),
        Token(TokenType.LEFT_CURLY_BRACKET, (7, 35)),
        Token(TokenType.RETURN_KEYWORD, (8, 13)),
        Token(TokenType.IDENTIFIER, (8, 20), "Dict"),
        Token(TokenType.LEFT_BRACKET, (8, 24)),
        Token(TokenType.LEFT_BRACKET, (8, 25)),
        Token(TokenType.STRING_LITERAL, (8, 26), "key1"),
        Token(TokenType.COLON, (8, 32)),
        Token(TokenType.INT_LITERAL, (8, 33), 1),
        Token(TokenType.RIGHT_BRACKET, (8, 34)),
        Token(TokenType.COMMA, (8, 35)),
        Token(TokenType.LEFT_BRACKET, (8, 36)),
        Token(TokenType.STRING_LITERAL, (8, 37), "key2"),
        Token(TokenType.COLON, (8, 43)),
        Token(TokenType.FLOAT_LITERAL, (8, 44), 2.5),
        Token(TokenType.RIGHT_BRACKET, (8, 47)),
        Token(TokenType.RIGHT_BRACKET, (8, 48)),
        Token(TokenType.SEMICOLON, (8, 49)),
        Token(TokenType.RIGHT_CURLY_BRACKET, (8, 50)),
        Token(TokenType.ELIF_KEYWORD, (8, 51)),
        Token(TokenType.LEFT_BRACKET, (8, 56)),
        Token(TokenType.IDENTIFIER, (8, 57), "typeOf"),
        Token(TokenType.LEFT_BRACKET, (8, 63)),
        Token(TokenType.IDENTIFIER, (8, 64), "a"),
        Token(TokenType.RIGHT_BRACKET, (8, 65)),
        Token(TokenType.NEQ_OPERATOR, (8, 66)),
        Token(TokenType.STRING_LITERAL, (8, 68), "Int"),
        Token(TokenType.RIGHT_BRACKET, (8, 73)),
        Token(TokenType.LEFT_CURLY_BRACKET, (8, 74)),
        Token(TokenType.RETURN_KEYWORD, (8, 75)),
        Token(TokenType.LEFT_SQUARE_BRACKET, (8, 82)),
        Token(TokenType.IDENTIFIER, (8, 83), "a"),
        Token(TokenType.MUL_OPERATOR, (8, 84)),
        Token(TokenType.IDENTIFIER, (8, 85), "b"),
        Token(TokenType.DIV_OPERATOR, (8, 86)),
        Token(TokenType.INT_LITERAL, (8, 87), 2),
        Token(TokenType.RIGHT_SQUARE_BRACKET, (8, 88)),
        Token(TokenType.SEMICOLON, (8, 89)),
        Token(TokenType.RIGHT_CURLY_BRACKET, (8, 90)),
        Token(TokenType.ELSE_KEYWORD, (9, 13)),
        Token(TokenType.LEFT_CURLY_BRACKET, (9, 18)),
        Token(TokenType.RETURN_KEYWORD, (10, 13)),
        Token(TokenType.STRING_LITERAL, (10, 20), "done"),
        Token(TokenType.SEMICOLON, (10, 26)),
        Token(TokenType.RIGHT_CURLY_BRACKET, (10, 27)),
        Token(TokenType.RIGHT_CURLY_BRACKET, (10, 28)),
        Token(TokenType.FOR_KEYWORD, (11, 5)),
        Token(TokenType.IDENTIFIER, (11, 9), "i"),
        Token(TokenType.IN_KEYWORD, (11, 11)),
        Token(TokenType.IDENTIFIER, (11, 14), "myList"),
        Token(TokenType.LEFT_CURLY_BRACKET, (11, 20)),
        Token(TokenType.IDENTIFIER, (11, 21), "i"),
        Token(TokenType.ASSIGN_OPERATOR, (11, 23)),
        Token(TokenType.MINUS_OPERATOR, (11, 24)),
        Token(TokenType.IDENTIFIER, (11, 25), "i"),
        Token(TokenType.SEMICOLON, (11, 26)),
        Token(TokenType.RIGHT_CURLY_BRACKET, (12, 5)),
        Token(TokenType.RIGHT_CURLY_BRACKET, (13, 1)),
        Token(TokenType.IDENTIFIER, (15, 1), "myList"),
        Token(TokenType.ASSIGN_OPERATOR, (15, 8)),
        Token(TokenType.LEFT_SQUARE_BRACKET, (15, 10)),
        Token(TokenType.INT_LITERAL, (15, 11), 1),
        Token(TokenType.COMMA, (15, 12)),
        Token(TokenType.FLOAT_LITERAL, (15, 13), 0.07),
        Token(TokenType.COMMA, (15, 17)),
        Token(TokenType.INT_LITERAL, (15, 18), 3),
        Token(TokenType.COMMA, (15, 19)),
        Token(TokenType.FLOAT_LITERAL, (15, 20), 2.01),
        Token(TokenType.COMMA, (15, 24)),
        Token(TokenType.FLOAT_LITERAL, (15, 25), 0.1),
        Token(TokenType.RIGHT_SQUARE_BRACKET, (15, 28)),
        Token(TokenType.SEMICOLON, (15, 29)),
        Token(TokenType.IDENTIFIER, (16, 1), "myList"),
        Token(TokenType.DOT_OPERATOR, (16, 7)),
        Token(TokenType.IDENTIFIER, (16, 8), "add"),
        Token(TokenType.LEFT_BRACKET, (16, 11)),
        Token(TokenType.INT_LITERAL, (16, 12), 4),
        Token(TokenType.RIGHT_BRACKET, (16, 13)),
        Token(TokenType.SEMICOLON, (16, 14)),
        Token(TokenType.IDENTIFIER, (17, 1), "another"),
        Token(TokenType.ASSIGN_OPERATOR, (17, 8)),
        Token(TokenType.FLOAT_LITERAL, (17, 9), 42.0),
        Token(TokenType.SEMICOLON, (17, 13)),
        Token(TokenType.IDENTIFIER, (18, 1), "flag"),
        Token(TokenType.ASSIGN_OPERATOR, (18, 5)),
        Token(TokenType.TRUE_LITERAL, (18, 6)),
        Token(TokenType.SEMICOLON, (18, 10)),
        Token(TokenType.IDENTIFIER, (19, 1), "message"),
        Token(TokenType.ASSIGN_OPERATOR, (19, 8)),
        Token(TokenType.STRING_LITERAL, (19, 9), 'Text with "escaping"'),
        Token(TokenType.SEMICOLON, (19, 33)),
        Token(TokenType.IDENTIFIER, (19, 34), "message2"),
        Token(TokenType.ASSIGN_OPERATOR, (19, 42)),
        Token(TokenType.STRING_LITERAL, (19, 43), "Another"),
        Token(TokenType.SEMICOLON, (19, 52)),
        Token(TokenType.IDENTIFIER, (20, 1), "value"),
        Token(TokenType.ASSIGN_OPERATOR, (20, 7)),
        Token(TokenType.LEFT_BRACKET, (20, 8)),
        Token(TokenType.FLOAT_LITERAL, (20, 9), 3.14),
        Token(TokenType.PLUS_OPERATOR, (20, 14)),
        Token(TokenType.INT_LITERAL, (20, 16), 2),
        Token(TokenType.RIGHT_BRACKET, (20, 17)),
        Token(TokenType.MUL_OPERATOR, (20, 19)),
        Token(TokenType.LEFT_BRACKET, (20, 21)),
        Token(TokenType.INT_LITERAL, (20, 22), 5),
        Token(TokenType.MINUS_OPERATOR, (20, 24)),
        Token(TokenType.INT_LITERAL, (20, 26), 1),
        Token(TokenType.RIGHT_BRACKET, (20, 27)),
        Token(TokenType.SEMICOLON, (20, 28)),
        Token(TokenType.IDENTIFIER, (21, 1), "result"),
        Token(TokenType.ASSIGN_OPERATOR, (21, 8)),
        Token(TokenType.MINUS_OPERATOR, (21, 10)),
        Token(TokenType.IDENTIFIER, (21, 11), "value"),
        Token(TokenType.SEMICOLON, (21, 16)),
        Token(TokenType.IDENTIFIER, (22, 1), "notFlag"),
        Token(TokenType.ASSIGN_OPERATOR, (22, 9)),
        Token(TokenType.LOGIC_NEG_OPERATOR, (22, 11)),
        Token(TokenType.IDENTIFIER, (22, 12), "flag"),
        Token(TokenType.SEMICOLON, (22, 16)),
        Token(TokenType.FROM_KEYWORD, (23, 1)),
        Token(TokenType.IDENTIFIER, (23, 6), "item"),
        Token(TokenType.IN_KEYWORD, (23, 11)),
        Token(TokenType.IDENTIFIER, (23, 14), "myList"),
        Token(TokenType.SELECT_KEYWORD, (24, 1)),
        Token(TokenType.IDENTIFIER, (24, 8), "item"),
        Token(TokenType.WHERE_KEYWORD, (25, 1)),
        Token(TokenType.IDENTIFIER, (25, 7), "item"),
        Token(TokenType.NEQ_OPERATOR, (25, 12)),
        Token(TokenType.INT_LITERAL, (25, 15), 2),
        Token(TokenType.ORDER_KEYWORD, (26, 1)),
        Token(TokenType.BY_KEYWORD, (26, 7)),
        Token(TokenType.IDENTIFIER, (26, 10), "item"),
        Token(TokenType.DESCENDING_KEYWORD, (26, 15)),
        Token(TokenType.SEMICOLON, (26, 25)),
        Token(TokenType.EOF, (26, 26)),
    ]
