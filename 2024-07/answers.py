"""A solution to an Advent of Code puzzle."""

# Data Model:
# ===========
# _lines_ is a list of "\n" terminated strings from the input file.


import os.path  # to get the directory name of the script (current puzzle year-day)

INPUT = "input.txt"


def part1(lines):
    """Solve part 1 of the problem."""
    data = parse(lines)
    total = 0
    for line in data:
        result = line[0]
        operands = line[1:]
        if is_valid(result, operands, ["*", "+"]):
            total += result
    return total


def part2(lines):
    """Solve part 2 of the problem."""
    data = parse(lines)
    total = 0
    for line in data:
        result = line[0]
        operands = line[1:]
        if is_valid(result, operands, ["*", "+", "|"]):
            total += result
    return total


def parse(lines):
    """Convert the lines of text into a useful data model."""
    data = []
    for line in lines:
        line = line.strip().replace(":", "")
        line = [int(x) for x in line.split()]
        data.append(line)
    return data


def is_valid(result, operands, operations):
    """Return True if some combination of operations on the operands (line[1:])
    is equal to the result. operations are performed in a strictly left to right
    order (ignore standard operator precedence)."""
    combinations = operator_combinations(operations, len(operands) - 1)
    other_operands = operands[1:]
    for combo in combinations:
        total = operands[0]
        for operation, operand in zip(combo, other_operands):
            if operation == "*":
                total *= operand
            if operation == "+":
                total += operand
            if operation == "|":
                # Concatenation (string) operator
                total = concatenate_ints(total, operand)
        if total == result:
            # print(combo, operands)
            return True
    return False


def concatenate_ints(int1, int2):
    """Return a new int by concatenating the string version of the two ints.
    i.e. 48 and 16 becomes 4816."""
    return int(str(int1) + str(int2))


def operator_combinations(operations, n):
    """return all the permutations of operations of length n"""
    if n == 1:
        return operations
    combos = []
    for tail in operator_combinations(operations, n - 1):
        for head in operations:
            combos.append(head + tail)
    return combos


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
