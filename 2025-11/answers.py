"""A solution to an Advent of Code puzzle."""

# Data Model:
# ===========
# _lines_ is a list of "\n" terminated strings from the input file.


import os.path  # to get the directory name of the script (current puzzle year-day)

INPUT = "input.txt"


def part1(lines):
    """Solve part 1 of the problem."""
    data = parse(lines)
    total = count_paths("you", "out", data)
    return total


def part2(lines):
    """Solve part 2 of the problem."""
    data = parse(lines)
    total = len(data)
    return total


def parse(lines):
    """Convert the lines of text into a useful data model."""
    data = {}
    for line in lines:
        line = line.strip()
        left, right = line.split(": ")
        right = set(right.split(" "))
        data[left] = right
    return data


def count_paths(current, dest, graph):
    """Return the number of paths from current node to dest node in graph"""
    neighbors = graph[current]
    if dest in neighbors:
        return 1
    total = 0
    for neighbor in neighbors:
        total += count_paths(neighbor, dest, graph)
    return total


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
