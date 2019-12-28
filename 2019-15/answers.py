import sys
from computer import Computer

def solve(intcode):
    computer = Computer(intcode)
    status = computer.start()
    return status

def main():
    program = [int(x) for x in sys.stdin.read().split(',')]
    answer = solve(program)
    print("Part 1: {0}".format(answer))

if __name__ == '__main__':
    main()
