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

    def add_token(self, token: str, token_name: str):
        print(f"{token_name} {token} null")

    def match(self, expected_token) -> bool:
        if self.is_at_end():
            return False
        if self.file[self.cur] != expected_token:
            return False
        self.cur += 1
        return True

    def scan_token(self):
        c: str = self.advance()
        if c in self.token_tab:
            self.add_token(token=c, token_name=self.token_tab.get(c, ""))
        elif c in self.token_match_tab:
            token: str = c
            token_name: str = self.token_match_tab.get(c, "")
            if self.match("="):
                self.add_token(token=f"{token}=", token_name=f"{token_name}_EQUAL")
            else:
                self.add_token(token=c, token_name=token_name)
        elif c == "/":
            if self.match("/"):
                # detect the comment syntax(which is "//"), and comment go until the end of the line
                while self.peek() != "\n" and not self.is_at_end():
                    self.advance()
            else:
                self.add_token(token=c, token_name="SLASH")
        elif c in [" ", "\t", "\r"]:
            pass
        elif c == "\n":
            self.line += 1
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
