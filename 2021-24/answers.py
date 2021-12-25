# Data Model:
# ===========
# lines is a list of "\n" terminated strings from the input file
# 

def part1(lines):
    cmds = parse(lines)
    n = 13579246899999
    print(model_number(n))
    valid = check_number(n, cmds)
    
    print(valid)
    return -1

def part2(lines):
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
    inputs = model_number(13579246899999)
    registers = [0, 0, 0, 0]
    for cmd in cmds:
        if not execute(cmd, registers, inputs):
            return False
    return registers[reg('z')] == 0

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
            print(f"ALU Panic. Division by zero. Command {cmd} skipped, registers = {registers}")
            return False
        else:
            # Integer division in Python (//) does not round towards zero for negative numbers
            # but int() of a float does round towards zero
            registers[r] = int(registers[r] / v)
    elif inst == "mod":
        r = reg(cmd[1])
        v = val(cmd[2], registers)
        if v == 0:
            print(f"ALU Panic. Division by zero. Command {cmd} skipped, registers = {registers}")
            return False
        if registers[r] < 0 or v < 0:
            print(f"ALU Panic. Modulo with a negative number. Command {cmd} skipped, registers = {registers}")
            return False
        registers[r] %= v
    elif inst == "eql":
        r = reg(cmd[1])
        v = val(cmd[2], registers)
        registers[r] = 1 if registers[r] == v else 0
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

if __name__ == '__main__':
    # alu_tests()
    lines = open("input.txt").readlines() # as a list of line strings
    print(f"Part 1: {part1(lines)}")
    # print(f"Part 2: {part2(lines)}")
