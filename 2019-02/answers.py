import sys


def add(a, b):
    return a + b


def mul(a, b):
    return a * b


def op3(ip, intcode, fn):
    a1 = intcode[ip + 1]
    a2 = intcode[ip + 2]
    a3 = intcode[ip + 3]
    ip = ip + 4
    v1 = intcode[a1]
    v2 = intcode[a2]
    intcode[a3] = fn(v1, v2)
    return ip


def execute(intcode):
    ip = 0
    instruction = intcode[ip]
    while instruction != 99:
        if instruction == 1:
            ip = op3(ip, intcode, add)
        elif instruction == 2:
            ip = op3(ip, intcode, mul)
        else:
            raise NotImplementedError
        instruction = intcode[ip]


def part1(code):
    code[1] = 12
    code[2] = 2
    execute(code)
    return code[0]


def part2(program):
    for noun in range(0, 99):
        for verb in range(0, 99):
            code = list(program)
            code[1] = noun
            code[2] = verb
            execute(code)
            if code[0] == 19690720:
                return noun, verb


if __name__ == "__main__":
    program = [int(x) for x in sys.stdin.read().split(",")]
    print("Part 1: {0}".format(part1(list(program))))
    noun, verb = part2(list(program))
    print("Part 1: {0:0>2}{1:0>2}".format(noun, verb))
