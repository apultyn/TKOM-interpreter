from functools import singledispatchmethod

import parser.parser_objects as po

from util.pyscript_exceptions import PyscriptException
from util.configs import InterpreterConfig
from util.error_handler import ErrorHandler
from .interpreter_objects import Env


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
    def eval(self, node: po.ParserObject, env):
        raise NotImplementedError(type(node))

    @eval.register
    def _(self, node: po.Program, env):
        try:
            for stmt in node.statements:
                self.eval(stmt, env)
        except PyscriptException as exc:
            self._error_handler.handle_error(exc)

    @eval.register
    def _(self, node: po.IfStmt, env):
        if self.eval(node.condition, env).truthy():
            self.eval(node.body, Env(env))
            return
        for elif_stmt in node.elif_statements:
            if self.eval(elif_stmt.condition, env).truthy():
                self.eval(elif_stmt.body, Env(env))
                return
        if node.else_body:
            self.eval(node.else_body, Env(env))

