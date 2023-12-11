"""A solution to an Advent of Code puzzle."""

# Data Model:
# ===========
# _lines_ is a list of "\n" terminated strings from the input file.


import os.path  # to get the directory name of the script (current puzzle year-day)

INPUT = "input.txt"
DEBUG = False
GALAXY = "#"


def part1(lines):
    """Solve part 1 of the problem."""
    expansion_factor = 2
    return compute_size(lines, expansion_factor)


def part2(lines):
    """Solve part 2 of the problem."""
    expansion_factor = 1000000
    return compute_size(lines, expansion_factor)


def compute_size(lines, factor):
    """Compute the sum of the distances between the galaxies in an expanded universe."""
    universe = [line.strip() for line in lines]
    galaxies = find_galaxies(universe)
    empty_rows = find_empty(galaxies, "R")
    empty_cols = find_empty(galaxies, "C")
    galaxies = expand(galaxies, empty_rows, empty_cols, factor)
    if DEBUG:
        print(empty_rows)
        print(empty_cols)
        print(galaxies)
    distances = all_min_distances(galaxies)
    return sum(distances)


def find_empty(galaxies, what):
    """Return the index of the empty rows (what == 'R') or cols (what == 'C') in
    the list of galaxies.  Galaxies is a list of (row,col) tuples for the location
    of the galaxy.  A row/col is empty if there are no galaxy with that row/col value.
    """
    if what == "R":
        items = [row for (row, _) in galaxies]
    else:
        items = [col for (_, col) in galaxies]
    possible = set(range(max(items)))
    missing = list(possible - set(items))
    missing.sort()
    return missing


def expand(galaxies, empty_rows, empty_cols, factor):
    """Increase the location of the galaxies by expanding
    the empty rows/cols per the EXPANSION_FACTOR."""
    rows = [row for (row, _) in galaxies]
    row_locs = location_map(rows, empty_rows, factor)
    cols = [col for (_, col) in galaxies]
    col_locs = location_map(cols, empty_cols, factor)
    # Create a new list of the new galaxy locations
    new_galaxies = []
    for row, col in galaxies:
        new_location = (row_locs[row], col_locs[col])
        new_galaxies.append(new_location)
    return new_galaxies


def location_map(items, empties, factor):
    """Create a dictionary mapping existing locations to new locations"""
    new_locs = {}
    new_loc = -1
    for old_loc in range(max(items) + 1):
        if old_loc in empties:
            new_loc += factor
        else:
            new_loc += 1
        new_locs[old_loc] = new_loc
    return new_locs


def find_galaxies(universe):
    """Return a list of (row,col) tuples for the location of each galaxy."""
    galaxies = []
    for row, line in enumerate(universe):
        for col, char in enumerate(line):
            if char == GALAXY:
                galaxies.append((row, col))
    return galaxies


def all_min_distances(galaxies):
    """Return a list of distances between each pair of galaxies"""
    distances = []
    for index, galaxy1 in enumerate(galaxies):
        r1, c1 = galaxy1
        for galaxy2 in galaxies[index + 1 :]:
            r2, c2 = galaxy2
            distance = abs(r2 - r1) + abs(c2 - c1)
            distances.append(distance)
    return distances


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
