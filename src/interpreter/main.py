import argparse

from src.lexer.lexer import Lexer
from src.lexer.lexer_config import LexerConfig


def main():
    arg_parser = argparse.ArgumentParser(description="Pyscript interpreter")
    arg_parser.add_argument("-c", "--config", help="Configuration file")

    args = arg_parser.parse_args()



if __name__ == "__main__":
    main()
