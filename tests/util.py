from src.util.token_type import TokenType


def get_token_list(lexer):
    tokens = []
    token = lexer.get_next_token()

    while token.type != TokenType.EOF:
        tokens.append(token)
        token = lexer.get_next_token()

    tokens.append(token)
    return tokens
