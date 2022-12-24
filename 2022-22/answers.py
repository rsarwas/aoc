# Data Model:
# ===========
# lines is a list of "\n" terminated strings from the input file
# instructions is a list of (int, char) tuples, where char is a turn 
# direction in {"L", "R"}, where "R" is clockwise
# row/col_min/max is are lists, the index is the row or col number (col are numbered
# from top to bottom), and the value is the number of the min or max col or row in
# that row or col respectively.  This is used for dete4cting and resolving wrap around

# movement directions are given by a tuple of row,col deltas
# i.e right is (0, 1) meaning row number stay the same, and col index advances by 1
UP = (-1,0)
DOWN = (1,0)
LEFT = (0,-1)
RIGHT = (0,1)

VOID = " "
OPEN = "."
WALL = "#"

FACE_SIZE = 50
R0 = 0
R1 = 1 * FACE_SIZE
R2 = 2 * FACE_SIZE
R3 = 3 * FACE_SIZE
R4 = 4 * FACE_SIZE
C0 = 0
C1 = 1 * FACE_SIZE
C2 = 2 * FACE_SIZE
C3 = 3 * FACE_SIZE

# Used to change some internals deep in the code for part 2 
PART = 1

def part1(lines):
    grid, instructions = parse(lines)
    # print(grid)
    # print(instructions)
    end, dir = process(grid, instructions)
    result = password(end, dir)
    return result


def part2(lines):
    global PART
    PART = 2
    return part1(lines)
    # first (wrong) run returned 145330, which is too low
    # another wrong attempt returned 184163 which is too high


def parse(lines):
    grid = []
    instructions = []
    for line in lines:
        if line == "\n":
            continue
        if line[0] in [VOID, OPEN, WALL]:
            grid.append(line.replace("\n",""))
        else:
            line = line.strip()
            start = 0
            end = 1
            while end < len(line):
                if line[end] in "LR":
                    dist = int(line[start:end])
                    instructions.append((dist,line[end]))
                    start = end+1
                    end = start+1
                else:
                    end += 1
            dist = int(line[start:])
            instructions.append((dist,None))
    return grid, instructions


def process(grid, instructions):
    loc = find_start(grid)
    dir = RIGHT
    for instruction in instructions:
        loc, dir = move(grid, loc, dir, instruction)
    return loc, dir


def find_start(grid):
    row = 0
    for col,char in enumerate(grid[row]):
        if char == OPEN:
            return (row,col)


def move(grid, loc, dir, instruction):
    dist, turn = instruction
    # print(loc, dir, dist, turn)
    loc, dir = march(grid, loc, dir, dist)
    dir = change_direction(dir, turn)
    # print("  =>", loc, dir)
    return loc, dir


def march(grid, loc, dir, dist):
    if dist == 0:
        return loc, dir
    loc, dir, wall = next_space(grid, loc, dir)
    step = 1
    while step < dist and not wall:
        loc, dir, wall = next_space(grid, loc, dir)
        step += 1
    return loc, dir


def next_space(grid, loc, dir):
    """ finds the next valid space to move to
    handles grid edge conditions wrap around
    and empty cells"""

    # In part2 of the puzzle we use a different method to find the next location (and direction) 
    if PART == 2:
        return next_space2(grid, loc, dir)
    
    row, col = loc
    dr, dc = dir
    # print(row,col,dr,dc)
    nrow, ncol = row + dr, col + dc
    safety = 0
    while True and safety < 200:
        safety += 1
        # print(nrow, ncol)
        if inside(grid, nrow, ncol):
            char = grid[nrow][ncol]
            # print(char)
            if char == WALL:
                return ((row, col), dir, True)
            if char == OPEN:
                return ((nrow, ncol), dir, False)
            # char must be VOID, advance until we wrap or hit a non-VOID space
            nrow, ncol = nrow + dr, ncol + dc
        else:
            # need to wrap around; Usually it can only hit one edge at a time
            # but some rows are shorter than others, so when going up or down,
            # we may find ourselves in a valid row, but beyond it's length
            if dr == 1 and nrow >= len(grid):
                nrow = 0
            if dc == 1 and ncol >= len(grid[nrow]):
                ncol = 0
            if dr == -1 and nrow < 0:
                nrow = len(grid) - 1
            if dc == -1 and ncol < 0:
                ncol = len(grid[nrow]) - 1
            if dr != 0 and ncol >= len(grid[nrow]):
                nrow = nrow + dr


