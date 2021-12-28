# Data Model:
# ===========
# lines is a list of "\n" terminated strings from the input file
# 

EW = ">" # East facing 
NS = "v" # south facing
EMPTY = "."

def part1(lines):
    map = parse(lines)
    # print(f"\nInitial state:")
    # for r in map:
    #     print("".join(r))
    moves = find_stasis(map)
    return moves

def part2(lines):
    return -1

def parse(lines):
    return [list(line.strip()) for line in lines]

def find_stasis(map):
    height = len(map)
    width = len(map[0])
    step = 1
    while True:
        moved = False
        # Move east facing
        moves = set()  # squares that became occupied on this step (do not move again)
        occupied = set() # squares that were occupied on the start of this step (do no occupy)
        for r in range(height):
            for c in range(width):
                if map[r][c] == EW:
                    if (r,c) in moves:
                        # this location was just occupied by a moving cucumber do not move it again
                        continue
                    c1 = (c + 1) % width
                    if map[r][c1] == EMPTY and (r,c1) not in occupied:
                        # print(r,c,c1, map[r][c], map[r][c1])
                        map[r][c1] = EW
                        map[r][c] = EMPTY
                        moved = True
                        occupied.add((r,c))
                        moves.add((r,c1))
        # Move south facing
        moves = set()
        occupied = set()
        for r in range(height):
            for c in range(width):
                if map[r][c] == NS:
                    if (r,c) in moves:
                        continue
                    r1 = (r + 1) % height
                    if map[r1][c] == EMPTY and (r1,c) not in occupied:
                        # print(r,c,c1, map[r][c], map[r][c1])
                        map[r1][c] = NS
                        map[r][c] = EMPTY
                        moved = True
                        occupied.add((r,c))
                        moves.add((r1,c))
        if not moved:
            break
        # if step < 5:
        #     print(f"\nAfter {step} steps:")
        #     for r in map:
        #         print("".join(r))
        step += 1
    return step

if __name__ == '__main__':
    # lines = open("test.txt").readlines() # as a list of line strings
    lines = open("input.txt").readlines() # as a list of line strings
    print(f"Part 1: {part1(lines)}")
    print(f"Part 2: {part2(lines)}")
