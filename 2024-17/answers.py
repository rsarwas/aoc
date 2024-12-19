"""A solution to an Advent of Code puzzle."""

# Data Model:
# ===========
# _lines_ is a list of "\n" terminated strings from the input file.


import os.path  # to get the directory name of the script (current puzzle year-day)

INPUT = "input.txt"


def part1(lines):
    """Solve part 1 of the problem."""
    registers, program = parse(lines)
    # to verify the python version of the program works correctly
    # a = registers[0]
    # output = code_in_python(a)
    # print("test python output", output)
    output = run_code(registers, program)
    total = ",".join([str(x) for x in output])
    return total


def part2(lines):
    """Solve part 2 of the problem."""
    registers, program = parse(lines)
    register_a = find_a(program)
    # test register A
    # registers[0] = register_a
    # output = run_code(registers, program)
    # if output != program:
    #     print("FAILED")
    #     print("register A:", register_a)
    #     print("program:", program)
    #     print("output: ", output)
    #     print("python: ", code_in_python(register_a))
    #     return None
    return register_a


def parse(lines):
    """Convert the lines of text into a useful data model."""
    registers = [int(x) for _, x in [line.strip().split(": ") for line in lines[0:3]]]
    program = [int(x) for x in lines[4].strip().split(": ")[1].split(",")]
    # program = zip(program[::2], program[1::2])  # [(opcode, operand), ...]
    return registers, program


def run_code(registers, program):
    """Run the program code in program, initializing the registers with registers.
    Return a list of output values when the program halts."""
    output = []
    opcodes = [adv, bxl, bst, jnz, bxc, out, bdv, cdv]
    # add an instruction pointer to the registers at index 3
    registers.append(0)
    while registers[3] < len(program) - 1:
        ip = registers[3]
        opcode, operand = program[ip], program[ip + 1]
        func = opcodes[opcode]
        result = func(operand, registers)
        if result is not None:
            output.append(result)
    return output


def adv(operand, registers):
    """The adv instruction (opcode 0) performs division. The numerator is the value
    in the A register. The denominator is found by raising 2 to the power of the
    instruction's combo operand. (So, an operand of 2 would divide A by 4 (2^2); an
    operand of 5 would divide A by 2^B.) The result of the division operation
    is truncated to an integer and then written to the A register.
    Register A, B, C = registers[0,1,2], Instruction Pointer = registers[3]."""
    numerator = registers[0]
    denominator = 1 << combo(operand, registers)
    registers[0] = numerator // denominator
    registers[3] += 2


def bxl(operand, registers):
    """The bxl instruction (opcode 1) calculates the bitwise XOR of register B and
    the instruction's literal operand, then stores the result in register B.
    Register A, B, C = registers[0,1,2], Instruction Pointer = registers[3]."""
    registers[1] ^= operand
    registers[3] += 2


def bst(operand, registers):
    """The bst instruction (opcode 2) calculates the value of its combo operand
    modulo 8 (thereby keeping only its lowest 3 bits), then writes that value to
    the B register.
    Register A, B, C = registers[0,1,2], Instruction Pointer = registers[3]."""
    registers[1] = combo(operand, registers) % 8
    registers[3] += 2


def jnz(operand, registers):
    """The jnz instruction (opcode 3) does nothing if the A register is 0. However,
    if the A register is not zero, it jumps by setting the instruction pointer to the
    value of its literal operand; if this instruction jumps, the instruction pointer
    is not increased by 2 after this instruction.
    Register A, B, C = registers[0,1,2], Instruction Pointer = registers[3]."""
    if registers[0] == 0:
        registers[3] += 2
    else:
        registers[3] = operand


def bxc(operand, registers):
    """The bxc instruction (opcode 4) calculates the bitwise XOR of register B and
    register C, then stores the result in register B. (For legacy reasons, this
    instruction reads an operand but ignores it.)
    Register A, B, C = registers[0,1,2], Instruction Pointer = registers[3]."""
    registers[1] ^= registers[2]
    registers[3] += 2


