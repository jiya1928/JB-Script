# JB Language V4 - Parser

from lexer import Lexer


# ============================================================
# AST NODES
# ============================================================

class Program:
    def __init__(self, statements):
        self.statements = statements


class NumberLiteral:
    def __init__(self, value):
        self.value = value


class StringLiteral:
    def __init__(self, value):
        self.value = value


class BooleanLiteral:
    def __init__(self, value):
        self.value = value


class NullLiteral:
    pass


class ArrayLiteral:
    def __init__(self, elements):
        self.elements = elements


class ObjectLiteral:
    def __init__(self, properties):
        self.properties = properties


class Variable:
    def __init__(self, name):
        self.name = name


class BinaryExpression:
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right


class UnaryExpression:
    def __init__(self, operator, operand):
        self.operator = operator
        self.operand = operand


class Assignment:
    def __init__(self, target, value):
        self.target = target
        self.value = value


class VariableDeclaration:
    def __init__(self, name, value):
        self.name = name
        self.value = value


class IfStatement:
    def __init__(self, condition, then_branch, else_branch=None):
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch


class WhileStatement:
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body


class ForStatement:
    def __init__(self, variable, iterable, body):
        self.variable = variable
        self.iterable = iterable
        self.body = body


class FunctionDeclaration:
    def __init__(self, name, parameters, body):
        self.name = name
        self.parameters = parameters
        self.body = body


# ============================================================
# CLASS AST
# ============================================================

class ClassDeclaration:
    def __init__(self, name, parent, members):
        self.name = name
        self.parent = parent
        self.members = members


class ClassProperty:
    def __init__(self, name, value):
        self.name = name
        self.value = value


class ClassMethod:
    def __init__(self, name, parameters, body):
        self.name = name
        self.parameters = parameters
        self.body = body


class ReturnStatement:
    def __init__(self, value):
        self.value = value


class BreakStatement:
    pass


class ContinueStatement:
    pass


class ExpressionStatement:
    def __init__(self, expression):
        self.expression = expression


class CallExpression:
    def __init__(self, callee, arguments):
        self.callee = callee
        self.arguments = arguments


class IndexExpression:
    def __init__(self, object_expr, index):
        self.object_expr = object_expr
        self.index = index


class MemberExpression:
    def __init__(self, object_expr, property_name):
        self.object_expr = object_expr
        self.property_name = property_name


class ImportStatement:
    def __init__(self, module_name):
        self.module_name = module_name


class TryCatchStatement:
    def __init__(self, try_body, catch_variable, catch_body):
        self.try_body = try_body
        self.catch_variable = catch_variable
        self.catch_body = catch_body


class ThrowStatement:
    def __init__(self, value):
        self.value = value


# ============================================================
# PARSER
# ============================================================

