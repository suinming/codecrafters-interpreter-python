import sys

from app.token_scanner import TokenScanner 
from app.parser import Parser
from app.scanner import Scanner


def main():
    if len(sys.argv) < 3:
        print("Usage: ./your_program.sh tokenize <filename>", file=sys.stderr)
        exit(1)

    command = sys.argv[1]
    filename = sys.argv[2]

    valid_commands = ["tokenize", "parse"]

    if command not in valid_commands:
        print(f"Unknown command: {command}", file=sys.stderr)
        exit(1)

    # read the file
    with open(filename) as file:
        file_content = file.read()

    # execute based on command
    if command == "tokenize":
        scanner = Scanner(file_content)
        scanner.scan_tokens()
    elif command == "parse":
        lexer = TokenScanner(file_content)
        lexer.scan_tokens()
        parser = Parser(lexer.tokens)
        print(parser.parse())


if __name__ == "__main__":
    main()
