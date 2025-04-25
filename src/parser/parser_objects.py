from dataclasses import dataclass
from typing import List, Any, Optional

from parser_util import (
    Node,
    AssignmentType,
    BinaryOperation,
    NegationType,
    SimpleLiteralType,
)


class Statement(Node):
    pass


class Expression(Node):
    pass


@dataclass
class Identifier(Expression):
    name: str


@dataclass
class Block(Statement):
    statements: List[Statement]


@dataclass
class Program:
    statements: List[Statement]


@dataclass
class IfStmt(Statement):
    condition: Expression
    body: Block
    else_if_statements: List["ElseIfStmt"]
    else_body: Block


@dataclass
class ElseIfStmt(Statement):
    condition: Expression
    body: Block


@dataclass
class WhileStmt(Statement):
    condition: Expression
    body: Block


@dataclass
class ForStmt(Statement):
    var: Identifier
    source: Expression
    body: Block


@dataclass
class ReturnStmt(Statement):
    value: Expression


@dataclass
class AssignmentStmt(Statement):
    l_value: Identifier
    type: AssignmentType
    r_value: Expression


@dataclass
class BinaryExpr(Expression):
    l_value: Expression
    operation: BinaryOperation
    r_value: Expression


@dataclass
class NegationExpr(Expression):
    neg_type: NegationType
    value: Expression


@dataclass
class Member(Expression):
    object: Expression
    target: Identifier


@dataclass
class Call(Expression):
    object: Expression
    args: List[Expression]


@dataclass
class SimpleTypeExpr(Expression):
    type: SimpleLiteralType
    value: Any


@dataclass
class ListExpr(Expression):
    elements: List[Expression]


@dataclass
class ItemExpr(Expression):
    key: Expression
    value: Expression


@dataclass
class DictExpr(Expression):
    pairs: List[ItemExpr]


@dataclass
class FunctionExpr(Expression):
    params: List[Identifier]
    body: Block


@dataclass
class LinqExpr(Expression):
    var: Identifier
    source: Expression
    selects: List[Expression]
    where: Optional[Expression] = None
    order_by: Optional[Expression] = None
    descending: bool = False


@dataclass
class BracketsExpr(Expression):
    value: Expression
