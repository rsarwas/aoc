"""A solution to an Advent of Code puzzle."""

# Data Model:
# ===========
# _lines_ is a list of "\n" terminated strings from the input file.


import os.path  # to get the directory name of the script (current puzzle year-day)

INPUT = "test.txt"
OPEN = "."
ROCK = "#"
START = "S"


def part1(lines):
    """Solve part 1 of the problem."""
    start, rocks, extents = parse(lines)
    steps = 64
    tiles = take_steps(start, rocks, extents, steps)
    total = len(tiles)
    return total


def part2(lines):
    """Solve part 2 of the problem."""
    start, rocks, size = parse(lines)
    steps = 500
    tiles = take_steps_v2(start, rocks, size, steps)
    total = len(tiles)
    return total


def parse(lines):
    """Convert the lines of text into a useful data model.
    Return a set of all the locations (row,col) of rocks (no-go tiles)
    and the extents, (max_row, max_col), and the start (row, col)"""
    max_rows = len(lines)
    max_cols = len(lines[0].strip())
    extents = (max_rows, max_cols)
    rocks = set()
    start = None
    for row, line in enumerate(lines):
        for col, char in enumerate(line.strip()):
            if char == START:
                start = (row, col)
            if char == ROCK:
                rocks.add((row, col))
    return start, rocks, extents


def take_steps(start, rocks, extents, steps):
    """Return all the possible tiles that could be the final
    resting place after taking steps from start"""
    origins = [start]
    for _ in range(steps):
        destinations = set()
        for location in origins:
            for neighbor in valid_neighbors(location, rocks, extents):
                destinations.add(neighbor)
        origins = destinations
    return destinations


def valid_neighbors(location, rocks, extents):
    """Return all the locations adjacent to location (up, down, left, right)
    that are on the grid GTE (0,0) and LT extents, and not a rock"""
    old_row, old_col = location
    max_row, max_col = extents
    neighbors = []
    for row in [old_row - 1, old_row + 1]:
        if row >= 0 and row < max_row and (row, old_col) not in rocks:
            neighbors.append((row, old_col))
    for col in [old_col - 1, old_col + 1]:
        if col >= 0 and col < max_col and (old_row, col) not in rocks:
            neighbors.append((old_row, col))
    return neighbors


def take_steps_v2(start, rocks, size, steps):
    """Return all the possible tiles that could be the final
    resting place after taking steps from start
    The grid has no bounds the values, and repeats in 4 direction

    This simple solution, works correctly, but takes way to long, even for
    steps == 500.  An optimization is needed."""
    origins = [start]
    for _ in range(steps):
        destinations = set()
        for location in origins:
            for neighbor in valid_neighbors_v2(location, rocks, size):
                destinations.add(neighbor)
        origins = destinations
    return destinations


def valid_neighbors_v2(location, rocks, size):
    """Return all the locations adjacent to location (up, down, left, right)
    and not a rock.
    The grid has no bounds the values, and repeats in 4 direction"""
    old_row, old_col = location
    max_row, max_col = size
    neighbors = []
    for row in [old_row - 1, old_row + 1]:
        if (row % max_row, old_col % max_col) not in rocks:
            neighbors.append((row, old_col))
    for col in [old_col - 1, old_col + 1]:
        if (old_row % max_row, col % max_col) not in rocks:
            neighbors.append((old_row, col))
    return neighbors


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
