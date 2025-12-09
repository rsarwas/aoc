"""A solution to an Advent of Code puzzle."""

# Data Model:
# ===========
# _lines_ is a list of "\n" terminated strings from the input file.


import os.path  # to get the directory name of the script (current puzzle year-day)

INPUT = "input.txt"


def part1(lines):
    """Solve part 1 of the problem."""
    data = parse(lines)
    max_area = 0
    for x1, y1 in data:
        for x2, y2 in data:
            area = calc_area(x1, y1, x2, y2)
            if area > max_area:
                max_area = area
    return max_area


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
        x, y = line.split(",")
        data.append((int(x), int(y)))
    return data


def calc_area(x1, y1, x2, y2):
    """Return the area of the rectangle"""
    dx = 1 + abs(x2 - x1)
    dy = 1 + abs(y2 - y1)
    return dx * dy


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
