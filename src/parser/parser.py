from lexer import Lexer
from token_type import TokenType
from src.util.error_handler import ErrorHandler
from src.util.pyscript_exceptions import PyscriptException

import parser_objects as po


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

        while self.current_token in [
            TokenType.BLOCK_COMMENT,
            TokenType.LINE_COMMENT,
        ]:
            self.current_token = self.lexer.get_next_token()
        return self.current_token

    def parse_program(self):
        statements = []
        while statement := self.parse_statement():
            statements.append(statement)
        return po.Program(statements)
