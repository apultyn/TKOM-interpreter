from lexer import Lexer
from src.util.token_type import TokenType
from src.util.error_handler import ErrorHandler
from src.util.pyscript_exceptions import SyntaxException

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
        except SyntaxException as e:
            self.error_handler.handle_error(e)

        while self.current_token.type in [
            TokenType.BLOCK_COMMENT,
            TokenType.LINE_COMMENT,
        ]:
            self.current_token = self.lexer.get_next_token()
        return self.current_token

    def must_be(self, token_type: TokenType, msg: str):
        token = self.current_token
        if token.type != token_type:
            raise SyntaxException(self.current_token.pos, msg)
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

    def binary_operation_builder(self, subrule: function, *tokens: TokenType):
        expr = subrule()
        while found_token := self.might_be_in(tokens):
            right = subrule()
            expr = po.BinaryExpr(expr, pu.match_binary_operation(found_token.type), right)
        return expr

    # program = { statement }, "EOF" ;
    def parse_program(self):
        statements = []
        while self.current_token.type != TokenType.EOF:
            statement = self.parse_statement()
            if not statement:
                raise SyntaxException()
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
        token = self.might_be(TokenType.IDENTIFIER)
        if not token:
            return None

        identifier = po.Identifier(token)
        statement = self.parse_assignment(identifier) or self.parse_call_stmt(
            identifier
        )
        if not statement:
            raise SyntaxException()

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

        expression = self.parse_expression()
        if not expression:
            raise SyntaxException()

        return po.AssignmentStmt(identifier, assignment_type, expression)

    # call_stmt = { access_suff | call_suff }, call_suff ;
    def parse_call_stmt(self, first_ident: po.Expression):
        expr = first_ident

        while (
            new_expr := (self.parse_access_suff(expr) or self.parse_call_suff(expr))
        ) is not None:
            expr = new_expr

        if new_expr := self.parse_call_suff(expr) is None:
            raise SyntaxException()
        return new_expr

    # access_suff = ".", identifier ;
    def parse_access_suff(self, source: po.Expression):
        if not self.might_be(TokenType.DOT_OPERATOR):
            return None

        ident_token = self.must_be(TokenType.IDENTIFIER, "Identifier expected")
        identifier = po.Identifier(ident_token)

        return po.AccessExpr(source, identifier)

    # call_suff = "(", [ argument_list ], ")" ;
    def parse_call_suff(self, source: po.Expression):
        if not self.might_be(TokenType.LEFT_BRACKET):
            return None

        arguments = self.parse_argument_list()

        self.must_be(TokenType.RIGHT_BRACKET, "')' expected")

        return po.CallExpr(source, arguments)

    # if_statement = "if", "(", expression, ")", block, { elif }, [ "else", block ] ;
    def parse_if_statement(self):
        if not self.might_be(TokenType.IF_KEYWORD):
            return None

        self.must_be(TokenType.LEFT_BRACKET, "'(' expected")
        condition = self.parse_expression()
        if not condition:
            raise SyntaxException()

        self.must_be(TokenType.RIGHT_BRACKET, "')' expected")

        body = self.parse_block()
        if not body:
            raise SyntaxException()

        elif_statements = []
        while elif_stmt := self.parse_elif():
            elif_statements.append(elif_stmt)

        else_body = None
        if self.might_be(TokenType.ELSE_KEYWORD):
            else_body = self.parse_block()

        return po.IfStmt(condition, body, elif_statements, else_body)

    # elif = "elif", "(", expression, ")", block ;
    def parse_elif(self):
        if not self.might_be(TokenType.ELIF_KEYWORD):
            return None

        self.must_be(TokenType.LEFT_BRACKET, "'(' expected")

        condition = self.parse_expression()
        if not condition:
            raise SyntaxException()

        self.must_be(TokenType.RIGHT_BRACKET, "')' expected")

        body = self.parse_block()
        if not body:
            raise SyntaxException()

        return po.ElifStmt(condition, body)

    # while_loop = "while", "(", expression, ")", block ;
    def parse_while_loop(self):
        if not self.might_be(TokenType.WHILE_KEYWORD):
            return None

        self.must_be(TokenType.LEFT_BRACKET, "'(' expected")

        condition = self.parse_expression()
        if not condition:
            raise SyntaxException()

        self.must_be(TokenType.RIGHT_BRACKET, "')' expected")

        body = self.parse_block()
        if not body:
            raise SyntaxException()

        return po.WhileStmt(condition, body)

    # for_loop = "for", identifier, "in", expression, block ;
    def parse_for_loop(self):
        if not self.might_be(TokenType.FOR_KEYWORD):
            return None

        token = self.must_be(TokenType.IDENTIFIER, "Identifier expected")
        var = po.Identifier(token.value)

        self.must_be(TokenType.IN_KEYWORD, "'in' keyword expected")

        source = self.parse_expression()
        if not source:
            raise SyntaxException()

        body = self.parse_block()
        if not body:
            raise SyntaxException()

        return po.ForStmt(var, source, body)

    # return_statement = "return", [ expression ], ";" ;
    def parse_return_statement(self):
        if not self.might_be(TokenType.RETURN_KEYWORD):
            return None

        value = self.parse_expression()

        self.must_be(TokenType.SEMICOLON, "';' expected")

        return po.ReturnStmt(value)

    # block	= "{", { statement }, "}" ;
    def parse_block(self):
        if self.might_be(TokenType.LEFT_CURLY_BRACKET):
            return None

        statements = []
        while statement := self.parse_statement():
            statements.append(statement)

        self.must_be(TokenType.RIGHT_CURLY_BRACKET, "'}' expected")

        return po.Block(statements)

    # expression = logic_or ;
    def parse_expression(self):
        return self.parse_logic_or()

    # logic_or = logic_and, { "or", logic_and } ;
    def parse_logic_or(self):
        return self.binary_operation_builder(
            self.parse_logic_and, TokenType.OR_OPERATOR
        )

    # logic_and = equality, { "and", equality } ;
    def parse_logic_and(self):
        return self.binary_operation_builder(
            self.parse_equality, TokenType.AND_OPERATOR
        )

    # equality = comparison, { ("==" | "!="), comparison } ;
    def parse_equality(self):
        return self.binary_operation_builder(
            self.parse_comparison, TokenType.EQ_OPERATOR, TokenType.NEQ_OPERATOR
        )

    # comparison = additive, { (">" | ">=" | "<" | "<="), additive } ;
    def parse_comparison(self):
        return self.binary_operation_builder(
            self.parse_additive,
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
            expr = po.NegationExpr(pu.match_negation_type(token.type), expr)
        return expr

    # postfix = primary, { call_suff | member_suff} ;
    def parse_postfix(self):
        expr = self.parse_primary()

        while (
            new_expr := (self.parse_access_suff(expr) or self.parse_call_suff(expr))
        ) is not None:
            expr = new_expr

        return expr

    # primary = integer
    # 				| float
    # 				| string
    # 				| "True" | "False"
    # 				| identifier
    # 				| list_literal
    # 				| dict_literal
    # 				| linq_query
    # 				| item_literal_or_parenthisis
    def parse_primary(self):
        token = self.current_token

        mapping = {
            TokenType.INT_LITERAL: po.SimpleTypeExpr(pu.SimpleLiteralType.INT, token.value),
            TokenType.FLOAT_LITERAL: po.SimpleLiteralType(pu.SimpleLiteralType.FLOAT, token.value),
            TokenType.STRING_LITERAL: po.SimpleLiteralType(pu.SimpleLiteralType.STRING, token.value),
            TokenType.TRUE_LITERAL: po.SimpleLiteralType(pu.SimpleLiteralType.BOOL, True),
            TokenType.FALSE_LITERAL: po.SimpleLiteralType(pu.SimpleLiteralType.BOOL, False),
            TokenType.IDENTIFIER: po.Identifier(token.value)
        }

        if simple_type := mapping.get(token.type, None) is not None:
            self.get_next_token()
            return simple_type

        return {
            self.parse_list_literal()
            or self.parse_dict_literal()
            or self.parse_linq_query()
            or self.parse_item_literal_or_parenthisis()
        }


    def parse_list_literal(self):
        pass

    def parse_dict_literal(self):
        pass

    def parse_linq_query(self):
        pass

    def parse_item_literal_or_parenthisis(self):
        pass

    def parse_argument_list(self):
        pass
