import sys

from app.constants import KEYWORDS, TOKEN_MATCH_TAB, TOKEN_TAB


class TokenScanner:
    def __init__(self, file: str):
        self.file = file
        self.start = 0
        self.cur = 0
        self.line = 1
        self.invalid_token_exist = False
        self.tokens = list()
        self.token_tab = TOKEN_TAB
        self.token_match_tab = TOKEN_MATCH_TAB
        self.keywords = KEYWORDS

    def scan_tokens(self):
        while not self.is_at_end():
            self.start = self.cur
            self.scan_token()

    def scan_token(self):
        c: str = self.advance()
        if c in self.token_tab:
            self.add_token(self.token_tab.get(c, ""), c)
        elif c in self.token_match_tab:
            token_type: str = self.token_match_tab.get(c, "")
            if self.match("="):
                self.add_token(f"{token_type}_EQUAL", f"{c}=")
            else:
                self.add_token(token_type, c)
        elif c == "/":
            if self.match("/"):
                # detect the comment syntax(which is "//"), and comment go until the end of the line
                while self.peek() != "\n" and not self.is_at_end():
                    self.advance()
            else:
                self.add_token("SLASH", c)
        elif c in [" ", "\t", "\r"]:
            pass
        elif c == "\n":
            self.line += 1
        elif c == '"':
            self.string()
        else:
            if self.is_digit(c):
                self.number()
            elif self.is_alpha(c):
                self.identifier()
            else:
                self.invalid_token_exist = True
                print(
                    f"[line {self.line}] Error: Unexpected character: {c}",
                    file=sys.stderr,
                )

    def is_at_end(self) -> bool:
        return self.cur >= len(self.file)

    def advance(self) -> str:
        c = self.file[self.cur]
        self.cur += 1
        return c

    def peek(self):
        """like the advance, but do not consume the character"""
        if self.is_at_end():
            return "\0"
        return self.file[self.cur]

    def peek_next(self):
        """check the token at pointer=(self.cur + 1)"""
        if self.cur + 1 >= len(self.file):
            return "\0"
        return self.file[self.cur + 1]

    def add_token(self, token_type: str, lexeme: str, literal: str | float = "null"):
        self.tokens.append(
            {"token_type": token_type, "lexeme": lexeme, "literal": literal}
        )

    def match(self, expected_token) -> bool:
        if self.is_at_end():
            return False
        if self.file[self.cur] != expected_token:
            return False
        self.cur += 1
        return True

    def string(self):
        while self.peek() != '"' and not self.is_at_end():
            self.advance()

        if self.is_at_end():
            print(
                f"[line {self.line}] Error: Unterminated string.",
                file=sys.stderr,
            )
            self.invalid_token_exist = True
            return

        # get the closing quote
        self.advance()

        complete_str_with_quotes = self.file[self.start : self.cur]
        complete_str = self.file[self.start + 1 : self.cur - 1]
        self.add_token("STRING", complete_str_with_quotes, complete_str)

    def is_digit(self, c: str) -> bool:
        """if the ASCII of c is within '0' and '9' then c is a digit"""
        return "0" <= c <= "9"

    def number(self):
        while self.is_digit(self.peek()):
            self.advance()

        # make sure the token after "." is a digit
        if self.peek() == "." and self.is_digit(self.peek_next()):
            # consume the "." token
            self.advance()
            # fraction part
            while self.is_digit(self.peek()):
                self.advance()

        self.add_token(
            "NUMBER",
            self.file[self.start : self.cur],
            float(self.file[self.start : self.cur]),
        )

    def is_alpha(self, c: str) -> bool:
        is_lower_case_alpha = True if "a" <= c <= "z" else False
        is_capital_case_alpha = True if "A" <= c <= "Z" else False
        is_underline = True if c == "_" else False
        return is_lower_case_alpha or is_capital_case_alpha or is_underline

    def is_alpha_numeric(self, c: str) -> bool:
        return self.is_alpha(c) or self.is_digit(c)

    def identifier(self):
        while self.is_alpha_numeric(self.peek()):
            self.advance()
        text = self.file[self.start : self.cur]
        token_type = self.keywords.get(text, None)
        # check if token exist in the keywords table. Otherwise, it’s a regular user-defined identifier.
        if token_type:
            self.add_token(token_type, self.file[self.start : self.cur], "null")
        else:
            self.add_token("IDENTIFIER", self.file[self.start : self.cur], "null")
