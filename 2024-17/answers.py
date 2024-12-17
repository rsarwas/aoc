"""A solution to an Advent of Code puzzle."""

# Data Model:
# ===========
# _lines_ is a list of "\n" terminated strings from the input file.


import os.path  # to get the directory name of the script (current puzzle year-day)

INPUT = "input.txt"


def part1(lines):
    """Solve part 1 of the problem."""
    registers, program = parse(lines)
    output = run_code(registers, program)
    total = ",".join([str(x) for x in output])
    return total


def part2(lines):
    """Solve part 2 of the problem."""
    data = parse(lines)
    total = len(data)
    return total


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
