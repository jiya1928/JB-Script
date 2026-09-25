import os

from parser import (
    Program,
    NumberLiteral,
    StringLiteral,
    BooleanLiteral,
    NullLiteral,
    ArrayLiteral,
    ObjectLiteral,
    Variable,
    BinaryExpression,
    UnaryExpression,
    Assignment,
    VariableDeclaration,
    IfStatement,
    WhileStatement,
    ForStatement,
    FunctionDeclaration,
    ReturnStatement,
    BreakStatement,
    ContinueStatement,
    ExpressionStatement,
    CallExpression,
    IndexExpression,
    MemberExpression,
    ImportStatement,
    TryCatchStatement,
    ThrowStatement,
)


# ============================================================
# CONTROL FLOW SIGNALS
# ============================================================

class ReturnSignal(Exception):
    def __init__(self, value):
        self.value = value


class BreakSignal(Exception):
    pass


class ContinueSignal(Exception):
    pass


class JBThrownError(Exception):
    def __init__(self, value):
        self.value = value
        super().__init__(str(value))


# ============================================================
# JB ERROR
# ============================================================

class JBError:
    def __init__(self, error_type, message):
        self.error_type = error_type
        self.message = message

    def __str__(self):
        return f"{self.error_type}: {self.message}"

    def __repr__(self):
        return str(self)


# ============================================================
# ENVIRONMENT
# ============================================================

class Environment:
    def __init__(self, parent=None):
        self.values = {}
        self.parent = parent

    def define(self, name, value):
        self.values[name] = value

    def get(self, name):
        if name in self.values:
            return self.values[name]

        if self.parent:
            return self.parent.get(name)

        raise Exception(
            f"Undefined variable '{name}'"
        )

    def set(self, name, value):
        if name in self.values:
            self.values[name] = value
            return

        if self.parent:
            self.parent.set(name, value)
            return

        raise Exception(
            f"Undefined variable '{name}'"
        )


# ============================================================
# JB FUNCTION
# ============================================================

class JBFunction:
    def __init__(self, declaration, closure, interpreter):
        self.declaration = declaration
        self.closure = closure
        self.interpreter = interpreter

    def call(self, arguments):
        declaration = self.declaration

        if len(arguments) != len(declaration.parameters):
            raise Exception(
                f"Function '{declaration.name}' expects "
                f"{len(declaration.parameters)} arguments, "
                f"got {len(arguments)}"
            )

        environment = Environment(self.closure)

        for parameter, argument in zip(
            declaration.parameters,
            arguments
        ):
            environment.define(
                parameter,
                argument
            )

        try:
            self.interpreter.execute_block(
                declaration.body,
                environment
            )

        except ReturnSignal as signal:
            return signal.value

        return None

    def __repr__(self):
        return f"<function {self.declaration.name}>"


# ============================================================
# INTERPRETER
# ============================================================

