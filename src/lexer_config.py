from dataclasses import dataclass
import json


@dataclass
class LexerConfig:
    max_comment_length: int = 10000
    max_identifier_length: int = 1000
    max_string_literal_length: int = 10000

    @staticmethod
    def from_json(path: str) -> "LexerConfig":
        with open(path, "r") as file_handle:
            data = json.load(file_handle)
        return LexerConfig(**data)
