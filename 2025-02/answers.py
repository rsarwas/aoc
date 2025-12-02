"""A solution to an Advent of Code puzzle."""

# Data Model:
# ===========
# _lines_ is a list of "\n" terminated strings from the input file.


import os.path  # to get the directory name of the script (current puzzle year-day)
import math  # for log10, to determine number of digits in number

INPUT = "input.txt"


def part1(lines):
    """Solve part 1 of the problem."""
    data = parse(lines)
    total = 0
    for n1, n2 in data:
        for n in range(n1, n2 + 1):
            if invalid(n):
                # print(n1, n2, n)
                total += n
    return total


def part2(lines):
    """Solve part 2 of the problem."""
    data = parse(lines)
    total = len(data)
    return total


def parse(lines):
    """Convert the lines of text into a useful data model."""
    data = []
    for rng in lines[0].strip().split(","):
        x, y = rng.split("-")
        data.append((int(x), int(y)))
    return data


def invalid(n):
    """Returns true if n is invalid; i.e. first half matches second half; e.g. 9797"""
    l = int(math.log10(n))
    if l % 2 == 0:
        # l is an even number, so there is an odd number of digits
        return False
    l2 = (l + 1) // 2
    s = str(n)
    return s[:l2] == s[l2:]


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
