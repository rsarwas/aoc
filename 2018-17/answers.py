"""A solution to an Advent of Code puzzle."""

# Data Model:
# ===========
# _lines_ is a list of "\n" terminated strings from the input file.
# a coordinate is an x,y tuple, y increases downward
# clay is a list of coordinates from the input where water cannot flow
# water is a list of coordinates where water has settled
# flow is a list of coordinates that water flows through
# Note, since water are flow are mutually exclusive and must be unique,
# water and flow are implemented as a dictionary called water with two values STILL and FLOWING
# pour_points is a list coordinates that water starts flowing down from
#   Initially there is only one pour point, the well. When a pour point is processed
#   i.e. flows downward until it hits a barrier (water or clay) or goes beyond the
#   lower limit, it is removed from the list and converted to a flow point.
#   (In the final tally, the well is not considered a flow point).
# flood_points is a list of coordinates that water starts to flow across from.
#   a flood point starts as a point in the flow that has hit a horizontal barrier
#   (clay or water). Once a flood point has been processed (floods horizontally),
#   it is converted to a water or flow point. It will be water if the flood is
#   constrained horizontally by clay, or a flow point if not. In which case it
#   will create a new pour point.
# pour_points and flood_points are implemented as sets to ensure duplicate
# points are not added

# flood points and pour points (except the well) are in flow

# 33245 is too high

import os.path  # to get the directory name of the script (current puzzle year-day)

INPUT = "input.txt"

FLOWING = "F"
STILL = "W"


def part1and2(lines):
    """Solve part 1 of the problem."""
    # Immutable State
    clay = parse(lines)
    envelope = bounds(clay)
    upper_limit = envelope[2]  # y_max (y increases downward)
    lower_limit = envelope[3]  # do not count water below the lowest clay
    well = (500, upper_limit - 1)  # do not count water above the highest clay
    # Mutable State
    pour_points = set([well])
    flood_points = set()
    water = {}
    while pour_points:
        # print("Pour Points", pour_points)
        pour_point = pour_points.pop()
        pour(pour_point, water, clay, lower_limit, flood_points)
        # print("Flood Points", flood_points)
        while flood_points:
            flood_point = flood_points.pop()
            flood(flood_point, water, clay, pour_points, flood_points)
    # display(water)
    # plot(envelope, clay, water)
    all = len(water)
    still = len([1 for w in water.values() if w == STILL])
    return (all, still)


def parse(lines):
    """Convert the lines of text into a useful data model."""
    data = []
    for line in lines:
        line = line.strip()
        single, range_desc = line.split(", ")
        axis, single = single.split("=")
        range_desc = range_desc.split("=")[1]
        if axis == "y":
            y = int(single)
            xs = range_desc.split("..")
            x1 = int(xs[0])
            x2 = int(xs[1])
            for x in range(x1, x2 + 1):
                data.append((x, y))
        else:
            x = int(single)
            ys = range_desc.split("..")
            y1 = int(ys[0])
            y2 = int(ys[1])
            for y in range(y1, y2 + 1):
                data.append((x, y))
    return data


def bounds(data):
    """Returns a tuple of the minimum and maximum values in the list of coordinates"""
    x_min = 10_000
    x_max = 0
    y_min = 10_000
    y_max = 0
    for x, y in data:
        if x < x_min:
            x_min = x
        if x > x_max:
            x_max = x
        if y < y_min:
            y_min = y
        if y > y_max:
            y_max = y
    return (x_min, x_max, y_min, y_max)


def pour(pour_point, water, clay, lower_limit, flood_points):
    """Process a pour point

    Add coordinates to the flow list from the pour_point downward
    until the you hit a barrier (water or clay) or go beyond the
    lower limit.

    The pour_point (except the initial well point) is already in the
    flow list.  It remains there.

    A new flood_point is created where the flow hits barrier."""

    # print("Pour from", pour_point)

    x, y = pour_point
    y += 1
    while not is_barrier((x, y), water, clay) and y <= lower_limit:
        water[(x, y)] = FLOWING
        y += 1
    if (x, y) in water or (x, y) in clay:
        flood_points.add((x, y - 1))


