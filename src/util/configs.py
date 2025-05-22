from dataclasses import dataclass, field
from pathlib import Path
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


@dataclass
class InterpreterConfig:
    pass


@dataclass
class AppConfig:
    lexer_config: LexerConfig = field(default_factory=LexerConfig)
    interpreter_config: InterpreterConfig = field(default_factory=InterpreterConfig)

    @staticmethod
    def from_json(path: Path) -> "AppConfig":
        with path.open("r", encoding="utf-8") as fp:
            raw = json.load(fp)

        return AppConfig(
            lexer_config=LexerConfig(**raw.get("lexer", {})),
            interpreter_config=InterpreterConfig(**raw.get("interpreter", {})),
        )
