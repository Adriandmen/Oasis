import ast
import argparse
import sys
import math
from primes import *
from commands import *


code = ""
elements = []
sys.setrecursionlimit(5000)

def func_a(n):



    stack = []

    def pop_stack(n2=n, s2=stack):
        if s2:
            return s2.pop()
        else:
            if n > len(elements) + 1000:
                func_a(n - 1000)
            if DEBUG:
                print("using a(" + str(n2 - 1) + ") = " + str(func_a(n2 - 1)))
            return func_a(n2 - 1)

    result = None
    has_calculated = False

    try:
        has_calculated = elements[n] is not None
    except:
        has_calculated = False

    if has_calculated:
        if DEBUG: print("already initialized: " + str(elements[n]) + " at n = " + str(n))
        return elements[n]

    if DEBUG:
        print("\n --- a(" + str(n) + ") --- ")

    pointer_position = -1
    while pointer_position < len(code) - 1:
        pointer_position += 1

        command = code[pointer_position]
        if DEBUG: print("command > " + command)

        if command == "+":
            b = pop_stack()
            a = pop_stack()
            stack.append(regular_arithmetic(a, b, "+"))

        elif command == "-":
            b = pop_stack()

            if stack:
                a = pop_stack()
            else:
                a, b = b, pop_stack()
            stack.append(regular_arithmetic(a, b, "-"))

        elif command == "*":
            b = pop_stack()
            a = pop_stack()
            stack.append(regular_arithmetic(a, b, "*"))

        elif command == "/":
            b = pop_stack()
            a = pop_stack()
            stack.append(regular_arithmetic(a, b, "/"))

        elif command == "m":
            b = pop_stack()
            a = pop_stack()
            stack.append(regular_arithmetic(a, b, "**"))

        elif command == "\u00f7":
            b = pop_stack()
            a = pop_stack()
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

        elif command == "n":
            stack.append(n)

        elif command == "a":
            x = pop_stack()
            stack.append(func_a(x))

        elif command == "b":
            stack.append(func_a(n - 1))

        elif command == "c":
            stack.append(func_a(n - 2))

        elif command == "d":
            stack.append(func_a(n - 3))

        elif command == "e":
            x = pop_stack()
            stack.append(func_a(n - x))

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

        elif command == "x":
            a = pop_stack()
            stack.append(single_arithmetic(a, "* 2"))

        elif command == "y":
            a = pop_stack()
            stack.append(single_arithmetic(a, "* 3"))

        elif command == "z":
            a = pop_stack()
            stack.append(single_arithmetic(a, "* 4"))

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
    parser.add_argument("program_path", help="Program path", type=str)

    args, num = parser.parse_known_args()
    filename = args.program_path
    DEBUG = args.debug
    SAFE_MODE = args.safe
    ENCODE_CP1252 = args.cp1252
    TIME_IT = args.time

    if ENCODE_CP1252:
        code = open(filename, "r", encoding="cp1252").read()
    else:
        code = open(filename, "r", encoding="utf-8").read()

    code = code.replace("T", "10")
    code = code.replace("U", "00")
    code = code.replace("V", "11")
    code = code.replace("W", "000")

    while is_digit_value(code[-1]) or code[-1] == "N":
        if code[-1] == "N":
            elements.append(None)
        else:
            elements.append(int(code[-1]))

        code = code[:-1]

    try:
        n_num = int(num[0])
    except:
        n_num = 0

    if TIME_IT:
        import time
        start_time = time.time()
        print(func_a(n_num))
        end_time = time.time()
        print()
        print("Elapsed: " + str(end_time - start_time) + " seconds")
    else:
        print(func_a(n_num))