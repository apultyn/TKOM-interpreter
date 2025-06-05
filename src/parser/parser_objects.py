from dataclasses import dataclass, field
from typing import List, Any, Optional
from abc import ABC


@dataclass(kw_only=True)
class ParserObject:
    _name: str = field(init=False, repr=False)
    pos: tuple[int, int] | None = None

    def __post_init__(self):
        self._name = self.__class__.__name__

    def accept(self, visitor, *args, **kwargs):
        method_name = f"visit_{self._name}"
        visit = getattr(visitor, method_name, visitor.visit_default)
        return visit(self, *args, **kwargs)


class Statement(ParserObject):
    pass


class Expression(ParserObject):
    pass


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
    elif_statements: List["ElifStmt"] = field(default_factory=list)
    else_body: Block | None = None


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
    var: "Identifier"
    source: Expression
    body: Block


@dataclass
class ReturnStmt(Statement):
    value: Expression


@dataclass
class AssignmentStmt(Statement):
    l_value: "Identifier"
    r_value: Expression


class NormalAssignmentStmt(AssignmentStmt):
    pass


class PlusAssignmentStmt(AssignmentStmt):
    pass


class MinusAssignmentStmt(AssignmentStmt):
    pass


@dataclass
class BinaryExpr(Expression):
    l_value: Expression
    r_value: Expression


class OrExpr(BinaryExpr):
    pass


class AndExpr(BinaryExpr):
    pass


class EqExpr(BinaryExpr):
    pass


class NeqExpr(BinaryExpr):
    pass


class GtExpr(BinaryExpr):
    pass


class GeqExpr(BinaryExpr):
    pass


class LtExpr(BinaryExpr):
    pass


class LeqExpr(BinaryExpr):
    pass


class AddExpr(BinaryExpr):
    pass


class SubExpr(BinaryExpr):
    pass


class MulExpr(BinaryExpr):
    pass


class DivExpr(BinaryExpr):
    pass


@dataclass
class NegationExpr(Expression):
    value: Expression


class LogicNegExpr(NegationExpr):
    pass


class ArithNegExpr(NegationExpr):
    pass


@dataclass
class AccessExpr(Expression):
    source: Expression
    target: "Identifier"


@dataclass
class CallExpr(Expression):
    callee: Expression
    args: List[Expression]


@dataclass
class SimpleExpr(Expression):
    value: Any


@dataclass
class IntExpr(SimpleExpr):
    value: int


@dataclass
class FloatExpr(SimpleExpr):
    value: float


@dataclass
class StringExpr(SimpleExpr):
    value: str


@dataclass
class Identifier(SimpleExpr):
    value: str


@dataclass
class BoolExpr(SimpleExpr):
    value: bool


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
