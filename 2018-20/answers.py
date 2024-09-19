"""A solution to an Advent of Code puzzle."""

# Data Model:
# ===========
# _lines_ is a list of "\n" terminated strings from the input file.


import os.path  # to get the directory name of the script (current puzzle year-day)

INPUT = "test.txt"


def part1(lines):
    """Solve part 1 of the problem."""
    data = parse(lines)
    total = len(data)
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
        data.append(len(line))
    return data


def test_part1():
    lines = open("test.txt").readlines()
    print(f"test 0: expect 3; Got {part1(lines)}")
    lines = open("test1.txt").readlines()
    print(f"test 1: expect 10; Got {part1(lines)}")
    lines = open("test2.txt").readlines()
    print(f"test 2: expect 18; Got {part1(lines)}")
    lines = open("test3.txt").readlines()
    print(f"test 3: expect 23; Got {part1(lines)}")
    lines = open("test4.txt").readlines()
    print(f"test 4: expect 31; Got {part1(lines)}")


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
