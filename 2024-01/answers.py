"""A solution to an Advent of Code puzzle."""

# Data Model:
# ===========
# _lines_ is a list of "\n" terminated strings from the input file.


import os.path  # to get the directory name of the script (current puzzle year-day)

INPUT = "input.txt"

from collections import Counter


def part1(lines):
    """Solve part 1 of the problem."""
    list1, list2 = parse(lines)
    list1.sort()
    list2.sort()
    deltas = [abs(x - y) for x, y in zip(list1, list2)]
    total = sum(deltas)
    return total


def part2(lines):
    """Solve part 2 of the problem."""
    list1, list2 = parse(lines)
    list2_counts = Counter(list2)
    total = 0
    for id in list1:
        if id in list2_counts:
            total += id * list2_counts[id]
    return total


def parse(lines):
    """Convert the lines of text into a useful data model."""
    list1 = []
    list2 = []
    for line in lines:
        line = line.strip()
        ids = [int(x) for x in line.split()]
        list1.append(ids[0])
        list2.append(ids[1])
    return list1, list2


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
