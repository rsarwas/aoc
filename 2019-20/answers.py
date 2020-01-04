import sys

COL0 = 3
ROW0 = 3
NCOL = 115
NROW = 123
OPEN = ord('.')
WALL = ord(' ')

def encode_maze(maze):
    int_maze = []
    for line in maze:
        line_as_int = [ord(a) for a in line]
        int_maze.append(line_as_int)
    # print('rows', len(int_maze), 'cols', len(int_maze[0]))
    return int_maze

def open_tile(maze, row, col):
    if maze[row-1][col] != WALL:
        return row-1, col
    if maze[row+1][col] != WALL:
        return row+1, col
    if maze[row][col-1] != WALL:
        return row, col-1
    if maze[row][col+1] != WALL:
        return row, col+1
    return None, None

def fill_dead_ends(maze):

    def is_dead_end(maze, row, col):
        # must be open and have three adjacent walls
        if maze[row][col] != OPEN:
            return False
        count = 0
        if maze[row-1][col] == WALL:
            count += 1
        if maze[row+1][col] == WALL:
            count += 1
        if maze[row][col-1] == WALL:
            count += 1
        if maze[row][col+1] == WALL:
            count += 1
        return count == 3

    def fill_dead_end(maze, row, col):
        while is_dead_end(maze, row, col):
            maze[row][col] = WALL
            row, col = open_tile(maze, row, col)


    # skip exterior walls; fill only open spaces at dead ends
    for row in range(ROW0, NROW-1):
        for col in range(COL0, NCOL-1):
            fill_dead_end(maze, row, col)

def find_intersections(maze):

    def has_three_open(maze, row, col):
        if maze[row][col] != OPEN:
            return False
        # and has three open tiles adjacent
        # We are ignoring the starting position, but by examination this doesn't matter
        count = 0
        if maze[row-1][col] == OPEN:
            count += 1
        if maze[row+1][col] == OPEN:
            count += 1
        if maze[row][col-1] == OPEN:
            count += 1
        if maze[row][col+1] == OPEN:
            count += 1
        return count == 3

    # skip exterior walls
    for row in range(1, NROW-1):
        for col in range(1, NCOL-1):
            if has_three_open(maze, row, col):
                maze[row][col] = ord('+')
                print('intersection', row, col)

def measure_segments(int_maze):
    lengths = {}
    for col in [1, 115]:
        for row in range(37, 88):
            if int_maze[row][col] != ord(' '):
                walk_path(lengths, int_maze, row, col)
    for row in [1, 123]:
        for col in range(35, 83):
            if int_maze[row][col] != ord(' '):
                walk_path(lengths, int_maze, row, col)
    row, col = 91, 57  # 7 to +
    walk_path(lengths, int_maze, row, col)
    row, col = 63, 33  # L to +
    walk_path(lengths, int_maze, row, col)
    row, col = 33, 59  # 6 to +
    walk_path(lengths, int_maze, row, col)
    row, col = 33, 65  # M to +
    walk_path(lengths, int_maze, row, col)

    return lengths

def walk_path(lengths, int_maze, row, col):
    # print(row, col, chr(int_maze[row][col]))
    start = int_maze[row][col]
    length = 0
    int_maze[row][col] = WALL
    row, col = open_tile(int_maze, row, col)
    end = int_maze[row][col]
    while end == OPEN:
        length += 1
        int_maze[row][col] = WALL
        row, col = open_tile(int_maze, row, col)
        end = int_maze[row][col]
    # These lengths include the portal jump at the beginning
    lengths[chr(start) + chr(end)] = length

def part1_length(lengths, solution):
    # print(lengths)
    length = 0
    for segment in solution:
        length += lengths[segment]
    length += 3  # legs with a plus do not inlcude the portal jump
    length -= 1  # suptract the first portal (at the start)
    return length

def print_maze(maze):
    for row in maze:
        row_as_char = ''.join([chr(a) for a in row])
        # print(row_as_char, end='')
        print(row_as_char.replace('#', ' '), end='')

def main():
    char_maze = sys.stdin.readlines()
    int_maze = encode_maze(char_maze)
    # Do the following with the original input
    #fill_dead_ends(int_maze)
    #find_intersections(int_maze)
    # print_maze(int_maze)
    # do this on the output from above, with the end points
    # replaced with single codes (input2.txt)
    lengths = measure_segments(int_maze)
    lengths['++'] = 36
    solution = [
        '1+', '7+', '78', '89', '9+', '++', 'M+', 'MN', 'NO', 'OP', 'PQ', 'QR', 'RS', 'T+', 'S+'
    ]
    length = part1_length(lengths, solution)
    print("Part 1: {0}".format(length))

if __name__ == '__main__':
    main()
