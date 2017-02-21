import ast
import argparse
import sys
import math
from primes import *
from commands import *


code = ""
elements = []
selector = []
sys.setrecursionlimit(5000)


def func_a(n, is_recurred=False):

    stack_len = 0
    if DEBUG and selector:
        print("selector >> " + str(selector))
    stack = []

    def pop_stack(num_s=1, n2=n, s2=stack):
        if stack:
            if DEBUG: print("stack non empty")
            return stack.pop()
        else:
            if DEBUG and not (FIRST_AFTER or NTH_ELEMENT):
                print("using a(" + str(n2 - num_s) + ") = " + str(func_a(n2 - num_s)))

            if FIRST_AFTER or NTH_ELEMENT:
                return n2

            if len(elements) == 0:
                return n2
            else:
                return func_a(n2 - num_s)

    result = None
    has_calculated = False

    try:
        has_calculated = elements[n] is not None
    except:
        has_calculated = False

    if has_calculated:
        if DEBUG: print("already initialized: " + str(elements[n]) + " at n = " + str(n))
        return elements[n]

    if len(elements) != 0 and n > len(elements) + 100:
        func_a(n - 100)

    if DEBUG:
        print("\n --- a(" + str(n) + ") --- ")
        input(FIRST_AFTER)

    pointer_position = -1
    while pointer_position < len(code) - 1:

        try:
            pointer_position += 1

            command = code[pointer_position]
            if DEBUG: print("command > " + command)
            stack_len = len(stack)

            if command == "+":
                b = pop_stack()
                a = pop_stack(2 - stack_len)
                stack.append(regular_arithmetic(a, b, "+"))

            elif command == "-":
                b = pop_stack()

                if stack:
                    a = pop_stack()
                else:
                    a, b = b, pop_stack(2 - stack_len)
                stack.append(regular_arithmetic(a, b, "-"))

            elif command == "*":
                b = pop_stack()
                a = pop_stack(2 - stack_len)
                stack.append(regular_arithmetic(a, b, "*"))

            elif command == "/":
                b = pop_stack()
                a = pop_stack(2 - stack_len)
                stack.append(regular_arithmetic(a, b, "/"))

            elif command == "_":
                a = pop_stack()
                c = single_arithmetic(a, "== 0")

                if type(c) is list:
                    stack.append([int(x) for x in c])
                else:
                    stack.append(int(c))

            elif command == "{":
                a = pop_stack()

                if type(a) is list:
                    stack.append(sorted(a))
                else:
                    stack.append(''.join(sorted(str(a))))

            elif command == "\u00A5":
                a = pop_stack()

                temp_list = []
                if type(a) is int:
                    a = str(a)

                length_of_list = len(a)

                for Q in range(0, length_of_list - 1):
                    temp_list.append(ast.literal_eval(str(a[Q + 1])) - ast.literal_eval(str(a[Q])))

                stack.append(temp_list)

            elif command == "A":
                a = pop_stack()
                c = single_arithmetic(a, "== 1")

                if type(c) is list:
                    stack.append([int(x) for x in c])
                else:
                    stack.append(int(c))

            elif command == "P":
                a = pop_stack()

                result = 1
                if type(a) is int:
                    a = str(a)

                for Q in a:
                    result *= ast.literal_eval(str(Q))

                stack.append(result)

            elif command == "Q":
                a = pop_stack()
                b = pop_stack(2 - stack_len)

                c = regular_arithmetic(a, b, "==")

                if type(c) is list:
                    stack.append([int(x) for x in c])
                else:
                    stack.append(int(c))

            elif command == "S":
                a = pop_stack()

                result = 0
                if type(a) is int:
                    a = str(a)

                for Q in a:
                    result += ast.literal_eval(str(Q))

                stack.append(result)

            elif command == "m":
                b = pop_stack()
                a = pop_stack(2 - stack_len)
                stack.append(regular_arithmetic(a, b, "**"))

            elif command == "%":
                b = pop_stack()
                a = pop_stack(2 - stack_len)
                stack.append(regular_arithmetic(a, b, "%"))

            elif command == "\u00f7":
                b = pop_stack()
                a = pop_stack(2 - stack_len)
                stack.append(regular_arithmetic(a, b, "//"))

            elif command == "\u00b2":
                a = pop_stack()
                stack.append(single_arithmetic(a, "** 2"))

            elif command == ">":
                a = pop_stack()
                stack.append(single_arithmetic(a, "+ 1"))

            elif command == "<":
                a = pop_stack()
                stack.append(single_arithmetic(a, "- 1"))

            elif command == "!":
                a = pop_stack()
                stack.append(math.factorial(a))

            elif command == "D":
                b = pop_stack()
                a = pop_stack(2 - stack_len)
                c = regular_arithmetic(a, b, "%")
                c = single_arithmetic(c, "== 0")

                if type(c) is list:
                    stack.append([int(x) for x in c])
                else:
                    stack.append(int(c))

            elif command == "E":
                a = pop_stack()

                if type(a) is list:
                    temp_list = []
                    for Q in a:
                        temp_list.append(convert_to_base(abs(int(Q)), 2))
                    stack.append(temp_list)
                else:
                    stack.append(convert_to_base(abs(int(a)), 2))

            elif command == "n":
                stack.append(n)

            elif command == "a":
                x = pop_stack()
                if type(x) is list:
                    temp_list = []
                    for Q in x:
                        temp_list.append(func_a(Q))
                    stack.append(temp_list)
                else:
                    stack.append(func_a(x))

            elif command == "R":
                try:
                    if type(stack[-1]) is list:
                        current_list = pop_stack()
                        temp_list = []
                        is_inclusive = False
                        for N in range(0, len(current_list) - 1):
                            b = int(current_list[N])
                            a = int(current_list[N + 1])
                            temp_list_2 = []
                            if int(b) > int(a):
                                for Q in range(int(a), int(b) + 1):
                                    temp_list_2.append(Q)
                                temp_list_2 = temp_list_2[::-1]
                            else:
                                for Q in range(int(b), int(a) + 1):
                                    temp_list_2.append(Q)
                            for Q in temp_list_2:
                                if is_inclusive and len(temp_list_2) > 1:
                                    is_inclusive = False
                                    continue
                                temp_list.append(Q)
                            is_inclusive = True
                    else:
                        if len(stack) > 1:
                            a, b = pop_stack(), pop_stack()
                        else:
                            b, a = pop_stack(), pop_stack()
                        temp_list = []
                        if int(b) > int(a):
                            for Q in range(int(a), int(b) + 1):
                                temp_list.append(Q)
                            temp_list = temp_list[::-1]
                        else:
                            for Q in range(int(b), int(a) + 1):
                                temp_list.append(Q)
                except:
                    a = pop_stack()
                    if type(a) is list:
                        current_list = a
                        temp_list = []
                        is_inclusive = False
                        for N in range(0, len(current_list) - 1):
                            b = int(current_list[N])
                            a = int(current_list[N + 1])
                            temp_list_2 = []
                            if int(b) > int(a):
                                for Q in range(int(a), int(b) + 1):
                                    temp_list_2.append(Q)
                                temp_list_2 = temp_list_2[::-1]
                            else:
                                for Q in range(int(b), int(a) + 1):
                                    temp_list_2.append(Q)
                            for Q in temp_list_2:
                                if is_inclusive and len(temp_list_2) > 1:
                                    is_inclusive = False
                                    continue
                                temp_list.append(Q)
                            is_inclusive = True
                    else:
                        b, a = a, pop_stack()
                        temp_list = []
                        if int(b) > int(a):
                            for Q in range(int(a), int(b) + 1):
                                temp_list.append(Q)
                            temp_list = temp_list[::-1]
                        else:
                            for Q in range(int(b), int(a) + 1):
                                temp_list.append(Q)

                stack.append(temp_list)

            elif command == "b":
                stack.append(func_a(n - 1))

            elif command == "c":
                stack.append(func_a(n - 2))

            elif command == "d":
                stack.append(func_a(n - 3))

            elif command == "e":
                x = pop_stack()
                stack.append(func_a(n - x))

            elif command == "\u00e0":
                stack.append(func_a(n - 1))
                stack.append(func_a(n - 2))

            elif command == "\u00e1":
                stack.append(func_a(n - 2))
                stack.append(func_a(n - 1))

            elif command == "i":

                if len(stack) > 0:
                    b = pop_stack()
                    a = pop_stack(2 - stack_len)
                else:
                    a = pop_stack()
                    b = pop_stack()

                if type(a) is list:
                    a = [str(x) for x in a]
                else:
                    a = str(a)

                stack.append(int(str(b) in a))

            elif command == "j":
                a = pop_stack()
                stack.append(largest_divisor(a))

            elif command == "p":
                a = pop_stack()
                stack.append(is_prime(a))

            elif command == "q":

                a = pop_stack()

                if -1 < a < 9999:
                    stack.append(primes_100000[a])
                else:
                    if a < 0:
                        stack.append(0)
                    else:
                        current_num = 104729
                        prime_count = 10000
                        while prime_count < a + 1:
                            current_num += 2
                            if is_prime(current_num):
                                prime_count += 1
                        stack.append(current_num)

            elif command == "s":
                a = pop_stack()
                b = pop_stack(2 - stack_len)

                stack.append(b)
                stack.append(a)

            elif command == "x":

                a = pop_stack()
                stack.append(single_arithmetic(a, "* 2"))

            elif command == "y":

                a = pop_stack()
                stack.append(single_arithmetic(a, "* 3"))

            elif command == "z":

                a = pop_stack()
                stack.append(single_arithmetic(a, "* 4"))

            elif command == "t":
                a = pop_stack()
                stack.append(single_arithmetic(a, "/ 2"))

            elif command == "u":
                a = pop_stack()
                stack.append(single_arithmetic(a, "/ 3"))

            elif command == "v":
                a = pop_stack()
                stack.append(single_arithmetic(a, "// 2"))

            elif command == "w":
                a = pop_stack()
                stack.append(single_arithmetic(a, "// 3"))

            elif command == "\"":
                temp_string = ""
                temp_string_2 = ""
                temp_position = pointer_position
                while temp_position < len(code) - 1:
                    temp_position += 1
                    try:
                        current_command = code[temp_position]
                    except:
                        break
                    if current_command == "\"":
                        break
                    elif current_command == "\u00ff":
                        temp_string += str(pop_stack(1))
                        pointer_position += 1
                    else:
                        temp_string += current_command
                        pointer_position += 1
                pointer_position += 1
                stack.append(temp_string)

            elif command == "C":
                b = pop_stack()
                a = pop_stack()

                if type(b) is not list:
                    b = str(b)

                if type(a) is not list:
                    a = str(a)

                stack.append(a.count(b))

            elif command == "G":
                a = pop_stack()

                if type(a) is not list:
                    a = str(a)

                result = []
                temp = ""
                prev = a[0]

                for Q in a + "\0":
                    if Q == prev:
                        temp += Q
                    else:
                        prev = Q
                        result.append(temp)
                        temp = Q

                stack.append(result)

            elif command == "l":
                a = pop_stack()

                if type(a) is not list:
                    a = str(a)

                stack.append(len(a))

            elif command == "L":
                temp_list = []
                a = pop_stack()
                if type(a) is list:
                    for Q in a:
                        Q = int(Q)
                        if Q > 0:
                            for X in range(1, Q + 1):
                                temp_list.append(X)
                        elif Q < 0:
                            for X in range(1, (Q * -1) + 1):
                                temp_list.append(X * -1)
                        else:
                            temp_list.append(0)
                else:
                    a = int(a)
                    if a > 0:
                        for X in range(1, a + 1):
                            temp_list.append(X)
                    elif a < 0:
                        for X in range(1, (a * -1) + 1):
                            temp_list.append(X * -1)
                    else:
                        temp_list.append(0)

                stack.append(temp_list)

            elif command == "\u00ab":

                a = pop_stack()
                stack.append(single_arithmetic(a, "- 2"))

            elif command == "\u00bb":

                a = pop_stack()
                stack.append(single_arithmetic(a, "+ 2"))

            elif command.isnumeric():
                temp_number = ""
                temp_number += command
                temp_position = pointer_position

                while temp_position < len(code) - 1:
                    temp_position += 1
                    try:
                        current_command = code[temp_position]
                    except:
                        break

                    if is_digit_value(current_command):
                        temp_number += current_command
                        pointer_position += 1
                    else:
                        break

                stack.append(int(temp_number))

            if DEBUG:
                print("stack >> " + str(stack))
        except:
            pass

    if stack:
        if DEBUG: print(" --- fin ---")

        while True:
            try:
                elements[n] = stack[-1]
                break
            except:
                elements.append(None)

        return stack[-1]
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('-d', '--debug', help="Debug mode", action="store_true")
    parser.add_argument('-s', '--safe', help="Safe mode", action="store_true")
    parser.add_argument('-c', '--cp1252', help="Encode from CP-1252", action="store_true")
    parser.add_argument('-t', '--time', help="Time the program", action="store_true")
    parser.add_argument('-q', '--start-with-one', help="Start with n = 1", action="store_true")
    parser.add_argument('-T', '--is-truthy', help="Checks each condition whether the value is truthy or falsy", action="store_true")
    parser.add_argument('-n', '--first-after', help="Get the first element after input that satisfies each condition", action="store_true")
    parser.add_argument('-N', '--nth-element', help="Get the nth element that satisfies the condition", action="store_true")
    parser.add_argument('-o', '--add-one', help="Add one to the input before calculating", action="store_true")
    parser.add_argument('-O', '--sub-one', help="Subtract one to the input before calculating", action="store_true")
    parser.add_argument("program_path", help="Program path", type=str)

    args, num = parser.parse_known_args()
    filename = args.program_path
    DEBUG = args.debug
    SAFE_MODE = args.safe
    ENCODE_CP1252 = args.cp1252
    TIME_IT = args.time
    FIRST_AFTER = args.first_after
    NTH_ELEMENT = args.nth_element
    IS_TRUTHY = args.is_truthy
    START_WITH_ONE = args.start_with_one

    ADD_ONE = args.add_one
    SUB_ONE = args.sub_one

    if ENCODE_CP1252:
        code = open(filename, "r", encoding="cp1252").read()
    else:
        code = open(filename, "r", encoding="utf-8").read()

    code = code.replace("T", "10")
    code = code.replace("U", "00")
    code = code.replace("V", "11")
    code = code.replace("W", "000")
    code = code.replace("X", "01")

    while is_digit_value(code[-1]) or code[-1] == "N" or code[-1] == "\u00df" or code[-1] == "\u00de":
        if code[-1] == "N":
            elements.append(None)
        elif code[-1] == "\u00df":
            code = code[:-1]
            digit = convert_from_base(code[-1], 214)
            elements.append(digit)
        elif code[-1] == "\u00de":
            code = code[:-1]
            digit = - convert_from_base(code[-1], 214)
            elements.append(digit)
        else:
            elements.append(int(code[-1]))

        code = code[:-1]

    try:
        n_num = int(num[0])
    except:
        try:
            n_num = str(num[0])
            selector = range(0, len(n_num))
        except:
            n_num = 0

    if ADD_ONE:
        n_num += 1
    if SUB_ONE:
        n_num -= 1

    if TIME_IT:
        import time
        start_time = time.time()
        print(func_a(n_num))
        end_time = time.time()
        print()
        print("Elapsed: " + str(end_time - start_time) + " seconds")
    else:
        if FIRST_AFTER:
            code_lines = code.split("\n")

            while True:
                n_num += 1

                has_succeeded = True
                for Q in code_lines:
                    code = Q
                    elements.clear()

                    if func_a(n_num) != 1:
                        has_succeeded = False
                        break

                if has_succeeded:
                    print(n_num)
                    break

        elif NTH_ELEMENT:
            code_lines = code.split("\n")

            successes = 0
            iteration = 0 + START_WITH_ONE

            while successes < n_num:

                has_succeeded = True
                for Q in code_lines:
                    code = Q
                    elements.clear()

                    if func_a(iteration) != 1:
                        has_succeeded = False
                        break

                if has_succeeded:
                    successes += 1

                iteration += 1

            print(iteration - 1)

        elif IS_TRUTHY:
            code_lines = code.split("\n")

            result = 1

            for line in code_lines:

                code = line
                elements.clear()

                if func_a(n_num) != 1:
                    result = 0
                    break

            print(result)

        else:
            print(func_a(n_num))
