import sys

# import pyparsing - available if you need it!
# import lark - available if you need it!

groups = []


def match(input_line, pattern):
    if pattern.startswith("^") and pattern[1] not in "[]()":
        if not start_of_line(input_line, pattern[1:]):
            return False
        return matchhere(input_line, pattern[1:])
    elif matchhere(input_line, pattern):
        return True
    return False
    # raise RuntimeError(f"Unhandled pattern: {pattern}")


def matchhere(input_line, pattern, exactMatch=False):
    if len(input_line) == 0 and len(pattern) > 0:
        if pattern[0] == "$":
            return True
        return False
    elif len(pattern) == 0:
        if len(input_line) > 0 and exactMatch:
            return False
        return True
    elif len(pattern) == 1 and pattern[0] == "+":
        return True
    elif len(pattern) > 1 and pattern[1] == "+":
        if pattern[0] != input_line[0]:
            return False
        while len(input_line) > 0 and input_line[0] == pattern[0]:
            input_line = input_line[1:]
        return matchhere(input_line, pattern[2:])

    elif pattern[0] == "^":
        return matchhere(input_line, pattern[1:])

    elif pattern[0] == "(":
        end_bracket_index = pattern.find(")")

        if "|" in pattern[:end_bracket_index]:
            alternation_index = pattern.find("|")
            first_word = pattern[1:alternation_index]

            second_word = pattern[alternation_index + 1 : end_bracket_index]

            word = None
            fw_result = matchhere(input_line, first_word)
            sw_result = matchhere(input_line, second_word)

            if (fw_result or sw_result) is False:
                return False

            if fw_result:
                word = first_word

            if sw_result:
                word = second_word

            groups.append(word)

            return matchhere(input_line, word + pattern[end_bracket_index + 1 :])

        if pattern[1:end_bracket_index].isalpha():
            groups.append(pattern[1:end_bracket_index])
            return matchhere(
                input_line,
                pattern[1:end_bracket_index] + pattern[end_bracket_index + 1 :],
                True,
            )

        result = False
        input = ""
        end_point = 0
        for i in range(len(input_line)):
            end_point = i
            if i + 1 == len(input_line):
                break
            rel = matchhere(input_line[: i + 1], pattern[1:end_bracket_index], True)
            if rel:
                input += input_line[i]
                result = True
                if input_line[i + 1] == " " or not input_line[i + 1].isalnum():
                    break
            if rel is False and result is True:
                break
            else:
                if i + 1 == len(input_line):
                    break
        if result is True:
            groups.append(input)
            return matchhere(
                input_line[end_point:],
                pattern[end_bracket_index + 1 :],
            )
        else:
            return False

    elif len(pattern) > 1 and pattern[1] == "?":
        value = 0
        while len(input_line) > 0 and input_line[0] == pattern[0] and value == 0:
            input_line = input_line[1:]
            value += 1
        if len(input_line) > 0 and input_line[0] == pattern[0]:
            return False
        return matchhere(input_line, pattern[2:], exactMatch)

    elif pattern[0] == "\\" and pattern[1] is not None and pattern[1].isdigit():
        backreference = f"\\{pattern[1]}"
        return matchhere(
            input_line, pattern.replace(backreference, groups[int(pattern[1]) - 1])
        )

    elif pattern[0] == ".":
        return matchhere(input_line[1:], pattern[1:])

    elif pattern[:2] == "\\d":
        if len(pattern) >= 3 and pattern[2] == "+":
            while len(input_line) != 0 and input_line[0].isdigit():
                input_line = input_line[1:]
            return matchhere(input_line, pattern[3:], exactMatch)

        else:
            num = None
            for i in range(len(input_line)):
                char = input_line[i]
                if char.isdigit():
                    num = i
                    break
            if num is not None:
                return matchhere(input_line[num + 1 :], pattern[2:], exactMatch)
            else:
                return False

    elif pattern[:2] == "\\w":
        if len(pattern) >= 3 and pattern[2] == "+":
            while len(input_line) != 0 and input_line[0].isalnum():
                input_line = input_line[1:]
            return matchhere(input_line, pattern[3:], exactMatch)

        else:
            num = None
            for i in range(len(input_line)):
                char = input_line[i]
                if char.isalnum():
                    num = i
                    break
            if num is not None:
                return matchhere(input_line[num + 1 :], pattern[2:], exactMatch)
            else:
                return False

    elif pattern[0] == "[":
        if "]" not in pattern[1:]:
            return False
        index = pattern.find("]")
        result = False
        if pattern[1] == "^":
            result = not any(char in pattern[2:index] for char in input_line)
            if result:
                return matchhere(input_line, pattern[index + 1 :])
            return False

        if (
            len(pattern) > index + 1
            and pattern[index + 1]
            and pattern[index + 1] == "+"
        ):
            result = all(char in pattern[1:index] for char in input_line)
            if result:
                return matchhere(input_line, pattern[index + 2 :])
            return False

        result = any(char in pattern[1:index] for char in input_line)
        if result:
            return matchhere(input_line, pattern[index + 1 :])
        return False

    elif pattern[0]:
        if pattern[0] != input_line[0] and len(input_line) < 2:
            return False
        elif pattern[0] != input_line[0] and exactMatch:
            return False
        elif pattern[0] != input_line[0] and input_line[1:] is not None:
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
