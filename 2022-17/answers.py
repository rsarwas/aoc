# Data Model:
# ===========
# lines is a list of "\n" terminated strings from the input file

RIGHT = ">"
LEFT = "<"

# origin is bottom left (x increasexs to the right, y increases upward)
ROCK1 = [(0, 0), (1, 0), (2, 0), (3, 0)]
ROCK2 = [(1, 0), (0, 1), (1, 1), (2, 1), (1, 2)]
ROCK3 = [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)]
ROCK4 = [(0, 0), (0, 1), (0, 2), (0, 3)]
ROCK5 = [(0, 0), (1, 0), (0, 1), (1, 1)]
ROCKS = [ROCK1, ROCK2, ROCK3, ROCK4, ROCK5]

WIDTH = 7
STARTX = 2
STARTY = 4


def part1(lines):
    gusts = lines[0].strip()
    drops = 500  # use 2022 for part1, use 1000000000000 for part 2 (takes too long)
    height = solve(gusts, drops)
    return height


def part2(lines):
    return -1


def solve(gusts, max_drops):
    rock_count = len(ROCKS)
    ri = 0  # index to ROCKS
    gi = 0  # index to gusts
    height = (
        0  # height of tallest rock (will be returned after last rock finishes dropping)
    )
    rocks = (
        set()
    )  # a set of tuples (x,y) coordinates that are occupied by a fallen rock
    drops = 0
    found_set = {(0, 0)}  # Used to find a pattern to optimize part2
    while True:
        rock = ROCKS[ri]
        x, y = STARTX, height + STARTY  # origin of the rock when it starts falling
        x, y, gi = find_final_position(rock, rocks, gusts, gi, x, y)
        # x,y is the origin of the rock after it stops falling
        # gi is the new gust index; gusts are consummed as the rock falls
        for xr, yr in rock:
            chunk = (x + xr, y + yr)
            rocks.add(chunk)
            if chunk[1] > height:
                height = chunk[1]
        # display(rocks, height)
        ri += 1
        ri %= rock_count
        drops += 1

        # Looking for a pattern to optimize for part 2
        if (ri, gi) in found_set:
            print((ri, gi), "is a dup")
            print("dropped", drops)
            # display(rocks, height)
        else:
            found_set.add((ri, gi))

        if drops == max_drops:
            return height


def find_final_position(rock, rocks, gusts, gi, x, y):
    """After a rock appears, it alternates between being pushed
    by a jet of hot gas one unit (in the direction indicated
    by the next symbol in the jet pattern) and then falling one
    unit down. If any movement would cause any part of the rock
    to move into the walls, floor, or a stopped rock, the movement
    instead does not occur. If a downward movement would have
    caused a falling rock to move into the floor or an already-fallen
    rock, the falling rock stops where it is (having landed on
    something) and a new rock immediately begins falling."""
    while True:
        gust = gusts[gi]
        gi += 1
        gi %= len(gusts)
        if can_move_x(gust, x, y, rock, rocks):
            if gust == RIGHT:
                x += 1
            else:
                x -= 1
        if can_move_down(x, y, rock, rocks):
            y -= 1
        else:
            return x, y, gi


def can_move_x(gust, ox, oy, rock, rocks):
    dx = 1
    if gust == LEFT:
        dx = -1
    ox += dx
    if ox < 0:
        return False
    for rx, ry in rock:
        x, y = ox + rx, oy + ry
        if x >= WIDTH:
            return False
        if (x, y) in rocks:
            return False
    return True


def can_move_down(ox, oy, rock, rocks):
    dy = -1
    oy += dy
    if oy == 0:
        return False
    for rx, ry in rock:
        x, y = ox + rx, oy + ry
        if (x, y) in rocks:
            return False
    return True


def display(rocks, height):
    rows = []
    for _ in range(height + 1):
        row = ["."] * WIDTH
        rows.append(row)
    for x, y in rocks:
        rows[height - y][x] = "#"
    print("\nHeight", height)
    print("top 20 rows")
    for row in rows[:20]:
        print("".join(row))


if __name__ == "__main__":
    lines = open("test.txt").readlines()
    print(f"Part 1: {part1(lines)}")
    print(f"Part 2: {part2(lines)}")
