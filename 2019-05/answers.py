import sys

# 1 is the input for part 1 (first execution), 5 is the input for part 2 (second execution of same intcode)
input = [5, 1]  # this will be pop()ed, from the end to the front.
output = []


def add(a, b):
    return a + b


def mul(a, b):
    return a * b


def lt(a, b):
    return 1 if a < b else 0


def eq(a, b):
    return 1 if a == b else 0


def read(intcode, a):
    intcode[a] = input.pop()


def write(intcode, a):
    output.append(intcode[a])


def op3(ip, intcode, fn, pm1=0, pm2=0):
    a1 = intcode[ip + 1] if pm1 == 0 else ip + 1
    a2 = intcode[ip + 2] if pm2 == 0 else ip + 2
    a3 = intcode[ip + 3]
    ip += 4
    v1 = intcode[a1]
    v2 = intcode[a2]
    intcode[a3] = fn(v1, v2)
    return ip


def op1(ip, intcode, fn, pm1=0):
    a1 = intcode[ip + 1] if pm1 == 0 else ip + 1
    ip += 2
    fn(intcode, a1)
    return ip


def jump(ip, intcode, if_true, pm1=0, pm2=0):
    a1 = intcode[ip + 1] if pm1 == 0 else ip + 1
    a2 = intcode[ip + 2] if pm2 == 0 else ip + 2
    v1 = intcode[a1]
    v2 = intcode[a2]
    ip += 3
    # if-true: if the first parameter is non-zero, it sets the instruction pointer to the value from the second parameter. Otherwise, it does nothing.
    # if-false: if the first parameter is zero, it sets the instruction pointer to the value from the second parameter. Otherwise, it does nothing.
    if if_true:
        if v1 != 0:
            ip = v2
    else:
        if v1 == 0:
            ip = v2
    return ip


def parse(code):
    parameters = code // 100
    instruction = code % 100
    pm1 = parameters % 10
    parameters //= 10
    pm2 = parameters % 10
    # pm3 = parameters // 10
    return instruction, pm1, pm2


"""
    Opcode 1 add parameter 1 and parameter 2 and store the result in parameter 3
    Opcode 2 multiply parameter 1 and parameter 2 and store the result in parameter 3
    Opcode 3 takes a single integer as input and saves it to the position given by its only parameter. For example, the instruction 3,50 would take an input value and store it at address 50.
    Opcode 4 outputs the value of its only parameter. For example, the instruction 4,50 would output the value at address 50.
    Opcode 5 is jump-if-true: if the first parameter is non-zero, it sets the instruction pointer to the value from the second parameter. Otherwise, it does nothing.
    Opcode 6 is jump-if-false: if the first parameter is zero, it sets the instruction pointer to the value from the second parameter. Otherwise, it does nothing.
    Opcode 7 is less than: if the first parameter is less than the second parameter, it stores 1 in the position given by the third parameter. Otherwise, it stores 0.
    Opcode 8 is equals: if the first parameter is equal to the second parameter, it stores 1 in the position given by the third parameter. Otherwise, it stores 0.
"""


def execute(intcode):
    ip = 0
    instruction, pm1, pm2 = parse(intcode[ip])
    while instruction != 99:
        if instruction == 1:
            ip = op3(ip, intcode, add, pm1, pm2)
        elif instruction == 2:
            ip = op3(ip, intcode, mul, pm1, pm2)
        elif instruction == 3:
            ip = op1(ip, intcode, read)
        elif instruction == 4:
            ip = op1(ip, intcode, write, pm1)
        elif instruction == 5:
            ip = jump(ip, intcode, True, pm1, pm2)
        elif instruction == 6:
            ip = jump(ip, intcode, False, pm1, pm2)
        elif instruction == 7:
            ip = op3(ip, intcode, lt, pm1, pm2)
        elif instruction == 8:
            ip = op3(ip, intcode, eq, pm1, pm2)
        else:
            print(ip, instruction, pm1, pm2)
            raise NotImplementedError
        instruction, pm1, pm2 = parse(intcode[ip])


if __name__ == "__main__":
    program = [int(x) for x in sys.stdin.read().split(",")]
    execute(list(program))
    print("Part 1: {0}".format(output[-1]))
    execute(program)
    print("Part 2: {0}".format(output[-1]))
