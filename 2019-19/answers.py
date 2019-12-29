import sys
from computer import Computer

def solve(intcode):
    # Simple brute force solution
    # we could print the 10 by 10 results to see if there is a cone pattern
    # and limit the edges of the cone, but this is just too easy.

    # While not stated clearly in the instructions, the program halts after
    # creating the output.  It cannot be resumed.  It can also not be restarted
    # I need to "reload" the int code for each run.

    total = 0
    for x in range(50):
        for y in range(50):
            computer = Computer(intcode)
            computer.push_input(y)
            computer.push_input(x)
            computer.start()
            output = computer.pop_output()
            if output == 1:
                total += 1
            # print(x, y, output, total)
    return total

def main():
    program = [int(x) for x in sys.stdin.read().split(',')]
    answer = solve(program)
    print("Part 1: {0}".format(answer))

if __name__ == '__main__':
    main()