class Parser:

    def __init__(self, source):
        self.tokens = Lexer(source).tokenize()
        self.position = 0

    # ========================================================
    # TOKEN HELPERS
    # ========================================================

    def current(self):
        if self.position >= len(self.tokens):
            return self.tokens[-1]

        return self.tokens[self.position]

    def peek(self, offset=1):
        index = self.position + offset

        if index >= len(self.tokens):
            return self.tokens[-1]

        return self.tokens[index]

    def advance(self):
        token = self.current()

        if self.position < len(self.tokens):
            self.position += 1

        return token

    def check(self, token_type):
        return self.current().type == token_type

    def match(self, *token_types):
        if self.current().type in token_types:
            return self.advance()

        return None

    def consume(self, token_type, message):
        token = self.current()

        if token.type != token_type:
            raise SyntaxError(
                f"{message}, got {token.type} "
                f"({token.value!r}) at line {token.line}"
            )

        self.position += 1

        return token

    def skip_newlines(self):
        while self.check("NEWLINE"):
            self.advance()

    # ========================================================
    # PROGRAM
    # ========================================================

    def parse(self):
        statements = []

        self.skip_newlines()

        while not self.check("EOF"):
            statements.append(self.parse_statement())
            self.skip_newlines()

        return Program(statements)

    # ========================================================
    # STATEMENTS
    # ========================================================

    def parse_statement(self):
        self.skip_newlines()

        token = self.current()

        if token.type == "LET":
            return self.parse_variable_declaration()

        if token.type == "FN":
            return self.parse_function_declaration()

        if token.type == "CLASS":
            return self.parse_class_declaration()

        if token.type == "IF":
            return self.parse_if()

        if token.type == "WHILE":
            return self.parse_while()

        if token.type == "FOR":
            return self.parse_for()

        if token.type == "RETURN":
            return self.parse_return()

        if token.type == "BREAK":
            self.advance()
            return BreakStatement()

        if token.type == "CONTINUE":
            self.advance()
            return ContinueStatement()

        if token.type == "IMPORT":
            return self.parse_import()

        if token.type == "TRY":
            return self.parse_try_catch()

        if token.type == "THROW":
            return self.parse_throw()

        expression = self.parse_expression()

        if self.match("ASSIGN"):
            value = self.parse_expression()

            return Assignment(
                expression,
                value
            )

        return ExpressionStatement(expression)

    # ========================================================
    # VARIABLE DECLARATION
    # ========================================================

    def parse_variable_declaration(self):
        self.consume(
            "LET",
            "Expected 'let'"
        )

        name = self.consume(
            "IDENTIFIER",
            "Expected variable name"
        )

        self.consume(
            "ASSIGN",
            "Expected '=' after variable name"
        )

        value = self.parse_expression()

        return VariableDeclaration(
            name.value,
            value
        )

    # ========================================================
    # FUNCTION
    # ========================================================

    def parse_function_declaration(self):
        self.consume(
            "FN",
            "Expected 'fn'"
        )

        name = self.consume(
            "IDENTIFIER",
            "Expected function name"
        )

        parameters = self.parse_parameters()

        body = self.parse_block()

        return FunctionDeclaration(
            name.value,
            parameters,
            body
        )

    # ========================================================
    # FUNCTION PARAMETERS
    # ========================================================

    def parse_parameters(self):
        self.consume(
            "LPAREN",
            "Expected '(' after function name"
        )

        parameters = []

        self.skip_newlines()

        if not self.check("RPAREN"):

            while True:

                parameter = self.consume(
                    "IDENTIFIER",
                    "Expected parameter name"
                )

                parameters.append(
                    parameter.value
                )

                self.skip_newlines()

                if not self.match("COMMA"):
                    break

                self.skip_newlines()

        self.consume(
            "RPAREN",
            "Expected ')' after parameters"
        )

        return parameters

    # ========================================================
    # CLASS
    # ========================================================

    def parse_class_declaration(self):
        self.consume(
            "CLASS",
            "Expected 'class'"
        )

        name = self.consume(
            "IDENTIFIER",
            "Expected class name"
        )

        parent = None

        self.skip_newlines()

        # class Student extends Person
        if self.match("EXTENDS"):

            parent_token = self.consume(
                "IDENTIFIER",
                "Expected parent class name after 'extends'"
            )

            parent = parent_token.value

        self.skip_newlines()

        self.consume(
            "LBRACE",
            "Expected '{' after class declaration"
        )

        members = []

        self.skip_newlines()

        while not self.check("RBRACE") and not self.check("EOF"):

            # Class method
            if self.check("FN"):
                members.append(
                    self.parse_class_method()
                )

            # Class property
            elif self.check("IDENTIFIER"):

                members.append(
                    self.parse_class_property()
                )

            # Allow `let` inside class too
            elif self.check("LET"):

                members.append(
                    self.parse_class_property_with_let()
                )

            else:

                token = self.current()

                raise SyntaxError(
                    f"Unexpected token in class body: "
                    f"{token.type} ({token.value!r}) "
                    f"at line {token.line}"
                )

            self.skip_newlines()

        self.consume(
            "RBRACE",
            "Expected '}' after class body"
        )

        return ClassDeclaration(
            name.value,
            parent,
            members
        )

    # ========================================================
    # CLASS PROPERTY
    # ========================================================

    def parse_class_property(self):
        name = self.consume(
            "IDENTIFIER",
            "Expected property name"
        )

        self.consume(
            "ASSIGN",
            "Expected '=' after property name"
        )

        value = self.parse_expression()

        return ClassProperty(
            name.value,
            value
        )

    # ========================================================
    # CLASS PROPERTY WITH LET
    # ========================================================

    def parse_class_property_with_let(self):
        self.consume(
            "LET",
            "Expected 'let'"
        )

        name = self.consume(
            "IDENTIFIER",
            "Expected property name"
        )

        self.consume(
            "ASSIGN",
            "Expected '=' after property name"
        )

        value = self.parse_expression()

        return ClassProperty(
            name.value,
            value
        )

    # ========================================================
    # CLASS METHOD
    # ========================================================

    def parse_class_method(self):
        self.consume(
            "FN",
            "Expected 'fn'"
        )

        name = self.consume(
            "IDENTIFIER",
            "Expected method name"
        )

        parameters = self.parse_parameters()

        body = self.parse_block()

        return ClassMethod(
            name.value,
            parameters,
            body
        )

    # ========================================================
    # IF
    # ========================================================

    def parse_if(self):
        self.consume(
            "IF",
            "Expected 'if'"
        )

        condition = self.parse_expression()

        then_branch = self.parse_block()

        else_branch = None

        self.skip_newlines()

        if self.match("OTHERWISE"):
            else_branch = self.parse_block()

        return IfStatement(
            condition,
            then_branch,
            else_branch
        )

    # ========================================================
    # WHILE
    # ========================================================

    def parse_while(self):
        self.consume(
            "WHILE",
            "Expected 'while'"
        )

        condition = self.parse_expression()

        body = self.parse_block()

        return WhileStatement(
            condition,
            body
        )

    # ========================================================
    # FOR
    # ========================================================

    def parse_for(self):
        self.consume(
            "FOR",
            "Expected 'for'"
        )

        variable = self.consume(
            "IDENTIFIER",
            "Expected loop variable"
        )

        self.consume(
            "IN",
            "Expected 'in' in for loop"
        )

        iterable = self.parse_expression()

        body = self.parse_block()

        return ForStatement(
            variable.value,
            iterable,
            body
        )

    # ========================================================
    # RETURN
    # ========================================================

    def parse_return(self):
        self.consume(
            "RETURN",
            "Expected 'return'"
        )

        if self.check("NEWLINE") or self.check("RBRACE"):
            return ReturnStatement(None)

        value = self.parse_expression()

        return ReturnStatement(value)

    # ========================================================
    # IMPORT
    # ========================================================

    def parse_import(self):
        self.consume(
            "IMPORT",
            "Expected 'import'"
        )

        module = self.consume(
            "IDENTIFIER",
            "Expected module name"
        )

        return ImportStatement(
            module.value
        )

    # ========================================================
    # TRY / CATCH
    # ========================================================

    def parse_try_catch(self):
        self.consume(
            "TRY",
            "Expected 'try'"
        )

        try_body = self.parse_block()

        self.skip_newlines()

        self.consume(
            "CATCH",
            "Expected 'catch' after try block"
        )

        catch_variable = self.consume(
            "IDENTIFIER",
            "Expected error variable after 'catch'"
        )

        catch_body = self.parse_block()

        return TryCatchStatement(
            try_body,
            catch_variable.value,
            catch_body
        )

    # ========================================================
    # THROW
    # ========================================================

    def parse_throw(self):
        self.consume(
            "THROW",
            "Expected 'throw'"
        )

        value = self.parse_expression()

        return ThrowStatement(value)

    # ========================================================
    # BLOCK
    # ========================================================

    def parse_block(self):
        self.consume(
            "LBRACE",
            "Expected '{'"
        )

        statements = []

        self.skip_newlines()

        while not self.check("RBRACE") and not self.check("EOF"):

            statements.append(
                self.parse_statement()
            )

            self.skip_newlines()

        self.consume(
            "RBRACE",
            "Expected '}'"
        )

        return statements

    # ========================================================
    # EXPRESSIONS
    # ========================================================

    def parse_expression(self):
        return self.parse_or()

    # ========================================================
    # OR
    # ========================================================

    def parse_or(self):
        expression = self.parse_and()

        while self.match("OR"):

            right = self.parse_and()

            expression = BinaryExpression(
                expression,
                "or",
                right
            )

        return expression

    # ========================================================
    # AND
    # ========================================================

    def parse_and(self):
        expression = self.parse_equality()

        while self.match("AND"):

            right = self.parse_equality()

            expression = BinaryExpression(
                expression,
                "and",
                right
            )

        return expression

    # ========================================================
    # EQUALITY
    # ========================================================

    def parse_equality(self):
        expression = self.parse_comparison()

        while self.check("EQ") or self.check("NE"):

            token = self.advance()

            right = self.parse_comparison()

            expression = BinaryExpression(
                expression,
                token.value,
                right
            )

        return expression

    # ========================================================
    # COMPARISON
    # ========================================================

    def parse_comparison(self):
        expression = self.parse_term()

        while self.current().type in (
            "LT",
            "LTE",
            "GT",
            "GTE"
        ):

            token = self.advance()

            right = self.parse_term()

            expression = BinaryExpression(
                expression,
                token.value,
                right
            )

        return expression

    # ========================================================
    # TERM
    # ========================================================

    def parse_term(self):
        expression = self.parse_factor()

        while self.current().type in (
            "PLUS",
            "MINUS"
        ):

            token = self.advance()

            right = self.parse_factor()

            expression = BinaryExpression(
                expression,
                token.value,
                right
            )

        return expression

    # ========================================================
    # FACTOR
    # ========================================================

    def parse_factor(self):
        expression = self.parse_unary()

        while self.current().type in (
            "STAR",
            "SLASH",
            "PERCENT"
        ):

            token = self.advance()

            right = self.parse_unary()

            expression = BinaryExpression(
                expression,
                token.value,
                right
            )

        return expression

    # ========================================================
    # UNARY
    # ========================================================

    def parse_unary(self):

        if self.current().type in (
            "MINUS",
            "BANG",
            "NOT"
        ):

            token = self.advance()

            operand = self.parse_unary()

            return UnaryExpression(
                token.value,
                operand
            )

        return self.parse_postfix()

    # ========================================================
    # POSTFIX
    # ========================================================

    def parse_postfix(self):

        expression = self.parse_primary()

        while True:

            # Function call
            if self.match("LPAREN"):

                arguments = []

                self.skip_newlines()

                if not self.check("RPAREN"):

                    while True:

                        arguments.append(
                            self.parse_expression()
                        )

                        self.skip_newlines()

                        if not self.match("COMMA"):
                            break

                        self.skip_newlines()

                self.consume(
                    "RPAREN",
                    "Expected ')' after arguments"
                )

                expression = CallExpression(
                    expression,
                    arguments
                )

            # Array/object indexing
            elif self.match("LBRACKET"):

                index = self.parse_expression()

                self.consume(
                    "RBRACKET",
                    "Expected ']' after index"
                )

                expression = IndexExpression(
                    expression,
                    index
                )

            # Property access
            elif self.match("DOT"):

                property_name = self.consume(
                    "IDENTIFIER",
                    "Expected property name after '.'"
                )

                expression = MemberExpression(
                    expression,
                    property_name.value
                )

            else:
                break

        return expression

    # ========================================================
    # PRIMARY
    # ========================================================

    def parse_primary(self):

        token = self.current()

        # Number
        if token.type == "NUMBER":

            self.advance()

            return NumberLiteral(
                token.value
            )

        # String
        if token.type == "STRING":

            self.advance()

            return StringLiteral(
                token.value
            )

        # True
        if token.type == "TRUE":

            self.advance()

            return BooleanLiteral(True)

        # False
        if token.type == "FALSE":

            self.advance()

            return BooleanLiteral(False)

        # Null
        if token.type == "NULL":

            self.advance()

            return NullLiteral()

        # Identifier
        if token.type == "IDENTIFIER":

            self.advance()

            return Variable(
                token.value
            )

        # Array
        if token.type == "LBRACKET":
            return self.parse_array()

        # Object
        if token.type == "LBRACE":
            return self.parse_object()

        # Parenthesized expression
        if token.type == "LPAREN":

            self.advance()

            expression = self.parse_expression()

            self.consume(
                "RPAREN",
                "Expected ')' after expression"
            )

            return expression

        raise SyntaxError(
            f"Unexpected token {token.type} "
            f"({token.value!r}) at line {token.line}"
        )

    # ========================================================
    # ARRAY
    # ========================================================

    def parse_array(self):

        self.consume(
            "LBRACKET",
            "Expected '['"
        )

        elements = []

        self.skip_newlines()

        if not self.check("RBRACKET"):

            while True:

                elements.append(
                    self.parse_expression()
                )

                self.skip_newlines()

                if not self.match("COMMA"):
                    break

                self.skip_newlines()

        self.consume(
            "RBRACKET",
            "Expected ']' after array"
        )

        return ArrayLiteral(elements)

    # ========================================================
    # OBJECT
    # ========================================================

    def parse_object(self):

        self.consume(
            "LBRACE",
            "Expected '{'"
        )

        properties = []

        self.skip_newlines()

        while not self.check("RBRACE"):

            if self.check("IDENTIFIER"):
                key = self.advance().value

            elif self.check("STRING"):
                key = self.advance().value

            else:

                token = self.current()

                raise SyntaxError(
                    f"Expected object key, got {token.type} "
                    f"({token.value!r}) at line {token.line}"
                )

            self.consume(
                "COLON",
                "Expected ':' after object key"
            )

            value = self.parse_expression()

            properties.append(
                (key, value)
            )

            self.skip_newlines()

            if self.match("COMMA"):
                self.skip_newlines()
                continue

            break

        self.skip_newlines()

        self.consume(
            "RBRACE",
            "Expected '}'"
        )

        return ObjectLiteral(properties)


# ============================================================
# HELPER
# ============================================================

def parse(source):
    return Parser(source).parse()


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    source = """
class Person {
    name = "John"
    age = 20

    fn greet() {
        say("Hello " + self.name)
    }
}

class Student extends Person {
    school = "JB Academy"

    fn study() {
        say("Studying")
    }
}
"""

    try:
        tree = parse(source)

        print("PARSER SUCCESS")
        print(
            f"Statements: {len(tree.statements)}"
        )

        for statement in tree.statements:

            if isinstance(statement, ClassDeclaration):

                print(
                    f"Class: {statement.name}"
                )

                if statement.parent:
                    print(
                        f"  Extends: {statement.parent}"
                    )

                for member in statement.members:

                    if isinstance(
                        member,
                        ClassProperty
                    ):
                        print(
                            f"  Property: {member.name}"
                        )

                    elif isinstance(
                        member,
                        ClassMethod
                    ):
                        print(
                            f"  Method: {member.name}"
                        )

    except Exception as error:

        print("PARSER ERROR:")
        print(error)