def flood(flood_point, water, clay, pour_points, flood_points):
    """Process a flood point

    A flood point is processed (floods horizontally), by creating flow or water points
    horizontally from the flood point until it hits a vertical barrier, or the horizontal
    barrier below ends. It will be water if the flood is constrained
    horizontally by clay in both directions, or a flow point otherwise.

    New pour points will be created at a flow point that does not have a barrier
    below it (horizontal flow stops at this point)."""

    # print("Flood from", flood_point)

    x, y = flood_point

    # search left
    left_limit = None
    has_left_barrier = False
    left = x - 1
    while is_barrier((left, y + 1), water, clay):
        if (left, y) in clay:
            has_left_barrier = True
            break
        left -= 1
    left_limit = (left, y)

    # search right
    right_limit = None
    has_right_barrier = False
    right = x + 1
    while is_barrier((right, y + 1), water, clay):
        if (right, y) in clay:
            has_right_barrier = True
            break
        right += 1
    right_limit = (right, y)

    # fill the flood zone
    left = left_limit[0] + 1
    if not has_left_barrier:
        left -= 1
    right = right_limit[0]
    if not has_right_barrier:
        right += 1
    for nx in range(left, right):
        if has_left_barrier and has_right_barrier:
            water[(nx, y)] = STILL
        else:
            water[(nx, y)] = FLOWING

    # Add flood points
    if has_left_barrier and has_right_barrier:
        # Usually water is flowing in from the cell directly above the current
        # flood point, but sometimes we have risen to a level where the water
        # is flowing in from the side, in that case we need to look for the
        # flood point above.

        test_point = (x, y - 1)  # try point above current flood point
        if is_flow(test_point, water):
            flood_points.add(test_point)
        else:
            for nx in range(left, right):
                test_point = (nx, y - 1)
                if is_flow(test_point, water):
                    flood_points.add(test_point)
                    break

    # Add pour points
    if not has_left_barrier:
        # overflows on left
        pour_points.add((left, y))
    if not has_right_barrier:
        # overflows on right
        pour_points.add((right - 1, y))


def is_barrier(point, water, clay):
    """Test if the point is a barrier (still water or clay)"""
    if point in clay:
        return True
    if point in water and water[point] == STILL:
        return True
    return False


def is_flow(point, water):
    """Test if the point is flowing water"""
    if point in water and water[point] == FLOWING:
        return True
    return False


def display(water):
    """Debug function to list the water cells in a readable manner"""
    still = [point for point in water.keys() if water[point] == STILL]
    still = [(y, x) for (x, y) in still]
    still.sort()
    print("Still Water", still)
    flow = [point for point in water.keys() if water[point] == FLOWING]
    flow = [(y, x) for (x, y) in flow]
    flow.sort()
    print("Flowing Water", flow)


def plot(bounds, clay, water):
    """Debug function to visualize the solution and check for errors"""
    (x_min, x_max, y_min, y_max) = bounds
    x_min -= 2
    x_range = x_max + 2 - x_min
    y_min = 0
    y_range = y_max - y_min
    grid = []
    for y in range(y_max + 1):
        row = ["."] * x_range
        grid.append(row)
    grid[0][500 - x_min] = "o"
    for x, y in clay:
        grid[y][x - x_min] = "#"
    for x, y in water:
        if water[(x, y)] == STILL:
            grid[y][x - x_min] = "~"
        else:
            grid[y][x - x_min] = "+"
    for row in grid:
        print("".join(row))


def main(filename):
    """Solve both parts of the puzzle."""
    _, puzzle = os.path.split(os.path.dirname(__file__))
    with open(filename, encoding="utf8") as data:
        lines = data.readlines()
    print(f"Solving Advent of Code {puzzle} with {filename}")
    part1, part2 = part1and2(lines)
    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}")


if __name__ == "__main__":
    main(INPUT)
