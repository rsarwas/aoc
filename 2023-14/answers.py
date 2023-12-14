"""A solution to an Advent of Code puzzle."""

# Data Model:
# ===========
# _lines_ is a list of "\n" terminated strings from the input file.


import os.path  # to get the directory name of the script (current puzzle year-day)
import hashlib  # to hash the grid

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
    grid = parse(lines)
    n = 1_000_000_000
    # assume at some point the grid will go into a repeating cycle
    hashes = {}
    weights = {}
    for i in range(1, n):
        grid = cycle(grid)
        h = identify(grid)
        if h in hashes:
            cycle_start = hashes[h]
            cycle_size = i - cycle_start
            break
        hashes[h] = i
        weights[i] = add_up_rocks(grid)
    i = cycle_start + ((n - cycle_start) % cycle_size)
    total = weights[i]
    return total


def parse(lines):
    """Convert the lines of text into a useful data model."""
    data = []
    for line in lines:
        items = list(line.strip())
        data.append(items)
    return data


def tilt_north(grid):
    """Shift all of the mobile rocks (O) to the north (up) as far as possible.
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


def tilt_west(grid):
    """Shift all of the mobile rocks (O) to the west (left) as far as possible.
    They will stack up along the left wall or an intermediate immobile rock (#)"""
    # work from top to bottom, left to right, moving anything mobile as far left as possible
    for row_id, row in enumerate(grid):
        barrier = 0
        for col_id, item in enumerate(row):
            if item == OPEN:
                continue
            if item == FIXED:
                barrier = col_id + 1
            else:  # item == MOBILE
                grid[row_id][col_id] = OPEN
                grid[row_id][barrier] = MOBILE
                barrier += 1
    return grid


def tilt_east(grid):
    """Shift all of the mobile rocks (O) to the east (right) as far as possible.
    They will stack up along the right wall or an intermediate immobile rock (#)"""
    # work from top to bottom, right to left, moving anything mobile as far right as possible
    for row_id, row in enumerate(grid):
        barrier = len(row) - 1
        for col_id in range(len(row) - 1, -1, -1):
            item = row[col_id]
            if item == OPEN:
                continue
            if item == FIXED:
                barrier = col_id - 1
            else:  # item == MOBILE
                grid[row_id][col_id] = OPEN
                grid[row_id][barrier] = MOBILE
                barrier -= 1
    return grid


def tilt_south(grid):
    """Shift all of the mobile rocks (O) to the south as far as possible.
    They will stack up along the south wall or an intermediate immobile rock (#)"""
    # work from left to right, bottom to top, moving anything mobile as far south as possible
    for col in range(len(grid[0])):
        barrier = len(grid) - 1
        for row_id in range(len(grid) - 1, -1, -1):
            data = grid[row_id]
            item = data[col]
            if item == OPEN:
                continue
            if item == FIXED:
                barrier = row_id - 1
            else:  # item == MOBILE
                data[col] = OPEN
                grid[barrier][col] = MOBILE
                barrier -= 1
    return grid


def cycle(grid):
    """Tilt the grid in all four directions"""
    grid = tilt_north(grid)
    grid = tilt_west(grid)
    grid = tilt_south(grid)
    grid = tilt_east(grid)
    return grid


def display(grid):
    """Format the grid and print to standard out"""
    print()
    for row in grid:
        print("".join(row))
    print()


def identify(grid):
    """Create a unique hash of the grid, so we can look for repeating patterns."""
    s = "".join(["".join(row) for row in grid])
    s = s.encode("ascii", "ignore")
    return hashlib.md5(s).hexdigest()


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
