"""A solution to an Advent of Code puzzle."""

# Data Model:
# ===========
# _lines_ is a list of "\n" terminated strings from the input file.
# _rays_ is also a list of (px, py, pz, vx, vy, vz) tuples


import os.path  # to get the directory name of the script (current puzzle year-day)

INPUT = "input.txt"


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
    total = len(rays)
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
