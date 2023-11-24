# Data Model:
# ===========
# lines is a list of "\n" terminated strings from the input file
# Each line is a ALU instruction similar to "mul x 0".  The first word
# is the command, the second word is always one of 4 registers: w,x,y,z
# the third word is optional and is either a register or an integer literal
#
# Building the processor was fairly easy, but it is impossible to check all
# 9^14 possible model numbers to find the largest one that leaves Z == 0.
# Since all digits are required to process a number I could think of no ways
# to simplify the process by checking individual digits.
# I examined the code, and realized it was just a simple function that was
# executed 14 times, once for each digit.
# the function is equivalent to the following:
##  i = 0   1   2    3   4   5   6   7   8   9  10  11  12   13
# I = [ 1,  3,  5,   7,  9,  2,  4,  6,  8,  9,  9,  9,  9,   9] # sample model number from puzzle statement
# a = [15, 12, 13, -14, 15, -7, 14, 15, 15, -7, -8, -7, -5, -10]
# b = [15,  5,  6,   7,  9,  6, 14,  3,  1,  3,  4,  6,  7,   1]
# c = [ 1,  1,  1,  26,  1, 26,  1,  1,  1, 26, 26, 26, 26,  26]
# z = 0
# for i in range(len(I)):
#     if I[i] == (z % 26) + a[i]:
#         z = z // c[i]
#     else:
#         z = 26 * (z // c[i]) + I[i] + b[i]
# I is valid if z == 0
# The lists a, b, and c were hard coded in the puzzle input, and are likely
# unique for each puzzler.

# By studying this function and a,b,c, it was clear that whenever a was
# greater than 9, the test would never pass and c was 1, so z would grow
# by a factor of 26 (plus a little more). For other values of a, Z would
# either grow just a little (if the test failed), or shrink by a factor a 26
# when the test passed.  Since there were 7 grows by 26, each shrink had to
# pass the test.  I started by plugging in all 9s, and looked at z % 26 at
# each step to figure out which digit would pass the test.  In some cases,
# z % 26 + b was not in the range 1..9, so no valid input would work. In this case,
# a preceding digit would need to be reduced in order to reduce the remainder.
# At that point, it was a matter of testing how different digits impacted the
# remainder in question, and find the least significant digit that would do the
# trick.
#
# Part 2 was solved the same way, but by starting with all 1s


def part1(lines):
    cmds = parse(lines)
    x = "01234567890123"
    n = 49917929934999
    # alu_in_python(n)
    # print()
    # print(model_number(n))
    valid = check_number(n, cmds)
    # print(valid)
    if valid:
        return n
    return -1


def part2(lines):
    x = "01234567890123"
    n = 11111111111111
    x = "012_4x678xxxxx"  # adjust numbers at 'x' to equal z % 26 + a (if possible)
    n = 11911111111111  # z % 26 = 7; 7 - 14 = -7; boost previous number by 8 so z % 26 = 15
    n = 11911311111111  # z % 26 = 10; 10 - 7 = 3; use I[5] = 3
    x = "012x4_678_xxxx"
    n = 11911311711111  # z % 26 = 2; 2 - 7 = -5, boost previous number by 6 so z % 26 = 8
    x = "012x4x678x_xxx"  # z % 26 = 4; 4 - 8 = -4, I want to boost the previous number by 5 so z % 26 = 9
    # however, I can't because the previous number needs to be 1 to pass the test.
    # skip for now.
    x = "012x4_678xx_xx"
    n = 11911311714111  # z % 26 = 5; 5 - 7 = -2, boost previous number by 3 so z % 26 = 8
    x = "012x4_678xxx_x"
    n = 11911311715211  # z % 26 = 15; 15 - 5 = 10, decrease previous number by 1 so z % 26 = 14
    # I can't go any lower than 1; back up increase previous 2 by 1
    # Ack that didn't change the remainder; skip for now
    x = "012x4_678xxxx_"
    n = 11911311714111  # z % 26 = 2; 2 - 10 = -8, increase previous number by 9 so z % 26 = 11;
    # unfortunately 1 + 9 = 10 is not a valid number.
    # backup to 11911311711111, now I can set the last two digits:
    n = 11911311711125
    # however that helps, but I need to fix the previous issues first
    #          x y    # the remainder at y is always the same as at x, so increase x to increase y
    n = 11911316711111
    x = "012345678xx_xx"  # z % 26 = 15; 15 - 7 = 8, use 8 in this spot
    n = 11911316711811
    x = "012345678xxx_x"  # z % 26 = 6; 6 - 5  = 1, so 1 is required
    x = "012345678xxxx_"  # z % 26 = 2; 16 - 10  = 6, use 6
    n = 11911316711816
    z = alu_in_python(n)
    if z == 0:
        return n
    return -1


def parse(lines):
    return [line.strip().split(" ") for line in lines]


def reg(s):
    # return an index to the register list; 'w' => 0, ... 'z' => 3
    return ord(s) - ord("w")


def val(s, registers):
    # given a the second command parameter string returns an int if possible,
    # otherwise the int value in the registers at the location of the parameter ('w' .. 'z')
    try:
        return int(s)
    except ValueError:
        return registers[reg(s)]


