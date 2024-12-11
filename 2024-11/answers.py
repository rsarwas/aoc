"""A solution to an Advent of Code puzzle."""

# Data Model:
# ===========
# _lines_ is a list of "\n" terminated strings from the input file.


import os.path  # to get the directory name of the script (current puzzle year-day)

INPUT = "input.txt"


def part1(lines):
    """Solve part 1 of the problem."""
    stones = parse(lines)
    # print(stones)
    blink_count = 25
    for _ in range(blink_count):
        stones = blink(stones)
        # print(stones)
    total = len(stones)
    return total


def part2(lines):
    """Solve part 2 of the problem."""
    data = parse(lines)
    total = len(data)
    return total


def parse(lines):
    """Convert the lines of text into a useful data model."""
    return [int(n) for n in lines[0].strip().split()]


def blink(stones):
    """change the stones according to the rules in the problem statement"""
    new_stones = []
    for stone in stones:
        new_stones += change(stone)
    return new_stones


def change(n):
    """Return a list of stones given the number engraved on a stone"""
    digits = str(n)
    if n == 0:
        return [1]
    if len(digits) % 2 == 0:
        mid = len(digits) // 2
        return [int(digits[:mid]), int(digits[mid:])]
    return [n * 2024]


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
