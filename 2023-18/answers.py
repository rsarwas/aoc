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
    vertices = perimeter_vertices(dig_plan)
    base_area = shoelace(vertices)
    # base area is to the center of the perimeter tiles
    area = base_area + perimeter_area(dig_plan)
    return area


def part2(lines):
    """Solve part 2 of the problem."""
    dig_plan = parse2(lines)
    vertices = perimeter_vertices(dig_plan)
    base_area = shoelace(vertices)
    # base area is to the center of the perimeter tiles
    area = base_area + perimeter_area(dig_plan)
    return area


def parse(lines):
    """Convert the lines of text into a useful data model."""
    data = []
    for line in lines:
        line = line.strip()
        direction, distance, color = line.split(" ")
        data.append((direction, int(distance), color))
    return data


def parse2(lines):
    """Convert the lines of text into a useful data model.
    Part 2 has a different definition of the input."""
    data = []
    for line in lines:
        line = line.strip()
        _, _, useful = line.split(" ")
        useful = useful[1:-1]  # remove parenthesis
        direction = convert_direction_codes(useful[-1])
        distance = int(useful[1:-1], 16)
        data.append((direction, distance, "x"))
    return data


def convert_direction_codes(char):
    """Convert direction codes from 0,1,2,3 to R,D,L,U."""
    if char == "0":
        return RIGHT
    if char == "1":
        return DOWN
    if char == "2":
        return LEFT
    # char == "3"
    return UP


def perimeter_vertices(dig_plan):
    """Return a list of coordinates (vertices) of the polygon described by the dig plan
    Per inspection and testing, this is a simple irregular rectilinear concave polygon.
    The list includes the starting vertex at the beginning and end. (closed polygon)"""
    current = (0, 0)  # Arbitrary starting point
    vertices = [current]
    for direction, distance, _ in dig_plan:
        current = move(current, direction, distance)
        vertices.append(current)
    return vertices


def move(location, direction, distance):
    """Return the new location after moving distance spaces in the direction given.
    There is no boundary that will limit the movement"""
    row, col = location
    if direction == RIGHT:
        col += distance
    elif direction == LEFT:
        col -= distance
    elif direction == UP:
        row -= distance
    else:  # DOWN
        row += distance
    return (row, col)


def shoelace(vertices):
    """Return the area of a polygon, given it's ordered vertices.
    This implementation of the [Shoelace Formula](https://en.wikipedia.org/wiki/Shoelace_formula)
    assumes counter-clockwise, with the start vertex repeated at the end of the list."""
    area = 0
    for i, vertex in enumerate(vertices[:-1]):
        # order of vertices (CW v. CCW) and row/col vs y/x and inverted y/row value
        # can cause a negative area if used incorrectly. It this case it is fine.
        y1, x1 = vertex
        y2, x2 = vertices[i + 1]
        area += x1 * y2 - x2 * y1
    return area / 2


def perimeter_area(dig_plan):
    """Calculate the area lost around the perimeter of the polygon."""
    perimeter = 0
    for _, distance, _ in dig_plan:
        perimeter += distance
    # Not sure why this works, but it does
    return (perimeter + 2) / 2


def main(filename):
    """Solve both parts of the puzzle."""
    _, puzzle = os.path.split(os.path.dirname(__file__))
    with open(filename, encoding="utf8") as data:
        lines = data.readlines()
    print(f"Solving Advent of Code {puzzle} with {filename}")
    print(f"Part 1: {part1(lines)}")
    print(f"Part 2: {part2(lines)}")


if __name__ == "__main__":
    # vertex = [
    #     (0, 0),
    #     (0, 7),
    #     (6, 7),
    #     (6, 5),
    #     (7, 5),
    #     (7, 7),
    #     (10, 7),
    #     (10, 1),
    #     (8, 1),
    #     (8, 0),
    #     (5, 0),
    #     (5, 2),
    #     (3, 2),
    #     (3, 0),
    #     (0, 0),
    # ]
    # print(shoelace(vertex))
    main(INPUT)
