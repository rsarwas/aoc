"""A solution to an Advent of Code puzzle."""

# Data Model:
# ===========
# _lines_ is a list of "\n" terminated strings from the input file.


import os.path  # to get the directory name of the script (current puzzle year-day)
import time

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
    robots = parse(lines)
    min_n = 0
    n = 0
    while True:
        update(robots, size())
        n += 1
        if n == 7892:
            display(robots, size())
            break
        # After failing to find any thing with symmetry, I displayed every frame.
        # I found a vertical cluster at n = 14, 115, 216 (or n % 101 == 14)
        # and a horizontal cluster at n = 64, 167, 270 (or n % 103 == 64)
        # so I limited my review to just those, and found it visually

        # if n % 101 == 14 or n % 103 == 64:
        #     print(n)
        #     display(robots, size())
        #     time.sleep(0.07)
        #
        #
        #
        # if n % 10000 == 0:
        #     print(n)
        # if is_symmetrical3(robots, size()) and min_n < n:
        #     print(n)
        #     display(robots, size())
        # break
        # nw, ne, sw, se = quadrify(robots, size())
        # if nw == ne and sw == se:
        #     print(n)
        #     display(robots, size())
    # display(robots, size())
    return n


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


def is_symmetrical(robots, size):
    """Return True if the locations of the robots are symmetrical about the vertical midline"""
    max_x, _ = size
    mid_x = max_x // 2
    max_x -= 1
    locations = {}
    for x, y, _, _ in robots:
        if y not in locations:
            locations[y] = []
        if x < mid_x:
            locations[y].append(x)
        else:
            x = max_x - x
            locations[y].append(x)
    errors = 0
    for y in locations:
        # if len(locations[y]) == 1:
        #     if locations[y][0] != mid_x:
        #         return False
        if len(locations[y]) == 2:
            if locations[y][0] != locations[y][1]:
                # return False
                errors += 1
                if errors > 5:
                    return False
    return True


def is_symmetrical2(robots, size):
    """Return True if the locations of the robots are symmetrical about the vertical midline"""
    max_x, _ = size
    mid_x = max_x // 2
    max_x -= 1
    locations = {}
    for x, y, _, _ in robots:
        if x not in locations:
            locations[x] = []
        locations[x].append(y)
    for x in locations:
        if x < mid_x:
            other_x = max_x - 1 - x
            if other_x not in locations:
                return False
            if len(locations[x]) != len(locations[other_x]):
                return False
    return True


def is_symmetrical3(robots, size):
    """Return True if the locations of the robots are symmetrical about the vertical midline"""
    max_x, _ = size
    mid_x = max_x // 2
    max_x -= 1
    locations = set([(x, y) for x, y, _, _ in robots])
    # print(locations)
    errors = 0
    for x, y in locations:
        if x < mid_x:
            other_x = max_x - x
            # print(x, other_x, y)
            if (other_x, y) not in locations:
                errors += 1
                if errors > 10:
                    return False
    return True


def display(robots, size):
    """Draw the locations of the robots, to see if it looks like a Christmas Tree"""
    max_x, max_y = size
    grid = []
    for _ in range(max_y):
        line = ["."] * max_x
        grid.append(line)
    for x, y, _, _ in robots:
        grid[y][x] = "#"
    for row in grid:
        print("".join(row))


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
