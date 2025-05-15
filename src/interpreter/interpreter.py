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

    @singledispatchmethod
    def eval(self, node: po.ParserObject, env: Env):
        raise NotImplementedError(type(node))

    @eval.register
    def _(self, node: po.Program, env: Env):
        try:
            for stmt in node.statements:
                self.eval(stmt, env)
        except PyscriptException as exc:
            self._error_handler.handle_error(exc)

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

    @eval.register
    def _(self, node: po.WhileStmt, env: Env):
        while self.eval(node.condition, env).truthy():
            self.eval(node.body, Env(env))

    @eval.register
    def _(self, node: po.ForStmt, env: Env):
        source = self.eval(node.source)

    @eval.register
    def _(self, node: po.AddExpr, env: Env):
        left = self.eval(node.l_value, env)
        right = self.eval(node.r_value, env)

        try:
            Value.typecheck(left, right, "add")
        except ValueError as exc:
            self._error_handler.handle_error(
                RuntimeException(
                    msg=exc.args[0],
                    pos=node.pos,
                )
            )

        if not isinstance(left, Additive):
            self._error_handler.handle_error(
                RuntimeException(
                    f"Add operation is not supported for type {left.__class__}",
                    pos=node.pos,
                )
            )

        return left + right

    @eval.register
    def _(self, node: po.SubExpr, env: Env):
        left = self.eval(node.l_value, env)
        right = self.eval(node.r_value, env)

        try:
            Value.typecheck(left, right, "sub")
        except ValueError as exc:
            self._error_handler.handle_error(
                RuntimeException(
                    msg=exc.args[0],
                    pos=node.pos,
                )
            )

        if not isinstance(left, Subtractive):
            self._error_handler.handle_error(
                RuntimeException(
                    f"Sub operation is not supported for type {left.__class__}",
                    pos=node.pos,
                )
            )

        return left - right

    @eval.register
    def _(self, node: po.MulExpr, env: Env):
        left = self.eval(node.l_value, env)
        right = self.eval(node.r_value, env)

        try:
            Value.typecheck(left, right, "mul")
        except ValueError as exc:
            self._error_handler.handle_error(
                RuntimeException(
                    msg=exc.args[0],
                    pos=node.pos,
                )
            )

        if not isinstance(left, Multiplicative):
            self._error_handler.handle_error(
                RuntimeException(
                    f"Mul operation is not supported for type {left.__class__}",
                    pos=node.pos,
                )
            )

        return left * right

    @eval.register
    def _(self, node: po.DivExpr, env: Env):
        left = self.eval(node.l_value)
        right = self.eval(node.r_value)

        try:
            Value.typecheck(left, right, "div")
        except ValueError as exc:
            self._error_handler.handle_error(
                RuntimeException(
                    msg=exc.args[0],
                    pos=node.pos,
                )
            )

        if isinstance(left, IntValue):
            try:
                return left // right
            except ZeroDivisionError:
                self._error_handler.handle_error(
                    RuntimeException("Division by zero is not allowed", pos=node.pos)
                )

        if isinstance(left, FloatValue):
            try:
                return left / right
            except ZeroDivisionError:
                self._error_handler.handle_error(
                    RuntimeException("Division by zero is not allowed", pos=node.pos)
                )

        self._error_handler.handle_error(
            RuntimeException(
                f"Div operation is not supported for type {left.__class__}",
                pos=node.pos,
            )
        )
