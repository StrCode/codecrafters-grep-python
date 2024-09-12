import sys

# import pyparsing - available if you need it!
# import lark - available if you need it!


def match_pattern(input_line, pattern):
    if len(pattern) == 1:
        return pattern in input_line
    elif pattern == "\\d":
        return any(char.isdigit() for char in input_line)
    elif pattern == "\\w":
        return input_line.isalnum()
    elif pattern[0] == "[" and pattern[-1] == "]":
        if pattern[1] == "^":
            return not any(char in pattern for char in input_line)
        return any(char in pattern for char in input_line)
    else:
        raise RuntimeError(f"Unhandled pattern: {pattern}")


def match(input_line, pattern):
    if pattern.startswith("^"):
        return matchhere(input_line, pattern[1:])
    elif matchhere(input_line, pattern):
        return True
    return False


def matchhere(input_line, pattern):
    if len(input_line) == 0 and len(pattern) > 0:
        return False
    elif len(pattern) == 0:
        return True
    elif pattern[:2] == "\\d":
        num = None
        for i in range(len(input_line)):
            char = input_line[i]
            if char.isdigit():
                num = i
                break
        if num is not None:
            char = input_line[num]
            return matchhere(input_line[num + 1 :], pattern[2:])
    elif pattern[:2] == "\\w":
        num = None
        for i in range(len(input_line)):
            char = input_line[i]
            if char.isalnum():
                num = i
                break
        if num is not None:
            char = input_line[num]
            return matchhere(input_line[num + 1 :], pattern[2:])
    elif pattern[0] == "[":
        if "]" not in pattern[1:]:
            return False
        index = pattern.find("]")
        result = False
        if pattern[1] == "^":
            result = not any(char in pattern[2:index] for char in input_line)
            if result:
                return matchhere(input_line, pattern[index + 1 :])
            else:
                return False
        result = any(char in pattern[1:index] for char in input_line)
        if result:
            return matchhere(input_line, pattern[index + 1 :])
        return False

    elif pattern[0]:
        if pattern[0] != input_line[0]:
            return False
        if input_line[1:] is not None:
            return matchhere(input_line[1:], pattern[1:])
        else:
            return False
    else:
        return True


def main():
    pattern = sys.argv[2]
    input_line = sys.stdin.read()

    if sys.argv[1] != "-E":
        print("Expected first argument to be '-E'")
        exit(1)

    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    # Uncomment this block to pass the first stage
    if match(input_line, pattern):
        exit(0)
    else:
        exit(1)


if __name__ == "__main__":
    main()
