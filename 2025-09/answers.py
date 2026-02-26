"""A solution to an Advent of Code puzzle."""

# Data Model:
# ===========
# _lines_ is a list of "\n" terminated strings from the input file.


import os.path  # to get the directory name of the script (current puzzle year-day)

INPUT = "input.txt"


def part1(lines):
    """Solve part 1 of the problem."""
    data = parse(lines)
    max_area = 0
    for i, (x1, y1) in enumerate(data[:-1]):
        for x2, y2 in data[i + 1 :]:
            area = calc_area(x1, y1, x2, y2)
            if area > max_area:
                max_area = area
    return max_area


def part2(lines):
    """Solve part 2 of the problem."""
    data = parse(lines)
    # display_minmax(data)
    # grid is approx 10^5 by 10^5.
    # too large to store the state of each grid point in an array

    """
    for each coordinate pair if the 4 perimeter lines are entirely within
    the larger area, then the rectangle is a valid, and we can consider
    it's area as a possible solution.
    A line is within the area if all the points along the line are within
    (it is not enough to just consider the end points).
    a point is within if there are a odd number of perpendicular
    crossings to each of xmin, ymin, xmax, ymax
    Note: caution is needed if crosses at the endpoints of a line.
    Consider the example.  The point 7,4 is inside, and crosses two
    lines to get to ymin, but is inside because while it crosses (7,1)-(11,1)
    and (2,3)-(7,3) it crosses one at the beginning and one at the end."""
    total = len(data)
    return total


def parse(lines):
    """Convert the lines of text into a useful data model."""
    data = []
    for line in lines:
        line = line.strip()
        x, y = line.split(",")
        data.append((int(x), int(y)))
    return data


def calc_area(x1, y1, x2, y2):
    """Return the area of the rectangle"""
    dx = 1 + abs(x2 - x1)
    dy = 1 + abs(y2 - y1)
    return dx * dy


def display_minmax(data):
    xs, xb = 1e10, 0
    ys, yb = 1e10, 0
    for x, y in data:
        if x < xs:
            xs = x
        if x > xb:
            xb = x
        if y < ys:
            ys = y
        if y > yb:
            yb = y
    print(f"({xs},{ys}) to ({xb},{yb})")
    dx = xb - xs + 1
    dy = yb - ys + 1
    size = dx * dy
    print(f"{dx}x{dy} = {size}")


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
