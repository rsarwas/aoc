# Data Model:
# ===========
# lines is a list of "\n" terminated strings from the input file
# 

def part1(lines):
    return -1

def part2(lines):
    return -1

if __name__ == '__main__':
    # data = open("input.txt").read() # as one big string
    lines = open("test.txt").readlines() # as a list of line strings
    # lines = open("input.txt").readlines() # as a list of line strings
    print(f"Part 1: {part1(lines)}")
    print(f"Part 2: {part2(lines)}")
