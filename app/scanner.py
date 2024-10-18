import sys


class Scanner:
    def __init__(self, file: str):
        self.file = file
        self.start = 0
        self.cur = 0
        self.line = 1
        self.invalid_token_exist = False
        self.token_tab = {
            "(": "LEFT_PAREN",
            ")": "RIGHT_PAREN",
            "{": "LEFT_BRACE",
            "}": "RIGHT_BRACE",
            "*": "STAR",
            ".": "DOT",
            ",": "COMMA",
            "+": "PLUS",
            "-": "MINUS",
            ";": "SEMICOLON",
        }
        self.token_match_tab = {
            "=": "EQUAL",
            "!": "BANG",
            "<": "LESS",
            ">": "GREATER",
        }

    def advance(self) -> str:
        c = self.file[self.cur]
        self.cur += 1
        return c

    def peek(self):
        """like the advance, but do not consume the character"""
        if self.is_at_end():
            return "\0"
        return self.file[self.cur]

    def is_at_end(self) -> bool:
        return self.cur >= len(self.file)

    def add_token(self, token_type: str, lexeme: str, literal="null"):
        print(f"{token_type} {lexeme} {literal}")

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
            self.invalid_token_exist = True
            print(
                f"[line {self.line}] Error: Unexpected character: {c}",
                file=sys.stderr,
            )

    def scan_tokens(self):
        while not self.is_at_end():
            self.start = self.cur
            self.scan_token()

        print("EOF  null")

        if self.invalid_token_exist:
            exit(65)
        else:
            exit(0)
