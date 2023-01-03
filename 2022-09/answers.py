# Data Model:
# ===========
# lines is a list of "\n" terminated strings from the input file

# Note: I would have solved part 1 much faster, but in my parser, I assumed that
# the distance was only a single digit, which is true for the test data, but not
# the full puzzle.  therefore my test passed, and when I printed each step as in
# the example, I concluded my code was correct, which led to a lot of head scratching
#
# part 2 would also have been faster, but I forgot to account for the case where
# dx and dy are both +/-2 (which I did not consider originally, because it is not
# possible in part 1)


def part1(lines):
    moves = parse(lines)
    head, tail = (0, 0), (0, 0)
    tail_positions = {tail}
    for move in moves:
        head, tail = update_position(head, tail, move, tail_positions)
        # print(head, tail)
    # display(tail_positions,6)
    return len(tail_positions)


def part2(lines):
    moves = parse(lines)
    knots = [(0, 0)] * 10  # knot[0] is the head, knot[9] is the tail
    tail_positions = {knots[0]}
    for move in moves:
        update_knots(knots, move, tail_positions)
        # print(knots)
    return len(tail_positions)


def parse(lines):
    data = []
    for line in lines:
        line = line.strip()
        dir, dist = line.split()
        data.append((dir, dist))
    return data


def update_position(head, tail, move, tail_positions):
    dir, dist = move
    # print()
    # print ("==", move, "==")
    if dir == "U":
        for i in range(int(dist)):
            head = (head[0], head[1] + 1)
            tail = update_tail(tail, head)
            tail_positions.add(tail)
            # display_th(head, tail, 6)
    elif dir == "D":
        for i in range(int(dist)):
            head = (head[0], head[1] - 1)
            tail = update_tail(tail, head)
            tail_positions.add(tail)
            # display_th(head, tail, 6)
    elif dir == "R":
        for i in range(int(dist)):
            head = (head[0] + 1, head[1])
            tail = update_tail(tail, head)
            tail_positions.add(tail)
            # display_th(head, tail, 6)
    elif dir == "L":
        for i in range(int(dist)):
            head = (head[0] - 1, head[1])
            tail = update_tail(tail, head)
            tail_positions.add(tail)
            # display_th(head, tail, 6)
    else:
        print("PANIC, unexpected direction")
    return head, tail


def update_knots(knots, move, tail_positions):
    dir, dist = move
    # print()
    # print ("==", move, "==")
    if dir == "U":
        for i in range(int(dist)):
            knots[0] = (knots[0][0], knots[0][1] + 1)
            for k in range(1, len(knots)):
                knots[k] = update_tail(knots[k], knots[k - 1])
            tail_positions.add(knots[9])
            # display_th(head, tail, 6)
    elif dir == "D":
        for _ in range(int(dist)):
            knots[0] = (knots[0][0], knots[0][1] - 1)
            for k in range(1, len(knots)):
                knots[k] = update_tail(knots[k], knots[k - 1])
            tail_positions.add(knots[9])
            # display_th(head, tail, 6)
    elif dir == "R":
        for _ in range(int(dist)):
            knots[0] = (knots[0][0] + 1, knots[0][1])
            for k in range(1, len(knots)):
                knots[k] = update_tail(knots[k], knots[k - 1])
            tail_positions.add(knots[9])
            # display_th(head, tail, 6)
    elif dir == "L":
        for _ in range(int(dist)):
            knots[0] = (knots[0][0] - 1, knots[0][1])
            for k in range(1, len(knots)):
                knots[k] = update_tail(knots[k], knots[k - 1])
            tail_positions.add(knots[9])
            # display_th(head, tail, 6)
    else:
        print("PANIC, unexpected direction")


def update_tail(tail, head):
    dx = head[0] - tail[0]
    dy = head[1] - tail[1]
    # abs(dy) and abs(dx) cannot be greater than 2, since we upodate for every increment of head
    # if abs(dy) and abs(dx) <= 1, then we do not need to move
    if dx == -2:
        if dy == -2 or dy == -1:
            tail = (tail[0] - 1, tail[1] - 1)
        if dy == 0:
            tail = (tail[0] - 1, tail[1])
        if dy == 1 or dy == 2:
            tail = (tail[0] - 1, tail[1] + 1)
    if dx == -1:
        if dy == -2:
            tail = (tail[0] - 1, tail[1] - 1)
        if dy == 2:
            tail = (tail[0] - 1, tail[1] + 1)
    if dx == 0:
        if dy == -2:
            tail = (tail[0], tail[1] - 1)
        if dy == 2:
            tail = (tail[0], tail[1] + 1)
    if dx == 1:
        if dy == -2:
            tail = (tail[0] + 1, tail[1] - 1)
        if dy == 2:
            tail = (tail[0] + 1, tail[1] + 1)
    if dx == 2:
        if dy == -2 or dy == -1:
            tail = (tail[0] + 1, tail[1] - 1)
        if dy == 0:
            tail = (tail[0] + 1, tail[1])
        if dy == 1 or dy == 2:
            tail = (tail[0] + 1, tail[1] + 1)
    return tail


def display_th(head, tail, size):
    print()
    grid = []
    for i in range(size - 1):
        row = ["."] * size
        grid.append(row)
    x, y = tail
    grid[size - 2 - y][x] = "T"
    x, y = head
    grid[size - 2 - y][x] = "H"
    for row in grid:
        print("".join(row))


def display(positions, size):
    print()
    grid = []
    for i in range(size):
        row = ["."] * size
        grid.append(row)
    for x, y in positions:
        grid[size - 1 - y][x] = "#"
    for row in grid:
        print("".join(row))


if __name__ == "__main__":
    lines = open("input.txt").readlines()
    print(f"Part 1: {part1(lines)}")
    print(f"Part 2: {part2(lines)}")
