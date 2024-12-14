"""A solution to an Advent of Code puzzle."""

# Data Model:
# ===========
# _lines_ is a list of "\n" terminated strings from the input file.


import os.path  # to get the directory name of the script (current puzzle year-day)

INPUT = "input.txt"


def part1(lines):
    """Solve part 1 of the problem."""
    robots = parse(lines)
    for _ in range(100):
        update(robots, size())
    nw, ne, sw, se = quadrify(robots, size())
    total = nw * ne * sw * se
    return total


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
        location, velocity = line.split(" ")
        x, y = [int(x) for x in location.replace("p=", "").split(",")]
        vx, vy = [int(x) for x in velocity.replace("v=", "").split(",")]
        data.append((x, y, vx, vy))
    return data


def size():
    """Return the size of the bathroom (grid)"""
    if INPUT == "input.txt":
        return 101, 103
    return 11, 7


def update(robots, size):
    """Update the location of each robot"""
    max_x, max_y = size
    for index, robot in enumerate(robots):
        x, y, vx, vy = robot
        x += vx
        y += vy
        x %= max_x
        y %= max_y
        robots[index] = (x, y, vx, vy)


def quadrify(robots, size):
    """Count the number of robots in each quadrant"""
    nw, ne, sw, se = 0, 0, 0, 0
    max_x, max_y = size
    mid_x, mid_y = max_x // 2, max_y // 2
    for robot in robots:
        x, y, _, _ = robot
        if x < mid_x:
            if y < mid_y:
                sw += 1
            if y > mid_y:
                nw += 1
        if x > mid_x:
            if y < mid_y:
                se += 1
            if y > mid_y:
                ne += 1
    return nw, ne, sw, se


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
