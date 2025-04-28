import argparse, json, pathlib, dataclasses

from enum import Enum

from src.parser.parser import Parser
from src.lexer.lexer import Lexer
from src.util.error_handler import ErrorHandler


def enum_default(obj):
    if isinstance(obj, Enum):
        return obj.to_json()
    raise TypeError

def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("--input")
    args = arg_parser.parse_args()

    with open(args.input) as file_handle:
        err = ErrorHandler()
        parser = Parser(
            lexer=Lexer(source=file_handle, error_handler=err),
            error_handler=err
        )

        program = parser.parse_program()
        program._name = args.input
        pathlib.Path("tree.json").write_text(
            json.dumps(dataclasses.asdict(program), indent=2, default=enum_default)
        )


if __name__ == "__main__":
    main()