from copy import deepcopy

import src.parser.parser_objects as po
from src.interpreter.util import (
    GLOBAL_ENV,
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
    UserFuncValue,
    BuiltInFuncValue,
    FuncValue,
    Collection,
    ReturnSignal,
    AccessedFuncValue,
    is_simple,
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

    def check_params(
        self, call_args: list[Value], function: FuncValue
    ) -> list[Value] | None:
        selected = None
        for param_variant in function.param_variants:
            if len(call_args) != len(param_variant):
                continue

            for call_arg, param in zip(call_args, param_variant):
                if not isinstance(call_arg, param):
                    break
            else:
                selected = param_variant
        return selected

    def eval(self, node: po.ParserObject, env: Env | None = None) -> Value:
        if env is None:
            env = self.global_env
        return node.accept(self, env)

    # Default
    def visit_default(self, node: po.ParserObject, _: Env | None = None):
        raise NotImplementedError(
            f"Interpreter does not support {node.__class__.__name__} node"
        )

    # Block
    def visit_Block(self, node: po.Block, env: Env | None = None):
        for stmt in node.statements:
            self.eval(stmt, env)

    # Program
    def visit_Program(self, node: po.Program, _: Env | None = None):
        try:
            print("=" * 30 + " Running script... " + "=" * 30)
            for stmt in node.statements:
                self.eval(stmt, self.global_env)
            print("=" * 30 + " Script executed " + "=" * 30)
        except ReturnSignal as exc:
            self._error_handler.handle_error(
                RuntimeException(
                    f"Return statement not allowed outside of function",
                    pos=exc.return_statement.pos,
                )
            )

    # If Statement
    def visit_IfStmt(self, node: po.IfStmt, env: Env | None = None):
        if self.eval(node.condition, env).truthy():
            self.eval(node.body, Env(node, env))
            return
        for elif_stmt in node.elif_statements:
            if self.eval(elif_stmt.condition, env).truthy():
                self.eval(elif_stmt.body, Env(node, env))
                return
        if node.else_body:
            self.eval(node.else_body, Env(node, env))

    # While Statement
    def visit_WhileStmt(self, node: po.WhileStmt, env: Env | None = None):
        while self.eval(node.condition, env).truthy():
            self.eval(node.body, Env(node, env))

    # For Statement
    def visit_ForStmt(self, node: po.ForStmt, env: Env | None = None):
        source = self.eval(node.source, env)

        if not isinstance(source, Collection):
            self._error_handler.handle_error(
                RuntimeException(
                    f"Source should be a collection, got {source.__class__.__qualname__}",
                    pos=node.source.pos,
                )
            )

        new_env = Env(node, env)
        new_env.define(node.var.val, None)
        for element in source.elements:
            new_env.set(node.var.name, element)
            self.eval(node.body, new_env)

    # Return Statement
    def visit_ReturnStmt(self, node: po.ReturnStmt, env: Env | None = None):
        value = None
        if node.value:
            value = self.eval(node.value, env)
        raise ReturnSignal(node, value)

    # Normal Assignment
    def visit_NormalAssignmentStmt(
        self, node: po.NormalAssignmentStmt, env: Env | None = None
    ):
        value = self.eval(node.r_value, env)
        ident = node.l_value

        if ident.value in env.symbols:
            env.set(ident.value, value)
        else:
            env.define(ident.value, value)

    # Plus Assignment
    def visit_PlusAssignmentStmt(
        self, node: po.PlusAssignmentStmt, env: Env | None = None
    ):
        name = node.l_value.value
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
    def visit_MinusAssignmentStmt(
        self, node: po.MinusAssignmentStmt, env: Env | None = None
    ):
        name = node.l_value.value
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
    def visit_OrExpr(self, node: po.OrExpr, env: Env | None = None):
        if self.eval(node.l_value, env).truthy():
            return BoolValue(True)

        if self.eval(node.r_value, env).truthy():
            return BoolValue(True)

        return BoolValue(False)

    # And Expr
    def visit_AndExpr(self, node: po.AndExpr, env: Env | None = None):
        if not self.eval(node.l_value, env).truthy():
            return BoolValue(False)

        if not self.eval(node.r_value, env).truthy():
            return BoolValue(False)

        return BoolValue(True)

    # Eq Expr
    def visit_EqExpr(self, node: po.EqExpr, env: Env | None = None):
        l_value = self.eval(node.l_value, env)
        r_value = self.eval(node.r_value, env)

        return BoolValue(l_value == r_value)

    # Neq Expr
    def visit_NeqExpr(self, node: po.NeqExpr, env: Env | None = None):
        l_value = self.eval(node.l_value, env)
        r_value = self.eval(node.r_value, env)

        return BoolValue(l_value != r_value)

    # Gt Expr
    def visit_GtExpr(self, node: po.GtExpr, env: Env | None = None):
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
    def visit_GeqExpr(self, node: po.GeqExpr, env: Env | None = None):
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
    def visit_LtExpr(self, node: po.LtExpr, env: Env | None = None):
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
    def visit_LeqExpr(self, node: po.LeqExpr, env: Env | None = None):
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
    def visit_AddExpr(self, node: po.AddExpr, env: Env | None = None):
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
    def visit_SubExpr(self, node: po.SubExpr, env: Env | None = None):
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
    def visit_MulExpr(self, node: po.MulExpr, env: Env | None = None):
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
    def visit_DivExpr(self, node: po.DivExpr, env: Env | None = None):
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
    def visit_LogicNegExpr(self, node: po.LogicNegExpr, env: Env | None = None):
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
    def visit_ArithNegExpr(self, node: po.ArithNegExpr, env: Env | None = None):
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
    def visit_AccessExpr(self, node: po.AccessExpr, env: Env | None = None):
        src = self.eval(node.source, env)
        field = node.target.value

        method_sig = src.__class__.__qualname__ + "." + field
        try:
            method = env.get(method_sig)
        except ValueError:
            self._error_handler.handle_error(
                RuntimeException(
                    f"Object of type '{src.type_of()}' has no '{field}' method",
                    pos=node.pos,
                )
            )
        method.owner = src
        return method

    # Call Expr
    def visit_CallExpr(self, node: po.CallExpr, env: Env | None = None):
        function: FuncValue = self.eval(node.callee, env)

        if not isinstance(function, FuncValue):
            self._error_handler.handle_error(
                RuntimeException(
                    f"Object '{function.__class__.__qualname__}' is not a function",
                    pos=node.callee.pos,
                )
            )

        arg_objects = [self.eval(arg, env) for arg in node.args]

        params = self.check_params(arg_objects, function)
        if params is None:
            raise RuntimeException(
                msg=f"No '{function.name}' function override with [{[f"'{call_arg.type_of()}'," for call_arg in arg_objects]}] types found",
                pos=node.pos,
            )

        try:
            if isinstance(function, UserFuncValue):
                func_env = Env(env)

                for name, arg in zip(params, arg_objects):
                    func_env.define(
                        name, deepcopy(arg) if is_simple(arg) else arg
                    )
                self.eval(function.body, func_env)

            if isinstance(function, BuiltInFuncValue):
                if function.needs_inter:
                    raise ReturnSignal(function.body(self.visit_body, Env(env), *arg_objects))
                else:
                    raise ReturnSignal(function.body(*arg_objects))

            if isinstance(function, AccessedFuncValue):
                if function.needs_inter:
                    raise ReturnSignal(function.body(self.visit_body, Env(env), function.owner, *arg_objects))
                else:
                    raise ReturnSignal(function.body(function.owner, *arg_objects))

        except RuntimeException as exc:
            exc.pos = node.pos
            self._error_handler.handle_error(exc)
        except IndexError as exc:
            self._error_handler.handle_error(
                RuntimeException(
                    exc.args[0],
                    pos=node.pos,
                )
            )
        except ReturnSignal as exc:
            return exc.return_value

    # Int Expr
    def visit_IntExpr(self, node: po.IntExpr, env: Env | None = None):
        return IntValue(node.value)

    # Float Expr
    def visit_FloatExpr(self, node: po.FloatExpr, env: Env | None = None):
        return FloatValue(node.value)

    # String Expr
    def visit_StringExpr(self, node: po.StringExpr, env: Env | None = None):
        return StringValue(node.value)

    # Identifier
    def visit_Identifier(self, node: po.Identifier, env: Env | None = None):
        return env.get(node.value)

    # Bool Expr
    def visit_BoolExpr(self, node: po.BoolExpr, env: Env | None = None):
        return BoolValue(node.value)

    # List Expr
    def visit_ListExpr(self, node: po.ListExpr, env: Env | None = None):
        elements = []
        for element in node.elements:
            object = self.eval(element, env)
            elements.append(object)

        return ListValue(elements)

    # Item Expr
    def visit_ItemExpr(self, node: po.ItemExpr, env: Env | None = None):
        key = self.eval(node.key, env)
        value = self.eval(node.value, env)

        return ItemValue(key, value)

    # Dict Expr
    def visit_DictExpr(self, node: po.DictExpr, env: Env | None = None):
        dict = DictValue([], lambda _, __: IntValue(1))

        for parser_item in node.items:
            interpreter_item = self.eval(parser_item, env)
            dict.add(interpreter_item)

        return dict

    # Function expr
    def visit_FunctionExpr(self, node: po.FunctionExpr, env: Env | None = None):
        param_names = [ident.value for ident in node.params]
        return UserFuncValue([param_names], node.body)

    # Linq expr
    def visit_LinqExpr(self, node: po.LinqExpr, env: Env | None = None):
        var = node.var
        source = self.eval(node.source, env)

        if not isinstance(source, Collection):
            self._error_handler.handle_error(
                RuntimeException(
                    f"Source should be a collection, got {source.__class__.__qualname__}",
                    pos=node.source.pos,
                )
            )

        new_env = Env(node, env)
        new_env.define(var.value, None)

        return_list = []

        for element in source.elements:
            new_env.set(var.value, element)

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
            selects = ListValue([self.eval(sel, new_env) for sel in node.selects])

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
    def visit_BracketsExpr(self, node: po.BracketsExpr, env: Env | None = None):
        return self.eval(node.value, env)
