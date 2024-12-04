"""A solution to an Advent of Code puzzle."""

# Data Model:
# ===========
# _lines_ is a list of "\n" terminated strings from the input file.


import os.path  # to get the directory name of the script (current puzzle year-day)

INPUT = "input.txt"


def part1(lines):
    """Solve part 1 of the problem."""
    data = parse(lines)
    total = 0
    num_rows = len(data)
    num_cols = len(data[0])
    for r, row in enumerate(data):
        for c, char in enumerate(row):
            if char == "X":
                count = find_xmas(r, num_rows, c, num_cols, data)
                total += count
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
        data.append(line)
    return data


def find_xmas(r, num_rows, c, num_cols, data):
    """Return the number (0..8) of occurrences of "XMAS"
    found in the letters in the grid"""
    found = 0
    if r > 2:  # search up
        if data[r - 1][c] == "M" and data[r - 2][c] == "A" and data[r - 3][c] == "S":
            found += 1
    if r > 2 and c < num_cols - 3:  # search up, right
        if (
            data[r - 1][c + 1] == "M"
            and data[r - 2][c + 2] == "A"
            and data[r - 3][c + 3] == "S"
        ):
            found += 1
    if c < num_cols - 3:  # search right
        if data[r][c + 1] == "M" and data[r][c + 2] == "A" and data[r][c + 3] == "S":
            found += 1
    if r < num_rows - 3 and c < num_cols - 3:  # search down, right
        if (
            data[r + 1][c + 1] == "M"
            and data[r + 2][c + 2] == "A"
            and data[r + 3][c + 3] == "S"
        ):
            found += 1
    if r < num_rows - 3:  # search down
        if data[r + 1][c] == "M" and data[r + 2][c] == "A" and data[r + 3][c] == "S":
            found += 1
    if r < num_rows - 3 and c > 2:  # search down, left
        if (
            data[r + 1][c - 1] == "M"
            and data[r + 2][c - 2] == "A"
            and data[r + 3][c - 3] == "S"
        ):
            found += 1
    if c > 2:  # search left
        if data[r][c - 1] == "M" and data[r][c - 2] == "A" and data[r][c - 3] == "S":
            found += 1
    if c > 2 and r > 2:  # search left, up
        if (
            data[r - 1][c - 1] == "M"
            and data[r - 2][c - 2] == "A"
            and data[r - 3][c - 3] == "S"
        ):
            found += 1
    return found


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
