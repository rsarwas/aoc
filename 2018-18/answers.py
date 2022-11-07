# Data Model:
# ===========
# lines is a list of "\n" terminated strings from the input file
# 

TREE = '|'
LUMBERYARD = '#'
GROUND = '.'

def part1(lines):
    map = parse(lines)
    # print("initial")
    # display(map)
    for minute in range(10):
        map = life(map)
        # print(f"After {minute+1} minute")
        # display(map)
    return score(map)

def part2(lines):
    map = parse(lines)
    minutes = 1_000_000_000
    minutes = 100
    # timing: 1000 = 10 seconds, 10,000 = 100 seconds
    #  => 1 billion = 10 million seconds (116 days)
    # that is too long!
    for minute in range(minutes):
        map = life(map)
    return score(map)

def parse(lines):
    map = []
    for line in lines:
        map.append(list(line.strip()))
    return map

def life(map):
    new_map = []
    for r in range(len(map)):
        new_row = []
        for c in range(len(map[r])):
            new_site = calc_cell(map, r, c)
            new_row.append(new_site)
        new_map.append(new_row)
    return new_map

def calc_cell(map, r, c):
    min_r, min_c = (0,0)
    max_r, max_c = (len(map), len(map[0]))
    me = map[r][c]
    # find what is adjacent to me; do not wrap around (8 or less adjacent squares)
    trees = 0
    yards = 0
    opens = 0
    for dr,dc in [(-1,-1,), (-1,0), (-1,1),  (0,-1,),(0,1),  (1,-1,), (1,0), (1,1)]:
        if r+dr < min_r or r+dr >= max_r:
            continue
        if c+dc < min_c or c+dc >= max_c:
            continue
        this = map[r+dr][c+dc]
        if this == TREE:
            trees += 1
        if this == LUMBERYARD:
            yards += 1
        if this == GROUND:
            opens += 1
    # * An open acre will become filled with trees if three or more adjacent
    #   acres contained trees. Otherwise, nothing happens.
    # * An acre filled with trees will become a lumberyard if three or more adjacent
    #   acres were lumberyards. Otherwise, nothing happens.
    # * An acre containing a lumberyard will remain a lumberyard if it was adjacent
    #   to at least one other lumberyard and at least one acre containing trees.
    #   Otherwise, it becomes open.
    new_me = ""
    if me == GROUND:
        new_me = TREE if trees >= 3 else GROUND
    if me == TREE:
        new_me = LUMBERYARD if yards >= 3 else TREE
    if me == LUMBERYARD:
        new_me = LUMBERYARD if yards >= 1 and trees >= 1 else GROUND
    return new_me

def score(map):
    yards = 0
    trees = 0
    for row in map:
        for acre in row:
            if acre == TREE:
                trees += 1
            if acre == LUMBERYARD:
                yards += 1
    return trees * yards

def display(map):
    for line in map:
        print("".join(line))

if __name__ == '__main__':
    # data = open("input.txt").read() # as one big string
    # lines = open("test.txt").readlines() # as a list of line strings
    lines = open("input.txt").readlines() # as a list of line strings
    print(f"Part 1: {part1(lines)}")
    print(f"Part 2: {part2(lines)}")
