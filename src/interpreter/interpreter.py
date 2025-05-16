from functools import singledispatchmethod

import src.parser.parser_objects as po

from src.util.pyscript_exceptions import RuntimeException
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
    StringValue,
    ListValue,
    ItemValue,
    DictValue,
    FuncValue,
)

GLOBAL_ENV = Env()


class Interpreter:
    def __init__(
        self,
        error_handler: ErrorHandler = ErrorHandler(),
        cfg: InterpreterConfig = InterpreterConfig(),
    ):
        self._error_handler = error_handler
        self._cfg = cfg
        self.global_env = GLOBAL_ENV

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

    # Block
    @eval.register
    def _(self, node: po.Block, env: Env):
        for stmt in node.statements:
            self.eval(stmt, env)

    # Program
    @eval.register
    def _(self, node: po.Program, env: Env):
        for stmt in node.statements:
            self.eval(stmt, env)

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
        value = self.eval(node.r_value, env)
        name = node.l_value.value

        if name in env.symbols:
            env.set(name, value)
        else:
            env.define(name, value)

    # Plus Assignment
    def _(self, node: po.PlusAssignmentStmt, env: Env):
        name = node.l_value.value
        try:
            l_value = env.get(name)
            r_value = self.eval(node.r_value, env)
            self.ensure_same_type(l_value, r_value, "+=", node)

            if not isinstance(l_value, Additive):
                raise RuntimeException(
                    f"Operation '+=' not supported for type {l_value.__class__}",
                    pos=node.pos,
                )

            env.set(name, l_value + r_value)
        except RuntimeException as exc:
            self._error_handler.handle_error(exc)

    # Minus Assignment
    def _(self, node: po.MinusAssignmentStmt, env: Env):
        name = node.l_value.value
        try:
            l_value = env.get(name)
            r_value = self.eval(node.r_value, env)
            self.ensure_same_type(l_value, r_value, "+=", node)

            if not isinstance(l_value, Subtractive):
                raise RuntimeException(
                    f"Operation '-=' not supported for type {l_value.__class__}",
                    pos=node.pos,
                )

            env.set(name, l_value - r_value)
        except RuntimeException as exc:
            self._error_handler.handle_error(exc)

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
            self._error_handler.handle_error(
                RuntimeException(
                    f"Operation '>' not supported on type {l_value.__class__}",
                    pos=node.pos,
                )
            )

    # Geq Expr
    @eval.register
    def _(self, node: po.GeqExpr, env: Env):
        l_value = self.eval(node.l_value, env)
        r_value = self.eval(node.r_value, env)

        self.ensure_same_type(l_value, r_value, ">=", node)

        try:
            return BoolValue(l_value >= r_value)
        except TypeError:
            self._error_handler.handle_error(
                RuntimeException(
                    f"Operation '>=' not supported on type {l_value.__class__}",
                    pos=node.pos,
                )
            )

    # Lt Expr
    @eval.register
    def _(self, node: po.LtExpr, env: Env):
        l_value = self.eval(node.l_value, env)
        r_value = self.eval(node.r_value, env)

        self.ensure_same_type(l_value, r_value, "<", node)

        try:
            return BoolValue(l_value < r_value)
        except TypeError:
            self._error_handler.handle_error(
                RuntimeException(
                    f"Operation '<' not supported on type {l_value.__class__}",
                    pos=node.pos,
                )
            )

    # Leq Expr
    @eval.register
    def _(self, node: po.LeqExpr, env: Env):
        l_value = self.eval(node.l_value, env)
        r_value = self.eval(node.r_value, env)

        self.ensure_same_type(l_value, r_value, "<=", node)

        try:
            return BoolValue(l_value <= r_value)
        except TypeError:
            self._error_handler.handle_error(
                RuntimeException(
                    f"Operation '<=' not supported on type {l_value.__class__}",
                    pos=node.pos,
                )
            )

    # Add Expr
    @eval.register
    def _(self, node: po.AddExpr, env: Env):
        l_value = self.eval(node.l_value, env)
        r_value = self.eval(node.r_value, env)

        self.ensure_same_type(l_value, r_value, "add", node)

        if not isinstance(l_value, Additive):
            self._error_handler.handle_error(
                RuntimeException(
                    f"Operation '+' not supported for type {l_value.__class__}",
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
                    f"Operation '-' not supported for type {l_value.__class__}",
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
                    f"Operation '*' not supported for type {l_value.__class__}",
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
                f"Operation '/' not supported for type {l_value.__class__}",
                pos=node.pos,
            )
        )

    # Logic Negation Expr
    @eval.register
    def _(self, node: po.LogicNegExpr, env: Env):
        value = self.eval(node.value, env)
        if not isinstance(value, BoolValue):
            self._error_handler.handle_error(
                RuntimeException(
                    f"Logic negation is not supported for type {value.__class__}",
                    pos=node.pos,
                )
            )
        return BoolValue(not value.value)

    # Arihmetic Negation Expr
    @eval.register
    def _(self, node: po.ArithNegExpr, env: Env):
        value = self.eval(node.value, env)

        if isinstance(value, IntValue):
            return IntValue(-value.value)

        if isinstance(value, FloatValue):
            return FloatValue(-value.value)

        self._error_handler.handle_error(
            RuntimeException(
                f"Arihmetic negation is not supported for type {value.__class__}",
                pos=node.pos,
            )
        )

    # Access Expr
    @eval.register
    def _(self, node: po.AccessExpr, env: Env):
        pass

    # Call Expr
    @eval.register
    def _(self, node: po.CallExpr, env: Env):
        callee: FuncValue = self.eval(node.callee, env)

        if not isinstance(callee, FuncValue):
            self._error_handler.handle_error(
                RuntimeException(
                    f"Object {callee.__class__} is not callable", pos=node.pos
                )
            )

        arg_vals = [self.eval(arg, env) for arg in node.args]

        try:
            exec_env = callee.get_call_env(arg_vals, node.pos)
            return self.eval(callee.body, exec_env)
        except RuntimeException as exc:
            self._error_handler.handle_error(exc)

    # Int Expr
    @eval.register
    def _(self, node: po.IntExpr, env: Env):
        return IntValue(node.value)

    # Float Expr
    @eval.register
    def _(self, node: po.FloatExpr, env: Env):
        return FloatValue(node.value)

    # String Expr
    @eval.register
    def _(self, node: po.StringExpr, env: Env):
        return StringValue(node.value)

    # Identifier
    @eval.register
    def _(self, node: po.Identifier, env: Env):
        return env.get(node.value)

    # Bool Expr
    @eval.register
    def _(self, node: po.BoolExpr, env: Env):
        return BoolValue(node.value)

    # List Expr
    @eval.register
    def _(self, node: po.ListExpr, env: Env):
        elements = []
        for element in node.elements:
            object = self.eval(element, env)
            elements.append(object)

        return ListValue(elements)

    # Item Expr
    @eval.register
    def _(self, node: po.ItemExpr, env: Env):
        key = self.eval(node.key, env)
        value = self.eval(node.value, env)

        return ItemValue(key, value)

    # Dict Expr
    @eval.register
    def _(self, node: po.DictExpr, env: Env):
        dict = DictValue(
            [], lambda x: 1
        )  # Tu kiedyś będzie musiała trafić defaultowa funkcja

        for parser_item in node.items:
            interpreter_item = self.eval(parser_item, env)
            dict.add(interpreter_item)

        return dict

    # Function expr
    @eval.register
    def _(self, node: po.FunctionExpr, env: Env):
        param_names = [ident.value for ident in node.params]
        return FuncValue(param_names, node.body, env)

    # Linq expr
    @eval.register
    def _(self, node: po.LinqExpr, env: Env):
        pass

    # Brackets expr
    @eval.register
    def _(self, node: po.BracketsExpr, env: Env):
        return self.eval(node.value, env)
