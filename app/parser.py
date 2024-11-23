# complete Lox expression grammar
# expression     → equality ;
# equality       → comparison ( ( "!=" | "==" ) comparison )* ;
# comparison     → term ( ( ">" | ">=" | "<" | "<=" ) term )* ;
# term           → factor ( ( "-" | "+" ) factor )* ;
# factor         → unary ( ( "/" | "*" ) unary )* ;
# unary          → ( "!" | "-" ) unary
#                | primary ;
# primary        → NUMBER | STRING | "true" | "false" | "nil"
#                | "(" expression ")" ;
from typing import List, TypedDict


def Binary(left, operator, right):
    return {"left": left, "operator": operator, "right": right}


def Grouping(expression, type: str):
    if type == "PAREN":
        return "(group " + expression + ")"
    if type == "BRACE":
        return "{group " + expression + "}"


def Literal(value):
    if value is None:
        return "nil"
    return str(value).lower()


def Unary(operator, right):
    return {"operator": operator, "right": right}


class TokenDict(TypedDict):
    token_type: str
    lexeme: str
    literal: str


class Parser:
    def __init__(self, tokens: List[TokenDict]) -> None:
        self.tokens = tokens
        self.cur: int = 0

    def parse(self):
        return self.expression()

    def expression(self):
        return self.equality()

    def equality(self):
        expr = self.comparison()

        while self.match("BANG_EQUAL", "EQUAL_EQUAL"):
            operator = self.previous()
            right = self.comparison()
            expr = Binary(expr, operator, right)

        return expr

    def comparison(self):
        expr = self.term()

        while self.match("GREATER", "GREATER_EQUAL", "LESS", "LESS_EQUAL"):
            operator = self.previous()
            right = self.term()
            expr = Binary(expr, operator, right)

        return expr

    def term(self):
        expr = self.factor()

        while self.match("MINUS", "PLUS"):
            operator = self.previous()
            right = self.factor()
            expr = Binary(expr, operator, right)

        return expr

    def factor(self):
        expr = self.unary()

        while self.match("SLASH", "STAR"):
            operator = self.previous()
            right = self.unary()
            expr = Binary(expr, operator, right)

        return expr

    # a bit different
    def unary(self):

        while self.match("BANG", "MINUS"):
            operator = self.previous()
            right = self.unary()
            return Unary(operator, right)

        return self.primary()

    def primary(self):
        if self.match("FALSE"):
            return Literal(False)
        if self.match("TRUE"):
            return Literal(True)
        if self.match("NIL"):
            return Literal(None)
        if self.match("NUMBER", "STRING"):
            return Literal(self.previous()["literal"])
        if self.match("LEFT_PAREN"):
            expr = self.expression()
            return Grouping(expr, "PAREN")
        if self.match("LEFT_BRACE"):
            expr = self.expression()
            return Grouping(expr, "BRACE")

    def match(self, *token_types: str) -> bool:
        for token_type in token_types:
            if self.check(token_type):
                self.advance()
                return True
        return False

    def is_at_end(self) -> bool:
        return self.cur >= len(self.tokens)

    def check(self, token_type: str) -> bool:
        if self.is_at_end():
            return False
        return token_type == self.peek()["token_type"]

    def peek(self) -> TokenDict:
        return self.tokens[self.cur]

    def advance(self) -> TokenDict:
        if not self.is_at_end():
            self.cur += 1
        return self.previous()

    def previous(self) -> TokenDict:
        return self.tokens[self.cur - 1]