def model_number(n):
    # converts a model number to an input list
    numbers = [int(s) for s in str(n)]
    numbers.reverse()
    return numbers


def check_number(n, cmds):
    # check a model number return true if it is valid
    # inputs = model_number(13579246899999)
    inputs = model_number(n)
    registers = [0, 0, 0, 0]
    for cmd in cmds:
        if not execute(cmd, registers, inputs):
            return False
    return registers[reg("z")] == 0


def execute(cmd, registers, inputs):
    # Executes the cmd and modifies the registers and inputs ("inp" cmd only)
    # Returns True if the command succeeded, and False if it failed (i.e. division by zero)
    # For efficiency, inputs are pop()ed from the end of the list.
    # cmd is a list of 2 or 3 strings depending on the command

    # inp a - Read an input value and write it to variable a.
    # add a b - Add the value of a to the value of b, then store the result in variable a.
    # mul a b - Multiply the value of a by the value of b, then store the result in variable a.
    # div a b - Divide the value of a by the value of b, truncate the result to an integer, then store the result in variable a. (Here, "truncate" means to round the value toward zero.)
    # mod a b - Divide the value of a by the value of b, then store the remainder in variable a. (This is also called the modulo operation.)
    # eql a b - If the value of a and b are equal, then store the value 1 in variable a. Otherwise, store the value 0 in variable a.

    inst = cmd[0]
    if inst == "inp":
        r = reg(cmd[1])
        v = inputs.pop()
        registers[r] = v
    elif inst == "add":
        r = reg(cmd[1])
        v = val(cmd[2], registers)
        registers[r] += v
    elif inst == "mul":
        r = reg(cmd[1])
        v = val(cmd[2], registers)
        registers[r] *= v
    elif inst == "div":
        r = reg(cmd[1])
        v = val(cmd[2], registers)
        if v == 0:
            print(
                f"ALU Panic. Division by zero. Command {cmd} skipped, registers = {registers}"
            )
            return False
        else:
            # Integer division in Python (//) does not round towards zero for negative numbers
            # but int() of a float does round towards zero
            registers[r] = int(registers[r] / v)
    elif inst == "mod":
        r = reg(cmd[1])
        v = val(cmd[2], registers)
        if v == 0:
            print(
                f"ALU Panic. Division by zero. Command {cmd} skipped, registers = {registers}"
            )
            return False
        if registers[r] < 0 or v < 0:
            print(
                f"ALU Panic. Modulo with a negative number. Command {cmd} skipped, registers = {registers}"
            )
            return False
        registers[r] %= v
    elif inst == "eql":
        r = reg(cmd[1])
        v = val(cmd[2], registers)
        registers[r] = 1 if registers[r] == v else 0
    if inst == "add" and cmd[1] == "z" and cmd[2] == "y":
        z = registers[3]
        print(f"W = {registers[0]}; Z = {z}; Z/26 == {z//26} rem {z%26}")
    return True


def alu_tests():
    # test 1
    # test1.txt is an ALU program which takes an input number, negates it, and stores it in x
    cmds = parse(open("test1.txt").readlines())
    inputs = [4]
    registers = [0, 0, 0, 0]
    for cmd in cmds:
        execute(cmd, registers, inputs)
    print(f"x = {registers[reg('x')]}; expected -4")

    # test 2
    # test2.txt is an ALU program which takes two input numbers,
    # then sets z to 1 if the second input number is three times
    # larger than the first input number, or sets z to 0 otherwise:
    cmds = parse(open("test2.txt").readlines())
    inputs = [-3, -1]
    registers = [0, 0, 0, 0]
    for cmd in cmds:
        execute(cmd, registers, inputs)
    print(f"z = {registers[reg('z')]}; expected 1")

    # test 2
    # test2.txt is an ALU program which takes a non-negative integer as input,
    # converts it into binary, and stores the lowest (1's) bit in z,
    # the second-lowest (2's) bit in y, the third-lowest (4's) bit in x,
    # and the fourth-lowest (8's) bit in w:
    cmds = parse(open("test3.txt").readlines())
    inputs = [14]
    registers = [0, 0, 0, 0]
    for cmd in cmds:
        if not execute(cmd, registers, inputs):
            print("Invalid Input")
            break
    print(f"registers = {registers}; expected 1 1 1 0")


def alu_in_python(n):
    I = [int(s) for s in str(n)]
    #     i = 0   1   2    3   4   5   6   7   8   9  10  11  12   13
    a = [15, 12, 13, -14, 15, -7, 14, 15, 15, -7, -8, -7, -5, -10]
    b = [15, 5, 6, 7, 9, 6, 14, 3, 1, 3, 4, 6, 7, 1]
    c = [1, 1, 1, 26, 1, 26, 1, 1, 1, 26, 26, 26, 26, 26]
    z = 0
    for i in range(len(I)):
        if I[i] == (z % 26) + a[i]:
            z = z // c[i]
        else:
            z = 26 * (z // c[i]) + I[i] + b[i]
        print(f"W = {I[i]}; Z = {z}; Z/26 == {z//26} rem {z%26}")
    return z


if __name__ == "__main__":
    # alu_tests()
    lines = open("input.txt").readlines()  # as a list of line strings
    print(f"Part 1: {part1(lines)}")
    print(f"Part 2: {part2(lines)}")
