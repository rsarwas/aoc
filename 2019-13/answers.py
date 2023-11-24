import sys
from computer import Computer

EMPTY = 0
WALL = 1
BLOCK = 2
PADDLE = 3
BALL = 4

CHARS = [" ", "#", "+", "_", "o"]

# The screen size was determined by analyzing output from the test run
# Assume that the arcade console sceen does not change.
NLINES = 21
NCOLS = 35

PADDLE_LEFT = -1
PADDLE_HOME = 0
PADDLE_RIGHT = 1

# Global State
Score = None
ball_x = 0
x_dir = 0  # new x - old x; + to right, - = to left; 0 is impossible
wait = True  # wait for the ball to hit the paddle (about 4 turns)
Screen = [EMPTY] * NLINES * NCOLS


def play(game):
    game[0] = 2  # put a quarter into the arcade
    c = Computer(game)
    status = c.start()
    update_screen(c.get_and_clear_output())
    # draw_screen()
    # print_score()
    while status != Computer.DONE:
        move = get_paddle_move()
        # print(ball_x, x_dir, move)
        c.push_input(move)
        status = c.resume()
        update_screen(c.get_and_clear_output())
        # draw_screen()
        # print_score()
    print_score()


def get_paddle_move():
    global wait
    # Analyze screen to figure out how to move paddle
    # wait until the ball gets to the paddle, and then move
    # the paddle with the ball
    if wait:
        if ball_x < 18:
            return PADDLE_HOME
        else:
            # ball_x = 17 and stop waiting
            wait = False
    return x_dir  # x_dir = +1 moving to right == PADDLE_RIGHT


def draw_screen():
    for line in format_screen():
        print(line)


def print_score():
    blocks = 0
    ball = (0, 0)
    paddle = (0, 0)
    for i, pixel in enumerate(Screen):
        if pixel == BLOCK:
            blocks += 1
        if pixel == BALL:
            ball = (i % NCOLS, i // NCOLS)
        if pixel == PADDLE:
            paddle = (i % NCOLS, i // NCOLS)
    if Score is not None:
        print(
            "Score = {0}; Blocks = {1}, Ball = {2}, PADDLE = {3}".format(
                Score, blocks, ball, paddle
            )
        )


def format_screen():
    list_matrix = [list(CHARS[EMPTY] * NCOLS) for _ in range(NLINES)]
    for i, pixel in enumerate(Screen):
        y = i // NCOLS
        x = i % NCOLS
        list_matrix[y][x] = CHARS[pixel]
    char_matrix = ["".join(l) for l in list_matrix]
    return char_matrix


def update_screen(data):
    global Score
    global ball_x, x_dir
    # Score = None
    i = 0
    while i < len(data):
        x = data[i]
        y = data[i + 1]
        cmd = data[i + 2]
        if cmd == BALL:
            x_dir = x - ball_x
            ball_x = x
        i += 3
        if x == -1 and y == 0:
            Score = cmd
        else:
            Screen[NCOLS * y + x] = cmd


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


if __name__ == "__main__":
    program = [int(x) for x in sys.stdin.read().split(",")]
    answer = number_block_tiles(program)
    print("Part 1: {0}".format(answer))
    play(program)
