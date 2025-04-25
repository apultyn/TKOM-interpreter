from dataclasses import dataclass
from typing import List, Optional


class Statement:
    pass


class Expression:
    pass


class Identifier:
    pass


@dataclass
class Block(Statement):
    statements: List[Statement]


@dataclass
class Program:
    statements: List[Statement]


@dataclass
class IfStatement(Statement):
    condition: Expression
    body: Block
    else_if_statements: List["ElseIfStatement"]
    else_body: Block


@dataclass
class ElseIfStatement(Statement):
    condition: Expression
    body: Block


@dataclass
class WhileStatement(Statement):
    condition: Expression
    body: Block


@dataclass
class ForStatement(Statement):
    element: Identifier
    collection: Expression
    body: Block


@dataclass
class ReturnStatement(Statement):
    value: Expression
