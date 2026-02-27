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
    """Solve part 2 of the problem.

    New Strategy.  If any boundary point is entirely inside a potential rectangle,
    Then it is invalid, otherwise it is valid.  Proof: by definition the one side
    of the boundary is inside, and one side is outside.  Therefore if a boundary
    point is inside the rectangle some of the outside must come with it.  Since we
    need a rectangle with no outside bits, we need a rectangle with no boundary points.

    This solution correctly eliminates many (most) invalid rectangles, it is still possible
    to have an invalid rectangle with no boundary points (just edges) within it."""

    data = parse(lines)
    sorted_data = data.copy()
    sorted_data.sort()
    max_area = 0
    for i, (x1, y1) in enumerate(sorted_data[:-1]):
        for x2, y2 in sorted_data[i + 1 :]:
            # eliminate the easy ones 118335 of 122760
            if within1(x1, y1, x2, y2, sorted_data):
                # do the hard check:
                if within2(x1, y1, x2, y2, data):
                    area = calc_area(x1, y1, x2, y2)
                    # print("rect", x1, y1, x2, y2, "area", area)
                    if area > max_area:
                        max_area = area
    return max_area


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


def within1(x1, y1, x2, y2, boundary_pts):
    """Return True if the rectangle is entirely within the boundary.
    boundary_pts is a sorted (xmin to xmax) list of perimeter points.
    x2 is always greater than or equal to x1
    Points on the edge or the rectangle are NOT within the rectangle"""
    for x, y in boundary_pts:
        if x >= x2:
            break
        if x <= x1:
            continue
        if (y < y2 and y > y1) or (y < y1 and y > y2):
            # print(x, y, "within", x1, y1, x2, y2)
            return False
    return True


def within2(x1, y1, x2, y2, boundary_pts):
    """Return True if the rectangle is entirely within the boundary.
    boundary_pts is an ordered list of perimeter points.
    If an edge of boundary bisects the rectangle, then it is NOT within"""
    for i, (p1x, p1y) in enumerate(boundary_pts[:-1]):
        p2x, p2y = boundary_pts[i + 1]
        # print("line", p1x, p1y, p2x, p2y, "rect", x1, y1, x2, y2)
        if bisects(p1x, p1y, p2x, p2y, x1, y1, x2, y2):
            # print("bisects")
            return False
    # check the closure line:
    p1x, p1y = boundary_pts[-1]
    p2x, p2y = boundary_pts[0]
    # print("closure line", p1x, p1y, p2x, p2y, "rect", x1, y1, x2, y2)
    if bisects(p1x, p1y, p2x, p2y, x1, y1, x2, y2):
        # print("bisects")
        return False
    return True


def bisects(p1x, p1y, p2x, p2y, x1, y1, x2, y2):
    """Return True if the line p1-p2 bisects the rectangle x1-y2
    precondition: x1 <= x2, but y1 and y2 are not necessarily so."""
    if p1x == p2x:
        # check vertical
        if p1x > x1 and p1x < x2:
            # order the y values
            if y2 < y1:
                y1, y2 = y2, y1
            if p2y < p1y:
                p1y, p2y = p2y, p1y
            # check for bisections
            if p1y <= y1 and p2y >= y2:
                return True
    else:
        # p1y == p2y, so check horizontal
        if y2 < y1:
            y1, y2 = y2, y1
        if p1y > y1 and p1y < y2:
            if p2x < p1x:
                p1x, p2x = p2x, p1x
            # check for bisections
            if p1x <= x1 and p2x >= x2:
                return True
    return False


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
