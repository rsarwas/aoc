"""A solution to an Advent of Code puzzle."""

# Data Model:
# ===========
# _lines_ is a list of "\n" terminated strings from the input file.


import os.path  # to get the directory name of the script (current puzzle year-day)

INPUT = "input.txt"
FIXED = "#"
MOBILE = "O"
OPEN = "."


def part1(lines):
    """Solve part 1 of the problem."""
    grid = parse(lines)
    grid = tilt_north(grid)
    total = add_up_rocks(grid)
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
        items = list(line.strip())
        data.append(items)
    return data


def tilt_north(grid):
    """Shift all of the mobile rocks (O) to the north as far as possible.
    They will stack up along the north wall or an intermediate immobile rock (#)"""
    # work from left to right, top to bottom, moving anything mobile as far north as possible
    for col in range(len(grid[0])):
        barrier = 0
        for row_id, data in enumerate(grid):
            item = data[col]
            if item == OPEN:
                continue
            if item == FIXED:
                barrier = row_id + 1
            else:  # item == MOBILE
                data[col] = OPEN
                grid[barrier][col] = MOBILE
                barrier += 1
    return grid


def add_up_rocks(grid):
    """Return the total weight of the rocks in the grid.
    Rocks at the top weigh more; proportional to the size of the grid"""
    size = len(grid)
    total = 0
    for i, row in enumerate(grid):
        multiplier = size - i  # bottom row = 1, top row = size
        count = len([x for x in row if x == MOBILE])
        weight = count * multiplier
        total += weight
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
