# Data Model:
# ===========
# lines is a list of "\n" terminated strings from the input file


def part1(lines):
    data = parse(lines)
    # print("Initial configuration")
    # display(data)
    for round in range(10):
        data, _ = update(data, round)
        # print("\nRound",round + 1)
        # display(data)
    result = empty(data)
    return result


def part2(lines):
    data = parse(lines)
    round = 0
    while True:
        data, no_moves = update(data, round)
        if no_moves:
            # display(data)
            break
        round += 1
    return round + 1  # my rounds start with 0, the puzzle starts with 1


def parse(lines):
    data = []
    for row, line in enumerate(lines):
        line = line.strip()
        for col, char in enumerate(line):
            if char == "#":
                data.append((row, col))
    return data


def find_extents(data):
    min_row = 1e10
    max_row = -1e10
    min_col = 1e10
    max_col = -1e10
    for row, col in data:
        if row < min_row:
            min_row = row
        if col < min_col:
            min_col = col
        if row > max_row:
            max_row = row
        if col > max_col:
            max_col = col
    return (min_row, min_col, max_row, max_col)


def empty(data):
    min_row, min_col, max_row, max_col = find_extents(data)
    area = (1 + max_row - min_row) * (1 + max_col - min_col)
    occupied = len(data)
    return area - occupied


def display(data):
    min_row, min_col, max_row, max_col = find_extents(data)
    n_rows = 1 + max_row - min_row
    n_cols = 1 + max_col - min_col
    grid = []
    for _ in range(n_rows):
        row = ["."] * n_cols
        grid.append(row)
    for (row, col) in data:
        grid[row - min_row][col - min_col] = "#"
    print("\nScore =", n_rows * n_cols - len(data))
    for row in grid:
        print("".join(row))


MOVES = [
    [(-1, -1), (-1, 0), (-1, 1)],  # NE, N, NW
    [(1, -1), (1, 0), (1, 1)],  # SE, S, SW
    [(-1, -1), (0, -1), (1, -1)],  # NW, W, SW
    [(-1, 1), (0, 1), (1, 1)],  # NE, E, SE
]
ADJACENT = [
    (-1, -1),
    (-1, 0),
    (-1, 1),
    (1, -1),
    (1, 0),
    (1, 1),
    (0, -1),
    (0, 1),
]  # NE, N, NW, SE, S, SW, W, E


def update(data, round):
    new_locs = []
    for loc in data:
        (r, c) = loc
        new_loc = None
        # check no move option (all adjencent squares are empty)
        clear = True
        for dr, dc in ADJACENT:
            if (r + dr, c + dc) in data:
                clear = False
                break
        if not clear:
            for i in range(round, round + 4):
                free = True
                moves = MOVES[i % len(MOVES)]
                for dr, dc in moves:
                    if (r + dr, c + dc) in data:
                        free = False
                        break
                if free:
                    new_loc = (r + moves[1][0], c + moves[1][1])
                    break
        new_locs.append(new_loc)

    no_moves = True
    for loc in new_locs:
        if loc:
            no_moves = False
            break

    if no_moves:
        return data, True

    conflicts = set()
    for loc in new_locs:
        if loc:
            c = new_locs.count(loc)
            if c > 1:
                conflicts.add(loc)

    new_data = []
    # moves = 0
    for i, new_loc in enumerate(new_locs):
        if new_loc and new_loc not in conflicts:
            new_data.append(new_loc)
            # moves += 1
        else:
            new_data.append(data[i])

    # print("round", round+1, "elves", len(data), "moves", moves, "conflicts", len(conflicts))
    return new_data, False


if __name__ == "__main__":
    lines = open("input.txt").readlines()
    print(f"Part 1: {part1(lines)}")
    print(f"Part 2: {part2(lines)}")
