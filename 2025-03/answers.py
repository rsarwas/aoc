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
        joltage = max_joltage(line)
        if INPUT == "test.txt":
            print(line, joltage)
        total += joltage
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
        data.append(line)
    return data


def max_joltage(line):
    """Return the largest 2 digit number from the line
    The digits do not need to be adjacent, just in the correct order"""
    for n1 in range(9, 0, -1):
        strn1 = str(n1)
        if strn1 in line[:-1]:
            index = line.index(strn1) + 1
            for n2 in range(9, -1, -1):
                strn2 = str(n2)
                if strn2 in line[index:]:
                    return n1 * 10 + n2


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
