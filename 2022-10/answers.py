# Data Model:
# ===========
# lines is a list of "\n" terminated strings from the input file


def part1(lines):
    data = parse(lines)
    # print(data)
    x = 1
    cycles = [20, 60, 100, 140, 180, 220]
    result = solve(data, x, cycles)
    return result


def part2(lines):
    data = parse(lines)
    # result = solve(data)
    # return result


def parse(lines):
    data = []
    for line in lines:
        line = line.strip()
        if line == "noop":
            data.append(None)
        else:
            _, val = line.split()
            data.append(int(val))
    return data


def solve(data, x, cycles):
    xs = [x]
    for item in data:
        if item:
            xs.append(x)
            x += item
            xs.append(x)
        else:
            xs.append(x)
    # print(xs)
    signals = [cycle * xs[cycle - 1] for cycle in cycles]
    return sum(signals)


if __name__ == '__main__':
    lines = open("input.txt").readlines()
    print(f"Part 1: {part1(lines)}")
    print(f"Part 2: {part2(lines)}")
