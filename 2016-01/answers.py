"""A solution to an Advent of Code puzzle."""

# Data Model:
# ===========
# _lines_ is a list of "\n" terminated strings from the input file.


import os.path  # to get the directory name of the script (current puzzle year-day)

INPUT = "test.txt"

N = 0
E = 1
S = 2
W = 3


def part1(lines):
    """Solve part 1 of the problem."""
    data = parse(lines)
    loc = (0, 0)
    heading = N
    for turn, dist in data:
        heading = update_heading(heading, turn)
        if heading == N:
            loc = (loc[0], loc[1] + dist)
        elif heading == S:
            loc = (loc[0], loc[1] - dist)
        elif heading == W:
            loc = (loc[0] + dist, loc[1])
        else:
            loc = (loc[0] - dist, loc[1])
    man_dist = abs(loc[0]) + abs(loc[1])
    return man_dist


def part2(lines):
    """Solve part 2 of the problem."""
    data = parse(lines)
    total = len(data)
    return total


def parse(lines):
    """Convert the lines of text into a useful data model."""
    data = []
    raw_data = lines[0].strip().split(", ")
    data = [(item[0], int(item[1:])) for item in raw_data]
    return data


def update_heading(heading, turn):
    if turn == "L":
        return (heading - 1) % 4
    return (heading + 1) % 4


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
