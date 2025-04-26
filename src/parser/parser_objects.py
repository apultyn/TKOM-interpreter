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
    elif_statements: List["ElifStmt"]
    else_body: Block


@dataclass
class ElifStmt(Statement):
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
    assign_type: AssignmentType
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
class AccessExpr(Expression):
    source: Expression
    target: Identifier


@dataclass
class CallExpr(Expression):
    callee: Expression
    args: List[Expression]


@dataclass
class SimpleTypeExpr(Expression):
    value_type: SimpleLiteralType
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
    items: List[ItemExpr]


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
