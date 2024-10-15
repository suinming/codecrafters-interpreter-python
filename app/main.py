import sys


def main():
    if len(sys.argv) < 3:
        print("Usage: ./your_program.sh tokenize <filename>", file=sys.stderr)
        exit(1)

    command = sys.argv[1]
    filename = sys.argv[2]

    if command != "tokenize":
        print(f"Unknown command: {command}", file=sys.stderr)
        exit(1)

    with open(filename) as file:
        file_contents = file.read()

    invalid_token_exist = False
    p = 0
    while len(file_contents):
        c = file_contents[p]
        if c == "(":
            print("LEFT_PAREN ( null")
        elif c == ")":
            print("RIGHT_PAREN ) null")
        elif c == "{":
            print("LEFT_BRACE { null")
        elif c == "}":
            print("RIGHT_BRACE } null")
        elif c == "*":
            print("STAR * null")
        elif c == ".":
            print("DOT . null")
        elif c == ",":
            print("COMMA , null")
        elif c == "+":
            print("PLUS + null")
        elif c == "-":
            print("MINUS - null")
        elif c == ";":
            print("SEMICOLON ; null")
        elif c == "=":
            if p + 1 < len(file_contents) and file_contents[p + 1] == "=":
                print("EQUAL_EQUAL == null")
                p += 1
            else:
                print("EQUAL = null")
        elif c == "!":
            if p + 1 < len(file_contents) and file_contents[p + 1] == "=":
                print("BANG_EQUAL != null")
                p += 1
            else:
                print("BANG ! null")
        else:
            # invalid token
            invalid_token_exist = True
            print(
                f"[line 1] Error: Unexpected character: {c}",
                file=sys.stderr,
            )

        # increment pointer
        if p + 1 < len(file_contents):
            p += 1
        else:
            break

    print("EOF  null")

    if invalid_token_exist:
        exit(65)
    else:
        exit(0)


if __name__ == "__main__":
    main()
