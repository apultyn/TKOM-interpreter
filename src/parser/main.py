import argparse, json, pathlib, dataclasses

from enum import Enum

from src.parser.parser import Parser
from src.lexer.lexer import Lexer
from src.util.source import Source


def enum_default(obj):
    if isinstance(obj, Enum):
        return obj.to_json()
    raise TypeError

def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("--input")
    args = arg_parser.parse_args()

    with open(args.input) as file_handle:
        parser = Parser(
            lexer=Lexer(source=file_handle)
        )

        program = parser.parse_program()
        program._name = args.input
        pathlib.Path("tree.json").write_text(
            json.dumps(dataclasses.asdict(program), indent=2, default=enum_default)
        )


if __name__ == "__main__":
    main()