def out(operand, registers):
    """The out instruction (opcode 5) calculates the value of its combo operand modulo 8,
    then outputs that value. (If a program outputs multiple values, they are separated
    by commas.)
    Register A, B, C = registers[0,1,2], Instruction Pointer = registers[3]."""
    registers[3] += 2
    return combo(operand, registers) % 8


def bdv(operand, registers):
    """The bdv instruction (opcode 6) works exactly like the adv instruction except that
    the result is stored in the B register. (The numerator is still read from the A
    register.)"""
    numerator = registers[0]
    denominator = 1 << combo(operand, registers)
    registers[1] = numerator // denominator
    registers[3] += 2


def cdv(operand, registers):
    """The cdv instruction (opcode 7) works exactly like the adv instruction except that
    the result is stored in the C register. (The numerator is still read from the A
    register.)"""
    numerator = registers[0]
    denominator = 1 << combo(operand, registers)
    registers[2] = numerator // denominator
    registers[3] += 2


def combo(operand, registers):
    """Calculates the value of a combo operand

    Combo operands 0 through 3 represent literal values 0 through 3.
    Combo operand 4 represents the value of register A.
    Combo operand 5 represents the value of register B.
    Combo operand 6 represents the value of register C.
    Combo operand 7 is reserved and will not appear in valid programs."""
    if operand < 4:
        return operand
    if operand < 7:
        return registers[operand - 4]


def code_in_python(a):
    """Given register A, generate the same output as the input code

    Analysis of Input:

    program code: 2,4,1,5,7,5,1,6,0,3,4,2,5,5,3,0

    working backwards:
        3,0: if register A > 0 jump to start, else end
        5,5: output register B % 8
        4,2: B ^= C
        0,3: ADV: A <- A // 2^3 (8)
        1,6: B ^= 6 (0110)
        7,5: CDV: C <- A // 2^B
        1,5: B ^= 5 (0101)
        2,4: B <- A % 8

    In psuedo code:

        while register A > 0:
            B = A % 8
            B ^= 5
                C = A // 2^B
            B ^= 6
            B ^= C
            A = A // 8
            output register B % 8
    """
    result = []
    while a > 0:
        # obvious code
        # b = a % 8
        # b ^= 5
        # c = a // 2**b
        # b ^= 6
        # b ^= c
        # b %= 8
        # a //= 8
        # simplified code
        b = a % 8  # get last 3 bits of 8
        c = (a // 2 ** (b ^ 5)) % 8
        out = b ^ 5 ^ 6 ^ c
        result.append(out)
        a //= 8  # shift a to remove last 3 bits
    return result


def find_a(code):
    """Find A by working backwards in the code.  A will be very small - only one byte
    to generate the last code point.  Each loop in the code lops off one byte from A,
    so we just apply the code backwards, building A up one byte at a time."""
    rcode = code.copy()
    rcode.reverse()
    a = 0
    for i, out in enumerate(rcode):
        a2 = 0
        # print(f"a = {a}, a2 = {a2}, out = {out}")
        while True:
            # a2 is the add on to a to get to the new number.  It is usually less than 1 byte
            a_test = a * 8 + a2
            b = a_test % 8
            c = (a_test // 2 ** (b ^ 5)) % 8
            b = b ^ 5 ^ 6 ^ c
            if b == out and code[-i - 1 :] == code_in_python(a_test):
                # Experience shows that sometimes the first value we find might screw up
                # the values we already have (due to the C variable.)
                # check the full output and keep looking if it doesn't satisfy the
                # rest of the output
                # print(f"Yeah! a = {a}, a2 = {a2}, a_test = {a_test}, b = {b}, c = {c}")
                a = a_test
                break
            else:
                a2 += 1
    return a


def main(filename):
    """Solve both parts of the puzzle."""
    _, puzzle = os.path.split(os.path.dirname(__file__))
    with open(filename, encoding="utf8") as data:
        lines = data.readlines()
    print(f"Solving Advent of Code {puzzle} with {filename}")
    print(f"Part 1: {part1(lines)}")
    print(f"Part 2: {part2(lines)}")


if __name__ == "__main__":
    main(INPUT)
