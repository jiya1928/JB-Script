# JB Language V4 - AST


class ASTNode:
    pass


class Program(ASTNode):
    def __init__(self, statements):
        self.statements = statements


class NumberLiteral(ASTNode):
    def __init__(self, value):
        self.value = value


class StringLiteral(ASTNode):
    def __init__(self, value):
        self.value = value


class BooleanLiteral(ASTNode):
    def __init__(self, value):
        self.value = value


class NullLiteral(ASTNode):
    def __init__(self):
        pass


class Variable(ASTNode):
    def __init__(self, name):
        self.name = name


class ArrayLiteral(ASTNode):
    def __init__(self, elements):
        self.elements = elements


class ObjectLiteral(ASTNode):
    def __init__(self, pairs):
        self.pairs = pairs


class BinaryExpression(ASTNode):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right


class UnaryExpression(ASTNode):
    def __init__(self, operator, operand):
        self.operator = operator
        self.operand = operand


class Assignment(ASTNode):
    def __init__(self, target, value):
        self.target = target
        self.value = value


class VariableDeclaration(ASTNode):
    def __init__(self, name, value):
        self.name = name
        self.value = value


class FunctionDeclaration(ASTNode):
    def __init__(self, name, parameters, body):
        self.name = name
        self.parameters = parameters
        self.body = body


class FunctionCall(ASTNode):
    def __init__(self, function, arguments):
        self.function = function
        self.arguments = arguments


class MemberExpression(ASTNode):
    def __init__(self, object_expr, property_name):
        self.object = object_expr
        self.property = property_name


class IndexExpression(ASTNode):
    def __init__(self, object_expr, index):
        self.object = object_expr
        self.index = index


class ReturnStatement(ASTNode):
    def __init__(self, value):
        self.value = value


class IfStatement(ASTNode):
    def __init__(
        self,
        condition,
        body,
        otherwise_body=None
    ):
        self.condition = condition
        self.body = body
        self.otherwise_body = otherwise_body


class WhileStatement(ASTNode):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body


class ForStatement(ASTNode):
    def __init__(self, variable, iterable, body):
        self.variable = variable
        self.iterable = iterable
        self.body = body


class BreakStatement(ASTNode):
    def __init__(self):
        pass


class ContinueStatement(ASTNode):
    def __init__(self):
        pass


class ImportStatement(ASTNode):
    def __init__(self, module_name):
        self.module_name = module_name


class TryCatchStatement(ASTNode):
    def __init__(
        self,
        try_body,
        catch_variable,
        catch_body
    ):
        self.try_body = try_body
        self.catch_variable = catch_variable
        self.catch_body = catch_body


class ThrowStatement(ASTNode):
    def __init__(self, value):
        self.value = value