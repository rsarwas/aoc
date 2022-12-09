# Data Model:
# ===========
# lines is a list of "\n" terminated strings from the input file


def part1(lines):
    data = parse(lines)
    result = solve(data)
    return result


def part2(lines):
    data = parse(lines)
    result = solve(data)
    return result


def parse(lines):
    data = []
    for line in lines:
        line = line.strip()
        item = line.split()
        data.append(item)
    return data


def solve(data):
    result = 0
    for item in data:
        result += len(item)
    return result


if __name__ == '__main__':
    lines = open("test.txt").readlines()
    print(f"Part 1: {part1(lines)}")
    print(f"Part 2: {part2(lines)}")
