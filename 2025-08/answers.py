"""A solution to an Advent of Code puzzle."""

# Data Model:
# ===========
# _lines_ is a list of "\n" terminated strings from the input file.


import os.path  # to get the directory name of the script (current puzzle year-day)
import math  # for sqrt


INPUT = "input.txt"


def part1(lines):
    """Solve part 1 of the problem."""
    data = parse(lines)
    lengths = sort_lengths(data)
    circuits = []
    n = 10 if INPUT == "test.txt" else 1000
    for i in range(n):
        _, index1, index2 = lengths[i]
        # print(index1, index2, circuits)
        circuit1, circuit2 = None, None
        for j, circuit in enumerate(circuits):
            if index1 in circuit:
                circuit1 = j
            if index2 in circuit:
                circuit2 = j
        if circuit1 is not None or circuit2 is not None:
            if circuit1 is None:
                circuits[circuit2].add(index1)
            elif circuit2 is None:
                circuits[circuit1].add(index2)
            elif circuit1 == circuit2:
                pass
            else:  # circuit 1 and circuit 2 are different, so I need to merge
                new_circuit = circuits[circuit1] | circuits[circuit2]
                # need to save this because it's index will change when we delete circuit1
                temp = circuits[circuit2]
                del circuits[circuit1]
                circuits.remove(temp)
                circuits.append(new_circuit)
        else:
            circuits.append(set([index1, index2]))
    sizes = []
    # print(circuits)
    for circuit in circuits:
        sizes.append(len(circuit))
    sizes.sort()
    sizes.reverse()
    # print(sizes)
    total = sizes[0] * sizes[1] * sizes[2]
    return total


def part2(lines):
    """Solve part 2 of the problem."""
    data = parse(lines)
    total = len(data)
    return total


def parse(lines):
    """Convert the lines of text into a useful data model."""
    data = []
    for line in lines:
        line = line.strip()
        coords = [int(x) for x in line.split(",")]
        coords = (coords[0], coords[1], coords[2])
        data.append(coords)
    return data


def sort_lengths(data):
    """Return a sorted list of (length,index1,index2) where length is the straight line distance
    between the 3D points at index1 and index2 in the list of points in data."""
    lengths = []
    for index1, point1 in enumerate(data[:-1]):
        for index2 in range(index1 + 1, len(data)):
            point2 = data[index2]
            x1, y1, z1 = point1
            x2, y2, z2 = point2
            dx, dy, dz = x2 - x1, y2 - y1, z2 - z1
            l = math.sqrt(dx * dx + dy * dy + dz * dz)
            # lengths[(index1,index2)] = l
            # lengths[(index2, index1)] = l
            lengths.append((l, index1, index2))
    lengths.sort()
    return lengths


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
