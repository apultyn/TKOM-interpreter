from collections.abc import Callable

from src.lexer.lexer import Lexer
from src.util.token_type import TokenType
from src.util.error_handler import ErrorHandler
from src.util.pyscript_exceptions import SyntaxException

import src.parser.parser_objects as po
import src.parser.parser_util as pu


class Parser:
    def __init__(self, *, lexer: Lexer, error_handler: ErrorHandler = ErrorHandler()):
        self.lexer = lexer
        self.current_token = None
        self.error_handler = error_handler
        self.current_token = self.get_next_token()

    def get_next_token(self):
        self.current_token = self.lexer.get_next_token()

        while self.current_token.type in [
            TokenType.BLOCK_COMMENT,
            TokenType.LINE_COMMENT,
        ]:
            self.current_token = self.lexer.get_next_token()
        return self.current_token

    def must_be(self, token_type: TokenType, msg: str):
        token = self.current_token
        if token.type != token_type:
            self.error_handler.handle_error(
                SyntaxException(msg=msg, pos=self.current_token.pos)
            )
        self.get_next_token()
        return token

    def must_be_created(self, parser_object, msg):
        if not parser_object:
            self.error_handler.handle_error(
                SyntaxException(msg=msg, pos=self.current_token.pos)
            )
        return parser_object

    def might_be(self, token_type: TokenType):
        token = self.current_token
        if token.type == token_type:
            self.get_next_token()
            return token
        return None

    def might_be_in(self, token_type_list: list[TokenType]):
        token = self.current_token
        if token.type in token_type_list:
            self.get_next_token()
            return token
        return None

    def binary_operation_builder(
        self, subrule: Callable[[], po.Expression], *tokens: TokenType
    ):
        expr = subrule()
        while found_token := self.might_be_in(tokens):
            right = subrule()
            expr = po.BinaryExpr(
                expr,
                pu.match_binary_operation(found_token.type),
                right,
                pos=found_token.pos,
            )
        return expr

    def parse_list(
        self,
        element_function: Callable[[], po.ParserObject],
        separator: TokenType,
        expected_item: str,
    ):
        items = []
        first_item = element_function()
        if first_item:
            items.append(first_item)

            while self.might_be(separator):
                next_item = self.must_be_created(
                    element_function(), f"{expected_item} expected"
                )
                items.append(next_item)
        return items

    # program = { statement }, "EOF" ;
    def parse_program(self):
        statements = []
        while self.current_token.type != TokenType.EOF:
            statement = self.must_be_created(
                self.parse_statement(), "Statement expected"
            )
            statements.append(statement)
        return po.Program(statements, pos=(1, 1))

    # statement = { ( stmt_with_ident, ";" )
    #                   | if_statement}
    #                   | while_loop
    #                   | for_loop
    #                   | ( return_statement, ";" )
    #                   | block
    def parse_statement(self):
        return (
            self.parse_stmt_with_ident()
            or self.parse_if_statement()
            or self.parse_while_loop()
            or self.parse_for_loop()
            or self.parse_return_statement()
            or self.parse_block()
        )

    # stmt_with_ident = identifier, ( assignment | call_stmt ) ;
    def parse_stmt_with_ident(self):
        token = self.might_be(TokenType.IDENTIFIER)
        if not token:
            return None

        identifier = po.Identifier(token.value, pos=token.pos)
        statement = self.must_be_created(
            self.parse_assignment(identifier) or self.parse_call_stmt(identifier),
            "Assignment or function call expected",
        )

        self.must_be(TokenType.SEMICOLON, "';' expected")

        return statement

    # assignment = ( "=" | "+=" | "-=" ),  expression ;
    def parse_assignment(self, identifier: po.Identifier):
        assign_token = self.might_be_in(
            (
                TokenType.ASSIGN_OPERATOR,
                TokenType.ASSIGN_PLUS_OPERATOR,
                TokenType.ASSIGN_MINUS_OPERATOR,
            )
        )

        if not assign_token:
            return None
        assignment_type = pu.match_assignment_type(assign_token.type)

        expression = self.must_be_created(
            self.parse_expression(), "Expression expected"
        )

        return po.AssignmentStmt(
            identifier, assignment_type, expression, pos=assign_token.pos
        )

    # call_stmt = { access_suff | call_suff }, call_suff ;
    def parse_call_stmt(self, first_ident: po.Expression):
        expr = first_ident

        while (
            new_expr := (self.parse_access_suff(expr) or self.parse_call_suff(expr))
        ) is not None:
            expr = new_expr

        if not isinstance(expr, po.CallExpr):
            return None
        return expr

    # access_suff = ".", identifier ;
    def parse_access_suff(self, source: po.Expression):
        if not (dot_operator := self.might_be(TokenType.DOT_OPERATOR)):
            return None

        ident_token = self.must_be(TokenType.IDENTIFIER, "Identifier expected")
        identifier = po.Identifier(ident_token.value, pos=ident_token.pos)

        return po.AccessExpr(source, identifier, pos=dot_operator.pos)

    # call_suff = "(", [ expression, { ",", expression } ], ")" ;
    def parse_call_suff(self, source: po.Expression):
        if not (left_bracket := self.might_be(TokenType.LEFT_BRACKET)):
            return None

        arguments = self.parse_list(
            self.parse_expression, TokenType.COMMA, "Expression"
        )

        self.must_be(TokenType.RIGHT_BRACKET, "')' expected")

        return po.CallExpr(source, arguments, pos=left_bracket.pos)

    # if_statement = "if", "(", expression, ")", block, { elif }, [ "else", block ] ;
    def parse_if_statement(self):
        if not (if_keyword := self.might_be(TokenType.IF_KEYWORD)):
            return None

        self.must_be(TokenType.LEFT_BRACKET, "'(' expected")
        condition = self.must_be_created(self.parse_expression(), "Expression expected")

        self.must_be(TokenType.RIGHT_BRACKET, "')' expected")

        body = self.must_be_created(self.parse_block(), "Body expected")

        elif_statements = []
        while elif_stmt := self.parse_elif():
            elif_statements.append(elif_stmt)

        else_body = None
        if self.might_be(TokenType.ELSE_KEYWORD):
            else_body = self.parse_block()

        return po.IfStmt(
            condition, body, elif_statements, else_body, pos=if_keyword.pos
        )

    # elif = "elif", "(", expression, ")", block ;
    def parse_elif(self):
        if not (elif_keyword := self.might_be(TokenType.ELIF_KEYWORD)):
            return None

        self.must_be(TokenType.LEFT_BRACKET, "'(' expected")

        condition = self.must_be_created(self.parse_expression(), "Expression expected")

        self.must_be(TokenType.RIGHT_BRACKET, "')' expected")

        body = self.must_be_created(self.parse_block(), "Body expected")

        return po.ElifStmt(condition, body, pos=elif_keyword.pos)

    # while_loop = "while", "(", expression, ")", block ;
    def parse_while_loop(self):
        if not (while_keyword := self.might_be(TokenType.WHILE_KEYWORD)):
            return None

        self.must_be(TokenType.LEFT_BRACKET, "'(' expected")

        condition = self.must_be_created(self.parse_expression(), "Expression expected")

        self.must_be(TokenType.RIGHT_BRACKET, "')' expected")

        body = self.must_be_created(self.parse_block(), "Body expected")

        return po.WhileStmt(condition, body, pos=while_keyword.pos)

    # for_loop = "for", identifier, "in", expression, block ;
    def parse_for_loop(self):
        if not (for_keyword := self.might_be(TokenType.FOR_KEYWORD)):
            return None

        token = self.must_be(TokenType.IDENTIFIER, "Identifier expected")
        var = po.Identifier(token.value, pos=token.pos)

        self.must_be(TokenType.IN_KEYWORD, "'in' keyword expected")

        source = self.must_be_created(self.parse_expression(), "Expression expected")
        body = self.must_be_created(self.parse_block(), "Body expected")

        return po.ForStmt(var, source, body, pos=for_keyword.pos)

    # return_statement = "return", [ expression ], ";" ;
    def parse_return_statement(self):
        if not (return_keyword := self.might_be(TokenType.RETURN_KEYWORD)):
            return None

        value = self.parse_expression()

        self.must_be(TokenType.SEMICOLON, "';' expected")

        return po.ReturnStmt(value, pos=return_keyword.pos)

    # block	= "{", { statement }, "}" ;
    def parse_block(self):
        if not (left_curly := self.might_be(TokenType.LEFT_CURLY_BRACKET)):
            return None

        statements = []
        while statement := self.parse_statement():
            statements.append(statement)

        self.must_be(TokenType.RIGHT_CURLY_BRACKET, "'}' or statement expected")

        return po.Block(statements, pos=left_curly.pos)

    # expression = logic_or ;
    def parse_expression(self):
        return self.parse_logic_or()

    # logic_or = logic_and, { "or", logic_and } ;
    def parse_logic_or(self):
        return self.binary_operation_builder(
            self.parse_logic_and, TokenType.OR_OPERATOR
        )

    # logic_and	= comparison, { "and", comparison } ;
    def parse_logic_and(self):
        return self.binary_operation_builder(
            self.parse_comparison, TokenType.AND_OPERATOR
        )

    # comparison = additive, { ("==" | "!=" | ">" | ">=" | "<" | "<="), additive } ;
    def parse_comparison(self):
        return self.binary_operation_builder(
            self.parse_additive,
            TokenType.EQ_OPERATOR,
            TokenType.NEQ_OPERATOR,
            TokenType.GT_OPERATOR,
            TokenType.GEQ_OPERATOR,
            TokenType.LT_OPERATOR,
            TokenType.LEQ_OPERATOR,
        )

    # additive = multiplicative, { ("+" | "-"), multiplicative } ;
    def parse_additive(self):
        return self.binary_operation_builder(
            self.parse_multiplicative, TokenType.PLUS_OPERATOR, TokenType.MINUS_OPERATOR
        )

    # multiplicative = unary, { ( "*" | "/" ), unary } ;
    def parse_multiplicative(self):
        return self.binary_operation_builder(
            self.parse_unary, TokenType.MUL_OPERATOR, TokenType.DIV_OPERATOR
        )

    # unary	= { ("!" | "-") }, postfix ;
    def parse_unary(self):
        prefixes: list[TokenType] = []
        while found_token := self.might_be_in(
            [TokenType.LOGIC_NEG_OPERATOR, TokenType.MINUS_OPERATOR]
        ):
            prefixes.append(found_token)

        expr = self.parse_postfix()

        for token in reversed(prefixes):
            expr = po.NegationExpr(
                pu.match_negation_type(token.type), expr, pos=token.pos
            )
        return expr

    # postfix = primary, { call_suff | member_suff} ;
    def parse_postfix(self):
        expr = self.parse_primary()
        if not expr:
            return None

        while new_expr := (self.parse_access_suff(expr) or self.parse_call_suff(expr)):
            expr = new_expr

        return expr

    # primary = integer
    # 				| float
    # 				| string
    # 				| "True" | "False"
    # 				| identifier
    # 				| list_literal
    # 				| dict_literal
    #               | func_literal
    # 				| linq_query
    # 				| item_literal_or_parenthesis
    def parse_primary(self):
        token = self.current_token

        mapping = {
            TokenType.INT_LITERAL: po.SimpleExpr(
                pu.SimpleExprType.INT, token.value, pos=token.pos
            ),
            TokenType.FLOAT_LITERAL: po.SimpleExpr(
                pu.SimpleExprType.FLOAT, token.value, pos=token.pos
            ),
            TokenType.STRING_LITERAL: po.SimpleExpr(
                pu.SimpleExprType.STRING, token.value, pos=token.pos
            ),
            TokenType.TRUE_LITERAL: po.SimpleExpr(
                pu.SimpleExprType.BOOL, True, pos=token.pos
            ),
            TokenType.FALSE_LITERAL: po.SimpleExpr(
                pu.SimpleExprType.BOOL, False, pos=token.pos
            ),
            TokenType.IDENTIFIER: po.Identifier(token.value, pos=token.pos),
        }

        if simple_type := mapping.get(token.type, None):
            self.get_next_token()
            return simple_type

        return (
            self.parse_list_literal()
            or self.parse_func_literal()
            or self.parse_dict_literal()
            or self.parse_linq_query()
            or self.parse_item_literal_or_parenthesis()
        )

    # list_literal = "[", [ expression, { ",", expression } ] "]" ;
    def parse_list_literal(self):
        if not (left_square := self.might_be(TokenType.LEFT_SQUARE_BRACKET)):
            return None

        elements = self.parse_list(self.parse_expression, TokenType.COMMA, "Expression")

        self.must_be(TokenType.RIGHT_SQUARE_BRACKET, "']' expected")

        return po.ListExpr(elements, pos=left_square.pos)

    # dict_literal = "{", [ item_literal, { ",", item_literal } ], "}" ;
    def parse_dict_literal(self):
        if not (left_curly := self.might_be(TokenType.LEFT_CURLY_BRACKET)):
            return None

        items = self.parse_list(
            self.parse_item_literal, TokenType.COMMA, "Item literal"
        )

        self.must_be(TokenType.RIGHT_CURLY_BRACKET, "'}' expected")

        return po.DictExpr(items, pos=left_curly.pos)

    # func_literal = "function", "(", [ identifier, { ",", identifier } ] ")", block ;
    def parse_func_literal(self):
        if not (func_keyword := self.might_be(TokenType.FUNCTION_KEYWORD)):
            return None

        self.must_be(TokenType.LEFT_BRACKET, "'(' expected")

        identifier_list = []
        if first_token := self.might_be(TokenType.IDENTIFIER):
            identifier_list.append(
                po.Identifier(first_token.value, pos=first_token.pos)
            )

            while self.might_be(TokenType.COMMA):
                next_token = self.must_be(TokenType.IDENTIFIER, "Identifier expected")
                identifier_list.append(
                    po.Identifier(next_token.value, pos=next_token.pos)
                )

        self.must_be(TokenType.RIGHT_BRACKET, "')' expected")

        body = self.must_be_created(self.parse_block(), "Body expected")

        return po.FunctionExpr(identifier_list, body, pos=func_keyword.pos)

    # linq_query = "from", identifier, "in", expression,
    # 				    "select", expression, { ",", expression }
    # 				    [ "where", expression ],
    # 				    [ "order", "by", expression, [ "descending" ] ] ;
    def parse_linq_query(self):
        if not (from_keyword := self.might_be(TokenType.FROM_KEYWORD)):
            return None

        identifier_token = self.must_be(TokenType.IDENTIFIER, "Identifier expected")
        var = po.Identifier(identifier_token.value, pos=identifier_token.pos)

        self.must_be(TokenType.IN_KEYWORD, "'in' keyword expected")
        source = self.must_be_created(self.parse_expression(), "Expression expected")
        self.must_be(TokenType.SELECT_KEYWORD, "'select' keyword expected")

        selects = [self.must_be_created(self.parse_expression(), "Expression expected")]
        while self.might_be(TokenType.COMMA):
            selects.append(
                self.must_be_created(self.parse_expression(), "Expression expected")
            )

        where = None
        if self.might_be(TokenType.WHERE_KEYWORD):
            where = self.must_be_created(self.parse_expression(), "Expression expected")

        order_by = None
        descending = False
        if self.might_be(TokenType.ORDER_KEYWORD):
            self.must_be(TokenType.BY_KEYWORD, "'by' keyword expected")
            order_by = self.must_be_created(
                self.parse_expression(), "Expression expected"
            )
            if self.might_be(TokenType.DESCENDING_KEYWORD):
                descending = True

        return po.LinqExpr(
            var, source, selects, where, order_by, descending, pos=from_keyword.pos
        )

    # item_literal_or_parenthesis = "(", expression, ( item_literal_tail | right_parenthesis ) ;
    def parse_item_literal_or_parenthesis(self):
        if not (left_bracket := self.might_be(TokenType.LEFT_BRACKET)):
            return None

        first_expression = self.must_be_created(
            self.parse_expression(), "Expression expected"
        )

        if item_literal := self.parse_item_literal_tail(first_expression, left_bracket):
            return item_literal

        self.must_be(TokenType.RIGHT_BRACKET, "')' expected")

        return po.BracketsExpr(first_expression, pos=left_bracket.pos)

    # item_literal = "(", expression, item_literal_tail ;
    def parse_item_literal(self):
        if not (left_bracket := self.might_be(TokenType.LEFT_BRACKET)):
            return None

        first_expression = self.must_be_created(
            self.parse_expression(), "Expression expected"
        )

        return self.must_be_created(
            self.parse_item_literal_tail(first_expression, left_bracket), "':' expected"
        )

    # item_literal_tail = ":", expression, ")" ;
    def parse_item_literal_tail(self, first_expression, left_bracket):
        if not self.might_be(TokenType.COLON):
            return None

        value = self.must_be_created(self.parse_expression(), "Expression expected")

        self.must_be(TokenType.RIGHT_BRACKET, "')' expected")

        return po.ItemExpr(first_expression, value, pos=left_bracket.pos)
