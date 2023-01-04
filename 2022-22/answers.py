"""A solution to an Advent of Code puzzle."""

# Data Model:
# ===========
# lines is a list of "\n" terminated strings from the input file
# instructions is a list of (int, char) tuples, where char is a turn
# direction in {"L", "R"}, where "R" is clockwise
# grid is a list of strings. Each string is a row.  The characters in the string are
# in the set {" ", ".", "#"} for {VOID, OPEN, WALL}.

# movement directions are given by a tuple of row,col deltas
# i.e right is (0, 1) meaning row number stay the same, and col index advances by 1

import os.path  # to get the directory name of the script (current puzzle year-day)

INPUT = "input.txt"

UP = (-1, 0)
DOWN = (1, 0)
LEFT = (0, -1)
RIGHT = (0, 1)

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
    """Solve part 1 of the puzzle."""
    grid, instructions = parse(lines)
    # print(grid)
    # print(instructions)
    end, direction = process(grid, instructions)
    result = password(end, direction)
    return result


def part2(lines):
    """Solve part 2 of the puzzle."""
    if INPUT == "test.txt":
        return "Not implemented"
    # pylint: disable=global-statement
    global PART
    PART = 2
    return part1(lines)


def parse(lines):
    """Parse the puzzle input file into a usable data structure."""
    grid = []
    instructions = []
    for line in lines:
        if line == "\n":
            continue
        if line[0] in [VOID, OPEN, WALL]:
            grid.append(line.replace("\n", ""))
        else:
            line = line.strip()
            start = 0
            end = 1
            while end < len(line):
                if line[end] in "LR":
                    dist = int(line[start:end])
                    instructions.append((dist, line[end]))
                    start = end + 1
                    end = start + 1
                else:
                    end += 1
            dist = int(line[start:])
            instructions.append((dist, None))
    return grid, instructions


def process(grid, instructions):
    """Execute the list of instructions on the grid."""
    location = find_start(grid)
    direction = RIGHT
    for instruction in instructions:
        location, direction = move(grid, location, direction, instruction)
    return location, direction


def find_start(grid):
    """Search the grid for the coordinates of the starting location."""
    row = 0
    for col, char in enumerate(grid[row]):
        if char == OPEN:
            return (row, col)
    return None


def move(grid, location, direction, instruction):
    """Given a location and direction on the grid execute the instruction.
    return the final location and direction."""
    dist, turn = instruction
    # print("Start  at", location, "Heading", p_dir(direction), " Move", dist, "Turn", turn, "\n")
    location, direction = march(grid, location, direction, dist)
    direction = change_direction(direction, turn)
    # print("\nFinish at", location, "Heading", p_dir(direction))
    return location, direction


def march(grid, location, direction, dist):
    """Proceed in a straight line (on the face of the cube for part2) for a distance dist."""
    if dist == 0:
        return location, direction
    location, direction, wall = next_space(grid, location, direction)
    step = 1
    while step < dist and not wall:
        location, direction, wall = next_space(grid, location, direction)
        step += 1
    return location, direction


def next_space(grid, location, direction):
    """finds the next valid space to move to
    handles grid edge conditions wrap around
    and empty cells.  ONLY WORKS WITH PART 1"""

    # In part2 of the puzzle we use a different method to find the next location (and direction)
    if PART == 2:
        return next_space2(grid, location, direction)

    row, col = location
    delta_row, delta_col = direction
    # print(row,col,delta_row,delta_col)
    new_row, new_col = row + delta_row, col + delta_col
    safety_valve = 0
    while safety_valve < 200:
        safety_valve += 1
        # print(new_row, new_col)
        if inside(grid, new_row, new_col):
            char = grid[new_row][new_col]
            # print(char)
            if char == WALL:
                return ((row, col), direction, True)
            if char == OPEN:
                return ((new_row, new_col), direction, False)
            # char must be VOID, advance until we wrap or hit a non-VOID space
            new_row, new_col = new_row + delta_row, new_col + delta_col
        else:
            # need to wrap around; Usually it can only hit one edge at a time
            # but some rows are shorter than others, so when going up or down,
            # we may find ourselves in a valid row, but beyond it's length
            if delta_row == 1 and new_row >= len(grid):
                new_row = 0
            if delta_col == 1 and new_col >= len(grid[new_row]):
                new_col = 0
            if delta_row == -1 and new_row < 0:
                new_row = len(grid) - 1
            if delta_col == -1 and new_col < 0:
                new_col = len(grid[new_row]) - 1
            if delta_row != 0 and new_col >= len(grid[new_row]):
                new_row = new_row + delta_row
    print("PANIC! Unable to find next space to move to")
    return None, None


