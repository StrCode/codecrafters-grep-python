import sys

# import pyparsing - available if you need it!
# import lark - available if you need it!


def match_pattern(input_line, pattern):
    if len(pattern) == 1:
        return pattern in input_line
    elif len(pattern) > 1:
        return match_here(input_line, pattern)
    else:
        raise RuntimeError(f"Unhandled pattern: {pattern}")


def match_here(input_line, pattern):
    line_number = 0
    result = False
    while len(pattern) != 0:
        if pattern[0] == "[":
            index = pattern.find("]")
            result = any([char in pattern[line_number:index] for char in input_line])
            if pattern[1] == "^":
                result = not result
            pattern = pattern[index + 1 :]

        elif pattern[0] == "^":
            if pattern[1] != input_line[line_number]:
                result = False
                return False
            pattern = pattern[1:]
            result = True

        elif pattern[:2].endswith("+"):
            print(pattern[:2])
            prefix = pattern[0]
            print(prefix)
            print("line number", input_line[line_number])
            if pattern[0] != input_line[line_number]:
                result = False
                break
            while prefix == input_line[line_number]:
                line_number += 1
            result = True
            input_line[line_number:]
            pattern = pattern[2:]

        elif pattern[:2].endswith("?"):
            prefix = pattern[0]
            print(prefix)
            if pattern[0] == input_line[line_number]:
                line_number += 1
            print(input_line[line_number:])
            result = True
            print("input line", input_line[line_number:])
            pattern = pattern[2:]

        elif pattern[0] == "$":
            if len(input_line[line_number:]) > 0:
                result = False
            else:
                result = True
            pattern = pattern[1:]

        elif pattern[:2] == "\\d":
            pattern = pattern[2:]
            while len(input_line[line_number:]) > 0:
                char = input_line[line_number]
                line_number += 1
                if char.isdigit():
                    result = True
                    break

        elif pattern[:2] == "\\w":
            pattern = pattern[2:]
            while len(input_line[line_number:]) > 0:
                char = input_line[line_number]
                line_number += 1
                if char.isalnum():
                    result = True
                    break

        elif len(pattern) > 0:
            if pattern[0] != input_line[line_number]:
                result = False
            else:
                pattern = pattern[1:]
            line_number += 1
        else:
            return False

    return result


def main():
    pattern = sys.argv[2]
    input_line = sys.stdin.read()

    if sys.argv[1] != "-E":
        print("Expected first argument to be '-E'")
        exit(1)

    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    # Uncomment this block to pass the first stage
    if match_pattern(input_line, pattern):
        exit(0)
    else:
        exit(1)


if __name__ == "__main__":
    main()
