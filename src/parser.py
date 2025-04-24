from lexer import Lexer
from token_type import TokenType

class Parser:
    def __init__(self, lexer: Lexer, error_handler):
        self.lexer = lexer
        self.current_token = None
        self.error_handler = error_handler
        self.current_token = self.get_next_token()

    def get_next_token(self):
        self.current_token = self.lexer.get_next_token()

        while self.current_token in [
            TokenType.BLOCK_COMMENT,
            TokenType.LINE_COMMENT,
        ]:
            self.current_token = self.lexer.get_next_token()
        return self.current_token