def next_space2(grid, location, direction):
    """finds the next valid space to move to
    handles grid edge conditions wrap around
    and empty cells.  ONLY WORKS WITH PART 2"""
    row, col = location
    delta_row, delta_col = direction
    new_row, new_col = row + delta_row, col + delta_col
    new_direction = direction

    in_face = face(row, col)
    new_face = face(new_row, new_col)

    if new_face is None:
        print("PANIC: I ended up off the cube")
        return -1

    if isinstance(new_face, int):
        # the new location is on a valid cube face
        pass
    else:
        # we have walked off the cube, and need to recalibrate to the new face:
        new_row, new_col, new_direction = recalibrate(row, col, in_face, new_face)
    char = grid[new_row][new_col]
    if char == WALL:
        # debug printing
        # if isinstance(new_face, int):
        #     print(f"   WALL at {new_face}({new_row},{new_col})")
        # else:
        #     print(f" * WALL at {new_face} aka {face(new_row, new_col)} ({new_row}, {new_col})")
        return ((row, col), direction, True)
    if char == OPEN:
        # debug printing
        # start = f"{in_face}({row},{col}) {p_dir(direction)}"
        # if isinstance(new_face, int):
        #     end = f"{new_face}({new_row},{new_col}) {p_dir(new_direction)}"
        #     print(f"   at {start} => {end}")
        # else:
        #     end1 = f"{new_face} aka {face(new_row, new_col)}"
        #     end2 = f"({new_row},{new_col}) {p_dir(new_direction)}"
        #     print(f" * at {start} => {end1}{end2}")
        return ((new_row, new_col), new_direction, False)

    print("PANIC: we are not on the cube anymore")
    return -1


def recalibrate(row, col, in_face, new_face):
    """Used to move the location and direction from one face to another.
    NOTE: This is specific for the cube layout in _MY_ puzzle input, which
    is different than the cube layout in the sample problem.  See face()."""
    # pylint: disable=too-many-branches, too-many-statements
    if new_face == (1, 6):
        new_row = col - R1 + C3
        new_col = 0
        new_direction = RIGHT  # up to right
        if face(new_row, new_col) != 6:
            print("PANIC 1,6", in_face, face(new_row, new_col))
    elif new_face == (2, 6):
        new_row = R4 - 1
        new_col = col - C2
        new_direction = UP  # up to up
        if face(new_row, new_col) != 6:
            print("PANIC 2,6", in_face, face(new_row, new_col))
    elif new_face == (1, 4):
        new_row = (R3 - 1) - row  # 0 -> 149; 49 -> 100
        new_col = 0
        new_direction = RIGHT  # left to right
        if face(new_row, new_col) != 4:
            print("PANIC 1,4", in_face, face(new_row, new_col))
    elif new_face == (2, 5):
        new_row = (R3 - 1) - row  # 0 -> 149; 49 -> 100
        new_col = C2 - 1
        new_direction = LEFT  # right to left
        if face(new_row, new_col) != 5:
            print("PANIC 2,5", in_face, face(new_row, new_col))
    elif new_face == (3, 4) and in_face == 3:
        new_row = R2
        new_col = row - R1
        new_direction = DOWN  # left to down
        if face(new_row, new_col) != 4:
            print("PANIC 3->4", in_face, face(new_row, new_col))
    elif new_face == (3, 4) and in_face == 4:
        new_row = col + R1
        new_col = C1
        new_direction = RIGHT  # up to right
        if face(new_row, new_col) != 3:
            print("PANIC 4->3", in_face, face(new_row, new_col))
    elif new_face == (2, 3) and in_face == 2:
        new_row = R1 + col - C2
        new_col = C2 - 1
        new_direction = LEFT  # down to left
        if face(new_row, new_col) != 3:
            print("PANIC 2->3", in_face, face(new_row, new_col))
    elif new_face == (2, 3) and in_face == 3:
        new_row = R1 - 1
        new_col = row - R1 + C2
        new_direction = UP  # right to up
        if face(new_row, new_col) != 2:
            print("PANIC 3->2", in_face, face(new_row, new_col))
    elif new_face == (4, 1):
        new_row = (R3 - 1) - row  # 100 -> 49; 149 -> 0
        new_col = C1
        new_direction = RIGHT  # left to right
        if face(new_row, new_col) != 1:
            print("PANIC 4,1", in_face, face(new_row, new_col))
    elif new_face == (5, 2):
        new_row = (R3 - 1) - row  # 100 -> 49; 149 -> 0
        new_col = C3 - 1
        new_direction = LEFT  # right to left
        if face(new_row, new_col) != 2:
            print("PANIC 5,2", in_face, face(new_row, new_col))
    elif new_face == (6, 1):
        new_row = 0
        new_col = row - R3 + C1
        new_direction = DOWN  # left to down
        if face(new_row, new_col) != 1:
            print("PANIC 6,1", in_face, face(new_row, new_col))
    elif new_face == (5, 6) and in_face == 5:
        new_row = col - C1 + R3
        new_col = C1 - 1
        new_direction = LEFT  # down to left
        if face(new_row, new_col) != 6:
            print("PANIC 5->6", in_face, face(new_row, new_col))
    elif new_face == (5, 6) and in_face == 6:
        new_row = R3 - 1
        new_col = row - R3 + C1
        new_direction = UP  # right to up
        if face(new_row, new_col) != 5:
            print("PANIC 6->5", in_face, face(new_row, new_col))
    elif new_face == (6, 2):
        new_row = 0
        new_col = col + C2
        new_direction = DOWN  # down to down
        if face(new_row, new_col) != 2:
            print("PANIC 6,2", in_face, face(new_row, new_col))
    return new_row, new_col, new_direction


