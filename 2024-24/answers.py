"""A solution to an Advent of Code puzzle."""

# Data Model:
# ===========
# _lines_ is a list of "\n" terminated strings from the input file.


import os.path  # to get the directory name of the script (current puzzle year-day)

INPUT = "input.txt"


def part1(lines):
    """Solve part 1 of the problem."""
    inputs, or_ops, xor_ops, and_ops = parse(lines)
    # print(inputs, or_ops, xor_ops, and_ops)
    values = fill_circuit(inputs, or_ops, xor_ops, and_ops)
    # print(values)
    names = [name for name in values.keys() if name.startswith("z")]
    names.sort()
    names.reverse()
    # print(names)
    output = []
    binary = {True: "1", False: "0"}
    for name in names:
        output.append(binary[values[name]])
    output = "".join(output)
    output = int(output, 2)
    return output


def part2(lines):
    """Solve part 2 of the problem."""
    data = parse(lines)
    total = len(data)
    return total


def parse(lines):
    """Convert the lines of text into a useful data model."""
    inputs = {}
    or_ops = {}
    xor_ops = {}
    and_ops = {}
    in_part1 = True
    for line in lines:
        line = line.strip()
        if not line:
            in_part1 = False
            continue
        if in_part1:
            name, value = line.split(": ")
            inputs[name] = value == "1"
        else:
            wire1, op, wire2, _, output = line.split(" ")
            if op == "OR":
                or_ops[output] = (wire1, wire2)
            if op == "XOR":
                xor_ops[output] = (wire1, wire2)
            if op == "AND":
                and_ops[output] = (wire1, wire2)
    return inputs, or_ops, xor_ops, and_ops


def fill_circuit(inputs, or_ops, xor_ops, and_ops):
    """Create a set of values for the circuit"""
    values = dict(inputs)
    # print(values)
    unchecked = set(or_ops.keys())
    unchecked = unchecked.union(xor_ops.keys())
    unchecked = unchecked.union(and_ops.keys())
    # print(unchecked)
    while unchecked:
        for name in or_ops:
            if name in values:
                continue
            name1, name2 = or_ops[name]
            if name1 in values and name2 in values:
                values[name] = values[name1] | values[name2]
                unchecked.remove(name)
        for name in xor_ops:
            if name in values:
                continue
            name1, name2 = xor_ops[name]
            if name1 in values and name2 in values:
                values[name] = values[name1] ^ values[name2]
                unchecked.remove(name)
        for name in and_ops:
            if name in values:
                continue
            name1, name2 = and_ops[name]
            if name1 in values and name2 in values:
                values[name] = values[name1] & values[name2]
                unchecked.remove(name)
    return values


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
