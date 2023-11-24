# Data Model:
# ===========
# lines is a list of "\n" terminated strings from the input file
# grid is a 10x10 matrix of ints from 0 to 10. Nominal values are
# 1 thru 9. 10 an 0 are similar, both indicate a cell that has
# flashed.  10 is after updating all cells, but before resolving
# which adjacent cells have flashed. 0 is all the cells that
# flashed in the previous round.


def part1(lines):
    grid = make_grid(lines)
    total = 0
    for _ in range(0, 100):
        update(grid)
        # print(f"grid")
        # for row in grid:
        #     print(row)
        total += flashed(grid)
    return total


def part2(lines):
    grid = make_grid(lines)
    for i in range(1, 1000):  # might need to expand the search space
        update(grid)
        if flashed(grid) == 100:
            return i
    return -1


def make_grid(lines):
    grid = []
    for line in lines:
        row = [int(n) for n in line.strip()]
        grid.append(row)
    return grid


def update(grid):
    rows = len(grid)
    cols = len(grid[0])
    for row in grid:
        for c in range(0, cols):
            row[c] += 1
    for r in range(0, rows):
        for c in range(0, cols):
            if grid[r][c] > 9:
                flash_cell(grid, r, c, rows, cols)


def flash_cell(grid, r, c, rows, cols):
    grid[r][c] = 0
    for dr, dc in [
        (-1, -1),
        (-1, 0),
        (-1, 1),
        (0, -1),
        (0, 1),
        (1, -1),
        (1, 0),
        (1, 1),
    ]:
        row = r + dr
        col = c + dc
        if row >= 0 and row < rows and col >= 0 and col < cols:
            if grid[row][col] != 0:  # only flash once
                grid[row][col] += 1  # update due to adjacent cell flashing
                if grid[row][col] > 9:
                    flash_cell(grid, row, col, rows, cols)


def flashed(grid):
    flashed = 0
    for row in grid:
        for cell in row:
            if cell == 0:
                flashed += 1
    return flashed


if __name__ == "__main__":
    # data = open("input.txt").read() # as one big string
    # lines = open("test.txt").readlines() # as a list of line strings
    lines = open("input.txt").readlines()  # as a list of line strings
    print(f"Part 1: {part1(lines)}")
    print(f"Part 2: {part2(lines)}")
