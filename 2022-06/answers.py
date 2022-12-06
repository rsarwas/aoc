# Data Model:
# ===========
# lines is a list of "\n" terminated strings from the input file
# there is only one line and it ia a random sequence of characters


def part1(lines):
    buffer = list(lines[0])
    for i in range(len(buffer)-4):
        group = set(buffer[i:i+4])
        if len(group) == 4:
            return i+4
    return -1


def part2(lines):
    buffer = list(lines[0])
    for i in range(len(buffer)-14):
        group = set(buffer[i:i+14])
        if len(group) == 14:
            return i+14
    return -1


if __name__ == '__main__':
    lines = open("input.txt").readlines()
    print(f"Part 1: {part1(lines)}")
    print(f"Part 2: {part2(lines)}")
