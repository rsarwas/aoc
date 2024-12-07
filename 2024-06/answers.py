"""A solution to an Advent of Code puzzle."""

# Data Model:
# ===========
# _lines_ is a list of "\n" terminated strings from the input file.


import os.path  # to get the directory name of the script (current puzzle year-day)

INPUT = "input.txt"

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3


def part1(lines):
    """Solve part 1 of the problem."""
    obstructions, guard, size = parse(lines)
    locations = guard_path(obstructions, guard, size)
    return len(set(locations))


def part2(lines):
    """Solve part 2 of the problem."""
    obstructions, guard, size = parse(lines)
    locations = guard_path(obstructions, guard, size)
    loops = 0
    # To have any impact, a new obstruction would need to be on the path the guard walks
    # ignore the start (location[0]) and only check each location once.
    for new_obstruction in set(locations[1:]):  # ignore the start and duplicates
        if is_loop(guard, obstructions + [new_obstruction], size):
            # print("loop", new_obstruction)
            loops += 1
    return loops


def parse(lines):
    """Convert the lines of text into a useful data model."""
    obstructions = []
    guard = None
    size = None
    row = 0
    for row, line in enumerate(lines):
        line = line.strip()
        for col, char in enumerate(line):
            if char == "#":
                obstructions.append((col, row))
            if char == "^":
                guard = (col, row, UP)
        size = len(line)
    return obstructions, guard, size


def guard_path(obstructions, guard, size):
    """Return a list of all the unigue coordinate pairs that the guard occupies
    start at guard location/direction. continue until the guard walks off the grid
    if the guard would an obstruction, turn right"""
    locations = []
    while guard[0] >= 0 and guard[0] < size and guard[1] >= 0 and guard[1] < size:
        locations.append((guard[0], guard[1]))
        guard = next_location(guard, obstructions)
    return locations


def next_location(guard, obstructions):
    """return the next location and direction of the guard."""
    x, y, d = guard
    nx, ny = x, y
    if d == UP:
        ny = y - 1
    if d == RIGHT:
        nx = x + 1
    if d == DOWN:
        ny = y + 1
    if d == LEFT:
        nx = x - 1
    if (nx, ny) not in obstructions:
        return (nx, ny, d)
    else:
        nx, ny = x, y
        nd = (d + 1) % 4
        if nd == UP:
            ny = y - 1
        if nd == RIGHT:
            nx = x + 1
        if nd == DOWN:
            ny = y + 1
        if nd == LEFT:
            nx = x - 1
        return (nx, ny, nd)


def is_loop(guard, obstructions, size):
    """Return True if the guard gets stuck in a loop (i.e. ends up in the same
    place while going the same direction), or False if she exits the grid.

    This solution works on the test case, but not the real problem. 1518 is too high
    (it also takes several minutes to compute)
    """
    locations = set()
    while guard[0] >= 0 and guard[0] < size and guard[1] >= 0 and guard[1] < size:
        if guard in locations:
            return True
        locations.add(guard)
        guard = next_location(guard, obstructions)
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
