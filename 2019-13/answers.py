import sys
from computer import Computer

def number_block_tiles(code):
    return 0
    
if __name__ == '__main__':
    program = [int(x) for x in sys.stdin.read().split(',')]
    answer = number_block_tiles(program)
    print("Part 1: {0}".format(answer))
