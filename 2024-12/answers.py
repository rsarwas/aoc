"""A solution to an Advent of Code puzzle."""

# Data Model:
# ===========
# _lines_ is a list of "\n" terminated strings from the input file.


import os.path  # to get the directory name of the script (current puzzle year-day)

INPUT = "test6fail.txt"


def part1(lines):
    """Solve part 1 of the problem."""
    data, size = parse(lines)
    regions = regionalize(data, size)
    total = 0
    for region in regions:
        area = len(region)
        perimeter = perim(region)
        # print("area", area, "perimeter", perimeter)
        total += area * perimeter
    return total


def part2(lines):
    """Solve part 2 of the problem."""

    # code works on test data, but 904679 is too low for real data.

    data, size = parse(lines)
    print(data)
    regions = regionalize(data, size)
    print(regions, len(regions))
    total = 0
    # count_sides(regions[1], size)
    for region in regions:
        area = len(region)
        sides = find_sides(region, size)
        count_sides = len(sides)
        print("area", area, "sides", len(sides))
        display(region, sides)
        total += area * count_sides
    return total


def parse(lines):
    """Convert the lines of text into a useful data model."""
    data = {}
    for row, line in enumerate(lines):
        line = line.strip()
        for col, char in enumerate(line):
            if char not in data:
                data[char] = []
            data[char].append((row, col))
    size = len(lines)
    return data, size


def regionalize(data, size):
    """break up the data into distinct regions"""
    regions = []
    for key in data:
        key_regions = separate(data[key], size)
        # print(key, key_regions)
        regions += key_regions
    return regions


def separate(plant, size):
    """Return a list of lists. Each list is a group of contiguous coordinates.
    plant is a list of all of the coordinates for that plant type."""
    regions = []
    while plant:
        coord = plant.pop()
        region = find_contiguous(coord, plant, size)
        regions.append(region)
    return regions


def find_contiguous(start, plant, size):
    """Find all the coords in plant that are contiguous to start.
    remove those coordinates from plant and return those coordinates in a list"""
    checked = []
    unchecked = [start]
    while unchecked:
        coord = unchecked.pop()
        checked.append(coord)
        r, c = coord
        if r - 1 >= 0 and (r - 1, c) in plant:
            plant.remove((r - 1, c))
            unchecked.append((r - 1, c))
        if r + 1 < size and (r + 1, c) in plant:
            plant.remove((r + 1, c))
            unchecked.append((r + 1, c))
        if c - 1 >= 0 and (r, c - 1) in plant:
            plant.remove((r, c - 1))
            unchecked.append((r, c - 1))
        if c + 1 < size and (r, c + 1) in plant:
            plant.remove((r, c + 1))
            unchecked.append((r, c + 1))
    return checked


def perim(region):
    """Return the perimeter of region.  Look at the adjacent squares
    for each square in region.  if the adjacent square is not in the region,
    then add one to the perimeter.  This will handle concave shapes and holes.
    Note that an adjacent square may be correctly counted multiple times.
    i.e. for a hole of size one, than square will be counted 4 times."""
    perimeter = 0
    for r, c in region:
        if (r - 1, c) not in region:
            perimeter += 1
        if (r + 1, c) not in region:
            perimeter += 1
        if (r, c - 1) not in region:
            perimeter += 1
        if (r, c + 1) not in region:
            perimeter += 1
    return perimeter


def find_sides(region, size):
    """Count and return the number of sides (of any length) enclosing the region.
    Do this by finding all the perimeter pieces, and then grouping them into
    contiguous chunks"""
    sides = []
    print(region)
    perimeter_parts = perim2(region)
    print(perimeter_parts, len(perimeter_parts))
    while perimeter_parts:
        side_part = perimeter_parts.pop()
        side = find_contiguous_side(side_part, perimeter_parts, size)
        sides.append(side)
    print("sides", sides, len(sides))
    return sides


