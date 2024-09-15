import sys

# import pyparsing - available if you need it!
# import lark - available if you need it!


def match(input_line, pattern):
    if pattern.startswith("^"):
        if not (start_of_line(input_line, pattern[1:])):
            return False
        return matchhere(input_line, pattern[1:])
    elif matchhere(input_line, pattern):
        return True
    return False
    # raise RuntimeError(f"Unhandled pattern: {pattern}")


def matchhere(input_line, pattern):
    print(f"Starting input_line: {input_line}, pattern: {pattern}")
    if len(input_line) == 0 and len(pattern) > 0:
        if pattern[0] == "$":
            return True
        return False
    elif len(pattern) == 0:
        return True
    elif len(pattern) > 1 and pattern[1] == "+":
        if pattern[0] != input_line[0]:
            return False
        while input_line[0] == pattern[0]:
            input_line = input_line[1:]
        return matchhere(input_line, pattern[2:])
    elif len(pattern) > 1 and pattern[1] == "?":
        while input_line[0] == pattern[0]:
            input_line = input_line[1:]
        return matchhere(input_line, pattern[2:])
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
        if pattern[0] != input_line[0] and len(input_line) < 2:
            return False
        elif pattern[0] != input_line[0] and input_line[1:] is not None:
            print("samuel")
            print(input_line[1:])
            print(pattern)
            return matchhere(input_line[1:], pattern)
        elif pattern[0] == input_line[0] and input_line[1:] is not None:
            return matchhere(input_line[1:], pattern[1:])
        elif pattern[0] == input_line[0]:
            return matchhere(input_line[1:], pattern[1:])
        else:
            return False
    else:
        return True


def start_of_line(input_line, pattern):
    if input_line[0] != pattern[0]:
        return False
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
        print("True")
        exit(0)
    else:
        print("False")
        exit(1)


if __name__ == "__main__":
    main()
