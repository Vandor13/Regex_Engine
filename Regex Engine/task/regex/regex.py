# write your code here
import sys

sys.setrecursionlimit(10000)


# returns rest of regex, rest of string and result as boolean
def check_next_character_regex(regex, string):
    if len(regex) > 1 and regex[1] in ["?", "*", "+"]:
        return check_next_special_character_regex(regex, string)
    # Only single character has to be checked
    else:
        if len(regex) == 0 or \
                (regex[0] == "." and len(string) > 0) or \
                regex[0] == string[0]:
            return regex[1:], string[1:], True
        else:
            return regex, string[1:], False


# returns rest of regex, rest of string and result as boolean for special operators
def check_next_special_character_regex(regex, string):
    character = regex[0]
    operator = regex[1]
    if operator == "?":
        if string[0] == character or character == ".":
            return regex[2:], string[1:], True
        else:
            return regex[2:], string, True
    elif operator == "*":
        if len(string) > 0 and (string[0] == character or character == "."):
            return check_next_special_character_regex(regex, string[1:])
        else:
            return regex[2:], string, True
    elif operator == "+":
        if len(string) > 0 and (string[0] == character or character == "."):
            _, rest_string, _ = check_next_special_character_regex(regex, string[1:])
            return regex[2:], rest_string, True
        else:
            return regex, string, False
    else:
        print("Unknown operator!")
        return regex, string, False


def check_regex_substring(regex, string, mode="", escaped=False):
    # if regex is empty, the regex was found. Exception: Mode with $, string has to be empty too
    if len(regex) == 0 and ("$" not in mode or len(string) == 0):
        return True
    # in mode $ we don't accept a regex with rest of input
    elif "$" in mode and len(regex) == 0 and len(string) > 0:
        return False
    elif len(string) == 0 != len(regex) and not (len(regex) > 2 and regex[1] in ["?", "*"]):
        return False

    # Handle escape characters
    if not escaped and len(regex) > 0 and regex[0] == "\\":
        return check_regex_substring(regex[1:], string, mode, True)

    # Very special case where next char is . followed by repetition character
    if len(regex) > 1 and regex[0] == "." and regex[1] in ["*", "+"]:
        operator = regex[1]
        # Case: Rest of string can be ANY character
        if operator == "*" and len(regex) == 2:
            return True
        # Case: Rest of string can be ANY character, but must be at least one char
        elif operator == "+" and len(regex) == 2 and len(string) > 0:
            return True
        else:
            # In this special case any substring has to be True for the rest of regex
            result = False
            for i in range(len(string)):
                if check_regex_substring(regex[2:], string[i:], mode):
                    result = True
            return result
    else:
        rest_regex, rest_string, result = check_next_character_regex(regex, string)
        if not result:
            return False
        else:
            return check_regex_substring(rest_regex, rest_string, mode)


def check_regex_mode(regex):
    mode = ""
    if regex[0] == "^":
        regex = regex[1:]
        mode += "^"
    if regex[-1] == "$":
        regex = regex[:-1]
        mode += "$"
    return regex, mode


def regex_check_start(regex, string):
    if len(regex) > 0:
        regex, mode = check_regex_mode(regex)
    else:
        mode = ""
    if "^" in mode:
        # In ^ mode the beginning of the string must fit the regex
        return check_regex_substring(regex, string, mode)
    if len(regex) == 0:
        return True
    for i in range(len(string)):
        if check_regex_substring(regex, string[i:], mode):
            return True
    return False


input_regex, input_string = input().split("|")
print(regex_check_start(input_regex, input_string))
# print(single_char_regex("a", "a"))
