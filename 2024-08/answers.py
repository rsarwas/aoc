"""A solution to an Advent of Code puzzle."""

# Data Model:
# ===========
# _lines_ is a list of "\n" terminated strings from the input file.


import os.path  # to get the directory name of the script (current puzzle year-day)

INPUT = "input.txt"


def part1(lines):
    """Solve part 1 of the problem."""
    data, size = parse(lines)
    # it would be simpler to just check if a potential antinode is within the bounds,
    # but I need to eliminated duplicates, so I need to keep track of the coordinates
    # I'm doing this as multiple steps anticipating it might make part 2 easier
    nodes = find_antinodes(data)
    bounded_nodes = [node for node in nodes if inbound(node, (0, size))]
    total = len(set(bounded_nodes))
    return total


def part2(lines):
    """Solve part 2 of the problem."""
    data = parse(lines)
    total = len(data)
    return total


def parse(lines):
    """Convert the lines of text into a useful data model."""
    data = {}
    size = len(lines)  # verified manually that data grid is square
    for row, line in enumerate(lines):
        line = line.strip()
        for col, char in enumerate(line):
            if char == ".":
                continue
            if char not in data:
                data[char] = []
            data[char].append((row, col))
    return data, size


def find_antinodes(data):
    """Find the coordinates of the antinodes.
    The data is a dictionary of list of antenna location for each antenna frequency.
    The antinodes are before the first node, and after the second node by the distance
    between them.  See the puzzle description for a better description."""
    antinodes = []
    for frequency in data:
        locations = data[frequency]
        if len(locations) < 2:
            continue
        for index, a in enumerate(locations[:-1]):
            for b in locations[index + 1 :]:
                delta = (b[0] - a[0], b[1] - a[1])
                before = (a[0] - delta[0], a[1] - delta[1])
                after = (b[0] + delta[0], b[1] + delta[1])
                antinodes.append(before)
                antinodes.append(after)
    return antinodes


def inbound(node, bounds):
    """Return True if node (x, y) are within the bounds (lower, upper)"""
    x, y = node
    lower, upper = bounds
    return lower <= x < upper and lower <= y < upper


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
