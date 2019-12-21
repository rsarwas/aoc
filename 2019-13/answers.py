import sys
from computer import Computer

EMPTY = 0
WALL = 1
BLOCK = 2
PADDLE = 3
BALL = 4

CHARS = [' ','#','+','_','o']

# The screen size was determined by analyzing output from the test run
# Assume that the arcade console sceen does not change.
NLINES = 21
NCOLS = 35

def draw_screen(screen):
    for line in format(screen):
        print(line)

def format(screen):
    """
    # This is only needed the first time to see how big the screen is
    maxx, maxy = 0,0
    for coords in screen:
        maxx = max(coords[0], maxx)
        maxy = max(coords[1], maxy)
    nchar = 1 + maxx
    nlines = 1 + maxy
    print(nlines,nchar)
    """
    # set it all to empty
    list_matrix = [list(CHARS[EMPTY]*NCOLS) for _ in range(NLINES)]
    for coords in screen:
        list_matrix[coords[1]][coords[0]] = CHARS[screen[coords]]
    char_matrix = [''.join(l) for l in list_matrix]
    return char_matrix

def build_screen(data):
    i = 0
    screen = {}
    while i < len(data):
        x = data[i]
        y = data[i+1]
        cmd = data[i+2]
        i += 3
        screen[(x,y)] = cmd
    return screen

def number_block_tiles(code):
    c = Computer(code)
    c.start()
    draw_instructions = c.copy_output()
    screen = build_screen(draw_instructions)
    draw_screen(screen)
    # Count blocks in FINAL screen state, not how many times I drew a block.
    # This may be the same, but I'm not sure if the the draw instructions will
    # over draw a tile, i.e. draw a block at (1,1), then draw a ball at (1,1)
    counter = 0
    for coords in screen:
        if screen[coords] == BLOCK:
            counter += 1
    return counter
    
if __name__ == '__main__':
    program = [int(x) for x in sys.stdin.read().split(',')]
    answer = number_block_tiles(program)
    print("Part 1: {0}".format(answer))
