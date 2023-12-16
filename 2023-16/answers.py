"""A solution to an Advent of Code puzzle."""

# Data Model:
# ===========
# _lines_ is a list of "\n" terminated strings from the input file.


import os.path  # to get the directory name of the script (current puzzle year-day)

INPUT = "input.txt"
DEBUG = False
EMPTY = "."
TILT_UP = "/"
TILT_DOWN = "\\"
SPLIT_EW = "-"
SPLIT_NS = "|"
RIGHT = ">"
LEFT = "<"
UP = "^"
DOWN = "v"


def part1(lines):
    """Solve part 1 of the problem."""
    size, grid = parse(lines)
    start = (0, 0, RIGHT)
    total = energized(grid, size, start)
    return total


def part2(lines):
    """Solve part 2 of the problem."""
    size, grid = parse(lines)
    rows, cols = size
    max_energy = 0
    for row in range(rows):
        start = (row, 0, RIGHT)
        energy = energized(grid, size, start)
        if energy > max_energy:
            max_energy = energy
        start = (row, cols - 1, LEFT)
        energy = energized(grid, size, start)
        if energy > max_energy:
            max_energy = energy
    for col in range(cols):
        start = (0, col, DOWN)
        energy = energized(grid, size, start)
        if energy > max_energy:
            max_energy = energy
        start = (rows - 1, col, UP)
        energy = energized(grid, size, start)
        if energy > max_energy:
            max_energy = energy
    return max_energy


def parse(lines):
    """Convert the lines of text into a useful data model."""
    grid = {}
    rows = len(lines)
    for row, line in enumerate(lines):
        line = line.strip()
        cols = len(line)
        for col, char in enumerate(line):
            if char != EMPTY:
                grid[(row, col)] = char
    return (rows, cols), grid


def energized(grid, size, start):
    """Return the number of tiles energized (light passed through) after
    the grid reaches a steady state."""
    visited = set()
    visited.add(start)
    current = [start]
    while current:
        temp_current = update(current, grid, size)
        current = []
        for photon in temp_current:
            if photon not in visited:
                visited.add(photon)
                current.append(photon)
    return count_tiles(visited)


def update(current, grid, size):
    """Given a list of current photons (positions and directions), Return a new updated list.
    A photon that goes off the grid is removed from the list.  A photon that hits a splitter
    edgewise changes direction and adds a new photon to the list. A photon that hits a mirror
    changes direction."""
    new_list = []
    for photon in current:
        (row, col, direction) = photon
        group = None
        if (row, col) in grid:
            tile = grid[(row, col)]
            if tile == TILT_UP:
                row, col, direction = move_in_mirror_up(row, col, direction)
            if tile == TILT_DOWN:
                row, col, direction = move_in_mirror_dn(row, col, direction)
            if tile == SPLIT_EW:
                group = move_in_split_ew(row, col, direction)
            if tile == SPLIT_NS:
                group = move_in_split_ns(row, col, direction)
        else:  # empty tile
            row, col, direction = move_in_empty(row, col, direction)

        if 0 <= row < size[0] and 0 <= col < size[1]:
            new_list.append((row, col, direction))
        if group is not None:
            for row, col, direction in group:
                if 0 <= row < size[0] and 0 <= col < size[1]:
                    new_list.append((row, col, direction))
    return new_list


def move_in_empty(row, col, direction):
    """Return the new location passing through an empty tile.
    The direction is returned even though it is unchanged, for
    compatibility with the splitter functions."""
    if direction == RIGHT:
        return (row, col + 1, direction)
    if direction == LEFT:
        return (row, col - 1, direction)
    if direction == UP:
        return (row - 1, col, direction)
    # direction == DOWN
    return (row + 1, col, direction)


def move_in_mirror_up(row, col, direction):
    """Return the new position after hitting a / mirror"""
    if direction == RIGHT:
        return (row - 1, col, UP)
    if direction == LEFT:
        return (row + 1, col, DOWN)
    if direction == UP:
        return (row, col + 1, RIGHT)
    # direction == DOWN
    return (row, col - 1, LEFT)


def move_in_mirror_dn(row, col, direction):
    """Return the new position after hitting a \\ mirror"""
    if direction == RIGHT:
        return (row + 1, col, DOWN)
    if direction == LEFT:
        return (row - 1, col, UP)
    if direction == UP:
        return (row, col - 1, LEFT)
    # direction == DOWN
    return (row, col + 1, RIGHT)


def move_in_split_ew(row, col, direction):
    """Return a list of new positions after hitting an EW (-) splitter"""
    if direction in [RIGHT, LEFT]:
        return [move_in_empty(row, col, direction)]
    # direction in [UP, DOWN]
    return [(row, col - 1, LEFT), (row, col + 1, RIGHT)]


def move_in_split_ns(row, col, direction):
    """Return the new position(s) after hitting a NS (|) splitter"""
    if direction in [UP, DOWN]:
        return [move_in_empty(row, col, direction)]
    # direction in [RIGHT, LEFT]
    return [(row - 1, col, UP), (row + 1, col, DOWN)]


def count_tiles(visited):
    """Return the number of unique tiles in visited.
    Each item in visited has a location and direction"""
    locations = set()
    for row, col, _ in visited:
        locations.add((row, col))
    if DEBUG:
        l = list(locations)
        l.sort()
        print(l)
    return len(locations)


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
