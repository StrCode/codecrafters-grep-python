import sys

from app.try1 import matchhere

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
                print("Samuel")
                print("Testing Pattern", pattern[1:index])
                print("Testing Input", input_line)

                for char in pattern[1:index]:
                    if (
                        len(input_line[line_number:]) > 0
                        and char in input_line[line_number]
                    ):
                        input_line = input_line[1:]
                    else:
                        return False

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
                    if len(input_line) > 0 and char in input_line[0]:
                        input_line = input_line[1:]
                    else:
                        return False

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

                f_w_result = matchhere(input_line, first_word)
                s_w_result = matchhere(input_line, second_word)

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
            while found is False and i < len(input_line):
                print(
                    "Match now:",
                    input_line[line_number:i],
                    "Pattern:",
                    pattern[1:index],
                )
                rel = match_pattern(input_line[line_number:i], pattern[1:index])
                print("main-rel-loop:", rel)
                if rel:
                    found = True
                    result = True
                    break
                i += 1

            groups.append(input_line[line_number:i])
            print("Next stage:", pattern[index + 1 :])
            pattern = pattern[index + 1 :]
            line_number = i
            print("next input line:", input_line[line_number:], "Groups:", groups)

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

        elif pattern[:2] == "\\d":
            pattern = pattern[2:]

            # while len(input_line[line_number:]) > 0:
            #     char = input_line[line_number]
            #     line_number += 1
            #     if char.isdigit():
            #         result = True
            #         break
            #     else:
            #         result = False
            #         break

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

            # while len(input_line[line_number:]) > 0:
            #     char = input_line[line_number]
            #     line_number += 1
            #     if char.isalnum():
            #         result = True
            #         break
            #     else:
            #         result = False
            if len(input_line[line_number:]) == 0:
                result = False
                break

            if input_line[line_number].isalnum():
                line_number += 1
                result = True
            else:
                result = False
                break

        elif len(pattern) > 0:
            if len(input_line[line_number:]) == 0 and len(pattern) > 0:
                print("i am here ")
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
