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

PADDLE_LEFT = -1
PADDLE_HOME = 0
PADDLE_RIGHT = 1

# Global State
Score = None
Screen = [EMPTY]*NLINES*NCOLS

def play(game):
    game[0] = 2  # put a quarter into the arcade
    c = Computer(game)
    status = c.start()
    update_screen(c.get_and_clear_output())
    # draw_screen()
    # print_score()
    while status != Computer.DONE:
        move = get_paddle_move()
        c.push_input(move)
        status = c.resume()
        update_screen(c.get_and_clear_output())
        # draw_screen()
        # print_score()

def get_paddle_move():
    # Analyze screen to figure out how to move paddle
    return PADDLE_HOME

def draw_screen():
    for line in format_screen():
        print(line)

def print_score():
    if Score is not None:
        print("Score = {0}".format(Score))

def format_screen():
    list_matrix = [list(CHARS[EMPTY]*NCOLS) for _ in range(NLINES)]
    for i, pixel in enumerate(Screen):
        y = i // NCOLS
        x = i % NCOLS
        list_matrix[y][x] = CHARS[pixel]
    char_matrix = [''.join(l) for l in list_matrix]
    return char_matrix

def update_screen(data):
    global Score
    Score = None
    i = 0
    while i < len(data):
        x = data[i]
        y = data[i+1]
        cmd = data[i+2]
        i += 3
        if x == -1 and y == 0:
            Score = cmd
        else:
            Screen[NCOLS*y + x] = cmd

def number_block_tiles(code):
    c = Computer(code)
    c.start()
    draw_instructions = c.copy_output()
    update_screen(draw_instructions)
    # draw_screen()
    # Count blocks in FINAL screen state, not how many times I drew a block.
    # This may be the same, but I'm not sure if the the draw instructions will
    # over draw a tile, i.e. draw a block at (1,1), then draw a ball at (1,1)
    counter = 0
    for pixel in Screen:
        if pixel == BLOCK:
            counter += 1
    return counter
    
if __name__ == '__main__':
    program = [int(x) for x in sys.stdin.read().split(',')]
    answer = number_block_tiles(program)
    print("Part 1: {0}".format(answer))
    play(program)
