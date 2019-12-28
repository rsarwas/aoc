import sys
from computer import Computer

def solve(intcode):
    def is_intersections(scaffold, index, platform, nchars):
        if scaffold[index] != platform:
            return False
        if scaffold[index-1] != platform:
            return False
        if scaffold[index+1] != platform:
            return False
        if scaffold[index-nchars] != platform:
            return False
        if scaffold[index+nchars] != platform:
            return False
        return True
    computer = Computer(intcode)
    computer.start()
    scaffold = computer.get_and_clear_output()
    # scaffold_string = ''.join([chr(a) for a in scaffold])
    # print(scaffold_string)
    # From inspecting the printed scaffold:
    nlines = 33
    nchars = 52 # includes the newline (13)
    platform = 35
    sum_of_locations = 0
    for line in range(1, nlines-1):
        for char in range(1, nchars-1):
            index = line*nchars + char
            if scaffold[index] == platform:
                if is_intersections(scaffold, index, platform, nchars):
                    # print((line, char))
                    sum_of_locations += line * char
    return sum_of_locations

def main():
    program = [int(x) for x in sys.stdin.read().split(',')]
    answer = solve(program)
    print("Part 1: {0}".format(answer))

if __name__ == '__main__':
    main()
