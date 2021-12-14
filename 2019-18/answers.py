import sys

NCOL = 81
NROW = 81
OPEN = 46
WALL = 35

def encode_maze(maze):
    global NROW
    NROW = len(maze)
    global NCOL
    NCOL = len(maze[0].strip())

    int_maze = []
    for line in maze:
        line_as_int = [ord(a) for a in line.strip()]
        int_maze.append(line_as_int)
    # print('rows', len(int_maze), 'cols', len(int_maze[0]))
    return int_maze

def fill_dead_ends(maze):

    def is_dead_end(maze, row, col, doors):
        if doors:
            # is open or a doorr 'A' to 'Z'
            tile = maze[row][col]
            open_or_door = tile == OPEN or (tile >= ord('A') and tile <= ord('Z'))
            if not open_or_door:
                return
        else:
            # is open
            if maze[row][col] != OPEN:
                return False
        # and has three adjacent walls
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

    def fill_dead_end(maze, row, col, fill_doors=False):
        while is_dead_end(maze, row, col, fill_doors):
            maze[row][col] = WALL
            row, col = open_tile(maze, row, col)

    def open_tile(maze, row, col):
        if maze[row-1][col] != WALL:
            return row-1, col
        if maze[row+1][col] != WALL:
            return row+1, col
        if maze[row][col-1] != WALL:
            return row, col-1
        if maze[row][col+1] != WALL:
            return row, col+1

    # skip exterior walls; fill only open spaces at dead ends
    for row in range(1, NROW-1):
        for col in range(1, NCOL-1):
            fill_dead_end(maze, row, col)

    # skip walls, ignore (fill) a door at a deadend; we do not need to open that door
    for row in range(1, NROW-1):
        for col in range(1, NCOL-1):
            fill_dead_end(maze, row, col, fill_doors=True)

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


def print_maze(maze):
    for row in maze:
        row_as_char = ''.join([chr(a) for a in row])
        print(row_as_char.replace('#', ' '))

def main():
    char_maze = sys.stdin.readlines()
    int_maze = encode_maze(char_maze)
    fill_dead_ends(int_maze)
    find_intersections(int_maze)
    print_maze(int_maze)
    # answer = solve(program)
    # print("Part 1: {0}".format(answer))

if __name__ == '__main__':
    main()
