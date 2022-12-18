# Data Model:
# ===========
# lines is a list of "\n" terminated strings from the input file


def part1(lines):
    data = parse(lines)
    # data = [(1,1,1), (2,1,1)] # testg data; result should be 10
    result = solve(data)
    return result


def part2(lines):
    return -1


def parse(lines):
    data = []
    for line in lines:
        line = line.strip()
        items = line.split(",")
        x,y,z = int(items[0]), int(items[1]), int(items[2])
        data.append((x,y,z))
    return data


def solve(data):
    result = 0
    for drop in data:
        result += exposed(drop, data)
    return result


def exposed(drop, drops):
    x,y,z = drop
    exposed = 6
    for other in drops:
        x1,y1,z1 = other
        if y1 == y and z1 == z and (x1 == x+1 or x1 == x-1):
            exposed -= 1
        elif x1 == x and z1 == z and (y1 == y+1 or y1 == y-1):
            exposed -= 1
        elif x1 == x and y1 == y and (z1 == z+1 or z1 == z-1):
            exposed -= 1
    return exposed


if __name__ == '__main__':
    lines = open("input.txt").readlines()
    print(f"Part 1: {part1(lines)}")
    print(f"Part 2: {part2(lines)}")
