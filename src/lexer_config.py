from dataclasses import dataclass
import json


@dataclass
class LexerConfig:
    max_comment_length: int = 10000
    max_identifier_length: int = 1000
    max_string_literal_length: int = 10000
    max_num_literal_length: int = 100

    def __post_init__(self):
        if self.max_identifier_length < 10:
            raise ValueError("Identifiers must be at least 10 characters long")
        if (
            self.max_comment_length < 0
            or self.max_string_literal_length < 0
            or self.max_num_literal_length < 0
        ):
            raise ValueError("Lengths can't be smaller than 0")

    @staticmethod
    def from_json(path: str) -> "LexerConfig":
        with open(path, "r") as file_handle:
            data = json.load(file_handle)
        return LexerConfig(**data)
