import sys
from computer import Computer

BLOCK = 2

def number_block_tiles(code):
    c = Computer(code)
    c.start()
    draw_instructions = c.get_output()
    i = 0
    screen = {}
    while i < len(draw_instructions):
        x = draw_instructions[i]
        y = draw_instructions[i+1]
        cmd = draw_instructions[i+2]
        i += 3
        screen[(x,y)] = cmd
    counter = 0
    for coords in screen:
        if screen[coords] == BLOCK:
            counter += 1
    return counter
    
if __name__ == '__main__':
    program = [int(x) for x in sys.stdin.read().split(',')]
    answer = number_block_tiles(program)
    print("Part 1: {0}".format(answer))
