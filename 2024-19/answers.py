"""A solution to an Advent of Code puzzle."""

# Data Model:
# ===========
# _lines_ is a list of "\n" terminated strings from the input file.


import os.path  # to get the directory name of the script (current puzzle year-day)

INPUT = "input.txt"


def part1(lines):
    """Solve part 1 of the problem."""
    towels, patterns = parse(lines)
    total = 0
    for pattern in patterns:
        if possible(pattern, towels):
            total += 1
    return total


def part2(lines):
    """Solve part 2 of the problem."""
    data = parse(lines)
    total = len(data)
    return total


def parse(lines):
    """Convert the lines of text into a useful data model."""
    patterns = []
    towels = lines[0].strip().split(", ")
    for line in lines[2:]:
        line = line.strip()
        patterns.append(line)
    return towels, patterns


cache = {}


def possible(pattern, towels):
    """Return True if it is possible to create the pattern with the towels"""
    if pattern in cache:
        return cache[pattern]
    if len(pattern) < 9 and pattern in towels:
        cache[pattern] = True
        return True
    for towel in towels:
        if pattern.startswith(towel):
            if possible(pattern[len(towel) :], towels):
                cache[pattern] = True
                return True
    cache[pattern] = False
    return False


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