def perim2(region):
    """Return the parts of the perimeter of region.
    See perim above for details."""
    perimeter = []
    for r, c in region:
        if (r - 1, c) not in region:
            perimeter.append((r - 1, c, "h"))
        if (r + 1, c) not in region:
            perimeter.append((r + 1, c, "h"))
        if (r, c - 1) not in region:
            perimeter.append((r, c - 1, "v"))
        if (r, c + 1) not in region:
            perimeter.append((r, c + 1, "v"))
    return perimeter


def find_contiguous_side(start, parts, size):
    """Find all the coords in parts that are contiguous to start.
    remove those coordinates from parts and return those coordinates in a list"""
    checked = []
    unchecked = [start]
    while unchecked:
        side_part = unchecked.pop()
        checked.append(side_part)
        r, c, d = side_part
        if d == "v":
            if r - 1 >= 0 and (r - 1, c, d) in parts and (r - 1, c, d) not in checked:
                parts.remove((r - 1, c, d))
                unchecked.append((r - 1, c, d))
            if r + 1 < size and (r + 1, c, d) in parts and (r + 1, c, d) not in checked:
                parts.remove((r + 1, c, d))
                unchecked.append((r + 1, c, d))
        if d == "h":
            if c - 1 >= 0 and (r, c - 1, d) in parts and (r, c - 1, d) not in checked:
                parts.remove((r, c - 1, d))
                unchecked.append((r, c - 1, d))
            if c + 1 < size and (r, c + 1, d) in parts and (r, c + 1, d) not in checked:
                parts.remove((r, c + 1, d))
                unchecked.append((r, c + 1, d))
    return checked


def display(region, sides):
    "Draw the region and the enclosing sides.  Used as a debugging aide."
    min_row, min_col, max_row, max_col = bounds(region, sides)
    n_rows = max_row - min_row + 1
    n_cols = max_col - min_col + 1
    # print(min_row, min_col, max_row, max_col)
    # print(n_rows, n_cols)
    grid = []
    for _ in range(n_rows):
        line = ["."] * n_cols
        grid.append(line)
    for row, col in region:
        # print(row, col)
        row -= min_row
        col -= min_col
        # print(row, col)
        grid[row][col] = "#"
    for side in sides:
        for row, col, orient in side:
            row -= min_row
            col -= min_col
            if orient == "h":
                if grid[row][col] == ".":
                    grid[row][col] = "-"
                else:
                    if grid[row][col] == "|":
                        grid[row][col] = "+"
                    elif grid[row][col] == "-":
                        grid[row][col] = "="
                    elif grid[row][col] in ["+", "=", '"']:
                        grid[row][col] = "3"
                    else:
                        n = int(grid[row][col])
                        grid[row][col] = str(n + 1)
            elif orient == "v":
                if grid[row][col] == ".":
                    grid[row][col] = "|"
                else:
                    if grid[row][col] == "|":
                        grid[row][col] = '"'
                    elif grid[row][col] == "-":
                        grid[row][col] = "+"
                    elif grid[row][col] in ["+", "=", '"']:
                        grid[row][col] = "3"
                    else:
                        n = int(grid[row][col])
                        grid[row][col] = str(n + 1)
            else:
                grid[row][col] = orient
    for line in grid:
        print("".join(line))


def bounds(region, sides):
    "Return the min/max row/col in region and sides"
    min_row, min_col = 5000, 5000
    max_row, max_col = 0, 0
    for side in sides:
        for part in side:
            row, col, _ = part
            if row < min_row:
                min_row = row
            if row > max_row:
                max_row = row
            if col < min_col:
                min_col = col
            if col > max_col:
                max_col = col
    for tile in region:
        row, col = tile
        if row < min_row:
            min_row = row
        if row > max_row:
            max_row = row
        if col < min_col:
            min_col = col
        if col > max_col:
            max_col = col
    return min_row, min_col, max_row, max_col


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
