import argparse
import dataclasses
import json
import pathlib

from enum import Enum

from src.parser.parser import Parser
from src.lexer.lexer import Lexer
from src.util.error_handler import ErrorHandler

# from src.parser.parser_objects import PrintVisitor


def enum_default(obj):
    if isinstance(obj, Enum):
        return obj.to_json()
    raise TypeError


def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("-i", "--input", required=True)
    arg_parser.add_argument("-o", "--output", required=True)
    args = arg_parser.parse_args()

    with open(args.input) as file_handle:
        err = ErrorHandler()
        parser = Parser(
            lexer=Lexer(source=file_handle, error_handler=err), error_handler=err
        )

        program = parser.parse_program()

        # # Print
        # printer = PrintVisitor()
        # program.accept(printer)

        program._name = args.input
        pathlib.Path(args.output).write_text(
            json.dumps(dataclasses.asdict(program), indent=2, default=enum_default)
        )


if __name__ == "__main__":
    main()
