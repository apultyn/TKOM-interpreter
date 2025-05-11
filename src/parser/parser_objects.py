from dataclasses import dataclass, field, fields
from typing import List, Any, Optional

from .parser_util import (
    AssignmentType,
    BinaryOperationType,
    NegationType,
    SimpleExprType,
)


@dataclass(kw_only=True)
class ParserObject:
    _name: str = field(init=False, repr=False)
    pos: tuple[int, int]

    def __post_init__(self):
        self._name = self.__class__.__name__


class Statement(ParserObject):
    pass


class Expression(ParserObject):
    pass


@dataclass
class Identifier(Expression):
    name: str


@dataclass
class Block(Statement):
    statements: List[Statement]


@dataclass
class Program(ParserObject):
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
    operation: BinaryOperationType
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
class SimpleExpr(Expression):
    value_type: SimpleExprType
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
