"""A solution to an Advent of Code puzzle."""

# Data Model:
# ===========
# _lines_ is a list of "\n" terminated strings from the input file.


import os.path  # to get the directory name of the script (current puzzle year-day)

INPUT = "input.txt"


def part1(lines):
    """Solve part 1 of the problem."""
    data = parse(lines)
    total = summarize(data, remove_smudge=False)
    return total


def part2(lines):
    """Solve part 2 of the problem."""
    data = parse(lines)
    total = summarize(data, remove_smudge=True)
    return total


def parse(lines):
    """Convert the lines of text into a useful data model."""
    data = "".join(lines)
    data = data.split("\n\n")
    maps = []
    for line_group in data:
        # Remove any empty lines (at least one at the end) from the grids
        grid = [line for line in line_group.split("\n") if line]
        maps.append(grid)
    return maps


def summarize(data, remove_smudge=False):
    """Return a total count of the lines of reflection in the data.
    data is a list of grids. row/col numbers start with 1. Columns
    are worth 1 point, rows are worth 100 points."""
    total = 0
    # print("line reflection points")
    # if remove_smudge:
    #     print("After Removing Smudges")
    # else:
    #     print("Without Removing Smudges")
    for grid in data:
        # print("  Column reflection points")
        column_num = find_reflection(grid, remove_smudge)
        if column_num is not None:
            # print(f"  Woot Woot: reflection at column {column_num}")
            total += column_num
        # if we found a column, we can skip row reflection search
        else:
            # print("  Row reflection points")
            grid = transpose(grid)
            row_num = find_reflection(grid, remove_smudge)
            if row_num is not None:
                # print(f"  Woot Woot: reflection at row {row_num}")
                total += 100 * row_num
    return total


def find_reflection(grid, remove_smudge):
    """Return the column number (starting with 1) of the grid, to the left
    of the vertical line of reflection. Return None if no reflection."""
    # Count the number of rows that have the same offset to a palindrome
    counts = reflection_offset_counts(grid)
    # If there is a smudge then one line can be fixed, so we match one less than all
    matches_needed = len(grid)
    if remove_smudge:
        matches_needed -= 1
    for offset, count in counts.items():
        if count == matches_needed:
            column = reflection_location(offset, len(grid[0]))
            return column
    return None


def reflection_location(offset, line_length):
    """Returns the row/col number above/left of the reflection line.
    offset is the number of columns to remove from the start (if positive)
    or end (if negative) of line"""
    if offset < 0:
        return (line_length + offset) // 2
    return offset + (line_length - offset) // 2


def reflection_offset_counts(grid):
    """Return a hashmap with the number of lines that each offset has."""
    counts = {}
    for line in grid:
        offsets = reflection_offsets(line)
        # print("  ", offsets)
        for offset in offsets:
            if offset not in counts:
                counts[offset] = 0
            counts[offset] += 1
    return counts


def is_palindrome(line, n, rev_line=None):
    """Return true if line is a palindrome when omitting the first
    n characters (if n is positive), or the last n characters if n is negative.
    providing the reverse of line will be more efficient if this is called with various n.
    n must be less than len(line) - 2; this leaves 2 characters to compare.
    comparing 1 or less makes no sense in this puzzle."""
    if abs(n) > len(line) - 2:
        raise ValueError
    if rev_line is None:
        if isinstance(line, list):
            rev_line = list(reversed(line))
        else:
            rev_line = "".join(reversed(line))
    if n == 0:
        return line == rev_line
    if n > 0:
        return line[n:] == rev_line[:-n]
    return line[:n] == rev_line[-n:]


def reflection_offsets(line):
    """Return all the offsets for a reflection point in a line of text.
    An offset is the amount of text to remove at the start (positive offset), or
    the end (negative offset) of a line to create a palindrome.
    line can be a string or a list of characters."""
    if isinstance(line, list):
        rev_line = list(reversed(line))
    else:
        rev_line = "".join(reversed(line))
    r = range(0, len(line), 2)
    if len(line) % 2 == 1:
        r = range(1, len(line), 2)
    offsets = []
    for i in r:
        for m in (-1, 1):
            n = m * i
            if is_palindrome(line, n, rev_line):
                offsets.append(n)
    return offsets


def transpose(matrix):
    """Returns the transpose of the matrix X
    note that the rows in the input matrix can be a list or a string, but
    will be returned as a list."""
    result = [[matrix[j][i] for j in range(len(matrix))] for i in range(len(matrix[0]))]
    return result


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
