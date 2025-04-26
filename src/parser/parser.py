from lexer import Lexer
from src.util.token_type import TokenType
from src.util.error_handler import ErrorHandler
from src.util.pyscript_exceptions import PyscriptException

import parser_objects as po
import parser_util as pu


class Parser:
    def __init__(self, lexer: Lexer, error_handler: ErrorHandler):
        self.lexer = lexer
        self.current_token = None
        self.error_handler = error_handler
        self.current_token = self.get_next_token()

    def get_next_token(self):
        try:
            self.current_token = self.lexer.get_next_token()
        except PyscriptException as e:
            self.error_handler.handle_error(e)

        while self.current_token.type in [
            TokenType.BLOCK_COMMENT,
            TokenType.LINE_COMMENT,
        ]:
            self.current_token = self.lexer.get_next_token()
        return self.current_token

    def must_be(self, token_type: TokenType, exception: PyscriptException):
        token = self.current_token
        if token.type != token_type:
            raise exception
        self.get_next_token()
        return token

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

    # program = { statement }, "EOF" ;
    def parse_program(self):
        statements = []
        while self.current_token.type != TokenType.EOF:
            statement = self.parse_statement()
            if not statement:
                raise PyscriptException()
            statements.append(statement)
        return po.Program(statements)

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
        token = self.must_be(TokenType.IDENTIFIER, PyscriptException())
        identifier = po.Identifier(token)

        statement = self.parse_assignment(identifier) or self.parse_call_stmt(
            identifier
        )
        if not statement:
            raise PyscriptException()

        self.must_be(TokenType.SEMICOLON, PyscriptException())

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
        assignment_type = pu.match_assignment_type(assign_token)

        expression = self.parse_expression()
        if not expression:
            raise PyscriptException()

        return po.AssignmentStmt(identifier, assignment_type, expression)

    # call_stmt = { access_suff | call_suff }, call_suff ;
    def parse_call_stmt(self, first_ident: po.Expression):
        expr = first_ident

        while (
            new_expr := self.parse_access_suff(expr) or self.parse_call_suff(expr)
        ) is not None:
            expr = new_expr

        if new_expr := self.parse_call_suff(expr) is None:
            raise PyscriptException()
        return new_expr

    # access_suff = ".", identifier ;
    def parse_access_suff(self, source: po.Expression):
        if self.might_be(TokenType.DOT_OPERATOR) is None:
            return None

        ident_token = self.must_be(TokenType.IDENTIFIER, PyscriptException())
        identifier = po.Identifier(ident_token)

        return po.AccessExpr(source, identifier)

    # call_suff = "(", [ argument_list ], ")" ;
    def parse_call_suff(self, source: po.Expression):
        if self.might_be(TokenType.LEFT_PARENTHESIS) is None:
            return None

        arguments = self.parse_argument_list()

        self.must_be(TokenType.RIGHT_PARENTHESIS, PyscriptException())

        return po.CallExpr(source, arguments)

    # if_statement = "if", "(", expression, ")", block, { else_if }, [ "else", block ] ;
    def parse_if_statement(self):
        if self.might_be(TokenType.IF_KEYWORD) is None:
            return None

        self.must_be(TokenType.LEFT_PARENTHESIS, PyscriptException())
        condition = self.parse_expression()
        if not condition:
            raise PyscriptException()

        self.must_be(TokenType.RIGHT_PARENTHESIS, PyscriptException())

        body = self.parse_block()
        if not body:
            raise PyscriptException()

        else_if_statements = []
        while else_if := self.parse_else_if():
            else_if_statements.append(else_if)

        else_body = None
        if self.might_be(TokenType.ELSE_KEYWORD):
            else_body = self.parse_block()

        return po.IfStmt(condition, body, else_if_statements, else_body)


    def parse_argument_list(self):
        pass
