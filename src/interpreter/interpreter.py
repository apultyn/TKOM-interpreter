from functools import singledispatchmethod

import src.parser.parser_objects as po
from src.interpreter.util import (
    GLOBAL_ENV,
    ReturnSignal,
    get_operation_unsupported_type_msg,
)

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
    BuiltInFunc,
    Collection,
)


class Interpreter:
    def __init__(
        self,
        *,
        error_handler: ErrorHandler = ErrorHandler(),
        config: InterpreterConfig = InterpreterConfig(),
        env: Env = GLOBAL_ENV,
    ):
        self._error_handler = error_handler
        self._config = config
        self.global_env = env

    def ensure_same_type(
        self, l_value: Value, r_value: Value, operation: str, node: po.ParserObject
    ):
        try:
            Value.typecheck(l_value, r_value, operation)
        except TypeError as exc:
            self._error_handler.handle_error(
                RuntimeException(
                    msg=exc.args[0],
                    pos=node.pos,
                )
            )

    # Default
    @singledispatchmethod
    def eval(self, node: po.ParserObject, env: Env | None = None):
        if env is None:
            env = self.global_env
        raise NotImplementedError(type(node))

    # Block
    @eval.register
    def _(self, node: po.Block, env: Env | None = None):
        if env is None:
            env = self.global_env
        for stmt in node.statements:
            self.eval(stmt, env)

    # Program
    @eval.register
    def _(self, node: po.Program):
        try:
            for stmt in node.statements:
                self.eval(stmt, self.global_env)
            print("Script executed.")
        except ReturnSignal as exc:
            self._error_handler.handle_error(
                RuntimeException(
                    f"Return statement not allowed outside of function",
                    pos=exc.return_statement.pos,
                )
            )

    # If Statement
    @eval.register
    def _(self, node: po.IfStmt, env: Env | None = None):
        if env is None:
            env = self.global_env
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
    def _(self, node: po.WhileStmt, env: Env | None = None):
        if env is None:
            env = self.global_env
        while self.eval(node.condition, env).truthy():
            self.eval(node.body, Env(env))

    # For Statement
    @eval.register
    def _(self, node: po.ForStmt, env: Env | None = None):
        if env is None:
            env = self.global_env
        source = self.eval(node.source, env)

    # Return Statement
    @eval.register
    def _(self, node: po.ReturnStmt, env: Env | None = None):
        if env is None:
            env = self.global_env
        value = None
        if node.value:
            value = self.eval(node.value, env)
        raise ReturnSignal

    # Normal Assignment
    @eval.register
    def _(self, node: po.NormalAssignmentStmt, env: Env | None = None):
        if env is None:
            env = self.global_env
        value = self.eval(node.r_value, env)
        ident = node.l_value

        if ident.value in env.symbols:
            env.set(ident, value)
        else:
            env.define(ident, value)

    # Plus Assignment
    @eval.register
    def _(self, node: po.PlusAssignmentStmt, env: Env | None = None):
        if env is None:
            env = self.global_env
        name = node.l_value
        try:
            l_value = env.get(name)
            r_value = self.eval(node.r_value, env)
            self.ensure_same_type(l_value, r_value, "+=", node)

            if not isinstance(l_value, Additive):
                raise RuntimeException(
                    get_operation_unsupported_type_msg(l_value, "+="),
                    pos=node.pos,
                )

            env.set(name, l_value + r_value)
        except RuntimeException as exc:
            self._error_handler.handle_error(exc)

    # Minus Assignment
    @eval.register
    def _(self, node: po.MinusAssignmentStmt, env: Env | None = None):
        if env is None:
            env = self.global_env
        name = node.l_value
        try:
            l_value = env.get(name)
            r_value = self.eval(node.r_value, env)
            self.ensure_same_type(l_value, r_value, "-=", node)

            if not isinstance(l_value, Subtractive):
                raise RuntimeException(
                    get_operation_unsupported_type_msg(l_value, "-="),
                    pos=node.pos,
                )

            env.set(name, l_value - r_value)
        except RuntimeException as exc:
            self._error_handler.handle_error(exc)

    # Or Expr
    @eval.register
    def _(self, node: po.OrExpr, env: Env | None = None):
        if env is None:
            env = self.global_env
        if self.eval(node.l_value, env).truthy():
            return BoolValue(True)

        if self.eval(node.r_value, env).truthy():
            return BoolValue(True)

        return BoolValue(False)

    # And Expr
    @eval.register
    def _(self, node: po.AndExpr, env: Env | None = None):
        if env is None:
            env = self.global_env
        if not self.eval(node.l_value, env).truthy():
            return BoolValue(False)

        if not self.eval(node.r_value, env).truthy():
            return BoolValue(False)

        return BoolValue(True)

    # Eq Expr
    @eval.register
    def _(self, node: po.EqExpr, env: Env | None = None):
        if env is None:
            env = self.global_env
        l_value = self.eval(node.l_value, env)
        r_value = self.eval(node.r_value, env)

        return BoolValue(l_value == r_value)

    # Neq Expr
    @eval.register
    def _(self, node: po.NeqExpr, env: Env | None = None):
        if env is None:
            env = self.global_env
        l_value = self.eval(node.l_value, env)
        r_value = self.eval(node.r_value, env)

        return BoolValue(l_value != r_value)

    # Gt Expr
    @eval.register
    def _(self, node: po.GtExpr, env: Env | None = None):
        if env is None:
            env = self.global_env
        l_value = self.eval(node.l_value, env)
        r_value = self.eval(node.r_value, env)

        self.ensure_same_type(l_value, r_value, ">", node)

        try:
            return BoolValue(l_value > r_value)
        except TypeError:
            self._error_handler.handle_error(
                RuntimeException(
                    get_operation_unsupported_type_msg(l_value, ">"),
                    pos=node.pos,
                )
            )

    # Geq Expr
    @eval.register
    def _(self, node: po.GeqExpr, env: Env | None = None):
        if env is None:
            env = self.global_env
        l_value = self.eval(node.l_value, env)
        r_value = self.eval(node.r_value, env)

        self.ensure_same_type(l_value, r_value, ">=", node)

        try:
            return BoolValue(l_value >= r_value)
        except TypeError:
            self._error_handler.handle_error(
                RuntimeException(
                    get_operation_unsupported_type_msg(l_value, ">="),
                    pos=node.pos,
                )
            )

    # Lt Expr
    @eval.register
    def _(self, node: po.LtExpr, env: Env | None = None):
        if env is None:
            env = self.global_env
        l_value = self.eval(node.l_value, env)
        r_value = self.eval(node.r_value, env)

        self.ensure_same_type(l_value, r_value, "<", node)

        try:
            return BoolValue(l_value < r_value)
        except TypeError:
            self._error_handler.handle_error(
                RuntimeException(
                    get_operation_unsupported_type_msg(l_value, "<"),
                    pos=node.pos,
                )
            )

    # Leq Expr
    @eval.register
    def _(self, node: po.LeqExpr, env: Env | None = None):
        if env is None:
            env = self.global_env
        l_value = self.eval(node.l_value, env)
        r_value = self.eval(node.r_value, env)

        self.ensure_same_type(l_value, r_value, "<=", node)

        try:
            return BoolValue(l_value <= r_value)
        except TypeError:
            self._error_handler.handle_error(
                RuntimeException(
                    get_operation_unsupported_type_msg(l_value, "<="),
                    pos=node.pos,
                )
            )

    # Add Expr
    @eval.register
    def _(self, node: po.AddExpr, env: Env | None = None):
        if env is None:
            env = self.global_env
        l_value = self.eval(node.l_value, env)
        r_value = self.eval(node.r_value, env)

        self.ensure_same_type(l_value, r_value, "+", node)

        if not isinstance(l_value, Additive):
            self._error_handler.handle_error(
                RuntimeException(
                    get_operation_unsupported_type_msg(l_value, "+"),
                    pos=node.pos,
                )
            )

        return l_value + r_value

    # Sub Expr
    @eval.register
    def _(self, node: po.SubExpr, env: Env | None = None):
        if env is None:
            env = self.global_env
        l_value = self.eval(node.l_value, env)
        r_value = self.eval(node.r_value, env)

        self.ensure_same_type(l_value, r_value, "-", node)

        if not isinstance(l_value, Subtractive):
            self._error_handler.handle_error(
                RuntimeException(
                    get_operation_unsupported_type_msg(l_value, "-"),
                    pos=node.pos,
                )
            )

        return l_value - r_value

    # Mul Expr
    @eval.register
    def _(self, node: po.MulExpr, env: Env | None = None):
        if env is None:
            env = self.global_env
        l_value = self.eval(node.l_value, env)
        r_value = self.eval(node.r_value, env)

        self.ensure_same_type(l_value, r_value, "*", node)

        if not isinstance(l_value, Multiplicative):
            self._error_handler.handle_error(
                RuntimeException(
                    get_operation_unsupported_type_msg(l_value, "*"),
                    pos=node.pos,
                )
            )

        return l_value * r_value

    # Div Expr
    @eval.register
    def _(self, node: po.DivExpr, env: Env | None = None):
        if env is None:
            env = self.global_env
        l_value = self.eval(node.l_value, env)
        r_value = self.eval(node.r_value, env)

        self.ensure_same_type(l_value, r_value, "/", node)

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
                get_operation_unsupported_type_msg(l_value, "/"),
                pos=node.pos,
            )
        )

    # Logic Negation Expr
    @eval.register
    def _(self, node: po.LogicNegExpr, env: Env | None = None):
        if env is None:
            env = self.global_env
        value = self.eval(node.value, env)
        if not isinstance(value, BoolValue):
            self._error_handler.handle_error(
                RuntimeException(
                    get_operation_unsupported_type_msg(value, "!"),
                    pos=node.pos,
                )
            )
        return BoolValue(not value.value)

    # Arihmetic Negation Expr
    @eval.register
    def _(self, node: po.ArithNegExpr, env: Env | None = None):
        if env is None:
            env = self.global_env
        value = self.eval(node.value, env)

        if isinstance(value, IntValue):
            return IntValue(-value.value)

        if isinstance(value, FloatValue):
            return FloatValue(-value.value)

        self._error_handler.handle_error(
            RuntimeException(
                get_operation_unsupported_type_msg(value, "-"),
                pos=node.pos,
            )
        )

    # Access Expr
    @eval.register
    def _(self, node: po.AccessExpr, env: Env | None = None):
        if env is None:
            env = self.global_env
        src = self.eval(node.source, env)
        field = node.target.value

        try:
            if field in src.members:
                return src.members[field].value
            raise AttributeError
        except AttributeError:
            self._error_handler.handle_error(
                RuntimeException(
                    f"Object {src.__class__} has no {field} member", pos=node.target.pos
                )
            )

    # Call Expr
    @eval.register
    def _(self, node: po.CallExpr, env: Env | None = None):
        if env is None:
            env = self.global_env
        callee: FuncValue | BuiltInFunc = self.eval(node.callee, env)
        arg_objects = [self.eval(arg, env) for arg in node.args]

        try:
            if isinstance(callee, FuncValue):
                exec_env = callee.get_call_env(arg_objects, node.pos)
                return self.eval(callee.body, exec_env)

            if isinstance(callee, BuiltInFunc):
                return callee(node.pos, arg_objects)

        except RuntimeException as exc:
            self._error_handler.handle_error(exc)
        except ReturnSignal as exc:
            return exc.return_value

        self._error_handler.handle_error(
            RuntimeException(
                f"Object {callee.__class__.__qualname__} is not callable", pos=node.pos
            )
        )

    # Int Expr
    @eval.register
    def _(self, node: po.IntExpr, env: Env | None = None):
        if env is None:
            env = self.global_env
        return IntValue(node.value)

    # Float Expr
    @eval.register
    def _(self, node: po.FloatExpr, env: Env | None = None):
        if env is None:
            env = self.global_env
        return FloatValue(node.value)

    # String Expr
    @eval.register
    def _(self, node: po.StringExpr, env: Env | None = None):
        if env is None:
            env = self.global_env
        return StringValue(node.value)

    # Identifier
    @eval.register
    def _(self, node: po.Identifier, env: Env | None = None):
        if env is None:
            env = self.global_env
        return env.get(node)

    # Bool Expr
    @eval.register
    def _(self, node: po.BoolExpr, env: Env | None = None):
        if env is None:
            env = self.global_env
        return BoolValue(node.value)

    # List Expr
    @eval.register
    def _(self, node: po.ListExpr, env: Env | None = None):
        if env is None:
            env = self.global_env
        elements = []
        for element in node.elements:
            object = self.eval(element, env)
            elements.append(object)

        return ListValue(elements)

    # Item Expr
    @eval.register
    def _(self, node: po.ItemExpr, env: Env | None = None):
        if env is None:
            env = self.global_env
        key = self.eval(node.key, env)
        value = self.eval(node.value, env)

        return ItemValue(key, value)

    # Dict Expr
    @eval.register
    def _(self, node: po.DictExpr, env: Env | None = None):
        if env is None:
            env = self.global_env
        dict = DictValue([], lambda x: IntValue(1))
        dict.bind(self)

        for parser_item in node.items:
            interpreter_item = self.eval(parser_item, env)
            dict.add(interpreter_item)

        return dict

    # Function expr
    @eval.register
    def _(self, node: po.FunctionExpr, env: Env | None = None):
        if env is None:
            env = self.global_env
        param_names = [ident.value for ident in node.params]
        return FuncValue(param_names, node.body, env)

    # Linq expr
    @eval.register
    def _(self, node: po.LinqExpr, env: Env | None = None):
        if env is None:
            env = self.global_env
        var = node.var
        source = self.eval(node.source, env)

        if not isinstance(source, Collection):
            self._error_handler.handle_error(
                RuntimeException(
                    f"Source should be a collection, got {source.__class__.__qualname__}",
                    pos=node.source.pos,
                )
            )

        new_env = Env(env)
        new_env.define(var, None)

        return_list = []

        for element in source:
            new_env.set(var, element)

            # where
            if node.where:
                condition = self.eval(node.where, new_env)

                if not isinstance(condition, BoolValue):
                    self._error_handler.handle_error(
                        f"'where' condition should be a BoolValue, got {condition.__class__.__qualname__}",
                        pos=node.where.pos,
                    )

                if not condition.value:
                    continue

            # selects
            selects = [self.eval(sel, new_env) for sel in node.selects]

            # order by
            order_key = None
            if node.order_by:
                order_key = self.eval(node.order_by, new_env)

                try:
                    inserted = False
                    # descending
                    if node.descending:
                        for i, item in enumerate(return_list):
                            if order_key > item[1]:
                                return_list.insert(i, (selects, order_key))
                                inserted = True
                                break
                    else:
                        for i, item in enumerate(return_list):
                            if order_key < item[i]:
                                return_list.insert(i, (selects, order_key))
                                inserted = True
                                break
                    if not inserted:
                        return_list.append((selects, order_key))

                except TypeError:
                    self._error_handler.handle_error(
                        RuntimeException(
                            f"Comparing not supported on type {order_key.__class__.__qualname__}",
                            pos=node.order_by.pos,
                        )
                    )
            else:
                return_list.append((selects, order_key))

        return ListValue([item[0] for item in return_list])

    # Brackets expr
    @eval.register
    def _(self, node: po.BracketsExpr, env: Env | None = None):
        if env is None:
            env = self.global_env
        return self.eval(node.value, env)
