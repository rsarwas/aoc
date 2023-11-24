def part1(lines):
    d = 0
    x = 0
    for line in lines:
        dir, dist = line.split()
        if dir == "forward":
            x += int(dist)
        elif dir == "up":
            d -= int(dist)
        elif dir == "down":
            d += int(dist)
        else:
            print(f"akk! unknown dir {dir} and {dist}")
    return x * d


def part2(lines):
    d = 0
    x = 0
    aim = 0
    for line in lines:
        dir, dist = line.split()
        if dir == "forward":
            x += int(dist)
            d += int(dist) * aim
        elif dir == "up":
            aim -= int(dist)
        elif dir == "down":
            aim += int(dist)
        else:
            print(f"akk! unknown dir {dir} and {dist}")
    return x * d


if __name__ == "__main__":
    # data = open("input.txt").read() # as one big string
    lines = open("input.txt").readlines()  # as a list of line strings
    print(f"Part 1: {part1(lines)}")
    print(f"Part 2: {part2(lines)}")
