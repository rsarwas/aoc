# Data Model:
# ===========
# lines is a list of "\n" terminated strings from the input file
# paths is a list of paths; path is a list of (x,y) tuples
#   each path segment is either horizontal or vertical
#   x increases to the right, and y increases down
# rock is a set of (x,y) tuples that are "covered" by the paths
# sand is a set of (x,y) tuples where a grain of sand comes to rest
# the abyss is the y value of the lowest rock (any sand reaching
# this point will not stop falling)


def part1(lines):
    paths = parse(lines)
    rock = draw_paths(paths)
    x1, x2, y1, y2 = find_extents(paths)
    abyss = y2
    sand = set()
    # display(rock, sand, x1, x2, y1, y2)
    start = (500, 1)
    add_sand(sand, rock, start, abyss)
    # display(rock, sand, x1, x2, y1, y2)
    return len(sand)


def part2(lines):
    paths = parse(lines)
    x1, x2, y1, y2 = find_extents(paths)
    y2 = y2 + 2
    abyss = y2
    x1 = min(x1, 500 - abyss)
    x2 = max(x2, 500 + abyss)
    paths.append([(x1, abyss), (x2, abyss)])
    rock = draw_paths(paths)
    sand = set()
    # display(rock, sand, x1, x2, y1, y2)
    start = (500, 0)
    add_sand(sand, rock, start, abyss)
    sand.add((start))
    # display(rock, sand, x1, x2, y1, y2)
    return len(sand)


def parse(lines):
    paths = []
    for line in lines:
        path = []
        line = line.strip()
        pairs = line.split(" -> ")
        for pair in pairs:
            x, y = pair.split(",")
            path.append((int(x), int(y)))
        item = line.split()
        paths.append(path)
    return paths


def draw_paths(paths):
    rocks = set()
    for path in paths:
        x1, y1 = path[0]
        rocks.add((x1, y1))
        for x2, y2 in path[1:]:
            rocks.add((x2, y2))
            if x1 == x2:
                dy = -1 if y2 < y1 else 1
                while y1 != y2:
                    y1 += dy
                    rocks.add((x1, y1))
            elif y1 == y2:
                dx = -1 if x2 < x1 else 1
                while x1 != x2:
                    x1 += dx
                    rocks.add((x1, y1))
            else:
                print("PANIC: diagonal lines are not supported")
            x1, y1 = x2, y2
    return rocks


def find_extents(paths):
    min_x = 1e10
    max_x = 0
    min_y = 0  # constant
    max_y = 0
    for path in paths:
        for x, y in path:
            if y > max_y:
                max_y = y
            if x > max_x:
                max_x = x
            if x < min_x:
                min_x = x
    return min_x, max_x, min_y, max_y


def add_sand(sand, rock, start, abyss):
    while True:
        end = drop_sand(start, sand, rock, abyss)
        # print(start, end)
        if end == start:
            return sand  # the grid created a bucket which is filled (nothing went into the abyss)
        if end[1] > abyss:
            return sand
        else:
            sand.add(end)  # add sand to map and keep going
    # while loop continues until function returns


def drop_sand(start, sand, rock, abyss):
    x, y = start
    deltas = [(0, 1), (-1, 1), (1, 1)]
    while True:
        # print(x,y)
        for dx, dy in deltas:
            tx, ty = x + dx, y + dy
            if ty > abyss:
                return (tx, ty)  # sand is off the map, stop dropping
            if (tx, ty) in sand or (tx, ty) in rock:
                if dx == 1 and dy == 1:
                    return (x, y)  # sand is at it's resting spot, stop dropping
                # else try other location
                continue
            else:
                # update the location of the samd, and keep dropping
                x, y = tx, ty
                break
    # while loop continues until function returns


def display(rock, sand, x1, x2, y1, y2):
    rows = []
    width = x2 - x1 + 3  # add a border at the sides
    for _ in range(y2 + 1):
        row = ["."] * width
        rows.append(row)
    rows[0][500 - x1 + 1] = "+"
    for x, y in rock:
        rows[y][x - x1 + 1] = "#"
    for x, y in sand:
        rows[y][x - x1 + 1] = "o"
    print()
    for row in rows:
        print("".join(row))


if __name__ == "__main__":
    lines = open("input.txt").readlines()
    print(f"Part 1: {part1(lines)}")
    print(f"Part 2: {part2(lines)}")
