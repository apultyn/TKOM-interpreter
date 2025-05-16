from functools import singledispatchmethod

import src.parser.parser_objects as po

from src.util.pyscript_exceptions import PyscriptException, RuntimeException
from src.util.configs import InterpreterConfig
from src.util.error_handler import ErrorHandler
from .interpreter_objects import (
    Env,
    Value,
    Additive,
    Subtractive,
    Multiplicative,
    IntValue,
    FloatValue,
    BoolValue,
)


class Interpreter:
    def __init__(
        self,
        error_handler: ErrorHandler = ErrorHandler(),
        cfg: InterpreterConfig = InterpreterConfig(),
    ):
        self._error_handler = error_handler
        self._cfg = cfg
        self.global_env = Env()

    def ensure_same_type(
        self, l_value: Value, r_value: Value, operation: str, node: po.ParserObject
    ):
        try:
            Value.typecheck(l_value, r_value, operation)
        except ValueError as exc:
            self._error_handler.handle_error(
                RuntimeException(
                    msg=exc.args[0],
                    pos=node.pos,
                )
            )

    # Default
    @singledispatchmethod
    def eval(self, node: po.ParserObject, env: Env):
        raise NotImplementedError(type(node))

    # Program
    @eval.register
    def _(self, node: po.Program, env: Env):
        try:
            for stmt in node.statements:
                self.eval(stmt, env)
        except PyscriptException as exc:
            self._error_handler.handle_error(exc)

    # If Statement
    @eval.register
    def _(self, node: po.IfStmt, env: Env):
        if self.eval(node.condition, env).truthy():
            self.eval(node.body, Env(env))
            return
        for elif_stmt in node.elif_statements:
            if self.eval(elif_stmt.condition, env).truthy():
                self.eval(elif_stmt.body, Env(env))
                return
        if node.else_body:
            self.eval(node.else_body, Env(env))

    # While Statement
    @eval.register
    def _(self, node: po.WhileStmt, env: Env):
        while self.eval(node.condition, env).truthy():
            self.eval(node.body, Env(env))

    # For Statement
    @eval.register
    def _(self, node: po.ForStmt, env: Env):
        source = self.eval(node.source, env)

    # Return Statement
    @eval.register
    def _(self, node: po.ReturnStmt, env: Env):
        if node.value:
            return self.eval(node.value, env)
        return None

    # Normal Assignment
    def _(self, node: po.NormalAssignmentStmt, env: Env):
        pass

    # Plus Assignment
    def _(self, node: po.PlusAssignmentStmt, env: Env):
        pass

    # Minus Assignment
    def _(self, node: po.MinusAssignmentStmt, env: Env):
        pass

    # Or Expr
    @eval.register
    def _(self, node: po.OrExpr, env: Env):
        if self.eval(node.l_value, env).truthy():
            return BoolValue(True)

        if self.eval(node.r_value, env).truthy():
            return BoolValue(True)

        return BoolValue(False)

    # And Expr
    @eval.register
    def _(self, node: po.AndExpr, env: Env):
        if not self.eval(node.l_value, env).truthy():
            return BoolValue(False)

        if not self.eval(node.r_value, env).truthy():
            return BoolValue(False)

        return BoolValue(True)

    # Eq Expr
    @eval.register
    def _(self, node: po.EqExpr, env: Env):
        l_value = self.eval(node.l_value, env)
        r_value = self.eval(node.r_value, env)

        return BoolValue(l_value == r_value)

    # Neq Expr
    @eval.register
    def _(self, node: po.NeqExpr, env: Env):
        l_value = self.eval(node.l_value, env)
        r_value = self.eval(node.r_value, env)

        return BoolValue(l_value != r_value)

    # Gt Expr
    @eval.register
    def _(self, node: po.GtExpr, env: Env):
        l_value = self.eval(node.l_value, env)
        r_value = self.eval(node.r_value, env)

        self.ensure_same_type(l_value, r_value, ">", node)

        try:
            return BoolValue(l_value > r_value)
        except TypeError:
            self._error_handler.handle_error(RuntimeException(""))

    # Add Expr
    @eval.register
    def _(self, node: po.AddExpr, env: Env):
        l_value = self.eval(node.l_value, env)
        r_value = self.eval(node.r_value, env)

        self.ensure_same_type(l_value, r_value, "add", node)

        if not isinstance(l_value, Additive):
            self._error_handler.handle_error(
                RuntimeException(
                    f"Add operation is not supported for type {l_value.__class__}",
                    pos=node.pos,
                )
            )

        return l_value + r_value

    # Sub Expr
    @eval.register
    def _(self, node: po.SubExpr, env: Env):
        l_value = self.eval(node.l_value, env)
        r_value = self.eval(node.r_value, env)

        self.ensure_same_type(l_value, r_value, "sub", node)

        if not isinstance(l_value, Subtractive):
            self._error_handler.handle_error(
                RuntimeException(
                    f"Sub operation is not supported for type {l_value.__class__}",
                    pos=node.pos,
                )
            )

        return l_value - r_value

    # Mul Expr
    @eval.register
    def _(self, node: po.MulExpr, env: Env):
        l_value = self.eval(node.l_value, env)
        r_value = self.eval(node.r_value, env)

        self.ensure_same_type(l_value, r_value, "mul", node)

        if not isinstance(l_value, Multiplicative):
            self._error_handler.handle_error(
                RuntimeException(
                    f"Mul operation is not supported for type {l_value.__class__}",
                    pos=node.pos,
                )
            )

        return l_value * r_value

    # Div Expr
    @eval.register
    def _(self, node: po.DivExpr, env: Env):
        l_value = self.eval(node.l_value)
        r_value = self.eval(node.r_value)

        self.ensure_same_type(l_value, r_value, "div", node)

        if isinstance(l_value, IntValue):
            try:
                return l_value // r_value
            except ZeroDivisionError:
                self._error_handler.handle_error(
                    RuntimeException("Division by zero is not allowed", pos=node.pos)
                )

        if isinstance(l_value, FloatValue):
            try:
                return l_value / r_value
            except ZeroDivisionError:
                self._error_handler.handle_error(
                    RuntimeException("Division by zero is not allowed", pos=node.pos)
                )

        self._error_handler.handle_error(
            RuntimeException(
                f"Div operation is not supported for type {l_value.__class__}",
                pos=node.pos,
            )
        )