class Interpreter:

    def __init__(self, base_path=None):
        self.global_environment = Environment()
        self.environment = self.global_environment

        self.base_path = (
            os.path.abspath(base_path)
            if base_path
            else os.getcwd()
        )

        self.module_cache = {}

        self.register_builtins()

    # ========================================================
    # BUILTINS
    # ========================================================

    def register_builtins(self):

        self.global_environment.define(
            "say",
            self.builtin_say
        )

        self.global_environment.define(
            "len",
            self.builtin_len
        )

        self.global_environment.define(
            "type",
            self.builtin_type
        )

        self.global_environment.define(
            "str",
            self.builtin_str
        )

        self.global_environment.define(
            "number",
            self.builtin_number
        )

        self.global_environment.define(
            "keys",
            self.builtin_keys
        )

        self.global_environment.define(
            "values",
            self.builtin_values
        )

        self.global_environment.define(
            "range",
            self.builtin_range
        )

        # ----------------------------------------------------
        # ERROR CONSTRUCTORS
        # ----------------------------------------------------

        self.global_environment.define(
            "Error",
            lambda message: JBError(
                "Error",
                self.stringify(message)
            )
        )

        self.global_environment.define(
            "ValueError",
            lambda message: JBError(
                "ValueError",
                self.stringify(message)
            )
        )

        self.global_environment.define(
            "TypeError",
            lambda message: JBError(
                "TypeError",
                self.stringify(message)
            )
        )

        self.global_environment.define(
            "RuntimeError",
            lambda message: JBError(
                "RuntimeError",
                self.stringify(message)
            )
        )

        self.global_environment.define(
            "NotFoundError",
            lambda message: JBError(
                "NotFoundError",
                self.stringify(message)
            )
        )

        self.global_environment.define(
            "NameError",
            lambda message: JBError(
                "NameError",
                self.stringify(message)
            )
        )

    # ========================================================
    # BUILTIN FUNCTIONS
    # ========================================================

    def builtin_say(self, *values):
        print(
            *[
                self.stringify(value)
                for value in values
            ]
        )

        return None

    def builtin_len(self, value):

        if isinstance(
            value,
            (str, list, dict)
        ):
            return len(value)

        raise Exception(
            "len() expects a string, array, or object"
        )

    def builtin_type(self, value):

        if isinstance(value, JBError):
            return "error"

        if value is None:
            return "null"

        if isinstance(value, bool):
            return "boolean"

        if isinstance(value, (int, float)):
            return "number"

        if isinstance(value, str):
            return "string"

        if isinstance(value, list):
            return "array"

        if isinstance(value, dict):
            return "object"

        if isinstance(value, JBFunction):
            return "function"

        if callable(value):
            return "function"

        return "object"

    def builtin_str(self, value):
        return self.stringify(value)

    def builtin_number(self, value):

        try:
            return float(value)

        except Exception:
            raise Exception(
                f"Cannot convert '{value}' to number"
            )

    def builtin_keys(self, value):

        if not isinstance(value, dict):
            raise Exception(
                "keys() expects an object"
            )

        return list(value.keys())

    def builtin_values(self, value):

        if not isinstance(value, dict):
            raise Exception(
                "values() expects an object"
            )

        return list(value.values())

    def builtin_range(self, *args):

        if len(args) == 1:

            return list(
                range(
                    int(args[0])
                )
            )

        if len(args) == 2:

            return list(
                range(
                    int(args[0]),
                    int(args[1])
                )
            )

        if len(args) == 3:

            return list(
                range(
                    int(args[0]),
                    int(args[1]),
                    int(args[2])
                )
            )

        raise Exception(
            "range() expects 1 to 3 arguments"
        )

    # ========================================================
    # RUN
    # ========================================================

    def run(self, source):

        from parser import Parser

        parser = Parser(source)
        program = parser.parse()

        return self.execute(program)

    # ========================================================
    # EXECUTION
    # ========================================================

    def execute(self, node):

        # ----------------------------------------------------
        # PROGRAM
        # ----------------------------------------------------

        if isinstance(node, Program):

            result = None

            for statement in node.statements:
                result = self.execute(statement)

            return result

        # ----------------------------------------------------
        # VARIABLE DECLARATION
        # ----------------------------------------------------

        if isinstance(node, VariableDeclaration):

            value = self.evaluate(
                node.value
            )

            self.environment.define(
                node.name,
                value
            )

            return value
        # ----------------------------------------------------
        # ASSIGNMENT
        # ----------------------------------------------------

        if isinstance(node, Assignment):

            value = self.evaluate(
                node.value
            )

            self.assign(
                node.target,
                value
            )

            return value
        # ----------------------------------------------------
        # EXPRESSION STATEMENT
        # ----------------------------------------------------

        if isinstance(node, ExpressionStatement):

            return self.evaluate(
                node.expression
            )

        # ----------------------------------------------------
        # FUNCTION DECLARATION
        # ----------------------------------------------------

        if isinstance(node, FunctionDeclaration):

            function = JBFunction(
                node,
                self.environment,
                self
            )

            self.environment.define(
                node.name,
                function
            )

            return function

        # ----------------------------------------------------
        # RETURN
        # ----------------------------------------------------

        if isinstance(node, ReturnStatement):

            value = None

            if node.value is not None:

                value = self.evaluate(
                    node.value
                )

            raise ReturnSignal(value)

        # ----------------------------------------------------
        # IF
        # ----------------------------------------------------

        if isinstance(node, IfStatement):

            condition = self.evaluate(
                node.condition
            )

            if self.is_truthy(condition):

                return self.execute_block(
                    node.then_branch,
                    Environment(self.environment)
                )

            if node.else_branch is not None:

                return self.execute_block(
                    node.else_branch,
                    Environment(self.environment)
                )

            return None

        # ----------------------------------------------------
        # WHILE
        # ----------------------------------------------------

        if isinstance(node, WhileStatement):

            result = None

            while self.is_truthy(
                self.evaluate(node.condition)
            ):

                try:

                    result = self.execute_block(
                        node.body,
                        Environment(self.environment)
                    )

                except ContinueSignal:

                    continue

                except BreakSignal:

                    break

            return result

        # ----------------------------------------------------
        # FOR
        # ----------------------------------------------------

        if isinstance(node, ForStatement):

            iterable = self.evaluate(
                node.iterable
            )

            if not hasattr(
                iterable,
                "__iter__"
            ):
                raise Exception(
                    "Object is not iterable"
                )

            result = None

            for item in iterable:

                loop_environment = Environment(
                    self.environment
                )

                loop_environment.define(
                    node.variable,
                    item
                )

                try:

                    result = self.execute_block(
                        node.body,
                        loop_environment
                    )

                except ContinueSignal:

                    continue

                except BreakSignal:

                    break

            return result

        # ----------------------------------------------------
        # BREAK
        # ----------------------------------------------------

        if isinstance(node, BreakStatement):

            raise BreakSignal()

        # ----------------------------------------------------
        # CONTINUE
        # ----------------------------------------------------

        if isinstance(node, ContinueStatement):

            raise ContinueSignal()

        # ----------------------------------------------------
        # IMPORT
        # ----------------------------------------------------

        if isinstance(node, ImportStatement):

            module = self.import_module(
                node.module_name
            )

            self.environment.define(
                node.module_name,
                module
            )

            return module

        # ----------------------------------------------------
        # TRY / CATCH
        # ----------------------------------------------------

        if isinstance(node, TryCatchStatement):

            try:

                return self.execute_block(
                    node.try_body,
                    Environment(self.environment)
                )

            except JBThrownError as error:

                catch_environment = Environment(
                    self.environment
                )

                catch_environment.define(
                    node.catch_variable,
                    error.value
                )

                return self.execute_block(
                    node.catch_body,
                    catch_environment
                )

        # ----------------------------------------------------
        # THROW
        # ----------------------------------------------------

        if isinstance(node, ThrowStatement):

            value = self.evaluate(
                node.value
            )

            raise JBThrownError(value)

        # ----------------------------------------------------
        # UNKNOWN STATEMENT
        # ----------------------------------------------------

        raise Exception(
            f"Unknown statement: "
            f"{type(node).__name__}"
        )

    # ========================================================
    # EXECUTE BLOCK
    # ========================================================

    def execute_block(
        self,
        statements,
        environment
    ):

        previous = self.environment

        try:

            self.environment = environment

            result = None

            for statement in statements:

                result = self.execute(
                    statement
                )

            return result

        finally:

            self.environment = previous

    # ========================================================
    # EXPRESSIONS
    # ========================================================

    def evaluate(self, node):

        # ----------------------------------------------------
        # NUMBER
        # ----------------------------------------------------

        if isinstance(node, NumberLiteral):

            return node.value

        # ----------------------------------------------------
        # STRING
        # ----------------------------------------------------

        if isinstance(node, StringLiteral):

            return node.value

        # ----------------------------------------------------
        # BOOLEAN
        # ----------------------------------------------------

        if isinstance(node, BooleanLiteral):

            return node.value

        # ----------------------------------------------------
        # NULL
        # ----------------------------------------------------

        if isinstance(node, NullLiteral):

            return None

        # ----------------------------------------------------
        # ARRAY
        # ----------------------------------------------------

        if isinstance(node, ArrayLiteral):

            return [
                self.evaluate(element)
                for element in node.elements
            ]

        # ----------------------------------------------------
        # OBJECT
        # ----------------------------------------------------

        if isinstance(node, ObjectLiteral):

            result = {}

            for key, value_node in node.properties:

                result[key] = self.evaluate(
                    value_node
                )

            return result

        # ----------------------------------------------------
        # VARIABLE
        # ----------------------------------------------------

        if isinstance(node, Variable):

            return self.environment.get(
                node.name
            )

        # ----------------------------------------------------
        # BINARY
        # ----------------------------------------------------

        if isinstance(node, BinaryExpression):

            return self.evaluate_binary(
                node
            )

        # ----------------------------------------------------
        # UNARY
        # ----------------------------------------------------

        if isinstance(node, UnaryExpression):

            return self.evaluate_unary(
                node
            )

        # ----------------------------------------------------
        # ASSIGNMENT
        # ----------------------------------------------------

        if isinstance(node, Assignment):

            value = self.evaluate(
                node.value
            )

            self.assign(
                node.target,
                value
            )

            return value

        # ----------------------------------------------------
        # CALL
        # ----------------------------------------------------

        if isinstance(node, CallExpression):

            callee = self.evaluate(
                node.callee
            )

            arguments = [
                self.evaluate(argument)
                for argument in node.arguments
            ]

            return self.call_function(
                callee,
                arguments
            )

        # ----------------------------------------------------
        # INDEX
        # ----------------------------------------------------

        if isinstance(node, IndexExpression):

            obj = self.evaluate(
                node.object_expr
            )

            index = self.evaluate(
                node.index
            )

            try:

                return obj[index]

            except Exception:

                raise Exception(
                    f"Cannot access index '{index}'"
                )

        # ----------------------------------------------------
        # MEMBER
        # ----------------------------------------------------

        if isinstance(node, MemberExpression):

            obj = self.evaluate(
                node.object_expr
            )

            return self.get_property(
                obj,
                node.property_name
            )

        # ----------------------------------------------------
        # UNKNOWN EXPRESSION
        # ----------------------------------------------------

        raise Exception(
            f"Unknown expression: "
            f"{type(node).__name__}"
        )

    # ========================================================
    # BINARY OPERATORS
    # ========================================================

    def evaluate_binary(self, node):

        operator = node.operator

        left = self.evaluate(
            node.left
        )

        # AND
        if operator == "and":

            if not self.is_truthy(left):
                return False

            return self.is_truthy(
                self.evaluate(node.right)
            )

        # OR
        if operator == "or":

            if self.is_truthy(left):
                return True

            return self.is_truthy(
                self.evaluate(node.right)
            )

        right = self.evaluate(
            node.right
        )

        if operator == "+":

            return left + right

        if operator == "-":

            return left - right

        if operator == "*":

            return left * right

        if operator == "/":

            return left / right

        if operator == "%":

            return left % right

        if operator == "==":

            return left == right

        if operator == "!=":

            return left != right

        if operator == "<":

            return left < right

        if operator == "<=":

            return left <= right

        if operator == ">":

            return left > right

        if operator == ">=":

            return left >= right

        raise Exception(
            f"Unknown operator '{operator}'"
        )

    # ========================================================
    # UNARY OPERATORS
    # ========================================================

    def evaluate_unary(self, node):

        value = self.evaluate(
            node.operand
        )

        if node.operator == "-":

            return -value

        if node.operator == "+":

            return +value

        if node.operator == "!":

            return not self.is_truthy(value)

        if node.operator == "not":

            return not self.is_truthy(value)

        raise Exception(
            f"Unknown unary operator "
            f"'{node.operator}'"
        )

    # ========================================================
    # ASSIGNMENT
    # ========================================================

    def assign(self, target, value):

        if isinstance(target, Variable):

            self.environment.set(
                target.name,
                value
            )

            return

        if isinstance(target, IndexExpression):

            obj = self.evaluate(
                target.object_expr
            )

            index = self.evaluate(
                target.index
            )

            obj[index] = value

            return

        if isinstance(target, MemberExpression):

            obj = self.evaluate(
                target.object_expr
            )

            self.set_property(
                obj,
                target.property_name,
                value
            )

            return

        raise Exception(
            "Invalid assignment target"
        )

    # ========================================================
    # PROPERTY ACCESS
    # ========================================================

    def get_property(self, obj, name):

        # ----------------------------------------------------
        # JB ERROR
        # ----------------------------------------------------

        if isinstance(obj, JBError):

            if name == "type":
                return obj.error_type

            if name == "message":
                return obj.message

            raise Exception(
                f"Error has no property '{name}'"
            )

        # ----------------------------------------------------
        # DICTIONARY / OBJECT
        # ----------------------------------------------------

        if isinstance(obj, dict):

            if name in obj:

                return obj[name]

            raise Exception(
                f"Object has no property '{name}'"
            )

        # ----------------------------------------------------
        # ARRAY
        # ----------------------------------------------------

        if isinstance(obj, list):

            if name == "length":

                return len(obj)

            if name == "push":

                return lambda value: obj.append(
                    value
                )

            if name == "pop":

                return lambda: obj.pop()

            if name == "shift":

                return lambda: obj.pop(0)

            if name == "unshift":

                return lambda value: obj.insert(
                    0,
                    value
                )

        # ----------------------------------------------------
        # STRING
        # ----------------------------------------------------

        if isinstance(obj, str):

            if name == "length":

                return len(obj)

            if name == "upper":

                return lambda: obj.upper()

            if name == "lower":

                return lambda: obj.lower()

            if name == "trim":

                return lambda: obj.strip()

        # ----------------------------------------------------
        # PYTHON OBJECT
        # ----------------------------------------------------

        if hasattr(obj, name):

            return getattr(
                obj,
                name
            )

        raise Exception(
            f"Object has no property '{name}'"
        )

    # ========================================================
    # PROPERTY SET
    # ========================================================

    def set_property(
        self,
        obj,
        name,
        value
    ):

        if isinstance(obj, dict):

            obj[name] = value

            return

        if hasattr(obj, name):

            setattr(
                obj,
                name,
                value
            )

            return

        raise Exception(
            f"Object has no property '{name}'"
        )

    # ========================================================
    # FUNCTIONS
    # ========================================================

    def call_function(
        self,
        function,
        arguments
    ):

        if isinstance(
            function,
            JBFunction
        ):

            return function.call(
                arguments
            )

        if callable(function):

            return function(
                *arguments
            )

        raise Exception(
            f"Object is not callable: {function}"
        )

    # ========================================================
    # IMPORTS
    # ========================================================

    def import_module(
        self,
        module_name
    ):

        # ----------------------------------------------------
        # WEB FRAMEWORK
        # ----------------------------------------------------

        if module_name == "web":

            from framework.web import web

            def create_web_app():

                return web(self)

            self.module_cache[
                module_name
            ] = create_web_app

            return create_web_app

        # ----------------------------------------------------
        # CACHE
        # ----------------------------------------------------

        if module_name in self.module_cache:

            return self.module_cache[
                module_name
            ]

        # ----------------------------------------------------
        # FIND MODULE
        # ----------------------------------------------------

        module_path = self.find_module(
            module_name
        )

        if module_path is None:

            raise Exception(
                f"Module not found: "
                f"{module_name}"
            )

        # ----------------------------------------------------
        # READ MODULE
        # ----------------------------------------------------

        with open(
            module_path,
            "r",
            encoding="utf-8"
        ) as file:

            source = file.read()

        # ----------------------------------------------------
        # CREATE MODULE INTERPRETER
        # ----------------------------------------------------

        module_interpreter = Interpreter(
            os.path.dirname(module_path)
        )

        module_interpreter.run(
            source
        )

        # ----------------------------------------------------
        # BUILD MODULE OBJECT
        # ----------------------------------------------------

        module = {}

        for name, value in (
            module_interpreter
            .global_environment
            .values
            .items()
        ):

            module[name] = value

        self.module_cache[
            module_name
        ] = module

        return module

    # ========================================================
    # FIND MODULE
    # ========================================================

    def find_module(
        self,
        module_name
    ):

        possible_paths = [

            os.path.join(
                self.base_path,
                module_name + ".jb"
            ),

            os.path.join(
                self.base_path,
                "stdlib",
                module_name + ".jb"
            ),

            os.path.join(
                os.getcwd(),
                module_name + ".jb"
            ),

            os.path.join(
                os.getcwd(),
                "stdlib",
                module_name + ".jb"
            ),
        ]

        for path in possible_paths:

            if os.path.isfile(path):

                return path

        return None

    # ========================================================
    # HELPERS
    # ========================================================

    def is_truthy(self, value):

        return bool(value)

    def stringify(self, value):

        if isinstance(value, JBError):

            return str(value)

        if value is None:

            return "null"

        if value is True:

            return "true"

        if value is False:

            return "false"

        if isinstance(value, list):

            return "[" + ", ".join(
                self.stringify(item)
                for item in value
            ) + "]"

        if isinstance(value, dict):

            items = []

            for key, item in value.items():

                items.append(
                    f"{key}: "
                    f"{self.stringify(item)}"
                )

            return "{" + ", ".join(
                items
            ) + "}"

        if isinstance(
            value,
            JBFunction
        ):

            return repr(value)

        return str(value)