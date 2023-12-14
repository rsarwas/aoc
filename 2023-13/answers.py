"""A solution to an Advent of Code puzzle."""

# Data Model:
# ===========
# _lines_ is a list of "\n" terminated strings from the input file.


import os.path  # to get the directory name of the script (current puzzle year-day)

INPUT = "input.txt"


def part1(lines):
    """Solve part 1 of the problem."""
    data = parse(lines)
    horizontals = [horizontal_reflection(grid) for grid in data]
    # Note, there is only one reflection per map, we could speed this up by only
    # checking for a vertical if we did not find a horizontal
    verticals = [vertical_reflection(grid) for grid in data]
    # print(horizontals)
    # print(verticals)
    # The row and column indexes start at zero in code, but 1 in the problem
    horizontals = [100 * (h + 1) for h in horizontals if h is not None]
    verticals = [v + 1 for v in verticals if v is not None]
    # print(horizontals, verticals)
    total = sum(horizontals) + sum(verticals)
    return total


def part2(lines):
    """Solve part 2 of the problem."""
    data = parse(lines)
    total = len(data)
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


def vertical_reflection(grid):
    """Return the column number on the left of the line of vertical reflection, or None."""
    # transposed the grid/matrix and then use the solution for the horizontal line of reflecton
    rotated = transpose(grid)
    return horizontal_reflection(rotated)


def horizontal_reflection(grid):
    """Return the row number on the top of the line of horizontal reflection, or None."""
    # for row in grid:
    #     print(row)
    for row_id, row in enumerate(grid[:-1]):
        next_row = grid[row_id + 1]
        if row == next_row:
            # print(len(grid), row_id, row, row_id + 1, next_row)
            if valid_reflection(row_id, grid):
                # print(row_id)
                return row_id
    # print(None)
    return None


def valid_reflection(row_id, grid):
    """Return True if all the lines above and below match (reflect)"""
    rows_below = list(range(row_id + 2, len(grid)))
    rows_above = list(range(0, row_id))
    # print(rows_below, rows_above)
    rows_above.reverse()
    # Note: by default zip stops when the shorted list is exhausted
    for row1, row2 in zip(rows_above, rows_below):
        # print(row1, grid[row1], row2, grid[row2])
        if grid[row1] != grid[row2]:
            return False
    return True


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
