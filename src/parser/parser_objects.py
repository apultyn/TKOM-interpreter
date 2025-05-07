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

    def accept(self, visitor: "Visitor"):
        method = getattr(visitor, f"visit_{self._name}", None)
        if method is None:
            return visitor.generic_visit(self)
        return method(self)


class Visitor:
    def generic_visit(self, node: ParserObject):
        for attr in fields(node):
            value = getattr(node, attr.name)
            if isinstance(value, ParserObject):
                value.accept(self)
            if isinstance(value, list):
                for item in value:
                    if isinstance(item, ParserObject):
                        item.accept(self)


class PrintVisitor(Visitor):
    def __init__(self, ident: int = 2, pos=False):
        self._level = 0
        self._ident = ident

    def _pad(self):
        return " " * (self._level * self._ident)

    def generic_visit(self, node):
        print(f"{self._pad()}{node._name}  pos={node.pos}")
        self._level += 1
        super().generic_visit(node)
        self._level -= 1

    def visit_Identifier(self, node: "Identifier"):
        print(f"{self._pad()}Identifier  name={node.name}  pos={node.pos}")

    def visit_IfStmt(self, node: "IfStmt"):
        print(f"{self._pad()}IfStatement  pos={node.pos}")
        self._level += 1
        print(f"{self._pad()}condition:")
        self._level += 1
        print(node.condition.accept(self))
        self._level -= 1
        print(f"{self._pad()}body:")
        self._level += 1
        print(node.body.accept(self))
        self._level -= 1
        print(f"{self._pad()}elif statements:")
        self._level += 1
        for elifstmt in node.elif_statements:
            print(elifstmt.accept(self))
        self._level -= 1
        print(f"{self._pad()}else statement:")
        self._level += 1
        if node.else_body:
            print(node.else_body.accept(self))
        self._level -= 2


class Statement(ParserObject):
    def __repr__(self):
        return None


class Expression(ParserObject):
    def __repr__(self):
        return None


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