def face(row, col):
    """Return the face id (1-6) for a given location.

    This is specific to my puzzle input, it does not match the test input
    it is also based on my arbitrary face numbering
    the tuples in or outside the grid are the invalid location that
    transport you to a different face, usually it is (from,to),
    but both (3,4), (2,3) and (5,6) are two way, so we need the starting face

         -1     0     1     2     3
     -1             (1,6) (2,6)
      0       (1,4)   1     2   (2,5)
      1       (3,4)   3   (2,3)
      2 (4,1)   4     5   (5,2)
      3 (6,1)   6   (5,6)   x
      4       (6,2)

    where each face is 50x50 and row and columns indices start at 0
    """
    # pylint: disable=too-many-branches, too-many-return-statements

    if row < R0:
        if col < C1:
            return None
        if col < C2:
            return (1, 6)
        if col < C3:
            return (2, 6)
        return None

    if row < R1:
        if col < C0:
            return None
        if col < C1:
            return (1, 4)
        if col < C2:
            return 1
        if col < C3:
            return 2
        return (2, 5)

    if row < R2:
        if col < C0:
            return None
        if col < C1:
            return (3, 4)
        if col < C2:
            return 3
        if col < C3:
            return (2, 3)
        return None

    if row < R3:
        if col < C0:
            return (4, 1)
        if col < C1:
            return 4
        if col < C2:
            return 5
        if col < C3:
            return (5, 2)
        return None

    if row < R4:
        if col < C0:
            return (6, 1)
        if col < C1:
            return 6
        if col < C2:
            return (5, 6)
        return None

    # Row 4 or higher:
    if col < C0:
        return None
    if col < C1:
        return (6, 2)
    return None


def inside(grid, row, col):
    """Return True if (row, col) is in the grid."""
    return 0 <= row < len(grid) and 0 <= col < len(grid[row])


def change_direction(direction, turn):
    """Return the new direction."""
    # pylint: disable=too-many-return-statements
    if turn == "R":
        if direction == UP:
            return RIGHT
        if direction == RIGHT:
            return DOWN
        if direction == DOWN:
            return LEFT
        if direction == LEFT:
            return UP
    if turn == "L":
        if direction == UP:
            return LEFT
        if direction == LEFT:
            return DOWN
        if direction == DOWN:
            return RIGHT
        if direction == RIGHT:
            return UP
    return direction


def password(location, direction):
    """The final password is the sum of 1000 times the row,
    4 times the column, and the facing.
    col and rows start at 1 and increase to the right and down respectively.
    0 for right (>), 1 for down (v), 2 for left (<), and 3 for up."""
    row, col = location
    result = 1000 * (row + 1) + 4 * (col + 1)
    # RIGHT + 0
    if direction == DOWN:
        return result + 1
    if direction == LEFT:
        return result + 2
    if direction == UP:
        return result + 3
    return result


def p_dir(direction):
    """Return the direction symbol (for debugging)"""
    if direction == UP:
        return "^"
    if direction == DOWN:
        return "v"
    if direction == RIGHT:
        return ">"
    if direction == LEFT:
        return "<"
    return ""


def test_face():
    """Print the face of various coordinates (for debugging)."""
    for row in [-1, 0, 49, 50, 99, 100, 149, 150, 199, 200]:
        print(row, end=" ")
        for col in [-1, 0, 49, 50, 99, 100, 149, 150]:
            print(face(row, col), end=" ")
        print("")


def main(filename):
    """Solve both parts of the puzzle."""
    _, puzzle = os.path.split(os.path.dirname(__file__))
    with open(filename, encoding="utf8") as data:
        lines = data.readlines()
    print(f"Solving Advent of Code {puzzle} with {filename}")
    print(f"Part 1: {part1(lines)}")
    print(f"Part 2: {part2(lines)}")


if __name__ == "__main__":
    # test_face()
    main(INPUT)
