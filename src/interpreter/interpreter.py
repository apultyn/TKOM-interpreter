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

        Value.typecheck(left, right, node)

        if not isinstance(left, Additive):
            raise RuntimeException(
                f"Add operation is not supported for type {left.__class__}",
                pos=node.pos,
            )

        return left + right

    @eval.register
    def _(self, node: po.SubExpr, env: Env):
        left = self.eval(node.l_value, env)
        right = self.eval(node.r_value, env)

        Value.typecheck(left, right, node)

        if not isinstance(left, Subtractive):
            raise RuntimeException(
                f"Sub operation is not supported for type {left.__class__}",
                pos=node.pos,
            )

        return left - right

    @eval.register
    def _(self, node: po.MulExpr, env: Env):
        left = self.eval(node.l_value, env)
        right = self.eval(node.r_value, env)

        Value.typecheck(left, right, node)

        if not isinstance(left, Multiplicative):
            raise RuntimeException(
                f"Mul operation is not supported for type {left.__class__}",
                pos=node.pos,
            )

        return left * right

    # @eval.register
    # def _(self, node: po.DivExpr, env: Env):
    #     left = self.eval(node.l_value)
    #     right = self.eval(node.r_value)

    #     Value.typecheck(left, right, node)

    #     if isinstance(left, IntValue):
    #         pass

    #     if isinstance(left, FloatValue):
    #         pass

    #     raise RuntimeException(
    #         f"Div operation is not supported for type {left.__class__}",
    #         pos=node.pos
    #     )
