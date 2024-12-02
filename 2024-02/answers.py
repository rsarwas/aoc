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
    for report in data:
        if safety_check(report):
            total += 1
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
        report = [int(x) for x in line.split()]
        data.append(report)
    return data


def safety_check(report):
    """Return True if the report passes the safety check
    I.e. both of the following are true:
    * The levels are either all increasing or all decreasing.
    * Any two adjacent levels differ by at least one and at most three."""
    prior = report[0]
    direction = 1
    if prior > report[1]:
        direction = -1
    for level in report[1:]:
        delta = direction * (level - prior)
        if delta < 1 or delta > 3:
            return False
        prior = level
    return True


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
