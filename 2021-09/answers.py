# Data Model:
# ===========
# lines is a list of "\n" terminated strings from the input file
# each character in the line is in {0..9}, with 0 the lowest, and 9
# the highest
# low_points is a list of (row,column) tuples where all adjacent
# cells are all greater (or equal?) - diagonal does not count
# a basin map is a int matrix (list of lists) with zeros at the basin
# boundaries (9s in the lines), and the low_point index +1 for the
# low point that this basin belongs to (0 are not in any basin)
# every point will be in only 1 basin (per the problem statement)
# The size of basin x (x in {1..n} is the number of locations in the
# basin map which have the value of x
# sizes is a list of the basin sizes, in no particular order

import math  # for prod (product of list elements)


def part1(lines):
    low_points = get_low_points(lines)
    total = 0
    for r, c in low_points:
        risk = int(lines[r][c]) + 1
        total += risk
    return total


def part2(lines):
    low_points = get_low_points(lines)
    basin_map = make_map(low_points, lines)
    basin_sizes = get_sizes(basin_map)
    # print(basin_sizes)
    total_top_three = math.prod(sorted(basin_sizes)[-3:])
    return total_top_three


def get_low_points(lines):
    low_points = []
    max_row = len(lines) - 1
    max_col = len(lines[0].strip()) - 1
    for row, line in enumerate(lines):
        for col, height in enumerate(line.strip()):
            up = None if row == 0 else lines[row - 1][col]
            left = None if col == 0 else lines[row][col - 1]
            down = None if row == max_row else lines[row + 1][col]
            right = None if col == max_col else lines[row][col + 1]
            if up and height >= up:
                continue
            if left and height >= left:
                continue
            if down and height >= down:
                continue
            if right and height >= right:
                continue
            low_points.append((row, col))
    return low_points


def make_map(low_points, lines):
    max_row = len(lines) - 1
    max_col = len(lines[0].strip()) - 1
    map = []
    for _ in range(max_row + 1):
        map.append([0] * (max_col + 1))
    for i, (row, col) in enumerate(low_points):
        basin_id = i + 1
        map[row][col] = basin_id
        fill_basin(map, basin_id, row, col, max_row, max_col, lines)
    # print(map)
    return map


def fill_basin(map, basin_id, row, col, max_row, max_col, lines):
    # a recursive function to fill all the points adjacent to a
    # the given point if they are not already filled, or not a basin
    # edge (the edge of the map, or a "9" in the puzzle input)
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        r = row + dy
        c = col + dx
        if r > max_row or r < 0 or c > max_col or c < 0:
            continue
        if lines[r][c] == "9":
            continue
        if map[r][c] != 0:
            continue
        map[r][c] = basin_id
        fill_basin(map, basin_id, r, c, max_row, max_col, lines)


def get_sizes(map):
    sizes = {}
    for row in map:
        for basin_id in row:
            if basin_id == 0:
                continue
            if basin_id in sizes:
                sizes[basin_id] += 1
            else:
                sizes[basin_id] = 1
    return sizes.values()


if __name__ == "__main__":
    # lines = open("test.txt").readlines() # as a list of line strings
    lines = open("input.txt").readlines()  # as a list of line strings
    print(f"Part 1: {part1(lines)}")
    print(f"Part 2: {part2(lines)}")
