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

    # general token
    t = {
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
        "/": "SLASH",
    }
    # token need advanced check
    t_advanced = {
        "=": "EQUAL",
        "!": "BANG",
        "<": "LESS",
        ">": "GREATER",
    }

    invalid_token_exist = False
    p = 0

    while len(file_contents):
        c = file_contents[p]
        if t.get(c):
            if p + 1 < len(file_contents) and file_contents[p] == "/" and file_contents[p + 1] == "/":
                # if comment detect ignore the remaining characters
                break
            else:
                print(f"{t.get(c)} {c} null")
        elif t_advanced.get(c):
            if p + 1 < len(file_contents) and file_contents[p + 1] == "=":
                print(f"{t_advanced.get(c)}_EQUAL {c}= null")
                p += 1
            else:
                print(f"{t_advanced.get(c)} {c} null")
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
