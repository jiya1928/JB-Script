# JB Language V4 - Lexer


class Token:
    def __init__(self, type_, value, line=1, column=1):
        self.type = type_
        self.value = value
        self.line = line
        self.column = column

    def __repr__(self):
        return f"Token({self.type!r}, {self.value!r})"


class LexerError(Exception):
    pass


class Lexer:
    KEYWORDS = {
        "let": "LET",
        "fn": "FN",
        "return": "RETURN",
        "if": "IF",
        "otherwise": "OTHERWISE",
        "while": "WHILE",
        "for": "FOR",
        "in": "IN",
        "break": "BREAK",
        "continue": "CONTINUE",

        # Classes
        "class": "CLASS",
        "extends": "EXTENDS",

        # Error handling
        "try": "TRY",
        "catch": "CATCH",
        "throw": "THROW",

        "true": "TRUE",
        "false": "FALSE",
        "null": "NULL",

        # Logical operators
        "and": "AND",
        "or": "OR",
        "not": "NOT",

        # Modules
        "import": "IMPORT",
    }

    TWO_CHAR_OPERATORS = {
        "==": "EQ",
        "!=": "NE",
        "<=": "LTE",
        ">=": "GTE",
        "->": "ARROW",
    }

    ONE_CHAR_TOKENS = {
        "+": "PLUS",
        "-": "MINUS",
        "*": "STAR",
        "/": "SLASH",
        "%": "PERCENT",

        "=": "ASSIGN",

        "<": "LT",
        ">": "GT",
        "!": "BANG",

        "(": "LPAREN",
        ")": "RPAREN",

        "{": "LBRACE",
        "}": "RBRACE",

        "[": "LBRACKET",
        "]": "RBRACKET",

        ",": "COMMA",
        ":": "COLON",
        ".": "DOT",
        ";": "SEMICOLON",
    }

    def __init__(self, source):
        self.source = source
        self.pos = 0
        self.line = 1
        self.column = 1
        self.tokens = []

    def current(self):
        if self.pos >= len(self.source):
            return "\0"

        return self.source[self.pos]

    def peek(self, amount=1):
        index = self.pos + amount

        if index >= len(self.source):
            return "\0"

        return self.source[index]

    def advance(self):
        char = self.current()

        self.pos += 1

        if char == "\n":
            self.line += 1
            self.column = 1
        else:
            self.column += 1

        return char

    def add_token(self, type_, value, line=None, column=None):
        self.tokens.append(
            Token(
                type_,
                value,
                line if line is not None else self.line,
                column if column is not None else self.column,
            )
        )

    def tokenize(self):
        while self.current() != "\0":
            char = self.current()

            # ------------------------------------------
            # Whitespace
            # ------------------------------------------

            if char in " \t\r":
                self.advance()
                continue

            # ------------------------------------------
            # New line
            # ------------------------------------------

            if char == "\n":
                line = self.line
                column = self.column

                self.advance()

                self.add_token(
                    "NEWLINE",
                    "\\n",
                    line,
                    column,
                )

                continue

            # ------------------------------------------
            # Comments
            # ------------------------------------------

            if char == "#":
                self.skip_comment()
                continue

            # ------------------------------------------
            # Strings
            # ------------------------------------------

            if char in ('"', "'"):
                self.read_string()
                continue

            # ------------------------------------------
            # Numbers
            # ------------------------------------------

            if char.isdigit():
                self.read_number()
                continue

            # ------------------------------------------
            # Identifiers / keywords
            # ------------------------------------------

            if char.isalpha() or char == "_":
                self.read_identifier()
                continue

            # ------------------------------------------
            # Two-character operators
            # ------------------------------------------

            pair = char + self.peek()

            if pair in self.TWO_CHAR_OPERATORS:
                line = self.line
                column = self.column

                self.advance()
                self.advance()

                self.add_token(
                    self.TWO_CHAR_OPERATORS[pair],
                    pair,
                    line,
                    column,
                )

                continue

            # ------------------------------------------
            # One-character tokens
            # ------------------------------------------

            if char in self.ONE_CHAR_TOKENS:
                line = self.line
                column = self.column

                token_type = self.ONE_CHAR_TOKENS[char]

                self.advance()

                self.add_token(
                    token_type,
                    char,
                    line,
                    column,
                )

                continue

            # ------------------------------------------
            # Unknown character
            # ------------------------------------------

            raise LexerError(
                f"Unexpected character {char!r} "
                f"at line {self.line}, column {self.column}"
            )

        # EOF
        self.add_token(
            "EOF",
            None,
            self.line,
            self.column,
        )

        return self.tokens

    # ==================================================
    # COMMENTS
    # ==================================================

    def skip_comment(self):
        while self.current() not in ("\n", "\0"):
            self.advance()

    # ==================================================
    # STRINGS
    # ==================================================

    def read_string(self):
        quote = self.current()

        line = self.line
        column = self.column

        self.advance()

        value = ""

        while self.current() != quote:
            if self.current() == "\0":
                raise LexerError(
                    f"Unterminated string at "
                    f"line {line}, column {column}"
                )

            if self.current() == "\\":
                self.advance()

                escaped = self.current()

                escapes = {
                    "n": "\n",
                    "t": "\t",
                    "r": "\r",
                    "\\": "\\",
                    '"': '"',
                    "'": "'",
                }

                value += escapes.get(
                    escaped,
                    escaped,
                )

                self.advance()

            else:
                value += self.advance()

        self.advance()

        self.add_token(
            "STRING",
            value,
            line,
            column,
        )

    # ==================================================
    # NUMBERS
    # ==================================================

    def read_number(self):
        line = self.line
        column = self.column

        number = ""
        has_dot = False

        while True:
            char = self.current()

            if char.isdigit():
                number += self.advance()

            elif (
                char == "."
                and not has_dot
                and self.peek().isdigit()
            ):
                has_dot = True
                number += self.advance()

            else:
                break

        if has_dot:
            value = float(number)
        else:
            value = int(number)

        self.add_token(
            "NUMBER",
            value,
            line,
            column,
        )

    # ==================================================
    # IDENTIFIERS / KEYWORDS
    # ==================================================

    def read_identifier(self):
        line = self.line
        column = self.column

        value = ""

        while True:
            char = self.current()

            if char.isalnum() or char == "_":
                value += self.advance()
            else:
                break

        token_type = self.KEYWORDS.get(
            value,
            "IDENTIFIER",
        )

        self.add_token(
            token_type,
            value,
            line,
            column,
        )


# ======================================================
# HELPER
# ======================================================

def tokenize(source):
    return Lexer(source).tokenize()


# ======================================================
# TEST
# ======================================================

if __name__ == "__main__":

    code = """
class Person extends Animal {
    let name = "John"

    fn greet() {
        say("Hello")
    }
}

try {
    let x = 10
} catch error {
    say(error)
}

throw "Something went wrong"
"""

    lexer = Lexer(code)

    for token in lexer.tokenize():
        print(token)