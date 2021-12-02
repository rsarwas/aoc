def part1(lines):
    return sum([int(line) for line in lines])

def part2(lines):
    return -1

if __name__ == '__main__':
    # data = open("input.txt").read() # as one big string
    lines = open("input.txt").readlines() # as a list of line strings
    print(f"Part 1: {part1(lines)}")
    print(f"Part 2: {part2(lines)}")
