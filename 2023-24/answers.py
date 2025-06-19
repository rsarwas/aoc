"""A solution to an Advent of Code puzzle."""

# Data Model:
# ===========
# _lines_ is a list of "\n" terminated strings from the input file.
# _rays_ is also a list of (px, py, pz, vx, vy, vz) tuples


import os.path  # to get the directory name of the script (current puzzle year-day)

INPUT = "test.txt"


def part1(lines):
    """Solve part 1 of the problem."""
    rays = parse(lines)
    total = 0
    if INPUT == "test.txt":
        bounds = (7, 27)
    else:
        bounds = (200000000000000, 400000000000000)
    for i, ray1 in enumerate(rays[:-1]):
        for ray2 in rays[i + 1 :]:
            if rays_intersect_xy(ray1, ray2, bounds, bounds):
                # print("   YES")
                total += 1
    return total


def part2(lines):
    """Solve part 2 of the problem."""
    rays = parse(lines)
    total = min_x_overlap(rays)
    return total


def parse(lines):
    """Convert the lines of text into a useful data model."""
    rays = []
    for line in lines:
        line = line.strip()
        position, velocity = line.split(" @ ")
        px, py, pz = position.split(", ")
        vx, vy, vz = velocity.split(", ")
        rays.append((int(px), int(py), int(pz), int(vx), int(vy), int(vz)))
    return rays


def rays_intersect_xy(ray1, ray2, x_bounds, y_bounds):
    """Return true IFF ray1 and ray2 intersect within the x and y bounds.
    Ignore the z values, and assume these are 2D rays."""
    x, y = lines_intersect_xy(ray1, ray2)
    # print(ray1, ray2)
    # print("   ", x, y)
    if x is None:
        return False
    if not on_ray(x, y, ray1):
        return False
    if not on_ray(x, y, ray2):
        return False
    # print("   on rays")
    x_min, x_max = x_bounds
    y_min, y_max = y_bounds
    return x_min <= x <= x_max and y_min <= y <= y_max


def lines_intersect_xy(ray1, ray2):
    """Return the x,y location of the intersection of the lines the rays are on
    y = m1x + b1 = m2x + b2 = y =>  x = (b2 - b1) / (m1 - m2)"""
    m1, b1 = slope_intercept_xy(ray1)
    m2, b2 = slope_intercept_xy(ray2)
    if m1 == m2:
        return None, None
    x = (b2 - b1) / (m1 - m2)
    y = m1 * x + b1
    return x, y


def slope_intercept_xy(ray):
    """Return the slope and intercept (y = mx + b) of the line the ray is on"""
    px, py, _, vx, vy, _ = ray
    m = vy / vx  # rise over run
    b = py - m * px  # b = y - mx
    return m, b


def on_ray(x, y, ray):
    """Return true if x,y is on the ray."""
    px, py, _, vx, vy, _ = ray
    if vx < 0 and x > px:
        return False
    if vx > 0 and x < px:
        return False
    if vy < 0 and y > py:
        return False
    if vy > 0 and y < py:
        return False
    return True


import sys


def min_x_overlap(rays):
    overlaps = [sys.maxsize, sys.maxsize, sys.maxsize]
    save_rays = [None, None, None]
    for ray1, ray2 in all_pairs(rays):
        p1x, p1y, p1z, v1x, v1y, v1z = ray1
        p2x, p2y, p2z, v2x, v2y, v2z = ray2
        x = overlap(p1x, p2x, v1x, v2x)
        if x < overlaps[0]:
            if x < 1:
                print("X", p1x, v1x, p2x, v2x, x)
            overlaps[0] = x
            save_rays[0] = (ray1, ray2)
        y = overlap(p1y, p2y, v1y, v2y)
        if y < overlaps[1]:
            if y < 1:
                print("Y", p1y, v1y, p2y, v2y, y)
            overlaps[1] = y
            save_rays[1] = (ray1, ray2)
        z = overlap(p1z, p2z, v1z, v2z)
        if z < overlaps[2]:
            if z < 1:
                print("Z", p1z, v1z, p2z, v2z, z)
            overlaps[2] = z
            save_rays[2] = (ray1, ray2)
    return overlaps, save_rays


def overlap(p1, p2, v1, v2):
    if (v1 < 0 and v2 < 0) or (v1 > 0 and v2 > 0):
        return sys.maxsize
    if v1 < v2:
        return p1 - p2
    return p2 - p1


def all_pairs(l):
    """Generate all the unique pair of list l"""
    for i, a in enumerate(l[:-1]):
        for b in l[i + 1 :]:
            yield (a, b)


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