def next_space2(grid, loc, dir):
    row, col = loc
    dr, dc = dir
    nrow, ncol = row + dr, col + dc
    ndir = dir

    in_face = face(row, col)
    new_face = face(nrow, ncol)

    if  new_face == None:
        print("PANIC: I ended up off the cube")
        return -1

    if isinstance(new_face, int):
        # the new face is on the map
        pass
    else:
        # we have walked off the map, and need to
        # recalibrate for the new face:
        if new_face ==  (1,6):
            nrow = col - R1 + C3
            ncol = 0
            ndir = RIGHT # up to right
            if face(nrow, ncol) != 6: print("PANIC 1,6", in_face, face(nrow, ncol))
        elif new_face == (2,6):
            nrow = R4 - 1
            ncol = col - C2
            ndir = UP # up to up
            if face(nrow, ncol) != 6: print("PANIC 2,6", in_face, face(nrow, ncol))
        elif new_face == (1,4):
            nrow = R3 - 1 - row
            ncol = 0
            ndir = RIGHT  # left to right
            if face(nrow, ncol) != 4: print("PANIC 1,4", in_face, face(nrow, ncol))
        elif new_face == (2,5):
            nrow = R3 - 1 - row
            ncol = C2 - 1
            ndir = LEFT # right to left
            if face(nrow, ncol) != 5: print("PANIC 2,5", in_face, face(nrow, ncol))
        elif new_face == (3,4) and in_face == 3:
            nrow = R2
            ncol = row - R1
            ndir = DOWN # left to down
            if face(nrow, ncol) != 4: print("PANIC 3->4", in_face, face(nrow, ncol))
        elif new_face == (3,4) and in_face == 4:
            nrow = col + R1
            ncol = C1
            ndir = RIGHT # up to right
            if face(nrow, ncol) != 3: print("PANIC 4->3", in_face, face(nrow, ncol))
        elif new_face == (2,3) and in_face == 2:
            nrow = R1 + col - C2
            ncol = C2 - 1
            ndir = LEFT # down to left
            if face(nrow, ncol) != 3: print("PANIC 2->3", in_face, face(nrow, ncol))
        elif new_face == (2,3) and in_face == 3:
            nrow = R1 - 1
            ncol = row - R1 + C2
            ndir = UP  # right to up
            if face(nrow, ncol) != 2: print("PANIC 3->2", in_face, face(nrow, ncol))
        elif new_face == (4,1):
            nrow = (R3 - 1) - row  # 149 -> 0; 100 -> 49
            ncol = C1
            ndir = RIGHT # left to right
            if face(nrow, ncol) != 1: print("PANIC 4,1", in_face, face(nrow, ncol))
        elif new_face == (5,2):
            nrow = R3 - row
            ncol = C3 - 1
            ndir = LEFT # right to left
            if face(nrow, ncol) != 2: print("PANIC 5,2", in_face, face(nrow, ncol))
        elif new_face == (6,1):
            nrow = 0
            ncol = row - R3 + C1
            ndir = DOWN  # left to down
            if face(nrow, ncol) != 1: print("PANIC 6,1", in_face, face(nrow, ncol))
        elif new_face == (5,6) and in_face == 5:
            nrow = col - C1 + R3
            ncol = C1 - 1
            ndir = LEFT # down to left
            if face(nrow, ncol) != 6: print("PANIC 5->6", in_face, face(nrow, ncol))
        elif new_face == (5,6) and in_face == 6:
            nrow = R3 - 1
            ncol = row - R3 + C1
            ndir = UP # right to up
            if face(nrow, ncol) != 5: print("PANIC 6->5", in_face, face(nrow, ncol))
        elif new_face == (6,2):
            nrow = 0
            ncol = col + C2
            ndir = DOWN # down to down
            if face(nrow, ncol) != 2: print("PANIC 6,2", in_face, face(nrow, ncol))
    # print(row, col, nrow, ncol, in_face, new_face, face(nrow, ncol))
    char = grid[nrow][ncol]
    if char == WALL:
        return ((row, col), dir, True)
    if char == OPEN:
        return ((nrow, ncol), ndir, False)
    
    print("PANIC: we are not on the cube anymore")


def face(row, col):
    # this is specific to my puzzle input, it does not match the test input
    # it is also based on my arbitrary face numbering
    # the tuples in or outside the grid are the invalid location that
    # transport you to a different face, usually it is (from,to),
    # but both (3,4), (2,3) and (5,6) are two way, so we need the starting face
    #
    #      -1     0     1     2     3
    #  -1             (1,6) (2,6)
    #   0       (1,4)   1     2   (2,5)
    #   1       (3,4)   3   (2,3)
    #   2 (4,1)   4     5   (5,2)
    #   3 (6,1)   6   (5,6)   x
    #   4       (6,2)
    #
    # where each face is 50x50 and row and columns indices start at 0

    if row < R0:
        if col < C1:
            return None
        if col < C2:
            return (1, 6)
        if  col < C3:
            return (2, 6)
        return None

    if row < R1:
        if col < C0:
            return None
        if col < C1:
            return (1,4)
        if col < C2:
            return 1
        if col < C3:
            return 2
        return (2,5)

    if row < R2:
        if col < C0:
            return None
        if col < C1:
            return (3,4)
        if col < C2:
            return 3
        if col < C3:
            return (2,3)
        return None

    if row < R3:
        if col < C0:
            return (4,1)
        if col < C1:
            return 4
        if col < C2:
            return 5
        if col < C3:
            return (5,6)
        return None

    if row < R4:
        if col < C0:
            return (6,1)
        if col < C1:
            return 6
        if col < C2:
            return (5,6)
        return None

    # Row 4 or higher:
    if col < C0:
        return None
    if col < C1:
        return (6,2)
    return None


def inside(grid, row, col):
    return row >= 0 and row < len(grid) and col >= 0 and col < len(grid[row])    


def change_direction(dir, turn):
    if turn == "R":
        if dir == UP:
            return RIGHT
        if dir == RIGHT:
            return DOWN
        if dir == DOWN:
            return LEFT
        if dir == LEFT:
            return UP  
    if turn == "L":
        if dir == UP:
            return LEFT
        if dir == LEFT:
            return DOWN
        if dir == DOWN:
            return RIGHT
        if dir == RIGHT:
            return UP
    return dir


def password(loc, dir):
    """The final password is the sum of 1000 times the row,
    4 times the column, and the facing.
    col and rows start at 1 and increase to the right and down respectively.
    0 for right (>), 1 for down (v), 2 for left (<), and 3 for up."""
    row, col = loc
    result = 1000 * (row + 1) + 4 * (col + 1)
    if dir == DOWN:
        return result + 1
    if dir == LEFT:
        return result + 2
    if dir == UP:
        return result + 3
    return result


if __name__ == '__main__':
    lines = open("input.txt").readlines()
    print(f"Part 1: {part1(lines)}")
    print(f"Part 2: {part2(lines)}")

# This code works on the sample, but fails on the real puzzle.
# my answer: 190056 is too high