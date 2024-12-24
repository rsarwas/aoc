"""A solution to an Advent of Code puzzle."""

# Data Model:
# ===========
# _lines_ is a list of "\n" terminated strings from the input file.


import os.path  # to get the directory name of the script (current puzzle year-day)

INPUT = "input.txt"


def part1(lines):
    """Solve part 1 of the problem."""
    inputs, gates = parse(lines)
    # print(inputs, gates)
    values = fill_circuit(inputs, gates)
    # print(values)
    return get_value("z", values)


def part2(lines):
    """Solve part 2 of the problem."""
    inputs, gates = parse(lines)
    # print(inputs, gates)
    pairs = find_mutations(inputs, gates)
    if pairs is None:
        return "Failed!"
    gate_list = []
    for name1, name2 in pairs:
        gate_list.append(name1)
        gate_list.append(name2)
    gate_list.sort()
    answer = ",".join(gate_list)
    return answer


def parse(lines):
    """Convert the lines of text into a useful data model."""
    inputs = {}
    gates = {}
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
            gates[output] = (op, wire1, wire2)
    return inputs, gates


def fill_circuit(inputs, gates):
    """Create a set of values for the circuit"""
    values = dict(inputs)
    # print(gates)
    names = gates.keys()
    unchecked = set(names)
    n = len(unchecked) + 1
    while len(unchecked) < n:
        n = len(unchecked)
        for name in gates:
            if name in values:
                continue
            op, name1, name2 = gates[name]
            if name1 in values and name2 in values:
                v1, v2 = values[name1], values[name2]
                value = None
                if op == "OR":
                    value = v1 | v2
                if op == "XOR":
                    value = v1 ^ v2
                if op == "AND":
                    value = v1 & v2
                values[name] = value
                unchecked.remove(name)
    return values


def find_mutations(inputs, gates):
    """Find the 4 swaps that make x + y == z"""
    x = get_value("x", inputs)
    y = get_value("y", inputs)
    names = list(gates.keys())
    for swaps in potential_swaps4(names):
        # print(swaps)
        values = process_swaps(inputs, gates, swaps)
        z = get_value("z", values)
        # print(x, y, z)
        if x + y == z:
            return swaps
    return None


def potential_swaps2(gates):
    """Return a list of all 4 pairs of potential swaps"""
    pairs = get_pairs(gates)
    for i1, p1 in enumerate(pairs[:-1]):
        for p2 in pairs[i1 + 1 :]:
            yield [p1, p2]


def potential_swaps4(gates):
    """Return a list of all 4 pairs of potential swaps"""
    pairs = get_pairs(gates)
    # print("pairs", len(pairs))
    for i1, p1 in enumerate(pairs[:-3]):
        s1 = set([p1[0], p1[1]])
        # print("p1", p1)
        for i2, p2 in enumerate(pairs[i1 + 1 : -2]):
            if p2[0] in s1 or p2[1] in s1:
                continue
            s2 = set([p2[0], p2[1]])
            # print("p2", p2)
            for i3, p3 in enumerate(pairs[i1 + i2 + 2 : -1]):
                if p3[0] in s1 or p3[1] in s1 or p3[0] in s2 or p3[1] in s2:
                    continue
                s3 = set([p3[0], p3[1]])
                # print("p3", p3)
                for p4 in pairs[i1 + i2 + i3 + 3 :]:
                    if (
                        p4[0] in s1
                        or p4[1] in s1
                        or p4[0] in s2
                        or p4[1] in s2
                        or p4[0] in s3
                        or p4[1] in s3
                    ):
                        continue
                    # print("p4", p4)
                    yield [p1, p2, p3, p4]


def get_pairs(gates):
    """Return a list of all the pairs of names"""
    pairs = []
    for index, name1 in enumerate(gates[:-1]):
        for name2 in gates[index + 1 :]:
            pairs.append((name1, name2))
    return pairs


def process_swaps(inputs, gates, swaps):
    """Change the ops per the swaps, and return the circuit output values"""
    # mutate ops_xxx per swaps
    do_swap(gates, swaps)
    values = fill_circuit(inputs, gates)
    # revert the swaps, by swapping again.
    do_swap(gates, swaps)
    return values


def do_swap(gates, swaps):
    """swap the input on the pairs of gates in the ops"""
    for name1, name2 in swaps:
        temp = gates[name1]
        gates[name1] = gates[name2]
        gates[name2] = temp


def get_value(name, values):
    """Get the value on the wires starting with name."""
    names = [key for key in values.keys() if key.startswith(name)]
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
