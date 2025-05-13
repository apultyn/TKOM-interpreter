import argparse

from pathlib import Path

from .util import open_source
from src.util.configs import AppConfig
from src.lexer.lexer import Lexer
from src.parser.parser import Parser
from src.util.error_handler import ErrorHandler


def main():
    arg_parser = argparse.ArgumentParser(description="Pyscript interpreter")
    arg_parser.add_argument("-c", "--config", type=Path, help="JSON configuration file")
    arg_parser.add_argument("-i", "--input", type=Path, help="Source code file")

    args = arg_parser.parse_args()

    cfg = AppConfig.from_json(args.config) if args.config else AppConfig()

    err = ErrorHandler()

    with open_source(args.input) as src:
        lexer = Lexer(source=src, error_handler=err, config=cfg.lexer_config)
        parser = Parser(lexer=lexer, error_handler=err)
        print(parser.parse_program())