"""A solution to an Advent of Code puzzle."""

# Data Model:
# ===========
# _lines_ is a list of "\n" terminated strings from the input file.
# bricks is a list of int 3D pairs: ((x1,y1,z1), x2,y2,z2))
# by example, and confirmed by examination of puzzle input: all of the pairs
# are 1 dimensional (i.e. only one of x, y, or z changes between start and end)
# in all cases x1 <= x2, y1 <= y2, and z1 <= z2, but the pairs are in no
# particular order


import os.path  # to get the directory name of the script (current puzzle year-day)

INPUT = "input.txt"


def part1(lines):
    """Solve part 1 of the problem."""
    bricks = parse(lines)
    bricks = sort_by_z(bricks)
    bricks = settle(bricks)
    # z values have changed, and the bricks may not be in sort order any longer
    #   We need the bricks in Z sort order for the removal process
    bricks = sort_by_z(bricks)
    n = removable_brick(bricks)
    return n


def part2(lines):
    """Solve part 2 of the problem."""
    bricks = parse(lines)
    total = len(bricks)
    return total


def parse(lines):
    """Convert the lines of text into a useful bricks model.
    Return a list of int 3D pairs: ((x1,y1,z1), x2,y2,z2))"""
    bricks = []
    for line in lines:
        line = line.strip()
        start, end = line.split("~")
        x1, y1, z1 = start.split(",")
        x2, y2, z2 = end.split(",")
        bricks.append(((int(x1), int(y1), int(z1)), (int(x2), int(y2), int(z2))))
    return bricks


def sort_by_z(bricks):
    """Return a list of bricks sorted by their z value"""
    bricks = [((z1, x1, y1), end) for ((x1, y1, z1), end) in bricks]
    bricks.sort()
    bricks = [((x1, y1, z1), end) for ((z1, x1, y1), end) in bricks]
    return bricks


def settle(bricks):
    """Shift all of the bricks in bricks to the lowest Z value possible.
    If there is no brick below it will go to Z = 1, otherwise it will
    stack on top of the brick below."""
    # min_z is the max z value of the highest brick at the (x,y) key.  If there is no
    # brick at that location it defaults to 0 (the floor). A falling brick will
    # stop when z1 = min_zs.
    min_zs = {}
    for i, brick in enumerate(bricks):
        z_min = find_new_min_z(brick, min_zs)
        # z_min is the new value for z1 (min_zs + 1)
        z1 = brick[0][2]
        if z1 < z_min:
            print("Unexpected input, brick: {brick} needs to be _raised_ to {z_min}???")
        else:
            # if z_min <= z1 Update min_zs; if z_min < z1 move brick
            # do it all in one step - brick location is the same if z_min == z1
            brick, min_zs = settle_brick(brick, z_min, min_zs)
            bricks[i] = brick
    return bricks


def find_new_min_z(brick, min_zs):
    """Find the lowest z value that this brick can have.
    The floor is at z == 0, so the default lowest Z is 1"""
    (x1, y1, _), (x2, y2, _) = brick
    z = 0
    if x1 < x2:  # y1 == y2, z1 == z2
        for x in range(x1, x2 + 1):
            if (x, y1) in min_zs and min_zs[(x, y1)] > z:
                z = min_zs[(x, y1)]
    elif y1 < y2:  #  x1 == x2, z1 == z2
        for y in range(y1, y2 + 1):
            if (x1, y) in min_zs and min_zs[(x1, y)] > z:
                z = min_zs[(x1, y)]
    else:  #  z1 < z2 and x1 == x2 and y1 == y2
        if (x1, y1) in min_zs:
            z = min_zs[(x1, y1)]
    return z + 1


def settle_brick(brick, z_min, min_zs):
    """Drop the brick so that z1 = z_min and update min_zs.
    min_zs needs updating to z2 for plan (all x,y coords) of brick
    Assume z_min <= z1 <= z2. if z_min == z1 brick stays the same,
    but min_zs is update. Also update the z2 value, and set min_zs to z2 along brick"""
    (x1, y1, z1), (x2, y2, z2) = brick
    z2 -= z1 - z_min
    z1 = z_min
    new_brick = (x1, y1, z1), (x2, y2, z2)
    if x1 < x2:  # y1 == y2
        for x in range(x1, x2 + 1):
            min_zs[(x, y1)] = z2
    elif y1 < y2:  #  x1 == x2
        for y in range(y1, y2 + 1):
            min_zs[(x1, y)] = z2
    else:  #  z1 < z2 and x1 == x2 and y1 == y2
        min_zs[(x1, y1)] = z2
    return new_brick, min_zs


def removable_brick(bricks):
    """Search through the bricks to find bricks that can be removed
    without causing a brick above to fall. Return the number of bricks"""
    n = 0
    # supports and supported by are lists of list indexes into bricks.
    # if brick i supports brick j, then j is in the list supports[i]
    # and i is in supported_by[j]
    supports, supported_by = find_dependencies(bricks)
    # print(supports, "\n", supported_by)
    for others in supports:
        # for part 1, we do not care which brick it is.
        if all_have_multiple_supports(others, supported_by):
            # print(f"Remove brick {i}")
            n += 1
    return n


def all_have_multiple_supports(bricks, supported_by):
    """Return True IFF all the bricks have 2 or more supports"""
    for brick in bricks:
        if len(supported_by[brick]) < 2:
            return False
    return True


def find_dependencies(bricks):
    """Return two lists describing the bricks in bricks by index.
    1) the bricks that the brick at index supports
    2) the bricks that are supported by the brick at index"""
    supports = []
    supported_by = []
    for _ in bricks:
        supports.append([])
        supported_by.append([])
    for i, brick in enumerate(bricks):
        # only check the other bricks with z1 that equal this bricks z2 + 1
        # bricks are sorted by z1, and z1 <= z2, so a brick with z1 = to this z2+1
        # must come later in the list.
        _, (_, _, z2) = brick
        j = i + 1
        while j < len(bricks) and bricks[j][0][2] <= z2 + 1:
            # only consider other bricks where z1 == z2 + 1
            if bricks[j][0][2] == z2 + 1 and intersects(brick, bricks[j]):
                supports[i].append(j)
                supported_by[j].append(i)
            j += 1
    return supports, supported_by


def intersects(line, other_line):
    """Return True if line intersects other_line"""
    (x1, y1, _), (x2, y2, _) = line
    (ox1, oy1, _), (ox2, oy2, _) = other_line
    return y1 <= oy2 and oy1 <= y2 and x1 <= ox2 and ox1 <= x2


def main(filename):
    """Solve both parts of the puzzle."""
    _, puzzle = os.path.split(os.path.dirname(__file__))
    with open(filename, encoding="utf8") as bricks:
        lines = bricks.readlines()
    print(f"Solving Advent of Code {puzzle} with {filename}")
    print(f"Part 1: {part1(lines)}")
    print(f"Part 2: {part2(lines)}")


if __name__ == "__main__":
    main(INPUT)
