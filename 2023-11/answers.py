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
    universe = [line.strip() for line in lines]
    universe = expand(universe)
    if DEBUG:
        for line in universe:
            print("".join(line))
    galaxies = find_galaxies(universe)
    distances = all_min_distances(galaxies)
    return sum(distances)


def part2(lines):
    """Solve part 2 of the problem."""
    universe = [line.strip() for line in lines]
    return len(universe)


def expand(universe):
    """Convert the lines of text into a useful data model."""
    # empty_col = find_empty_columns
    universe = add_rows(universe)
    universe = transpose(universe)
    universe = add_rows(universe)
    universe = transpose(universe)
    return universe


def add_rows(universe):
    """If a row in the universe map is empty then add another one"""
    new_universe = []
    for line in universe:
        new_universe.append(line)
        if row_is_empty(line):
            new_universe.append(line)
    return new_universe


def transpose(matrix):
    """Returns the transpose of the matrix X
    note that the rows in the input matrix can be a list or a string, but
    will be returned as a list."""
    result = [[matrix[j][i] for j in range(len(matrix))] for i in range(len(matrix[0]))]
    return result


def row_is_empty(line):
    """Return True if there are no galaxies in this row of the universe"""
    for char in line:
        if char == GALAXY:
            return False
    return True


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
