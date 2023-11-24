"""A solution to an Advent of Code puzzle."""

# Data Model:
# ===========
# lines is a list of "\n" terminated strings from the input file

import os.path  # to get the directory name of the script (current puzzle year-day)

INPUT = "input.txt"


def part1(lines):
    """Solve part 1 of the puzzle."""
    print("Warning the part 1 solution is slow (about 8 seconds)")
    data = parse(lines)
    # print("Initial configuration")
    # display(data)
    for round_number in range(10):
        data, _ = update(data, round_number)
        # print("\nRound:",round_number + 1)
        # display(data)
    result = empty(data)
    return result


def part2(lines):
    """Solve part 2 of the puzzle."""
    print("Warning the part 2 solution is VERY slow (about 17 minutes)")

    data = parse(lines)
    round_number = 0
    while True:
        data, no_moves = update(data, round_number)
        if no_moves:
            break
        round_number += 1
    return round_number + 1  # my round_numbers start with 0, the puzzle starts with 1


def parse(lines):
    """Parse the puzzle input file into a usable data structure."""
    data = []
    for row, line in enumerate(lines):
        line = line.strip()
        for col, char in enumerate(line):
            if char == "#":
                data.append((row, col))
    return data


def find_extents(data):
    """FInd the extents of the data."""
    min_row = 1e10
    max_row = -1e10
    min_col = 1e10
    max_col = -1e10
    for row, col in data:
        if row < min_row:
            min_row = row
        if col < min_col:
            min_col = col
        if row > max_row:
            max_row = row
        if col > max_col:
            max_col = col
    return (min_row, min_col, max_row, max_col)


def empty(data):
    """Find the count of the empty space."""
    min_row, min_col, max_row, max_col = find_extents(data)
    area = (1 + max_row - min_row) * (1 + max_col - min_col)
    occupied = len(data)
    return area - occupied


def display(data):
    """Draw the data structure as represented in the description (for debugging)"""
    min_row, min_col, max_row, max_col = find_extents(data)
    n_rows = 1 + max_row - min_row
    n_cols = 1 + max_col - min_col
    grid = []
    for _ in range(n_rows):
        row = ["."] * n_cols
        grid.append(row)
    for row, col in data:
        grid[row - min_row][col - min_col] = "#"
    print("\nScore =", n_rows * n_cols - len(data))
    for row in grid:
        print("".join(row))


MOVES = [
    [(-1, -1), (-1, 0), (-1, 1)],  # NE, N, NW
    [(1, -1), (1, 0), (1, 1)],  # SE, S, SW
    [(-1, -1), (0, -1), (1, -1)],  # NW, W, SW
    [(-1, 1), (0, 1), (1, 1)],  # NE, E, SE
]
ADJACENT = [
    (-1, -1),
    (-1, 0),
    (-1, 1),
    (1, -1),
    (1, 0),
    (1, 1),
    (0, -1),
    (0, 1),
]  # NE, N, NW, SE, S, SW, W, E


def update(data, round_number):
    """Update the puzzle state for the round_number."""

    potential_moves = get_potential_moves(data, round_number)

    no_moves = True
    for location in potential_moves:
        if location:
            no_moves = False
            break

    if no_moves:
        return data, True

    conflicts = set()
    for location in potential_moves:
        if location:
            count = potential_moves.count(location)
            if count > 1:
                conflicts.add(location)

    new_data = []
    # move_count = 0
    for i, location in enumerate(potential_moves):
        if location and location not in conflicts:
            new_data.append(location)
            # move_count += 1
        else:
            new_data.append(data[i])

    # print("round_number", "elves", len(data), "moves", move_count, "conflicts", len(conflicts))
    return new_data, False


def get_potential_moves(data, round_number):
    """Get the available new locations."""
    potential_moves = []
    for location in data:
        (row, col) = location
        new_location = None
        # check no move option (all adjacent squares are empty)
        clear = True
        for d_row, d_col in ADJACENT:
            if (row + d_row, col + d_col) in data:
                clear = False
                break
        if not clear:
            for i in range(round_number, round_number + 4):
                free = True
                moves = MOVES[i % len(MOVES)]
                for d_row, d_col in moves:
                    if (row + d_row, col + d_col) in data:
                        free = False
                        break
                if free:
                    new_location = (row + moves[1][0], col + moves[1][1])
                    break
        potential_moves.append(new_location)
    return potential_moves


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
