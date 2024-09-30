import sys

# import pyparsing - available if you need it!
# import lark - available if you need it!

groups = []


# Python3 code to Check for
# balanced parentheses in an expression
def check(expression):
    open_tup = tuple("({[")
    close_tup = tuple(")}]")
    map = dict(zip(open_tup, close_tup))
    queue = []

    for i in expression:
        if i in open_tup:
            queue.append(map[i])
        elif i in close_tup:
            if not queue or i != queue.pop():
                return False
    if not queue:
        return True
    else:
        return False


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
        if pattern.startswith("[^"):
            index = pattern.find("]")
            times = 0
            notseen = False

            if (
                len(pattern) > index + 1
                and pattern[index + 1]
                and pattern[index + 1] == "+"
            ):
                for char in pattern[2:index]:
                    if len(input_line[line_number:]) == 0:
                        result = False
                        break
                    elif char not in input_line[line_number]:
                        print("char", char, "inputline", input_line[line_number])
                        line_number += 1
                        result = True
                    else:
                        result = False
                        break

                pattern = pattern[index + 2 :]
                break

            for char in input_line:
                if char in pattern[line_number:index] and notseen is True:
                    notseen = False
                    if times != 0:
                        result = False
                        break
                if char is not pattern[line_number:index]:
                    result = True
                    notseen = True
                times += 1
                line_number += 1

            pattern = pattern[index + 1 :]

        elif pattern[0] == "[":
            index = pattern.find("]")
            times = 0
            seen = False

            if (
                len(pattern) > index + 1
                and pattern[index + 1]
                and pattern[index + 1] == "+"
            ):
                for char in pattern[1:index]:
                    if len(input_line[line_number:]) == 0:
                        result = False
                        break
                    elif char in input_line[line_number]:
                        line_number += 1
                        result = True
                    else:
                        result = False
                        break

                pattern = pattern[index + 2 :]
                break

            for char in input_line:
                if char not in pattern[line_number:index] and seen is True:
                    seen = False
                    if times != 0:
                        result = False
                    break
                if char in pattern[line_number:index]:
                    result = True
                    seen = True
                times += 1
                line_number += 1

            pattern = pattern[index + 1 :]

        elif pattern[0] == "(":
            index = pattern.find(")")

            if "|" in pattern[1:index]:
                separator = pattern[1:index].find("|")
                first_word = pattern[1 : separator + 1]
                second_word = pattern[separator + 2 : index]

                f_w_result = match_pattern(input_line, first_word)
                s_w_result = match_pattern(input_line, second_word)

                if not (f_w_result or s_w_result):
                    return False

                if f_w_result:
                    pattern = first_word + pattern[index + 1 :]

                if s_w_result:
                    pattern = second_word + pattern[index + 1 :]

                groups.append(pattern)
                result = True
                break

            i = line_number + 1
            print("pattern to search for", pattern[1:index])
            print("input to search", input_line[line_number:])

            found = False

            if pattern[1:index].isalnum():
                while found is False or i < len(input_line):
                    print("hit here")
                    print(
                        "Match now:",
                        input_line[line_number:i],
                        "Pattern:",
                        pattern[1:index],
                    )
                    rel = match_pattern(input_line[line_number:i], pattern[1:index])
                    print("main=rel:", rel)
                    if rel:
                        result = True
                        found = True
                        break
                    i += 1

            else:
                while i < len(input_line):
                    print(
                        "Match now:",
                        input_line[line_number:i],
                        "Pattern:",
                        pattern[1:index],
                    )
                    rel = match_pattern(input_line[line_number:i], pattern[1:index])
                    print("sam-main=rel:", rel)
                    if rel:
                        found = True
                    else:
                        i += 1
                        if found is True:
                            result = True
                            break

            groups.append(input_line[line_number:i])
            print("Next stage:", pattern[index + 1 :])
            pattern = pattern[index + 1 :]
            line_number = i
            print("next input line:", input_line[line_number:], "Groups:", groups)

        elif pattern.startswith("^("):
            pattern = pattern[1:]
            result = True

        elif pattern[0] == "^":
            if pattern[1] != input_line[line_number]:
                result = False
                return False
            pattern = pattern[1:]
            result = True

        elif pattern[:1] == "\\" and pattern[1].isdigit():
            pattern = pattern.replace(f"\\{pattern[1]}", groups[int(pattern[1]) - 1])

        elif pattern[0] == ".":
            line_number += 1
            pattern = pattern[1:]
            result = True

        elif pattern[:2] == "\\d":
            pattern = pattern[2:]

            if pattern[:2].endswith("+"):
                while input_line[line_number].isdigit():
                    line_number += 1
                result = True
                input_line[line_number:]
                pattern = pattern[2:]
                break

            if len(input_line[line_number:]) == 0:
                result = False
                break

            if input_line[line_number].isdigit():
                line_number += 1
                result = True
            else:
                result = False

        elif pattern[:2] == "\\w":
            pattern = pattern[2:]

            if pattern[:2].endswith("+"):
                print("we just got it here and i have this")
                while (
                    len(input_line[line_number:]) != 0
                    and input_line[line_number].isalnum()
                ):
                    line_number += 1
                    result = True
                if len(input_line[line_number:]) == 0:
                    result = True
                    break

            if len(input_line[line_number:]) == 0:
                result = False
                break

            if input_line[line_number].isalnum() and not pattern[:2].endswith("+"):
                line_number += 1
                result = True
            else:
                result = False
                break

        elif pattern[:2].endswith("+"):
            prefix = pattern[0]
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
            if pattern[0] == input_line[line_number]:
                line_number += 1
            result = True
            pattern = pattern[2:]

        elif pattern[0] == "$":
            if len(input_line[line_number:]) > 0:
                result = False
            else:
                result = True
            pattern = pattern[1:]

        elif len(pattern) > 0:
            if len(input_line[line_number:]) == 0 and len(pattern) > 0:
                result = False
                break
            elif len(pattern) == 0 and len(input_line[line_number:]) > 0:
                result = False
                break
            elif pattern[0] != input_line[line_number]:
                result = False
            elif pattern[0] == input_line[line_number]:
                print(pattern[0], input_line[line_number])
                pattern = pattern[1:]
                result = True
            line_number += 1

        else:
            return result

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
        print("True")
        exit(0)
    else:
        print("False")
        exit(1)


if __name__ == "__main__":
    main()
