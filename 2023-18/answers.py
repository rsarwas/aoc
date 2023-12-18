"""A solution to an Advent of Code puzzle."""

# Data Model:
# ===========
# _lines_ is a list of "\n" terminated strings from the input file.


import os.path  # to get the directory name of the script (current puzzle year-day)

INPUT = "input.txt"
RIGHT = "R"
LEFT = "L"
UP = "U"
DOWN = "D"


def part1(lines):
    """Solve part 1 of the problem."""
    dig_plan = parse(lines)
    perimeter = dig(dig_plan)
    # After struggling to find a solution to similliar to 2023-10,
    # I resorted to a grid filling algorithm with a manually selected
    # interior point.
    grid = fill(perimeter)
    return area(grid)


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
        direction, distance, color = line.split(" ")
        data.append((direction, int(distance), color))
    return data


def dig(dig_plan):
    """Return a list of coordinates of 1 meter cubes that have been excavated"""
    current = (0, 0)
    perimeter = [current]
    for direction, distance, _ in dig_plan:
        for _ in range(distance):
            current = move(current, direction)
            perimeter.append(current)
    return perimeter


def move(location, direction):
    """Return the new location after moving one space in the direction given"""
    row, col = location
    if direction == RIGHT:
        col += 1
    elif direction == LEFT:
        col -= 1
    elif direction == UP:
        row -= 1
    else:  # DOWN
        row += 1
    return (row, col)


def area(grid):
    """Return the total of the filled (1) tiles; empty tiles are 0"""
    return sum([sum(row) for row in grid])


def fill(perimeter):
    """Create a grid and fill it"""
    min_row, max_row = 0, 0
    min_col, max_col = 0, 0
    for row, col in perimeter:
        if row < min_row:
            min_row = row
        if row > max_row:
            max_row = row
        if col < min_col:
            min_col = col
        if col > max_col:
            max_col = col
    n_cols = max_col - min_col + 1
    n_rows = max_row - min_row + 1

    grid = []
    for _ in range(n_rows):
        row = [0] * n_cols
        grid.append(row)
    for row, col in perimeter:
        grid[row - min_row][col - min_col] = 1
    # for row in grid:
    #    print("".join(row))
    print(grid[0])
    print(grid[1])
    grid[1][101] = 1
    print(grid[1])
    # FILL
    # start with an interior node, and find all the empty adjacent nodes.
    # ill them and add their neighbors, etc
    # known_interior = (1, 1) # test file
    known_interior = (1, 101)  # puzzle file
    unmarked_interior = [known_interior]
    while len(unmarked_interior) > 0:
        node = unmarked_interior.pop()
        mark_interior(grid, node)
        for neighbor in find_unmarked_neighbors(node, grid):
            unmarked_interior.append(neighbor)
    # print()
    # for row in grid:
    #    print("".join(row))
    return grid


def mark_interior(grid, node):
    """Flag the node location in grid as interior"""
    row, col = node
    grid[row][col] = 1


def find_unmarked_neighbors(node, grid):
    """Return the neighbors (U,D,L,R) of node that are not already marked as interior/perimeter"""
    row, col = node
    neighbors = []
    above = (row - 1, col)
    below = (row + 1, col)
    left = (row, col - 1)
    right = (row, col + 1)
    for neighbor in [above, below, left, right]:
        row, col = neighbor
        try:
            if grid[row][col] == 0:
                neighbors.append(neighbor)
        except IndexError:
            pass
    return neighbors


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
