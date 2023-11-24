def part1(lines):
    last_depth = 100000
    inc = 0
    for depth in [int(line) for line in lines]:
        if depth > last_depth:
            inc += 1
        last_depth = depth
    return inc


def part2(lines):
    last_depth = 100000
    inc = 0
    for i in range(0, len(lines) - 2):
        depth = int(lines[i]) + int(lines[i + 1]) + int(lines[i + 2])
        print(depth)
        if depth > last_depth:
            inc += 1
        last_depth = depth
    return inc


if __name__ == "__main__":
    # data = open("input.txt").read() # as one big string
    lines = open("input.txt").readlines()  # as a list of line strings
    print(f"Part 1: {part1(lines)}")
    print(f"Part 2: {part2(lines)}")
