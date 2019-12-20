import sys
from computer import Computer

def robot(code):
    c = Computer(code)
    c.push_input(0)
    c.start()
    return c.pop_output()
    
if __name__ == '__main__':
    program = [int(x) for x in sys.stdin.read().split(',')]
    answer = robot(program)
    print("Part 1: {0}".format(answer))
